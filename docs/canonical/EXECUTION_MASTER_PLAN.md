# Fehrest Execution Master Plan

**Status:** CANONICAL EXECUTION ORDER — DOES NOT ITSELF AUTHORIZE PRODUCT WORK  
**Created:** 2026-08-28  
**Current frontier:** `specs/CURRENT.md`

## 1. Purpose

This document defines the dependency-ordered route from the current R1 thesis experiment to a proven Fehrest product.

It is deliberately different from architecture documentation:

- architecture documents define what Fehrest is allowed to become;
- `specs/CURRENT.md` defines what may happen now;
- this file defines the ordered route between gates;
- the active Spec Kit defines implementation details.

No line in this file widens founder authorization.

## 2. Authority order

When sources disagree, use:

```text
1. Live repository/evidence truth
2. Founder authorization records
3. Architecture Freeze / Constitution
4. Security, threat and canonical-data invariants
5. Active benchmark preregistration
6. specs/CURRENT.md
7. This master plan
8. Active Spec Kit
9. Older reports, handoffs and research notes
```

A benchmark preregistration outranks implementation convenience.

## 3. Global execution invariants

### E-01 — One active frontier

Exactly one product/experiment frontier is active at a time.

### E-02 — One active product Spec Kit

At most one implementation Spec Kit may be active. Future Spec Kits may exist as plans but are not authorization.

```text
SPECIFIED != AUTHORIZED
```

### E-03 — Gates require evidence

Tasks/phases close only when their named evidence exists. Never convert intent or an unchecked assumption into PASS.

### E-04 — Negative results are first-class

A failed benchmark closes honestly. It does not authorize adding more technology merely to improve the number.

### E-05 — No silent phase reorder

Changing phase order or benchmark decision authority requires the change-control class defined by the frozen architecture, normally ADR/review for architecture-semantic changes.

### E-06 — Donor research creates no dependency

External projects are `USE / ADAPT / STUDY / BENCHMARK / DEFER / REJECT` candidates. Inclusion in a donor matrix does not make them production dependencies.

### E-07 — AI OFF remains complete

Core correctness, security, canonical state and replay semantics must not require a paid model or network service.

### E-08 — Canonical truth remains Fehrest-owned

No graph, vector, crawler, agent framework, memory service or model can mint canonical identity or user authority.

### E-09 — Model-visible Fehrest context becomes receipted

By the end of Phase 5, every Fehrest-produced model-visible package must bind request, grant, canonical state, compiler policy and emitted content to an auditable receipt.

### E-10 — No UI before proof

The desktop product cannot become an escape hatch from a failed core thesis.

---

# 4. Current gate — R1 terminal thesis experiment

## Objective

Finish the current longitudinal continuation experiment without changing sealed v1.1 semantics.

Historical sealed anchor:

