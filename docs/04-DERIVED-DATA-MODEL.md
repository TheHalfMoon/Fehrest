# E. Derived Data Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Derived state is everything reconstructable from canonical state. Its governing property is [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable): delete all of it, restart, and the system is functionally identical.

That property is not a convenience. It is what makes every index decision in this document reversible, and it is the reason index corruption is an availability problem rather than a security problem ([T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes)).

---

## 1. Two classes of state inside `.fehrest/`

> **CLARIFIED IN F1-R1 ([R1-16](reviews/F1-R1-RECONCILIATION.md)).** F1 was correct that derived state is rebuildable, but its phrasing invited a catastrophic misreading: that the whole `.fehrest/` directory is disposable. **It is not.**

| | **Canonical** — inside `.fehrest/` | **Derived** — inside `.fehrest/derived/` |
|---|---|---|
| Contents | event journal, memory assertions, sidecars, vault identity, schema version | search index, graph, vectors, caches, projections |
| Rebuildable | **No** | **Yes, always** |
| If deleted | **Irreplaceable history loss** | Inconvenience |
| Backup | **Required** | Never needed |
| Sync | Must be included | Should be excluded |

**The rule:** *"delete derived state and restart"* is a supported recovery instruction. *"delete `.fehrest/` and restart"* **destroys the event journal and every memory** — the two things in Fehrest that cannot be recomputed from anything.

Every recovery instruction, support document and CLI affordance must name the **derived subtree explicitly**. A `fehrest doctor --reset-derived` command should exist precisely so no user is ever told to delete a directory by hand.

The rest of this document concerns the **derived** class only.

## 2. Inventory

| Artifact | Store | Rebuild source | Rebuild cost (10K files) | Required? |
|---|---|---|---|---|
| Object index | `index.sqlite` | Frontmatter + file stat | ~1 min | Yes |
| Link/backlink index | `index.sqlite` | Markdown link parse | ~1 min | Yes |
| FTS5 index | `index.sqlite` | Object bodies | ~2 min | Yes |
| Memory projection | `index.sqlite` | Memory JSONL | seconds | Yes |
| Event mirror | `index.sqlite` | Event JSONL | ~1 min | No — convenience |
| Structural graph | `derived/graph/` | Sidecar extraction | **~9 min** ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)) | No |
| Graph↔object ID map | `index.sqlite` | Graph + object index | seconds | No |
| Communities | `derived/graph/` | Graph | ~1 min | No |
| Extracted text | `derived/cache/` | Attachments | Varies; **lossy if source deleted** | No |
| Embeddings | `derived/vectors/` | Object bodies + model | Hours, needs a model | **No** |
| Thumbnails / summaries | `derived/cache/` | Sources | Varies | No |

Only five artifacts are required, and all five rebuild in **under 5 minutes for 10K files**. This is deliberate: the mandatory rebuild path must be fast enough that "delete derived state and restart" is a viable support instruction. Everything slow is optional.

---

## 3. Tiering

| Tier | Meaning | Members | Startup behaviour |
|---|---|---|---|
| **D1 — Required** | Core function degrades without it | object index, links, FTS, memory projection | Built before the app is interactive; must be fast |
| **D2 — Enhancing** | Improves retrieval; absence is graceful | graph, communities, ID map, event mirror | Built in background; **never gates startup** |
| **D3 — Optional** | Requires a model or heavy compute | embeddings, summaries, OCR, transcripts | Explicit opt-in only |

D2's "never gates startup" is forced by measurement: full graph extraction is ~9 minutes at 10K files and ~90 minutes at 100K ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)). Any design that blocks the UI on graph availability is dead on arrival for a large vault. The application must be fully usable — search, read, edit, memory, context compilation — with the graph entirely absent.

---

## 4. SQLite as the derived store

One database, `.fehrest/derived/index.sqlite`, containing all D1 state and the D2 mappings.

**Configuration:** WAL journaling, `synchronous=NORMAL`, `foreign_keys=ON`, busy timeout set, single writer with a connection pool for readers.

`synchronous=NORMAL` rather than `FULL` because the database is derived: a power-loss corruption costs a rebuild, not data. Trading durability for write throughput is correct *precisely because* [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) holds. This is an example of the invariant paying for itself.

Sketch of the required tables:

