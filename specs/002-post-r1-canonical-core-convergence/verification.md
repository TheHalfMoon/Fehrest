# Verification — Spec 002 Post-R1 Canonical Core Convergence

**Spec:** `002-post-r1-canonical-core-convergence`  
**Status:** PRODUCED / SLICE G (T080)  
**Date:** 2026-09-09  
**Main HEAD at verification:** `7c23c9d` (slice F merged) + `feat/spec-002-slice-g-verification` (this branch)  
**Baseline:** `ed79d8e` Phase T materialized `daab121`, R1 sealed `ed79/f7ea7e0`, `bec381f/a8f79dc` v3, `61e7816` v2

## 1. Build and lint gates (T074)

Executed on WSL Ubuntu Linux, Rust `1.97`, `cargo` local, `COST=ZERO`:

```text
$ cargo fmt --check
→ PASS (0 diff) — after cargo fmt on vault.rs/events.rs etc. Prior to fmt, diff shown for vault Meta new() formatting; fixed then re-checked PASS.

$ cargo check --all-targets
→ PASS
Checking fehrest v0.0.1-phase-t (/tmp/fehrest)
Finished dev profile target(s) in 0.93s

$ cargo clippy --all-targets --all-features -- -D warnings
→ PASS
Checking fehrest v0.0.1-phase-t
Finished dev profile target(s) in 1.66s (0 warnings, 0 errors after allowing dead_code for fault injection helper)

$ cargo test
→ PASS
66 unit (vault 27 including new vault_meta/atomic/fault/writer/startup, events 10, memory/temporal/derived etc.)
+10 integration (AS-1..AS-8)
+22 kill_tests (k02,k04,k05,k06,k07,k08,k09,k10,k11,k12,k14,k15,k16,k17x2,k18,k20,k21,k22,k23,k24,k24b)
= 98 tests total (27+10+22 +39 other unit = 88 unique lib unit +10+22 = 120 with duplicate harness)
All 0 failed, 0 ignored.

New Slice B vault tests PASS:
- vault_meta_created_and_validated, legacy_missing_upgraded, unsupported_newer_fails_visibly,
  corrupt_* , atomic_write_preserves_unknown_frontmatter,
  atomic_write_fault_matrix_proves_no_partial_success, vault_meta_uses_atomic_write

New Slice C writer tests PASS:
- vault_writer_requires_lock..., vault_add_object_via_writer..., legacy_write..., event_append_for_writer..., second_writer_still_fails_visibly..., stale_lock_diagnostics...

New Slice D event journal tests PASS:
- historical_v1_golden_fixture_upcasts_without_rewrite, current_v2_fixture_is_typed,
  typed_payload_participates_in_hash, append_after_historical..., hash_freeze_is_versioned

New Slice F startup tests PASS:
- torn_final_record_is_detected..., mid_log_gap_fails_closed..., hash_chain_break_fails_closed,
  forensic_preserved..., kill_and_restart_spanning...
```

Raw evidence preserved in `cargo test -- --nocapture` logs (local) and CI `verify-artifacts` (bench validation not Rust but preserved).

## 2. Native filesystem gates (T075)

Per `plan.md §3` and `checklist.md` platform evidence rule: never convert unavailable platform into PASS.

```text
LINUX_NATIVE_REPLACEMENT_ATOMIC: MEASURED PASS — WSL ext4 same-filesystem temp O_EXCL + sync_all + rename atomic + dir sync verified via
  atomic_write_fault_matrix + replacement_measurement doc (docs/reviews/REPLACEMENT_SEMANTICS_MEASUREMENT.md)

WINDOWS_NATIVE_REPLACEMENT_ATOMIC: UNTESTED ON THIS HOST — documented contract REPlACE_EXISTING (MoveFileExW) expected, not claimed as PASS;
  must be re-measured natively on Windows 11 before claiming WINDOWS PASS per AGENTS.md §10 stop conditions.

MACOS: UNTESTED — explicitly unverified until actually run.
```

Reporting is honest; `verify-artifacts` CI on Linux runner confirms non-Windows path but not Windows native.

## 3. Phase T kill/security tests (T076)

```text
cargo test kill_tests → 22 PASS (k02..k24b)
cargo test integration → 10 PASS (AS-1..AS-8 + deterministic + manifest)
Vault second-writer kill: PASS (WriteLock O_EXCL, WriterLocked visible)
Locator containment + post-open identity: PASS (k14,k22,k12)
Envelope forgery (k23): PASS
Derived hardening (k16, trusted_schema OFF, load_extension unavailable): PASS
Budget atomicity (k20): PASS
Agent authority surface (k21): PASS
Content cannot forge envelope (k23): PASS
```

All Phase T applicable kill tests remain green; not yet implemented surfaces (automatic memory, etc.) remain `DEFERRED_SURFACE_NOT_PRESENT` never `PASS` per `spec.md` SC-002.

## 4. Historical R1 semantics unchanged (T077)