```text
commit=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
tree=f7ea7e0f57019c8061a4019ac614730f68750f19
preregistration=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

The GitHub bootstrap history is documented separately and must not replace these historical evidence identifiers.

## Required R1 order

```text
valid variance pilot execution
→ raw evidence seal
→ execution review
→ blinded pilot scoring when authorized
→ power analysis
→ confirmatory N
→ confirmatory manifest seal
→ confirmatory execution
→ raw seal
→ blinded scoring
→ scoring seal
→ unblind
→ terminal verdict
```

The exact active sub-gate comes from live R1 evidence, not this plan.

## Forbidden while R1 is open

```text
product behavior changes
R1 arm/seed/corpus/task/scoring changes
graph/vector/automatic-memory integration
post-hoc benchmark redesign
using pilot outcomes to tune product behavior
UI work
```

## Terminal routing

### THESIS_SUPPORTED

Founder may authorize Spec 002.

### THESIS_SUPPORTED_ON_COST

Founder may authorize Spec 002, but cost/token/maintenance efficiency becomes a primary design constraint.

### THESIS_SUPPORTED_ON_SAFETY

Founder may authorize Spec 002 with stale-use/constraint safety retained as a primary acceptance dimension.

### THESIS_SUPPORTED_WITH_COST_CAVEAT

Do not expand expensive capabilities. Founder chooses cost-reduction work, limited hardening or stop.

### THESIS_NOT_SUPPORTED

Trigger product-thesis failure review. Do not begin Spec 002 by default.

### THESIS_FAIL

Halt product expansion and reconsider the thesis.

### INCONCLUSIVE

No silent continuation. Founder explicitly chooses extension, limited hardening with rationale, or stop.

---

# 5. Phase 1 — Canonical Core Convergence

**Spec Kit:** `002-post-r1-canonical-core-convergence`  
**Current status:** PREPARED / BLOCKED

## Goal

Turn the Phase T canonical mechanisms into the production-grade canonical core before expanding derived or agent-facing capability.

## Required work

### 1A — Phase T truth reconciliation

Record exactly:

- what Phase T implemented;
- what it intentionally minimized;
- what R1 actually measured;
- what remains deferred.

Known reconciliation points:

```text
memory value semantics exist; durable memory product surface remains later
Phase T compiler is bounded deterministic assembly, not the full production pipeline
Phase T byte budget is not the final tokenizer budget
incremental-vs-clean B-12 was unavailable because incremental indexing did not exist
vault single-writer locking already exists; the remaining gap is stronger mutator enforcement
```

Do not rewrite historical evidence to hide these distinctions.

### 1B — Vault identity and crash-safe canonical writes

Implement and verify:

```text
vault identity
format/schema version
atomic/crash-aware canonical replacement
explicit persistence boundary
unsupported-filesystem failure visibility
```

Do not promise durability stronger than measured platform behavior.

### 1C — Writer-owned mutation boundary

Reuse current `Vault/WriteLock` semantics. Strengthen the API so canonical mutations require/prove writer ownership rather than relying solely on caller discipline.

No automatic stale-lock theft.

### 1D — Production event journal

Implement:

```text
versioned event envelope
typed payloads
contiguous sequence + honest hash chain
explicit flush/sync boundary
torn-tail detection/quarantine
mid-log gap and chain-break fail-closed behavior
schema upcasting skeleton
golden old-version fixtures
recovery evidence
```

### Phase 1 exit

Canonical loss under the required fault matrix must be zero. All existing security/path/identity/resource invariants remain green. R1 sealed semantics remain unchanged.

---

# 6. Phase 2 — Derived Index and Lexical Retrieval Convergence

**Future Spec Kit:** `003-phase2-derived-index-convergence`

## Goal

Make derived lexical/index state genuinely disposable, incremental and deterministically reconcilable.

## Required work

```text
content-hash incremental update
watcher + debounce
reconciliation scan
full rebuild
resumable/cancellable rebuild where required
derivation registry
projection checkpoints
invalidation completeness
incremental-vs-clean equivalence
```

FTS/BM25 remains candidate generation, not authority.

Run the incremental-vs-fresh benchmark before package identity depends on history-sensitive ranking.

### Strong simple baseline

Aider repo-map becomes a mandatory context baseline for code/project workloads.

### Vectors

Qdrant, Chroma and other vector systems remain optional benchmark/provider candidates. No vector default is authorized here.

---

# 7. Phase 3A — Graph Intelligence Capability Experiment

**Future Spec Kit:** `004-gi-cap`

## Goal

Ask whether graph structure materially helps before building graph infrastructure.

## Comparator family

Where workloads are comparable, include:

```text
Fehrest lexical/structured/temporal baseline
Graphify
Code-Graph-RAG
Graphiti for workloads matching temporal-context-graph semantics
```

Normalize tasks, model-visible budget and evaluation criteria; do not force incompatible systems into fake equivalence.

## Measure

```text
retrieval quality
task/continuation correctness
build time
incremental cost
memory/disk footprint
context tokens
API cost where applicable
```

## Decision

If graph adds no material value at acceptable cost:

```text
GRAPH_PRODUCTION_INTEGRATION=REJECT_FOR_V1
```

Proceed to Phase 4.

If retained, Phase 3B becomes eligible.

---

# 8. Phase 3B — Optional Graph Production Integration

**Future Spec Kit:** `005-graph-production-integration`  
**Entry:** Phase 3A retains graph capability.

Implement the smallest replaceable `GraphProvider`-style boundary required by measured needs.

Hard invariants:

```text
external graph ids != Fehrest identity
graph paths != filesystem authority
graph rank != authorization
graph bytes = disposable
graph absent => visible recall degradation, not canonical failure
```

Graphify remains a candidate, not a predetermined dependency. Code-Graph-RAG contributes strong evaluation/provenance methods. Graphiti remains a direct temporal-context competitor where appropriate.

---

# 9. Editor gate

The editor remains a separate prototype/evidence gate.

It does not authorize desktop implementation. v0 may be used only under the already-defined future design workflow.

---

# 10. Phase 4 — Temporal Memory Productization

**Future Spec Kit:** `006-phase4-memory-productization`

## Goal

Turn existing Phase T memory semantics into a durable product subsystem.

## Required work

```text
canonical memory journal/store
explicit memory-write surface
schema versioning/upcasting
provenance verification
PENDING/ACTIVE/RETRACTED/SUPERSEDED transitions
confirmation and contradiction workflows
current/as-of query APIs
memory recovery
```

## Memory role research

Study an additional orthogonal role axis:

```text
Semantic
Procedural
Episodic
```

Do not replace Fehrest's existing domain memory categories merely to match external frameworks.

## Required current comparators/donors

Refresh and evaluate:

```text
Mem0
Letta Code
Graphiti
Chroma agentic memory
Hermes memory/skills
```

Vendor-reported results are hypotheses to reproduce, not local proof.

## Automatic memory

Still blocked initially.

Model-assisted extraction may create only evidence-bound `PENDING` candidates until a later promotion gate proves acceptable poisoning/staleness/confirmation behavior.

---

# 11. Phase 5 — Full Context Compiler and Agent Gateway

**Future Spec Kit:** `007-phase5-context-compiler-agent-gateway`

This is the defining production phase.

## Full deterministic compiler

Implement the already-specified pipeline:

```text
AUTHORIZE
→ SEED
→ STATE RESOLUTION
→ LEXICAL
→ optional GRAPH
→ optional VECTOR
→ FUSION
→ TEMPORAL FILTER
→ SCOPE ASSERTION
→ BUDGET
→ ASSEMBLE
```

No model is required for correctness.

## Query-conditioned candidate selection

Stop treating all scanned objects as equivalent project state. Every candidate must have an inspectable reason it entered the set.

## SelectionTrace

Record as derived evidence:

```text
candidate identity
retriever/backend + generation
rank/fusion rank
temporal result
scope result
inclusion/omission reason
budget cost
transform chain
```

The manifest records what was served. SelectionTrace explains why.

## Production manifest / receipt

Bind at minimum:

```text
manifest schema version
context instance/content identity
compiler/policy version
principal/session/agent
request digest
grant snapshot digest
canonical high-water mark
derived-generation bindings
tokenizer/version when model-facing
package digest
selection-trace digest
```

Per item bind source revision/content, rendered hash, trust/provenance/lifecycle/resolution/scope and transform/truncation metadata.

## Replay outcomes

Exactly:

```text
IDENTICAL
DIVERGED(reason + item diff)
UNRECONSTRUCTABLE(reason)
```

Never report divergent output as reproduced.

## Budget model

Keep a deterministic hard-byte safety ceiling and add pinned tokenizer/model-token accounting for model-facing efficiency.

## Agent authorization gateway

```text
deny by default
immutable session grant
single authorization chokepoint
scope enforced during retrieval
agents address object IDs, never arbitrary paths
subagent grants are subsets
user authority is separate from model content
```

## Runtime interoperability

Fehrest is not an agent framework. Study adapters to LangGraph, Hermes, Letta, mini-SWE-agent, OpenHands and standard client surfaces.

DeepSeek Harness contributes the useful principle:

```text
MODEL_VISIBLE_FEHREST_INPUT => RECEIPTED
```

Do not adopt its framework wholesale.

---

# 12. Phase 6 — Full Vertical Proof

**Future Spec Kit:** `008-phase6-vertical-proof`

## Goal

Prove the complete product mechanism before UI.

Freeze tasks and evaluation before tuning.

## Strong baseline ladder

Use applicable subsets of:

```text
competent plain agent + files
strong AGENTS.md / repository-native docs
raw history
BM25 / lexical
maintained LLM wiki
Aider repo-map
current Mem0
current Letta Code
Graphiti
Graphify
Code-Graph-RAG
Fehrest deterministic core
Fehrest as-shipped
```

Pre-register which comparators apply to each workload; do not inflate experiments with irrelevant systems.

## Agent harness

Prefer a minimal inspectable coding harness such as mini-SWE-agent where it reduces framework confounding. Also test at least one richer real-world runtime.

## Trajectory interoperability

Use an open full-fidelity trajectory record, with Harbor ATIF as a primary reference. A compact Fehrest agent-readable trajectory may exist as a derived view.

Raw trajectory evidence is not automatically canonical memory.

## Safe execution

Do not build a sandbox platform. Compare/provider-adapt:

```text
OpenSandbox
E2B
Daytona
local Docker
```

OpenSandbox is particularly relevant for egress policy, credential injection and strong isolation.

## Evaluation records

Fehrest owns one local open trial schema. Optional exporters may target Braintrust, OpenTelemetry/Phoenix, Langfuse, Promptfoo, DeepEval or RAGAS.

Hosted services never become the only experiment record.

## Context compression

Treat compression as an experiment:

```text
none
safe deterministic truncation
deterministic extractive
LLMLingua / LLMLingua-2
model-assisted compression
```

Keep original evidence and transform provenance.

## Autoresearch-style Context Research Lab

Only after benchmark freeze, allow bounded experiments over `context-policy.toml`.

It may optimize selection/allocation. It may not self-modify canonical authority, security invariants, benchmark tasks, scoring or thresholds.

## Falsification

If the defining continuation benchmark fails its preregistered criteria, do not proceed to UI.

---

# 13. Phase 7 — Desktop Product

**Future Spec Kit:** `009-phase7-desktop`

Hard entry:

```text
Phase 6 full proof PASS
AND editor gate CLOSED
AND founder authorizes product UI
```

The UI is presentation. Headless Rust Core remains complete and authoritative.

---

# 14. External acquisition

Firecrawl and LlamaIndex are optional acquisition/parser donors when a measured external-evidence requirement exists. They are not default Phase 1–5 dependencies.

Any acquisition adapter must preserve:

```text
source URL/path
source revision/etag when available
acquired_at
raw hash
normalized hash
acquirer id/version
parser id/version
trust classification
```

External content remains evidence, never instruction or capability authority.

---

# 15. Evidence freshness

Load-bearing external claims must carry enough state to detect staleness:

```text
source
immutable revision/version
claim
claim class
verified_at
status
supersedes
```

Recommended statuses:

```text
CURRENT
STALE_UNVERIFIED
SUPERSEDED
RETRACTED
UNAVAILABLE
```

Use review TTL only where freshness can materially change a current architecture, benchmark, security or dependency decision.

---

# 16. Planned Spec Kit sequence

| ID | Planned Spec Kit | Entry |
|---|---|---|
| 002 | `post-r1-canonical-core-convergence` | R1 route + founder authorization |
| 003 | `phase2-derived-index-convergence` | 002 PASS |
| 004 | `gi-cap` | 003 PASS |
| 005 | `graph-production-integration` | 004 retains graph |
| 006 | `phase4-memory-productization` | Phase 2 + graph decision |
| 007 | `phase5-context-compiler-agent-gateway` | 006 PASS; graph optional |
| 008 | `phase6-vertical-proof` | 007 PASS |
| 009 | `phase7-desktop` | 008 PASS + editor gate + founder authorization |

If graph is rejected, 005 may remain unused. Do not renumber history for aesthetics.

---

# 17. Master failure routing

```text
canonical integrity failure      → stop before Phase 2
incremental/rebuild mismatch     → fix/redesign Phase 2
graph no material benefit        → remove graph from v1
memory resolution not exact      → no agent gateway
compiler replay/determinism fail → no agent exposure
scope/injection security fail    → no MCP/agent tools
vertical proof fails             → no desktop product
```

---

# 18. Deliberate rejections

```text
feature accumulation as strategy
agent framework inside Fehrest Core
mandatory graph database
mandatory vector database
own crawler
own sandbox platform
own generic eval SaaS
automatic memory before explicit memory works
UI before thesis proof
popularity as architecture evidence
vendor benchmarks as local proof
rewriting failed evidence
```

---

# 19. Completion definition

Fehrest reaches the v1 product gate only when:

1. canonical data survives failures and remains inspectable;
2. derived data is genuinely disposable;
3. temporal memory resolves correctly;
4. the context compiler is bounded, authorized, auditable and replayable;
5. agent integration cannot widen authority;
6. strong simple and mature external baselines are beaten under fair budgets;
7. recovery/security/scale gates pass;
8. Core remains useful without UI, network, Python, graph, vector or paid model;
9. only then is the desktop product built around the proven Core.

The end-state test is:

> A fresh agent can enter a long-running project without inheriting chat history and receive the right current evidence, constraints, decisions, gotchas, provenance, contradictions and permitted actions — within a bounded context — more reliably than strong alternatives.
