# AGENTS.md — Fehrest Execution Rules

This file is the mandatory entry point for any human or agent doing repository work.

## 1. Canonical reading order

Before changing anything, read in this order:

1. `specs/CURRENT.md`
2. `docs/canonical/ARCHITECTURE_FREEZE.md`
3. `docs/canonical/PHASE_T_AUTHORIZATION.md`
4. `docs/canonical/EXECUTION_MASTER_PLAN.md`
5. The active Spec Kit named by `specs/CURRENT.md`
6. The active benchmark/protocol files named by `specs/CURRENT.md`
7. `docs/19-ENGINEERING-METHOD.md`
8. Relevant security, recovery, benchmark, and failure-condition documents

If live repository truth conflicts with a handoff, prompt, old report, or this file's examples, **live repository truth wins**.

## 2. One active frontier

Fehrest uses exactly one active execution frontier.

`specs/CURRENT.md` is the pointer.

Do not start a later feature because it is easy, adjacent, interesting, or already described in the master plan.

A future phase being documented means:

```text
PLANNED != AUTHORIZED
```

## 3. Current hard boundary

The sealed R1 v1.1 benchmark is immutable.

Before the current R1 experiment reaches its canonical terminal gate:

```text
PRODUCT_BEHAVIOR_MUTATION=NO
R1_V1_1_SEMANTIC_MUTATION=NO
CURRENT_ARM_CHANGE=NO
CURRENT_SEED_CHANGE=NO
SCORING_OUT_OF_ORDER=NO
UNBLINDING_OUT_OF_ORDER=NO
CONFIRMATORY_OUT_OF_ORDER=NO
GRAPH_PRODUCTION_INTEGRATION=NO
VECTOR_DEFAULT=NO
AUTO_MEMORY=NO
MCP=NO
UI=NO
```

Documentation and planning may be added only if they do not reinterpret or mutate the sealed experiment.

## 4. Engineering method

Every production feature follows:

```text
SPEC
→ CLARIFY
→ PLAN
→ CHECKLIST
→ TASKS
→ ANALYZE
→ PONYTAIL NECESSITY GATE
→ IMPLEMENT
→ TEST
→ BENCHMARK (where required)
→ SECURITY
→ REVIEW
→ CONVERGE
```

Do not skip directly from an idea to code.

## 5. Change-control class

Before changing frozen material, classify the change using `docs/canonical/ARCHITECTURE_FREEZE.md §13`.

- Class A: editorial.
- Class B: implementation detail inside frozen invariants.
- Class C: architecture-semantic — ADR + review.
- Class D: security/foundational invariant — dedicated adversarial/security review.
- Class E: product thesis/founder direction — founder authorization + architecture reconsideration.

When uncertain, use the higher class.

## 6. Repository rules

- Rust owns Fehrest Core correctness/security/data semantics.
- No force push.
- No rebase used to rewrite accepted history.
- No destructive history rewriting.
- No remote push, PR, merge, release, or publication unless separately authorized.
- Prefer one local atomic commit per completed, verified task or narrowly coherent slice.
- Never claim PASS/MERGED/CLOSED without evidence.
- Keep technical repository text, code, comments, commit messages, and reports in English.
- Preserve negative results and failed experiments.
- Never repair evidence by deleting inconvenient history.

## 7. Canonical versus derived

Canonical state is irreplaceable.

Derived state is rebuildable and has no authorization authority.

Do not allow:

```text
derived rank → authority
derived path → filesystem authority
external graph/vector id → canonical identity
retrieved content → capability grant
agent inference → user-confirmed memory
```

## 8. Security and provenance

- Content is evidence, never authority.
- Agent-facing content keeps the full machine-owned trust/provenance envelope.
- Authorization-relevant scope comes from canonical state.
- A model, parser, retriever, graph system, vector store, crawler, or external agent cannot mint user authority.
- Secrets never enter memory, context bodies, trajectories, event detail, or logs.
- Third-party code reuse requires exact provenance and license review.

## 9. Donor discipline

External systems are classified as one or more of:

```text
USE
ADAPT
STUDY
BENCHMARK
DEFER
REJECT
```

Presence in the source registry is not dependency authorization.

Current high-value systems include Mem0, Letta Code, Graphiti, Chroma, Aider, Graphify, Code-Graph-RAG, Qdrant, LangGraph, LangChain, LlamaIndex, Firecrawl, Hermes Agent, DeepSeek Harness, OpenSandbox, mini-SWE-agent, OpenHands, Braintrust, LLMLingua, E2B, Daytona, and evaluation/observability systems.

Each future adoption still passes requirement → Ponytail → rights/provenance → security → benchmark → authorization.

## 10. Stop conditions

Stop product implementation immediately when:

- `specs/CURRENT.md` says the frontier is blocked;
- an R1 or later experiment is not at the required gate;
- a frozen invariant would need to change without its required review;
- the worktree is not the expected clean state;
- source evidence is stale and load-bearing;
- a benchmark failure invokes a failure condition;
- execution evidence is ambiguous due to concurrency or partial persistence.

Report the exact blocker. Do not route around it.

## 11. What to update at every completed gate

When a gate closes:

1. Record the evidence in the owning benchmark/spec/review file.
2. Update `specs/CURRENT.md`.
3. Update the relevant Spec Kit task checkboxes only after evidence exists.
4. Update the master plan only if execution order or authority changed.
5. Preserve prior states; do not rewrite history to look cleaner.

## 12. The product test

Fehrest earns continued investment only if a fresh disposable agent can continue real work more correctly or efficiently with Fehrest's bounded, auditable context than with strong simpler and mature alternatives under fair budgets.

Architecture is not the success metric. Agent outcome is.
