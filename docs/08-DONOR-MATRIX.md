# I. Donor Matrix

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Decision summary for every donor. Full metadata, pinned commits, licenses and provenance strategy live in [FEHREST_SOURCE_REGISTRY.md](research/FEHREST_SOURCE_REGISTRY.md); this document carries the *reasoning* and is the place to challenge a decision.

---

## 1. Dispositions, as reconciled in F1-R1

Read this section first. **Four dispositions changed in F1-R1 itself**, correcting F1 errors — those are marked ⚠️.

| Donor | Brief said | F1 said | **R1 says** | Deciding evidence |
|---|---|---|---|---|
| ⚠️ **BlockSuite** | `USE`, Priority **S+** | ❌ DEFER (as "unmaintained") | **CANDIDATE B in the [Editor Gate](18-EDITOR-GATE.md)** | The *standalone mirror* is stale, but `AFFiNE/blocksuite/…` is actively developed through 2026-08-10 with editor feature and security commits ([E-10.1](research/EVIDENCE_LOG.md#e-101--the-evidence-f1-missed-the-affine-subtree-is-active)) |
| ⚠️ **CodeMirror 6** | *absent* | ❌ USE (decided) | **CANDIDATE A in the Editor Gate** | Strong candidate, but must win on measurement, not argument ([R1-03](reviews/F1-R1-RECONCILIATION.md)) |
| ⚠️ **Yjs** | `USE / PROTOTYPE` | DEFER (flat) | **CONDITIONAL / EDITOR-DEPENDENT** | Healthy (MIT, 13.6.32). If Candidate B wins, Yjs arrives with the substrate ([R1-09](reviews/F1-R1-RECONCILIATION.md)) |
| ⚠️ **AFFiNE** | `ADAPT` | STUDY | **STUDY + SOURCE OF CANDIDATE B** | Split license and 446 MB monorepo are real costs — but it is where the maintained editor lives |
| **Graphify** | `USE + ADAPT` | ADAPT | **ADAPT — one implementation of a core, falsifiable product hypothesis** | Extractor IDs are path-derived and scheme-versioned *by design* ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)); runtime shape pending GI-BENCH |
| **DuckDB** | `USE`, Priority **S** | DEFER | **DEFER** (confirmed) | Data Intelligence is outside MVP by the brief's own scope |

**The capability/implementation distinction that governs this whole matrix ([R1-06](reviews/F1-R1-RECONCILIATION.md)):**

```
GRAPH INTELLIGENCE:       CORE CURRENT PRODUCT HYPOTHESIS — EXPLICITLY FALSIFIABLE
GRAPHIFY_PYTHON_RUNTIME:  REPLACEABLE IMPLEMENTATION CANDIDATE
```

No donor's implementation cost may by itself delete a core capability — a weak result from one donor is evidence about that donor. But the capability is a **hypothesis, not an axiom**: if benchmarks show graph-assisted understanding gives no material benefit over simpler local retrieval at acceptable cost, Fehrest must permit redesign or removal ([F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)).

Everything else in the brief's registry is confirmed, with reasoning tightened.

---

## 2. Code donors — USE

