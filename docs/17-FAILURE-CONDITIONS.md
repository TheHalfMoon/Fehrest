# Architectural Failure Conditions

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

What findings would force redesign, donor replacement, or postponement. A plan without these is unfalsifiable, and an unfalsifiable plan cannot be reviewed — only believed.

Each condition names the trigger, the detecting benchmark, the consequence, and the documents invalidated.

---

## 1. Thesis-level failures

### F-1 — Compiled context does not beat a competent agent with plain file tools

> **STAGED IN F1-R2 ([R2-10](reviews/F1-R2-RECONCILIATION.md)).** F1 detected this only at Phase 6 — after the sidecar, the compiler, the full memory model and the agent gateway were built. The condition now has an **early indicator** and a **definitive trigger**, and only the second may fire it.

**Trigger — definitive.** [B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark), the **pre-registered, powered** confirmatory study: the Fehrest arms do not beat the plain-agent arm by the pre-registered margin at the pre-registered power. **Only B-7b may fire this condition.**

**Early indicator — may NOT fire it.** [B-7a](10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) at [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice). A pilot sized to detect signal cheaply is, by construction, badly sized to prove absence. Its permitted verdicts are `SIGNAL`, `NO SIGNAL` and **`INCONCLUSIVE`**, and an underpowered `NO SIGNAL` is a reason to **stop and reconsider before building the expensive architecture** — not a falsification of the thesis. **Treating "we did not detect it" as "it is not there" is the absence-of-signal error that produced two of F1's three retracted findings** ([VERDICT](VERDICT.md)); it must not be re-committed against the product's own thesis.

