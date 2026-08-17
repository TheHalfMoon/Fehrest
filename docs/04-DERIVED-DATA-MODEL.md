# E. Derived Data Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Derived state is everything reconstructable from canonical state. Its governing property is [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable): delete all of it, restart, and the system is functionally identical.

That property is not a convenience. It is what makes every index decision in this document reversible, and it is the reason index corruption is an availability problem rather than a security problem ([T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes)).

---

## 1. Inventory

| Artifact | Store | Rebuild source | Rebuild cost (10K files) | Required? |
|---|---|---|---|---|
| Object index | `index.sqlite` | Frontmatter + file stat | ~1 min | Yes |
| Link/backlink index | `index.sqlite` | Markdown link parse | ~1 min | Yes |
| FTS5 index | `index.sqlite` | Object bodies | ~2 min | Yes |
| Memory projection | `index.sqlite` | Memory JSONL | seconds | Yes |
| Event mirror | `index.sqlite` | Event JSONL | ~1 min | No — convenience |
| Structural graph | `derived/graph/` | Sidecar extraction | **~9 min** ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)) | No |
| Graph↔object ID map | `index.sqlite` | Graph + object index | seconds | No |
| Communities | `derived/graph/` | Graph | ~1 min | No |
| Extracted text | `derived/cache/` | Attachments | Varies; **lossy if source deleted** | No |
| Embeddings | `derived/vectors/` | Object bodies + model | Hours, needs a model | **No** |
| Thumbnails / summaries | `derived/cache/` | Sources | Varies | No |

Only five artifacts are required, and all five rebuild in **under 5 minutes for 10K files**. This is deliberate: the mandatory rebuild path must be fast enough that "delete derived state and restart" is a viable support instruction. Everything slow is optional.

---

## 2. Tiering

| Tier | Meaning | Members | Startup behaviour |
|---|---|---|---|
| **D1 — Required** | Core function degrades without it | object index, links, FTS, memory projection | Built before the app is interactive; must be fast |
| **D2 — Enhancing** | Improves retrieval; absence is graceful | graph, communities, ID map, event mirror | Built in background; **never gates startup** |
| **D3 — Optional** | Requires a model or heavy compute | embeddings, summaries, OCR, transcripts | Explicit opt-in only |

D2's "never gates startup" is forced by measurement: full graph extraction is ~9 minutes at 10K files and ~90 minutes at 100K ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)). Any design that blocks the UI on graph availability is dead on arrival for a large vault. The application must be fully usable — search, read, edit, memory, context compilation — with the graph entirely absent.

---

## 3. SQLite as the derived store

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

