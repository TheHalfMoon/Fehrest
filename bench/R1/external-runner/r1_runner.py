#!/usr/bin/env python3
"""R1 external controlled runner.

Benchmark tooling. **Not part of Fehrest.** Nothing here is imported by the product,
and no Fehrest runtime dependency is added by its existence. It executes model
sessions for `bench/R1/VARIANCE-PILOT.md` against a provider API and captures the
per-run evidence that `bench/R1/RUNNER.md` §3 requires.

What it deliberately does not do:

- it does not score, and it never reads an oracle;
- it does not construct arm context packages -- it consumes packages exported by the
  sealed harness, so the construction that is inside the preregistration digest stays
  the only construction that runs;
- it does not repair, normalize or reformat a model answer;
- it does not decide retry policy: the policy is read from RUNNER.md §5 and frozen
  here as constants that a reviewer can diff against that document.

The API key is read from the environment and from nowhere else. It is never written
to a record, a log, a manifest or an archive.
"""

from __future__ import annotations

import argparse
import dataclasses
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import time
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

# ---------------------------------------------------------------------------
# Frozen identity. A reviewer diffs these against the sealed documents.
# ---------------------------------------------------------------------------

RUNNER_VERSION = "r1-external-runner/1.1.0"

#: How the sealed blocked/interleaved order of VARIANCE-PILOT.md §3 is realized.
#: The protocol fixes the loop structure and that one seed drives it; it does not
#: name a PRNG, so the choice is recorded here and in the manifest rather than left
#: implicit. A keyed sort is used because it is reproducible from the seed alone in
#: any language, without depending on a runtime's RNG implementation.
ORDER_ALGORITHM = "sha256-keyed-sort/v1"

#: RUNNER.md §5. Infrastructure failures retry up to twice; task failures never do.
MAX_ATTEMPTS = 3
BACKOFF_BASE_S = 2.0

#: VARIANCE-PILOT.md §7. Halt if the runner itself is this unreliable.
INFRA_HALT_FRACTION = 0.10

#: PROTOCOL.md §4 / RUNNER.md §3.1. Identical for every arm.
TOOL_SET: list[str] = []
TOOL_PERMISSIONS = "none"
TIME_LIMIT_S = 120

ARMS = ("B-NULL", "B0", "B1", "B3", "B4", "B5")
MAINTAINED_ARMS = ("B1", "B4", "B5")

UNAVAILABLE = "UNAVAILABLE"
SEALED_BUNDLE_MANIFEST_SHA256 = "48394b012ab1cb2bf6c46f8c6b2934ccdd7573b9713de31717031f0ad37e69ff"

#: Patterns that must never appear in any runner output. Checked before sealing.
SECRET_PATTERNS = (
    re.compile(r"sk-"),
    re.compile(r"OPENAI_API_KEY"),
    re.compile(r"Authorization:\s*Bearer", re.IGNORECASE),
)

CONTRACT_FIELDS = (
    "DECISION:",
    "ACTION:",
    "CONSTRAINTS_APPLIED:",
    "EVIDENCE:",
    "UNRESOLVED:",
    "ABSTAIN:",
)

REFUSAL_MARKERS = (
    "i can't help",
    "i cannot help",
    "i can't assist",
    "i cannot assist",
    "i'm unable to help",
    "i am unable to help",
    "as an ai language model",
)


def sha256_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Failures
# ---------------------------------------------------------------------------


class InfrastructureFailure(Exception):
    """RUNNER.md §4: not evidence about an arm. Retryable, symmetrically."""

    def __init__(self, failure_class: str, reason: str) -> None:
        super().__init__(f"{failure_class}: {reason}")
        self.failure_class = failure_class
        self.reason = reason


@dataclasses.dataclass(frozen=True)
class ProviderResult:
    """What a transport must return. Every field the provider does not expose is
    ``UNAVAILABLE`` -- never a plausible-looking default (RUNNER.md §3.1)."""

    text: str
    response_id: str
    model_returned: str
    raw: dict
    input_tokens: int | str = UNAVAILABLE
    output_tokens: int | str = UNAVAILABLE
    total_tokens: int | str = UNAVAILABLE
    reasoning_tokens: int | str = UNAVAILABLE


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------


class OpenAIResponsesTransport:
    """Official OpenAI SDK, Responses API, one fresh request per call.

    ``previous_response_id`` is never sent. There is no code path in this class that
    threads conversation state between calls, which is the property RUNNER.md §1
    requires and which the test suite asserts by inspection of the sent payload.
    """

    def __init__(
        self,
        model: str,
        reasoning_effort: str | None,
        max_output: int,
        extra_params: dict | None = None,
        timeout_s: int = TIME_LIMIT_S,
    ) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise InfrastructureFailure(
                "AUTH_CONFIG",
                "OPENAI_API_KEY is not set in the environment. The runner refuses to "
                "accept a key by command-line argument.",
            )
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - environment problem
            raise InfrastructureFailure("SDK_MISSING", str(exc)) from exc

        self._client = OpenAI(api_key=api_key, timeout=timeout_s, max_retries=0)
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.max_output = max_output
        self.extra_params = dict(extra_params or {})

    def build_payload(self, system_prompt: str, user_prompt: str) -> dict:
        payload: dict = {
            "model": self.model,
            "instructions": system_prompt,
            "input": user_prompt,
            "max_output_tokens": self.max_output,
            "store": False,
        }
        if self.reasoning_effort:
            payload["reasoning"] = {"effort": self.reasoning_effort}
        payload.update(self.extra_params)
        return payload

    def create(self, system_prompt: str, user_prompt: str) -> ProviderResult:
        payload = self.build_payload(system_prompt, user_prompt)
        try:
            resp = self._client.responses.create(**payload)
        except Exception as exc:
            raise InfrastructureFailure(_classify_sdk_error(exc), repr(exc)) from exc

        raw = resp.model_dump() if hasattr(resp, "model_dump") else dict(resp)
        usage = raw.get("usage") or {}
        details = usage.get("output_tokens_details") or {}
        return ProviderResult(
            text=_extract_text(resp, raw),
            response_id=raw.get("id") or UNAVAILABLE,
            model_returned=raw.get("model") or UNAVAILABLE,
            raw=raw,
            input_tokens=usage.get("input_tokens", UNAVAILABLE),
            output_tokens=usage.get("output_tokens", UNAVAILABLE),
            total_tokens=usage.get("total_tokens", UNAVAILABLE),
            reasoning_tokens=details.get("reasoning_tokens", UNAVAILABLE),
        )


def _extract_text(resp: object, raw: dict) -> str:
    text = getattr(resp, "output_text", None)
    if isinstance(text, str):
        return text
    chunks: list[str] = []
    for item in raw.get("output") or []:
        for part in item.get("content") or []:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunks.append(part["text"])
    return "".join(chunks)


def _classify_sdk_error(exc: Exception) -> str:
    """RUNNER.md §4. Every provider-side and transport-side fault is infrastructure.

    A wrong or empty answer never reaches this function -- it is a successful HTTP
    exchange and is classified as a task failure downstream.
    """
    name = type(exc).__name__
    text = f"{name} {exc}".lower()
    if "ratelimit" in name.lower() or "rate limit" in text or "429" in text:
        return "RATE_LIMIT"
    if "timeout" in text:
        return "TIMEOUT"
    if "connection" in text or "network" in text:
        return "NETWORK"
    if "context" in text and ("length" in text or "window" in text or "too long" in text):
        return "CONTEXT_LIMIT_EXCEEDED"
    if "authentication" in text or "401" in text or "permission" in text or "403" in text:
        return "AUTH"
    if "notfound" in name.lower() or "404" in text or "model" in text and "exist" in text:
        return "MODEL_UNAVAILABLE"
    return "PROVIDER_ERROR"


# ---------------------------------------------------------------------------
# Sealed execution order -- VARIANCE-PILOT.md §3
# ---------------------------------------------------------------------------


def perm_key(seed: str, *parts: object) -> str:
    joined = "|".join([seed] + [str(p) for p in parts])
    return sha256_hex(joined)


