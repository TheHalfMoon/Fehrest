# O. Performance Budgets

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Measurable target envelopes, not adjectives. Every budget states what happens when it is missed.

---

## 1. Basis and honesty about it

Budgets are anchored on measurements from [E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint), [E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution) and [E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-cold-vs-warm) — the only real numbers available before implementation:

| Measured | Value |
|---|---|
| Graphify extraction | 776 files in 42.22 s → **≈18.4 files/s**, 12 workers |
| Nodes/edges per file | ≈17.7 nodes, ≈34.7 edges |
| Graphify cold import | **4,451 ms** |
| Graphify warm import | **276 ms** |
| Bare CPython start | ≈98–119 ms |
| Sidecar install footprint | 32 packages, **130 MB** |

**Everything else in this document is projection.** Two caveats that a reviewer should hold against every number below:

1. All measurements are single-machine, Windows 11, cold cache ([E-15 environment](research/EVIDENCE_LOG.md#measurement-environment)). Cross-platform re-measurement is required at [Phase 0](15-IMPLEMENTATION-PHASES.md).
2. Extrapolation assumes linearity in file count, which is [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) — **unproven beyond 776 files.** Cross-file symbol resolution is a plausible superlinear term. [B-1](10-BENCHMARK-PLAN.md) decides this, and if it fails these budgets are void, not merely optimistic.

Reference hardware for all budgets: 4-core / 16 GB / NVMe, on each of Windows, macOS and Linux.

---

## 2. Vault size classes

| Class | Files | Attachments | Events | Memories |
|---|---|---|---|---|
| **S** | 1,000 | 100 MB | 10K | 1K |
| **M** | 10,000 | 1 GB | 100K | 10K |
| **L** | 100,000 | 10 GB | 500K | 100K |
| **XL** | 1,000,000 | 100 GB | 5M | 1M |

**XL is explicitly out of scope for v1** and is listed only so that no design choice silently forecloses it. Targeting XL would force graph partitioning, index sharding and a distributed rebuild model — complexity that would sink the MVP for a user base that does not yet exist.

---

## 3. Startup

| Operation | S | M | L | Miss behaviour |
|---|---|---|---|---|
| Cold start to interactive | < 1 s | < 2 s | < 5 s | Blocking defect |
| Warm start to interactive | < 500 ms | < 800 ms | < 1.5 s | Blocking defect |
| First search available | < 1 s | < 2 s | < 5 s | Blocking defect |
| Graph available after start | background | background | background | **Must never block** |

**Hard rule: the 4,451 ms Graphify cold import may never appear on the startup path** ([E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-cold-vs-warm)). The sidecar starts lazily on first graph need. A build in which app startup pays sidecar import cost is a release blocker, not a performance regression.

---

## 4. Indexing

### 4.1 Initial full index

| Tier | S | M | L |
|---|---|---|---|
| **D1** (object, links, FTS, memory) | < 10 s | < 60 s | < 10 min |
| **D2** (graph) | ~1 min | **~9 min** | **~90 min** |
| **D3** (embeddings, optional) | ~10 min | ~2 h | impractical without GPU |

The D2 figures derive directly from 18.4 files/s. They are the numbers that shape the architecture:

- D2 must be a **background, resumable, cancellable** job with visible progress ([N §3.8](13-RECOVERY-MODEL.md#38-interrupted-rebuild)).
- D2 must be **genuinely optional** — retrieval degrades to FTS-only without it ([E §8](04-DERIVED-DATA-MODEL.md#8-failure-and-degradation)).
- A 90-minute rebuild that restarts from zero on interruption is unacceptable, which is why durable progress is a requirement rather than an optimisation.

### 4.2 Incremental

| Operation | Target (M) | Miss behaviour |
|---|---|---|
| Single file save → D1 query-visible | **< 200 ms p95** | Blocking defect |
| Single file save → D2 graph-updated | < 5 s p95 | Degraded, acceptable |
| Bulk change (git checkout, 1000 files) → D1 | < 30 s | Degraded |
| Watch-event debounce | 300 ms | Tunable |

The 200 ms D1 target is the one users feel. Search returning stale results for a file just edited is immediately noticeable and erodes trust in the whole system, so this budget is a defect threshold rather than a quality goal.

---

## 5. Query

| Operation | S p50/p95 | M p50/p95 | L p50/p95 |
|---|---|---|---|
| Identity lookup | 1 / 5 ms | 1 / 5 ms | 2 / 10 ms |
| Structured property query | 5 / 20 ms | 10 / 40 ms | 30 / 120 ms |
| FTS search | 10 / 40 ms | 25 / 100 ms | 80 / 300 ms |
| Graph expansion (2 hops, capped) | 20 / 80 ms | 40 / 150 ms | 100 / 400 ms |
| Memory resolution (single subject) | 2 / 10 ms | 3 / 15 ms | 8 / 30 ms |
| Backlinks for one object | 5 / 20 ms | 8 / 30 ms | 20 / 80 ms |

---

## 6. Context compilation

| Vault | p50 | p95 | Miss behaviour |
|---|---|---|---|
| S | < 150 ms | < 400 ms | Degraded |
| M | < 400 ms | < 1.2 s | Degraded |
| L | < 1.5 s | < 4 s | Investigate |

Latency is a first-class metric because LongMemEval-V2 treats accuracy and query latency as co-equal ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). A compiler that is right in 30 seconds will not be used, and an unused compiler has no measurable quality.

**Quality budgets:** compression ≥ 20× versus raw history at equal or better correctness; unsourced items **exactly 0**; determinism **100%** across repeated runs on unchanged state.

Determinism at 100% is a correctness requirement, not a performance target — anything less breaks replay and [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable).

---

## 7. Memory footprint

| State | S | M | L |
|---|---|---|---|
| Core process RSS, idle | < 150 MB | < 250 MB | < 500 MB |
| Core process RSS, indexing | < 400 MB | < 800 MB | < 1.5 GB |
| Sidecar RSS, idle | < 200 MB | < 200 MB | < 200 MB |
| Sidecar RSS, extracting | < 1 GB | < 2 GB | < 3 GB |
| **Total during full index** | < 1.5 GB | < 3 GB | < 4.5 GB |

The sidecar spawns 12 worker processes during extraction ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)). Worker count must be **configurable and capped by available memory**, not fixed at core count: 12 workers on a 8 GB machine is a swap-thrash scenario that would make a large vault unindexable.

---

## 8. Disk

| Artifact | S | M | L |
|---|---|---|---|
| Canonical files | user's own | — | — |
| Event log (1 year) | ~20 MB | ~200 MB | ~1 GB |
| Memory log (1 year) | ~2 MB | ~20 MB | ~200 MB |
| SQLite derived | ~30 MB | ~300 MB | ~3 GB |
| Graph derived | ~10 MB | ~100 MB | ~1 GB |
| Embeddings (optional) | ~30 MB | ~300 MB | ~3 GB |
| **Derived total (no vectors)** | ~40 MB | ~400 MB | ~4 GB |

**Rule: derived state must stay under 50% of canonical size for a typical vault.** Exceeding it means Fehrest costs more disk than the knowledge it indexes, which is difficult to justify to a user and is a signal that something is being stored that should be recomputed.

**Installer:** core < 60 MB; optional graph capability +200–300 MB ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)); optional local model, user-supplied.

Shipping a ~350 MB default installer for a note-taking app would be a product problem, which is exactly why the graph is an **optional capability install** rather than bundled by default.

---

## 9. Growth over time

Ten years at 50 memories/day and 500 events/day: ~1.8M events, ~180K memories, ~2 GB of canonical logs.

Requirements: query latency must not degrade more than 2× from year 1 to year 10 on a fixed vault size; T2 compaction must keep the *active* log within an order of magnitude of the T1 log; and startup must not scan the full history — projections are incremental and checkpointed.

The last point matters most. A startup that replays 1.8M events would take minutes by year ten. Memory and object projections must be checkpointed so startup replays only events since the last checkpoint, with a full replay available as a repair operation.

---

## 10. Human-factor budgets

Not performance in the usual sense, but they determine whether controls work:

| Metric | Target | Rationale |
|---|---|---|
| Memory confirmations per active day | **< 5** | Above this users approve blindly and the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) control becomes theatre |
| Tool approvals per agent session | < 3 | Same failure mode ([T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin)) |
| Time to first useful context after vault open | < 5 min | Onboarding viability |
| Manual steps to recover from any [N](13-RECOVERY-MODEL.md) scenario | 0–1 | Recovery must not require expertise |

