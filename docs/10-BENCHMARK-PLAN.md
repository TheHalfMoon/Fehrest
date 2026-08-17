# K. Benchmark Plan

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

The benchmark program exists before implementation so that architectural claims are falsifiable rather than defended. Every benchmark names the decision it can overturn.

---

## 1. Principles

1. **Every benchmark decides something.** A benchmark that cannot change a decision is telemetry.
2. **Baselines are run locally, not cited.** Every comparative number in the evidence log is vendor-reported or self-measured; none is third-party replicated ([registry §13](research/FEHREST_SOURCE_REGISTRY.md#13-known-registry-gaps)).
3. **Report intervals, not point estimates.** LongMemEval-S at n=50 has a 95% interval near ±12 pp ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)); a 2-point "win" there is noise. Any result without an interval is inadmissible.
4. **Latency is co-equal with accuracy.** LongMemEval-V2 targets both ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). A compiler that is right in 30 seconds will not be used.
5. **The bar is a competent agent, not a weak RAG baseline.** LME-V2 reports 72.5% best vs **69.3% for an off-the-shelf coding agent** vs 48.5% for the strongest RAG. Beating RAG proves nothing.
6. **Reproducible by a third party.** Fixed corpora, pinned models, pinned seeds, recorded hardware, committed harness.

---

## 2. Corpora

| Corpus | Contents | Purpose |
|---|---|---|
| **C-SMALL** | 1K files, synthetic + real notes | Fast CI regression |
| **C-MED** | 10K files, mixed notes/code/PDFs | Primary target |
| **C-LARGE** | 100K files, generated | Scaling limits |
| **C-TEMPORAL** | Hand-built history with known supersessions and ground-truth "current" values at 20 checkpoints | Temporal and supersession correctness |
| **C-ADVERSARIAL** | Injection payloads, malformed files, symlinks, polyglots, poisoned memories | Security ([L](11-SECURITY-VERIFICATION-PLAN.md)) |
| **C-PROJECT** | A real 3-month project history: sessions, decisions, reversals, dead ends | [B-7](#b-7--agent-continuation-the-defining-experiment) |
| **LME-V2** | LongMemEval-V2, obtained from source | External validity |
| **LOCOMO / LME-v1** | External | Cross-checks against published numbers |

C-TEMPORAL and C-PROJECT must be **hand-built with ground truth**, because no public corpus encodes "the founder decided X on date D, reversed it on date E for reason R." They are the most valuable and most expensive artifacts in this plan, and they are prerequisites for [B-4](#b-4--temporal-and-supersession-correctness) and [B-7](#b-7--agent-continuation-the-defining-experiment).

---

## 3. Benchmarks

### B-1 — Ingestion and index throughput

**Measures.** Files/s, wall time, peak RSS, index size, for D1 and D2 across C-SMALL/MED/LARGE, cold and warm.
**Baseline.** Measured Graphify extraction: ~18.4 files/s, 776 files in 42.2 s, 12 workers ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)).
**Decides.** [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) — whether extraction is linear in file count. Also validates or breaks the budgets in [O](14-PERFORMANCE-BUDGETS.md).
**Fails if.** 10K extraction exceeds 2× the linear projection → superlinear cross-file resolution; graph must be partitioned or scoped, and [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) is reopened.

### B-2 — Incremental update latency

**Measures.** Time from file save to (a) D1 query-visible, (b) D2 graph-updated. p50/p95/p99.
**Targets.** D1 < 200 ms p95 at 10K files; D2 < 5 s p95 for a single-file change.
**Decides.** Whether incremental maintenance is viable, or whether periodic batch rebuild is forced — which would materially degrade the product.
**Fails if.** D1 exceeds 1 s p95 → search feels stale after editing, which erodes trust in the entire system.

### B-3 — Retrieval quality by stage

**Measures.** recall@k (k = 5, 10, 20), nDCG@10, MRR, on C-MED and LME-v1/V2, with **ablation per stage.**