| Donor | Layer | What we take | Why it is safe to depend on |
|---|---|---|---|
| **SQLite** | DERIVED | Derived store, FTS5 | Public domain, ubiquitous, crash-tested. Only holds derived state, so corruption costs a rebuild |
| **SQLite FTS5** | DERIVED | BM25 lexical baseline | Ships with SQLite; zero extra dependency; the floor every other retrieval method must beat |
| ~~CodeMirror 6~~ | UI | — | **Moved to the [Editor Gate](18-EDITOR-GATE.md) as Candidate A.** Not a settled `USE` — it must win a bake-off against the maintained AFFiNE BlockSuite subtree ([R1-02](reviews/F1-R1-RECONCILIATION.md)) |
| **Google Magika** | INGEST | Content-based type detection before parser dispatch | Apache-2.0, active. Security-relevant: extension-based dispatch is a parser-confusion vector ([T-12](02-THREAT-MODEL.md#t-12--malicious-attachment--parser-confusion)) |
| **Model Context Protocol** | AGENT | Agent transport | A standard, not a runtime. **Not an authorization boundary** — authorization is enforced in Fehrest before any tool runs ([T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin)) |
| **llama.cpp** | MEMORY/AGENT | Optional local inference | MIT, very active. Fehrest must pass its full core suite with this absent ([I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api)) |

---

## 3. Code donors — ADAPT

### Graphify — ADAPT via sidecar

**Take:** deterministic tree-sitter extraction across 28 grammars; the `{nodes, edges, relation, confidence}` schema as a wire contract; `EXTRACTED`/`INFERRED` labelling; `source_file` + `source_location` provenance; incremental cache and watch-debounce semantics; `graph_diff` for incremental updates; `security.py`'s path-confinement and label-sanitisation as prior art.

**Reject:** `ids.py` as an identity authority; the whole MCP surface; PR/repository tooling; LLM-assisted extraction paths; Neo4j/FalkorDB exporters; `graphify-out/` as an output location.

**Why ADAPT and not USE:** three boundary changes are mandatory, and each is a real modification rather than configuration.
1. **Identity.** Node IDs are path-derived **by design** (`{parent_dir}_{stem}`) and their scheme changes across versions — upstream itself rejected an alternative because it "would rewrite every file and symbol id" ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)). *(The historical collision and Unicode bugs F1 cited are **fixed** — #2614 in 0.9.40, #811/#1033/#550 root cause resolved — and are no longer part of this argument, per [R1-05](reviews/F1-R1-RECONCILIATION.md).)* Fehrest allocates its own UUIDv7 identities and treats `extractor_id` as a rebuildable mapping.
2. **Authority.** The sidecar is a compute service with no write authority ([R-7](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)); core validates every response against schema before accepting it.
3. **Surface.** Its agent-facing tools are never re-exported, or agents gain a second unaudited retrieval path around the compiler ([E-7](research/EVIDENCE_LOG.md#e-7--graphify-agent-facing-surface)).

**Why worth the cost:** ~18.4 files/s, 97.2% `EXTRACTED` confidence, line-level provenance, **zero LLM credits** ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary), [E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)). Reimplementing 60,202 lines and 28 grammars is not defensible against an active Apache-2.0 upstream.

**Accepted costs:** 32 packages / 130 MB, ~200–300 MB installer delta with a runtime ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)); 4,451 ms cold start, mitigated by a long-lived sidecar ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)); a Python parser surface processing hostile input ([T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities)).

### DeepSeek Harness — ADAPT patterns only

**Take:** append-only typed event log as source of truth with agent-visible history *derived*, never stored; one event type with two interchangeable backends and no parallel persisted type; non-truncating crash repair via a synthetic terminator no producer emits; header metadata outside the event vocabulary; merge-extensible event map; branded non-interchangeable identifiers; approval as a log-only asked/decided pair failing closed; oversized output replaced by a locator with "source is not access control" and "a name is not a path"; honest per-platform partial-enforcement reporting; package-owned runtime invariants.

**Reject:** Cordis as a runtime framework; the TS agent loop; plugin runtime; model adapters; compaction engine; `apps/*`.

