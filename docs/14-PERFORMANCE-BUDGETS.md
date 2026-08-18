# O. Performance Budgets

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Measurable target envelopes, not adjectives. Every budget states what happens when it is missed.

---

## 1. Basis and honesty about it

Budgets are anchored on measurements from [E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint), [E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary) and [E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-preliminary) — the only real numbers available before implementation:

| Measured | Value |
|---|---|
| Graphify extraction | 776 files in 42.22 s → **≈18.4 files/s**, 12 workers |
| Nodes/edges per file | ≈17.7 nodes, ≈34.7 edges |
| Graphify cold import | **4,451 ms** |
| Graphify warm import | **276 ms** |
| Bare CPython start | ≈98–119 ms |
| Sidecar install footprint | 32 packages, **130 MB** |

> **All Graphify figures are `PRELIMINARY / SINGLE-ENVIRONMENT / SINGLE-CORPUS` ([R1-07](reviews/F1-R1-RECONCILIATION.md)).** They were measured on one machine against one corpus — Graphify's own Python source. They indicate *order of magnitude and architectural shape*, nothing more.

**Everything else in this document is projection.** Three caveats a reviewer should hold against every number below:

1. All measurements are single-machine, Windows 11, cold cache ([E-15 environment](research/EVIDENCE_LOG.md#measurement-environment)). Cross-platform re-measurement is required at [Phase 0](15-IMPLEMENTATION-PHASES.md).
2. Extrapolation assumes linearity in file count — [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count), **unproven beyond 776 files.** Cross-file symbol resolution is a plausible superlinear term.
3. **Corpus type is entirely unmodelled.** One code-heavy corpus tells us nothing about a Markdown-heavy vault, a many-small-files vault, or a few-large-files vault. This is the gap [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) exists to close, and it is likely the largest source of error in this document.

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

**Hard rule: the 4,451 ms Graphify cold import may never appear on the startup path** ([E-6](research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-preliminary)). The sidecar starts lazily on first graph need. A build in which app startup pays sidecar import cost is a release blocker, not a performance regression.

---

## 4. Indexing

### 4.1 Initial full index

| Tier | S | M | L |
|---|---|---|---|
| **D1** (object, links, FTS, memory) | < 10 s | < 60 s | < 10 min |
| **D2** (graph) | **TBD — GI-BENCH** | **TBD — GI-BENCH** | **TBD — GI-BENCH** |
| **D3** (embeddings, optional) | ~10 min | ~2 h | impractical without GPU |

> **D2 budgets withdrawn in F1-R1 ([R1-07](reviews/F1-R1-RECONCILIATION.md)).** F1 published ~1 min / ~9 min / ~90 min as budgets. Those were a **naive linear extrapolation from one corpus of one type on one machine** and must not be treated as system properties. Real budgets are set from [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix), which measures 4 vault sizes × 5 corpus types × 10 operations × concurrency. Corpus type in particular was entirely unmodelled and is likely to dominate.

The *architectural consequences* below stand regardless of the exact numbers, because they follow from the graph build being **minutes-to-hours rather than milliseconds** — which the preliminary measurement establishes even if its magnitude is wrong:

- D2 must be a **background, resumable, cancellable** job with visible progress ([N §3.8](13-RECOVERY-MODEL.md#38-interrupted-rebuild)).
- D2 must **never gate startup or interactivity** — retrieval degrades to FTS-only while it is absent or building ([E §9](04-DERIVED-DATA-MODEL.md#9-failure-and-degradation)).
- A long rebuild that restarts from zero on interruption is unacceptable, which is why durable progress is a requirement rather than an optimisation.

Note the distinction: the graph *build* may be incomplete at any moment, but **Graph Intelligence is a core current product hypothesis, not an optional feature** ([R1-06](reviews/F1-R1-RECONCILIATION.md)). Degrading gracefully while it builds is not the same as the product working without it. That hypothesis is nonetheless **explicitly falsifiable** — if measured benefit does not justify measured cost, [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) permits redesign or removal, and these budget rows go with it.

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

Determinism at 100% is a correctness requirement, not a performance target — anything less breaks replay and [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable).

---

## 7. Memory footprint

| State | S | M | L |
|---|---|---|---|
| Core process RSS, idle | < 150 MB | < 250 MB | < 500 MB |
| Core process RSS, indexing | < 400 MB | < 800 MB | < 1.5 GB |
| Sidecar RSS, idle | < 200 MB | < 200 MB | < 200 MB |
| Sidecar RSS, extracting | < 1 GB | < 2 GB | < 3 GB |
| **Total during full index** | < 1.5 GB | < 3 GB | < 4.5 GB |

The sidecar spawns 12 worker processes during extraction ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)). Worker count must be **configurable and capped by available memory**, not fixed at core count: 12 workers on a 8 GB machine is a swap-thrash scenario that would make a large vault unindexable.

---

## 8. Disk

> **The log rows below are derived from the unvalidated 500 events/day assumption and are `PENDING B-0`** ([R2-12](reviews/F1-R2-RECONCILIATION.md)). Index and graph rows are derived from file counts and are unaffected.

| Artifact | S | M | L |
|---|---|---|---|
| Canonical files | user's own | — | — |
| Event log (1 year) — **PENDING B-0** | ~20 MB | ~200 MB | ~1 GB |
| Memory log (1 year) — **PENDING B-0** | ~2 MB | ~20 MB | ~200 MB |
| Served-item manifests (1 year) — **PENDING B-0** | TBD | TBD | TBD |
| SQLite derived | ~30 MB | ~300 MB | ~3 GB |
| Graph derived | ~10 MB | ~100 MB | ~1 GB |
| Embeddings (optional) | ~30 MB | ~300 MB | ~3 GB |
| **Derived total (no vectors)** | ~40 MB | ~400 MB | ~4 GB |

**Rule: derived state must stay under 50% of canonical size for a typical vault.** Exceeding it means Fehrest costs more disk than the knowledge it indexes, which is difficult to justify to a user and is a signal that something is being stored that should be recomputed.

**Installer:** core < 60 MB; optional graph capability +200–300 MB ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)); optional local model, user-supplied.

Shipping a ~350 MB default installer for a note-taking app would be a product problem, which is exactly why the graph is an **optional capability install** rather than bundled by default.

---

## 9. Growth over time

```
EVENT AND MEMORY VOLUME:
UNVALIDATED PLANNING ASSUMPTION — PENDING MEASUREMENT (B-0)
```

> **RECLASSIFIED IN F1-R2 ([R2-12](reviews/F1-R2-RECONCILIATION.md)).** The figures below rest on **50 memories/day and 500 events/day**. Those numbers were never measured. They are not a budget, not a finding, and not a system property — they are an assumption that has been propagating through this document, [F §8](05-MEMORY-MODEL.md#8-growth-and-forgetting), [D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief) and [§8 Disk](#8-disk) as though it were grounded.
>
> **What was also NOT accepted:** the review's counter-estimate of `10K–100K events/day`. It is an unverified estimate offered without measurement. Replacing one ungrounded number with another that is two orders of magnitude larger would change which decisions are wrong without making any of them right — and a 200× disagreement about the input is itself the finding: **nobody knows, so measure.**

**Illustrative only, at the assumed rate:** ten years at 50 memories/day and 500 events/day → ~1.8M events, ~180K memories, ~2 GB of canonical logs.

**[B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) at Phase 0** captures or reconstructs representative real multi-agent usage and counts potential events **by class**. Its measured distributions — not the numbers above — decide:

- which event types deserve canonical retention at all;
- whether the T1/T2 split is necessary and where the line falls;
- the retention window and compaction policy;
- the disk budget in [§8](#8-disk);
- checkpoint cadence;
- the per-item cost ceiling for the served-item manifest ([H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1)).

**Gate: no event-tiering, retention, compaction or checkpoint-cadence parameter may be frozen before B-0 reports.**

**Requirements that hold regardless of volume**, because they follow from the architecture rather than from the number: query latency must not degrade more than 2× from year 1 to year 10 on a fixed vault size; compaction must keep the *active* log within an order of magnitude of the permanent log; and **startup must not scan the full history** — projections are incremental and checkpointed ([E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints)).

The last point matters most, and it holds more strongly the larger the true volume turns out to be. Memory and object projections are checkpointed so that startup replays only events since the last valid checkpoint.

**Two startup paths, budgeted separately ([R2-08](reviews/F1-R2-RECONCILIATION.md)):**

| Path | Budget |
|---|---|
| **Healthy start** — a valid checkpoint exists; replay the tail only | [§3](#3-startup) |
| **Degraded recovery** — no valid checkpoint; full replay of canonical state | **Deliberately unbudgeted. Measured, then set** |

**No degraded-path number is invented here.** Setting one would require knowing the event volume (unmeasured, above), the replay throughput (unimplemented), and the checkpoint cadence (unset because it depends on the first two). A plausible-sounding figure derived from three unknowns is not a budget; it is a guess that later gets cited as a requirement.

---

## 10. Human-factor budgets

Not performance in the usual sense, but they determine whether controls work:

| Metric | Target | Rationale |
|---|---|---|
| Memory confirmations per active day | **UNVALIDATED — assumed < 5, to be measured** | Above whatever the real tolerance is, users approve blindly and the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) control becomes theatre |
| Tool approvals per agent session | < 3 | Same failure mode ([T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin)) |
| Time to first useful context after vault open | < 5 min | Onboarding viability |
| Manual steps to recover from any [N](13-RECOVERY-MODEL.md) scenario | 0–1 | Recovery must not require expertise |

> **The "< 5 confirmations per active day" figure is NOT canonised ([R2-06](reviews/F1-R2-RECONCILIATION.md)).** It appeared in F1 as a design target and was then cited across [F §9](05-MEMORY-MODEL.md#9-falsification-criteria), [F-17](17-FAILURE-CONDITIONS.md#f-17--confirmation-fatigue) and [B-5](10-BENCHMARK-PLAN.md#b-5--memory-promotion-quality) as though it were a measured tolerance. **It is an assumption about human behaviour, made without observing any human**, and it has never been tested against real multi-agent traces — which is also where the confirmation volume actually comes from. Both the *tolerable* rate and the *produced* rate are measured in dogfooding before either becomes a gate, and **before automatic promotion is widened**.

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
| D2 full index exceeds 3× projection at M ([H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) falsified) | Graph must be scoped/partitioned, or [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) reopens toward a native port |
| Context compilation exceeds 2× budget at M | Pre-computation and caching become mandatory, threatening determinism |
| Memory footprint exceeds 2× at M | Streaming/paged processing required throughout |
| Derived state exceeds canonical size | Index design is wrong |
| Startup exceeds 5 s at M **on the healthy path** | Projection checkpointing is insufficient |
| **Measured event volume ([B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement)) differs from assumption by more than an order of magnitude** | Every log-derived row in [§8](#8-disk) and [§9](#9-growth-over-time) is re-derived, and the T1/T2 tiering in [D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief) is re-decided before it is frozen |
| **Degraded full-replay recovery proves unacceptably slow once measured** | Increase checkpoint cadence, or checkpoint more projections — never make a checkpoint authoritative to avoid replaying ([E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints)) |

---

## 13. Local resource-safety bounds

> **ADDED IN G3 ([SEC-R7](reviews/G3-SECURITY-RECONCILIATION.md), G3-M5).** An authorized agent can drive operations that **permanently amplify canonical state** — compile requests writing T1 manifests, memory writes, approval pairs. Each is individually legitimate; unbounded, they are a disk-exhaustion and audit-flood primitive that no authorization check catches, because every request is authorized.

### 13.1 These are safety bounds, not product limits

**The distinction is a founder principle and it is not negotiable here.** Fehrest imposes **no artificial product limits**. The bounds below exist because a local process can fill a local disk, and for no other reason.

| **NOT permitted** — commercial or artificial | **Permitted** — local resource safety |
|---|---|
| Daily compile limits | Maximum accepted request size |
| Paid-tier limits | Maximum event size |
| Trial-style limits | Bounded concurrent work |
| Arbitrary lifetime quotas | Bounded compile frequency/burst **where required** |
| Vendor-controlled waiting queues | Disk-reserve threshold |
| | Bounded pending-approval amplification |

**Exact numeric values remain benchmark and configuration decisions** ([B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) supplies the real distributions). Freezing numbers here would repeat the R2-12 error of shipping an unmeasured figure as a threshold.

### 13.2 Prefer absorption over rejection

Where possible, **coalescing · idempotency · deduplication · bounded concurrency** come before rate rejection. A duplicate compile of unchanged state should be *absorbed*, not refused — refusing correct work is a worse failure than doing it once.

### 13.3 Properties of a safety rejection

When a bound does fire, the rejection is:

```
EXPLICIT · AUDITED · LOCAL · NON-COMMERCIAL · NON-TIER-BASED
```

and it **must never silently discard canonical state**. A dropped memory write that the caller believes succeeded is data loss wearing a rate limiter's clothing — the failure must be visible to the caller and recorded.

Kill test [K-24b](11-SECURITY-VERIFICATION-PLAN.md#13-kill-test-canon).