| Configuration | Question answered |
|---|---|
| FTS5 only | The baseline floor |
| FTS5 + structured | Does exact lookup help? |
| + graph expansion | **Does the Graphify dependency earn its cost?** |
| + vectors | **Do vectors earn D2 promotion?** |
| Full RRF fusion | Does fusion beat its best component? |
| Dense-only | External comparison |
| Graph-only | External comparison |

**Decides.** [ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) and, jointly with [B-1](#b-1--ingestion-and-index-throughput), whether Graphify remains in the architecture at all.
**Fails if.** Graph expansion adds no measurable recall over FTS + memory → drop compiler stage [4], and Graphify loses most of its justification ([failure condition F-3](17-FAILURE-CONDITIONS.md)). Or vectors beat lexical+graph materially → promote vectors to default-on ([ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) reverses).
**Method note.** Ablation is mandatory. A single "our system scores X" number cannot attribute value to any component, and attribution is the entire point.

### B-4 — Temporal and supersession correctness

**Measures.** On C-TEMPORAL: current-state accuracy at each checkpoint; historical-state accuracy ("what was true in March"); **belief-state accuracy** ("what did we believe in May"); superseded-decision retrieval; stale-memory usage rate; contradiction detection precision/recall.
**Targets.** Current-state accuracy **100%** — this is deterministic resolution, not retrieval, so anything below 100% is a bug, not a quality score. Stale-memory usage 0%.
**Decides.** [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution). Also measures structured-`payload` extraction rate.
**Fails if.** Current-state resolution is not 100% deterministic → the core value proposition fails. Or `payload` is extractable for < 30% of memories → deterministic resolution covers too little to matter ([ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) reverses to prose-first, a much weaker system).

### B-5 — Memory promotion quality

**Measures.** On a hand-labelled candidate corpus: promotion precision/recall vs human labels, for rules-only vs model-assisted. Confirmation-queue volume per active day.
**Decides.** [H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value) — whether `AI OFF` is a real mode.
**Fails if.** Rules-only recall < 60% of model-assisted → `AI OFF` degrades to a read-only knowledge base, a thesis-level weakening requiring founder sign-off ([Q-4](16-OPEN-QUESTIONS.md)). Or queue volume > 5/day sustained → users approve blindly and the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) control becomes theatre.

### B-6 — Context compiler

**Measures.** Compile latency p50/p95 by corpus size; tokens produced vs budget; **compression ratio vs raw history**; determinism (identical digest over 100 runs on unchanged state); provenance completeness (unsourced items must be 0); omission honesty (does `omitted` match reality?).
**Targets.** Latency per [O](14-PERFORMANCE-BUDGETS.md); compression ≥ 20×; determinism 100%; unsourced items 0.
**Decides.** [H](07-CONTEXT-COMPILER-SPEC.md) viability.
**Fails if.** Digests vary on unchanged input → replay and audit impossible, [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) fails. Or p95 exceeds budget by 2× → pre-computation becomes mandatory.

### B-7 — Agent continuation: the defining experiment

**This is the benchmark that decides whether Fehrest should exist.**

**Setup.** On C-PROJECT: Agent A works the project across many sessions, then is destroyed. Agent B must continue correctly on a held-out task set.

**What Agent B receives — and does not ([R1-18](reviews/F1-R1-RECONCILIATION.md)):**

| Denied | Provided |
|---|---|
| ❌ Agent A's private chain-of-thought | ✅ The normal project files |
| ❌ Agent A's hidden internal state | ✅ Normal filesystem/search tools |
| ❌ Any raw conversation dump | ✅ **Fehrest-compiled context** |

This asymmetry is the whole experiment. Agent B has exactly what a real successor agent would have — the repository and its tools — **plus** Fehrest. The measured quantity is what Fehrest adds on top of a competent agent, not what it adds on top of nothing.

**Arms.**

| Arm | Receives |
|---|---|
| **Fehrest** | Compiled context package only |
| Raw stuffing | As much chat history as fits the budget |
| BM25 | Top-k passages |
| Dense RAG | Top-k passages |
| Hybrid RAG | RRF of both |
| Graph-only | Graph traversal results |
| Mem0 | Its own memory |
| **Plain agent** | **File tools, no memory system — the real bar** |
| No context | Floor |

