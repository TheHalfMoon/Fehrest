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
| [0010](#adr-0010--core-implementation-language) | Core implementation language | ✅ **ACCEPTED — Rust** (founder decision D-1, F1-R2) |
| [0011](#adr-0011--desktop-shell) | Desktop shell | **OPEN** — deliberately *not* resolved by D-1 |
| [0012](#adr-0012--crdt-adoption-is-editor-dependent) | CRDT adoption is editor-dependent | 🔄 **CONDITIONAL** (reclassified in R1) |
| [0013](#adr-0013--storage-layout-provisional) | Physical storage layout | 🔄 **PROVISIONAL** — semantic categories first |
| [0014](#adr-0014--engineering-method-spec-kit--ponytail) | Engineering method: Spec Kit + Ponytail | ✅ **ACCEPTED** (founder decisions D-2, D-3, F1-R2) |
| [0015](#adr-0015--long-term-canonical-schema-compatibility) | Long-term canonical schema compatibility | 🔄 **OPEN — study framed** (F1-R2) |
| [0016](#adr-0016--derivation-lineage-and-projection-checkpoints) | Derivation lineage and projection checkpoints | **PROPOSED** (F1-R2) |

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

**Sequencing corrected in F1-R2 ([R2-15](reviews/F1-R2-RECONCILIATION.md)).** [GI-CAP (B-13)](10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) — a throwaway static-graph capability experiment with no supervisor, IPC, packaging, Python lifecycle or incremental pipeline — **runs before any production integration work begins** ([Phase 3A](15-IMPLEMENTATION-PHASES.md#phase-3a--capability-experiment-throwaway)). F1 built the integration and then measured the benefit, which made [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)'s removal branch payable only after its cost had been sunk. **Graph Intelligence remains a `CORE CURRENT PRODUCT HYPOTHESIS` that is `EXPLICITLY FALSIFIABLE`; Graphify remains an `OPTIONAL IMPLEMENTATION CANDIDATE`.** The reordering does not change either status — it makes the falsifiability affordable.

**Finalised when.** GI-CAP retains the capability, **and** GI-BENCH reports across 4 vault sizes × 5 corpus types × 10 operations × concurrency levels.

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

**Amended in F1-R2 ([R2-04](reviews/F1-R2-RECONCILIATION.md), [R2-05](reviews/F1-R2-RECONCILIATION.md)).** Two changes to the resolution half of this ADR:

1. **Resolution is deterministic but no longer *total*.** The ladder in [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution) compares one well-founded axis per rung and skips rungs where no comparison exists. Where nothing separates two candidates, the result is `CONTRADICTION` — the honest answer, and one the compiler already has a section for.
2. **Uncalibrated confidence is removed from the resolution path entirely.** F1's final tie-break let a model-produced float decide what Fehrest reported as true whenever principled rules ran out — importing exactly the non-determinism this ADR rejects in its own "Rejected" list, through the last rung.

**Reverses if.** Structured `payload` proves extractable for < 30% of real memories → deterministic resolution covers too little to matter and the model degrades to prose-first, which is much weaker. This is the main risk to this ADR and is measured in [B-4](10-BENCHMARK-PLAN.md). **`CONTRADICTION` being returned too often is not a reversal condition for the confidence removal** — it is an argument for more evidence-based rungs, never for restoring a number that has no evidential content.

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

**Status: ✅ ACCEPTED — Rust. Closed by founder decision D-1 in F1-R2.**

> This ADR was `OPEN` through F1 and F1-R1, deliberately, because the choice turned on a founder priority rather than an architectural deduction. **The founder has now made it.** The weak recommendation recorded in R1 — Rust core, TypeScript UI — is the decision, and it is recorded as a founder decision rather than as an architect's inference.

**Decision.** **Rust is the canonical implementation language for Fehrest Core.**

**Rust owns all correctness- and security-sensitive product logic:**

```
canonical domain model · stable identity · filesystem reconciliation
canonical write and recovery semantics · SQLite and storage · migrations
FTS integration · event and audit primitives · temporal memory
deterministic resolution · retrieval · context compilation · provenance
authorization · agent gateway · MCP server · CLI · recovery
every security-sensitive boundary
```

**TypeScript/React may be used for presentation and UI.** **No business-critical state semantic may be duplicated in TypeScript** — not memory resolution, not supersession, not authorization, not identity allocation, not any canonical write path. The UI renders what the Core decides.

**Python may be used only behind an explicit optional process boundary**, for hypothesis-gated donor capabilities such as Graph Intelligence ([ADR-0003](#adr-0003--graph-intelligence-runtime-integration-shape)). **Canonical Fehrest operation must not require Python.**

**Two invariants make this testable rather than aspirational** ([B](01-ARCHITECTURE-CONSTITUTION.md)):

- **[I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)** — if the desktop UI disappears, Fehrest remains operable through its Rust Core and CLI.
- **[I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)** — if Python disappears, canonical Fehrest knowledge, memory and recovery remain usable.

**Reasoning.** The TCB should be memory-safe, and the parser, event-log and reconciliation surfaces are exactly the fuzzing targets ([L §4](11-SECURITY-VERIFICATION-PLAN.md#4-fuzzing)). A memory OS that must outlive its own dependencies benefits from a single-binary distribution with no runtime to install. And the thesis — *the user's knowledge must survive Fehrest itself* — is better served by a Core with one language, one binary and no interpreter than by a stack whose correctness is spread across three runtimes.

**Rejected alternatives.**
- *TypeScript core* — fastest iteration and a direct transplant of the donor's TS patterns, but weaker isolation in the TCB, a heavier runtime, and a much larger supply-chain surface for a component that holds a decade of private knowledge.
- *Go core* — simple concurrency and easy single binaries, but the weakest ecosystem fit for the editor/UI seam and the fewest relevant donors.
- *Rust core with business logic mirrored in TypeScript for UI responsiveness* — rejected explicitly, because a mirrored state semantic is two semantics, and the one users see would win arguments it should lose.

**Consequences.** Donor patterns from a TypeScript source ([ADR-0005](#adr-0005--fehrest-adapts-harness-event-patterns-without-depending-on-the-harness-runtime)) must be reimplemented rather than transplanted, losing declaration merging and branded types — replaced by Rust's type system plus runtime invariant checks, which was already the plan. Iteration on UI-adjacent work is slower. The UI needs a separate stack, which [ADR-0011](#adr-0011--desktop-shell) still has to choose.

**What this decision does NOT decide.** **[ADR-0011](#adr-0011--desktop-shell) (desktop shell) remains OPEN.** Tauri 2 pairs naturally with a Rust core and remains the leading candidate, but "the Core is Rust" does not entail "the shell is Tauri" — that is a separate decision with separate evidence, and resolving it by association is exactly the unearned inference this package exists to prevent.

**Reverses if.** Rust proves unable to meet the interactive latency budgets in [O](14-PERFORMANCE-BUDGETS.md) — implausible, and would indicate a design fault rather than a language fault. Or the founder reverses D-1 explicitly. **Implementation velocity alone is not a reversal condition**; it was weighed and decided against.

---

## ADR-0011 — Desktop shell

**Status: OPEN — and deliberately NOT resolved by founder decision D-1.**

> **Explicitly stated in F1-R2.** D-1 decided the **Core language** ([ADR-0010](#adr-0010--core-implementation-language)), not the shell. Tauri 2 is written in Rust and pairs naturally with a Rust core, and that adjacency is exactly why the inference must be refused: "our core is Rust, therefore our shell is Tauri" is an association, not an argument. **Tauri 2 may remain the leading candidate; it is not a decision.**

**Candidates.** Tauri 2 (Apache-2.0, active, capability system usable as boundary B1 — [SRC-041](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)); Electron (mature, heavy, weaker default isolation); native per platform (best integration, 3× the work); CLI-first with a later GUI.

**Weak recommendation:** Tauri 2, primarily for its capability allowlist as a real boundary rather than for bundle size. But the brief lists it as `STUDY → likely USE`, and inheriting "likely" as a decision would be exactly the unearned assumption this document is meant to prevent. A genuine ADR is owed at Phase 3.

**Note.** [Phase 0](15-IMPLEMENTATION-PHASES.md#phase-0--foundation-validation), [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) and Phases 1–6 are headless, so this decision is not on the critical path and can be made with more information. [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) additionally guarantees it can never become one: the Core must work without any shell, permanently.

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

---

## ADR-0014 — Engineering method: Spec Kit + Ponytail

**Status: ✅ ACCEPTED — founder decisions D-2 and D-3, F1-R2.**

**Context.** Fehrest is built largely by AI coding agents against a specification-heavy planning package. Two failure modes follow directly from that: work that drifts from the specification because no artifact binds them, and code that accretes because generating a new implementation is cheaper for an agent than finding the existing one. Both are governance problems, and neither is solved by architecture.

**Decision.** Two development disciplines are adopted, and **neither is a Fehrest runtime dependency** ([R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)). Full specification: [S — Engineering Method](19-ENGINEERING-METHOD.md).

**D-2 — GitHub Spec Kit is the canonical specification-driven implementation workflow.**

```
constitution → specify → clarify → plan → checklist → tasks
             → analyze → implement → converge
```

The full production lifecycle is used where appropriate. **A reduced workflow may be used for small bounded work where the reduction is justified in writing** — an escape hatch that is recorded, not assumed, because an unjustifiable reduction is how a process becomes a formality.

**D-3 — Ponytail is the canonical implementation-minimisation / reuse-first discipline.** Before writing new code, in order:

1. Does this capability need to exist?
2. Does Fehrest already implement it?
3. Can Rust `std`/`core` or a platform primitive solve it?
4. Can an already-approved dependency solve it?
5. Can the requirement be satisfied with a smaller implementation?
6. Only then: implement the minimum correct solution.

**Ponytail's hard exclusions — the list is the decision.** Ponytail MUST NOT be used to minimise:

```
authorization boundaries · canonical-data integrity · security controls
recovery correctness · provenance · privacy · data-loss prevention
required accessibility · invariant tests
```

**Reasoning.** These two disciplines fail in opposite directions, which is why both are needed and why each is bounded. Spec Kit without Ponytail produces well-specified bloat: every specification is honoured and the codebase doubles. Ponytail without Spec Kit produces minimal code that solves the wrong problem. **Ponytail applied to a security boundary produces a smaller attack surface in exactly the sense that a thinner wall is smaller** — hence the exclusion list, which is not advisory.

**Rejected alternatives.**
- *Neither, relying on review* — review catches drift after it is written, which is the expensive point.
- *Spec Kit as runtime architecture* — a category error; it is a development workflow, and [R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) forbids it in a shipped dependency graph.
- *Ponytail without exclusions* — would license arguing that an authorization chokepoint "does not need to exist," which is the failure mode the discipline is most likely to produce when applied by an agent optimising for less code.

**Consequences.** Each production feature carries specification artifacts. Reviews check the Ponytail gate explicitly. Neither tool is installed into the project during F1-R2; both are stood up at [Phase 0](15-IMPLEMENTATION-PHASES.md#phase-0--foundation-validation) as CI/governance tooling.

**Reverses if.** Spec Kit's artifact overhead measurably exceeds its drift-prevention benefit across several features → reduce to the shortened workflow by default, keeping `specify` and `analyze`. Or Ponytail's gate is observed producing under-built security-relevant code despite the exclusion list → the exclusions are insufficiently specific, and the gate is removed from those paths entirely rather than reworded.

---

## ADR-0015 — Long-term canonical schema compatibility

**Status: 🔄 OPEN — study framed, policy deliberately not frozen. Opened in F1-R2 ([R2-17](reviews/F1-R2-RECONCILIATION.md)).**

**Context.** [M §3](12-MIGRATION-SCHEMA-EVOLUTION.md#3-event-and-memory-log-evolution) states that *"the upcast chain is permanent. Deleting an old upcaster makes historical logs unreadable, which is data loss."* [M §4](12-MIGRATION-SCHEMA-EVOLUTION.md#4-file-level-migration) states that readers must therefore support **every** historical version forever.

**The concern is valid.** A runtime that supports every schema version it has ever emitted, through an ever-growing chain of upcasters, carries an **unbounded maintenance and security surface**: every upcaster is code that parses old, potentially attacker-influenced data, is exercised rarely, and can never be deleted. Over a decade that is a large quantity of rarely-run parsing code inside a system whose event-log parser is [the one component whose corruption is unrecoverable](11-SECURITY-VERIFICATION-PLAN.md#4-fuzzing).

**What must NOT be concluded from that.** The obvious response — bound the compatibility window, drop old upcasters — **abandons old-vault readability**, which contradicts the product's governing promise: *the user's knowledge must survive Fehrest itself* ([A §1](00-PRODUCT-THESIS.md#1-what-fehrest-is)). A user's decade-old vault becoming unreadable because Fehrest evolved is precisely the failure the whole architecture exists to prevent. **Both horns are real**, which is why this is an open ADR rather than a decision.

**The model to study** — not adopted:

- A **bounded live-runtime compatibility window** — the shipping binary reads recent versions directly.
- **Explicit versioned migration tooling** for anything older, shipped and maintained separately from the runtime.
- **Preserved, published documentation of every historical format**, permanently, so that a third party can read an old vault with no Fehrest software at all ([I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended), [I-9](01-ARCHITECTURE-CONSTITUTION.md#i-9--export-does-not-depend-on-fehrest-infrastructure)).
- **Mandatory backup before any migration**, already required by [M §6](12-MIGRATION-SCHEMA-EVOLUTION.md#6-migration-execution).
- **Migration epochs** at major boundaries, so the chain has documented joints rather than growing monotonically.
- **An auditable path from any historical canonical record to its current form**, whatever tooling that path requires.

**The property that must hold under any policy chosen:** *a user-owned old vault must not become unreadable merely because Fehrest evolved.* "Readable" may come to mean "readable via a documented migration tool" rather than "readable by double-clicking the current release" — that is a legitimate narrowing. "Readable only if you kept a five-year-old binary" is not.

**Deliberately not frozen.** R2 evidence is insufficient: there is no implementation, no schema history, and no measurement of upcaster maintenance cost. Freezing a compatibility window now would be a guess with a decade-long blast radius.

**Decided when.** After the first two real major schema migrations, when the maintenance cost of an upcaster chain is an observation rather than a projection.

---

## ADR-0016 — Derivation lineage and projection checkpoints

**Status: PROPOSED (F1-R2 — [R2-07](reviews/F1-R2-RECONCILIATION.md), [R2-08](reviews/F1-R2-RECONCILIATION.md)).**

**Context.** [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) makes derived state rebuildable; [E §6](04-DERIVED-DATA-MODEL.md#6-incremental-maintenance) makes the *normal* path incremental because a full rebuild is minutes to hours. Those are only compatible if incremental maintenance provably converges to the same state as a rebuild — and F1 had no mechanism that could test it. Separately, [O §9](14-PERFORMANCE-BUDGETS.md#9-growth-over-time) required checkpointed projections without specifying what a checkpoint is.

**Decision.** Adopt two small, closely related mechanisms, specified in [E §10](04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data) and [E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints):

1. **A derivation registry** — every derived artifact records `artifact`, `inputs`, `deriver_id`, `deriver_version`. **Lineage as data, not a workflow engine.**
2. **A checkpoint contract** — checkpoints are derived, non-authoritative, disposable and rebuildable, carrying `log_sequence_high_water_mark`, `schema_version`, `deriver_version`, `digest`. Invalid → discard → older valid checkpoint → otherwise full replay.

**Provenance of the idea, stated precisely.** The lineage-as-data concept and the framing of a checkpoint as *truncation of recomputation depth* are taken from studying Apache Spark ([SRC-100](research/FEHREST_SOURCE_REGISTRY.md#414-apache-spark--study--defer)). **Nothing else is.**

**Explicitly rejected for v1:** the Spark runtime, any JVM requirement, driver/executor architecture, cluster execution, RDD/DataFrame as a runtime dependency, Structured Streaming, GraphX/Pregel, a DAG scheduler, and lazy distributed recomputation. Adopting a concept is not adopting a system, and a memory OS whose thesis is that knowledge must outlive its dependencies has no business acquiring a cluster computing framework.

**Consequences.** Two new test properties become expressible: `test_incremental_equals_full` and `test_invalidation_completeness`. Every deriver must be versioned. A small amount of bookkeeping is added to every derived write.

**What is deliberately not specified.** The degraded-recovery latency budget — full replay after checkpoint loss. It is **measured, not asserted** ([E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints)); the review's suggestion that replay "necessarily takes minutes" is an unmeasured claim about an unbuilt system running an unvalidated event volume, and three unknowns multiplied do not make a budget.

**Reverses if.** The registry's bookkeeping measurably dominates incremental update latency → reduce granularity (per-artifact-class rather than per-artifact), never remove the lineage. Or `test_incremental_equals_full` proves unachievable within documented tolerances → **incremental maintenance is unsound and full rebuild becomes the only correct path**, which would be a serious finding requiring [E §6](04-DERIVED-DATA-MODEL.md#6-incremental-maintenance) to be redesigned rather than the test to be relaxed.
