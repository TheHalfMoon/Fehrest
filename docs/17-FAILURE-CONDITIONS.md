# Architectural Failure Conditions

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

What findings would force redesign, donor replacement, or postponement. A plan without these is unfalsifiable, and an unfalsifiable plan cannot be reviewed — only believed.

Each condition names the trigger, the detecting benchmark, the consequence, and the documents invalidated.

---

## 1. Thesis-level failures

### F-1 — Compiled context does not beat a competent agent with plain file tools
**Trigger.** [B-7](10-BENCHMARK-PLAN.md): the Fehrest arm does not beat the plain-agent arm by more than the confidence interval.
**Consequence.** **REDESIGN or ABANDON.** Not a tuning problem. The product exists to make a fresh agent continue work correctly from compiled memory; if an agent with `grep` does as well, the entire memory apparatus is unjustified complexity.
**Invalidates.** [A](00-PRODUCT-THESIS.md), [H](07-CONTEXT-COMPILER-SPEC.md), [F](05-MEMORY-MODEL.md), and the rationale for [Phase 7+](15-IMPLEMENTATION-PHASES.md).
**Detected at.** Phase 6 — deliberately before any UI investment.
**Honest note.** This is the condition I consider most likely to fire, because LongMemEval-V2's own reporting shows the best memory system beating an off-the-shelf coding agent by only 3.2 points ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). The margin is genuinely thin.

### F-2 — Deterministic current-state resolution is unachievable
**Trigger.** [B-4](10-BENCHMARK-PLAN.md): current-state accuracy below 100% on C-TEMPORAL, or resolution proves non-deterministic on real conflicts.
**Consequence.** **REDESIGN of the memory model.** The differentiator versus RAG is answering "what is true now" deterministically. Falling back to LLM-adjudicated conflicts would violate [R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) and make Fehrest a slower RAG.
**Invalidates.** [F](05-MEMORY-MODEL.md), [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution), parts of [H](07-CONTEXT-COMPILER-SPEC.md).
**Detected at.** Phase 4.

---

## 2. Donor replacement

### F-3 — The Graph Intelligence *capability* does not earn its cost

> **REWRITTEN IN F1-R1 ([R1-06](reviews/F1-R1-RECONCILIATION.md)).** F1 permitted "drop the graph entirely." That conflated **implementation cost** with **capability importance**, and would have let an implementation problem delete a thesis-critical capability.

**The split that governs this condition:**

```
GRAPH_INTELLIGENCE_CAPABILITY  = CORE          -> may be REPLACED, never DROPPED
GRAPHIFY_PYTHON_RUNTIME        = REPLACEABLE   -> may be replaced freely
```

**Trigger.** [B-3](10-BENCHMARK-PLAN.md) ablation shows graph expansion adds no measurable recall over FTS + memory; **or** [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) shows the runtime is untenable in a target corpus type; **or** [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is falsified and parser fuzzing yields escapes.

**Consequence, graduated by trigger:**

| Trigger | Permitted response | **Forbidden** |
|---|---|---|
| No recall gain in the tested retrieval configuration | Re-examine how the graph is *used* (expansion depth, seeding, ranking); evaluate an alternative extractor; scope to corpus types where it helps | Concluding "connections do not matter" from one retrieval design |
| Superlinear scaling | Partition or scope the graph; evaluate an alternative extractor; reconsider runtime shape | Dropping the capability |
| Sandbox escape | **Halt graph work**; require per-parser WASM isolation ([SRC-043](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)) before resuming | Shipping anyway |

**Why dropping is forbidden.** Graph Intelligence answers *"what is connected?"* — one of the four questions in the [four-layer architecture](00-PRODUCT-THESIS.md#5-the-four-layer-architecture). Lexical search cannot answer it. Without it the product reduces toward a local RAG app with a temporal layer, which is not the thesis. A benchmark showing *one implementation* underperforms *one retrieval configuration* is evidence about that pairing, not about whether relationships matter.

**Invalidates.** [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape), [SRC-001](research/FEHREST_SOURCE_REGISTRY.md#21-graphify), graph rows in [O](14-PERFORMANCE-BUDGETS.md). **Does not invalidate** [E §5](04-DERIVED-DATA-MODEL.md#5-graph-intelligence-capability-vs-implementation) or the four-layer architecture.

**Detected at.** Phase 3 (recall, GI-BENCH), continuous (fuzzing).

**Structural protection.** The capability sits behind a wire contract and a rebuildable ID mapping ([E §5.3](04-DERIVED-DATA-MODEL.md#53-id-mapping-is-the-critical-seam)), so replacing the implementation touches no canonical record — which is what makes "replaceable" true in practice rather than in principle.

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
**Consequence.** Per-parser WASM isolation becomes mandatory before shipping the graph, **or** the graph is dropped ([F-3](#f-3--the-graph-intelligence-capability-does-not-earn-its-cost)).
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
**Trigger.** [O §10](14-PERFORMANCE-BUDGETS.md): more than 5 memory confirmations per active day, sustained.
**Consequence.** Users approve blindly and the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) control becomes theatre. Retune promotion rules — **the rules are wrong, not the user.** Listed as a failure condition because the usual industry response is to blame the operator and keep the alerts.

---

## 7. Priority

If several fire at once:

| Rank | Condition | Why |
|---|---|---|
| 1 | [F-9](#f-9--the-instructionknowledge-boundary-is-not-structural) security boundary | Halt everything |
| 2 | [F-6](#f-6--derived-state-is-not-genuinely-rebuildable) rebuildability | Invalidates the most documents |
| 3 | [F-1](#f-1--compiled-context-does-not-beat-a-competent-agent-with-plain-file-tools) thesis | Determines whether to continue |
| 4 | [F-2](#f-2--deterministic-current-state-resolution-is-unachievable) determinism | Core differentiator |
| 5 | [F-11](#f-11--sidecar-confinement-is-insufficient) sidecar escape | Blocks a subsystem |
| 6 | [F-3](#f-3--the-graph-intelligence-capability-does-not-earn-its-cost) Graphify | Removal, not rewrite |
| 7 | Everything else | Localised |

---

## 8. Conditions that would *strengthen* the plan

Falsification runs both ways. These findings would justify expanding scope:

- Vectors materially beat lexical+graph → promote to default-on ([ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) reverses).
- Graph expansion contributes far more than expected → justify native investment in extraction.
- Deterministic promotion approaches model-assisted quality → `AI OFF` becomes a genuine competitive advantage rather than a constraint.
- Context compilation beats every baseline by a wide margin → accelerate [Phase 7](15-IMPLEMENTATION-PHASES.md) and consider making the compiler a standalone product surface.

Recording these matters: a plan that only lists ways it could fail will be revised only downward, and the same evidence that could shrink the scope could also justify enlarging it.