These are measured in dogfooding ([B-5](10-BENCHMARK-PLAN.md)). Missing them means the *rules* are wrong, not the user — a distinction worth stating, because the usual response to alert fatigue is to blame the operator.

---

## 11. Enforcement

Budgets are enforced in CI on C-SMALL and C-MED (nightly for C-LARGE): a regression over 20% fails the build; a budget miss on a "blocking defect" row blocks release; all results are tracked over time so drift is visible before it becomes a rewrite.

A budget that is missed and then quietly raised is worse than no budget. Any budget change requires an ADR-style note recording the old value, the new value, and why the change is acceptable rather than a concession.

---

## 12. What would force redesign

| Finding | Consequence |
|---|---|
| D1 incremental exceeds 1 s p95 at M | Indexing architecture redesign |
| D2 full index exceeds 3× projection at M ([H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) falsified) | Graph must be scoped/partitioned, or [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graphify-runs-as-a-managed-long-lived-sidecar) reopens toward a native port |
| Context compilation exceeds 2× budget at M | Pre-computation and caching become mandatory, threatening determinism |
| Memory footprint exceeds 2× at M | Streaming/paged processing required throughout |
| Derived state exceeds canonical size | Index design is wrong |
| Startup exceeds 5 s at M | Projection checkpointing is insufficient |