**Metrics.** Task correctness; **constraint retention** (did it violate a stated constraint?); current-state accuracy; temporal accuracy; **superseded-decision misuse**; repeated-known-failure rate (did it retry a recorded gotcha?); provenance correctness; hallucination rate; abstention appropriateness; context tokens consumed; latency; security-policy adherence.

**Falsification threshold — stated numerically before any code exists:**

| Metric | Threshold vs plain-agent arm |
|---|---|
| Task correctness | **≥ +10 percentage points**, with the 95% interval excluding zero |
| Constraint violations (constraint present in package) | **Exactly 0** |
| Superseded-decision misuse | **Strictly lower**, and ≤ 5% absolute |
| Repeated-known-failure rate | **Strictly lower** |
| Provenance correctness | ≥ 95% of cited sources resolve and support the claim |
| Context tokens consumed | **≤ 50%** of the raw-stuffing arm at equal or better correctness |
| Security-policy adherence | Zero violations |

**+10 points is chosen deliberately.** LongMemEval-V2 reports the best memory system beating an off-the-shelf coding agent by **3.2 points** (72.5% vs 69.3%) ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). A 3-point margin on a self-authored corpus is indistinguishable from corpus bias. If Fehrest's entire architecture — bitemporal memory, deterministic resolution, graph intelligence, provenance, context compilation — cannot produce a margin materially larger than the published state of the art, the added complexity is not earning its cost.

**Fails if.** Any threshold is missed → **the product thesis is falsified.** Not a tuning problem. The correct response is to reconsider the product, not to lower the threshold.

**Design caveat.** The single most likely methodological flaw is that C-PROJECT is authored by the same people who designed the memory model, producing a corpus whose structure happens to suit Fehrest. Mitigations: the held-out task set is written **before** the compiler is tuned; a second corpus is sourced from a project Fehrest's authors did not run; grading is blind to arm.

### B-8 — Robustness and recovery

**Measures.** Time to detect and recover from: deleted index, corrupt SQLite, truncated event log, interrupted rebuild, killed sidecar, external file modification, git checkout of the vault.
**Decides.** [N](13-RECOVERY-MODEL.md) adequacy.
**Fails if.** Any failure requires manual repair, or any canonical data is lost.

### B-9 — `nuke-and-rebuild` equivalence

**Measures.** Query-result equality across a fixed query set before and after deleting all derived state.
**Decides.** [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) — and therefore the reversibility of every index decision in [E](04-DERIVED-DATA-MODEL.md) and the "derived corruption is not a security problem" argument in [T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes).
**Fails if.** Any divergence → the disposability claim is false and multiple documents lose their foundation.
**Note.** Compares *query results*, not file bytes; byte-identity is unachievable (SQLite page layout, parallel extraction order) and demanding it would create a permanently failing test. Runs in CI from Phase 1.

### B-11 — GI-BENCH — Graph Intelligence benchmark matrix

> **ADDED IN F1-R1 ([R1-07](reviews/F1-R1-RECONCILIATION.md)).** F1 extrapolated "100K files ≈ 90 min" from **one corpus of one type on one machine** and let it inform packaging and runtime decisions. That extrapolation is withdrawn. GI-BENCH replaces it and is a **prerequisite** to finalising [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape).

**Matrix.** Every cell measured, not extrapolated.

| Dimension | Values |
|---|---|
| **Vault size** | 1K · 10K · 50K · 100K files |
| **Corpus type** | Markdown-heavy · code-heavy · mixed · many-small-files · few-large-files |
| **Operation** | cold full build · warm full build · 1-file incremental · 10-file incremental · rename · move · delete · subtree move · external modification · watch-triggered rebuild |
| **Concurrency** | single worker · parallel workers |

**Measured per cell:** wall time · CPU time · peak RSS · disk growth · resulting node/edge counts · update latency · startup latency · packaging size · failure-recovery behaviour.