```sql
CREATE TABLE object (
  id TEXT PRIMARY KEY,              -- UUIDv7, from frontmatter
  path TEXT NOT NULL,               -- location, not identity (I-15)
  type TEXT NOT NULL,
  title TEXT,
  content_hash TEXT NOT NULL,       -- staleness decided by hash, never mtime (T-9)
  mtime INTEGER NOT NULL,           -- fast-path hint only
  size INTEGER NOT NULL,
  frontmatter JSON NOT NULL,        -- verbatim, including unknown fields (R-8)
  indexed_at INTEGER NOT NULL
);
CREATE UNIQUE INDEX object_path ON object(path);

CREATE TABLE link (
  src TEXT NOT NULL REFERENCES object(id) ON DELETE CASCADE,
  dst TEXT,                         -- NULL = unresolved
  raw TEXT NOT NULL,                -- as written, for repair and rewrite
  kind TEXT NOT NULL,               -- wikilink | id | markdown | embed
  line INTEGER NOT NULL             -- provenance back to source position
);

CREATE VIRTUAL TABLE object_fts USING fts5(
  title, body, tokenize = 'unicode61 remove_diacritics 2',
  content = '', contentless_delete = 1
);

-- Extractor ids are name/path-derived and scheme-versioned (E-4):
-- mapping only, never identity. Satisfies G-ID-1..G-ID-4.
CREATE TABLE graph_node_map (
  extractor_id      TEXT NOT NULL,   -- G-ID-1: never a canonical identity
  extractor_version TEXT NOT NULL,   -- G-ID-3: makes stale mappings detectable
  fehrest_object_id TEXT REFERENCES object(id) ON DELETE CASCADE,  -- G-ID-2
  symbol            TEXT,
  source_uri        TEXT NOT NULL,   -- G-ID-4: trace back to canonical evidence
  source_revision   TEXT,            -- G-ID-4: content hash at extraction time
  source_location   TEXT,            -- G-ID-4: line/range
  relationship_confidence TEXT NOT NULL,  -- extractor label, mapped into the
                                          -- Fehrest trust model (F §3.3), not
                                          -- used as a trust value directly
  PRIMARY KEY (extractor_id, extractor_version, fehrest_object_id)
);
```

Two schema choices carry weight:

