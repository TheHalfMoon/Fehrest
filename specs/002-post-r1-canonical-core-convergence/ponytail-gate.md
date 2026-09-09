# Ponytail Gate — Spec 002 (T045 implementation necessity)

**Status:** PASS — 2026-09-09 Slice A (T041–T045)
**Spec:** `002-post-r1-canonical-core-convergence`
**Conformance input:** `docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md`
**Analyze input:** `specs/002-post-r1-canonical-core-convergence/analyze.md` (post-Slice-A)
**Method:** `docs/19-ENGINEERING-METHOD.md §2 Ponytail` — requirement → reuse check (Fehrest? std? platform? existing dep? smaller correct?) → rights/security/benchmark/authorization
**Cost:** `COST=ZERO` — no model API, no paid service, no heavy local model download

## Necessity verdict

**KEEP** the Phase 1 convergence work.

It protects canonical, unrecomputable state. It is not optional polish. The Phase T truth reconciliation (T041–T044) confirms the gap is real: without Spec 002, canonical writes are `fs::write` not crash-aware, event durability is undefined, typed versioning and upcasting are absent, writer ownership is a `bool` guard not a capability, and startup integrity is documented not implemented — all irreplaceable state under `Recovery Model §1 principle 1` and `I-6`/`F-CORE-02`. Deferring would ship founder-selected scope on a durability lie. No alternative plan satisfies `FR2-003..006` at lower cost than the specified minimal slices; cost-caveat verdict demands durability without expansion, not deferral.

## Reuse before invention (evidence: /tmp/fehrest-r1v11 materialized ed79)

### Single-writer

Existing `Vault` / `WriteLock` is present (`src/vault.rs:292-321`, `create_new(true)` atomic, `WriterLocked` visible, no auto-steal). Phase T already satisfies `FR2-007/009`.

```text
QUESTION: Does Spec 002 need a new lock framework?
EVIDENCE:  WriteLock exists and passes kill tests (second_writer_fails_visibly, stale not stolen).
DECISION=REUSE
NEW_LOCK_FRAMEWORK=NO
RATIONALE: Adding a framework would increase concurrency surface, violate minimization, and need a failure-condition exception not justified by measurement. Strengthen API boundary (capability type), not mechanism.
```

### Canonical write

Phase T `add_object` is `fs::write(target, content)` (direct, not atomic-replace). It is sufficient for experiment but not for product crash-awareness.

```text
QUESTION: How to make object replacement crash-aware?
PONytail ORDER:
  1. Rust std + existing primitives (fs, io, tempfile pattern manual)
  2. Existing admitted crate (serde/serde_json/sha2/uuid/rusqlite already in Cargo.toml)
  3. New small crate only if measurement proves 1+2 insufficient
EVIDENCE: Plan §3 required measurement T049 on Windows + Linux before helper selection; until then std likely sufficient.
DECISION=PREFER STD (same-filesystem temp file + complete write + flush/sync + rename + parent-dir sync where contract supports, cleanup after known outcome)
NEW_DEPENDENCY_TARGET=0
REJECT: storage engine (SQLite/MDB) to replace Markdown object replacement — violates open canonical (F-CORE-02), adds indirection, needs a `NEW_RUNTIME_DEPENDENCY` decision not yet justified.
```

### Event schema

Existing stack: `serde 1 + serde_json 1 + sha2` already pinned; `Event {seq, kind, subject, detail, prev_hash, hash}` with `detail: String` free-form exists.

```text
QUESTION: Need versioned envelope + typed payloads (FR2-011/012)?
EVIDENCE: detail is bounded 16KiB but free-form; no schema_version; no typed variant; hash canonical order is ad-hoc string `"{seq}|{kind:?}|{subject}|{detail}|{prev}"`.
PONytail:
  KEEP serde/serde_json (serialization correctness + JSON escaping)
  ADD minimal versioned envelope: {schema_version: u32, payload: enum<Typed>} via existing serde tag, plus per-version frozen hash serialization
  REJECT protobuf / Cap'n Proto / FlatBuffers — would add codegen, schema compiler, and binary framing without measured durability/size failure (spec §8: if JSONL fails measured needs, invoke failure condition; do not silently change format). Std approach covers 1MiB vault eventualities at lower cost.
```

### Recovery

Recovery Model already defines required failure classes; Phase T implements 0 of the startup sequence (§2 `vault.json` absent, torn-tail not quarantined, gap/chain not fail-closed before writer).