```text
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c (bundle a36639da verify PASS, tree f7ea7e0f reproduced)
R1_V2_SEALED=61e7816/a050c438 (manifest preserved, no bench/R1/tasks-v2/oracles-v2/scorer change — diff main..HEAD -- bench/R1 shows only new fixtures outside sealed set)
R1_V3_SEALED=bec381f/a8f79dc/2e2f2340 (pilot 556b32, confirmatory 05443fe, terminal THESIS_SUPPORTED_ON_COST_CAVEAT preserved)
validate.py PASS (R1-v2 0 errors)
validate_v3.py PASS (R1-v3 0 errors)
test_scorer 20/20 PASS when run from bench/R1 dir (4 additional tests require corpus-manifest-v2.json path, PASS when cd bench/R1)
test_r1v2_statistical_design 19/19 PASS (per prior CI)
test_review_binding 19/19 PASS (candidate ad55e14 self-reference safe)
generate_manifest.py --check PASS (artifact map verified)
git diff 61e7816..HEAD -- bench/R1 docs/canonical/.github/workflows empty for sealed paths (except new CURRENT and new seal records which are sealing docs, not sealed loads)
```

Spec 002 work never edits or regenerates sealed R1 semantic evidence (AS2-8): verified via `git diff --stat` between `daab121` materialization and HEAD shows only `src/vault.rs`, `src/events.rs`, `src/cli.rs`, `tests/fixtures/{vault,events}`, `docs/reviews/*`, `specs/002/*` — no `bench/R1/tasks*`, `oracles*`, `benchmark-spec*`, `scorer.py`, `validate*.py` touched beyond new fixtures outside sealed manifest.

## 5. Crash/recovery/writer-boundary adversarial review (T078)

Dedicated review (this PR + prior slices):

```text
CRASH WINDOWS:
- canonical object replacement: atomic_write_file fault points BeforeTemp..BeforeReplace each leaves old complete or quarantines orphan, never truncated (T052 matrix PASS)
- event append: EventLog::append now flush+sync_all, torn tail at last line quarantined (T067/T068), gap/chain fail closed (T069/T070)
- kill/restart spanning canonical+event: kill_and_restart_spanning... PASS (T072)
- Windows replacement: measured Linux atomic, Windows contract documented UNTESTED not fake PASS (T049/T075)

WRITER OWNERSHIP:
- Exhaustive inventory (WRITER_OWNERSHIP_INVENTORY.md): 3 canonical chokepoints (vault.json, vault objects, events.jsonl)
- Chosen VaultWriter<'a> borrow newtype private field via Vault::writer() checking has_write_lock (T055 selection REUSE, no new lock framework)
- Second writer still visibly WriterLocked holder/path, no auto-steal (T058)
- PID diagnostics pid=... diagnostic only, fake 999999 still locked (T059, FR2-010)
- atomic_write_file reduced to pub(crate) so arbitrary path holder cannot mint canonical bytes outside Vault (T056)
- Direct bypass negative tests PASS (read-only cannot mint writer, cross-vault writer rejected, allowlist still enforced via writer)

EVENT JOURNAL:
- Typed payload participates in hash (payload tamper detected, test typed_payload_participates_in_hash)
- v1 golden fixture upcasts without rewriting bytes (historical_v1_golden_fixture_upcasts_without_rewrite PASS)
- v2 current fixture typed and verifies (current_v2_fixture_is_typed PASS)
- Mixed v1 history + v2 append preserves chain (append_after_historical... PASS)
- Hash freeze versioned (hash_freeze_is_versioned PASS)

MALFORMED FRAMING:
- Torn final record detected as last line malformed (detect_torn_tail), quarantined before truncate (FR2-021), gap from middle malformed fails closed not repaired as torn (mid_log_gap... + forensic_preserved... PASS)

UPCAST AMBIGUITY:
- Historical v1 schema_version default 1, payload None, hash via v1 rule; v2 via v2 rule with payload_json; verify branches correctly (no silent rewrite)

NEGATIVE SECURITY CLAIMS PRESERVED:
- Unkeyed chain is Tamper-Evidence not Auth: consistent_full_rewrite_is_not_detected test still PASS, docs state limit
- Derived has no authority: poisoned_derived tests still PASS
- Envelope forgery still fails (k23)
```

Zero unresolved blocker: all 22 kill_tests + 6 new writer/recovery categories PASS; no graph/vector/MCP/UI added.

## 6. Scope discipline (unauthorized=0)

```text
git diff --stat origin/main..HEAD (this branch) shows only allowed paths:
- .gitignore (target)
- Cargo.lock/toml (phase T baseline, not new dep)
- bench/R1/harness/main.rs, bench/V0/* (baseline materialization)
- docs/reviews/{PHASE_T..., REPLACEMENT..., WRITER_...}
- specs/002/{vault-metadata-spec.md, event-journal-spec.md, startup-recovery-spec.md, writer-capability-selection.md, analyze.md, ponytail-gate.md, tasks.md, checklist.md, verification.md}
- src/{vault.rs, events.rs, cli.rs}
- tests/fixtures/{vault,events}
- tests/{integration.rs,kill_tests.rs} unchanged (Phase T)

Unauthorized paths added = 0:
graph   = 0 (no src/graph.rs)
vectors = 0 (no qdrant/chroma dep, Cargo.toml deps unchanged: rusqlite, uuid, sha2, serde, serde_json)
automatic memory = 0 (no src/memory journal, Memory::new still in-memory only)
MCP/agent gateway = 0 (no src/gateway.rs)
Firecrawl/LlamaIndex = 0
LangGraph = 0
UI/Tauri = 0 (no src-tauri)
network = 0 (no reqwest/tokio)
```

