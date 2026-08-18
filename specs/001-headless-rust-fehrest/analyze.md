# Analyze — Cross-Artifact Consistency Gate

**Date:** 2026-08-18 · **Status:** PASS — implementation may begin

Non-destructive consistency check across [spec](./spec.md), [clarify](./clarify.md), [plan](./plan.md), [dependencies](./dependencies.md), [ponytail-gate](./ponytail-gate.md), [checklist](./checklist.md) and [tasks](./tasks.md), against the frozen architecture and the Phase T authorization boundary.

---

## Gate results

```
SPEC_KIT_CONSTITUTION_ALIGNED = YES
SPEC_COMPLETE                 = YES
CLARIFY_COMPLETE              = YES
PLAN_COMPLETE                 = YES
CHECKLIST_COMPLETE            = YES
TASKS_COMPLETE                = YES
PONYTAIL_GATE_COMPLETE        = YES
ANALYZE_BLOCKERS              = 0
FROZEN_ARCHITECTURE_CONFLICTS = 0
UNAUTHORIZED_FEATURES_IN_PLAN = 0
```

---

## Coverage — every functional requirement reaches a task and a checklist item

| FR | Task | Checklist |
|---|---|---|
| FR-001..003 vault, allowlist, exclusions | T003 | CL-57..60 |
| FR-004..005 identity, path ≠ identity | T002 | CL-04 |
| FR-006 duplicate UUID | T007 | CL-18 |
| FR-007 root containment | T005 | CL-11..15 |
| FR-008 post-open verification | T006 | CL-16, CL-17 |
| FR-009 locator is a hint | T005, T028-30 | CL-15 |
| FR-010 derived index | T009 | CL-05, CL-06 |
| FR-011 derived grants nothing | T013, T029 | CL-08, CL-24 |
| FR-012 SQLite hardening | T008 | CL-20..23 |
| FR-013 literal FTS | T010 | CL-25..27 |
| FR-014 rebuild loses nothing | T009 | CL-05 |
| FR-015..018 explicit memory, axes, basis, no confidence | T012 | CL-33, CL-36 |
| FR-019..020 resolver, as-of | T014, T015 | CL-29..32 |
| FR-021 supersession validation | T016 | CL-34, CL-35 |
| FR-022 PENDING excluded | T012, T014 | CL-36 |
| FR-023 event chain | T017 | CL-37, CL-38 |
| FR-024 single writer | T004 | CL-51..53 |
| FR-025..026 envelope | T019, T020 | CL-42..46 |
| FR-027 bounded compiler | T021 | CL-49 |
| FR-028 budget atomicity | T022 | CL-47, CL-48 |
| FR-029 manifest + evidence check | T023, T024 | CL-39..41 |
| FR-030 CLI | T026 | — |
| FR-031 resource bounds | T025 | CL-54..56 |

**Uncovered requirements: 0. Orphan tasks: 0.**

---

## Frozen-architecture conflict scan

Each `F-CORE-*` checked against plan and tasks:

| | Conflict? |
|---|---|
| F-CORE-01 local-first, zero services | None — no network dependency admitted |
| F-CORE-02 open canonical | None — Markdown on disk |
| F-CORE-03 Rust Core | None — single Rust package |
| F-CORE-04 path ≠ identity | None — separate types, no conversion |
| F-CORE-05 content is evidence | None — content is a value field |
| F-CORE-06 temporal memory | None — T014/T015 |
| F-CORE-07 orthogonal axes | None — four separate enums; T033 asserts confidence invariance |
| F-CORE-08 context compiler | None — T021..T024 |
| F-CORE-09 served-item manifest | None — built in the emit loop |
| F-CORE-10 derived has no authority | None — containment and identity implemented and tested **separately** |
| F-CORE-11 root of trust | None — no auth subsystem; K-21 tests the enforceable invariant |
| F-CORE-12 honest audit | None — chain tests assert detection, never authentication |
| F-CORE-13 single writer | None — T004 |
| F-CORE-14 safe serialization | None — length-prefixed; no injection-immunity claim |
| F-CORE-15 safety not quotas | None — CL-55 greps for quota concepts |
| F-CORE-16 ingestion allowlist | None — T003 |
| F-CORE-17 negative claims | None — CL-46, CL-38 |

**Conflicts: 0.**

---

## Unauthorized-feature scan

Every prohibited item searched across plan, tasks and structure:

```
UI · v0 · React · Tauri · editor · canvas · MCP · Cedar · Graphify
graph · petgraph · vectors · embeddings · CRDT · sync · collaboration
cloud · plugins · automatic memory · confirmation queue · dashboard
analytics · PDF · DOCX · OCR · audio · multi-user · remote service
telemetry · mandatory LLM
```

**Found in plan or tasks: none.** Each appears only in [ponytail-gate.md](./ponytail-gate.md) under DEFER, which records *why it is absent* — the correct place for it.

**`UNAUTHORIZED_FEATURES_IN_PLAN = 0`.**

---

## Ambiguity scan

No `[NEEDS CLARIFICATION]` markers remain. All ten clarification items resolved from canonical documents; five deferred with recorded reasons ([clarify.md](./clarify.md)).

---

## Findings — non-blocking, recorded

**A-01 · B-12 cannot run as specified.** [C-06](./clarify.md) defers incremental reindex, so the incremental-vs-fresh comparison has no incremental arm. Phase T instead tests **rebuild-vs-rebuild determinism**, which is a weaker property. **Reported as untested, never as passed** — the finding is recorded here rather than allowed to disappear into a green checklist.

**A-02 · Platform coverage will be partial.** The development host is Windows 11. Linux and macOS paths are written portably but **claims will be marked `PENDING_*` unless natively executed**. K-13 (junction/reparse) is Windows-specific and executable here; K-12 (symlink) may require privilege on Windows and is marked accordingly.

**A-03 · Byte budget, not token budget.** [C-09](./clarify.md). The Core cannot honestly report tokens without a tokenizer, and Phase T requires no model. The harness converts where a tokenizer legitimately exists. Recorded so no reader mistakes a byte budget for a token budget.

**A-04 · Five memory types, not eleven.** [Ponytail SHRINK](./ponytail-gate.md). The five carry every benchmark dimension; the rest would add vocabulary without a tested property.

**None of these blocks implementation.** Each is a scope limit that is recorded rather than hidden.

---

## Verdict

**`ANALYZE_BLOCKERS = 0`. Implementation authorized to begin at T001.**