-- Graph node ids are name-derived and unstable (E-4): mapping only, never identity.
CREATE TABLE graph_node_map (
  graphify_node_id TEXT NOT NULL,
  object_id TEXT REFERENCES object(id) ON DELETE CASCADE,
  symbol TEXT, source_file TEXT, source_location TEXT,
  confidence TEXT NOT NULL,         -- EXTRACTED | INFERRED | AMBIGUOUS
  PRIMARY KEY (graphify_node_id, object_id)
);
```

Two schema choices carry weight:

- **`content_hash` decides staleness, `mtime` is only a fast-path hint.** mtime is unreliable across filesystems, sync tools, and restores, and trusting it enables the provenance race in [T-9](02-THREAT-MODEL.md#t-9--filesystem-race-conditions).
- **`frontmatter` is stored verbatim as JSON.** Round-tripping through a typed struct is how unknown fields get dropped, violating [R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules).

---

## 4. The Graphify boundary

### 4.1 Ownership

| Owned by Graphify (sidecar) | Owned by Fehrest (core) |
|---|---|
| tree-sitter parsing, 28 grammars | Object identity |
| Node/edge extraction | Canonical writes |
| Cross-file symbol resolution | ID mapping and scope enforcement |
| Community detection | Retrieval policy and ranking |
| Graph diff | Memory and provenance |

The rule is [R-7](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules): **the sidecar has no authority.** It receives file paths and returns proposed facts. It cannot write canonical state, allocate identity, or influence authorization.

### 4.2 The wire contract

Fehrest consumes the documented extraction schema as a stable contract ([E-2](research/EVIDENCE_LOG.md#e-2--graphify-module-inventory-and-size)):

```json
{
  "nodes": [{"id": "...", "label": "...", "source_file": "...", "source_location": "L42"}],
  "edges": [{"source": "...", "target": "...", "relation": "calls|imports|...",
             "confidence": "EXTRACTED|INFERRED|AMBIGUOUS"}]
}
```

Core validates every response against this schema before accepting it — the sidecar is semi-trusted ([boundary B2](02-THREAT-MODEL.md#4-trust-boundaries)), so a malformed or hostile response must be rejected rather than ingested.

**Measured properties Fehrest must design around:**
- Confidence is effectively binary: `EXTRACTED` 97.2%, `INFERRED` 2.8%, `AMBIGUOUS` **0.0%** ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)). No UI or trust logic may depend on `AMBIGUOUS` being populated, though the vocabulary stays open.
- Observed relation vocabulary: `calls`, `contains`, `rationale_for`, `imports`, `references`, `imports_from`, `method`, `indirect_call`. Fehrest treats this as **open** and must not enumerate it exhaustively in a schema constraint, or an upstream addition breaks ingestion.
- Missing optional grammars degrade to partial graphs with warnings rather than failures. Fehrest surfaces these as index health, not errors.

### 4.3 ID mapping is the critical seam

Graphify node IDs are name-derived slugs, unstable under rename and Unicode representation, with documented same-filename collisions ([E-4](research/EVIDENCE_LOG.md#e-4--graphify-node-ids-are-name-derived-not-stable-identities)). Therefore:

1. `graph_node_map` is many-to-many and **fully rebuildable**.
2. No canonical record ever references a Graphify node ID.
3. A collision produces multiple mappings, surfaced as ambiguity, never silently resolved to one.
4. On rename, the map entry is invalidated and re-derived; object identity is untouched because it never depended on the graph.

This is the concrete mechanism by which [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) survives contact with a donor that violates it.

### 4.4 Process model

**Long-lived managed sidecar.** Forced by measurement: cold import 4,451 ms, warm 276 ms, bare interpreter ~100 ms ([E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-cold-vs-warm)). Per-operation invocation costs ~376 ms of pure overhead even warm, making per-file calls impossible; the 4.45 s cold path would make first use look broken.

Lifecycle: lazy start on first graph need (never on app launch — startup must not pay 4.45 s); private authenticated local channel; read-only path-confined to the vault; no credentials; network features disabled ([T-11](02-THREAT-MODEL.md#t-11--sidecar-network-egress)); supervised with restart-on-crash and backoff; idle shutdown; resource caps. Extraction spawns 12 worker subprocesses ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)), which must be counted in resource budgets.

**A Rust port is not justified by current evidence.** The measured cost being amortised is *startup*, which a sidecar eliminates entirely. Porting 60,202 lines across 28 grammars would address *throughput*, which has not been shown to be the binding constraint. Reconsider only if [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) is falsified or packaging proves untenable. See [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graphify-runs-as-a-managed-long-lived-sidecar).

---

## 5. Incremental maintenance

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

## 6. Vectors

**Optional, D3, off by default.** Three independent reasons:

1. **Constitutional.** [I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) — embeddings require a model.
2. **Engineering.** sqlite-vec's current release line is `v0.1.10-alpha.*`, newest stable `v0.1.9` ([E-12](research/EVIDENCE_LOG.md#e-12--vector-store-maturity)). Alpha status alone disqualifies it from being required.
3. **Empirical.** The only prose-memory benchmark reported for the graph donor shows graph retrieval **tying** dense RAG (76% vs 76% on LongMemEval-S, n=50), while its clear wins are recall and cost ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)). That evidence does not establish that vectors are unnecessary — it establishes that neither approach dominates, which means vectors must earn inclusion by measurement on Fehrest's own corpus rather than by convention.

Sequencing: FTS5 first, measured; graph expansion second, measured; vectors third, adopted only if [B-3](10-BENCHMARK-PLAN.md) shows a material gain. Backend chosen by benchmark between sqlite-vec and USearch ([SRC-012](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval), [SRC-013](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval)).

When enabled, embeddings are stored with the model identifier and dimension. A model change invalidates the whole index — which is fine, because it is derived.

---

## 7. Rebuild semantics

**Determinism requirement:** rebuilding must produce *functionally identical* query results, not byte-identical files. Byte-identical is unachievable (SQLite page layout, insertion order, parallel extraction ordering) and demanding it would create a permanently failing test.

`test_nuke_and_rebuild_equivalence` therefore compares a fixed query set's results — ordered result IDs, scores within tolerance, memory resolutions, context package digests — rather than file bytes. This is the most important test in the suite because it is the guarantee that every decision in this document is reversible.

**Cost, extrapolated from measurement** ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution), linear assumption flagged as [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count)):

| Vault | D1 (required) | D2 graph | D3 embeddings |
|---|---|---|---|
| 1K files | < 10 s | ~1 min | ~10 min |
| 10K files | < 60 s | ~9 min | ~2 h |
| 100K files | < 10 min | **~90 min** | impractical without a GPU |

The 100K graph figure is the number that shapes the architecture: it must be a resumable background job with visible progress, and it must be genuinely optional. Budgets in [O](14-PERFORMANCE-BUDGETS.md).

---

## 8. Failure and degradation

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
