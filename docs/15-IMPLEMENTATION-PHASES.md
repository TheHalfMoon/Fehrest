# P. Implementation Phases

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

**No implementation is authorized.** This document defines what implementation *would* look like once the review gates in the brief are cleared.

---

## 1. Structure

> **PHASE ORDER CORRECTED IN F1-R2 ([R2-10](reviews/F1-R2-RECONCILIATION.md)).** F1's ordering built the whole architecture and then, at Phase 6, ran the experiment that decides whether the product should exist. **[Phase T](#phase-t--headless-rust-thesis-proof-slice) is inserted immediately after Phase 0** as the first authorized implementation: a headless Rust slice that tests the smallest version of the thesis before the expensive architecture is built.

The plan builds **one vertical slice, end to end, before any horizontal expansion**:

```
local Markdown file → stable identity → deterministic ingestion → graph relation
→ FTS retrieval → temporal memory → context compilation → MCP query
→ source provenance → restart → deterministic reconstruction
```

Phases 0–6 build that slice **CLI-first, with no UI**. UI begins at Phase 7, only after the slice is proven. **This is now a constitutional property, not merely a sequencing preference** — [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) requires the Core to remain fully operable without a UI at every point, permanently.

**Language is decided.** Founder decision D-1 makes **Rust the canonical implementation language for Fehrest Core** ([ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) — `ACCEPTED`). Every phase below implements in Rust. TypeScript/React appear only at Phase 7 and only as presentation. Python appears only behind the optional sidecar boundary ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)).

