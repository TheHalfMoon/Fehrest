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
| **MemOra** *(F1-R2)* | External — memory updates, invalid/obsolete memory, forgetting | **Whether Fehrest avoids using a memory that was once true and no longer is** — the same property as C-TEMPORAL's stale-memory metric, but **externally authored**, which C-TEMPORAL by construction cannot be ([SRC-161](research/FEHREST_SOURCE_REGISTRY.md#146-memory-research-and-benchmarks)) |
| **EvoMemBench** *(F1-R2)* | External — episodic vs cross-episode, knowledge vs execution experience | Deliberate **contrary evidence**: it compares memory strategies against long-context approaches, and is included specifically to test the assumption that one strategy wins every workload ([SRC-162](research/FEHREST_SOURCE_REGISTRY.md#146-memory-research-and-benchmarks)) |

C-TEMPORAL and C-PROJECT must be **hand-built with ground truth**, because no public corpus encodes "the founder decided X on date D, reversed it on date E for reason R." They are the most valuable and most expensive artifacts in this plan, and they are prerequisites for [B-4](#b-4--temporal-and-supersession-correctness) and [B-7](#b-7--agent-continuation-the-defining-experiment).

---

## 3. Benchmarks

### 3.1 The baseline ladder

> **STRENGTHENED IN F1-R2 ([R2-10](reviews/F1-R2-RECONCILIATION.md)).** Baselines are ordered so that **each step attributes value to exactly one addition.** A benchmark whose baselines are all weak measures only that they were weak.

| # | Baseline | What beating it proves |
|---|---|---|
| 1 | **Competent plain agent** — files, `grep`/search, Git | That a memory system is needed at all. The bar that matters ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)) |
| 2 | **Strong repository-native documentation** — a well-maintained `AGENTS.md`-style state file | That structured project state must be a *system*, not a convention |
| 3 | **Raw-history stuffing** where practical | That compilation beats volume |
| 4 | **Lexical / BM25 context** | That retrieval needs more than term matching |
| 5 | **Karpathy-style maintained LLM Wiki** — raw sources + a maintained, interlinked Markdown wiki + ordinary agent search/read ([SRC-101](research/FEHREST_SOURCE_REGISTRY.md#82-andrej-karpathy--llm-wiki)) | **The strongest simple alternative.** That a *persistent maintained knowledge artifact* is not sufficient without temporal state, supersession and provenance |
| 6 | **Fehrest Core** — lexical + temporal + provenance + bounded compilation | The core thesis |
| 7 | + graph intelligence | Whether [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)'s hypothesis holds |
| 8 | + automatic memory promotion | Whether promotion earns its confirmation cost |
| 9 | + richer event experience | Whether the Event Plane's depth pays |

**Steps 1–6 are the pilot ([B-7a](#b-7a--early-headless-thesis-pilot)); 7–9 are only meaningful once step 6 shows signal.** Adding graph intelligence to a core that does not work measures nothing.

**Baseline 5 is the one F1 was missing, and it is the sharpest.** RAG repeatedly *reconstructs* understanding from raw sources on every query; an LLM Wiki instead builds a **persistent, maintained, interlinked artifact that compounds over time** — which is a far closer relative of Fehrest's thesis than any RAG variant, and is achievable with a directory of Markdown files and no system at all. Fehrest must therefore demonstrate what measurable value comes specifically from **temporal state, supersession, provenance, deterministic context compilation, the agent experience, and optionally graph intelligence** — on top of a maintained wiki, not on top of nothing. *(No claim is made that Karpathy endorses any part of Fehrest's architecture; the pattern is used as a baseline, not as an authority — see [SRC-101](research/FEHREST_SOURCE_REGISTRY.md#82-andrej-karpathy--llm-wiki).)*

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
**Fails if.** Graph expansion adds no material recall or answer-quality gain over FTS + memory → drop compiler stage [4], and — jointly with GI-BENCH's cost figures — trigger [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost), which permits **redesign or removal of Graph Intelligence from the core product hypothesis**. Or vectors beat lexical+graph materially → promote vectors to default-on ([ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) reverses).
**Method note.** Ablation is mandatory. A single "our system scores X" number cannot attribute value to any component, and attribution is the entire point.

### B-4 — Temporal and supersession correctness

**Measures.** On C-TEMPORAL: current-state accuracy at each checkpoint; historical-state accuracy ("what was true in March"); **belief-state accuracy** ("what did we believe in May"); superseded-decision retrieval; stale-memory usage rate; contradiction detection precision/recall.
**Targets.** Current-state accuracy **100%** — this is deterministic resolution, not retrieval, so anything below 100% is a bug, not a quality score. Stale-memory usage 0%.
**Decides.** [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution). Also measures structured-`payload` extraction rate.
**Fails if.** Current-state resolution is not 100% deterministic → the core value proposition fails. Or `payload` is extractable for < 30% of memories → deterministic resolution covers too little to matter ([ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) reverses to prose-first, a much weaker system).

### B-5 — Memory promotion quality

**Measures.** On a hand-labelled candidate corpus: promotion precision/recall vs human labels, for rules-only vs model-assisted. Confirmation-queue volume per active day.

**Added in F1-R2 ([R2-16](reviews/F1-R2-RECONCILIATION.md)) — type-assignment precision, as a safety metric:**

| Metric | Why it is a safety metric, not a quality metric |
|---|---|
| Overall type-assignment precision vs human labels | Ordinary quality |
| **Rate at which confirmation-required memories (`decision`, `constraint`, `preference`) were classified into an auto-promote type** | Each occurrence is a memory that acquired steering authority over every future agent **without a human ever seeing it**. This is [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) reached by misclassification rather than by attack |
| Rate at which unclassified prose was auto-typed with AI off | Must be **zero** by construction ([F §5.1](05-MEMORY-MODEL.md#51-which-stages-are-deterministic)); a non-zero result means the safe default is not implemented |

**Decides.** [H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value) — whether `AI OFF` is a real mode — and whether auto-promotion may be widened.
**Fails if.** Rules-only recall < 60% of model-assisted → `AI OFF` degrades to a read-only knowledge base, a thesis-level weakening requiring founder sign-off ([Q-4](16-OPEN-QUESTIONS.md)). Or unclassified prose is auto-typed with AI off → a correctness defect, not a tuning issue. Or confirmation volume exceeds what dogfooding shows users actually service → users approve blindly and the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) control becomes theatre. **The tolerable confirmation rate is measured here, not assumed** ([R2-06](reviews/F1-R2-RECONCILIATION.md)); the former "> 5/day" figure was an assumption presented as a threshold.

### B-6 — Context compiler

**Measures.** Compile latency p50/p95 by corpus size; tokens produced vs budget; **compression ratio vs raw history**; determinism (identical digest over 100 runs on unchanged state); provenance completeness (unsourced items must be 0); omission honesty (does `omitted` match reality?); **manifest completeness and per-item storage cost** ([R2-01](reviews/F1-R2-RECONCILIATION.md)); **replay-outcome correctness** across deliberately induced `IDENTICAL` / `DIVERGED` / `UNRECONSTRUCTABLE` cases ([H §3.3](07-CONTEXT-COMPILER-SPEC.md#33-replay-outcomes-are-explicit--three-results-never-two)).
**Targets.** Latency per [O](14-PERFORMANCE-BUDGETS.md); compression ≥ 20×; determinism 100%; unsourced items 0; **manifest covers 100% of emitted items, and a divergent replay is never reported as `IDENTICAL`**.
**Decides.** [H](07-CONTEXT-COMPILER-SPEC.md) viability.
**Fails if.** Digests vary on unchanged input → replay and audit impossible, [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) fails. Or p95 exceeds budget by 2× → pre-computation becomes mandatory.

### B-7 — Agent continuation: the defining experiment

**This is the benchmark that decides whether Fehrest should exist.**

> **RESTRUCTURED IN F1-R2 ([R2-10](reviews/F1-R2-RECONCILIATION.md)) into two stages: an early pilot and a confirmatory powered study.**
>
> Two defects in the F1 design are corrected. First, **the experiment that decides whether the product should exist ran at Phase 6**, after the desktop-adjacent architecture, the sidecar, the compiler and the full memory model were built — spending the entire budget before testing the premise. Second, **its thresholds had no statistical design**: `+10 percentage points` with "the 95% interval excluding zero" specifies an effect and a confidence level but never a sample size, a design, or a power target, so the study could be run, fail to reach significance, and produce no interpretable answer at all.
>
> **What was NOT accepted:** the review's proposed `n ≈ 300+` is **rejected as a universal requirement**. Required n is a *derived* quantity, not a constant: it depends on paired-vs-independent design, baseline rate, discordance rate on paired items, the minimum meaningful effect, α, power, and which endpoint is primary. Freezing a guessed n would replace one unjustified number with another. **The sample size is calculated, and the calculation is pre-registered.**

#### B-7a — Early headless thesis pilot

**When.** [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) — the first authorized implementation, before the sidecar, the editor, the desktop shell, automatic promotion, or any production integration.

**Purpose.** Detect whether the **simplest possible Fehrest mechanism** contains meaningful signal, at the cheapest point at which that question can be asked. Nothing more.

**Arms.** The pilot runs the progressively-stronger baseline ladder in §3.1 up to and including *Fehrest Core (lexical + temporal + provenance + bounded compilation)*. No graph, no vectors, no automatic promotion.

**Permitted conclusions — and this constraint is the point:**

| Result | Permitted conclusion |
|---|---|
| Clear positive signal | Proceed to the production architecture; the confirmatory study is worth its cost |
| Clear negative signal on a well-powered contrast | Reconsider before building the expensive architecture |
| Anything else | **`INCONCLUSIVE`** |

**An underpowered pilot may report `INCONCLUSIVE`. It may NOT falsify the product thesis.** [F-1](17-FAILURE-CONDITIONS.md#f-1--compiled-context-does-not-beat-a-competent-agent-with-plain-file-tools) is fired only by B-7b. A pilot sized to detect signal cheaply is, by construction, badly sized to prove absence — and treating "we did not detect it" as "it is not there" is the same absence-of-signal error that produced two of F1's three retracted findings ([R1 verdict](VERDICT.md)).

#### B-7b — Confirmatory powered benchmark

**When.** Phase 6, as before.

**Pre-registered before any data is collected, and committed in-repo:**

| Element | Requirement |
|---|---|
| **Primary metric** | Exactly one, named in advance. Everything else is secondary and reported as such |
| **Minimum meaningful effect** | Justified against [E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)'s 3.2-point published margin, not chosen for beatability |
| **Design** | **Paired wherever possible** — the same task attempted by each arm — which is both more powerful and the reason the required n cannot be quoted from an unpaired formula |
| **α, power** | Stated in advance |
| **Sample-size calculation** | **Derived from the four rows above**, with the calculation itself recorded. Not a round number |
| **Multiple-comparison handling** | Stated in advance, because the arm list is long |
| **Held-out corpus policy** | Which tasks are held out, when they were written, and who saw them |
| **Blind grading policy** | Graders blind to arm; two-judge agreement reported |

**Only B-7b may fire a definitive product-thesis falsification.**

**Setup.** On C-PROJECT: Agent A works the project across many sessions, then is destroyed. Agent B must continue correctly on a held-out task set.

**What Agent B receives — and does not ([R1-18](reviews/F1-R1-RECONCILIATION.md)):**

| Denied | Provided |
|---|---|
| ❌ Agent A's private chain-of-thought | ✅ The normal project files |
| ❌ Agent A's hidden internal state | ✅ Normal filesystem/search tools |
| ❌ Any raw conversation dump | ✅ **Fehrest-compiled context** |

This asymmetry is the whole experiment. Agent B has exactly what a real successor agent would have — the repository and its tools — **plus** Fehrest. The measured quantity is what Fehrest adds on top of a competent agent, not what it adds on top of nothing.

**Arms — two Fehrest arms, not one ([R2-03](reviews/F1-R2-RECONCILIATION.md)).**

| Arm | Receives |
|---|---|
| **Fehrest — compiled-context-only** | Compiled context package only. Isolates the compiler |
| **Fehrest — as shipped** | Compiled context **plus the normal permitted agent tools** (`search.query`, `object.read`, `memory.retrieve`, `graph.query`) |
| Raw stuffing | As much chat history as fits the budget |
| BM25 | Top-k passages |
| Dense RAG | Top-k passages |
| Hybrid RAG | RRF of both |
| Graph-only | Graph traversal results |
| Mem0 | Its own memory |
| **Plain agent** | **File tools, no memory system — the real bar** |
| No context | Floor |

**Why the second Fehrest arm is mandatory.** F1 measured only the compiled-context-only configuration — a configuration **no user will ever run**. Fehrest ships an agent gateway whose tool surface is the point of the product ([G §3](06-AGENT-MODEL.md#3-tools)); an agent connected to Fehrest will search, read objects, and query memory directly. Measuring only the package measures a component, and then reports the result as though it were the product. The compiled-context-only arm is retained because it attributes value to the compiler specifically; **the as-shipped arm is the one that answers whether the product works.**

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

**+10 points is the *effect*, not the *design*.** It is an input to the power analysis above, not a substitute for one. The sample size required to detect it at the stated α and power is calculated and pre-registered; the threshold is meaningless without it, because a study too small to detect a 10-point effect cannot fail to reach it in any informative way.

**Fails if.** Any threshold is missed **in B-7b** → **the product thesis is falsified.** Not a tuning problem. The correct response is to reconsider the product, not to lower the threshold. A B-7a pilot missing a threshold is `INCONCLUSIVE` and falsifies nothing.

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

**Fails if.** Any cell exceeds 3× its linear projection → the extractor is superlinear in that regime; scope or partition the graph, or evaluate alternatives.

**Relationship to the capability question.** A cost result alone speaks to the *implementation*. GI-BENCH's cost figures combine with [B-3](#b-3--retrieval-quality-by-stage)'s benefit figures to answer [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost): if the measured benefit does not justify the measured cost across configurations and corpus types, Fehrest **must permit redesign or removal of Graph Intelligence from the core product hypothesis**.

**Gate.** No packaging, bundling or runtime decision may be finalised before GI-BENCH reports.

### B-10 — Scale and growth

**Measures.** Behaviour at C-LARGE and with 10 years of simulated events: cold start, search latency, compile latency, memory footprint, index size, compaction effectiveness.
**Input caveat ([R2-12](reviews/F1-R2-RECONCILIATION.md)).** The former "~500K events, ~180K memories" figures derived from the **unvalidated** 500 events/day and 50 memories/day assumptions. The simulated volumes are set from the [B-0](#b-0--event-volume-measurement) measurement, not from those numbers. Running B-10 against an invented volume measures an invented system.
**Fails if.** Cold start exceeds 10 s at 100K files, or memory growth is superlinear.

### B-0 — Event volume measurement

> **ADDED IN F1-R2 ([R2-12](reviews/F1-R2-RECONCILIATION.md)).** Numbered `B-0` because it runs at Phase 0 and because several other benchmarks take their inputs from it.

**Status of the current numbers.** The planning package's 500 events/day and 50 memories/day are **UNVALIDATED PLANNING ASSUMPTIONS**, and are labelled as such everywhere they appear ([O §9](14-PERFORMANCE-BUDGETS.md#9-growth-over-time), [F §8](05-MEMORY-MODEL.md#8-growth-and-forgetting), [D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)).

**What was NOT accepted.** The review asserted realistic volume is `10K–100K events/day`. That figure is **not adopted as fact** — it is an unverified estimate, offered without measurement, and replacing an ungrounded number with another ungrounded number two orders of magnitude larger would change which decisions are wrong without making any of them right. Both numbers are treated as unvalidated; the measurement decides.

**Measures.** Capture or reconstruct representative **real multi-agent usage** — the founder's own sessions across several agents, plus reconstructed traces from existing agent transcripts — and count **potential events by class**: object mutations, agent steps, tool calls and results, model requests/responses, memory candidates and promotions, context compilations and their served-item counts, approval pairs.

**Decides.**
- Which event types deserve canonical retention at all.
- Whether the T1/T2 split is necessary, and where the line falls ([D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)).
- Retention window and compaction policy.
- Disk budget ([O §8](14-PERFORMANCE-BUDGETS.md#8-disk)).
- Checkpoint cadence and the degraded-recovery budget ([E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints)).
- The per-item cost ceiling for the served-item manifest ([H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1)).

**Gate.** **No event-tiering, retention, compaction or checkpoint-cadence parameter may be frozen before B-0 reports.**

### B-12 — FTS5 rebuild and ranking stability

> **ADDED IN F1-R2 ([R2-14](reviews/F1-R2-RECONCILIATION.md)).** Raw FTS5 ranking determinism was treated as an assumption. It is now an empirical requirement, tested early, because a load-bearing deterministic digest sits on top of it.

**Setup.** Construct one logical corpus **A** by two different routes:

| Route | How A is reached |
|---|---|
| **Incremental** | Heavy mutation history — interleaved `insert`, `update`, `delete`, `replace`, rename, and re-insert — arriving at exactly corpus A |
| **Fresh** | A single clean build from corpus A's final state |

**Compare, between the two indexes:**

- candidate membership for a fixed query set
- ranking order
- raw scores
- resulting context selection
- **the context package's served-item manifest and package digest**

**Configuration.** At minimum the currently proposed FTS5 schema — `fts5(title, body, tokenize='unicode61 remove_diacritics 2', content='', contentless_delete=1)` ([E §4](04-DERIVED-DATA-MODEL.md#4-sqlite-as-the-derived-store)). `contentless_delete` is specifically exercised, since contentless tables with deletes are where divergence is most plausible.

**Decides.** Whether [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)'s equivalence test and [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)'s digest may rest on FTS5 ranking as-is.

**Fails if.** Membership, order, or the package digest differs between routes.

**Remedy is NOT chosen here.** If drift is measured, candidates include: a different FTS5 table configuration; using FTS purely for **candidate generation** with a deterministic Fehrest-owned rerank over stable keys; or another minimal measured approach. **Benchmark it, then decide** — picking a remedy in R2 for a defect not yet measured would be the same unearned confidence this package exists to avoid.

**When.** Phase 2, at the first derived byte — before the compiler depends on the digest, not after.

### B-13 — GI-CAP — Graph Intelligence capability experiment

> **ADDED IN F1-R2 ([R2-15](reviews/F1-R2-RECONCILIATION.md)).** [GI-BENCH](#b-11--gi-bench--graph-intelligence-benchmark-matrix) measures the **cost** of a graph implementation. [B-3](#b-3--retrieval-quality-by-stage) measures retrieval **quality** — but only once the sidecar, IPC, packaging, Python lifecycle and incremental pipeline exist. That ordering builds the entire integration **before** asking whether the capability helps, which means [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)'s "remove it" branch would fire only after its cost had already been paid.

**GI-CAP runs first, and is deliberately throwaway.** A static, one-shot, offline graph — extracted by hand-run tooling into a flat artifact — with **no** supervisor, **no** IPC, **no** packaging, **no** Python lifecycle management, **no** incremental pipeline, and **no** graph explorer. None of that is needed to answer the question.

**Compare, at minimum:**

| Configuration |
|---|
| FTS + structured + temporal memory |
| FTS + structured + temporal memory **+ static graph expansion** |

**On both corpus types, because they exercise different extractor paths and the [v1 wedge](00-PRODUCT-THESIS.md#4-the-v1-user-wedge) has users with both:**

- a **code-heavy** corpus
- a **Markdown/knowledge-heavy** corpus

**Measure.** Retrieval quality (recall@k, nDCG@10, MRR) and — where feasible at this stage — continuation outcome on the [B-7a](#b-7a--early-headless-thesis-pilot) task set.

**Decides.** Whether production Graphify integration is worth starting at all.

**Gate.** **No production graph integration work begins before GI-CAP reports.** If the capability does not materially improve outcomes at acceptable cost, v1 must be able to remove it *before* the integration exists — which is only possible if this experiment precedes it.

**Status is unchanged by this reordering:** Graph Intelligence remains a `CORE CURRENT PRODUCT HYPOTHESIS` that is `EXPLICITLY FALSIFIABLE`, and Graphify remains an `OPTIONAL IMPLEMENTATION CANDIDATE`. GI-CAP is what makes the falsifiability affordable.

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
| **S-8** Served-item provenance ([R2-02](reviews/F1-R2-RECONCILIATION.md)) | An evidence claim naming an object **in-grant but not in the served-item manifest** is never accepted as observed by that session |
| **S-9** Unlabelled content path ([R2-03](reviews/F1-R2-RECONCILIATION.md)) | **Zero** agent-facing read paths return content outside the core envelope |

---

## 5. Harness requirements

Committed in-repo under `bench/`. Requirements: one command runs a suite; pinned model, seed and tokenizer per run; hardware and OS recorded automatically; results as structured data plus a report; **confidence intervals mandatory**; every baseline runnable under identical conditions; blind grading with a second-judge agreement check (the donor reports 90.6% agreement, κ 0.81 — a reasonable target).

**Cost-aware evaluation — added in F1-R2 ([SRC-163](research/FEHREST_SOURCE_REGISTRY.md#146-memory-research-and-benchmarks)).** Accuracy alone is not a fair comparison between memory systems, because the expensive way to be right is always available. Every arm therefore records, where practical:

| Recorded per run | Why |
|---|---|
| Task correctness | The primary metric |
| **Context tokens consumed** | Already a B-7 threshold; now recorded for every arm, not just the stuffing baseline |
| **Latency** | Co-equal with accuracy per [E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target) |
| **CPU time** | A system that wins by burning the machine has not won on a laptop |
| **Disk growth** | Directly relevant to [B-0](#b-0--event-volume-measurement) and the [O §8](14-PERFORMANCE-BUDGETS.md#8-disk) budgets |
| **Number of model calls** | The clearest proxy for hidden cost, and invisible in an accuracy score |
| **Monetary provider cost** | Where an arm uses a paid provider at all |

This matters most for the arms Fehrest is trying to beat: raw-history stuffing can buy correctness with tokens, and an agentic baseline can buy it with model calls. A comparison that records only the score rewards exactly that.

Two rules that prevent the harness from lying:
- **A run that cannot record its full configuration is invalid**, not "approximately right."
- **Baselines and Fehrest share one code path** for prompting, budgeting and grading. Adapters, not separate scripts — otherwise the comparison measures harness quality, not system quality.
- **Benchmark conclusions are never copied without checking methodology.** [E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks) is the worked example: a 76% vs 76% "result" at n=50 whose 95% interval is roughly ±12 points distinguishes nothing. Upstream claims from any external memory system enter this package labelled `UPSTREAM_CLAIM` until reproduced locally.

---

## 6. Gating

| Phase | Must pass before exit |
|---|---|
| 0 | **B-0** (event volume) |
| **T** | **B-7a** reports a verdict (positive · negative · `INCONCLUSIVE`), B-9, B-12 |
| 1 | B-9 |
| 2 | B-1, B-2, B-9, **B-12** |
| 3 | **B-13 (GI-CAP) before any integration work**, then B-3, B-9, B-11 |
| 4 | B-4, B-5, S-3 |
| 5 | B-6, S-1, S-2, S-6 |
| 6 | **B-7b**, B-8, B-10, all S-* |

No phase may exit on unmeasured claims. A benchmark that has not been run is a failed benchmark for gating purposes.

**Two gates are ordering constraints rather than pass/fail thresholds ([R2-10](reviews/F1-R2-RECONCILIATION.md), [R2-15](reviews/F1-R2-RECONCILIATION.md)):** B-7a must *report* before the production architecture is built — a verdict of `INCONCLUSIVE` still satisfies the gate, because the gate exists to force the question to be asked early, not to force a particular answer. B-13 must report before graph integration begins, for the same reason.

---

## 7. Known limitations

0. **The confirmatory study's sample size does not exist yet** ([R2-10](reviews/F1-R2-RECONCILIATION.md)). It is derived from a pre-registered power analysis at Phase 6, not quoted here. Any figure a reader carries away from this document as "the required n" is one this plan did not state.
1. **C-PROJECT and C-TEMPORAL are self-authored.** Mitigated by pre-written held-out tasks, a second externally-sourced corpus, and blind grading — but not eliminated.
2. **LLM-judge grading is noisy.** Mitigated by two-judge agreement reporting; results near the interval are reported as ties, not wins.
3. **Single-machine measurement.** All current figures are Windows 11, one machine ([E-15 environment](research/EVIDENCE_LOG.md#measurement-environment)). Cross-platform re-measurement is required at Phase 0.
4. **LME-V2 figures are not yet reproduced.** They inform targets; they cannot be acceptance thresholds until re-run locally ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)).
5. **No benchmark measures whether users want this.** Product-market fit is not falsifiable by this program, and no amount of benchmark success substitutes for it.