- **`content_hash` decides staleness, `mtime` is only a fast-path hint.** mtime is unreliable across filesystems, sync tools, and restores, and trusting it enables the provenance race in [T-9](02-THREAT-MODEL.md#t-9--filesystem-race-conditions).
- **`frontmatter` is stored verbatim as JSON.** Round-tripping through a typed struct is how unknown fields get dropped, violating [R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules).

---

## 5. Graph Intelligence: capability vs implementation

> **CLARIFIED IN F1-R1 ([R1-06](reviews/F1-R1-RECONCILIATION.md)).** F1 framed this section as "the Graphify boundary," which risked binding a core capability to one donor's implementation cost.

```
GRAPH INTELLIGENCE:            CORE CURRENT PRODUCT HYPOTHESIS — EXPLICITLY FALSIFIABLE
GRAPHIFY_PYTHON_RUNTIME:       REPLACEABLE IMPLEMENTATION CANDIDATE
```

**The capability** — deterministic extraction of relationships between objects, with provenance to source locations — answers *"what is connected?"*, one of the four questions Fehrest exists to answer ([A §5](00-PRODUCT-THESIS.md#5-the-four-layer-architecture)). The **hypothesis** is that lexical search cannot answer it and that answering it materially improves agent continuation.

**The implementation** is a choice among: upstream Graphify as a managed worker · adapted Graphify modules · a bundled persistent worker · a later native reimplementation · a different extractor entirely if benchmarks favour one.

**Two distinct failure modes, with different consequences ([F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)):**

| Finding | Consequence |
|---|---|
| Graphify is too heavy, slow or risky | **Replace the implementation** |
| The capability shows no material benefit over simpler local retrieval at acceptable cost, across configurations and corpus types | **Redesign or remove Graph Intelligence from the core product hypothesis** |

The second row is what keeps the claim falsifiable. Nothing in the canonical data model depends on the graph existing, so removal touches no canonical record.

Separately, whether the graph is *installed* on a given machine is a packaging question (D2 tiering below); a user without it gets degraded retrieval.

### 5.1 Ownership

| Owned by the extractor (worker) | Owned by Fehrest (core) |
|---|---|
| Parsing, grammars | Object identity |
| Node/edge extraction | Canonical writes |
| Cross-file symbol resolution | ID mapping and scope enforcement |
| Community detection | Retrieval policy and ranking |
| Graph diff | Memory, provenance and trust classification |

The rule is [R-7](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules): **the extractor has no authority.** It receives file paths and returns proposed facts. It cannot write canonical state, allocate identity, or influence authorization. This holds for *any* implementation, which is what makes the implementation replaceable without re-litigating the security model.

### 5.2 The wire contract

Fehrest consumes the documented extraction schema as a stable contract ([E-2](research/EVIDENCE_LOG.md#e-2--graphify-module-inventory-and-size)):

```json
{
  "nodes": [{"id": "...", "label": "...", "source_file": "...", "source_location": "L42"}],
  "edges": [{"source": "...", "target": "...", "relation": "calls|imports|...",
             "confidence": "EXTRACTED|INFERRED|AMBIGUOUS"}]
}
```

Core validates every response against this schema before accepting it — the sidecar is semi-trusted ([boundary B2](02-THREAT-MODEL.md#4-trust-boundaries)), so a malformed or hostile response must be rejected rather than ingested.

**Properties Fehrest must design around:**
- **Extractor confidence labels are inputs, not trust values.** One corpus showed `EXTRACTED` 97.2% / `INFERRED` 2.8% / `AMBIGUOUS` 0.0% ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)), but a single corpus proves nothing about ambiguity in general ([R1-08](reviews/F1-R1-RECONCILIATION.md)). Fehrest defines its **own** evidence and trust model ([F §3.3](05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model)); extractor labels **map into** it. No Fehrest trust semantics may be derived from an extractor's label distribution.
- The relation vocabulary is **open**. Never enumerate it exhaustively in a schema constraint, or an upstream addition breaks ingestion.
- Missing optional grammars degrade to partial graphs with warnings rather than failures. Surface as index health, not errors.

### 5.3 ID mapping is the critical seam

Extractor IDs are name- or path-derived and their schemes change across versions ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)). This is a property of extractors in general, not a defect of one. Therefore:

1. `graph_node_map` is many-to-many and **fully rebuildable** (G-ID-3).
2. No canonical record ever references an extractor ID (G-ID-1).
3. Every derived node maps to a Fehrest identity where one exists (G-ID-2).
4. Every derived node retains `source_uri` + `source_revision` + `source_location` to trace back to canonical evidence (G-ID-4).
5. A collision produces multiple mappings, surfaced as ambiguity, never silently resolved.
6. On rename, map entries are invalidated and re-derived; object identity is untouched because it never depended on the graph.
7. On extractor upgrade, `extractor_version` changes and mappings rebuild; **canonical identity does not move.**

Point 7 is the load-bearing one. It is what lets Fehrest upgrade or **swap** its extractor without migrating a single canonical record — the mechanism that makes [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)'s "implementation is replaceable" true in practice rather than in principle.

### 5.4 Process model — PROVISIONAL

**Provisional shape: a long-lived managed worker**, indicated by preliminary measurement — cold import ≈4,451 ms, warm ≈276 ms, bare interpreter ≈100 ms ([E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-preliminary)). Per-operation invocation would cost ~376 ms of pure overhead even warm.

Lifecycle: lazy start on first graph need (**never** on app launch); private authenticated local channel; read-only, path-confined to the vault; no credentials; network features disabled ([T-11](02-THREAT-MODEL.md#t-11--sidecar-network-egress)); supervised with restart-and-backoff; idle shutdown; resource caps. Extraction spawned 12 worker subprocesses in the observed configuration, which must be counted in resource budgets and made configurable.

**Not final.** These figures are single-machine, single-corpus ([R1-07](reviews/F1-R1-RECONCILIATION.md)). The choice among lazy worker, preloaded worker, background process and adaptation depends on incremental-update latency, memory under concurrency, and behaviour across corpus *types* — none measured. **[GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) decides.**

**Do not port Graphify** ([R1-06](reviews/F1-R1-RECONCILIATION.md)). Revisit only if GI-BENCH shows throughput or packaging — not startup — is the binding constraint.

---

## 6. Incremental maintenance

Full rebuild is a fallback, not the normal path — at 10K files the graph alone is ~9 minutes.

**Pipeline:**

```
file change (watch, debounced)
  → hash content
  → unchanged hash? stop.
  → update object row, re-parse links, update FTS        [D1: milliseconds]
  → enqueue graph extraction for the changed file        [D2: background]
  → sidecar extracts; graph diff applied to affected region
  → recompute communities for affected components only
  → enqueue embedding if D3 enabled
```

**Rules:**
- D1 updates are synchronous with respect to the user's next query. Search must never return stale results for a file the user just edited — that is immediately noticeable and erodes trust in the whole system.
- D2 updates are asynchronous, cancellable, resumable, and coalesced.
- Rebuild progress is durable, so an interrupted rebuild resumes rather than restarting ([N](13-RECOVERY-MODEL.md)).
- External modification (git checkout, sync, editor outside Fehrest) is detected by hash comparison on a scan, not by trusting the watcher — watchers miss events, and a missed event that silently drops a file from the index is a suppression bug indistinguishable from [T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes).

**Reconciliation:** a periodic full scan compares the canonical inventory to the index, reporting objects present on disk but missing from the index and vice versa. This is both a correctness check and the detector for index-suppression attacks.

---

## 7. Vectors

**Optional, D3, off by default.** Three independent reasons:

1. **Constitutional.** [I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) — embeddings require a model.
2. **Engineering.** sqlite-vec's current release line is `v0.1.10-alpha.*`, newest stable `v0.1.9` ([E-12](research/EVIDENCE_LOG.md#e-12--vector-store-maturity)). Alpha status alone disqualifies it from being required.
3. **Empirical.** The only prose-memory benchmark reported for the graph donor shows graph retrieval **tying** dense RAG (76% vs 76% on LongMemEval-S, n=50), while its clear wins are recall and cost ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)). That evidence does not establish that vectors are unnecessary — it establishes that neither approach dominates, which means vectors must earn inclusion by measurement on Fehrest's own corpus rather than by convention.

Sequencing: FTS5 first, measured; graph expansion second, measured; vectors third, adopted only if [B-3](10-BENCHMARK-PLAN.md) shows a material gain. Backend chosen by benchmark between sqlite-vec and USearch ([SRC-012](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval), [SRC-013](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval)).

When enabled, embeddings are stored with the model identifier and dimension. A model change invalidates the whole index — which is fine, because it is derived.

---

## 8. Rebuild semantics

**Determinism requirement:** rebuilding must produce *functionally identical* query results, not byte-identical files. Byte-identical is unachievable (SQLite page layout, insertion order, parallel extraction ordering) and demanding it would create a permanently failing test.

`test_nuke_and_rebuild_equivalence` therefore compares a fixed query set's results — ordered result IDs, scores within tolerance, memory resolutions, context package digests — rather than file bytes. This is the most important test in the suite because it is the guarantee that every decision in this document is reversible.

**Cost, extrapolated from measurement** ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary), linear assumption flagged as [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count)):

| Vault | D1 (required) | D2 graph | D3 embeddings |
|---|---|---|---|
| 1K files | < 10 s | ~1 min | ~10 min |
| 10K files | < 60 s | ~9 min | ~2 h |
| 100K files | < 10 min | **~90 min** | impractical without a GPU |

The 100K graph figure is the number that shapes the architecture: it must be a resumable background job with visible progress, and it must be genuinely optional. Budgets in [O](14-PERFORMANCE-BUDGETS.md).

---

## 9. Failure and degradation

| Failure | Detection | Response | User impact |
|---|---|---|---|
| SQLite corrupt | `PRAGMA integrity_check` on open | Quarantine, rebuild D1 | Minutes unavailable |
| Graph missing/stale | Health check | Retrieval degrades to FTS-only, flagged in UI | Reduced recall |
| Sidecar crash | Supervisor | Restart with backoff; after N failures disable graph and notify | Reduced recall |
| Sidecar absent | Startup probe | Graph features hidden, not broken | Feature unavailable |
| Embeddings stale after model change | Model id mismatch | Mark invalid, offer rebuild | Vector search off |
| Watcher missed events | Reconciliation scan | Re-index affected objects | Brief staleness |
| Disk full during rebuild | Write error | Abort cleanly, retain previous index | Rebuild deferred |

**The design rule across every row: derived-state failure degrades retrieval quality and never blocks core function.** A user with a corrupt graph, a dead sidecar and no embeddings must still be able to open the app, search their notes, read and write, record memories, and compile context. If any derived-state failure can prevent that, the tiering in §2 has been violated.