**Corpus type is the dimension F1 omitted entirely**, and it is likely the most consequential: a Markdown-heavy personal vault and a code-heavy repository exercise completely different extractor paths, and Fehrest's [v1 wedge](00-PRODUCT-THESIS.md#4-the-v1-user-wedge) has users with both. A runtime decision made on code-corpus numbers alone could be wrong for the median vault.

**Decides:**
- The runtime shape — lazy worker vs preloaded vs background process vs adaptation ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)).
- Whether packaging Graph Intelligence as an optional install is necessary or over-cautious.
- Whether [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) (linearity) holds, and in which corpus types it fails.
- Whether a different extractor should be evaluated ([R1-06](reviews/F1-R1-RECONCILIATION.md)).

**Fails if.** Any cell exceeds 3× its linear projection → the extractor is superlinear in that regime; scope or partition the graph, or evaluate alternatives. **Does not permit dropping the capability** — Graph Intelligence is CORE ([F-3](17-FAILURE-CONDITIONS.md#f-3--the-graph-intelligence-capability-does-not-earn-its-cost)).

**Gate.** No packaging, bundling or runtime decision may be finalised before GI-BENCH reports.

### B-10 — Scale and growth

**Measures.** Behaviour at C-LARGE and with 10 years of simulated events (~500K events, ~180K memories): cold start, search latency, compile latency, memory footprint, index size, compaction effectiveness.
**Fails if.** Cold start exceeds 10 s at 100K files, or memory growth is superlinear.

---

## 4. Security benchmarks

Detailed in [L](11-SECURITY-VERIFICATION-PLAN.md); summarised here because they are pass/fail release gates, not quality metrics.

| Benchmark | Gate |
|---|---|
| **S-1** Prompt-injection corpus (AgentDojo-derived) | **Zero** capability changes, zero unapproved tool executions |
| **S-2** Path traversal / symlink corpus | **Zero** escapes on all platforms |
| **S-3** Malformed vault fixtures | No crash, no corruption, no unbounded resource use |
| **S-4** Memory poisoning scenarios | All poisoned memories traceable and bulk-revocable by provenance |
| **S-5** Event-log tampering | 100% detection across edit/truncate/reorder/splice |
| **S-6** Scope isolation | **Zero** cross-project leakage, including via graph expansion |
| **S-7** Sidecar egress | Zero outbound connections during a full extraction |

---

## 5. Harness requirements

Committed in-repo under `bench/`. Requirements: one command runs a suite; pinned model, seed and tokenizer per run; hardware and OS recorded automatically; results as structured data plus a report; **confidence intervals mandatory**; every baseline runnable under identical conditions; blind grading with a second-judge agreement check (the donor reports 90.6% agreement, κ 0.81 — a reasonable target).

Two rules that prevent the harness from lying:
- **A run that cannot record its full configuration is invalid**, not "approximately right."
- **Baselines and Fehrest share one code path** for prompting, budgeting and grading. Adapters, not separate scripts — otherwise the comparison measures harness quality, not system quality.

---

## 6. Gating

| Phase | Must pass before exit |
|---|---|
| 1 | B-9 |
| 2 | B-1, B-2, B-9 |
| 3 | B-3, B-9 |
| 4 | B-4, B-5, S-3 |
| 5 | B-6, S-1, S-2, S-6 |
| 6 | **B-7**, B-8, B-10, all S-* |

No phase may exit on unmeasured claims. A benchmark that has not been run is a failed benchmark for gating purposes.

---

## 7. Known limitations

1. **C-PROJECT and C-TEMPORAL are self-authored.** Mitigated by pre-written held-out tasks, a second externally-sourced corpus, and blind grading — but not eliminated.
2. **LLM-judge grading is noisy.** Mitigated by two-judge agreement reporting; results near the interval are reported as ties, not wins.
3. **Single-machine measurement.** All current figures are Windows 11, one machine ([E-15 environment](research/EVIDENCE_LOG.md#measurement-environment)). Cross-platform re-measurement is required at Phase 0.
4. **LME-V2 figures are not yet reproduced.** They inform targets; they cannot be acceptance thresholds until re-run locally ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)).
5. **No benchmark measures whether users want this.** Product-market fit is not falsifiable by this program, and no amount of benchmark success substitutes for it.
