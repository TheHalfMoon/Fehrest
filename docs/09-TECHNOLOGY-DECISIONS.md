# J. Technology Decisions (ADRs)

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Each ADR states context, decision, alternatives rejected with reasons, consequences, and **the finding that would reverse it**. An ADR without a reversal condition is dogma.

Statuses: `PROPOSED` (awaiting review) · `OPEN` (decision deliberately not yet made) · `ACCEPTED` (post-review only).

| # | Decision | Status |
|---|---|---|
| [0001](#adr-0001--canonical-state-is-open-files-plus-an-append-only-event-log) | Canonical state is open files + append-only event log | PROPOSED |
| [0002](#adr-0002--v1-editing-is-markdown-native-blocksuite-is-deferred) | v1 editing is Markdown-native; BlockSuite deferred | PROPOSED |
| [0003](#adr-0003--graphify-runs-as-a-managed-long-lived-sidecar) | Graphify runs as a managed long-lived sidecar | PROPOSED |
| [0004](#adr-0004--object-identity-is-fehrest-allocated-and-opaque) | Object identity is Fehrest-allocated UUIDv7 | PROPOSED |
| [0005](#adr-0005--fehrest-adapts-harness-event-patterns-without-depending-on-the-harness-runtime) | Adapt harness event patterns, not the runtime | PROPOSED |
| [0006](#adr-0006--sqlite-is-the-derived-store-and-only-the-derived-store) | SQLite is the derived store, and only that | PROPOSED |
| [0007](#adr-0007--retrieval-is-lexical-first-vectors-are-optional) | Retrieval is lexical-first; vectors optional | PROPOSED |
| [0008](#adr-0008--memory-is-bitemporal-with-deterministic-resolution) | Memory is bitemporal with deterministic resolution | PROPOSED |
| [0009](#adr-0009--agents-address-objects-by-id-never-by-path) | Agents address objects by ID, never by path | PROPOSED |
| [0010](#adr-0010--core-implementation-language) | Core implementation language | **OPEN** |
| [0011](#adr-0011--desktop-shell) | Desktop shell | **OPEN** |
| [0012](#adr-0012--no-crdt-in-v1) | No CRDT in v1 | PROPOSED |

---

## ADR-0001 — Canonical state is open files plus an append-only event log

**Context.** Fehrest must satisfy [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default), [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended), [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) and [I-9](01-ARCHITECTURE-CONSTITUTION.md#i-9--export-does-not-depend-on-fehrest-infrastructure): knowledge lives locally, in open specified formats, and must be recoverable without Fehrest.

**Decision.** Canonical state is exactly: Markdown + YAML frontmatter files, original attachment bytes, an append-only JSONL event journal, append-only JSONL memory assertions, and JSON sidecars. Everything else is derived and deletable ([D](03-CANONICAL-DATA-MODEL.md), [E](04-DERIVED-DATA-MODEL.md)).

**Rejected alternatives.**
- *Database-canonical with file export* — inverts [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default); the vault becomes a database with a directory of stale copies beside it.
- *Files-only, no event log* — history cannot be recomputed from files, so audit, replay and provenance ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable)) become impossible.
- *Git as the event log* — attractive but wrong: git records file states, not typed semantic events with actors and scopes, and requiring git makes it a hard dependency of a system that must work without one.

**Consequences.** Two write paths (files and journal) must be kept consistent under crash. JSONL is verbose. Full text search requires derived indexing. All accepted; recovery specified in [N](13-RECOVERY-MODEL.md).

**Reverses if.** JSONL cannot meet durability or size budgets at a decade of events → replace with a specified append-only binary format, which [I-5-as-amended](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) explicitly permits given a spec and a lossless exporter.

---

## ADR-0002 — v1 editing is Markdown-native; BlockSuite is deferred

**Context.** The brief designates BlockSuite the primary editing substrate at Priority S+ and names the rich-state↔Markdown round-trip a major architecture gate.

**Decision.** v1 editing is **Markdown-native on CodeMirror 6**. The canonical bytes are the document model. Block identity, annotations and agent provenance live in documented sidecars ([D §4.4](03-CANONICAL-DATA-MODEL.md#44-the-sidecar-format)). BlockSuite and Yjs are deferred.

**Reasoning — two independent lines converging.**

*Structural.* A rich block CRDT holds per-block identity, overlapping marks, anchored comments and operation history. CommonMark expresses none of these. A lossless mapping therefore requires a sidecar carrying CRDT history — and at that point **the sidecar is the document**, Markdown becomes a lossy projection, and [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) inverts. The gate cannot be passed; it can only be dissolved by not adopting a document model richer than the canonical format ([D §7](03-CANONICAL-DATA-MODEL.md#7-why-a-rich-block-crdt-cannot-be-canonical-in-v1)).

*Empirical.* BlockSuite's repository is a downstream mirror whose sync stopped 2025-07-07; `@blocksuite/store` has not published since 2025-07-01 at pre-1.0 `0.22.4`; six dependency-vulnerability branches are open and unmerged; development happens inside the 446 MB AFFiNE monorepo under a split license ([E-10](research/EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate)). Even a solvable gate could not be cleared *against a maintained upstream*.

**Rejected alternatives.**
- *Adopt BlockSuite anyway* — puts an unmaintained, unreleased, pre-1.0 component with unpatched transitive vulnerabilities on the critical path of a product whose thesis is longevity.
- *Fork BlockSuite* — permanent ownership of a large editor codebase by a small team; per-file license provenance required.
- *ProseMirror / Lexical / Tiptap* — all sound, but all rich-document models, so all reintroduce the structural problem. If a rich model is ever needed, these are the candidates to re-evaluate ahead of BlockSuite.
- *Build a block editor* — the most expensive thing in the plan, for a feature set not yet validated.

**Consequences.** No block transclusion, no concurrent rich-text editing, no database blocks, no inline comments beyond sidecar annotations in v1. This is a **real product cost, stated plainly.** In exchange: round-trip is the identity function, canonical files are genuinely canonical, the dependency is MIT and current, and the most expensive subsystem in the plan is not built.

**Reverses if.** [H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work) is falsified — dogfooding shows Markdown-plus-sidecars genuinely cannot support required knowledge work. Then re-evaluate ProseMirror/Lexical *before* BlockSuite, and accept a documented sidecar-canonical model with an explicit [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) amendment. Deliberately the cheapest hypothesis in the plan to test.

---

## ADR-0003 — Graphify runs as a managed long-lived sidecar

**Context.** The brief offers three options: bundle Python locally, ship a managed sidecar, or adapt deterministic portions natively later.

**Decision.** **Option B — a managed long-lived sidecar process**, started lazily, read-only and path-confined to the vault, no credentials, network features disabled, supervised with restart-and-backoff, idle shutdown, resource caps.

**Reasoning from measurement.** Cold `import graphify.extract` = **4,451 ms**; warm = **276 ms**; bare interpreter ≈100 ms ([E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-cold-vs-warm)). Per-operation invocation costs ~376 ms of pure overhead even warm — impossible for per-file work — and the 4.45 s cold path would make first use appear broken. A long-lived process pays this **once per session**.

Extraction itself runs at ~18.4 files/s with 12 workers ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)), so throughput is adequate; only startup was pathological, and a sidecar removes startup entirely.

**Rejected alternatives.**
- *In-process Python (embedded interpreter)* — couples Fehrest's process to a 130 MB / 32-package dependency tree and puts hostile-input parsers inside the TCB ([T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities)).
- *Per-operation CLI invocation* — refuted by measurement above.
- *Port to Rust now* — the measured problem is startup, which the sidecar solves; porting addresses throughput, which is not the binding constraint. 60,202 lines and 28 grammars is a disproportionate cost for an unmeasured gain. Premature per the brief's own instruction.
- *Require a user-installed Graphify* — an install failure would silently disable a core feature.

**Consequences.** ~200–300 MB installer delta with a bundled runtime ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)) — mitigated by making the graph an **optional capability install**. A second process to supervise, and IPC to design. An independent sidecar update channel is required, since the app and sidecar cannot share a release cadence given upstream CVE tracking.

**Reverses if.** [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) is falsified and throughput becomes the constraint; **or** packaging proves untenable on a target platform; **or** [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is falsified and per-parser isolation is required — in which case the answer is likely WASM-isolated parsers, not a Rust port.

---

## ADR-0004 — Object identity is Fehrest-allocated and opaque

**Context.** [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) requires identity to survive rename and move. Graphify supplies node IDs that look usable.

**Decision.** Identity is a Fehrest-allocated **UUIDv7**, stored in the file's own frontmatter, immutable for the object's life. Graphify node IDs appear only in a rebuildable mapping table and never as a key in canonical state.

**Reasoning.** Graphify IDs are name-derived normalised slugs — NFKC + casefold + non-word collapse — with a documented history of same-filename collisions (#550), Unicode collapse (#811), producer disagreement (#1033) and idempotency failure on Turkish identifiers (#2614), whose stated failure mode is splitting one entity into "disconnected ghost nodes" ([E-4](research/EVIDENCE_LOG.md#e-4--graphify-node-ids-are-name-derived-not-stable-identities)). Adopting them as identity would violate [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) by construction.

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

**Reasoning.** Single-axis temporality cannot answer "what did we believe last month," which is exactly the question asked when auditing a wrong agent decision — a core Fehrest promise ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable)). Dynamic state tracking is one of LongMemEval-V2's five measured abilities ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). And the failure it prevents — surfacing two conflicting values and letting a model guess — is the failure the product exists to fix.

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

## ADR-0012 — No CRDT in v1

**Decision.** No CRDT runtime in v1. Yjs and Automerge are deferred.

**Reasoning.** A CRDT solves concurrent multi-writer editing. v1 has one writer on one machine, so it solves no v1 problem. It introduces the precise class of state [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) forbids: document state authoritative in the runtime but inexpressible in the open file. And the operation history that gives a CRDT its value is exactly what Markdown cannot hold ([D §7](03-CANONICAL-DATA-MODEL.md#7-why-a-rich-block-crdt-cannot-be-canonical-in-v1)).

Note this is **deferral on necessity, not on health** — Yjs is MIT and actively released ([E-11](research/EVIDENCE_LOG.md#e-11--yjs-and-codemirror-are-healthy-the-crdt-is-not-the-stale-part)) — which makes it a weak, easily reversed decision rather than a rejection.

**Rejected.** Yjs now "to be ready later" (pays full cost for zero v1 benefit and constrains the canonical format immediately); Automerge (same, plus a second ecosystem); both (explicitly forbidden absent a proven need neither satisfies alone).

**Consequences.** No real-time collaboration, no offline multi-device merge beyond file-level conflict handling. External concurrent modification is handled by hash-based detection and explicit conflict surfacing ([N](13-RECOVERY-MODEL.md)) — genuinely weaker than a CRDT for that case, and accepted.

**Reverses if.** Collaboration enters scope → adopt Yjs (single CRDT only) with a dedicated ADR on how CRDT state relates to canonical files, since that is where the deferred difficulty actually lives, not in adding the library.