```text
QUESTION: How much recovery to build?
EVIDENCE: Required: torn tail detection/quarantine (FR2-015), mid-log gap fail-closed (FR2-016/T069), hash-chain fail-closed (T070), forensic bytes before destructive cleanup (FR2-021), synthetic/interrupted reason distinction (3.5), checkpoint-loss none/canonical (3A.8).
DECISION=Implement ONLY Recovery Model §3.2,3.3,3.4,3.5,3A.8 + plan §6 before-writable-open sequence.
REJECT: generic transaction manager, two-phase commit, WAL — not required by acceptance scenarios AS2-1..2-8, would hide authority and add complexity.
```

### Vault identity / format

```text
QUESTION: Minimal identity metadata?
EVIDENCE: Phase T vault is `root.join(".fehrest").is_dir()` only — no vault_id/format_version (see conformance §3 row).
DECISION=ADD only currently required machine-owned metadata such as {vault_id (UUIDv7), format_version: u32, created_by_version: String} as JSON next to control dir; no cloud/collaboration fields.
REJECT: pre-designing sync/CRDT/cloud fields — no evidence, violates Ponytail SHRINK.
```

## Explicit deferrals (reaffirmed after Slice A evidence, no widening)

```text
memory curator            DEFER Phase 4+ (conformance §4.2 — durable memory journal/CLI write surface is not Phase 1)
graph                     DEFER Phase 3 gate (Spec 004 GI-CAP, then 005; no graph production module in 002)
vectors                   DEFER benchmark gate (no vector default; Qdrant/Chroma remain benchmark-only)
incremental indexing      DEFER Phase 2 (003) — B-12 remains UNTESTED until incremental exists; no silent PASS
MCP / agent gateway       DEFER Phase 5 (007); no Cedar/MCP/authorization gateway here
automatic memory          DEFER Phase 4+ per FOUNDER_AUTHORIZATION REJECT for Spec 002
agent runtime             REJECT as a core concern (Fehrest is what agents connect to, not framework)
sandbox platform          REJECT as a core concern (compare/adapt OpenSandbox/E2B/Daytona, not build)
web acquisition           DEFER until a measured need (Firecrawl/LlamaIndex not default 1–5 deps)
UI (v0/Tauri/canvas)      DEFER Phase 7 (009) — headless core remains complete without UI (I-16)
plugin architecture       REJECT for this feature (no plugin system in v1; isolation seam preserved SRC-043)
context compression LLMLingua / model-assisted  DEFER Phase 6 only after benchmark freeze
```

No deferred system may be added merely to solve the no-paid-API policy (per Founder cost policy §1 list: graph production integration now REJECT, not moved to 002).

## Necessity decision matrix (Phase 1 slices B–F)

| Requirement | Needs to exist? | Already in Fehrest? | In std/platform/approved dep? | Smaller correct path? | Decision |
|---|---|---|---|---|---|
| vault_id/format_version file | Yes (FR2-001) | No (only .fehrest dir) | std `fs` + serde can write/read JSON | No independent crate needed | **WRITE with std+serde** |
| crash-aware `write → fsync → rename → dir fsync` | Yes (FR2-003/004) | Partial (direct fs::write) | `std::fs::File::sync_all`, `rename`, `File::open(dir).sync_all` on Unix + measured Windows path | Manual temp pattern first | **STD PRIMITIVES, measure Windows semantics at T049** |
| fault-injection seam | Yes (FR2-005/T051) | No | test-controlled injected failure enum, no prod dep | N/A (test-only) | **TEST-ONLY INJECTION, zero runtime dep** |
| writer capability type `VaultWriter<'a>` etc. | Yes (FR2-008/AS2-3) | No (bool guard) | Rust lifetime + newtype wrapper around &Vault with WriteLock proof | No crate | **NEWTYPE/LIFETIME wrapper around existing WriteLock** |
| typed event payloads + schema_version + canonical hash freeze | Yes (FR2-011/012/013) | No (detail:String) | serde tagged enum + frozen per-version hash fn (string interpolation order fixed) | No protobuf | **SERDE TAG + FROZEN HASH FN** |
| golden historical fixture + upcasting | Yes (FR2-017/AS2-6) | No | `read → if version==1 → into v2 in-mem, no rewrite` | N/A | **READ-TIME UPCAST, fixture bytes immutable** |
| torn-tail quarantine + gap/chain fail-closed + startup gate | Yes (FR2-015/016/019/T066–T071) | No | `read_all` with detection, quarantine file write, `verify()` before writable open | N/A | **EXISTING verify() + QUARANTINE FILE + gated open_write** |
| new DB/vector/graph/Cedar/async/unsafe | — | — | — | — | **REJECT (unsafe forbid in lib.rs, no network/async)** |

