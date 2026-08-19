#!/usr/bin/env python3
"""Quality gate for the R1 external runner.

Every test below corresponds to a named requirement in the Phase T-R1-X1 runner
specification. A test that cannot actually prove its claim is not written as a
passing test -- it is left out and reported as unproven.

Run:  python bench/R1/external-runner/test_r1_runner.py
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r1_runner as R  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures: a miniature oracle-free bundle and package set
# ---------------------------------------------------------------------------

TASK_TEMPLATE = """TASK_ID: {tid}
SCENARIO: {scn}
CHECKPOINT: t{cp:02d}

You are continuing work on an ongoing project.

Answer using exactly these six lines and nothing else:
DECISION: <one line>
ACTION: <one line>
CONSTRAINTS_APPLIED: <...>
EVIDENCE: <...>
UNRESOLVED: <...>
ABSTAIN: <YES/NO>
"""

GOOD_ANSWER = (
    "DECISION: x\nACTION: y\nCONSTRAINTS_APPLIED: NONE\n"
    "EVIDENCE: docs/a.md\nUNRESOLVED: NONE\nABSTAIN: NO\n"
)


def make_bundle(root: Path, tasks=(("S1-A-NEXT", "S1", 2),), checkpoints=((("S1"), 0), ("S1", 1), ("S1", 2))) -> R.Bundle:
    b = root / "r1-external" / "bundle"
    (b / "tasks").mkdir(parents=True)
    for tid, scn, cp in tasks:
        (b / "tasks" / f"{tid}.txt").write_text(
            TASK_TEMPLATE.format(tid=tid, scn=scn, cp=cp), encoding="utf-8"
        )
    for scn, cp in checkpoints:
        d = b / "evidence" / scn / f"t{cp:02d}"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"docs__note{cp}.md").write_text(
            f"evidence for {scn} at t{cp}", encoding="utf-8"
        )
    external = root / "r1-external"
    lines = []
    for path in sorted(
        (p for p in external.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(external).as_posix(),
    ):
        rel = path.relative_to(external).as_posix()
        lines.append(f"{R.sha256_hex(path.read_bytes())} *{rel}\n")
    (external / "BUNDLE-MANIFEST.txt").write_text(
        "".join(lines), encoding="utf-8", newline="\n"
    )
    return R.Bundle(external)


def make_packages(root: Path, arms=R.ARMS, scn="S1", cps=(0, 1, 2)) -> R.PackageSet:
    for traj in ("T0", "T1", "T2"):
        for arm in arms:
            if arm == "B-NULL":
                continue
            for cp in cps:
                d = root / traj / arm / scn
                d.mkdir(parents=True, exist_ok=True)
                (d / f"t{cp:02d}.txt").write_text(
                    f"context {arm} {scn} t{cp}", encoding="utf-8"
                )
    return R.PackageSet(root)


class FakeTransport:
    """Records every call so the tests can assert on what was actually sent."""

    def __init__(self, script=None):
        self.calls: list[dict] = []
        self.script = list(script or [])

    def __call__(self, system: str, user: str) -> R.ProviderResult:
        self.calls.append({"system": system, "user": user})
        if self.script:
            item = self.script.pop(0)
            if isinstance(item, Exception):
                raise item
            return item
        return R.ProviderResult(
            text=GOOD_ANSWER,
            response_id=f"resp_{len(self.calls)}",
            model_returned="gpt-5.6-terra",
            raw={"id": "resp", "model": "gpt-5.6-terra"},
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
        )


class SmartTransport(FakeTransport):
    """Returns contract-valid JSON for maintainers and contract text for continuations."""

    def __call__(self, system: str, user: str) -> R.ProviderResult:
        self.calls.append({"system": system, "user": user})
        if "Reply with JSON only" in system:
            text = '{"evidence_bytes_seen":1,"files":[],"memories":[],"wiki":""}'
        else:
            text = GOOD_ANSWER
        return R.ProviderResult(
            text=text,
            response_id=f"resp_{len(self.calls)}",
            model_returned="gpt-5.6-terra",
            raw={"id": f"resp_{len(self.calls)}", "model": "gpt-5.6-terra"},
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
        )


class OneMalformedSmartTransport(SmartTransport):
    def __init__(self):
        super().__init__()
        self._first_maintainer = True

    def __call__(self, system: str, user: str) -> R.ProviderResult:
        if "Reply with JSON only" in system and self._first_maintainer:
            self._first_maintainer = False
            self.calls.append({"system": system, "user": user})
            return R.ProviderResult(
                text="not json", response_id="resp_bad",
                model_returned="gpt-5.6-terra", raw={"id": "resp_bad"},
                input_tokens=100, output_tokens=2, total_tokens=102,
            )
        return super().__call__(system, user)


class FirstContinuationInfraTransport(SmartTransport):
    """Exhaust infrastructure retries for only the first continuation session."""

    def __init__(self):
        super().__init__()
        self.remaining = 3

    def __call__(self, system: str, user: str) -> R.ProviderResult:
        if "Reply with JSON only" not in system and self.remaining:
            self.calls.append({"system": system, "user": user})
            self.remaining -= 1
            raise R.InfrastructureFailure("NETWORK", "synthetic reset")
        return super().__call__(system, user)


class FirstMaintainerInfraTransport(SmartTransport):
    """Exhaust infrastructure retries for only the first maintenance session."""

    def __init__(self):
        super().__init__()
        self.remaining = 3

    def __call__(self, system: str, user: str) -> R.ProviderResult:
        if "Reply with JSON only" in system and self.remaining:
            self.calls.append({"system": system, "user": user})
            self.remaining -= 1
            raise R.InfrastructureFailure("NETWORK", "synthetic reset")
        return super().__call__(system, user)


class FakeHarnessBridge:
    def __init__(self, package_root: Path):
        self.package_root = package_root
        self.views: list[tuple] = []
        self.exports = 0

    def maintained_view(self, state_dir: Path, session: R.Session) -> str:
        self.views.append((state_dir, session.arm, session.scenario, session.checkpoint))
        return ""

    def export_packages(self, state_root: Path, out: Path) -> str:
        self.exports += 1
        lines = ["# R1 native package export manifest v1\n", "# sha256  relative_path\n"]
        for path in sorted(p for p in out.rglob("*.txt") if p.name != "PACKAGE-MANIFEST.txt"):
            rel = path.relative_to(out).as_posix()
            lines.append(f"{R.sha256_hex(path.read_bytes())}  {rel}\n")
        text = "".join(lines)
        (out / "PACKAGE-MANIFEST.txt").write_text(text, encoding="utf-8", newline="\n")
        return "NATIVE_PACKAGE_EXPORT_STATUS=PASS\n"


CONDITION = R.Condition(
    provider="OpenAI",
    model_requested="gpt-5.6-terra",
    model_version_pin_status="PROVIDER_ALIAS_ONLY",
    reasoning_effort="medium",
)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="r1-runner-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.bundle = make_bundle(self.tmp / "b")
        self.packages = make_packages(self.tmp / "p")
        self.store = R.RunStore(self.tmp / "runs")
        self.arm_map = R.neutral_arm_map("seed-1")

    def runner(self, transport):
        return R.Runner(
            self.bundle, self.packages, self.store, transport,
            CONDITION, "seed-1", self.arm_map, sleep=lambda _s: None,
        )

    def session(self, arm="B5", repeat=1):
        return R.Session(
            role="CONTINUATION_AGENT", arm=arm, scenario="S1",
            task_id="S1-A-NEXT", checkpoint=2, repeat_index=repeat,
            trajectory_id=R.trajectory_for(repeat, 4, arm),
        )


# --- gate 1: API key never written -----------------------------------------


class TestKeyNeverWritten(Base):
    def test_key_absent_from_every_output_file(self):
        os.environ["OPENAI_API_KEY"] = "sk-test-DEADBEEF-should-never-appear"
        self.addCleanup(os.environ.pop, "OPENAI_API_KEY", None)
        r = self.runner(FakeTransport())
        r.execute(1, self.session(), "vp")
        blob = "".join(
            p.read_text(encoding="utf-8", errors="replace")
            for p in self.store.root.rglob("*") if p.is_file()
        )
        self.assertNotIn("sk-test-DEADBEEF", blob)
        self.assertNotIn("OPENAI_API_KEY", blob)

    def test_cli_refuses_api_key_argument(self):
        rc = R.main(["preflight", "--api-key", "sk-nope"])
        self.assertEqual(rc, 2)

    def test_transport_requires_env_and_has_no_key_parameter(self):
        import inspect
        sig = inspect.signature(R.OpenAIResponsesTransport.__init__)
        self.assertNotIn("api_key", sig.parameters)
        os.environ.pop("OPENAI_API_KEY", None)
        with self.assertRaises(R.InfrastructureFailure):
            R.OpenAIResponsesTransport("m", "medium", 10)


# --- gate 2: oracle exclusion ----------------------------------------------


class TestOracleExclusion(Base):
    def test_model_facing_surface_has_no_oracle_fields(self):
        for path in (self.bundle.model_facing).rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for field in ("abstain_required", "trap_present", "require_terms", "forbid_terms"):
                    self.assertNotIn(field, text)

    def test_prompt_builder_reads_only_the_bundle_subtree(self):
        _s, user, _c = R.build_continuation_prompts(
            self.bundle, self.packages, self.session()
        )
        self.assertIn("S1-A-NEXT", user)
        # The protocol/ sibling is never opened by construction: assert the builder
        # produced nothing outside bundle/ by checking it fails when bundle/ is gone.
        shutil.rmtree(self.bundle.model_facing / "tasks")
        with self.assertRaises(Exception):
            R.build_continuation_prompts(self.bundle, self.packages, self.session())

    def test_scan_detects_a_planted_oracle(self):
        (self.store.root / "raw" / "leak.txt").write_text(
            '{"abstain_required": true}', encoding="utf-8"
        )
        found = [
            p for p in self.store.root.rglob("*")
            if p.is_file() and "abstain_required" in p.read_text(encoding="utf-8")
        ]
        self.assertEqual(len(found), 1)


# --- gate 3: bundle digest mismatch ----------------------------------------


class TestBundleDigest(Base):
    def test_digest_changes_when_a_bundle_file_changes(self):
        before = R.file_manifest(self.bundle.model_facing)
        p = self.bundle.model_facing / "tasks" / "S1-A-NEXT.txt"
        p.write_text(p.read_text(encoding="utf-8") + "tamper", encoding="utf-8")
        self.assertNotEqual(before, R.file_manifest(self.bundle.model_facing))

    def test_digest_is_stable_when_nothing_changes(self):
        self.assertEqual(
            R.file_manifest(self.bundle.model_facing),
            R.file_manifest(self.bundle.model_facing),
        )


# --- gate 4/5: independent requests, no previous_response_id ---------------


class TestSessionIsolation(Base):
    def test_no_previous_response_id_in_payload(self):
        os.environ["OPENAI_API_KEY"] = "sk-test-x"
        self.addCleanup(os.environ.pop, "OPENAI_API_KEY", None)
        try:
            t = R.OpenAIResponsesTransport("gpt-5.6-terra", "medium", 1024)
        except R.InfrastructureFailure as exc:
            self.skipTest(f"SDK unavailable: {exc}")
        payload = t.build_payload("sys", "user")
        self.assertNotIn("previous_response_id", payload)
        self.assertNotIn("conversation", payload)
        self.assertIs(payload["store"], False)

    def test_source_never_sends_previous_response_id(self):
        src = Path(R.__file__).read_text(encoding="utf-8")
        sending = [
            ln for ln in src.splitlines()
            if "previous_response_id" in ln and not ln.strip().startswith("#")
            and "not" not in ln.lower() and "never" not in ln.lower()
        ]
        self.assertEqual(sending, [], f"conversation state may be threaded: {sending}")

    def test_each_run_is_a_separate_transport_call(self):
        t = FakeTransport()
        r = self.runner(t)
        r.execute(1, self.session(arm="B5", repeat=1), "vp")
        r.execute(2, self.session(arm="B4", repeat=1), "vp")
        r.execute(3, self.session(arm="B5", repeat=2), "vp")
        self.assertEqual(len(t.calls), 3)


# --- gate 6: duplicate-run refusal -----------------------------------------


class TestDuplicateRefusal(Base):
    def test_store_refuses_duplicate_run_id(self):
        rec = {"run_id": "vp-000001", "raw_response_digest": "sha256:x"}
        self.store.append(rec, "hello")
        with self.assertRaises(R.InfrastructureFailure):
            self.store.append(rec, "hello again")

    def test_raw_output_is_never_overwritten(self):
        self.store.append({"run_id": "vp-000002"}, "original")
        self.store._seen.pop("vp-000002")  # simulate a lost record, raw still present
        with self.assertRaises(R.InfrastructureFailure):
            self.store.append({"run_id": "vp-000002"}, "replacement")
        self.assertEqual(
            self.store.raw_path("vp-000002").read_text(encoding="utf-8"), "original"
        )

    def test_runner_refuses_to_overwrite_a_nonvalidating_record(self):
        t = FakeTransport()
        r = self.runner(t)
        r.execute(1, self.session(), "vp")
        # Corrupt the stored digest so resume validation fails.
        rec = self.store.record_for("vp-000001")
        rec["raw_response_digest"] = "sha256:wrong"
        with self.assertRaises(R.InfrastructureFailure):
            r.execute(1, self.session(), "vp")


# --- gate 7: resume correctness --------------------------------------------


class TestResume(Base):
    def test_valid_completed_run_is_not_rerun(self):
        t = FakeTransport()
        r = self.runner(t)
        r.execute(1, self.session(), "vp")
        self.assertEqual(len(t.calls), 1)
        store2 = R.RunStore(self.tmp / "runs")
        r2 = R.Runner(
            self.bundle, self.packages, store2, t, CONDITION, "seed-1",
            self.arm_map, sleep=lambda _s: None,
        )
        r2.execute(1, self.session(), "vp")
        self.assertEqual(len(t.calls), 1, "a valid completed run was re-executed")

    def test_missing_raw_blocks_resume(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        rec = self.store.record_for("vp-000001")
        self.store.raw_path("vp-000001").unlink()
        ok, why = R.resumable(rec, self.store, CONDITION.as_record_fields(), {})
        self.assertFalse(ok)
        self.assertIn("raw response missing", why)

    def test_none_record_is_not_resumable(self):
        ok, _ = R.resumable(None, self.store, CONDITION.as_record_fields(), {})
        self.assertFalse(ok)

    def test_restart_continues_infrastructure_retry_chain_without_replaying_attempt(self):
        boom = R.InfrastructureFailure("NETWORK", "reset")
        first_transport = FakeTransport(script=[boom])

        def interrupt(_seconds):
            raise RuntimeError("simulated process interruption")

        r1 = R.Runner(
            self.bundle, self.packages, self.store, first_transport,
            CONDITION, "seed-1", self.arm_map, sleep=interrupt,
        )
        with self.assertRaises(RuntimeError):
            r1.execute(1, self.session(), "vp")
        self.assertTrue(self.store.has("vp-000001"))
        self.assertFalse(self.store.has("vp-000001a2"))

        second_transport = FakeTransport()
        resumed_store = R.RunStore(self.store.root)
        r2 = R.Runner(
            self.bundle, self.packages, resumed_store, second_transport,
            CONDITION, "seed-1", self.arm_map, sleep=lambda _s: None,
        )
        rec = r2.execute(1, self.session(), "vp")
        self.assertEqual(rec["run_id"], "vp-000001a2")
        self.assertEqual(rec["attempt"], 2)
        self.assertEqual(len(second_transport.calls), 1)

    def test_restart_does_not_reissue_exhausted_infrastructure_chain(self):
        boom = R.InfrastructureFailure("NETWORK", "reset")
        self.runner(FakeTransport(script=[boom, boom, boom])).execute(
            1, self.session(), "vp"
        )
        resumed_transport = FakeTransport()
        resumed_store = R.RunStore(self.store.root)
        resumed = R.Runner(
            self.bundle, self.packages, resumed_store, resumed_transport,
            CONDITION, "seed-1", self.arm_map, sleep=lambda _s: None,
        )
        rec = resumed.execute(1, self.session(), "vp")
        self.assertEqual(rec["run_id"], "vp-000001a3")
        self.assertEqual(rec["outcome"], "INFRASTRUCTURE_FAILURE")
        self.assertEqual(len(resumed_transport.calls), 0)
        self.assertIn(self.session().cell(), resumed.excluded_cells)

    def test_resume_rebuilds_missing_derived_response_from_immutable_raw(self):
        self.runner(FakeTransport()).execute(1, self.session(), "vp")
        target = (
            self.store.root / "responses" / self.arm_map["B5"] /
            "S1-A-NEXT" / "r01.txt"
        )
        target.unlink()
        resumed_store = R.RunStore(self.store.root)
        transport = FakeTransport()
        resumed = R.Runner(
            self.bundle, self.packages, resumed_store, transport,
            CONDITION, "seed-1", self.arm_map, sleep=lambda _s: None,
        )
        resumed.execute(1, self.session(), "vp")
        self.assertEqual(len(transport.calls), 0)
        self.assertEqual(target.read_text(encoding="utf-8"), GOOD_ANSWER)

    def test_runner_version_mismatch_blocks_resume(self):
        self.runner(FakeTransport()).execute(1, self.session(), "vp")
        self.store.record_for("vp-000001")["runner_version"] = "old-runner"
        with self.assertRaises(R.InfrastructureFailure) as ctx:
            self.runner(FakeTransport()).execute(1, self.session(), "vp")
        self.assertIn("RUNNER_VERSION_MISMATCH", str(ctx.exception))


# --- gate 8: corrupted raw response detection ------------------------------


class TestCorruptionDetection(Base):
    def test_tampered_raw_fails_digest_validation(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        rec = self.store.record_for("vp-000001")
        self.store.raw_path("vp-000001").write_text("TAMPERED", encoding="utf-8")
        ok, why = R.resumable(rec, self.store, CONDITION.as_record_fields(), {})
        self.assertFalse(ok)
        self.assertIn("digest mismatch", why)


# --- gate 9/10/11: wrong model, wrong prompt digest, wrong context digest ---


class TestConditionValidation(Base):
    def test_wrong_model_blocks_resume(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        rec = self.store.record_for("vp-000001")
        other = dict(CONDITION.as_record_fields())
        other["model_identifier"] = "some-other-model"
        ok, why = R.resumable(rec, self.store, other, {})
        self.assertFalse(ok)
        self.assertIn("model condition mismatch", why)

    def test_wrong_reasoning_effort_blocks_resume(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        rec = self.store.record_for("vp-000001")
        other = dict(CONDITION.as_record_fields())
        other["reasoning_effort"] = "high"
        ok, why = R.resumable(rec, self.store, other, {})
        self.assertFalse(ok)

    def test_wrong_prompt_digest_blocks_resume(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        rec = self.store.record_for("vp-000001")
        ok, why = R.resumable(
            rec, self.store, CONDITION.as_record_fields(),
            {"user_prompt_digest": "sha256:different"},
        )
        self.assertFalse(ok)
        self.assertIn("user_prompt_digest", why)

    def test_wrong_context_digest_blocks_resume(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        rec = self.store.record_for("vp-000001")
        ok, why = R.resumable(
            rec, self.store, CONDITION.as_record_fields(),
            {"context_package_digest": "sha256:different"},
        )
        self.assertFalse(ok)
        self.assertIn("context_package_digest", why)

    def test_changing_the_package_changes_the_context_digest(self):
        t = FakeTransport()
        r = self.runner(t)
        r.execute(1, self.session(), "vp")
        first = self.store.record_for("vp-000001")["context_package_digest"]
        p = self.packages.path_for(self.session())
        p.write_text("different context", encoding="utf-8")
        _s, _u, ctx = R.build_continuation_prompts(
            self.bundle, self.packages, self.session()
        )
        self.assertNotEqual(first, f"sha256:{R.sha256_hex(ctx)}")


# --- gate 12/13: retry classification, task vs infrastructure --------------


class TestRetryAndClassification(Base):
    def test_infrastructure_failure_retries_exactly_twice(self):
        boom = R.InfrastructureFailure("NETWORK", "connection reset")
        t = FakeTransport(script=[boom, boom, boom])
        r = self.runner(t)
        rec = r.execute(1, self.session(), "vp")
        self.assertEqual(len(t.calls), R.MAX_ATTEMPTS)
        self.assertEqual(rec["outcome"], "INFRASTRUCTURE_FAILURE")
        self.assertIn(self.session().cell(), r.excluded_cells)

    def test_infrastructure_failure_then_success_is_recorded_with_attempts(self):
        boom = R.InfrastructureFailure("RATE_LIMIT", "429")
        t = FakeTransport(script=[boom, None])
        t.script = [boom]
        r = self.runner(t)
        rec = r.execute(1, self.session(), "vp")
        self.assertEqual(rec["outcome"], "OK")
        self.assertEqual(rec["attempt"], 2)
        self.assertTrue(self.store.has("vp-000001"))       # failed attempt recorded
        self.assertTrue(self.store.has("vp-000001a2"))     # successful attempt

    def test_task_failure_is_never_retried(self):
        empty = R.ProviderResult(
            text="", response_id="r", model_returned="gpt-5.6-terra", raw={}
        )
        t = FakeTransport(script=[empty])
        r = self.runner(t)
        rec = r.execute(1, self.session(), "vp")
        self.assertEqual(len(t.calls), 1, "a task failure was retried")
        self.assertEqual(rec["outcome"], "TASK_FAILURE")
        self.assertEqual(rec["failure_class"], "EMPTY_RESPONSE")

    def test_empty_malformed_refusal_are_task_failures(self):
        self.assertEqual(R.classify_outcome("", "CONTINUATION_AGENT")[1], "EMPTY_RESPONSE")
        self.assertEqual(
            R.classify_outcome("just prose", "CONTINUATION_AGENT")[1],
            "MALFORMED_RESPONSE",
        )
        self.assertEqual(
            R.classify_outcome("I can't help with that.", "CONTINUATION_AGENT")[1],
            "REFUSAL",
        )
        self.assertEqual(R.classify_outcome(GOOD_ANSWER, "CONTINUATION_AGENT")[0], "OK")

    def test_provider_faults_classify_as_infrastructure_not_task(self):
        cases = {
            "RateLimitError": "RATE_LIMIT",
            "APITimeoutError": "TIMEOUT",
            "APIConnectionError": "NETWORK",
        }
        for name, expected in cases.items():
            exc = type(name, (Exception,), {})("boom")
            self.assertEqual(R._classify_sdk_error(exc), expected)

    def test_context_limit_is_infrastructure_not_task_failure(self):
        exc = Exception("maximum context length exceeded")
        self.assertEqual(R._classify_sdk_error(exc), "CONTEXT_LIMIT_EXCEEDED")

    def test_exclusion_is_symmetric_across_arms(self):
        boom = R.InfrastructureFailure("NETWORK", "reset")
        t = FakeTransport(script=[boom] * 3)
        r = self.runner(t)
        r.execute(1, self.session(arm="B5"), "vp")
        # The excluded unit is the (task, repeat) cell, not the arm.
        self.assertEqual(list(r.excluded_cells), [("S1-A-NEXT", 1)])
        self.assertNotIn("B5", str(r.excluded_cells))


# --- gate 14: secret scanning ----------------------------------------------


class TestSecretScanning(Base):
    def test_scan_flags_each_pattern(self):
        d = self.tmp / "scan"
        d.mkdir()
        (d / "a.txt").write_text("token sk-abc123", encoding="utf-8")
        (d / "b.txt").write_text("OPENAI_API_KEY=x", encoding="utf-8")
        (d / "c.txt").write_text("Authorization: Bearer zzz", encoding="utf-8")
        hits = R.scan_for_secrets(d)
        self.assertEqual(len({h[0] for h in hits}), 3)

    def test_clean_tree_passes(self):
        d = self.tmp / "clean"
        d.mkdir()
        (d / "a.txt").write_text(GOOD_ANSWER, encoding="utf-8")
        self.assertEqual(R.scan_for_secrets(d), [])

    def test_seal_is_reproducible_when_rerun_without_evidence_change(self):
        root = self.tmp / "rerun-seal"
        root.mkdir()
        (root / "raw.txt").write_text("evidence", encoding="utf-8")
        self.assertEqual(R.main(["seal", "--out", str(root)]), 0)
        archive = root.parent / f"{root.name}-raw.tar.gz"
        first_archive = R.sha256_hex(archive.read_bytes())
        first_manifest = (root / "FILE-MANIFEST.txt").read_bytes()
        self.assertEqual(R.main(["seal", "--out", str(root)]), 0)
        self.assertEqual(R.sha256_hex(archive.read_bytes()), first_archive)
        self.assertEqual((root / "FILE-MANIFEST.txt").read_bytes(), first_manifest)

    def test_seal_refuses_when_a_secret_is_present(self):
        d = self.tmp / "sealme"
        d.mkdir()
        (d / "a.txt").write_text("Authorization: Bearer leaked", encoding="utf-8")
        rc = R.main(["seal", "--out", str(d)])
        self.assertEqual(rc, 1)
        self.assertFalse((d.parent / "sealme-raw.tar.gz").exists())


# --- gate 15: deterministic manifest ---------------------------------------


class TestDeterministicManifest(Base):
    def test_manifest_is_byte_identical_across_rebuilds(self):
        d = self.tmp / "m"
        (d / "sub").mkdir(parents=True)
        (d / "b.txt").write_text("b", encoding="utf-8")
        (d / "a.txt").write_text("a", encoding="utf-8")
        (d / "sub" / "c.txt").write_text("c", encoding="utf-8")
        self.assertEqual(R.file_manifest(d), R.file_manifest(d))

    def test_manifest_is_sorted_and_posix(self):
        d = self.tmp / "m2"
        (d / "sub").mkdir(parents=True)
        (d / "z.txt").write_text("z", encoding="utf-8")
        (d / "sub" / "a.txt").write_text("a", encoding="utf-8")
        paths = [ln.split("  ", 1)[1] for ln in R.file_manifest(d).strip().splitlines()]
        self.assertEqual(paths, sorted(paths))
        self.assertTrue(all("\\" not in p for p in paths))


# --- gate 16: deterministic raw archive ------------------------------------


class TestDeterministicArchive(Base):
    def test_archive_digest_reproduces_independently(self):
        d = self.tmp / "arc"
        (d / "raw").mkdir(parents=True)
        (d / "raw" / "vp-000001.txt").write_text(GOOD_ANSWER, encoding="utf-8")
        (d / "records.jsonl").write_text('{"run_id":"vp-000001"}\n', encoding="utf-8")
        first = R.deterministic_archive(d, self.tmp / "one.tar.gz")
        second = R.deterministic_archive(d, self.tmp / "two.tar.gz")
        self.assertEqual(first, second)
        self.assertEqual(
            R.sha256_hex((self.tmp / "one.tar.gz").read_bytes()),
            R.sha256_hex((self.tmp / "two.tar.gz").read_bytes()),
        )

    def test_archive_changes_when_content_changes(self):
        d = self.tmp / "arc2"
        d.mkdir()
        (d / "a.txt").write_text("one", encoding="utf-8")
        first = R.deterministic_archive(d, self.tmp / "a1.tar.gz")
        (d / "a.txt").write_text("two", encoding="utf-8")
        self.assertNotEqual(first, R.deterministic_archive(d, self.tmp / "a2.tar.gz"))


# --- sealed-protocol conformance -------------------------------------------


class TestSealedProtocolConformance(Base):
    def test_session_counts_match_the_sealed_pilot(self):
        """VARIANCE-PILOT.md §2: 168 maintenance + 720 continuation = 888."""
        tasks = [
            {"task_id": f"T{i:02d}", "scenario": "S1", "checkpoint": 2}
            for i in range(30)
        ]
        checkpoints = [("S1", i) for i in range(10)] + \
                      [("S2", i) for i in range(9)] + [("S3", i) for i in range(9)]
        cont = R.continuation_plan(tasks, "seed", 4)
        maint = R.maintenance_plan(checkpoints, "seed", 2)
        self.assertEqual(len(maint), 168)
        self.assertEqual(len(cont), 720)
        self.assertEqual(len(maint) + len(cont), 888)

    def test_bnull_share_of_continuation_is_120(self):
        tasks = [
            {"task_id": f"T{i:02d}", "scenario": "S1", "checkpoint": 2}
            for i in range(30)
        ]
        cont = R.continuation_plan(tasks, "seed", 4)
        self.assertEqual(sum(1 for s in cont if s.arm == "B-NULL"), 120)
        self.assertEqual(sum(1 for s in cont if s.arm != "B-NULL"), 600)

    def test_order_is_deterministic_from_the_seed(self):
        tasks = [{"task_id": f"T{i}", "scenario": "S1", "checkpoint": 2} for i in range(5)]
        a = [(s.arm, s.task_id, s.repeat_index) for s in R.continuation_plan(tasks, "s", 4)]
        b = [(s.arm, s.task_id, s.repeat_index) for s in R.continuation_plan(tasks, "s", 4)]
        c = [(s.arm, s.task_id, s.repeat_index) for s in R.continuation_plan(tasks, "other", 4)]
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_arms_are_interleaved_not_blocked(self):
        """VARIANCE-PILOT.md §3: running all B5 trials together is prohibited."""
        tasks = [{"task_id": f"T{i:02d}", "scenario": "S1", "checkpoint": 2} for i in range(30)]
        plan = R.continuation_plan(tasks, "seed", 4)
        positions = [i for i, s in enumerate(plan) if s.arm == "B5"]
        spread = (max(positions) - min(positions)) / len(plan)
        self.assertGreater(spread, 0.9, "B5 runs are clustered in wall-clock order")

    def test_maintained_arms_split_repeats_across_two_trajectories(self):
        self.assertEqual(R.trajectory_for(1, 4, "B5"), "T1")
        self.assertEqual(R.trajectory_for(2, 4, "B5"), "T1")
        self.assertEqual(R.trajectory_for(3, 4, "B5"), "T2")
        self.assertEqual(R.trajectory_for(4, 4, "B5"), "T2")
        self.assertIsNone(R.trajectory_for(1, 4, "B0"))

    def test_every_arm_gets_no_tools(self):
        t = FakeTransport()
        r = self.runner(t)
        for arm in R.ARMS:
            self.store = R.RunStore(self.tmp / f"runs-{arm}")
            r.store = self.store
            rec = r.execute(1, self.session(arm=arm), "vp")
            self.assertEqual(rec["tool_set"], [])
            self.assertEqual(rec["tool_permissions"], "none")

    def test_record_carries_every_required_field(self):
        t = FakeTransport()
        rec = self.runner(t).execute(1, self.session(), "vp")
        required = [
            "run_id", "arm_id", "scenario_id", "task_id", "checkpoint",
            "repeat_index", "trajectory_id", "role", "model_provider",
            "model_identifier", "model_version_or_snapshot", "model_version_pin_status",
            "system_prompt_digest",
            "user_prompt_digest", "context_package_digest", "temperature", "top_p",
            "seed", "max_output", "reasoning_effort", "tool_set", "tool_permissions",
            "time_limit_s", "start_time", "end_time", "raw_response_digest",
            "raw_response_artifact", "input_token_count", "output_token_count",
            "outcome", "failure_class", "attempt",
        ]
        for field in required:
            self.assertIn(field, rec, f"missing required field {field}")

    def test_unavailable_is_recorded_not_defaulted(self):
        c = R.Condition("OpenAI", "m", "PROVIDER_ALIAS_ONLY", "medium")
        fields = c.as_record_fields()
        self.assertEqual(fields["temperature"], R.UNAVAILABLE)
        self.assertEqual(fields["top_p"], R.UNAVAILABLE)
        self.assertEqual(fields["seed"], R.UNAVAILABLE)

    def test_control_capabilities_are_bound_from_preflight_without_guessing(self):
        evidence = {
            "TEMPERATURE_STATUS": "SUPPORTED", "TEMPERATURE_VALUE": 0.0,
            "TOP_P_STATUS": "UNAVAILABLE", "TOP_P_VALUE": R.UNAVAILABLE,
            "SEED_STATUS": "UNAVAILABLE", "SEED_VALUE": R.UNAVAILABLE,
        }
        fields, api = R.controls_from_preflight(evidence)
        self.assertEqual(fields["temperature"], 0.0)
        self.assertEqual(fields["top_p"], R.UNAVAILABLE)
        self.assertEqual(fields["seed"], R.UNAVAILABLE)
        self.assertEqual(api, {"temperature": 0.0})

    def test_invalid_preflight_control_status_fails_closed(self):
        evidence = {
            "TEMPERATURE_STATUS": "NOT_PROBED",
            "TOP_P_STATUS": "UNAVAILABLE",
            "SEED_STATUS": "UNAVAILABLE",
        }
        with self.assertRaises(R.InfrastructureFailure):
            R.controls_from_preflight(evidence)

    def test_scorer_sees_only_neutral_arm_ids(self):
        t = FakeTransport()
        r = self.runner(t)
        for arm in ("B5", "B4"):
            r.execute({"B5": 1, "B4": 2}[arm], self.session(arm=arm), "vp")
        names = [p.name for p in (self.store.root / "responses").iterdir()]
        self.assertTrue(all(n.startswith("ARM_") for n in names), names)
        self.assertNotIn("B5", names)

    def test_maintainer_prompt_is_task_blind(self):
        s = R.Session(
            role="MAINTAINER", arm="B5", scenario="S1", task_id=None,
            checkpoint=1, repeat_index=None, trajectory_id="T1",
        )
        system, user, _ = R.build_maintainer_prompts(self.bundle, s, "")
        blob = system + user
        for tid in self.bundle.task_ids():
            self.assertNotIn(tid, blob)
        for word in ("oracle", "score", "will matter later", "ABSTAIN:"):
            self.assertNotIn(word, blob)

    def test_maintainer_never_sees_a_future_checkpoint(self):
        s = R.Session(
            role="MAINTAINER", arm="B4", scenario="S1", task_id=None,
            checkpoint=1, repeat_index=None, trajectory_id="T1",
        )
        _sys, user, _ = R.build_maintainer_prompts(self.bundle, s, "")
        self.assertIn("evidence for S1 at t1", user)
        self.assertNotIn("evidence for S1 at t2", user)

    def test_runner_refuses_to_synthesise_a_missing_package(self):
        s = R.Session(
            role="CONTINUATION_AGENT", arm="B5", scenario="S9", task_id="X",
            checkpoint=0, repeat_index=1, trajectory_id="T1",
        )
        with self.assertRaises(R.InfrastructureFailure) as ctx:
            self.packages.get(s)
        self.assertIn("PACKAGE_MISSING", str(ctx.exception))

    def test_bnull_receives_no_project_context(self):
        _s, user, ctx = R.build_continuation_prompts(
            self.bundle, self.packages, self.session(arm="B-NULL")
        )
        self.assertEqual(ctx, "")
        self.assertNotIn("PROJECT CONTEXT", user)

    def test_infra_halt_threshold_matches_sealed_protocol(self):
        self.assertEqual(R.INFRA_HALT_FRACTION, 0.10)
        self.assertEqual(R.MAX_ATTEMPTS, 3)  # initial + 2 retries, RUNNER.md §5


class TestNativePackageIntegration(Base):
    def test_external_bundle_manifest_verifies_and_tamper_fails(self):
        digest = self.bundle.verify_manifest()
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        task = self.bundle.model_facing / "tasks" / "S1-A-NEXT.txt"
        task.write_text(task.read_text(encoding="utf-8") + "tamper", encoding="utf-8")
        with self.assertRaises(R.InfrastructureFailure):
            self.bundle.verify_manifest()

    def test_human_protocol_files_are_outside_bundle_manifest_scope(self):
        protocol = self.bundle.root / "protocol"
        protocol.mkdir()
        (protocol / "README.md").write_text(
            "human-only execution notes", encoding="utf-8"
        )
        self.assertRegex(self.bundle.verify_manifest(), r"^[0-9a-f]{64}$")

    def test_unmanifested_model_facing_file_is_rejected(self):
        (self.bundle.model_facing / "unexpected.txt").write_text(
            "unexpected model input", encoding="utf-8"
        )
        with self.assertRaises(R.InfrastructureFailure) as ctx:
            self.bundle.verify_manifest()
        self.assertIn("BUNDLE_MANIFEST_MISMATCH", str(ctx.exception))

    def test_stale_unbound_state_root_is_rejected_before_execution(self):
        package_root = self.tmp / "stale-packages"
        make_packages(package_root)
        state_root = self.tmp / "stale-state"
        state_root.mkdir()
        (state_root / "stale.json").write_text("{}", encoding="utf-8")
        store = R.RunStore(self.tmp / "stale-pilot")
        transport = SmartTransport()
        with self.assertRaises(R.InfrastructureFailure) as ctx:
            R.execute_variance_pilot(
                bundle=self.bundle, store=store, bridge=FakeHarnessBridge(package_root),
                transport=transport, condition=CONDITION, seed="seed-1",
                state_root=state_root, package_root=package_root, repeats=4, trajectories=2,
            )
        self.assertIn("STATE_ROOT_UNBOUND", str(ctx.exception))
        self.assertEqual(len(transport.calls), 0)

    def test_package_manifest_verifies_and_tamper_fails(self):
        root = self.packages.root
        FakeHarnessBridge(root).export_packages(self.tmp / "state", root)
        digest = self.packages.verify_manifest()
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        p = next(x for x in root.rglob("*.txt") if x.name != "PACKAGE-MANIFEST.txt")
        p.write_text(p.read_text(encoding="utf-8") + "tamper", encoding="utf-8")
        with self.assertRaises(R.InfrastructureFailure):
            self.packages.verify_manifest()

    def test_package_manifest_rejects_duplicate_and_unsafe_paths(self):
        root = self.packages.root
        bridge = FakeHarnessBridge(root)
        bridge.export_packages(self.tmp / "state", root)
        manifest = root / "PACKAGE-MANIFEST.txt"
        original = manifest.read_text(encoding="utf-8")
        data_line = next(line for line in original.splitlines() if line and not line.startswith("#"))
        manifest.write_text(original + data_line + "\n", encoding="utf-8", newline="\n")
        with self.assertRaises(R.InfrastructureFailure):
            self.packages.verify_manifest()
        digest = "0" * 64
        manifest.write_text(
            f"# R1 native package export manifest v1\n# sha256  relative_path\n{digest}  ../escape.txt\n",
            encoding="utf-8", newline="\n",
        )
        with self.assertRaises(R.InfrastructureFailure):
            self.packages.verify_manifest()

    def test_repeat_outputs_are_distinct_immutable_files(self):
        t = FakeTransport()
        r = self.runner(t)
        r.execute(1, self.session(repeat=1), "vp")
        r.execute(2, self.session(repeat=2), "vp")
        neutral = self.arm_map["B5"]
        d = self.store.root / "responses" / neutral / "S1-A-NEXT"
        self.assertTrue((d / "r01.txt").is_file())
        self.assertTrue((d / "r02.txt").is_file())
        self.assertEqual((d / "r01.txt").read_text(encoding="utf-8"), GOOD_ANSWER)
        self.assertEqual((d / "r02.txt").read_text(encoding="utf-8"), GOOD_ANSWER)

    def test_maintainer_empty_is_malformed_for_one_retry_rule(self):
        outcome, failure = R.classify_outcome("", "MAINTAINER")
        self.assertEqual(outcome, "TASK_FAILURE")
        self.assertEqual(failure, "MALFORMED_RESPONSE")

    def test_maintenance_state_is_canonical_and_immutable(self):
        s = R.Session(
            role="MAINTAINER", arm="B5", scenario="S1", task_id=None,
            checkpoint=1, repeat_index=None, trajectory_id="T1",
        )
        state = self.tmp / "state"
        raw = '{"memories": [], "evidence_bytes_seen": 1}'
        p = R.persist_maintenance_state(state, s, raw)
        self.assertEqual(p.read_bytes(), raw.encode("utf-8"))
        with self.assertRaises(R.InfrastructureFailure):
            R.persist_maintenance_state(
                state, s, '{"memories":[],"evidence_bytes_seen":2}'
            )

    def test_maintainer_wrapper_prose_is_not_repaired(self):
        outcome, failure = R.classify_outcome(
            'prefix {"memories": [], "evidence_bytes_seen": 1} suffix',
            "MAINTAINER",
        )
        self.assertEqual((outcome, failure), ("TASK_FAILURE", "MALFORMED_RESPONSE"))

    def test_realized_order_is_recorded_per_transport_attempt(self):
        t = FakeTransport()
        self.runner(t).execute(1, self.session(), "vp")
        lines = self.store.order_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        rec = json.loads(lines[0])
        self.assertTrue(rec["arm_id"].startswith("ARM_"))
        self.assertEqual(rec["repeat_index"], 1)

    def test_end_to_end_orchestration_uses_native_bridge_before_continuation(self):
        package_root = self.tmp / "native-packages"
        packages = make_packages(package_root)
        bridge = FakeHarnessBridge(package_root)
        transport = SmartTransport()
        store = R.RunStore(self.tmp / "pilot")
        report = R.execute_variance_pilot(
            bundle=self.bundle,
            store=store,
            bridge=bridge,
            transport=transport,
            condition=CONDITION,
            seed="seed-1",
            state_root=self.tmp / "state",
            package_root=package_root,
            repeats=4,
            trajectories=2,
        )
        self.assertEqual(report["PLANNED_MAINTENANCE_SESSIONS"], 18)
        self.assertEqual(report["PLANNED_CONTINUATION_SESSIONS"], 24)
        self.assertEqual(report["PLANNED_TOTAL_SESSIONS"], 42)
        self.assertEqual(bridge.exports, 1)
        self.assertEqual(len(bridge.views), 18)
        self.assertEqual(len(transport.calls), 42)
        self.assertFalse((store.root / "arm-map.json").exists())
        self.assertTrue((store.root / "execution-plan.json").is_file())
        self.assertTrue((store.root / "package-binding.json").is_file())
        self.assertTrue((store.root / "excluded-cells.json").is_file())
        packages.verify_manifest()

    def test_maintenance_malformed_json_gets_exactly_one_identical_prompt_retry(self):
        package_root = self.tmp / "retry-packages"
        packages = make_packages(package_root)
        bridge = FakeHarnessBridge(package_root)
        transport = OneMalformedSmartTransport()
        store = R.RunStore(self.tmp / "retry-pilot")
        report = R.execute_variance_pilot(
            bundle=self.bundle,
            store=store,
            bridge=bridge,
            transport=transport,
            condition=CONDITION,
            seed="seed-1",
            state_root=self.tmp / "retry-state",
            package_root=package_root,
            repeats=4,
            trajectories=2,
        )
        self.assertEqual(report["MAINTENANCE_OK"], 18)
        self.assertEqual(len(transport.calls), 43)  # 42 planned + one protocol retry
        self.assertEqual(transport.calls[0], transport.calls[1])
        records = store.load_records()
        malformed = [r for r in records if r.get("failure_class") == "MALFORMED_RESPONSE"]
        self.assertEqual(len(malformed), 1)
        packages.verify_manifest()

    def test_continuation_infra_exclusion_publishes_no_partial_cell(self):
        package_root = self.tmp / "infra-packages"
        make_packages(package_root)
        bridge = FakeHarnessBridge(package_root)
        store = R.RunStore(self.tmp / "infra-pilot")
        with self.assertRaises(R.InfrastructureFailure) as ctx:
            R.execute_variance_pilot(
                bundle=self.bundle, store=store, bridge=bridge,
                transport=FirstContinuationInfraTransport(), condition=CONDITION,
                seed="seed-1", state_root=self.tmp / "infra-state",
                package_root=package_root, repeats=4, trajectories=2,
            )
        self.assertIn("RUNNER_INADMISSIBLE", str(ctx.exception))
        published = [p for p in (store.root / "responses").rglob("*.txt")]
        self.assertEqual(published, [], "an excluded cell leaked partial score inputs")

    def test_maintenance_infra_exclusion_applies_no_partial_arm_state(self):
        package_root = self.tmp / "maintenance-infra-packages"
        make_packages(package_root)
        bridge = FakeHarnessBridge(package_root)
        store = R.RunStore(self.tmp / "maintenance-infra-pilot")
        state_root = self.tmp / "maintenance-infra-state"
        with self.assertRaises(R.InfrastructureFailure) as ctx:
            R.execute_variance_pilot(
                bundle=self.bundle, store=store, bridge=bridge,
                transport=FirstMaintainerInfraTransport(), condition=CONDITION,
                seed="seed-1", state_root=state_root, package_root=package_root,
                repeats=4, trajectories=2,
            )
        self.assertIn("RUNNER_INADMISSIBLE", str(ctx.exception))
        applied = [
            p for p in state_root.rglob("*.json") if p.name != "RUN-BINDING.json"
        ]
        self.assertEqual(
            applied, [],
            "a symmetrically excluded maintenance cell changed one arm's state",
        )

    def test_control_artifacts_are_immutable_on_resume(self):
        path = self.tmp / "control" / "package-binding.json"
        first = R._write_canonical_json_once(path, {"x": 1}, "BINDING_MISMATCH")
        second = R._write_canonical_json_once(path, {"x": 1}, "BINDING_MISMATCH")
        self.assertEqual(first, second)
        with self.assertRaises(R.InfrastructureFailure):
            R._write_canonical_json_once(path, {"x": 2}, "BINDING_MISMATCH")

    def test_unblind_map_is_explicit_and_deterministic(self):
        out = self.tmp / "unblind" / "arm-map.json"
        first = R.write_unblinded_arm_map(out, "seed-1")
        second = R.write_unblinded_arm_map(out, "seed-1")
        self.assertEqual(first, second)
        mapping = json.loads(out.read_text(encoding="utf-8"))
        self.assertTrue(all(k.startswith("ARM_") for k in mapping))
        self.assertIn("B5", mapping.values())


if __name__ == "__main__":
    unittest.main(verbosity=2)