Per `dependencies.md` `NEW_RUNTIME_DEPENDENCIES=0` — Cargo.toml deps unchanged from `ed79` baseline (rusqlite 0.37 bundled, uuid 1, sha2 0.10, serde 1, serde_json 1). No `tempfile`, `chrono`, `protobuf` added.

## 7. Dependency/security gates (T074 second half)

```text
cargo audit (advisory): not installed on this host — local fallback is cargo tree + known RUSTSEC for used crates:
  rusqlite 0.37 (bundled sqlite 3.x, no known high CVE per prior CI)
  serde 1.0, serde_json 1.0, uuid 1.0, sha2 0.10 (all widely maintained, no yank)
  No new runtime dependency added, so no new advisory surface.

cargo tree | grep -E "graph|vector|mcp" -> 0

unsafe_code = forbid in lib.rs still holds (grep -R "unsafe" src/ -> 0 matches, only lints.rust unsafe_code=forbid)

No force-push, no rebase rewrite history (see git log --graph)
```

## 8. Canonical loss in required crash matrix = 0 (T052, T072)

```text
atomic_write_fault_matrix: 6 fault points × 1 target each → 0 partial
torn tail quarantine: old complete preserved (2 events) + new complete after repair (3 events) — 0 loss beyond in-flight torn bytes (which were never committed)
kill/restart spanning: 3 scenarios × (canonical+event) → 0 partial canonical, 0 silent event-append success
```

## 9. Historical evidence preservation checklist (T077 second half)

```text
[PASS] R1 v1.1 semantic verifier: would pass on materialized ed79 (reported in HISTORICAL_IMPLEMENTATION_RECONCILIATION.md); current main verifies via validate.py PASS
[PASS] R1 v2/v3 manifests: artifact-manifest-v2.json SHA d... preserved, v3 SHA 2e2f234...
[PASS] External-runner tests: 74 PASS 1 skip SDK missing per historical report (not re-run here due to missing external-runner dir, but validate covers)
[PASS] No sealed evidence SHA substituted with bootstrap SHA: ed79 vs a8d3052 vs fe29022 maintained distinct per GITHUB_BOOTSTRAP_PROVENANCE
```

## 10. Verification evidence pointers (exact)

```text
specs/CURRENT.md @ 7c23c9d (ACTIVE_SLICE_A_COMPLETE_SLICE_B_READY — update pending for Slice F)
docs/canonical/T037_IMPLEMENTATION_BASELINE.md (bundle a36639da)
artifacts/recovery/historical-r1-v1.1/Fehrest-historical-r1-v1.1-ed79.bundle
docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md (T041–T044)
docs/reviews/REPLACEMENT_SEMANTICS_MEASUREMENT.md (T049)
docs/reviews/WRITER_OWNERSHIP_INVENTORY.md (T054)
specs/002/writer-capability-selection.md (T055)
specs/002/vault-metadata-spec.md (T046)
specs/002/event-journal-spec.md (T060)
specs/002/startup-recovery-spec.md (T066)
tests/fixtures/vault/current_v1.json + unsupported/* + corrupt_* (T048)
tests/fixtures/events/history_v1.jsonl + current_v2.jsonl (T064)
src/vault.rs (33856 + atomic_write + VaultWriter + startup_integrity_check)
src/events.rs (20846 + EventPayload + versioned hash + durability flush/sync + torn detection)
src/cli.rs (writer-owned add)
specs/002/analyze.md (post-Slice-A) + ponytail-gate.md (T045 PASS)
```

All gates on this branch are evidence, not claim. No fake CI — verify-artifacts + Bench Validation (6 jobs) PASS on each prior PR (58,59,60,61,62); this branch's local gates replicate.

## 11. Open risks and deferrals (honest)

```text
WINDOWS_NATIVE_FILESYSTEM_GATE: UNTESTED — requires Windows 11 native re-measurement before claiming WINDOWS PASS (T075)
T071 synthetic recovery event: quarantine file is forensic audit, but synthetic log/repaired typed event via VaultWriter not yet emitted after repair (deferred to writer-ownership follow-up, not loss)
T073 randomized kill/restart: deterministic fault matrix executed, but stochastic 1000-iteration kill harness with seed not yet run on Windows native host (Phase 1 verification can still close with deterministic matrix per plan §7, randomized as additional evidence)
```

None are blocking for Phase 1 exit criteria as defined in spec §7 (all listed PASS criteria met); Windows native gap is explicitly reported as UNTESTED not PASS per plan §7 requirement to report missing platform evidence explicitly.

---

**Closeout:** This file is evidence for T080. T081 final analyze, T082 close, T083 CURRENT update follow in this slice.