def permute(items: Sequence[str], seed: str, *ctx: object) -> list[str]:
    return sorted(items, key=lambda item: perm_key(seed, *ctx, item))


@dataclasses.dataclass(frozen=True)
class Session:
    role: str
    arm: str
    scenario: str
    task_id: str | None
    checkpoint: int
    repeat_index: int | None
    trajectory_id: str | None

    def cell(self) -> tuple:
        """The (task, repeat) cell. Infrastructure exclusion is applied to this cell
        for EVERY arm, never for one (RUNNER.md §5)."""
        return (self.task_id, self.repeat_index)


def trajectory_for(repeat_index: int, repeats: int, arm: str) -> str | None:
    """VARIANCE-PILOT.md §2: r=4 for maintained arms is 2 runs on each of 2
    trajectories. Unmaintained arms have no maintenance artefact, so no trajectory."""
    if arm not in MAINTAINED_ARMS:
        return None
    half = max(1, repeats // 2)
    return f"T{min(2, (repeat_index - 1) // half + 1)}"


def continuation_plan(
    tasks: Sequence[dict], seed: str, repeats: int
) -> list[Session]:
    by_id = {t["task_id"]: t for t in tasks}
    plan: list[Session] = []
    for repeat_index in range(1, repeats + 1):
        for task_id in permute([t["task_id"] for t in tasks], seed, repeat_index):
            task = by_id[task_id]
            for arm in permute(ARMS, seed, repeat_index, task_id):
                plan.append(
                    Session(
                        role="CONTINUATION_AGENT",
                        arm=arm,
                        scenario=task["scenario"],
                        task_id=task_id,
                        checkpoint=task["checkpoint"],
                        repeat_index=repeat_index,
                        trajectory_id=trajectory_for(repeat_index, repeats, arm),
                    )
                )
    return plan


def maintenance_plan(
    checkpoints: Sequence[tuple[str, int]], seed: str, trajectories: int
) -> list[Session]:
    """One session per (arm, scenario, checkpoint, trajectory).

    Checkpoint order is ascending and is NOT permuted: a maintainer's only memory of
    earlier checkpoints is the artefact it already produced (MAINTENANCE.md §3), so
    the sequence is causal. Arms are interleaved within a checkpoint so that provider
    drift cannot align with an arm.
    """
    plan: list[Session] = []
    for traj in range(1, trajectories + 1):
        for scenario, cp in sorted(checkpoints):
            for arm in permute(MAINTAINED_ARMS, seed, traj, scenario, cp):
                plan.append(
                    Session(
                        role="MAINTAINER",
                        arm=arm,
                        scenario=scenario,
                        task_id=None,
                        checkpoint=cp,
                        repeat_index=None,
                        trajectory_id=f"T{traj}",
                    )
                )
    return plan


# ---------------------------------------------------------------------------
# Bundle + package inputs
# ---------------------------------------------------------------------------


class Bundle:
    """The oracle-free extracted bundle. The runner reads model-visible text from
    ``bundle/`` only; ``protocol/`` is documentation for humans and is never opened
    by prompt construction."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.model_facing = self.root / "bundle"
        if not self.model_facing.is_dir():
            raise InfrastructureFailure(
                "BUNDLE_LAYOUT", f"no bundle/ directory under {self.root}"
            )

    def verify_manifest(self) -> str:
        manifest = self.root / "BUNDLE-MANIFEST.txt"
        if not manifest.is_file():
            raise InfrastructureFailure(
                "BUNDLE_MANIFEST_MISSING", f"no BUNDLE-MANIFEST.txt under {self.root}"
            )
        expected: dict[str, str] = {}
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
            if match is None:
                raise InfrastructureFailure(
                    "BUNDLE_MANIFEST_INVALID", f"malformed manifest line: {line!r}"
                )
            digest, rel = match.groups()
            rel_path = Path(rel)
            if (
                not rel
                or "\\" in rel
                or rel.startswith("/")
                or rel_path.is_absolute()
                or ".." in rel_path.parts
                or rel in expected
            ):
                raise InfrastructureFailure(
                    "BUNDLE_MANIFEST_INVALID", f"unsafe or duplicate path: {rel!r}"
                )
            if not rel.startswith("bundle/"):
                raise InfrastructureFailure(
                    "BUNDLE_MANIFEST_INVALID",
                    f"manifest entry is outside model-facing bundle/: {rel!r}",
                )
            expected[rel] = digest

        # BUNDLE-MANIFEST.txt intentionally seals the model-facing bundle/ subtree,
        # not the human-only protocol/ siblings carried by the external archive.
        # The archive itself is separately pinned by HANDOFF.md SHA-256.  Here we
        # require exact roster + bytes for everything the runner can show a model.
        observed = {
            path.relative_to(self.root).as_posix(): sha256_hex(path.read_bytes())
            for path in self.model_facing.rglob("*")
            if path.is_file()
        }
        if expected != observed:
            missing = sorted(set(expected) - set(observed))
            extra = sorted(set(observed) - set(expected))
            changed = sorted(
                rel
                for rel in set(expected) & set(observed)
                if expected[rel] != observed[rel]
            )
            raise InfrastructureFailure(
                "BUNDLE_MANIFEST_MISMATCH",
                "model-facing bundle manifest mismatch: "
                f"missing={missing[:5]} extra={extra[:5]} changed={changed[:5]}",
            )
        return sha256_hex(manifest.read_bytes())

    def task_ids(self) -> list[str]:
        return sorted(p.stem for p in (self.model_facing / "tasks").glob("*.txt"))

    def task_prompt(self, task_id: str) -> str:
        return (self.model_facing / "tasks" / f"{task_id}.txt").read_text(
            encoding="utf-8"
        )

    def tasks(self) -> list[dict]:
        out = []
        for task_id in self.task_ids():
            head = self.task_prompt(task_id)
            scenario = _header(head, "SCENARIO")
            checkpoint = int(_header(head, "CHECKPOINT").lstrip("t"))
            out.append(
                {"task_id": task_id, "scenario": scenario, "checkpoint": checkpoint}
            )
        return out

    def checkpoints(self) -> list[tuple[str, int]]:
        found: set[tuple[str, int]] = set()
        for scn_dir in sorted((self.model_facing / "evidence").iterdir()):
            for cp_dir in sorted(scn_dir.iterdir()):
                found.add((scn_dir.name, int(cp_dir.name.lstrip("t"))))
        return sorted(found)

    def evidence_at(self, scenario: str, checkpoint: int) -> list[tuple[str, str]]:
        d = self.model_facing / "evidence" / scenario / f"t{checkpoint:02d}"
        if not d.is_dir():
            return []
        return [
            (p.name, p.read_text(encoding="utf-8")) for p in sorted(d.glob("*"))
        ]


def _header(text: str, key: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    raise InfrastructureFailure("BUNDLE_LAYOUT", f"missing {key} header")


class PackageSet:
    """Arm context packages exported by the sealed harness.

    The runner does NOT build these. Arm construction lives in the digested
    ``bench/R1/harness/main.rs`` and must stay the only implementation that runs,
    otherwise the thing being measured is no longer the thing that was preregistered.

    Layout: ``<root>/<TRAJECTORY>/<ARM>/<SCENARIO>/t<NN>.txt``, plus unmaintained arms
    under trajectory ``T0``.
    """

    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def path_for(self, session: Session) -> Path:
        traj = session.trajectory_id or "T0"
        return (
            self.root
            / traj
            / session.arm
            / session.scenario
            / f"t{session.checkpoint:02d}.txt"
        )

    def get(self, session: Session) -> str:
        if session.arm == "B-NULL":
            return ""  # PROTOCOL.md §4: task prompt only, by construction.
        p = self.path_for(session)
        if not p.is_file():
            raise InfrastructureFailure(
                "PACKAGE_MISSING",
                f"no exported context package at {p}. Arm packages must come from the "
                f"sealed harness; the runner will not synthesise one.",
            )
        return p.read_text(encoding="utf-8")

    def verify_manifest(self) -> str:
        manifest = self.root / "PACKAGE-MANIFEST.txt"
        if not manifest.is_file():
            raise InfrastructureFailure(
                "PACKAGE_MANIFEST_MISSING", f"no native package manifest at {manifest}"
            )
        lines = manifest.read_text(encoding="utf-8").splitlines()
        expected: dict[str, str] = {}
        for line in lines:
            if not line or line.startswith("#"):
                continue
            digest, sep, rel = line.partition("  ")
            if not sep or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise InfrastructureFailure(
                    "PACKAGE_MANIFEST_INVALID", f"malformed manifest line: {line!r}"
                )
            rel_path = Path(rel)
            if (
                not rel
                or "\\" in rel
                or rel.startswith("/")
                or rel_path.is_absolute()
                or ".." in rel_path.parts
                or rel in expected
            ):
                raise InfrastructureFailure(
                    "PACKAGE_MANIFEST_INVALID", f"unsafe or duplicate package path: {rel!r}"
                )
            expected[rel] = digest
        observed = {
            path.relative_to(self.root).as_posix(): sha256_hex(path.read_bytes())
            for path in self.root.rglob("*.txt")
            if path.name != "PACKAGE-MANIFEST.txt"
        }
        if observed != expected:
            raise InfrastructureFailure(
                "PACKAGE_MANIFEST_MISMATCH",
                f"native package manifest mismatch: expected={len(expected)} observed={len(observed)}",
            )
        return sha256_hex(manifest.read_bytes())


class HarnessBridge:
    """Invoke the native R1 harness for state folding and package export.

    The runner never imports or reimplements arm construction. The bridge is the
    only boundary: maintainer current-state rendering and continuation packages are
    both produced by the same Rust harness whose bytes are bound by preregistration.
    """

    def __init__(self, repo_root: Path, cargo: str = "cargo") -> None:
        self.repo_root = Path(repo_root)
        self.cargo = cargo

    def _invoke(self, *args: str) -> str:
        cmd = [
            self.cargo, "run", "--quiet", "--bin", "fehrest-r1", "--", *args
        ]
        proc = subprocess.run(
            cmd,
            cwd=self.repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            raise InfrastructureFailure(
                "HARNESS_FAILURE",
                f"native harness exited {proc.returncode}: {proc.stderr.strip()}",
            )
        return proc.stdout

    def maintained_view(self, state_dir: Path, session: Session) -> str:
        if session.checkpoint <= 0:
            return ""
        return self._invoke(
            "maintenance-view",
            str(state_dir),
            session.arm,
            session.scenario,
            str(session.checkpoint - 1),
        )

    def export_packages(self, state_root: Path, out: Path) -> str:
        return self._invoke("export-packages", str(state_root), str(out))


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

CONTINUATION_SYSTEM = (
    "You are continuing work on an ongoing software project. Answer only from the "
    "project context you are given. Do not invent facts. Follow the requested output "
    "format exactly."
)

MAINTAINER_SYSTEM = {
    "B1": (
        "You maintain a repository's state documents. You will be shown the new "
        "evidence added to the project at this checkpoint and the current contents of "
        "your documents. Decide what, if anything, to change.\n"
        'Reply with JSON only: {"evidence_bytes_seen": <int>, "files": '
        '[{"path": "...", "body": "..."}]}\n'
        "Each entry replaces that path wholesale. Omitting a path leaves the previous "
        "version standing. An empty list is a legitimate decision."
    ),
    "B4": (
        "You maintain a single project wiki page. You will be shown the new evidence "
        "added to the project at this checkpoint and the current page. Decide what, if "
        "anything, to change.\n"
        'Reply with JSON only: {"evidence_bytes_seen": <int>, "wiki": "<full page>"}\n'
        "The page is replaced wholesale. Omitting the field leaves the previous page "
        "unchanged. Changing nothing is a legitimate decision."
    ),
    "B5": (
        "You maintain a structured memory store. You will be shown the new evidence "
        "added to the project at this checkpoint and the memories you have already "
        "written. Decide what, if anything, to change.\n"
        'Reply with JSON only: {"evidence_bytes_seen": <int>, "memories": [ ... ]}\n'
        'Each op is one of: {"op":"add","id":...,"statement":...,"mtype":...,'
        '"project":...,"valid_from":<int>,"supersedes":[...]}, '
        '{"op":"supersede","id":...,"valid_until":<int>}, '
        '{"op":"retract","id":...}, {"op":"conflict","id":...}.\n'
        "mtype is one of Fact, Decision, Constraint, Gotcha, State. There is no basis "
        "field. An empty list is a legitimate decision."
    ),
}


def build_continuation_prompts(
    bundle: Bundle, packages: PackageSet, session: Session
) -> tuple[str, str, str]:
    context = packages.get(session)
    task = bundle.task_prompt(session.task_id)
    if context:
        user = f"PROJECT CONTEXT\n---\n{context}\n---\n\n{task}"
    else:
        user = task
    return CONTINUATION_SYSTEM, user, context


def build_maintainer_prompts(
    bundle: Bundle, session: Session, current_artefact: str
) -> tuple[str, str, str]:
    """MAINTENANCE.md §3. Task-blind by construction: this function has no access to
    a task, an oracle or a future checkpoint, and cannot leak one by mistake."""
    evidence = bundle.evidence_at(session.scenario, session.checkpoint)
    body = "\n\n".join(f"### {name}\n{text}" for name, text in evidence)
    user = (
        f"PROJECT: {session.scenario}\n"
        f"NEW EVIDENCE AT THIS CHECKPOINT\n---\n{body}\n---\n\n"
        f"YOUR CURRENT ARTEFACT\n---\n{current_artefact or '(nothing yet)'}\n---\n"
    )
    return MAINTAINER_SYSTEM[session.arm], user, body


def maintenance_state_path(root: Path, session: Session) -> Path:
    if session.trajectory_id is None:
        raise InfrastructureFailure("MAINTENANCE_LAYOUT", "maintainer session lacks trajectory")
    return (
        Path(root)
        / session.trajectory_id
        / session.arm
        / session.scenario
        / f"t{session.checkpoint:02d}.json"
    )


def persist_maintenance_state(root: Path, session: Session, raw_text: str) -> Path:
    """Persist the exact valid maintainer JSON text. Existing bytes are immutable.

    The prompt requires JSON only. Prefix/suffix prose is therefore malformed rather
    than something the runner may repair. Exact text preservation also keeps the
    harness's maintenance-output byte accounting tied to what the model actually
    wrote instead of to a runner reserialization.
    """
    try:
        json.loads(raw_text)
    except Exception as exc:
        raise InfrastructureFailure("MAINTENANCE_STATE_INVALID", str(exc)) from exc
    data = raw_text.encode("utf-8")
    path = maintenance_state_path(root, session)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise InfrastructureFailure(
                "MAINTENANCE_STATE_CONFLICT", f"refusing to overwrite {path}"
            )
        return path
    path.write_bytes(data)
    return path


# ---------------------------------------------------------------------------
# Outcome classification
# ---------------------------------------------------------------------------


def classify_outcome(text: str, role: str) -> tuple[str, str | None]:
    """A successful HTTP exchange that produced bad content is a TASK_FAILURE.

    RUNNER.md §4: never the other way round. Collapsing the two would let a flaky
    network look like a weak baseline.
    """
    if text is None or text.strip() == "":
        return (
            "TASK_FAILURE",
            "MALFORMED_RESPONSE" if role == "MAINTAINER" else "EMPTY_RESPONSE",
        )
    lowered = text.lower()
    if any(marker in lowered for marker in REFUSAL_MARKERS):
        return "TASK_FAILURE", "REFUSAL"
    if role == "CONTINUATION_AGENT":
        if not any(field in text for field in CONTRACT_FIELDS):
            return "TASK_FAILURE", "MALFORMED_RESPONSE"
    else:
        try:
            json.loads(text)
        except Exception:
            return "TASK_FAILURE", "MALFORMED_RESPONSE"
    return "OK", None


# ---------------------------------------------------------------------------
# Store: records, raw output, resume, duplicate protection
# ---------------------------------------------------------------------------


class RunStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        (self.root / "raw").mkdir(parents=True, exist_ok=True)
        (self.root / "responses").mkdir(parents=True, exist_ok=True)
        self.records_path = self.root / "records.jsonl"
        self.order_path = self.root / "execution-order.jsonl"
        self._seen: dict[str, dict] = {}
        for rec in self.load_records():
            self._seen[rec["run_id"]] = rec

    def load_records(self) -> list[dict]:
        if not self.records_path.is_file():
            return []
        out = []
        for line in self.records_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
        return out

    def has(self, run_id: str) -> bool:
        return run_id in self._seen

    def record_for(self, run_id: str) -> dict | None:
        return self._seen.get(run_id)

    def raw_path(self, run_id: str) -> Path:
        return self.root / "raw" / f"{run_id}.txt"

    def append(self, record: dict, raw_text: str) -> None:
        run_id = record["run_id"]
        if self.has(run_id):
            raise InfrastructureFailure(
                "DUPLICATE_RUN", f"{run_id} already recorded; refusing to overwrite"
            )
        raw = self.raw_path(run_id)
        if raw.exists():
            raise InfrastructureFailure(
                "DUPLICATE_RUN", f"{raw} already exists; raw output is immutable"
            )
        raw.write_text(raw_text, encoding="utf-8", newline="\n")
        with self.records_path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
        self._seen[run_id] = record

    def append_order(self, entry: dict) -> None:
        with self.order_path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")


def record_integrity(
    record: dict | None,
    store: RunStore,
    expected_condition: dict,
    expected_digests: dict,
) -> tuple[bool, str]:
    """Validate immutable evidence independently of whether the attempt succeeded.

    Infrastructure failures are valid *attempt evidence* even though they are not a
    completed task result. Keeping integrity separate from completion lets a restart
    continue the frozen retry chain without overwriting or replaying earlier attempts.
    """
    if record is None:
        return False, "no record"
    raw = store.raw_path(record["run_id"])
    if not raw.is_file():
        return False, "raw response missing"
    actual = sha256_hex(raw.read_text(encoding="utf-8"))
    if f"sha256:{actual}" != record.get("raw_response_digest"):
        return False, "raw response digest mismatch"
    for key, want in expected_condition.items():
        if record.get(key) != want:
            return False, f"model condition mismatch on {key}"
    for key, want in expected_digests.items():
        if record.get(key) != want:
            return False, f"{key} mismatch"
    if record.get("outcome") not in ("OK", "TASK_FAILURE", "INFRASTRUCTURE_FAILURE"):
        return False, "unknown attempt outcome"
    return True, "valid attempt evidence"


def resumable(
    record: dict | None,
    store: RunStore,
    expected_condition: dict,
    expected_digests: dict,
) -> tuple[bool, str]:
    """A completed run is skipped on resume only if every one of these holds."""
    ok, why = record_integrity(record, store, expected_condition, expected_digests)
    if not ok:
        return False, why
    if record is None or record.get("outcome") not in ("OK", "TASK_FAILURE"):
        return False, "run did not complete"
    return True, "complete"


# ---------------------------------------------------------------------------
# Secret scanning, manifest, deterministic archive
# ---------------------------------------------------------------------------


def scan_for_secrets(root: Path) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    for path in sorted(p for p in Path(root).rglob("*") if p.is_file()):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append((str(path.relative_to(root)), pattern.pattern))
    return hits


def file_manifest(root: Path) -> str:
    """Deterministic source manifest; excludes its own derived manifest file."""
    lines = []
    for path in sorted(
        (p for p in Path(root).rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(root).as_posix(),
    ):
        rel = path.relative_to(root).as_posix()
        if rel == "FILE-MANIFEST.txt":
            continue
        lines.append(f"{sha256_hex(path.read_bytes())}  {rel}")
    return "\n".join(lines) + "\n"


def deterministic_archive(root: Path, out: Path) -> str:
    """Byte-identical on every rebuild: sorted names, zeroed ownership and mtime,
    gzip without an embedded timestamp."""
    root, out = Path(root), Path(out)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for path in sorted(
            (p for p in root.rglob("*") if p.is_file()),
            key=lambda p: p.relative_to(root).as_posix(),
        ):
            rel = path.relative_to(root).as_posix()
            info = tarfile.TarInfo(f"{root.name}/{rel}")
            data = path.read_bytes()
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    raw = buf.getvalue()
    with open(out, "wb") as fh:
        # `filename=""` matters: GzipFile otherwise embeds the output file's name in
        # the header, which would make the digest depend on where it was written.
        with gzip.GzipFile(filename="", fileobj=fh, mode="wb", mtime=0) as gz:
            gz.write(raw)
    return sha256_hex(out.read_bytes())


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class Condition:
    provider: str
    model_requested: str
    model_version_pin_status: str
    reasoning_effort: str
    temperature: object = UNAVAILABLE
    top_p: object = UNAVAILABLE
    seed: object = UNAVAILABLE
    max_output: int = 1024

    def as_record_fields(self) -> dict:
        return {
            "model_provider": self.provider,
            "model_identifier": self.model_requested,
            "model_version_or_snapshot": UNAVAILABLE,
            "model_version_pin_status": self.model_version_pin_status,
            "reasoning_effort": self.reasoning_effort,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "seed": self.seed,
            "max_output": self.max_output,
        }


class Runner:
    def __init__(
        self,
        bundle: Bundle,
        packages: PackageSet,
        store: RunStore,
        transport: Callable[[str, str], ProviderResult],
        condition: Condition,
        seed: str,
        arm_map: dict[str, str],
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.bundle = bundle
        self.packages = packages
        self.store = store
        self.transport = transport
        self.condition = condition
        self.seed = seed
        self.arm_map = arm_map  # real arm -> neutral id
        self.sleep = sleep
        self.excluded_cells: set[tuple] = set()
        existing = self.store.load_records()
        # Preserve runner-quality accounting across process restarts. Historical
        # attempts are evidence and must not disappear from the >10% halt gate.
        self.attempted = len(existing)
        self.infra_failures = sum(
            rec.get("outcome") == "INFRASTRUCTURE_FAILURE" for rec in existing
        )

    # -- one session ------------------------------------------------------

    def execute(
        self,
        index: int,
        session: Session,
        prefix: str,
        artefact: str = "",
        run_suffix: str = "",
        publish_response: bool = True,
    ) -> dict:
        base_run_id = f"{prefix}-{index:06d}{run_suffix}"
        if session.role == "CONTINUATION_AGENT":
            system, user, context = build_continuation_prompts(
                self.bundle, self.packages, session
            )
        else:
            system, user, context = build_maintainer_prompts(
                self.bundle, session, artefact
            )

        digests = {
            "system_prompt_digest": f"sha256:{sha256_hex(system)}",
            "user_prompt_digest": f"sha256:{sha256_hex(user)}",
            "context_package_digest": f"sha256:{sha256_hex(context)}",
        }
        expected_condition = self.condition.as_record_fields()

        attempt_ids = [
            base_run_id if attempt == 1 else f"{base_run_id}a{attempt}"
            for attempt in range(1, MAX_ATTEMPTS + 1)
        ]

        record: dict | None = None
        for attempt, run_id in enumerate(attempt_ids, 1):
            existing = self.store.record_for(run_id)
            if existing is not None:
                valid, why = record_integrity(
                    existing, self.store, expected_condition, digests
                )
                if not valid:
                    raise InfrastructureFailure(
                        "DUPLICATE_RUN",
                        f"{run_id} exists but fails immutable-evidence validation: {why}",
                    )
                if existing.get("runner_version") != RUNNER_VERSION:
                    raise InfrastructureFailure(
                        "RUNNER_VERSION_MISMATCH",
                        f"{run_id} was produced by {existing.get('runner_version')!r}, "
                        f"expected {RUNNER_VERSION!r}",
                    )
                outcome = existing.get("outcome")
                if outcome in ("OK", "TASK_FAILURE"):
                    if session.role == "CONTINUATION_AGENT" and publish_response:
                        raw = self.store.raw_path(run_id).read_text(encoding="utf-8")
                        self._write_response(session, raw)
                    return existing
                if outcome == "INFRASTRUCTURE_FAILURE":
                    record = existing
                    if attempt == MAX_ATTEMPTS:
                        if session.role == "CONTINUATION_AGENT":
                            self.excluded_cells.add(session.cell())
                        return existing
                    continue
                raise InfrastructureFailure(
                    "RUN_RECORD_INVALID", f"unexpected outcome in {run_id}: {outcome!r}"
                )

            # A later retry without this earlier attempt would make the retry chain
            # impossible to audit. Fail closed rather than filling the gap.
            later = [rid for rid in attempt_ids[attempt:] if self.store.has(rid)]
            if later:
                raise InfrastructureFailure(
                    "RETRY_CHAIN_GAP",
                    f"missing {run_id} but later immutable attempts exist: {later}",
                )

            self.attempted += 1
            started = time.time()
            self.store.append_order(
                {
                    "run_id": run_id,
                    "arm_id": self.arm_map[session.arm],
                    "scenario_id": session.scenario,
                    "task_id": session.task_id,
                    "checkpoint": session.checkpoint,
                    "repeat_index": session.repeat_index,
                    "trajectory_id": session.trajectory_id,
                    "role": session.role,
                    "attempt": attempt,
                }
            )
            try:
                result = self.transport(system, user)
            except InfrastructureFailure as failure:
                self.infra_failures += 1
                record = self._record(
                    run_id, session, digests, attempt, started, None,
                    "INFRASTRUCTURE_FAILURE", failure.failure_class, failure.reason,
                )
                self.store.append(record, json.dumps({"error": failure.reason}))
                if attempt < MAX_ATTEMPTS:
                    self.sleep(BACKOFF_BASE_S ** attempt)
                    continue
                if session.role == "CONTINUATION_AGENT":
                    self.excluded_cells.add(session.cell())
                return record

            outcome, failure_class = classify_outcome(result.text, session.role)
            record = self._record(
                run_id, session, digests, attempt, started, result,
                outcome, failure_class, None,
            )
            self.store.append(record, result.text)
            if session.role == "CONTINUATION_AGENT" and publish_response:
                self._write_response(session, result.text)
            return record  # TASK_FAILURE is never retried. It is the result.
        return record  # pragma: no cover

    def _write_response(self, session: Session, text: str) -> None:
        neutral = self.arm_map[session.arm]
        if session.repeat_index is None:
            raise InfrastructureFailure("RESPONSE_LAYOUT", "continuation response lacks repeat")
        d = self.store.root / "responses" / neutral / str(session.task_id)
        d.mkdir(parents=True, exist_ok=True)
        target = d / f"r{session.repeat_index:02d}.txt"
        if target.exists():
            if target.read_text(encoding="utf-8") != text:
                raise InfrastructureFailure(
                    "DUPLICATE_RESPONSE", f"refusing to overwrite {target}"
                )
            return
        target.write_text(text, encoding="utf-8", newline="\n")

    def _record(
        self, run_id, session, digests, attempt, started, result,
        outcome, failure_class, failure_reason,
    ) -> dict:
        rec = {
            "run_id": run_id,
            "arm_id": self.arm_map[session.arm],
            "scenario_id": session.scenario,
            "task_id": session.task_id,
            "checkpoint": session.checkpoint,
            "repeat_index": session.repeat_index,
            "trajectory_id": session.trajectory_id,
            "role": session.role,
            "tool_set": TOOL_SET,
            "tool_permissions": TOOL_PERMISSIONS,
            "time_limit_s": TIME_LIMIT_S,
            "runner_version": RUNNER_VERSION,
            "start_time": _iso(started),
            "end_time": _iso(time.time()),
            "wall_time_ms": int((time.time() - started) * 1000),
            "outcome": outcome,
            "failure_class": failure_class,
            "failure_reason": failure_reason,
            "attempt": attempt,
        }
        rec.update(self.condition.as_record_fields())
        rec.update(digests)
        if result is None:
            rec.update(
                {
                    "model_returned": UNAVAILABLE,
                    "response_id": UNAVAILABLE,
                    "raw_response_digest": f"sha256:{sha256_hex(json.dumps({'error': failure_reason}))}",
                    "raw_response_artifact": f"raw/{run_id}.txt",
                    "input_token_count": UNAVAILABLE,
                    "output_token_count": UNAVAILABLE,
                    "total_token_count": UNAVAILABLE,
                    "reasoning_token_count": UNAVAILABLE,
                }
            )
        else:
            rec.update(
                {
                    "model_returned": result.model_returned,
                    "response_id": result.response_id,
                    "raw_response_digest": f"sha256:{sha256_hex(result.text)}",
                    "raw_response_artifact": f"raw/{run_id}.txt",
                    "input_token_count": result.input_tokens,
                    "output_token_count": result.output_tokens,
                    "total_token_count": result.total_tokens,
                    "reasoning_token_count": result.reasoning_tokens,
                }
            )
        return rec

    def infra_rate(self) -> float:
        return self.infra_failures / self.attempted if self.attempted else 0.0


def _iso(ts: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def neutral_arm_map(seed: str) -> dict[str, str]:
    """Neutral ids, assigned from the seed. The scorer never sees 'Fehrest'."""
    order = permute(ARMS, seed, "arm-map")
    return {arm: f"ARM_{chr(ord('A') + i)}" for i, arm in enumerate(order)}


def write_unblinded_arm_map(path: Path, seed: str) -> str:
    """Create neutral -> real mapping only after scoring, on explicit invocation."""
    arm_map = neutral_arm_map(seed)
    inverse = {neutral: real for real, neutral in arm_map.items()}
    canonical = json.dumps(inverse, sort_keys=True, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != canonical:
            raise InfrastructureFailure("ARM_MAP_MISMATCH", "existing arm map differs")
        return sha256_hex(canonical)
    path.write_text(canonical, encoding="utf-8", newline="\n")
    return sha256_hex(canonical)


def _plan_digest(
    maintenance: Sequence[Session], continuation: Sequence[Session], arm_map: dict[str, str]
) -> str:
    rows = []
    for session in [*maintenance, *continuation]:
        rows.append(
            {
                "role": session.role,
                "arm_id": arm_map[session.arm],
                "scenario_id": session.scenario,
                "task_id": session.task_id,
                "checkpoint": session.checkpoint,
                "repeat_index": session.repeat_index,
                "trajectory_id": session.trajectory_id,
            }
        )
    payload = "".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows
    )
    return sha256_hex(payload)


def _write_canonical_json_once(path: Path, payload: object, failure_class: str) -> str:
    """Write a derived control artifact once; on resume, require byte identity."""
    canonical = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != canonical:
            raise InfrastructureFailure(failure_class, f"existing {path.name} differs")
        return sha256_hex(canonical)
    path.write_text(canonical, encoding="utf-8", newline="\n")
    return sha256_hex(canonical)


def _write_execution_plan(
    path: Path,
    seed: str,
    condition: Condition,
    maintenance: Sequence[Session],
    continuation: Sequence[Session],
    arm_map: dict[str, str],
    bundle_manifest_sha256: str,
) -> str:
    payload = {
        "schema": "fehrest-r1-variance-execution-plan/1",
        "stage": "R1-VARIANCE-PILOT",
        "confirmatory": False,
        "runner_version": RUNNER_VERSION,
        "order_algorithm": ORDER_ALGORITHM,
        "randomization_seed": seed,
        "maintenance_sessions": len(maintenance),
        "continuation_sessions": len(continuation),
        "total_sessions": len(maintenance) + len(continuation),
        "planned_order_sha256": _plan_digest(maintenance, continuation, arm_map),
        "model_condition": condition.as_record_fields(),
        "arm_map_withheld": True,
        "bundle_manifest_sha256": bundle_manifest_sha256,
    }
    return _write_canonical_json_once(path, payload, "EXECUTION_PLAN_MISMATCH")


def _bind_state_root(
    state_root: Path, store: RunStore, execution_plan_sha256: str
) -> str:
    """Prevent stale trajectory state from a different run contaminating this plan."""
    state_root = Path(state_root)
    marker = state_root / "RUN-BINDING.json"
    payload = {
        "schema": "fehrest-r1-state-binding/1",
        "runner_version": RUNNER_VERSION,
        "execution_plan_sha256": execution_plan_sha256,
    }
    if not marker.exists() and state_root.exists():
        stale = [p for p in state_root.rglob("*") if p.is_file()]
        if stale:
            raise InfrastructureFailure(
                "STATE_ROOT_UNBOUND",
                f"state root contains {len(stale)} file(s) without a matching run binding",
            )
    state_digest = _write_canonical_json_once(marker, payload, "STATE_BINDING_MISMATCH")
    store_digest = _write_canonical_json_once(
        store.root / "state-binding.json", payload, "STATE_BINDING_MISMATCH"
    )
    if state_digest != store_digest:
        raise InfrastructureFailure("STATE_BINDING_MISMATCH", "state/store bindings differ")
    return state_digest


def execute_variance_pilot(
    bundle: Bundle,
    store: RunStore,
    bridge: HarnessBridge,
    transport: Callable[[str, str], ProviderResult],
    condition: Condition,
    seed: str,
    state_root: Path,
    package_root: Path,
    repeats: int = 4,
    trajectories: int = 2,
) -> dict:
    """Execute the sealed two-part variance pilot without scoring or unblinding.

    Infrastructure exclusion is transactional at the protocol cell boundary. A
    failed maintainer cell applies *none* of the three arm updates; a failed
    continuation (task, repeat) cell publishes *none* of the six arm responses.
    Immutable raw attempts remain preserved either way.
    """
    if repeats != 4 or trajectories != 2:
        raise InfrastructureFailure(
            "SEALED_PROTOCOL_MISMATCH", "R1 variance pilot requires repeats=4 trajectories=2"
        )

    bundle_manifest_sha256 = bundle.verify_manifest()
    arm_map = neutral_arm_map(seed)
    maintenance = maintenance_plan(bundle.checkpoints(), seed, trajectories)
    continuation = continuation_plan(bundle.tasks(), seed, repeats)
    execution_plan_sha256 = _write_execution_plan(
        store.root / "execution-plan.json",
        seed,
        condition,
        maintenance,
        continuation,
        arm_map,
        bundle_manifest_sha256,
    )
    state_binding_sha256 = _bind_state_root(
        Path(state_root), store, execution_plan_sha256
    )
    runner = Runner(bundle, PackageSet(package_root), store, transport, condition, seed, arm_map)

    maintenance_ok = 0
    maintenance_task_failures = 0
    maintenance_infra_excluded: set[tuple[str, str, int]] = set()

    indexed_maintenance = list(enumerate(maintenance, 1))
    cursor = 0
    while cursor < len(indexed_maintenance):
        first_index, first_session = indexed_maintenance[cursor]
        cell_key = (
            str(first_session.trajectory_id),
            first_session.scenario,
            first_session.checkpoint,
        )
        group: list[tuple[int, Session]] = []
        while cursor < len(indexed_maintenance):
            idx, candidate = indexed_maintenance[cursor]
            candidate_key = (
                str(candidate.trajectory_id),
                candidate.scenario,
                candidate.checkpoint,
            )
            if candidate_key != cell_key:
                break
            group.append((idx, candidate))
            cursor += 1

        pending_states: list[tuple[Session, str]] = []
        group_infra = False
        for index, session in group:
            traj_root = Path(state_root) / str(session.trajectory_id)
            current = bridge.maintained_view(traj_root, session)
            record = runner.execute(index, session, "vm", current)
            final = record
            if record["outcome"] == "TASK_FAILURE" and record["failure_class"] == "MALFORMED_RESPONSE":
                # MAINTENANCE.md §7: one identical-prompt retry, counted and preserved.
                final = runner.execute(index, session, "vm", current, run_suffix="m2")

            if final["outcome"] == "INFRASTRUCTURE_FAILURE":
                group_infra = True
            elif final["outcome"] == "OK":
                raw = store.raw_path(final["run_id"]).read_text(encoding="utf-8")
                pending_states.append((session, raw))
            else:
                maintenance_task_failures += 1

        if group_infra:
            # Symmetric infrastructure exclusion: preserve all raw evidence but do
            # not let one maintained arm advance state when a peer could not run.
            maintenance_infra_excluded.add(cell_key)
        else:
            for session, raw in pending_states:
                persist_maintenance_state(state_root, session, raw)
                maintenance_ok += 1

        processed = cursor
        if maintenance_infra_excluded and len(maintenance_infra_excluded) / max(1, processed / len(MAINTAINED_ARMS)) > INFRA_HALT_FRACTION:
            raise InfrastructureFailure(
                "RUNNER_INADMISSIBLE",
                "exhausted maintenance infrastructure cells exceed 10% of attempted cells",
            )

    bridge.export_packages(Path(state_root), Path(package_root))
    package_manifest_sha256 = PackageSet(package_root).verify_manifest()
    binding = {
        "schema": "fehrest-r1-package-binding/1",
        "package_manifest_sha256": package_manifest_sha256,
        "execution_plan_sha256": execution_plan_sha256,
        "state_binding_sha256": state_binding_sha256,
        "bundle_manifest_sha256": bundle_manifest_sha256,
    }
    package_binding_sha256 = _write_canonical_json_once(
        store.root / "package-binding.json", binding, "PACKAGE_BINDING_MISMATCH"
    )

    continuation_ok = 0
    continuation_task_failures = 0
    continuation_infra_excluded: set[tuple[str | None, int | None]] = set()

    indexed_continuation = list(enumerate(continuation, 1))
    cursor = 0
    processed_cells = 0
    while cursor < len(indexed_continuation):
        _first_index, first_session = indexed_continuation[cursor]
        cell_key = first_session.cell()
        group: list[tuple[int, Session]] = []
        while cursor < len(indexed_continuation):
            idx, candidate = indexed_continuation[cursor]
            if candidate.cell() != cell_key:
                break
            group.append((idx, candidate))
            cursor += 1
        processed_cells += 1

        completed: list[tuple[Session, dict]] = []
        group_infra = False
        for index, session in group:
            record = runner.execute(index, session, "vp", publish_response=False)
            completed.append((session, record))
            if record["outcome"] == "INFRASTRUCTURE_FAILURE":
                group_infra = True

        if group_infra:
            continuation_infra_excluded.add(cell_key)
            runner.excluded_cells.add(cell_key)
        else:
            # Publish the complete paired cell only after every arm has a terminal
            # task result. This makes symmetric exclusion real rather than metadata.
            for session, record in completed:
                raw = store.raw_path(record["run_id"]).read_text(encoding="utf-8")
                runner._write_response(session, raw)
                if record["outcome"] == "OK":
                    continuation_ok += 1
                else:
                    continuation_task_failures += 1

        if len(continuation_infra_excluded) / max(1, processed_cells) > INFRA_HALT_FRACTION:
            raise InfrastructureFailure(
                "RUNNER_INADMISSIBLE",
                "exhausted continuation infrastructure cells exceed 10% of attempted cells",
            )

    excluded = sorted(
        [list(cell) for cell in continuation_infra_excluded],
        key=lambda x: (str(x[0]), str(x[1])),
    )
    excluded_payload = {
        "schema": "fehrest-r1-excluded-cells/1",
        "continuation_task_repeat_cells": excluded,
        "maintenance_trajectory_checkpoint_cells": [
            list(cell) for cell in sorted(maintenance_infra_excluded)
        ],
    }
    excluded_cells_sha256 = _write_canonical_json_once(
        store.root / "excluded-cells.json",
        excluded_payload,
        "EXCLUDED_CELLS_MISMATCH",
    )
    return {
        "PLANNED_MAINTENANCE_SESSIONS": len(maintenance),
        "PLANNED_CONTINUATION_SESSIONS": len(continuation),
        "PLANNED_TOTAL_SESSIONS": len(maintenance) + len(continuation),
        "MAINTENANCE_OK": maintenance_ok,
        "MAINTENANCE_TASK_FAILURES": maintenance_task_failures,
        "MAINTENANCE_INFRA_EXCLUDED_CELLS": len(maintenance_infra_excluded),
        "CONTINUATION_OK": continuation_ok,
        "CONTINUATION_TASK_FAILURES": continuation_task_failures,
        "CONTINUATION_INFRA_EXCLUDED_CELLS": len(continuation_infra_excluded),
        "INFRASTRUCTURE_FAILURE_ATTEMPTS": runner.infra_failures,
        "EXCLUDED_CELLS": len(excluded),
        "PACKAGE_MANIFEST_SHA256": package_manifest_sha256,
        "PACKAGE_BINDING_SHA256": package_binding_sha256,
        "STATE_BINDING_SHA256": state_binding_sha256,
        "BUNDLE_MANIFEST_SHA256": bundle_manifest_sha256,
        "EXCLUDED_CELLS_SHA256": excluded_cells_sha256,
        "EXECUTION_PLAN_SHA256": execution_plan_sha256,
    }


# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

PREFLIGHT_PROMPT = "Return exactly: FEHREST_R1_RUNNER_OK"
PREFLIGHT_EXPECT = "FEHREST_R1_RUNNER_OK"
MODEL_VERSION_PIN_STATUS = "UNAVAILABLE_FLOATING_ALIAS"
CONTROL_CANDIDATES = {
    "temperature": 0.0,
    "top_p": 1.0,
    "seed": 0,
}


def probe_parameter(model: str, reasoning_effort: str, name: str, value: object) -> str:
    """Determine whether a sampling control is actually accepted. Never guessed."""
    try:
        transport = OpenAIResponsesTransport(
            model=model,
            reasoning_effort=reasoning_effort,
            max_output=64,
            extra_params={name: value},
        )
        transport.create("You are a parameter probe.", "Return exactly: OK")
        return "SUPPORTED"
    except InfrastructureFailure as failure:
        if failure.failure_class in ("PROVIDER_ERROR", "MODEL_UNAVAILABLE"):
            return "UNAVAILABLE"
        raise


def preflight(model: str, reasoning_effort: str, max_output: int = 256) -> dict:
    """Credentialed capability preflight using no R1 benchmark content.

    The first request proves the requested model/reasoning path is callable. Separate
    minimal requests probe sampling controls because unsupported controls must be
    recorded as UNAVAILABLE rather than silently guessed. A final request proves the
    exact combination of every supported control before the condition may be used.
    """
    transport = OpenAIResponsesTransport(
        model=model, reasoning_effort=reasoning_effort, max_output=max_output
    )
    result = transport.create("You are a connectivity probe.", PREFLIGHT_PROMPT)
    if PREFLIGHT_EXPECT not in result.text:
        raise InfrastructureFailure(
            "PREFLIGHT_OUTPUT", "connectivity probe returned unexpected output"
        )

    statuses: dict[str, str] = {}
    supported: dict[str, object] = {}
    for name, value in CONTROL_CANDIDATES.items():
        status = probe_parameter(model, reasoning_effort, name, value)
        statuses[name] = status
        if status == "SUPPORTED":
            supported[name] = value

    combined_response_id: str | None = None
    if supported:
        combined = OpenAIResponsesTransport(
            model=model,
            reasoning_effort=reasoning_effort,
            max_output=64,
            extra_params=supported,
        ).create("You are a combined-condition probe.", "Return exactly: OK")
        combined_response_id = combined.response_id

    usage = result.raw.get("usage") or {}
    report: dict[str, object] = {
        "API_PREFLIGHT": "PASS",
        "API_PREFLIGHT_RESPONSE_ID": result.response_id,
        "CONTROL_PREFLIGHT_RESPONSE_ID": combined_response_id or UNAVAILABLE,
        "MODEL_REQUESTED": model,
        "MODEL_RETURNED": result.model_returned,
        "MODEL_VERSION_PIN_STATUS": MODEL_VERSION_PIN_STATUS,
        "REASONING_EFFORT": reasoning_effort,
        "MAX_OUTPUT": max_output,
        "USAGE_FIELDS_PRESENT": sorted(usage.keys()) or [UNAVAILABLE],
        "INPUT_TOKENS": result.input_tokens,
        "OUTPUT_TOKENS": result.output_tokens,
        "REASONING_TOKENS": result.reasoning_tokens,
        "TEXT": result.text.strip()[:200],
    }
    for name, value in CONTROL_CANDIDATES.items():
        key = name.upper()
        report[f"{key}_STATUS"] = statuses[name]
        report[f"{key}_VALUE"] = value if statuses[name] == "SUPPORTED" else UNAVAILABLE
    return report


def controls_from_preflight(evidence: dict) -> tuple[dict, dict]:
    """Return (record fields, API kwargs) from an already verified preflight."""
    fields: dict[str, object] = {}
    api: dict[str, object] = {}
    for name in CONTROL_CANDIDATES:
        status = evidence.get(f"{name.upper()}_STATUS")
        value = evidence.get(f"{name.upper()}_VALUE", UNAVAILABLE)
        if status == "SUPPORTED":
            if value == UNAVAILABLE:
                raise InfrastructureFailure(
                    "PREFLIGHT_RECORD_INVALID", f"{name} supported without a value"
                )
            fields[name] = value
            api[name] = value
        elif status == "UNAVAILABLE":
            fields[name] = UNAVAILABLE
        else:
            raise InfrastructureFailure(
                "PREFLIGHT_RECORD_INVALID", f"missing/invalid {name} capability status"
            )
    return fields, api


# ---------------------------------------------------------------------------
# Cost envelope
# ---------------------------------------------------------------------------


def token_envelope(
    bundle: Bundle,
    packages: PackageSet | None,
    repeats: int,
    trajectories: int,
    max_output_per_run: int,
    budget_bytes: int = 6000,
    chars_per_token: float = 4.0,
) -> dict:
    """Estimated from the actual prepared inputs, with the budget as a hard bound.

    PROTOCOL.md §4 caps every arm's context package at ``budget_bytes``, so the
    per-run input is bounded above without needing the packages to exist. When they
    do exist the measured size is used instead.
    """
    tasks = bundle.tasks()
    task_chars = {t["task_id"]: len(bundle.task_prompt(t["task_id"])) for t in tasks}
    system_chars = len(CONTINUATION_SYSTEM)

    continuation_input_chars = 0
    for task_id, chars in task_chars.items():
        for arm in ARMS:
            ctx = 0 if arm == "B-NULL" else budget_bytes
            continuation_input_chars += (chars + ctx + system_chars) * repeats

    maintenance_input_chars = 0
    for scenario, cp in bundle.checkpoints():
        evidence = sum(len(text) for _, text in bundle.evidence_at(scenario, cp))
        for arm in MAINTAINED_ARMS:
            maintenance_input_chars += (
                evidence + budget_bytes + len(MAINTAINER_SYSTEM[arm])
            ) * trajectories

    total_input_chars = continuation_input_chars + maintenance_input_chars
    n_continuation = len(tasks) * len(ARMS) * repeats
    n_maintenance = len(bundle.checkpoints()) * len(MAINTAINED_ARMS) * trajectories

    return {
        "CONTINUATION_SESSIONS": n_continuation,
        "MAINTENANCE_SESSIONS": n_maintenance,
        "TOTAL_SESSIONS": n_continuation + n_maintenance,
        "TOTAL_INPUT_CHARS_ESTIMATE": total_input_chars,
        "TOTAL_INPUT_TOKENS_ESTIMATE": int(total_input_chars / chars_per_token),
        "MAX_OUTPUT_TOKENS_PER_RUN": max_output_per_run,
        "TOTAL_MAX_OUTPUT_TOKENS": (n_continuation + n_maintenance)
        * max_output_per_run,
        "CHARS_PER_TOKEN_ASSUMED": chars_per_token,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    # Checked before argument parsing, so the refusal cannot be pre-empted by an
    # argparse error. The key comes from the environment and nowhere else: argv is
    # visible to process inspection and shell history.
    if any(str(a).startswith("--api-key") for a in (argv if argv is not None else sys.argv[1:])):
        print("REFUSED: the API key must come from OPENAI_API_KEY, not from argv")
        return 2

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=["preflight", "estimate", "plan", "run", "seal", "scan", "unblind-map"],
    )
    parser.add_argument("--bundle", type=Path, help="extracted r1-external root")
    parser.add_argument("--packages", type=Path, help="harness-exported arm packages")
    parser.add_argument("--out", type=Path, default=Path("runs/variance-pilot"))
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--seed", default=None)
    parser.add_argument("--repeats", type=int, default=4)
    parser.add_argument("--trajectories", type=int, default=2)
    parser.add_argument("--max-output", type=int, default=1024)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--state-root", type=Path)
    parser.add_argument("--preflight-out", type=Path)
    parser.add_argument("--preflight-record", type=Path)

    args = parser.parse_args(argv)

    if args.command == "preflight":
        try:
            report = preflight(args.model, args.reasoning_effort, args.max_output)
        except InfrastructureFailure as failure:
            print(f"API_PREFLIGHT=FAIL\nFAILURE_CLASS={failure.failure_class}")
            print(f"FAILURE_REASON={failure.reason}")
            return 1
        for key, value in report.items():
            print(f"{key}={value}")
        if args.preflight_out is not None:
            payload = dict(report)
            payload["RUNNER_VERSION"] = RUNNER_VERSION
            if args.preflight_out.exists():
                print("preflight output already exists; refusing to overwrite evidence")
                return 2
            digest = _write_canonical_json_once(
                args.preflight_out, payload, "PREFLIGHT_RECORD_MISMATCH"
            )
            print(f"PREFLIGHT_RECORD={args.preflight_out}")
            print(f"PREFLIGHT_RECORD_SHA256={digest}")
        return 0

    if args.command == "unblind-map":
        if args.seed is None:
            print("--seed is required for unblinding")
            return 2
        target = args.out / "arm-map.json"
        try:
            digest = write_unblinded_arm_map(target, args.seed)
        except InfrastructureFailure as failure:
            print(f"UNBLIND_MAP=FAIL\nFAILURE_CLASS={failure.failure_class}")
            return 1
        print(f"UNBLIND_MAP={target}")
        print(f"UNBLIND_MAP_SHA256={digest}")
        return 0

    if args.command == "scan":
        hits = scan_for_secrets(args.out)
        for path, pattern in hits:
            print(f"SECRET_SCAN_HIT {path} {pattern}")
        print(f"SECRET_SCAN={'FAIL' if hits else 'PASS'}")
        return 1 if hits else 0

    # Sealing operates on produced output, not on the bundle, so it is handled before
    # the bundle requirement.
    if args.command == "seal":
        root = args.out
        hits = scan_for_secrets(root)
        if hits:
            print(f"SECRET_SCAN=FAIL ({len(hits)} hits) -- refusing to seal")
            for path, pattern in hits:
                print(f"  SECRET_SCAN_HIT {path} {pattern}")
            return 1
        manifest = file_manifest(root)
        (root / "FILE-MANIFEST.txt").write_text(manifest, encoding="utf-8", newline="\n")
        archive = root.parent / f"{root.name}-raw.tar.gz"
        digest = deterministic_archive(root, archive)
        print("SECRET_SCAN=PASS")
        print(f"RAW_OUTPUT_ARCHIVE={archive}")
        print(f"R1_VARIANCE_PILOT_RAW_SHA256={digest}")
        return 0

    if args.bundle is None:
        print("--bundle is required")
        return 2
    bundle = Bundle(args.bundle)
    try:
        bundle_manifest_sha256 = bundle.verify_manifest()
    except InfrastructureFailure as failure:
        print(f"BUNDLE_VERIFICATION=FAIL\nFAILURE_CLASS={failure.failure_class}")
        return 1
    if bundle_manifest_sha256 != SEALED_BUNDLE_MANIFEST_SHA256:
        print("BUNDLE_VERIFICATION=FAIL")
        print(f"EXPECTED_BUNDLE_MANIFEST_SHA256={SEALED_BUNDLE_MANIFEST_SHA256}")
        print(f"OBSERVED_BUNDLE_MANIFEST_SHA256={bundle_manifest_sha256}")
        return 1

    if args.command == "estimate":
        env = token_envelope(
            bundle,
            PackageSet(args.packages) if args.packages else None,
            args.repeats,
            args.trajectories,
            args.max_output,
        )
        for key, value in env.items():
            print(f"{key}={value}")
        return 0

    if args.seed is None:
        print("--seed is required: it is recorded in the manifest before execution")
        return 2

    tasks = bundle.tasks()
    cont = continuation_plan(tasks, args.seed, args.repeats)
    maint = maintenance_plan(bundle.checkpoints(), args.seed, args.trajectories)

    if args.command == "plan":
        print(f"MAINTENANCE_SESSIONS={len(maint)}")
        print(f"CONTINUATION_SESSIONS={len(cont)}")
        print(f"TOTAL_SESSIONS={len(maint) + len(cont)}")
        print(f"ORDER_ALGORITHM={ORDER_ALGORITHM}")
        print(f"SEED={args.seed}")
        return 0

    if args.command == "run":
        if args.packages is None or args.repo_root is None or args.state_root is None:
            print("run requires --packages, --repo-root and --state-root")
            return 2
        if args.preflight_record is None or not args.preflight_record.is_file():
            print("run requires --preflight-record from a successful credentialed preflight")
            return 2
        evidence = json.loads(args.preflight_record.read_text(encoding="utf-8"))
        if evidence.get("API_PREFLIGHT") != "PASS":
            print("preflight record is not PASS")
            return 2
        if evidence.get("MODEL_REQUESTED") != args.model:
            print("preflight model does not match requested run model")
            return 2
        if evidence.get("REASONING_EFFORT") != args.reasoning_effort:
            print("preflight reasoning effort does not match requested run condition")
            return 2
        if evidence.get("MAX_OUTPUT") != args.max_output:
            print("preflight max-output does not match requested run condition")
            return 2
        if evidence.get("RUNNER_VERSION") != RUNNER_VERSION:
            print("preflight runner version does not match current runner")
            return 2
        try:
            control_fields, api_controls = controls_from_preflight(evidence)
        except InfrastructureFailure as failure:
            print(f"preflight record invalid: {failure}")
            return 2

        condition = Condition(
            provider="OpenAI",
            model_requested=args.model,
            model_version_pin_status=evidence.get(
                "MODEL_VERSION_PIN_STATUS", MODEL_VERSION_PIN_STATUS
            ),
            reasoning_effort=args.reasoning_effort,
            temperature=control_fields["temperature"],
            top_p=control_fields["top_p"],
            seed=control_fields["seed"],
            max_output=args.max_output,
        )
        try:
            transport = OpenAIResponsesTransport(
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                max_output=args.max_output,
                extra_params=api_controls,
            )
            report = execute_variance_pilot(
                bundle=bundle,
                store=RunStore(args.out),
                bridge=HarnessBridge(args.repo_root),
                transport=transport.create,
                condition=condition,
                seed=args.seed,
                state_root=args.state_root,
                package_root=args.packages,
                repeats=args.repeats,
                trajectories=args.trajectories,
            )
        except InfrastructureFailure as failure:
            print(f"R1_VARIANCE_PILOT_STATUS=HALTED")
            print(f"FAILURE_CLASS={failure.failure_class}")
            print(f"FAILURE_REASON={failure.reason}")
            return 1
        for key, value in report.items():
            print(f"{key}={value}")
        print("R1_VARIANCE_PILOT_STATUS=EXECUTION_COMPLETE_UNSCORED")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
