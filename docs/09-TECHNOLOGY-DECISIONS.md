# J. Technology Decisions (ADRs)

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Each ADR states context, decision, alternatives rejected with reasons, consequences, and **the finding that would reverse it**. An ADR without a reversal condition is dogma.

Statuses: `PROPOSED` (awaiting review) · `OPEN` (decision deliberately not yet made) · `PROVISIONAL` (direction set, pending named evidence) · `CONDITIONAL` (resolved by another decision) · `ACCEPTED` (post-review only).

| # | Decision | Status |
|---|---|---|
| [0001](#adr-0001--canonical-state-is-open-files-plus-an-append-only-event-log) | Canonical state is open files + append-only event log | PROPOSED |
| [0002](#adr-0002--editor-architecture-open--prototype-gated) | Editor architecture | 🔄 **OPEN / PROTOTYPE-GATED** (reopened in R1) |
| [0003](#adr-0003--graph-intelligence-runtime-integration-shape) | Graph Intelligence runtime integration shape | 🔄 **PROVISIONAL** — pending GI-BENCH |
| [0004](#adr-0004--object-identity-is-fehrest-allocated-and-opaque) | Object identity is Fehrest-allocated UUIDv7 | PROPOSED (evidence re-grounded in R1) |
| [0005](#adr-0005--fehrest-adapts-harness-event-patterns-without-depending-on-the-harness-runtime) | Adapt harness event patterns, not the runtime | PROPOSED |
| [0006](#adr-0006--sqlite-is-the-derived-store-and-only-the-derived-store) | SQLite is the derived store, and only that | PROPOSED |
| [0007](#adr-0007--retrieval-is-lexical-first-vectors-are-optional) | Retrieval is lexical-first; vectors optional | PROPOSED |
| [0008](#adr-0008--memory-is-bitemporal-with-deterministic-resolution) | Memory is bitemporal with deterministic resolution | PROPOSED |
| [0009](#adr-0009--agents-address-objects-by-id-never-by-path) | Agents address objects by ID, never by path | PROPOSED |
| [0010](#adr-0010--core-implementation-language) | Core implementation language | **OPEN** |
| [0011](#adr-0011--desktop-shell) | Desktop shell | **OPEN** |
| [0012](#adr-0012--crdt-adoption-is-editor-dependent) | CRDT adoption is editor-dependent | 🔄 **CONDITIONAL** (reclassified in R1) |
| [0013](#adr-0013--storage-layout-provisional) | Physical storage layout | 🔄 **PROVISIONAL** — semantic categories first |

---

## ADR-0001 — Canonical state is open files plus an append-only event log

**Context.** Fehrest must satisfy [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default), [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended), [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) and [I-9](01-ARCHITECTURE-CONSTITUTION.md#i-9--export-does-not-depend-on-fehrest-infrastructure): knowledge lives locally, in open specified formats, and must be recoverable without Fehrest.

**Decision.** Canonical state is exactly: Markdown + YAML frontmatter files, original attachment bytes, an append-only JSONL event journal, append-only JSONL memory assertions, and JSON sidecars. Everything else is derived and deletable ([D](03-CANONICAL-DATA-MODEL.md), [E](04-DERIVED-DATA-MODEL.md)).

**Rejected alternatives.**
- *Database-canonical with file export* — inverts [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default); the vault becomes a database with a directory of stale copies beside it.
- *Files-only, no event log* — history cannot be recomputed from files, so audit, replay and provenance ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)) become impossible.
- *Git as the event log* — attractive but wrong: git records file states, not typed semantic events with actors and scopes, and requiring git makes it a hard dependency of a system that must work without one.

**Consequences.** Two write paths (files and journal) must be kept consistent under crash. JSONL is verbose. Full text search requires derived indexing. All accepted; recovery specified in [N](13-RECOVERY-MODEL.md).

**Reverses if.** JSONL cannot meet durability or size budgets at a decade of events → replace with a specified append-only binary format, which [I-5-as-amended](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) explicitly permits given a spec and a lossless exporter.

---

## ADR-0002 — Editor architecture: OPEN / PROTOTYPE-GATED

**Status: REOPENED in F1-R1 ([R1-02](reviews/F1-R1-RECONCILIATION.md), [R1-03](reviews/F1-R1-RECONCILIATION.md), [R1-04](reviews/F1-R1-RECONCILIATION.md)).** The F1 decision — *"v1 editing is Markdown-native on CodeMirror 6; BlockSuite is deferred"* — is **withdrawn**. It was reached on incomplete evidence and an unproven impossibility argument.

**Why the F1 decision was withdrawn.**

*Incomplete evidence.* F1 established that the standalone `toeverything/blocksuite` mirror is stale (last sync 2025-07-07; `@blocksuite/store` unpublished since 2025-07-01 at `0.22.4`) and concluded the editor was unmaintained. It missed that the implementation is actively developed inside `toeverything/AFFiNE` under `blocksuite/`, with editor feature work, a mobile fix, toolchain upgrades and a **security** dependency bump landing through 2026-08-10 ([E-10.1](research/EVIDENCE_LOG.md#e-101--the-evidence-f1-missed-the-affine-subtree-is-active)). The distribution path is stale; the editor is not. That distinction changes the decision.

*Unproven impossibility.* F1 argued that lossless rich-editor↔Markdown round-trip requires preserving CRDT operation history, therefore any sidecar becomes the real canonical document, therefore the gate is unpassable. This conflated six separable concerns and treated collaboration machinery as document meaning. It was never demonstrated ([D §7](03-CANONICAL-DATA-MODEL.md#7-the-rich-editor--canonical-file-question-open)).

**Decision.** The editor is chosen by an **executable bake-off**, specified in [18-EDITOR-GATE](18-EDITOR-GATE.md) and executed at [Phase 3E](15-IMPLEMENTATION-PHASES.md#phase-3e--editor-bake-off-gate).

| Candidate | Substrate |
|---|---|
| **A** | CodeMirror 6 — Markdown-native; canonical bytes are the document model |
| **B** | **Maintained AFFiNE `blocksuite/` subtree at a pinned commit** — never the stale standalone package |
| **C** | ProseMirror / Tiptap / Milkdown — **only** if A and B both leave a documented gap |

Scoring: canonical/open-file fidelity 30% · maintenance burden 20% · rich editing 15% · performance 10% · install size 10% · security surface 5% · agent editability 5% · future canvas 5%. Weights fixed before evaluation.

Elimination regardless of score: silent data loss, content loss on crash, or a sidecar that must carry document content.

**What is NOT reopened.** The constitutional requirement stands: whatever wins, canonical artifacts must remain open, specified, locally readable and losslessly exportable ([I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended)), and derived state must remain rebuildable ([I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)). A candidate that cannot satisfy those is eliminated, however capable.

**Consequences of reopening.** No editor may be assumed by downstream design. [Phase 7](15-IMPLEMENTATION-PHASES.md#phase-7--desktop-application) scope is gate-dependent. [ADR-0012](#adr-0012--crdt-adoption-is-editor-dependent) (CRDT/Yjs) becomes editor-dependent. [ADR-0011](#adr-0011--desktop-shell) is partly editor-dependent. Phases 0–3 are unaffected — they are CLI-only and touch no editor.

**Closes when.** Phase 3E produces a successor ADR with per-candidate measurements. An inconclusive result is a legitimate outcome and must be reported as such rather than resolved by aggregate score.

---

## ADR-0003 — Graph Intelligence runtime: integration shape

**Status: PROVISIONAL — pending [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) ([R1-06](reviews/F1-R1-RECONCILIATION.md), [R1-07](reviews/F1-R1-RECONCILIATION.md)).**

**The capability/implementation split (R1-06).** Two separate things must not be conflated:

```
GRAPH INTELLIGENCE:       CORE CURRENT PRODUCT HYPOTHESIS — EXPLICITLY FALSIFIABLE
GRAPHIFY_PYTHON_RUNTIME:  REPLACEABLE IMPLEMENTATION CANDIDATE
```

Fehrest's thesis holds that understanding relationships beyond lexical search materially improves agent continuation. *That capability* is a core **current product hypothesis** — testable, and removable on evidence ([F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)). *Graphify* is the leading candidate implementation of it, not a permanent part of Fehrest's identity. Candidate implementations: upstream Graphify sidecar · adapted Graphify modules · bundled persistent worker · later native reimplementation · a different extractor if benchmarks prove it superior.

**Context.** Three integration shapes were considered: bundle Python in-process, invoke a CLI per operation, or run a managed long-lived process.

**Provisional decision.** A **managed long-lived worker**, started lazily, read-only and path-confined to the vault, no credentials, network features disabled, supervised with restart-and-backoff, idle shutdown, resource caps.

**Reasoning from PRELIMINARY measurement.** Cold `import graphify.extract` ≈ **4,451 ms**; warm ≈ **276 ms**; bare interpreter ≈100 ms ([E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-preliminary)). Per-operation invocation costs ~376 ms of pure overhead even warm, and the cold path would make first use appear broken. A long-lived process pays this once per session.

**Why this is provisional and not decided.** These figures are single-machine, single-corpus, Windows, cold-cache ([R1-07](reviews/F1-R1-RECONCILIATION.md)). The cold/warm gap is large enough (~16×) that measurement noise is an implausible explanation, so the *direction* is solid. But the choice among lazy worker, preloaded worker, background process and adaptation depends on incremental-update latency, memory under concurrency, and behaviour across corpus *types* — none of which has been measured. **[GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) must run before this ADR is finalised.**

**Explicitly not decided here:** whether to port Graphify to a native language. F1 argued against on the grounds that startup, not throughput, was the binding constraint. That reasoning holds for the data available, but the data is one corpus. **Do not port Graphify** ([R1-06](reviews/F1-R1-RECONCILIATION.md)); revisit only if GI-BENCH shows throughput or packaging is genuinely binding.

**Rejected alternatives.**
- *In-process Python (embedded interpreter)* — couples Fehrest's process to a 130 MB / 32-package dependency tree and puts hostile-input parsers inside the TCB ([T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities)).
- *Per-operation CLI invocation* — refuted by the startup measurement.
- *Port to a native language now* — premature. Explicitly forbidden until GI-BENCH evidence justifies it.
- *Require a user-installed Graphify* — an install failure would silently disable a core capability.

**Consequences.** ~200–300 MB installer delta with a bundled runtime ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)) — mitigated by making Graph Intelligence an **optional capability install**. A second process to supervise, and IPC to design. An independent update channel is required, since the app and worker cannot share a release cadence given upstream CVE tracking.

**Finalised when.** GI-BENCH reports across 4 vault sizes × 5 corpus types × 10 operations × concurrency levels.

**Reverses if.** GI-BENCH shows throughput or incremental latency is the binding constraint rather than startup; **or** packaging proves untenable on a target platform; **or** [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is falsified and per-parser isolation is required — in which case the answer is likely WASM-isolated parsers, not a rewrite.

**Does not reverse on implementation cost alone.** A weak result from *this* implementation means replace *this* implementation. Whether the **capability** itself survives is a separate question, decided by [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) — which explicitly permits redesign or removal if graph-assisted understanding shows no material benefit over simpler local retrieval at acceptable cost.

---

## ADR-0004 — Object identity is Fehrest-allocated and opaque

**Context.** [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) requires identity to survive rename and move. Graphify supplies node IDs that look usable.

**Decision.** Identity is a Fehrest-allocated **UUIDv7**, stored in the file's own frontmatter, immutable for the object's life. Graphify node IDs appear only in a rebuildable mapping table and never as a key in canonical state.

**Reasoning — re-grounded in F1-R1 ([R1-05](reviews/F1-R1-RECONCILIATION.md)).** F1 justified this by citing upstream bugs. **Those bugs are fixed** (#2614 in 0.9.40; #811, #1033 and the #550 root cause all resolved, now guarded by contract and property tests), and citing them was wrong. The conclusion stands on structural grounds instead, which is a stronger position because upstream fixes cannot erode it:

1. **Path-derived.** File node IDs follow the spec `{parent_dir}_{stem}` — a function of location. Rename or move changes the ID.
2. **Scheme-versioned.** Upstream explicitly rejected an alternative ID scheme because it "would rewrite every file and symbol id and force a full-rebuild migration." An identifier whose scheme is expected to change across versions cannot anchor durable references.
3. **Rebuild-sensitive.** Incremental updates can retain stale IDs until a forced rebuild.

None of these is a defect; all follow from what an extractor ID is for — addressing nodes within one build of one graph. That is simply not durable object identity. Adopting such an ID would violate [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) by construction ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)).

**Generalised.** This applies to **any** extractor, not to Graphify specifically — formalised as [G-ID-1…G-ID-4](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities).

**Rejected alternatives.** Path as identity (breaks on rename — the exact failure [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) forbids); content hash (changes on every edit); UUIDv4 (no time locality for index/log scans); ULID (equivalent properties, less standardised — tie broken by RFC 9562 status); Graphify node id (above).

**Consequences.** Fehrest writes to user files to allocate identity — a real intrusion, mitigated by lazy allocation on first meaningful interaction and by configurability. Frontmatter stripped by another tool loses identity; recovery is by content similarity, presented as a user decision, never guessed ([N](13-RECOVERY-MODEL.md)).

**Reverses if.** Users reject frontmatter injection outright → fall back to a vault-level path↔id map, accepting weaker rename survival and losing the "identity travels with the file" property. Strictly worse; only if user rejection is decisive.

---

## ADR-0005 — Fehrest adapts harness event patterns without depending on the harness runtime

**Context.** DeepSeek Harness solves Fehrest's event-plane problems at specification quality across 45 subsystem documents ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)).

**Decision.** Adopt the patterns; take **no runtime dependency** on the harness or on Cordis.

**Adopted:** derived-not-stored agent-visible history; one event type with two backends (JSONL canonical, SQLite derived); non-truncating crash repair via a synthetic terminator no producer emits; header metadata outside the event vocabulary; merge-extensible vocabulary; branded non-interchangeable identifiers; approval as a log-only asked/decided pair failing closed; oversized output → locator, with "source is not access control" and "a name is not a path"; honest partial-enforcement reporting; package-owned runtime invariants.

**Rejected:** Cordis as a framework, the TS agent loop, plugin runtime, model adapters, compaction engine.

**Reasoning for rejecting Cordis.** Making an external meta-framework load-bearing contradicts *"the user's knowledge must survive Fehrest itself."* A memory OS that cannot boot without a third-party plugin framework has a shorter effective lifespan than the knowledge it stores. The brief's own instruction applies: do not introduce unstable dependencies because their architecture is elegant.

**Consequences.** The patterns must be reimplemented, losing TypeScript's declaration merging and branded types — replaced by the host language's type system plus runtime invariant checks. Divergence from upstream improvements must be tracked manually.

**Reverses if.** Reimplementation proves materially harder than expected **and** Fehrest's core language is TypeScript **and** Cordis is demonstrably stable — in which case a narrowly scoped dependency on the event-log package alone could be argued. The framework-wide dependency does not reverse.

---

## ADR-0006 — SQLite is the derived store, and only the derived store

**Decision.** One SQLite database holds all required derived state (object index, links, FTS5, memory projection) plus optional D2 mappings. WAL, `synchronous=NORMAL`, `foreign_keys=ON`, single writer. **No canonical state in SQLite.**

**Reasoning.** `synchronous=NORMAL` is safe *because* the store is derived: power-loss corruption costs a rebuild, not data. This is [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) paying for itself in write throughput. Corruption becomes an availability problem rather than a security one ([T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes)).

**Rejected.** SQLite as canonical (violates [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default)/[I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended)); separate databases per concern (cross-store transactions, more corruption surface); CozoDB (interesting Datalog+graph, but unproven for this and would make a young engine load-bearing); embedded KV store (loses SQL and FTS5 for no gain).

**Reverses if.** Write contention makes single-writer untenable at scale → shard by concern, still derived. Or FTS5 fails a measured budget → Tantivy for search only, SQLite retained for structure.

---

## ADR-0007 — Retrieval is lexical-first; vectors are optional

**Decision.** Retrieval order: identity → structured property → FTS5/BM25 → graph expansion → *optional* vectors → RRF fusion. Vectors are D3, off by default.

**Reasoning.** Three independent arguments.
1. **Constitutional** — embeddings need a model ([I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api)).
2. **Engineering** — sqlite-vec's current release line is `v0.1.10-alpha.*` ([E-12](research/EVIDENCE_LOG.md#e-12--vector-store-maturity)); alpha alone disqualifies a required component.
3. **Empirical** — the only prose-memory benchmark reported for the graph donor shows it **tying** dense RAG (76% vs 76%, LongMemEval-S n=50), with its real wins in recall and cost ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)). Neither approach dominates, so vectors must earn inclusion by measurement rather than convention.

RRF is chosen for fusion because it is deterministic, rank-only, and needs no score normalisation across incomparable scales.

**Rejected.** Vector-first (fails all three arguments); vector-only (no exact lookup, no temporal filtering, no abstention signal); graph-only (measurement does not support graph dominance for prose).

**Reverses if.** [B-3](10-BENCHMARK-PLAN.md) shows vectors materially beating lexical+graph on Fehrest's own corpus → promote to D2 default-on **when a stable release exists**. Note this is a promotion of *default*, never of *requirement*.

---

## ADR-0008 — Memory is bitemporal with deterministic resolution

**Decision.** Every memory carries valid time (`valid_from`/`valid_until`) and recorded time (`recorded_at`). Current state is resolved by a deterministic total ordering with explicit abstention and explicit contradiction ([F §4](05-MEMORY-MODEL.md#4-bitemporality)).

**Reasoning.** Single-axis temporality cannot answer "what did we believe last month," which is exactly the question asked when auditing a wrong agent decision — a core Fehrest promise ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)). Dynamic state tracking is one of LongMemEval-V2's five measured abilities ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). And the failure it prevents — surfacing two conflicting values and letting a model guess — is the failure the product exists to fix.

`recorded_at` is system-assigned, which is what makes backdating impossible ([T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse)).

**Rejected.** Single-axis valid time (no belief archaeology); single-axis recorded time (cannot answer "what was true in March"); no temporality (the product's core failure mode); LLM-resolved conflicts (non-deterministic, unauditable, and forbidden on core paths by [R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).

**Consequences.** Wider indexes, more complex queries, and users must sometimes supply `valid_from`. No LLM, graph DB or vector store required.

**Reverses if.** Structured `payload` proves extractable for < 30% of real memories → deterministic resolution covers too little to matter and the model degrades to prose-first, which is much weaker. This is the main risk to this ADR and is measured in [B-4](10-BENCHMARK-PLAN.md).

---

## ADR-0009 — Agents address objects by ID, never by path

**Decision.** No agent-facing tool accepts a filesystem path. Agents pass object IDs; core resolves ID→path internally. No `read_file`, no `write_file`, no shell, no network tool ([G §3.1](06-AGENT-MODEL.md#31-what-fehrest-deliberately-does-not-expose)).

**Reasoning.** This eliminates the entire path-traversal and symlink attack class **at the interface**, rather than defending against it at every call site ([T-7](02-THREAT-MODEL.md#t-7--path-traversal), [T-8](02-THREAT-MODEL.md#t-8--symlink-and-junction-attacks)). Validation is a defence that must be perfect everywhere; removing the parameter is a property. It also makes scope enforcement trivial, since an ID resolves to a known object with a known scope while a path must be classified.

Adopts the donor's two rules verbatim: a location is not an authorization token, and a suggested name is not a path ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)).

**Rejected.** Path-based with validation (correct-by-vigilance rather than by construction; one missed call site is a vault escape); chroot/jail only (does not address scope, only containment); full filesystem access for "convenience" (abandons [I-10](01-ARCHITECTURE-CONSTITUTION.md#i-10--agents-receive-explicitly-bounded-access) entirely).

**Consequences.** Agents cannot explore the vault as a filesystem; they must discover via search and list. This is less familiar and may be less ergonomic — the accepted cost, and the primary risk to this ADR.

**Reverses if.** Agents provably cannot work usefully without filesystem semantics → design a scoped, core-mediated file tool that still resolves through IDs internally and never accepts a caller-supplied path.

---

## ADR-0010 — Core implementation language

**Status: OPEN — deliberately not decided.**

**Context.** The core must implement identity, the event log, the memory projection, retrieval, the compiler, and the policy chokepoint. Constraints: single-binary desktop distribution, must supervise a Python sidecar, must be memory-safe in the TCB, must reimplement patterns from a TypeScript donor.

**Candidates.**

| Option | For | Against |
|---|---|---|
| **Rust** | Memory-safe TCB; excellent SQLite/fuzzing/single-binary story; pairs with Tauri; `cargo-fuzz` for the parser/log surface | Slower iteration; donor patterns are TS; UI needs a separate stack |
| **TypeScript (Node/Bun)** | Direct pattern transplant from the donor; one language with the UI; fastest iteration | Weaker isolation guarantees in the TCB; heavier runtime; supply-chain surface |
| **Go** | Simple concurrency, fast builds, easy single binary | Weakest ecosystem fit for editor/UI; fewer relevant donors |

**Why left open.** The right answer depends on [ADR-0011](#adr-0011--desktop-shell) and on whether the founder's velocity or the TCB's safety properties dominate — a founder decision, not an architectural deduction. Deciding it here on my own preference would be exactly the false confidence this package is meant to avoid.

**Weak recommendation:** Rust core + TypeScript UI, on the grounds that the TCB should be memory-safe and the parser/event-log surfaces are the fuzzing targets. Explicitly not a decision. See [Q-2](16-OPEN-QUESTIONS.md).

---

## ADR-0011 — Desktop shell

**Status: OPEN.**

**Candidates.** Tauri 2 (Apache-2.0, active, capability system usable as boundary B1 — [SRC-041](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)); Electron (mature, heavy, weaker default isolation); native per platform (best integration, 3× the work); CLI-first with a later GUI.

**Weak recommendation:** Tauri 2, primarily for its capability allowlist as a real boundary rather than for bundle size. But the brief lists it as `STUDY → likely USE`, and inheriting "likely" as a decision would be exactly the unearned assumption this document is meant to prevent. A genuine ADR is owed at Phase 3.

**Note.** [Phase 0–2](15-IMPLEMENTATION-PHASES.md) are CLI-only, so this decision is not on the critical path and can be made with more information.

---

## ADR-0012 — CRDT adoption is editor-dependent

**Status: CONDITIONAL — resolved by the Editor Gate ([R1-09](reviews/F1-R1-RECONCILIATION.md)).** F1 classified Yjs as a flat `DEFER`. That was too coarse: whether a CRDT enters v1 is not an independent choice, it is a **consequence of [ADR-0002](#adr-0002--editor-architecture-open--prototype-gated)**.

**Decision.**

| Editor Gate outcome | CRDT status |
|---|---|
| **Candidate B wins** (maintained AFFiNE BlockSuite subtree) | Yjs arrives **as part of the substrate**. Not a separate adoption decision. The gate's ADR must then specify which CRDT state is canonical, which is collaboration-specific, and which is transient ([18-EDITOR-GATE §4](18-EDITOR-GATE.md#4-the-round-trip-proof-obligation)) |
| **Candidate A or C wins** (Markdown-native / other) | Yjs stays **deferred** until collaboration or sync independently justifies it |

**Hard constraint, independent of outcome: collaboration must NOT be added to the MVP in order to justify a CRDT** ([R1-09](reviews/F1-R1-RECONCILIATION.md)). If a CRDT arrives, it arrives because the winning editor uses it for local document state — not because Fehrest acquired a collaboration requirement it did not have.

**Health vs necessity.** Yjs is MIT and actively released — `yjs@13.6.32`, published 2026-08-04 ([E-11](research/EVIDENCE_LOG.md#e-11--yjs-and-codemirror-are-healthy-the-crdt-is-not-the-stale-part)). There is **no maintenance objection**. The only question is necessity, which the Editor Gate answers.

**Still rejected regardless of outcome.** Two CRDT runtimes simultaneously. Automerge alongside Yjs requires a dedicated ADR proving a need neither satisfies alone.

**Consequences while conditional.** No design may assume a CRDT is present, and none may assume it is absent. Where the two differ — chiefly external-concurrent-modification handling ([N §3.10](13-RECOVERY-MODEL.md#310-concurrent-editor-external-modification)) — the plan specifies the no-CRDT behaviour as the floor, since that is the weaker case and must work anyway.

---

## ADR-0013 — Storage layout: provisional

**Status: PROVISIONAL ([R1-17](reviews/F1-R1-RECONCILIATION.md)).** F1 presented a concrete `.fehrest/` hierarchy without an ADR justifying it. A physical layout committed before storage and recovery prototypes exist is a guess wearing a specification's clothes.

**Decision.** Fix the **semantic storage categories** now; defer the physical layout to a successor ADR after the Phase 1–2 storage and recovery prototypes.

**Semantic categories** (these are stable and may be designed against):

| Category | Class | Rebuildable? |
|---|---|---|
| Canonical identity | canonical | No |
| Canonical events | canonical | No |
| Canonical explicit memory | canonical | No |
| Canonical content + attachments | canonical | No |
| Schema / version state | canonical | No |
| Derived search index | derived | Yes |
| Derived graph | derived | Yes |
| Derived vectors | derived | Yes |
| Cache (extracted text, thumbnails, summaries) | derived | Yes |

**The load-bearing constraint, independent of layout ([R1-16](reviews/F1-R1-RECONCILIATION.md)):** canonical and derived state must be **separable by directory**, so that derived state can be deleted wholesale without touching canonical state. The layout in [D §2](03-CANONICAL-DATA-MODEL.md#2-storage-categories-provisional-layout) satisfies this and is a **worked illustration, not a commitment**.

**Explicitly warned against:** reading "`.fehrest/` is disposable." It is not. It contains canonical event and memory state. Only the derived subtree is disposable.

**Finalised when.** Phase 1–2 prototypes report on write patterns, crash behaviour, backup ergonomics, and how sync tools and `git` interact with the directory.