**Why reject Cordis specifically:** making an external meta-framework load-bearing directly contradicts *"the user's knowledge must survive Fehrest itself."* A memory OS whose core cannot boot without a third-party plugin framework has a shorter lifespan than the knowledge it holds. Elegance is not a reason to take a dependency ([ADR-0005](09-TECHNOLOGY-DECISIONS.md#adr-0005--fehrest-adapts-harness-event-patterns-without-depending-on-the-harness-runtime)).

**Gap inherited:** the donor's sandbox governs filesystem effects only and its Windows backend self-reports partial enforcement ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)). Fehrest gets **no network boundary** from it and must specify one ([T-11](02-THREAT-MODEL.md#t-11--sidecar-network-egress), [T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix)).

### Docling / MarkItDown — ADAPT as optional capability + fallback

Docling for high-fidelity extraction (MIT, very active), MarkItDown as the lightweight fallback. Docling must be an **optional install**: its ML dependency tree would otherwise violate the offline/no-model floor. Its weight is unmeasured — a registry gap ([registry §13](research/FEHREST_SOURCE_REGISTRY.md#13-known-registry-gaps)).

### AWS Cedar — ADAPT the model, DEFER the engine

Adopt `principal + action + resource + context` as the decision shape ([G §2](06-AGENT-MODEL.md#2-capabilities)). Embedding the engine is separable and premature: v1's policy space is small enough that a hand-written evaluator is auditable, and an auditable 200-line evaluator is better security than a correctly-used large dependency.

---

## 4. DEFER

| Donor | Why deferred | Reconsider when |
|---|---|---|
| ~~BlockSuite~~ | **No longer deferred.** Moved to the [Editor Gate](18-EDITOR-GATE.md) as **Candidate B** — the maintained `AFFiNE/blocksuite/…` subtree, never the stale standalone package ([R1-02](reviews/F1-R1-RECONCILIATION.md)) | — |
| ~~Yjs~~ | **No longer flatly deferred.** Reclassified **CONDITIONAL / EDITOR-DEPENDENT** ([R1-09](reviews/F1-R1-RECONCILIATION.md)): arrives with Candidate B if it wins; stays deferred otherwise. **Collaboration must not be added to justify it** | Editor Gate closes |
| **sqlite-vec** | Release line is `v0.1.10-alpha.*` | [B-3](10-BENCHMARK-PLAN.md) shows material vector gain **and** a stable release exists |
| **USearch / LanceDB / FAISS** | No vector requirement proven | Same gate as above |
| **Tantivy** | FTS5 has not failed | FTS5 misses a measured budget in [O](14-PERFORMANCE-BUDGETS.md) |
| **DuckDB** | Data Intelligence out of MVP | Dataset/analytics objects enter scope |
| **Wasmtime / WASI** | No plugin system in v1 | Third-party plugins are designed; the seam must stay viable |
| **JSON Canvas** | Canvas is not MVP | Canvas ships (Phase 6). Format decision already made — MIT, active |
| **PaddleOCR / whisper.cpp** | Optional media ingestion | Users demonstrate need |
| **TimesFM / Data Formulator** | Forecasting and BI far out of scope | Post-v1 at the earliest |
| **Cytoscape.js** | Graph explorer cut from MVP | Graph UI is scheduled |
| **Automerge** | Sync deferred | Sync ADR; never alongside Yjs without proof |

---

## 5. STUDY — mechanisms, not vibes

Each entry names the **specific mechanism** studied. "Inspiration" is not a disposition.

| Donor | Mechanism studied | Explicitly not taken |
|---|---|---|
| **Obsidian** | Vault semantics; files usable without the app; backlink computation; wikilink resolution; keyboard-first palette | Its plugin API; its proprietary sync |
| **Cordis** | Plugin composition, reversible effects, scoped services, effect-scoped disposal | Cordis itself as a dependency |
| **Graphiti** | Temporal graph memory; changing facts; temporal retrieval | Mandatory external graph service |
| **Letta** | Memory-block lifecycle; consolidation | Agent-framework coupling |
| **Mem0** | User/session/agent scope separation | Its retrieval quality — recall@10 **0.048** on LOCOMO makes it a floor, not a goal ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)) |
| **Microsoft GraphRAG** | Hierarchical communities; local vs global queries; claims | LLM-heavy indexing — deterministic extraction meets the need at zero cost |
| **MemGPT** | Tiered memory; paging | LLM-managed paging as a requirement |
| **A-MEM** | Zettelkasten-style memory linking and evolution | LLM-only link generation |
| **AgeMem** | The six-operation API (`add`/`update`/`delete`/`retrieve`/`summary`/`filter`) | **The mechanism** — a three-stage RL-trained policy cannot be the promotion decider under `AI OFF` ([E-15](research/EVIDENCE_LOG.md#e-15--agemem-is-a-learned-policy-not-a-transplantable-algorithm)) |
| **HippoRAG** | Associative graph retrieval; multi-hop recall | LLM-built graph |
| **RAPTOR** | Hierarchical recursive summarisation | Mandatory LLM summarisation at index time ([R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)) |
| **Peritext** | Why rich-text marks resist CRDT representation | — (supports [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated)) |
| **Local-first Software** | Seven ideals as a design test; network as optimisation | Its assumption that CRDTs are the natural substrate |
| **W3C PROV** | Entity/Activity/Agent; `wasDerivedFrom`, `wasAttributedTo` | Becoming an RDF system |
| **Bitemporal DB literature** | Valid vs recorded time; as-of resolution | Dialect-specific syntax |
| **Linear** | Keyboard-first interaction; instant command surfaces | Cloning the product |
| **Logseq / SiYuan** | Block-level identity in plain text and its file-format cost | Outliner-only storage model |
| **Airtable / Teable / Baserow / NocoDB** | One dataset, many views | Building a database product in v1 |
| **AFFiNE** | Workspace UX; document/canvas/database unification | Any code; forking it |
| **Excalidraw / tldraw / draw.io** | Canvas interaction, gestures, export, shape libraries | A second canvas runtime |
| **Superset / Data Formulator** | Semantic metrics; transformation lineage | Their service architectures |
| **Apache Spark** *(F1-R2, [SRC-100](research/FEHREST_SOURCE_REGISTRY.md#414-apache-spark--study--defer))* | **Lineage as data**; **checkpoint as truncation of recomputation depth**; bounded batch/backpressure lessons where justified | **The runtime, and everything attached to it** — JVM, driver/executor, cluster, RDD/DataFrame, Structured Streaming, GraphX/Pregel, DAG scheduler, lazy distributed recomputation |
| **Karpathy's LLM Wiki** *(F1-R2, [SRC-101](research/FEHREST_SOURCE_REGISTRY.md#82-andrej-karpathy--llm-wiki))* | The distinction between **reconstructing understanding per query (RAG)** and **maintaining a persistent interlinked artifact that compounds**; and a benchmark baseline built from it | Any claim of endorsement. **None is established for Fehrest, Graphify or Graph Intelligence** |
| **Jujutsu** *(F1-R2, [SRC-140](research/FEHREST_SOURCE_REGISTRY.md#src-140--jujutsu))* | Operation-log concepts; durable undo; historical state inspection; **conflict as representable state rather than corruption** | Jujutsu as storage; requiring `jj`; becoming a VCS; importing merge semantics into memory without checking domain fit |
| **OpenLineage** *(F1-R2, [SRC-141](research/FEHREST_SOURCE_REGISTRY.md#src-141--openlineage))* | Run/Job/Dataset/Event/**Facets** separation; extensible facets as an alternative to a monolithic event schema that can only grow | Any runtime dependency; data-pipeline vocabulary imported without checking that it transfers |
| **in-toto attestations** *(F1-R2, [SRC-142](research/FEHREST_SOURCE_REGISTRY.md#src-142--in-toto-attestations))* | Authenticated claims; subject digests; typed predicates; actor/tool evidence | Supply-chain terminology imposed on human memory. A memory is an assertion by an actor, not a build artifact |
| **Penpot** *(F1-R2, [SRC-120](research/FEHREST_SOURCE_REGISTRY.md#src-120--penpot))* | Open-standard visual document architecture; SVG/CSS/HTML/JSON interoperability; design tokens; components and variants; large-canvas mutation handling; security lessons from a mature collaborative editor | The server and runtime wholesale; server infrastructure adopted by association; becoming a design tool |
| **Apache Superset** *(F1-R2, [SRC-170](research/FEHREST_SOURCE_REGISTRY.md#src-170--apache-superset))* | Semantic data definitions separated from visual presentation; reusable metrics and dimensions; chart/view plugin organisation; permission-aware analytics | Runtime dependency; Python; Redis/Celery; a mandatory database server; DuckDB in the MVP; dashboards before the thesis-proof |
| **AppFlowy-Collab** *(F1-R2, [SRC-133](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates))* | A Rust collaborative substrate shared across document, database and workspace types — evidence for or against a shared Fehrest object substrate | The product architecture wholesale; any code import before exact license and provenance review |
| **Salsa** *(F1-R2, [SRC-152](research/FEHREST_SOURCE_REGISTRY.md#145-retrieval-graph-and-semantic-interoperability))* | Canonical inputs → derived queries → memoized outputs → selective invalidation, as a way of thinking about derived state | Salsa as a v1 runtime dependency. The validated requirement is a four-field manifest, not a framework |
| **Anytype / any-sync** *(F1-R2, [SRC-134](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates))* | Local-first object architecture; P2P sync; encrypted collaboration; object-oriented knowledge UX | Any assumption of uniform permissive licensing across `anyproto` components |

---

## 6. BENCHMARK

| Donor | Role | Gate it decides |
|---|---|---|
| **LongMemEval-V2** | Primary memory benchmark | Whether the memory model represents the five measured abilities ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)) |
| **LongMemEval (v1)** | Secondary | Temporal reasoning, knowledge updates, abstention |
| **AgentDojo** | Security benchmark | Whether [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority) holds under adversarial content — **extended in F1-R2 with Fehrest-specific attack classes** ([L §6.1](11-SECURITY-VERIFICATION-PLAN.md#61-c-inject--prompt-injection)) |
| **MemOra** *(F1-R2)* | Memory-update benchmark | Whether Fehrest **avoids using a memory that was once true and no longer is** — externally sourced, unlike C-TEMPORAL |
| **EvoMemBench** *(F1-R2)* | Episodic vs cross-episode benchmark | Deliberate **contrary evidence** against assuming one memory strategy wins every workload |
| **Hindsight** *(F1-R2)* | Memory architecture reference | World knowledge vs agent experience; retain/recall/reflect. Claims treated as `UPSTREAM_CLAIM` until reproduced |
| **BM25 / dense / hybrid / graph-only** | Retrieval baselines | Whether each retrieval stage earns inclusion ([B-3](10-BENCHMARK-PLAN.md)) |
| **Mem0** | Memory baseline | Floor |
| **Raw history stuffing** | Compression baseline | Whether compilation beats stuffing ([B-7](10-BENCHMARK-PLAN.md)) |
| **Repository-native documentation** *(F1-R2)* | Convention baseline | Whether project state must be a *system* rather than a maintained file |
| **Karpathy-style maintained LLM Wiki** *(F1-R2)* | **The strongest simple alternative** | Whether temporal state, supersession, provenance and deterministic compilation add measurable value **over a maintained knowledge artifact** ([K §3.1](10-BENCHMARK-PLAN.md#31-the-baseline-ladder)) |
| **Competent agent, plain file tools, no memory** | **The bar that matters** | Whether Fehrest deserves to exist — 69.3% in LME-V2's reporting |

---

## 7. REJECT

Only two outright rejections. Most disagreements are `DEFER`, because deferral is reversible and rejection should be reserved for things that are wrong in principle.

| Donor | Rejected as | Reason |
|---|---|---|
| **Cordis** *(as a dependency)* | Runtime framework | Contradicts "knowledge must survive Fehrest itself." Retained as `STUDY` |
| **Any mandatory hosted service, hosted auth, opaque telemetry** | — | Violates [I-2](01-ARCHITECTURE-CONSTITUTION.md#i-2--core-functionality-requires-no-network), [I-3](01-ARCHITECTURE-CONSTITUTION.md#i-3--core-functionality-requires-no-fehrest-hosted-service), [I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) |

Also rejected as *architectural positions* rather than donors: forking AFFiNE and renaming it; embedding any single commercial model provider; making any vector store, graph database, or local model mandatory.

---

## 8. Aggregate dependency risk

| Risk | Exposure | Mitigation |
|---|---|---|
| Graphify pre-1.0 on a moving branch (`v8`) | Graph capability | Pinned commit; schema contract test; graph is D2-optional so its loss degrades rather than breaks |
| Python sidecar tree (32 packages) | Security, packaging | `pip-audit`; independent update channel; read-only, no-network, no-credential confinement |
| 28 tree-sitter grammars | Parser attack surface | Sidecar confinement; fuzzing; per-file caps and non-fatal failure |
| CodeMirror carries no rich-block features | Product capability | Stated v1 cost; sidecar covers annotations; gated on [H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work) |
| No third-party replication of any retrieval claim | Every comparative number | Re-run all baselines locally before they become thresholds ([K](10-BENCHMARK-PLAN.md)) |

**Structural mitigation:** every heavy donor sits behind a boundary whose failure is *degradation*, not breakage. Graphify absent → FTS-only retrieval. Vectors absent → default. Local model absent → `AI OFF`. Docling absent → MarkItDown. Sidecar dead → graph features hidden. **Python absent entirely → still a working memory OS** ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)). **UI absent entirely → still a working memory OS** ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)).

**Corrected in F1-R2.** The former claim that *"the only donors whose absence breaks Fehrest are SQLite and CodeMirror"* no longer holds, in a way that strengthens the position: **CodeMirror is not a donor whose absence breaks Fehrest**, because [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) requires the Core to be fully operable with no editor and no UI at all, and because the editor is still [OPEN / prototype-gated](18-EDITOR-GATE.md). **The only donor whose absence breaks Fehrest is SQLite** — public domain, ubiquitous, and holding derived state only. That is the intended shape of the dependency graph, and F1-R2 makes it one item shorter.