**Method is decided.** Every phase's production work passes the Spec Kit → Ponytail → implement → verify → converge → review loop specified in [S — Engineering Method](19-ENGINEERING-METHOD.md) ([ADR-0014](09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail)). Neither is a runtime dependency ([R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).

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
- **[B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) — measure real multi-agent event volume by class ([R2-12](reviews/F1-R2-RECONCILIATION.md)).** Capture or reconstruct representative traces; count potential events per class per active day. No event-tiering, retention, compaction or checkpoint-cadence parameter may be frozen before this reports.
- Decide [ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) (shell). *([ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) is closed by founder decision D-1 — Rust.)*
- Stand up CI: the four dependency scanners, CodeQL, Semgrep with the custom rules from [L §2.1](11-SECURITY-VERIFICATION-PLAN.md#21-custom-semgrep-rules--the-invariants-that-decay-silently).
- **Stand up the Spec Kit + Ponytail development workflow** ([S](19-ENGINEERING-METHOD.md)) as CI/governance tooling, outside the product dependency graph ([R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).
- Build C-SMALL and C-TEMPORAL corpora.

**Non-goals.** Any product code. Any UI. Any schema commitment.

**Deliverables.** Cross-platform measurement report; H-2 verdict; **B-0 event-volume report**; ADR-0011 accepted; sidecar confinement prototype; CI skeleton; development workflow in place; two corpora; **Research Freeze declared** ([registry §12](research/FEHREST_SOURCE_REGISTRY.md#12-research-freeze)).

**Exit criteria.**
1. Measurements reproduced on all three platforms, with deviations documented.
2. H-2 answered: linear, or the superlinear term quantified.
3. **B-0 reports measured event volume by class**, replacing the unvalidated 500/day assumption.
4. ADR-0011 moved from OPEN to ACCEPTED.
5. `test_sidecar_no_egress` passes on all three platforms, **or** the platform gap is documented as an accepted risk with the compensating control named.
6. CI green on an empty repository.

**Rollback.** None — nothing built.

---

## Phase T — Headless Rust thesis-proof slice

> **ADDED IN F1-R2 ([R2-10](reviews/F1-R2-RECONCILIATION.md)).** This is **the first authorized implementation** — after Phase 0, and after every review gate and explicit founder authorization. **It is defined here, not built here.**

**Objective.** Prove or falsify **the smallest version of the Fehrest thesis before building the expensive architecture.** Nothing in this phase exists to be impressive; it exists to make [B-7a](10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) runnable at the earliest possible moment.

**Scope — deliberately minimal, and every line of it Rust:**

- Rust CLI. No UI, no shell, no webview.
- Ordinary local Markdown / open files as the corpus.
- Fehrest UUID identity in frontmatter ([D §3](03-CANONICAL-DATA-MODEL.md#3-object-identity)).
- SQLite as the derived store.
- FTS5 candidate retrieval.
- **Minimal deterministic temporal / supersession model** — valid time, recorded time, supersession, and the §4.2 resolver ladder. Not the full memory taxonomy.
- **Explicit durable memory writes only.** No candidate extraction, no triage, no promotion pipeline, no classification.
- **Only the T1 audit events the proof itself requires.** Not the full vocabulary.
- **Context-package served-item manifest** ([H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1)) — included because it is what makes the experiment auditable and because [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) has no mechanism without it.
- Deterministic bounded Context Compiler.
- Baseline harnesses: plain agent, repository-native docs, raw stuffing, BM25, and the **Karpathy-style maintained LLM Wiki** ([§3.1 ladder](10-BENCHMARK-PLAN.md#31-the-baseline-ladder)).

#### Security floor — added in G3 ([G3 reconciliation](reviews/G3-SECURITY-RECONCILIATION.md))

The slice above is the *thesis* boundary. G3 adds the **security** boundary it must satisfy, because a proof slice that establishes signal on an unsound base establishes nothing transferable:

```
+ explicit single-user OS-account trust model        (C section 3.1)
+ no agent path capable of minting user authority    (G section 2.4)
+ root-confined filesystem read/write discipline     (E section 12.1)
+ post-open UUID verification                        (E section 12.1)
+ canonical scope as authorization authority         (E section 12.2)
+ derived paths treated only as locator hints        (E section 12)
+ SQLite / FTS5 hardening baseline                   (E section 13)
+ valid supersession graph                           (F section 6.1)
+ inter-process single-writer discipline             (D section 9)
+ honest hash-chain / tamper-evidence semantics      (C section 6.1)
+ typed trust envelope + canonical serialization     (G section 4.3)
+ per-item / package budget atomicity                (H section 4)
+ bounded local resource safety                      (O section 13)
+ supported-content ingestion allowlist              (D section 10)
+ no network · no process execution · no plugins
```

**Every item is a property of code that is already being written for the thesis proof**, not an additional subsystem. That is the test of whether the security floor is correctly scoped: containment discipline, post-open verification and a single-writer lock are *how* the slice reads and writes files, not extra components beside it.

**Explicitly NOT in this phase** — and none of it may be added for convenience:

```
desktop UI · editor · Graphify production sidecar · vectors
automatic memory promotion · T2/T3 compaction engine · cloud · sync
mobile · marketplace · plugins · Spark · DuckDB · TimesFM
```

**And, added in G3 — no security subsystem beyond the declared threat model:**

```
no MAC / keychain / TPM / signing service        (C section 6.1 — honest claim instead)
no user-authentication subsystem                 (C section 3.1 — OS account is the root)
no TTY / PTY detection as authentication         (explicitly forbidden)
no Cedar policy engine                           (SEC-R15 — minimum deny-by-default instead)
no cap-std adoption decision                     (SEC-R14 — evaluated at implementation)
no MCP                                           (SEC-R16 — deferred to the MCP gate)
no external notarization or cloud authority      (SEC-R12 — limitation documented instead)
```

**The temptation this list exists to name:** a security review makes it feel responsible to add mechanisms. Each line above would *exceed* the declared threat model rather than satisfy it, and a mechanism whose key custody is the same OS account it defends against is ceremony, not security ([C §7.1](02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make)).

An item leaves this list **only** if it becomes strictly required to run the experiment, and only with that requirement written down first.

**Relationship to Phases 1–5.** Phase T is a **thin vertical cut through** them, not a parallel implementation. Its components are the genuine beginnings of the production Core, built to production correctness standards for the narrow surface they cover; Phases 1, 2, 4 and 5 then broaden that surface. **It is not a throwaway prototype and must not be rewritten from scratch** — Ponytail's first two questions ([S §2](19-ENGINEERING-METHOD.md#2-the-ponytail-necessity-gate)) apply to Fehrest's own code before they apply to anyone else's.

**Dependencies.** Phase 0. Explicit founder implementation authorization.

**Acceptance criteria.**
1. `test_identity_survives_rename` on the narrow surface, including the [D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics) per-platform cases.
2. `test_nuke_and_rebuild_equivalence` ([B-9](10-BENCHMARK-PLAN.md#b-9--nuke-and-rebuild-equivalence)) green.
3. **[B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability)** green, or its measured drift characterised and the remedy chosen before the digest is depended on.
4. `test_bitemporal_resolution_deterministic` on the minimal model.
5. `test_manifest_is_permanent` and `test_context_determinism`.
6. `test_no_python_required` ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)) and `test_core_suite_headless` ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)) — both trivially satisfiable here, and both must stay green forever after.
7. **[B-7a](10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) executed and a verdict reported.**

**Exit criteria.** All of the above, **plus a written verdict of `SIGNAL` / `NO SIGNAL` / `INCONCLUSIVE`** with the evidence.

**The decision this phase forces.**

| B-7a verdict | Consequence |
|---|---|
| `SIGNAL` | Proceed to Phase 1. The production architecture is worth its cost |
| `INCONCLUSIVE` | **A legitimate outcome.** Proceed with the reason recorded, or extend the pilot. It does **not** falsify the thesis ([R2-10](reviews/F1-R2-RECONCILIATION.md)) |
| `NO SIGNAL` on a well-powered contrast | **Stop and reconsider the product before building the expensive architecture.** This is the entire reason the phase exists |

**Rollback.** The slice is small and additive; nothing downstream depends on it yet.

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

**Dependencies.** Phase 0, **Phase T** (which already establishes identity, the frontmatter round-trip and a minimal event log; Phase 1 broadens them rather than reimplementing them).

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

**Added in F1-R2.** The **derivation registry** ([E §10](04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data)) — artifact / inputs / `deriver_id` / `deriver_version` — lands here, because it is what makes the incremental path in this phase provably equivalent to the rebuild path. **Projection checkpoints** ([E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints)) land here with their validity and discard rules.

**Benchmarks.** [B-1](10-BENCHMARK-PLAN.md), [B-2](10-BENCHMARK-PLAN.md), [B-9](10-BENCHMARK-PLAN.md), **[B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability)**. D1 incremental **< 200 ms p95** at C-MED; D1 full index **< 60 s** at C-MED.

**Security gates.** C-PATH passes on all platforms. `no-derived-to-canonical` rule active. **`no-canonical-ref-to-disposable`** active ([D §5.5](03-CANONICAL-DATA-MODEL.md#55-spilled-locators-have-a-declared-durability-class)).

**Additional acceptance criteria (F1-R2).**
6. **`test_incremental_equals_full`** — a mutation sequence applied incrementally yields the same observable result as a rebuild from the identical final state, within documented tolerances ([R2-07](reviews/F1-R2-RECONCILIATION.md)).
7. **`test_invalidation_completeness`** — every artifact whose recorded inputs include a mutated identity is invalidated.
8. **`test_checkpoint_is_disposable`** — deleting every checkpoint loses nothing; an invalid checkpoint is discarded and recovery falls back correctly ([R2-08](reviews/F1-R2-RECONCILIATION.md)).
9. **`test_filesystem_identity_matrix`** — the [D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics) per-platform matrix, including Windows case-only rename and macOS NFC/NFD equivalence ([R2-09](reviews/F1-R2-RECONCILIATION.md)).

**Exit criteria.** B-9 green in CI and **kept green from here to the end of the project**; B-12 green or its remedy chosen on measurement; D1 budgets met; C-PATH zero escapes; the filesystem identity matrix green on all three platforms.

**Rollback.** Derived state is disposable by construction — rollback is deleting a directory.

---

## Phase 3 — Graph sidecar

**Objective.** Structural understanding as strictly optional derived state, and proof that its absence degrades nothing but recall.

> **PHASE 3 IS NOW TWO STAGES ([R2-15](reviews/F1-R2-RECONCILIATION.md)).** F1 built the sidecar, IPC, packaging, Python lifecycle and incremental pipeline **and then** measured whether the graph helps ([B-3](10-BENCHMARK-PLAN.md#b-3--retrieval-quality-by-stage)). Under that ordering, [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)'s "remove the capability" branch could only ever fire after its full cost had been paid — which makes an explicitly falsifiable hypothesis expensive to falsify, and therefore unlikely to be.

### Phase 3A — Capability experiment (throwaway)

**Scope.** [B-13 — GI-CAP](10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment). A **static, offline, hand-run** graph extraction into a flat artifact, used to compare `FTS + structured + temporal memory` against the same plus static graph expansion, on a **code-heavy** and a **Markdown/knowledge-heavy** corpus.

**Explicitly NOT built in 3A:** supervisor, IPC, packaging, Python lifecycle management, incremental graph pipeline, graph explorer. None of it is needed to answer the question, and building it first is what made the question expensive.

**Exit.** GI-CAP reports measured retrieval quality and, where feasible, continuation outcome.

**Decision.** If the capability does not materially improve outcomes at acceptable cost, **v1 removes it here** — before the integration exists ([F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)). Removal touches no canonical record.

### Phase 3B — Production integration

**Entry criterion — hard.** GI-CAP reported, and the capability was retained on that evidence.

**Scope.** Sidecar lifecycle: lazy start, supervision, backoff, idle shutdown, resource caps; confinement (read-only, path-confined, no network, no credentials); IPC and schema validation of every response; graph ingestion and the **rebuildable** `graph_node_map`; incremental update via graph diff; communities; CLI `graph`, `related`.

**Non-goals.** Vectors. Memory. Agents. UI. Re-exporting any Graphify tool.

**Dependencies.** Phase 2, then Phase 3A.

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

**Scope.** Memory JSONL log; the record schema ([F §3](05-MEMORY-MODEL.md#3-the-memory-record)); **the four event-sourced semantic axes** ([F §3.3](05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model)); **orthogonal scope selectors** ([F §3.4](05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice)); deterministic bitemporal resolution ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)); supersession; **`PENDING` lifecycle semantics** ([F §5.5](05-MEMORY-MODEL.md#55-pending-confirmation-semantics)); the promotion pipeline (deterministic stages only in this phase) with the **AI-OFF safe classification default** ([F §5.1](05-MEMORY-MODEL.md#51-which-stages-are-deterministic)); memory projection into SQLite; CLI `remember`, `recall`, `memory audit`, `memory as-of`, `memory pending`.

**Non-goals.** Model-assisted promotion (Phase 6). Agents. UI. Vectors.

**Dependencies.** Phase 2 (projection). Phase 3 optional.

**Acceptance criteria.**
1. `test_memory_requires_provenance` — rejected at the **storage layer**, not the UI.
2. `test_bitemporal_resolution_deterministic` — property test vs a naive reference over random histories.
3. `test_resolution_monotone_and_order_stable` — monotone in `recorded_at`; stable under input reordering.
4. `test_status_transitions_are_event_sourced` + `test_axes_are_independent` — each of the four axes is projected from events, and no API returns a collapsed status.
5. `test_supersession_retains_original` — superseded memories remain queryable.
6. `test_abstention` — no matching memory returns `NO_ANSWER`, never a guess.
7. `test_contradiction_surfaced` — unresolvable conflicts are returned as contradictions, **including incomparable-scope conflicts**.
8. **`test_provenance_cannot_be_spoofed`** — evidence must be a subset of what the session's **served-item manifests** record as served, **including the in-grant-but-not-served negative case** ([R2-02](reviews/F1-R2-RECONCILIATION.md)).
9. **`test_confidence_is_not_truth_authority`** — mutating `confidence_diagnostic` across its full range never changes a resolution result ([R2-04](reviews/F1-R2-RECONCILIATION.md)).
10. **`test_pending_never_authoritative`**, `test_pending_is_visible`, `test_pending_cannot_supersede` ([R2-06](reviews/F1-R2-RECONCILIATION.md)).
11. **`test_scope_cross_project_poisoning`**, `test_scope_incomparable_yields_contradiction`, `test_vault_global_requires_user_authority` ([R2-05](reviews/F1-R2-RECONCILIATION.md)).
12. **`test_ai_off_does_not_auto_type`** — with AI off, unclassified prose is queued as `PENDING`, never auto-promoted ([R2-16](reviews/F1-R2-RECONCILIATION.md)).

**Benchmarks.** [B-4](10-BENCHMARK-PLAN.md) on C-TEMPORAL: current-state accuracy must be **100%** (this is resolution, not retrieval — anything less is a bug). [B-5](10-BENCHMARK-PLAN.md) rules-only promotion quality.

**Security gates.** C-POISON passes: all poisoned memories traceable and bulk-revocable by provenance.

**Exit criteria.** B-4 current-state accuracy 100%; stale-memory usage 0%; structured-`payload` extraction rate measured and reported.

**Decision point.** If `payload` is extractable for < 30% of real memories, [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) reverses toward prose-first resolution — materially weaker, and a founder decision ([Q-6](16-OPEN-QUESTIONS.md)).

**Rollback.** Memory log is append-only and separable; disabling memory reverts to Phase 3.

---

## Phase 5 — Context compiler and agent gateway

**Objective.** The defining feature, plus the boundary that makes it safe to expose.

**Scope.** The ten-stage deterministic pipeline ([H §4](07-CONTEXT-COMPILER-SPEC.md#4-pipeline)); RRF fusion; budget allocation with mandatory omission reporting; package digests, the **permanent served-item manifest** and `context/compiled` events; **three-outcome replay** ([H §3.3](07-CONTEXT-COMPILER-SPEC.md#33-replay-outcomes-are-explicit--three-results-never-two)); capability grants over orthogonal scope dimensions; the single authorization chokepoint; scope filtering **during** retrieval including graph expansion; approval flow with branded ids; **spilled-locator durability classes** ([D §5.5](03-CANONICAL-DATA-MODEL.md#55-spilled-locators-have-a-declared-durability-class)); the MCP server with the tool surface from [G §3](06-AGENT-MODEL.md#3-tools); **the single core response envelope across every read path** ([G §4.1](06-AGENT-MODEL.md#41-one-envelope-every-read-path)); CLI `fehrest context`.

**Non-goals.** UI. Model-assisted stages. Sync. Plugins.

**Dependencies.** Phases 2 and 4. Phase 3 optional.

**Acceptance criteria.**
1. `test_deny_by_default` — empty grant permits nothing, including read.
2. `test_chokepoint_coverage` — every tool handler reachable **only** through authorization (coverage assertion, not convention).
3. `test_grant_immutable_in_session` — no path widens a grant mid-session.
4. `test_scope_isolation` — zero cross-project leakage, including via graph expansion, on deliberately entangled projects.
5. `test_no_path_from_agent` — no agent-facing tool accepts a path ([ADR-0009](09-TECHNOLOGY-DECISIONS.md#adr-0009--agents-address-objects-by-id-never-by-path)).
6. `test_context_determinism` — 100 runs on unchanged state produce one digest.
7. **`test_context_package_replay`** — every historical package reports `IDENTICAL` / `DIVERGED` / `UNRECONSTRUCTABLE` **with the correct reason**; a divergent replay reported as success fails the build ([R2-01](reviews/F1-R2-RECONCILIATION.md)).
8. `test_omission_honesty` — `omitted` counts match reality.
9. `test_provenance_completeness` — unsourced items **exactly 0**.
10. `test_subagent_subset` — property test over random delegation trees.
11. **`test_no_unlabelled_content_path`** — the **full** agent-facing read surface returns the core envelope with trust level, provenance, the four axes and supersession intact ([R2-03](reviews/F1-R2-RECONCILIATION.md)).
12. **`test_manifest_is_permanent`** — after full T2 compaction, every historical manifest still enumerates its served items.
13. **`test_canonical_never_references_disposable`** — no T1 or T2 event references a `DERIVED_DISPOSABLE` locator ([R2-11](reviews/F1-R2-RECONCILIATION.md)).

**Benchmarks.** [B-6](10-BENCHMARK-PLAN.md): latency budgets, ≥ 20× compression, 100% determinism.

**Security gates.** **C-INJECT passes: zero capability changes, zero unapproved tool executions.** C-PATH, C-TAMPER, scope isolation all green. This is the phase where [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority) is proven or disproven.

**Exit criteria.** All ten acceptance tests green; B-6 budgets met; C-INJECT zero boundary violations.

**Rollback.** The MCP server is a separable surface; disabling it reverts to a local-only system.

---

## Phase 6 — Vertical proof

**Objective.** Prove the thesis. This is the phase that decides whether Fehrest should exist.

**Scope.** Build C-PROJECT (a real multi-month project history) and the held-out task set — **written before the compiler is tuned**; **pre-register the [B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark) statistical design and its derived sample size before any data is collected**; implement the full [baseline ladder](10-BENCHMARK-PLAN.md#31-the-baseline-ladder) as adapters in one shared harness; run B-7b with **both Fehrest arms** (compiled-context-only and as-shipped); optional model-assisted promotion and compiler stages, measured against the deterministic baseline; full recovery and chaos testing; scale testing at C-LARGE and **measured** 10-year growth ([B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement)-derived, not assumption-derived).

**Non-goals.** UI. New features of any kind.

**Dependencies.** Phase 5. Phase T's B-7a verdict, which this study confirms or overturns.

**Acceptance criteria.**
1. **[B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark): Fehrest beats the plain-agent-with-file-tools arm by the pre-registered margin, at the pre-registered power — and beats the [maintained-LLM-Wiki baseline](10-BENCHMARK-PLAN.md#31-the-baseline-ladder), which is the strongest simple alternative.**
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

**Continuous from Phase T:** B-9 nuke-and-rebuild green in CI; all four dependency scanners green; Semgrep custom rules green; the provenance ledger complete and CI-verified; every donor-derived file carrying a provenance header; **`test_no_python_required` and `test_core_suite_headless` green** ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface), [I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)).

**Every phase must satisfy:** all prior phases' tests still pass; `AI OFF` passes the full core suite; the vault remains readable by the previous version for minor changes; the residual-risk statement is updated; and **every production change passes the Spec Kit → Ponytail → implement → verify → converge → review loop** ([S](19-ENGINEERING-METHOD.md)).

The `AI OFF` requirement repeated every phase is deliberate. It is the invariant most likely to erode gradually — one convenient model call at a time — and the only defence is testing it continuously rather than at the end. **The same argument now applies to I-16 and I-17**, for the same reason: a UI-only affordance and a Python-only code path are each added one convenience at a time.
