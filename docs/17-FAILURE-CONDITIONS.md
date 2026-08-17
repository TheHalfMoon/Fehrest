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

### F-3 — Graphify does not earn its cost
**Trigger.** [B-3](10-BENCHMARK-PLAN.md) ablation shows graph expansion adds no measurable recall over FTS + memory; **or** [B-1](10-BENCHMARK-PLAN.md) shows extraction is badly superlinear ([H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) falsified at >3× projection); **or** [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is falsified and parser fuzzing yields escapes from the sidecar.
**Consequence, graduated by trigger.**
- No recall gain → **drop the graph entirely.** Removes ~300 MB, one process, a Python tree, and 28 grammars of attack surface. A *good* outcome if the evidence says so.
- Superlinear → restrict to code-only or scoped subtrees; reopen [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graphify-runs-as-a-managed-long-lived-sidecar) toward a native port of the deterministic core.
- Sandbox escape → **halt graph work**; require per-parser WASM isolation ([SRC-043](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)) before resuming.
**Invalidates.** [E §4](04-DERIVED-DATA-MODEL.md#4-the-graphify-boundary), [ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graphify-runs-as-a-managed-long-lived-sidecar), [SRC-001](research/FEHREST_SOURCE_REGISTRY.md#21-graphify), graph rows in [O](14-PERFORMANCE-BUDGETS.md).
**Detected at.** Phase 3 (recall, scale), continuous (fuzzing).
**Structural protection.** The graph is D2-optional, so this is a *removal*, not a rewrite. That is why the tiering in [E §2](04-DERIVED-DATA-MODEL.md#2-tiering) exists.

### F-4 — Markdown-native editing proves insufficient
**Trigger.** [H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work) falsified: dogfooding shows users routinely need block transclusion, inline comments, or database blocks that sidecars cannot express.
**Consequence.** **EDITOR REPLACEMENT.** Re-evaluate ProseMirror/Lexical/Tiptap **before** BlockSuite — all are maintained, whereas BlockSuite is a stale mirror ([E-10](research/EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate)). Accepting a richer document model requires an explicit [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) amendment making the sidecar canonical, plus a major migration ([M §9](12-MIGRATION-SCHEMA-EVOLUTION.md#9-anticipated-migrations)).
**Invalidates.** [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--v1-editing-is-markdown-native-blocksuite-is-deferred), [D §7](03-CANONICAL-DATA-MODEL.md#7-why-a-rich-block-crdt-cannot-be-canonical-in-v1), [SRC-003](research/FEHREST_SOURCE_REGISTRY.md#23-codemirror-6).
**Detected at.** Phase 7 — the cheapest hypothesis in the plan to test, needing a week of real use rather than infrastructure.

### F-5 — BlockSuite's status changes
**Trigger.** Upstream resumes independent releases for two consecutive quarters.
**Consequence.** Reopen [SRC-004](research/FEHREST_SOURCE_REGISTRY.md#31-blocksuite--defer-reclassified-from-s) — but only jointly with [F-4](#f-4--markdown-native-editing-proves-insufficient). Maintenance health alone does not justify adopting a richer document model; the structural round-trip argument stands independently of upstream activity ([D §7.2](03-CANONICAL-DATA-MODEL.md#72-the-answer-not-in-general-and-the-impossibility-is-structural)).

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
**Trigger.** T2 compaction loses information later needed for audit or replay; or T1 alone is insufficient to reconstruct agent-visible state ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable) fails).
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
**Consequence.** Per-parser WASM isolation becomes mandatory before shipping the graph, **or** the graph is dropped ([F-3](#f-3--graphify-does-not-earn-its-cost)).
**Detected at.** Phase 3 onward, continuously.

### F-12 — Event-log tamper-evidence is defeatable
**Trigger.** C-TAMPER shows an undetectable modification.
**Consequence.** **Withdraw the claim** rather than weaken the test. Provenance guarantees ([I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance), [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable)) would need restating as best-effort. Documenting a weaker guarantee honestly is acceptable; shipping a claim known to be false is not.

---

## 5. Feature postponement

### F-13 — Collaboration stays postponed
**Trigger.** No demonstrated multi-writer need; or the CRDT↔canonical-file relationship remains unsolved.
**Consequence.** Collaboration stays out. [ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--no-crdt-in-v1) holds. The hard part was never adding Yjs — it is defining how CRDT state relates to canonical files without inverting [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended).

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
**Consequence.** Indexing redesign, or mandatory pre-computation and caching for the compiler — which threatens determinism ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable)) and would need its own ADR.

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
| 6 | [F-3](#f-3--graphify-does-not-earn-its-cost) Graphify | Removal, not rewrite |
| 7 | Everything else | Localised |

---

## 8. Conditions that would *strengthen* the plan

Falsification runs both ways. These findings would justify expanding scope:

- Vectors materially beat lexical+graph → promote to default-on ([ADR-0007](09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional) reverses).
- Graph expansion contributes far more than expected → justify native investment in extraction.
- Deterministic promotion approaches model-assisted quality → `AI OFF` becomes a genuine competitive advantage rather than a constraint.
- Context compilation beats every baseline by a wide margin → accelerate [Phase 7](15-IMPLEMENTATION-PHASES.md) and consider making the compiler a standalone product surface.

Recording these matters: a plan that only lists ways it could fail will be revised only downward, and the same evidence that could shrink the scope could also justify enlarging it.
