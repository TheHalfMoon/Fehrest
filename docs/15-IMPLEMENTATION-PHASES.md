# P. Implementation Phases

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

**No implementation is authorized.** This document defines what implementation *would* look like once the review gates in the brief are cleared.

---

## 1. Structure

The plan builds **one vertical slice, end to end, before any horizontal expansion**:

```
local Markdown file → stable identity → deterministic ingestion → graph relation
→ FTS retrieval → temporal memory → context compilation → MCP query
→ source provenance → restart → deterministic reconstruction
```

Phases 0–6 build that slice **CLI-first, with no UI**. UI begins at Phase 7, only after the slice is proven.

Two rules govern the whole plan:

1. **A phase cannot start until its predecessor's exit criteria are met.** Not "mostly met."
2. **Every phase's exit criteria are executable tests**, not judgements. A phase exits when CI says so.

Rule 2 is what prevents the failure the brief names: downstream work starting when predecessor invariants are unproven.

**Phase sizing note:** no duration estimates appear below. This plan has one measured data point about implementation velocity — none — and inventing week counts would be exactly the false precision this package is meant to avoid. Phases are sized by *scope and gate*, and sequencing is by dependency.

---

## Phase 0 — Foundation validation

**Objective.** Verify that the measurements this plan rests on hold beyond one machine, and close the decisions deliberately left open.