**Second bar added in F1-R2.** Fehrest must also beat the **maintained Karpathy-style LLM Wiki baseline** ([§3.1 ladder](10-BENCHMARK-PLAN.md#31-the-baseline-ladder)) — raw sources plus a maintained, interlinked Markdown wiki plus ordinary agent search. That is the strongest *simple* alternative, achievable with a directory of files and no system, and it is a closer relative of Fehrest's thesis than any RAG variant. Beating a plain agent while tying a maintained wiki would mean the value is in *having a maintained artifact*, not in temporal state, supersession, provenance or deterministic compilation — a materially different and much smaller product.

**Consequence.** **REDESIGN or ABANDON.** Not a tuning problem. The product exists to make a fresh agent continue work correctly from compiled memory; if an agent with `grep` does as well, the entire memory apparatus is unjustified complexity.
**Invalidates.** [A](00-PRODUCT-THESIS.md), [H](07-CONTEXT-COMPILER-SPEC.md), [F](05-MEMORY-MODEL.md), and the rationale for [Phase 7+](15-IMPLEMENTATION-PHASES.md).
**Detected at.** Indicated at **Phase T**, decided at Phase 6 — deliberately before any UI investment, and now with a cheap early warning before most of the architecture is built.
**Honest note.** This is the condition I consider most likely to fire, because LongMemEval-V2's own reporting shows the best memory system beating an off-the-shelf coding agent by only 3.2 points ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). The margin is genuinely thin.

### F-2 — Deterministic current-state resolution is unachievable
**Trigger.** [B-4](10-BENCHMARK-PLAN.md): current-state accuracy below 100% on C-TEMPORAL, or resolution proves non-deterministic on real conflicts.
**Consequence.** **REDESIGN of the memory model.** The differentiator versus RAG is answering "what is true now" deterministically. Falling back to LLM-adjudicated conflicts would violate [R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) and make Fehrest a slower RAG.
**Invalidates.** [F](05-MEMORY-MODEL.md), [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution), parts of [H](07-CONTEXT-COMPILER-SPEC.md).
**Detected at.** Phase 4.

---

## 2. Donor replacement

### F-3 — Graph Intelligence does not deliver material benefit at acceptable cost

> **AMENDED PRE-G2 (governance correction 2).** The F1-R1 revision of this condition stated that the capability "may be REPLACED, never DROPPED." That made a core product claim **unfalsifiable**, which is exactly what this document exists to prevent. Removal is now explicitly permitted on evidence.

**Status of the claim under test:**

```
GRAPH INTELLIGENCE:
CORE CURRENT PRODUCT HYPOTHESIS
EXPLICITLY FALSIFIABLE
```

Graph Intelligence is a **current product hypothesis**, not an axiom. The hypothesis: answering *"what is connected?"* materially improves agent continuation over simpler local retrieval, at acceptable cost.

**The governing failure condition:**

> **If controlled continuation/retrieval benchmarks show that graph-assisted understanding does not provide a material benefit over simpler local retrieval approaches at acceptable cost, Fehrest MUST permit redesign or removal of Graph Intelligence from the core product hypothesis.**

**Trigger.** **[GI-CAP (B-13)](10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) shows static graph expansion adds no material gain over FTS + structured + temporal memory on either corpus type** — the earliest and cheapest trigger, added in F1-R2 ([R2-15](reviews/F1-R2-RECONCILIATION.md)); **or** [B-3](10-BENCHMARK-PLAN.md) ablation shows graph expansion adds no material recall or answer-quality gain over FTS + memory; **or** [B-7](10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment) shows no material continuation gain attributable to graph-assisted understanding; **or** [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) shows the cost (latency, memory, packaging, rebuild time) is unacceptable for the benefit measured; **or** [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is falsified and parser fuzzing yields escapes.

**Why GI-CAP matters more than its size suggests.** Under F1's ordering, this condition's "remove the capability" branch could only fire *after* the sidecar, IPC, packaging, Python lifecycle and incremental pipeline had been built — so exercising the falsifiability meant discarding work already paid for. **A falsification condition that is expensive to act on is one that gets deflected**, whatever the document says. GI-CAP makes removal cheap while it is still possible.

**Consequence, graduated by what the evidence actually shows:**

| Finding | Permitted response |
|---|---|
| A specific **implementation** underperforms | Replace the extractor; reconsider runtime shape ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)) |
| A specific **retrieval configuration** underperforms | Re-examine expansion depth, seeding and ranking; retest |
| The **capability** shows no material benefit at acceptable cost across configurations and corpus types | **REDESIGN or REMOVE Graph Intelligence from the core product hypothesis.** Revise [A §5](00-PRODUCT-THESIS.md#5-the-four-layer-architecture), this condition, and the affected ADRs |
| Cost is unacceptable but benefit is real | Redesign for cost: scope, partition, or restrict to corpus types where it pays |
| Sandbox escape | **Halt graph work**; require per-parser WASM isolation ([SRC-043](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)) before resuming |

**Evidential discipline — what still may not be concluded carelessly.** Removal must follow from evidence about the *capability*, not from a single pairing. One implementation underperforming one retrieval configuration on one corpus type is evidence about that pairing. The row above requires "across configurations and corpus types" precisely so that a weak result cannot be used to delete a capability prematurely — and equally, so that a genuinely negative result cannot be deflected indefinitely as "we configured it wrong."

**If removal is chosen**, the following must be revised together, and the product thesis restated honestly: [A §5](00-PRODUCT-THESIS.md#5-the-four-layer-architecture) (four-layer architecture), [E §5](04-DERIVED-DATA-MODEL.md#5-graph-intelligence-capability-vs-implementation), [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape), [SRC-001](research/FEHREST_SOURCE_REGISTRY.md#21-graphify), graph rows in [O](14-PERFORMANCE-BUDGETS.md), and the [v1 wedge](00-PRODUCT-THESIS.md#4-the-v1-user-wedge) consequence that keeps the graph in v1.

**Detected at.** Phase 3 (B-3 ablation, GI-BENCH), Phase 6 (B-7 continuation), continuous (fuzzing).

**Structural protection.** The capability sits behind a wire contract and a rebuildable ID mapping ([E §5.3](04-DERIVED-DATA-MODEL.md#53-id-mapping-is-the-critical-seam)), so both replacement *and removal* touch no canonical record. Nothing in the canonical data model depends on the graph existing.

### F-4 — No editor candidate clears the fidelity floor

> **REWRITTEN IN F1-R1 ([R1-02](reviews/F1-R1-RECONCILIATION.md)).** F1's F-4 assumed CodeMirror 6 had been chosen and asked what would unseat it. With the editor decision reopened, the real failure condition is that the [Editor Gate](18-EDITOR-GATE.md) produces no winner.

**Trigger.** Phase 3E: no candidate satisfies the round-trip proof obligation — P-1 (fidelity), P-2 (no silent loss), P-5 (canonical sufficiency), P-6 (sidecar boundedness) — **or** every candidate triggers an elimination condition (silent data loss, content loss on crash, sidecar carrying document content).

**Consequence.** **SCOPE DECISION, not a default pick.** Picking a winner on aggregate score when none cleared the floor would ship a canonical format that silently loses user data. Permitted responses:
1. Narrow the required feature set until a candidate clears the floor (e.g. accept no rich blocks in v1).
2. Amend [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) to make a documented sidecar canonical — explicitly, with a specification and lossless exporter, plus a major migration ([M §9](12-MIGRATION-SCHEMA-EVOLUTION.md#9-anticipated-migrations)).
3. Evaluate Candidate C (ProseMirror/Tiptap/Milkdown) against the specific gap.

**Forbidden.** Shipping a candidate that fails P-2 or the crash test, whatever it scores.

**Invalidates.** [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated) resolution; [Phase 7](15-IMPLEMENTATION-PHASES.md#phase-7--desktop-application) entry criteria.
**Detected at.** Phase 3E.

### F-5 — Candidate B proves unextractable from AFFiNE

**Trigger.** The maintained `AFFiNE/blocksuite/…` subtree cannot be vendored at acceptable cost: coupling to AFFiNE-specific infrastructure is too deep, per-file license provenance cannot be established (MIT applies only outside `packages/backend` and `packages/common/native`), or the dependency surface is unacceptable.

**Consequence.** Candidate B is eliminated **on packaging grounds**, and the gate proceeds with A and possibly C. This is a legitimate, evidence-based elimination — distinct from F1's erroneous elimination on *maintenance* grounds, which the evidence refuted ([E-10.1](research/EVIDENCE_LOG.md#e-101--the-evidence-f1-missed-the-affine-subtree-is-active)).

**Note for reviewers.** F1 eliminated BlockSuite for the wrong reason. If it is eliminated again, the reason must be recorded precisely, because "we tried and it did not work" and "we assumed it was dead" produce the same outcome with very different evidential weight.
**Detected at.** Phase 3E, during Candidate B setup.

---

## 3. Storage and event model

### F-6 — Derived state is not genuinely rebuildable
**Trigger.** [B-9](10-BENCHMARK-PLAN.md) `nuke-and-rebuild` produces divergent query results.
**Consequence.** **STORAGE MODEL REDESIGN.** This is the most load-bearing invariant in the plan. If it fails: index corruption becomes a *data-loss* incident rather than an availability one ([T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes)); `synchronous=NORMAL` becomes unsafe ([ADR-0006](09-TECHNOLOGY-DECISIONS.md#adr-0006--sqlite-is-the-derived-store-and-only-the-derived-store)); "delete derived state" stops being a support instruction ([N §3.6–3.7](13-RECOVERY-MODEL.md#36-corrupt-sqlite-derived)); and every index decision becomes irreversible.
**Invalidates.** [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) and, through it, [E](04-DERIVED-DATA-MODEL.md), [ADR-0006](09-TECHNOLOGY-DECISIONS.md#adr-0006--sqlite-is-the-derived-store-and-only-the-derived-store), [M §1 rule 4](12-MIGRATION-SCHEMA-EVOLUTION.md#1-governing-rules), and security arguments in [C](02-THREAT-MODEL.md).
**Detected at.** Phase 2, then continuously in CI. Testing it from the first derived byte is what prevents this from being discovered late.

### F-7 — JSONL event log misses durability or size budgets
**Trigger.** [B-10](10-BENCHMARK-PLAN.md): log exceeds ~1 GB/year at C-LARGE with unacceptable append or verification latency.
**Consequence.** **EVENT MODEL CHANGE** — replace JSONL with a specified append-only binary format. [I-5-as-amended](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) already permits this given a published spec and a lossless exporter, which is precisely why that amendment was made. Major migration ([M](12-MIGRATION-SCHEMA-EVOLUTION.md)).
**Invalidates.** [ADR-0001](09-TECHNOLOGY-DECISIONS.md#adr-0001--canonical-state-is-open-files-plus-an-append-only-event-log) partially; [D §5.3](03-CANONICAL-DATA-MODEL.md#53-event-record).
**Detected at.** Phase 6.

### F-8 — Event tiering is wrong
**Trigger.** T2 compaction loses information later needed for audit or replay; or T1 alone is insufficient to reconstruct agent-visible state ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) fails).
**Consequence.** Promote events from T2 to T1 and accept the growth, or redesign compaction. Since compaction retains digests of removed segments, the *detection* is reliable even though the data is gone.
**Detected at.** Phase 5–6.

---

## 4. Security

### F-9 — The instruction/knowledge boundary is not structural
**Trigger.** C-INJECT ([L §6.1](11-SECURITY-VERIFICATION-PLAN.md#61-c-inject--prompt-injection)) shows retrieved content changing a capability grant, adding a tool, or causing an unapproved side effect.
**Consequence.** **HALT.** No release. [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority) is thesis-critical; a memory OS that lets a poisoned document escalate privilege is worse than no memory OS, because it concentrates and then leaks a decade of private knowledge.
**Invalidates.** [C §1](02-THREAT-MODEL.md#1-governing-principle), [G](06-AGENT-MODEL.md).
**Detected at.** Phase 5.

### F-10 — Scope isolation fails through graph expansion
**Trigger.** [S-6](10-BENCHMARK-PLAN.md): cross-project leakage on entangled projects.
**Consequence.** Scope filtering is in the wrong layer. Either move it deeper into traversal or partition the graph by scope — the latter costs cross-project retrieval entirely, a real product loss.
**Detected at.** Phase 5.

### F-11 — Sidecar confinement is insufficient
**Trigger.** [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) falsified — fuzzing yields host code execution or egress from vault content.
**Consequence.** Per-parser WASM isolation becomes mandatory before shipping the graph, **or** the graph is dropped ([F-3](#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)).
**Detected at.** Phase 3 onward, continuously.

### F-12 — Event-log tamper-evidence is defeatable
**Trigger.** C-TAMPER shows an undetectable modification.
**Consequence.** **Withdraw the claim** rather than weaken the test. Provenance guarantees ([I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance), [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)) would need restating as best-effort. Documenting a weaker guarantee honestly is acceptable; shipping a claim known to be false is not.

---

## 5. Feature postponement

### F-13 — Collaboration stays postponed
**Trigger.** No demonstrated multi-writer need; or the CRDT↔canonical-file relationship remains unsolved.
**Consequence.** Collaboration stays out. [ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent) holds. The hard part was never adding Yjs — it is defining how CRDT state relates to canonical files without inverting [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended).

### F-14 — Semantic vectors stay postponed
**Trigger.** [B-3](10-BENCHMARK-PLAN.md) shows no material gain over lexical + graph; **or** no stable sqlite-vec release exists ([E-12](research/EVIDENCE_LOG.md#e-12--vector-store-maturity): current line is `v0.1.10-alpha.*`).
**Consequence.** Vectors stay D3-optional. [ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) holds. **This is the expected outcome, not a failure** — it is listed here so that the opposite finding (vectors clearly winning) is also treated as a documented trigger to change the default.

### F-15 — `AI OFF` proves too weak to be a product
**Trigger.** [B-5](10-BENCHMARK-PLAN.md): rules-only promotion recall below 60% of model-assisted ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)).
**Consequence.** Not an architecture failure — a **positioning** failure. Fehrest becomes "a memory OS that works best with a model," with `AI OFF` as a genuine but thinner fallback. Requires a founder decision ([Q-4](16-OPEN-QUESTIONS.md)) and honest marketing, since [I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) would still hold technically while being misleading in spirit.

---

## 6. Performance

### F-16 — Interactive budgets unreachable
**Trigger.** D1 incremental > 1 s p95 at C-MED, or context compilation > 2× budget.
**Consequence.** Indexing redesign, or mandatory pre-computation and caching for the compiler — which threatens determinism ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)) and would need its own ADR.

### F-17 — Confirmation fatigue
**Trigger.** Sustained confirmation volume above the rate dogfooding shows users actually service ([O §10](14-PERFORMANCE-BUDGETS.md#10-human-factor-budgets)).
**Consequence.** Users approve blindly and the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) control becomes theatre. Retune promotion rules — **the rules are wrong, not the user.** Listed as a failure condition because the usual industry response is to blame the operator and keep the alerts.
**Note ([R2-06](reviews/F1-R2-RECONCILIATION.md)).** The former "> 5/day" trigger was an **assumption about human behaviour made without observing any human**, and it had been cited across three documents as though it were a measured tolerance. Both the tolerable rate and the produced rate are measured before this condition can fire.

---

## 4A. Conditions added in F1-R2

### F-18 — FTS5 ranking is not stable across rebuild histories
**Trigger.** [B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability): an index reached by heavy incremental mutation differs from one built fresh from the identical corpus — in candidate membership, ranking, or the resulting context package digest.
**Consequence.** The deterministic context digest cannot rest on engine-internal ranking. Remedies — a different FTS5 configuration, FTS as candidate generation only with a deterministic Fehrest-owned rerank, or another minimal approach — are **chosen on the measurement, not now**.
**Invalidates.** Parts of [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)'s equivalence test and [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)'s digest as currently specified.
**Detected at.** Phase T / Phase 2 — deliberately before the digest is depended upon.

### F-19 — Incremental maintenance does not converge to a rebuild
**Trigger.** `test_incremental_equals_full` ([E §10](04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data)) diverges outside documented tolerances, or `test_invalidation_completeness` finds artifacts that should have been invalidated and were not.
**Consequence.** **Incremental maintenance is unsound.** Either fix invalidation, or make full rebuild the only correct path — which would make [E §6](04-DERIVED-DATA-MODEL.md#6-incremental-maintenance) untenable at the measured rebuild cost and force a redesign. **Relaxing the test is not a permitted response**; a stale index that looks like a fresh one is the [T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes) suppression failure arrived at by accident.
**Detected at.** Phase 2, then continuously.

### F-20 — The four-axis memory model produces unusable abstention rates
**Trigger.** Removing uncalibrated confidence from resolution ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)) yields `CONTRADICTION` so often that agents cannot act.
**Consequence.** Add **evidence-based** rungs to the ladder, or accept a higher abstention rate as the honest answer. **Restoring uncalibrated model confidence as truth authority is forbidden** — that is the defect [R2-04](reviews/F1-R2-RECONCILIATION.md) removed, and a high abstention rate is a symptom of thin evidence, not an argument for inventing some.
**Detected at.** Phase 4 ([B-4](10-BENCHMARK-PLAN.md#b-4--temporal-and-supersession-correctness)).

### F-21 — Cloud-sync environments prove incompatible
**Trigger.** The [N §3A](13-RECOVERY-MODEL.md#3a-hostile-filesystem-and-sync-environments) suite fails against real OneDrive on Windows or real iCloud Drive on macOS — canonical loss, undetected identity splits, or placeholder files indexed as empty.
**Consequence.** **The environment is reported as unsupported rather than silently broken**, and the vault refuses or warns on that location. Since the founder's own environment is a synced Windows folder, an unresolvable failure here is a *product* problem, not a compatibility footnote.
**Detected at.** Phase 2 onward, on real clients.

### F-22 — The served-item manifest is unaffordable
**Trigger.** [B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) and [B-6](10-BENCHMARK-PLAN.md#b-6--context-compiler) together show per-item manifest cost dominating canonical storage at realistic volume.
**Consequence.** Reduce **what is recorded per item**; never what is recorded per package. Dropping the manifest re-breaks [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) and returns [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) property 1 to being unenforceable — which is the state F1 was in.
**Detected at.** Phase 5–6.

---

## 7. Priority

If several fire at once:

| Rank | Condition | Why |
|---|---|---|
| 1 | [F-9](#f-9--the-instructionknowledge-boundary-is-not-structural) security boundary | Halt everything |
| 2 | [F-6](#f-6--derived-state-is-not-genuinely-rebuildable) rebuildability | Invalidates the most documents |
| 3 | [F-1](#f-1--compiled-context-does-not-beat-a-competent-agent-with-plain-file-tools) thesis | Determines whether to continue |
| 4 | [F-2](#f-2--deterministic-current-state-resolution-is-unachievable) determinism | Core differentiator |
| 5 | [F-19](#f-19--incremental-maintenance-does-not-converge-to-a-rebuild) incremental divergence | A sibling of F-6; makes the normal path unsound |
| 6 | [F-11](#f-11--sidecar-confinement-is-insufficient) sidecar escape | Blocks a subsystem |
| 7 | [F-3](#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) Graph Intelligence | Redesign or removal |
| 8 | Everything else | Localised |

---

## 8. Conditions that would *strengthen* the plan

Falsification runs both ways. These findings would justify expanding scope:

- Vectors materially beat lexical+graph → promote to default-on ([ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) reverses).
- Graph expansion contributes far more than expected → justify native investment in extraction.
- Deterministic promotion approaches model-assisted quality → `AI OFF` becomes a genuine competitive advantage rather than a constraint.
- Context compilation beats every baseline by a wide margin → accelerate [Phase 7](15-IMPLEMENTATION-PHASES.md) and consider making the compiler a standalone product surface.

Recording these matters: a plan that only lists ways it could fail will be revised only downward, and the same evidence that could shrink the scope could also justify enlarging it.