## Security non-minimization (must remain green through Spec 002 — invariant, not negotiable)

Ponytail may not remove or weaken — verified against `src/locator.rs`, `src/identity.rs`, `src/vault.rs`, `src/envelope.rs`, `docs/02-THREAT-MODEL` :

```text
root confinement                 (locator::open_confined reject + canonicalise check, vault.rs RESERVED_DIRS)
post-open identity verification  (locator::read_verified — handle read then identity::read_id, fail IdentityMismatch)
writer ownership                 (WriteLock O_EXCL, WriterLocked visible, no auto-steal — strengthen, not replace)
canonical durability/recovery    (Recovery Model §3.1 quarantine not delete, §3.2 torn preserve before truncate, §5 audit events log/repaired)
event integrity checks           (EventLog::verify seq contiguity + prev_hash + recomputed hash, Gap vs Broken distinct, broken reported at_seq)
provenance + honest chain claim  (unkeyed chain is Tamper-Evidence not Auth — no MAC invented, consistent full rewrite test preserved AS2-7)
resource bounds                  (limits::* MAX_* as local safety, never commercial quota, LimitExceeded not silent discard, prefer coalescing/dedup per G3-M5)
negative security claims         (12 items in THREAT-MODEL §7.1: OS root, same-user, human auth, full rewrite, injection immunity, secret DLP, multi-user, sync, Cedar, MCP, cap-std, derived corruption — none silently weakened)
allowlist ingestion              (vault.rs SUPPORTED_EXTENSIONS allowlist + reserved exclusion, never indexing .fehrest/.git)
```

Any Ponytail proposal that would reduce these gates **FAILS CLOSED** — e.g., removing `is_reserved_component` to “simplify”, skipping `read_verified` on `Derived` hint reads, or auto-stealing stale `writer.lock` would be `CLASS D` security-semantic and requires dedicated adversarial review + Founder authorization, not minimization.

## Dependency target

```text
NEW_RUNTIME_DEPENDENCIES=0  (reaffirmed after Slice A measurement — std + existing serde/sha2/uuid/rusqlite/bundled sufficient)
```

Any deviation requires a written dependency decision with:

```text
REQUIREMENT
WHY_STD_OR_EXISTING_IS_INSUFFICIENT (measured, not claimed)
LICENSE / PROVENANCE (+observed upstream license survival)
SECURITY / ADVISORY STATE (cargo audit / RUSTSEC)
FOOTPRINT (disk/RAM/VRAM, binary size)
MAINTENANCE_HEALTH (bus factor, release cadence, yanking history)
EXACT PIN / VERSION DECISION
EXIT_STRATEGY (how to remove if it rots)
```

Otherwise `NEW_RUNTIME_DEPENDENCY=REJECT`. For T049–T053 the measurement is filesystem rename idempotence under contention and `File::sync_all` availability per platform — both provable with std. If a future helper like `tempfile 3.x` were truly needed for Windows `UpdateFileAttributes` precision, its decision would be written before adoption, and `unsafe_code = forbid` would still hold.

## T045 verdict

```text
PONYTAIL_GATE= PASS (KEEP, with reuse before invention provably exercised)
SLICE_A_CONFORMANCE_REQUIRED=YES → satisfied by PHASE_T_IMPLEMENTATION_CONFORMANCE.md
ANALYZE_REQUIRED=YES → satisfied by updated analyze.md post-Slice-A
SECURITY_NON_MINIMIZATION=PASS
DEFERRED_SYSTEMS_REAFFIRMED=8 (memory curator, graph, vectors, MCP, agent runtime, sandbox, web acquisition, UI/plugins)
NEW_DEPENDENCY=0
FAILURE_ROUTING_ARMED: canonical loss→stop before Phase 2; unsupported rename→ record limitation; event JSONL durability failing→ invoke Failure Conditions F, not silent format swap
NEXT= T046 minimal vault identity/version metadata schema (dependency-ready) + T049 native replacement semantics measurement
```