**Scope.**
- Re-run [E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint), [E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary), [E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-preliminary) on Windows, macOS and Linux.
- Measure extraction at 5K and 10K files to test [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) (linearity).
- Measure Docling's installed weight to settle its optional/required classification.
- Obtain LongMemEval-V2; reproduce at least one published baseline locally ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)).
- Prototype sidecar IPC and confinement (read-only, path-confined, no egress) on all three platforms.
- Decide [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) (language) and [ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) (shell).
- Stand up CI: the four dependency scanners, CodeQL, Semgrep with the custom rules from [L §2.1](11-SECURITY-VERIFICATION-PLAN.md#21-custom-semgrep-rules--the-invariants-that-decay-silently).
- Build C-SMALL and C-TEMPORAL corpora.

**Non-goals.** Any product code. Any UI. Any schema commitment.

**Deliverables.** Cross-platform measurement report; H-2 verdict; ADR-0010 and ADR-0011 accepted; sidecar confinement prototype; CI skeleton; two corpora; **Research Freeze declared** ([registry §12](research/FEHREST_SOURCE_REGISTRY.md#12-research-freeze)).

**Exit criteria.**
1. Measurements reproduced on all three platforms, with deviations documented.
2. H-2 answered: linear, or the superlinear term quantified.
3. ADR-0010 and ADR-0011 moved from OPEN to ACCEPTED.
4. `test_sidecar_no_egress` passes on all three platforms, **or** the platform gap is documented as an accepted risk with the compensating control named.
5. CI green on an empty repository.

**Rollback.** None — nothing built.

**Redesign trigger.** If H-2 is falsified badly (10K extraction > 3× projection), reopen [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) before writing any code that assumes the graph is affordable.

---

## Phase 1 — Canonical core

**Objective.** Identity, files, and the event log — the state that cannot be recomputed.

**Scope.**
- Vault creation, `vault.json`, format versioning.
- UUIDv7 allocation; frontmatter read/write with **verbatim unknown-field preservation**.
- Atomic file writes (temp + rename).
- Append-only JSONL event log with contiguous `seq` and hash chaining.
- T1/T2/T3 tiering ([D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)).
- Startup integrity sequence and repair: torn tail, gap, chain break, unterminated session ([N §2–3.5](13-RECOVERY-MODEL.md#2-startup-integrity-sequence)).
- Read-time upcasting skeleton with a v1 golden file ([M §3](12-MIGRATION-SCHEMA-EVOLUTION.md#3-event-and-memory-log-evolution)).
- CLI: `fehrest init`, `add`, `show`, `log`, `verify`.

**Non-goals.** Search. Graph. Memory. Agents. UI. Sidecar.

**Dependencies.** Phase 0.

**Acceptance criteria.**
1. `test_identity_survives_rename` — rename, move, case change; identity and history intact.
2. `test_unknown_frontmatter_preserved` — round-trip preserves unknown fields byte-for-byte.
3. `test_vault_is_self_contained` — copy to a clean machine; everything readable.
4. `test_chain_verification_detects_edit` — 100% detection across edit/truncate/reorder/splice.
5. `test_crash_recovery` — fault injection at every write point; **zero canonical loss**.
6. `test_unterminated_session_synthetic_close` — repaired sessions distinguishable from clean ones.
7. `test_no_actor_supplied_timestamp` (Semgrep) — `recorded_at` never from request data.

**Benchmarks.** Event append throughput; log verification time at 100K events.

**Security gates.** Fuzz the event-log record parser and the frontmatter parser (highest priority per [L §4](11-SECURITY-VERIFICATION-PLAN.md#4-fuzzing) — the log is the only unrecoverable component). C-MALFORMED passes. `no-secret-in-event` rule active.

**Exit criteria.** All acceptance tests green; fuzzers ≥ 24 h with no reachable crashes; a vault survives 1,000 randomised kill-and-restart cycles with zero canonical loss.

**Rollback.** Format is versioned from the first commit; no vault exists in the wild yet, so a breaking change here is free. This is the last phase where that is true.

---

## Phase 2 — Derived index and lexical retrieval

**Objective.** D1 derived state, and the proof that derived state is genuinely disposable.

**Scope.** SQLite schema; object/link/FTS5 indexing; incremental update on file change; content-hash staleness (never mtime); filesystem watch with debounce; reconciliation scan; full rebuild, resumable and cancellable; CLI `search`, `backlinks`, `reindex`, `doctor`.

**Non-goals.** Graph. Vectors. Memory. Agents. UI.

**Dependencies.** Phase 1.

**Acceptance criteria.**
1. **`test_nuke_and_rebuild_equivalence`** — delete all derived state, rebuild, identical query results. *The single most important test in the plan*; it is what makes [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) real and every index decision reversible.
2. `test_index_reconciliation` — injected index deletions are detected.
3. `test_external_modification` — git checkout and external edits re-index correctly.
4. `test_read_hash_consistency` — hash reflects the bytes actually read, under concurrent mutation ([T-9](02-THREAT-MODEL.md#t-9--filesystem-race-conditions)).
5. `test_sqlite_corruption_recovery` — corrupt the DB; automatic rebuild; zero canonical loss.

**Benchmarks.** [B-1](10-BENCHMARK-PLAN.md), [B-2](10-BENCHMARK-PLAN.md), [B-9](10-BENCHMARK-PLAN.md). D1 incremental **< 200 ms p95** at C-MED; D1 full index **< 60 s** at C-MED.

**Security gates.** C-PATH passes on all platforms. `no-derived-to-canonical` rule active.

**Exit criteria.** B-9 green in CI and **kept green from here to the end of the project**; D1 budgets met; C-PATH zero escapes.

**Rollback.** Derived state is disposable by construction — rollback is deleting a directory.

---

## Phase 3 — Graph sidecar

**Objective.** Structural understanding as strictly optional derived state, and proof that its absence degrades nothing but recall.

**Scope.** Sidecar lifecycle: lazy start, supervision, backoff, idle shutdown, resource caps; confinement (read-only, path-confined, no network, no credentials); IPC and schema validation of every response; graph ingestion and the **rebuildable** `graph_node_map`; incremental update via graph diff; communities; CLI `graph`, `related`.

**Non-goals.** Vectors. Memory. Agents. UI. Re-exporting any Graphify tool.

**Dependencies.** Phase 2.

**Acceptance criteria.**
1. `test_graphify_ids_are_not_identities` — no canonical record keys on a Graphify node ID.
2. `test_graph_absent_degrades` — with the sidecar disabled, **every** Phase 1–2 test still passes.
3. `test_sidecar_readonly` — sidecar cannot write anywhere in the vault.
4. `test_sidecar_no_egress` — zero outbound connections during a full extraction.
5. `test_sidecar_crash_recovery` — SIGKILL mid-extraction; resumes; no corruption.
6. `test_id_collision_surfaced` — a same-filename collision produces multiple mappings surfaced as ambiguity, never a silent pick ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)).
7. `test_schema_validation_rejects_malformed` — a hostile sidecar response is rejected, not ingested.
8. `test_startup_excludes_sidecar_import` — the 4,451 ms cold import never appears on the startup path.

**Benchmarks.** [B-1](10-BENCHMARK-PLAN.md) at C-MED and C-LARGE; [B-3](10-BENCHMARK-PLAN.md) ablation: **does graph expansion add recall over FTS alone?**

**Security gates.** Sidecar extraction fuzzing begins ([H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path)). Platform enforcement matrix accurate.

**Exit criteria.** All acceptance tests green; B-3 ablation reports the graph's measured contribution.

**Benchmarks (added in R1).** [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) runs here. **No packaging or runtime decision may be finalised before it reports** ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) is PROVISIONAL until then).

**Decision point.** If B-3 shows graph expansion adds no material recall gain over FTS + memory, or GI-BENCH shows cost is unacceptable for the benefit measured, invoke [failure condition F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost). It is graduated: a weak result from *one implementation* or *one retrieval configuration* means replace or retune that; a capability showing no material benefit at acceptable cost **across configurations and corpus types** permits **redesign or removal of Graph Intelligence from the core product hypothesis**. Removal touches no canonical record.

**Rollback.** Disable the sidecar; the system reverts to Phase 2 behaviour with no data loss.

---

## Phase 3E — Editor bake-off gate

> **ADDED IN F1-R1 ([R1-03](reviews/F1-R1-RECONCILIATION.md)).** F1 chose the editor by argument. R1 requires it be chosen by executable prototype. Full specification: [18-EDITOR-GATE](18-EDITOR-GATE.md).

**Objective.** Decide the editor architecture on measured evidence, producing an ADR that supersedes [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated).

**Scope.** Build the common corpus (`bench/editor/corpus/`) with expected-output fixtures; implement a minimal round-trip harness per candidate — **A** CodeMirror 6, **B** maintained AFFiNE `blocksuite/` subtree at a pinned commit, **C** only if A and B leave a documented gap; run the 24-item acceptance suite identically across candidates; score against fixed weights.

**Non-goals.** Building the actual Fehrest editor. Shipping UI. Canvas. Collaboration. This phase produces a **decision and throwaway prototypes**, not product code.

**Dependencies.** Phase 1 (identity, canonical files) so round-trip has something canonical to round-trip against. Independent of Phases 2–4; **may run in parallel**.

**Acceptance criteria.**
1. All 24 acceptance tests executed against every candidate, results recorded with raw measurements.
2. **P-1…P-6** verdicts recorded per candidate ([18-EDITOR-GATE §4.3](18-EDITOR-GATE.md#43-what-must-be-proven)).
3. Every fidelity deviation **enumerated** — no candidate scored on "mostly works."
4. Elimination conditions evaluated: silent data loss, content loss on crash (test 15), sidecar carrying document content (P-6).
5. Turkish/combining-mark idempotency verified for any candidate computing block identity from content (test 11).
6. Git-diff readability measured (test 18) — a one-word change must produce a minimal reviewable diff.
7. Successor ADR written, including the consequent status of [ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent) (CRDT/Yjs).

**Security gates.** Any candidate's dependency tree passes the [L §3](11-SECURITY-VERIFICATION-PLAN.md#3-dependency-and-supply-chain) scanners. For Candidate B, per-file license provenance is established for every vendored file before scoring is finalised.

**Exit criteria.** A decision with recorded evidence — **or** a recorded finding that no candidate clears the fidelity floor, which is a legitimate outcome requiring a scope conversation rather than a winner picked on aggregate score.

**Rollback.** Prototypes are throwaway. No canonical format is committed by this phase.

**Blocks.** [Phase 7](#phase-7--desktop-application). No UI work may begin until this gate closes.

---

## Phase 4 — Temporal memory

**Objective.** Bitemporal memory with deterministic resolution, provenance, and promotion.

**Scope.** Memory JSONL log; the record schema ([F §3](05-MEMORY-MODEL.md#3-the-memory-record)); event-sourced `epistemic_status`; deterministic bitemporal resolution ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)); supersession; the promotion pipeline (deterministic stages only in this phase); memory projection into SQLite; CLI `remember`, `recall`, `memory audit`, `memory as-of`.

**Non-goals.** Model-assisted promotion (Phase 6). Agents. UI. Vectors.

**Dependencies.** Phase 2 (projection). Phase 3 optional.

**Acceptance criteria.**
1. `test_memory_requires_provenance` — rejected at the **storage layer**, not the UI.
2. `test_bitemporal_resolution_deterministic` — property test vs a naive reference over random histories.
3. `test_resolution_monotone_and_order_stable` — monotone in `recorded_at`; stable under input reordering.
4. `test_status_transitions_are_event_sourced` — projected status always equals event-derived status.
5. `test_supersession_retains_original` — superseded memories remain queryable.
6. `test_abstention` — no matching memory returns `NO_ANSWER`, never a guess.
7. `test_contradiction_surfaced` — unresolvable conflicts are returned as contradictions.
8. `test_provenance_cannot_be_spoofed` — evidence must be a subset of what the session was served.

**Benchmarks.** [B-4](10-BENCHMARK-PLAN.md) on C-TEMPORAL: current-state accuracy must be **100%** (this is resolution, not retrieval — anything less is a bug). [B-5](10-BENCHMARK-PLAN.md) rules-only promotion quality.

**Security gates.** C-POISON passes: all poisoned memories traceable and bulk-revocable by provenance.

**Exit criteria.** B-4 current-state accuracy 100%; stale-memory usage 0%; structured-`payload` extraction rate measured and reported.

**Decision point.** If `payload` is extractable for < 30% of real memories, [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) reverses toward prose-first resolution — materially weaker, and a founder decision ([Q-6](16-OPEN-QUESTIONS.md)).

**Rollback.** Memory log is append-only and separable; disabling memory reverts to Phase 3.

---

## Phase 5 — Context compiler and agent gateway

**Objective.** The defining feature, plus the boundary that makes it safe to expose.

**Scope.** The ten-stage deterministic pipeline ([H §4](07-CONTEXT-COMPILER-SPEC.md#4-pipeline)); RRF fusion; budget allocation with mandatory omission reporting; package digests and `context/compiled` events; capability grants; the single authorization chokepoint; scope filtering **during** retrieval including graph expansion; approval flow with branded ids; the MCP server with the tool surface from [G §3](06-AGENT-MODEL.md#3-tools); the evidence envelope; CLI `fehrest context`.

**Non-goals.** UI. Model-assisted stages. Sync. Plugins.

**Dependencies.** Phases 2 and 4. Phase 3 optional.

**Acceptance criteria.**
1. `test_deny_by_default` — empty grant permits nothing, including read.
2. `test_chokepoint_coverage` — every tool handler reachable **only** through authorization (coverage assertion, not convention).
3. `test_grant_immutable_in_session` — no path widens a grant mid-session.
4. `test_scope_isolation` — zero cross-project leakage, including via graph expansion, on deliberately entangled projects.
5. `test_no_path_from_agent` — no agent-facing tool accepts a path ([ADR-0009](09-TECHNOLOGY-DECISIONS.md#adr-0009--agents-address-objects-by-id-never-by-path)).
6. `test_context_determinism` — 100 runs on unchanged state produce one digest.
7. `test_context_package_replay` — every historical package recompiles to its recorded digest, or reports the changed high-water mark.
8. `test_omission_honesty` — `omitted` counts match reality.
9. `test_provenance_completeness` — unsourced items **exactly 0**.
10. `test_subagent_subset` — property test over random delegation trees.

**Benchmarks.** [B-6](10-BENCHMARK-PLAN.md): latency budgets, ≥ 20× compression, 100% determinism.

**Security gates.** **C-INJECT passes: zero capability changes, zero unapproved tool executions.** C-PATH, C-TAMPER, scope isolation all green. This is the phase where [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority) is proven or disproven.

**Exit criteria.** All ten acceptance tests green; B-6 budgets met; C-INJECT zero boundary violations.

**Rollback.** The MCP server is a separable surface; disabling it reverts to a local-only system.

---

## Phase 6 — Vertical proof

**Objective.** Prove the thesis. This is the phase that decides whether Fehrest should exist.

**Scope.** Build C-PROJECT (a real multi-month project history) and the held-out task set — **written before the compiler is tuned**; implement all baseline arms as adapters in one shared harness; run [B-7](10-BENCHMARK-PLAN.md); optional model-assisted promotion and compiler stages, measured against the deterministic baseline; full recovery and chaos testing; scale testing at C-LARGE and 10-year simulated growth.

**Non-goals.** UI. New features of any kind.

**Dependencies.** Phase 5.

**Acceptance criteria.**
1. **[B-7](10-BENCHMARK-PLAN.md): Fehrest beats the plain-agent-with-file-tools arm by a margin exceeding the confidence interval.**
2. Zero constraint violations where the constraint was present in the package.
3. Repeated-known-failure rate below the plain-agent arm.
4. [B-8](10-BENCHMARK-PLAN.md) recovery: every [N](13-RECOVERY-MODEL.md) scenario recovers automatically or with one guided step, zero canonical loss.
5. [B-10](10-BENCHMARK-PLAN.md) scale: budgets met at C-LARGE; startup < 5 s with 10 years of simulated events.
6. All S-* security benchmarks pass.
7. `AI OFF` passes the entire core suite.

**Exit criteria.** All of the above, plus a written assessment of where Fehrest lost to a baseline and why.

**This is the falsification gate.** If criterion 1 fails, do not proceed to UI. Invoke [failure condition F-1](17-FAILURE-CONDITIONS.md) and reconsider the product. Building UI on an unproven thesis is how a project spends two years being beautiful and useless.

**Rollback.** N/A — this phase adds measurement, not architecture.

---

## Phase 7 — Desktop application

**Objective.** Make the proven slice usable by a human.

**Entry criteria — hard.** Phase 6 exit criteria met **in full**, **and [Phase 3E](#phase-3e--editor-bake-off-gate) closed with a decided editor ADR.** No UI work begins on an unproven thesis or an undecided substrate.

**Scope.** Desktop shell ([ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell)); **the editor chosen by Phase 3E**; vault browser; search UI; memory review and confirmation queue; agent session and audit views; provenance and trust-level display; onboarding including backup guidance; the UI capability boundary (B1) with **no raw filesystem API exposed to the webview**.

**Non-goals.** Canvas. Graph explorer. Database views. Plugins. Sync. Mobile.

**Acceptance criteria.** UI cannot bypass the authorization chokepoint; every budget in [O §3](14-PERFORMANCE-BUDGETS.md) met with UI attached; confirmation queue measured **< 5/day** in dogfooding ([O §10](14-PERFORMANCE-BUDGETS.md)); accessibility baseline (keyboard-complete, screen-reader labelled, WCAG AA contrast, no colour-only encoding); [H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work) tested in real use.

**Decision point.** If [H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work) is falsified — Markdown plus sidecars genuinely cannot support the work — [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated) reopens. Re-evaluate ProseMirror/Lexical **before** BlockSuite.

---

## Phase 8+ — Deferred

Not scheduled. Each requires its own ADR and a demonstrated need: canvas (JSON Canvas — format already chosen), graph explorer, vectors (only if [B-3](10-BENCHMARK-PLAN.md) justifies), sync and CRDT, structured/database views, plugins with WASI isolation, local model integration, OCR and transcription, mobile.

---

## 2. Cross-phase requirements

**Continuous from Phase 1:** B-9 nuke-and-rebuild green in CI; all four dependency scanners green; Semgrep custom rules green; the provenance ledger complete and CI-verified; every donor-derived file carrying a provenance header.

**Every phase must satisfy:** all prior phases' tests still pass; `AI OFF` passes the full core suite; the vault remains readable by the previous version for minor changes; and the residual-risk statement is updated.

The `AI OFF` requirement repeated every phase is deliberate. It is the invariant most likely to erode gradually — one convenient model call at a time — and the only defence is testing it continuously rather than at the end.
