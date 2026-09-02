# Fehrest Full Project Review 2026

**Status:** NON-AUTHORIZING WHOLE-PROJECT READINESS REVIEW  
**Date:** 2026-09-02  
**Review scope:** governance, product thesis, architecture, source/donor readiness, benchmark route, project portability, memory/agent context, security boundaries, and future execution sequencing.  
**Active execution frontier:** `R1 / REPLACEMENT_VARIANCE_PILOT_EXECUTION`

> This review does not authorize implementation, graph/vector production integration, automatic memory, MCP/ACP, Git import/export, collaboration, sync, UI, or any later product phase while blocked by `specs/CURRENT.md`.

---

## 1. Executive assessment

Fehrest now has a coherent and unusually strong long-term architecture direction, but its readiness must be described in layers rather than with one blanket `READY` claim.

Current assessment:

```text
PRODUCT_NORTH_STAR=STRONG
CORE_INVARIANTS=STRONG
CANONICAL_EXECUTION_ORDER=DEFINED
R1_TERMINAL_EVIDENCE=NOT_YET_PRESENT
SOURCE_DISCOVERY_COVERAGE=STRONG
CURRENT_SOURCE_ROLE_MAPPING=STRONG
HISTORICAL_SOURCE_EVIDENCE_RECOVERY=INCOMPLETE
GRAPH_EXPERIMENT_DESIGN=READY_FOR_FUTURE_SPECIFICATION
MEMORY_COMPARATOR_SET=READY_FOR_FUTURE_SPECIFICATION
AGENT_INTEROP_SOURCE_SET=READY_FOR_FUTURE_SPECIFICATION
PROJECT_TRANSPORT_SOURCE_SET=READY_FOR_FUTURE_SPECIFICATION
LOCAL_FIRST_COLLAB_SOURCE_SET=READY_FOR_FUTURE_RESEARCH
PRODUCTION_DEPENDENCY_PINS=NOT_REQUIRED_YET_AND_NOT_COMPLETE
PRODUCTION_IMPLEMENTATION_AUTHORIZED=NO
```

The most important conclusion is that the plan should **not** select Graphify, GraphRAG, Mem0, Letta, Buzz, a vector database, an agent runtime, or a sandbox by popularity. Fehrest has enough source coverage to run requirement-driven experiments and retain only capabilities that materially improve the project brain under fair cost, latency, security, and portability constraints.

---

## 2. What Fehrest is trying to prove

The product thesis is now clearer than a feature-parity plan.

Fehrest aims to become:

> **The durable project brain and governed work substrate that lets a fresh authorized human or agent recover the right current context quickly, preserve project learning across disposable tools and models, act under explicit authority, and prove what happened.**

For developer projects, this includes the additional portability thesis:

> **Import a project without requiring a remote fork, enrich it with durable semantic project state, continue work with any compatible agent or IDE, reconcile upstream explicitly, and publish selected Git changes back to GitHub or another forge when desired.**

The critical product laws remain:

```text
PROJECT != REPOSITORY
REPOSITORY != PROJECT_BRAIN
GIT_HISTORY != PROJECT_MEMORY
CANONICAL != DERIVED
EVIDENCE != AUTHORITY
IMPORT != FORK
IMPORT != PUBLISH_AUTHORITY
MODEL_OUTPUT != FACT
CHAT != CANONICAL_STATE
FAST_CONTEXT != FULL_HISTORY_DUMP
REMEMBERING != VALIDITY
IDE != MEMORY_OWNER
AGENT_RUNTIME != MEMORY_OWNER
MODEL_PROVIDER != MEMORY_OWNER
```

---

## 3. Governance review

### 3.1 What is strong

Fehrest has structural defenses against the most common ambitious-project failure mode: turning planning into accidental implementation authority.

The live repository currently provides:

- one active execution frontier in `specs/CURRENT.md`;
- canonical dependency ordering in `docs/canonical/EXECUTION_MASTER_PLAN.md`;
- a frozen architecture/constitution and threat model;
- explicit benchmark/failure conditions;
- explicit donor discipline in `AGENTS.md`;
- exact R1 historical evidence identity separated from later GitHub bootstrap identity;
- negative-result preservation;
- exact evidence gates before task closeout.

### 3.2 Current blocker remains legitimate

The project is **not** product-implementation ready today because the R1 terminal thesis experiment is not complete.

Current live state remains conceptually:

```text
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
```

Planning can be improved now. Product behavior cannot be advanced merely because future architecture is well specified.

### 3.3 PR #2 and PR #27 must remain conceptually separate

- PR #2 is a broad V2 founder-product proposal and remains draft/non-authorizing.
- PR #27 is the current hardening/research review that sharpens the Agent Brain, project-substrate, market, Buzz-donor, source-readiness, and whole-project planning.

Neither PR should be used to bypass R1 or activate Spec 002.

---

## 4. Source evidence review

### 4.1 Critical historical source gap

Several mirrored architecture, benchmark, recovery, and security documents reference:

```text
docs/research/EVIDENCE_LOG.md
docs/research/FEHREST_SOURCE_REGISTRY.md
```

Those historical files are not currently present in the GitHub mirror reviewed here.

This review therefore adopts the only safe rule compatible with `AGENTS.md`:

```text
DO_NOT_RECONSTRUCT_MISSING_HISTORICAL_EVIDENCE_FROM_MEMORY
```

The new dated file:

```text
docs/research/FEHREST_SOURCE_READINESS_REGISTRY_2026.md
```

is a **new current-source registry**, not a claim to recover the historical documents.

If original bytes later appear in a recovery bundle or source archive, they should be reconciled as historical evidence without rewriting this newer record.

### 4.2 Current source coverage

The present source set is broad enough for future architecture and benchmark design across the important Fehrest capability families:

```text
graph intelligence / GraphRAG
lexical + vector retrieval
temporal memory / continual learning
agent protocols
agent runtimes
execution isolation
security / capability policy
external document/web ingestion
local-first collaboration
Git/project transport
evaluation / observability
context compression
```

The source portfolio is intentionally redundant. Redundancy is useful because Fehrest should compare independent approaches rather than inherit one donor's assumptions.

---

## 5. Graph Intelligence review

Graph capability is strategically interesting but remains explicitly falsifiable.

### 5.1 Required future comparator family

The future Graph Intelligence capability experiment should use workload-appropriate subsets of:

```text
Fehrest lexical / structured / temporal baseline
Aider repo-map baseline
Graphify
Code-Graph-RAG
Graphiti
Microsoft GraphRAG
LightRAG
optional Fehrest-native tree-sitter extraction path
```

### 5.2 Why these are not interchangeable

#### Graphify

Best fit for deterministic local code-structure extraction and a donor-quality graph construction pipeline. It is relevant to code relationships, AST structure, provenance, and repository understanding.

#### Code-Graph-RAG

Best used as a code-graph retrieval and code-understanding comparator/donor. It is especially useful for testing whether graph structure improves code navigation, structural search, impact analysis, and agent task performance.

#### Graphiti

Best fit for temporal context-graph comparison. It is more relevant to evolving facts, history and temporal relationships than a static code-only graph benchmark.

#### Microsoft GraphRAG

Valuable methodology and research comparator for entity/relationship/claim extraction, communities, and global/local graph query behavior. It should not be presumed to be a production dependency.

#### LightRAG

Useful lightweight graph-RAG comparator for hybrid retrieval/cost experiments.

#### tree-sitter

Important native substrate reference. If graph capability proves valuable but a heavy Python sidecar does not earn its operational cost, Fehrest needs a plausible Rust-controlled extraction route.

### 5.3 Decision rule

Graph production work remains contingent on measurable incremental value.

```text
IF graph does not materially improve continuation/retrieval/task outcomes
AT acceptable latency + build cost + memory/disk + maintenance cost
THEN reject graph production integration for the relevant release.
```

Graph sophistication is not itself product success.

---

## 6. Retrieval architecture review

Fehrest should retain a layered retrieval ladder:

```text
exact structured state
lexical / BM25
project-native structural context
optional graph
optional vector
fusion
explicit temporal/scope filtering
budgeted deterministic assembly
```

Sources ready for future evaluation include:

```text
Aider repo-map
Qdrant
Chroma
sqlite-vec
Graphify / Code-Graph-RAG / Graphiti
LLMLingua for compression experiments
```

Key rule:

```text
RETRIEVAL_RANK != AUTHORIZATION
```

A vector, graph, or fusion layer may choose candidates. It may not decide what the agent is allowed to see or what becomes canonical truth.

---

## 7. Memory and continual-learning review

The memory plan is stronger when treated as a lifecycle rather than a retrieval database.

Future comparator/reference set:

```text
Mem0
Letta
Graphiti
Hermes Agent
LongMemEval-V2
```

Required Fehrest lifecycle:

```text
experience
→ evidence / trajectory
→ candidate memory / procedure / decision / gotcha
→ verification
→ durable state
→ use
→ source change / contradiction / feedback
→ revalidation / supersession / retraction / consolidation
```

Critical correctness dimensions:

```text
current-state correctness
temporal/as-of correctness
stale-memory error rate
unsupported-memory rate
constraint preservation
supersession correctness
revalidation latency
source-change invalidation quality
continuation outcome per context token
```

The strongest Fehrest advantage will not be storing more memories. It will be **remembering with provenance and knowing when remembered state may have become invalid**.

---

## 8. Context compiler review

The defining production mechanism remains deterministic, bounded context compilation.

Future architecture remains:

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

The user goal that an agent can understand a project in seconds should be implemented as an SLO and benchmark suite, not a promise to dump all history.

Required future metrics include:

```text
project orientation P50/P95
task-context compile P50/P95
first useful context latency
continuation success
constraint miss rate
stale-state rate
context recall at budget
tokens / bytes / cost
provenance completeness
cross-runtime continuation success
```

Recommended architecture:

```text
Working Continuity Layer
+ Deep Project Memory
```

The first is a fast reproducible projection. The second preserves the authorized history/evidence needed for drill-down.

---

## 9. Agent interoperability review

Fehrest should avoid owning a proprietary agent loop merely to capture users.

Current source set supports a protocol-first future:

```text
MCP
ACP
Buzz ACP/MCP patterns
Hermes
mini-SWE-agent
OpenHands
Aider
other future runtimes through adapters
```

### Required correction before implementation

The exact ACP canonical specification/repository and immutable revision must be pinned before Phase 5 design becomes implementation-ready.

MCP version must likewise be fixed in a specification when Phase 5 activates.

### Core boundary

```text
PROTOCOL_CAPABILITY != FEHREST_AUTHORITY
```

Fehrest capability grants/leases and canonical scope checks remain authoritative regardless of what an MCP server or ACP client advertises.

---

## 10. Execution and sandbox review

A useful agent brain must eventually support safe governed action.

Future comparison set:

```text
NativeExecutor
local Docker / OCI
E2B
Daytona
OpenSandbox after exact source identity is resolved
Buzz dev-MCP process lifecycle patterns
```

The architecture must preserve:

```text
PROCESS_LIFECYCLE_HARDENED != SECURITY_SANDBOXED
```

Required dimensions:

```text
filesystem confinement
network/egress policy
credential injection and redaction
child-process cleanup
cancellation
timeouts
resource budgets
artifact capture
cross-platform behavior
receipt completeness
```

Daytona's current public license requires special care before source adaptation. OpenHands also requires path-level license review because licensing is not uniformly described by one simple repository-wide reuse assumption.

---

## 11. Git and project-substrate review

The no-fork project concept is architecturally sound if Fehrest does not blur Git semantics with project-memory semantics.

Future transport comparison should include:

```text
system Git
gix / gitoxide
libgit2 / git2-rs
```

Required evaluation dimensions:

```text
object fidelity
pack/protocol coverage
partial/shallow repository behavior
submodules/LFS policy
Windows behavior
performance
security surface
maintenance burden
bundle/patch/export fidelity
upstream reconciliation
```

Project import must preserve exact source provenance and license/notice evidence where relevant.

A Fehrest Project may contain multiple repositories and non-Git evidence. Git transport therefore remains one subsystem inside a larger Project Capsule.

---

## 12. External evidence ingestion review

Future source set is sufficient to design a fair ingestion architecture:

```text
Firecrawl
Docling
Microsoft MarkItDown
LlamaIndex connector/parser ecosystem
native/simple parsers where sufficient
```

Docling is particularly relevant for structured PDF/document ingestion. MarkItDown is a useful lightweight conversion baseline. Firecrawl is useful only where live web acquisition is justified.

Every acquisition route must record:

```text
source location
source revision / etag when available
acquired_at
raw hash
normalized hash
acquirer id/version
parser id/version
trust classification
```

External bytes are evidence. They are not instructions or capability authority.

---

## 13. Local-first collaboration review

The mature Slack/Buzz-class collaboration goal is compatible with Fehrest only if a replication constitution exists before implementation.

Current useful source family:

```text
Automerge
Yjs
local-first / CRDT literature
Buzz collaboration/event patterns
```

The key architecture decision is not “which CRDT library.” The hard problem is semantic authority:

```text
which events are canonical?
what can merge automatically?
what conflicts must remain explicit?
how are decisions/grants/work-state transitions represented?
what may remain local/private?
how can a user fully export and recover a shared project?
how can a hosted agent operate without making the server canonical authority?
```

CRDT convergence can solve data synchronization mechanics. It cannot replace those domain decisions.

---

## 14. Security review of source adoption

Every external implementation must be assumed to enlarge the trusted or semi-trusted computing surface.

Before reuse/adoption:

```text
source repository + immutable revision
license SPDX and exceptions
NOTICE/attribution/trademark obligations
copied/adapted paths
upstream copyright headers
SBOM/dependency snapshot
network behavior
filesystem behavior
secret handling
update policy
known advisories
removal/escape path
benchmark justification
active-spec authority
```

Relevant security references already mapped include:

```text
cap-std
Cedar
AgentDojo
Buzz permission/process patterns
sandbox provider comparisons
```

No external policy engine, graph service, vector store, parser, crawler, or agent runtime becomes a canonical authority.

---

## 15. Evaluation readiness review

Fehrest should not rely on one benchmark.

The future benchmark portfolio should include:

```text
LongMemEval-V2-style memory tasks
fresh-agent continuation experiments
SWE-bench-style repository work where applicable
maintained wiki baseline
plain competent agent + files baseline
Aider repo-map baseline
retrieval/graph comparator experiments
security/prompt-injection suite
multi-agent conflict tests
cross-IDE/CLI/runtime continuation
context latency / token / cost evaluation
import/export fidelity
upstream reconciliation
backup/restore/corruption recovery
human attention / approval friction
```

Fehrest should own an open local trial/evidence record. Braintrust/OpenTelemetry/etc. are optional exporters, never the only experiment ledger.

---

## 16. What sources are ready now

“Ready” here means ready for future study/spec/benchmark design, not production adoption.

### Strongly ready source families

```text
Graph / GraphRAG:
  Graphify
  Code-Graph-RAG
  Graphiti
  Microsoft GraphRAG
  LightRAG
  tree-sitter

Memory:
  Mem0
  Letta
  Graphiti
  Hermes
  LongMemEval-V2

Retrieval:
  Aider repo-map
  Qdrant
  Chroma
  sqlite-vec
  LLMLingua

Agent/runtime:
  MCP
  Buzz
  Hermes
  mini-SWE-agent
  OpenHands

Execution:
  local Docker/OCI
  E2B
  Daytona
  Buzz process lifecycle patterns

Ingestion:
  Firecrawl
  Docling
  MarkItDown
  LlamaIndex

Collaboration:
  Automerge
  Yjs

Git/project transport:
  Git
  gix/gitoxide
  libgit2/git2-rs

Evaluation:
  LongMemEval-V2
  SWE-bench
  AgentDojo
  OpenTelemetry-compatible exporters
```

### Source items that still need exact identity/pin work

```text
historical Fehrest EVIDENCE_LOG bytes
historical Fehrest SOURCE_REGISTRY bytes
exact ACP source/spec revision
exact intended OpenSandbox upstream
exact production pins for every donor only when a real requirement reaches its adoption gate
```

This is acceptable at the current R1 frontier because those items are not authorized production dependencies today.

---

## 17. Dependency-ordered future readiness plan

This review does not modify the canonical master plan. It confirms and hardens the intended order.

### Gate R1 — finish thesis evidence

```text
valid replacement pilot
→ evidence seal
→ review/scoring/power/confirmatory sequence
→ terminal R1 verdict
→ explicit founder route decision
```

### Phase 1 — canonical core convergence

No new graph/vector/agent dependency required.

Prove canonical identity, durable writes, event journal, recovery and writer ownership first.

### Phase 2 — derived lexical/index convergence

Build the strong simple baseline before graph complexity.

Use:

```text
native lexical / FTS
Aider repo-map comparator
optional vector candidates only as experiments
```

### Phase 3A — Graph Intelligence capability experiment

Freeze fair workloads and budgets, then compare workload-appropriate subsets of:

```text
simple Fehrest baseline
Graphify
Code-Graph-RAG
Graphiti
Microsoft GraphRAG
LightRAG
native tree-sitter candidate if useful
```

Outcome decides whether Phase 3B exists.

### Phase 3B — graph integration only if retained

Select the smallest replaceable provider shape supported by benchmark results. Re-pin/relicense/resecurity-review the actual chosen implementation at that time.

### Phase 4 — temporal memory productization

Benchmark against current Mem0, Letta, Graphiti and Hermes. Preserve Fehrest's candidate/verification/supersession model.

### Phase 5 — context compiler + agent gateway

Pin exact MCP/ACP specs. Implement Fehrest-owned grants, context receipts, SelectionTrace and replay before broad agent integration.

### Phase 6 — full vertical proof

Run real continuation, cross-runtime, recovery, security, cost, latency and import/export trials against strong baselines.

### Phase 7+ — product surfaces

Desktop/workspace/collaboration/project management expand only after core proof. Replication constitution precedes multi-user collaboration. Project Capsule/Git import/export receives its own bounded specification and fidelity gates.

---

## 18. Plan-readiness checklist

The future plan is considered research-ready only if all of the following remain true:

```text
[PASS] one active execution frontier is preserved
[PASS] R1 is not reinterpreted by future planning
[PASS] graph capability is falsifiable
[PASS] graph donors are replaceable
[PASS] strong simple retrieval baseline exists
[PASS] memory competitors are current-enough to design future evaluation
[PASS] automatic memory remains gated
[PASS] agent protocols do not own authority
[PASS] execution lifecycle and sandbox security are distinguished
[PASS] project identity is above Git repository identity
[PASS] no-fork import preserves upstream provenance
[PASS] publish authority is explicit
[PASS] external ingestion remains evidence-only
[PASS] local-first collaboration has a required constitution gate
[PASS] open semantic export remains mandatory
[PASS] source/adoption rights gate is explicit
[PASS] missing historical source bytes are acknowledged, not invented
[PASS] phase ordering remains canonical
```

Open source-readiness items:

```text
[OPEN] recover/reconcile historical EVIDENCE_LOG when original bytes are found
[OPEN] recover/reconcile historical SOURCE_REGISTRY when original bytes are found
[OPEN] pin ACP when Phase 5 specification begins
[OPEN] resolve exact OpenSandbox upstream before its first benchmark
[OPEN] pin/license/SBOM each actual production donor only after a requirement selects it
```

---

## 19. Whole-project readiness verdict

```text
WHOLE_PROJECT_VISION=READY_FOR_CONTINUED_GOVERNED_EXECUTION
WHOLE_PROJECT_PLAN=READY_AS_NON_AUTHORIZING_FUTURE_DIRECTION
SOURCE_PORTFOLIO=SUFFICIENT_FOR_FUTURE_REQUIREMENT_DRIVEN_RESEARCH
GRAPH_AND_GRAPHRAG_SOURCE_COVERAGE=STRONG
MEMORY_SOURCE_COVERAGE=STRONG
AGENT_INTEROP_SOURCE_COVERAGE=STRONG
PROJECT_TRANSPORT_SOURCE_COVERAGE=STRONG
INGESTION_SOURCE_COVERAGE=STRONG
COLLABORATION_SOURCE_COVERAGE=SUFFICIENT_FOR_CONSTITUTION_RESEARCH
HISTORICAL_SOURCE_RECOVERY=INCOMPLETE_BUT_EXPLICIT
PRODUCTION_DEPENDENCY_SELECTION=INTENTIONALLY_DEFERRED
CURRENT_PRODUCT_IMPLEMENTATION_AUTHORITY=NO
R1_ACTIVE_FRONTIER_CHANGED=NO
```

The repository is therefore ready to continue the project **in the correct order**. The planning/source layer is no longer missing obvious Graphify/GraphRAG/memory/runtime/project-transport families. Remaining source gaps are explicit, bounded, and not prerequisites for the current R1 execution gate.

The next legitimate product move remains whatever live canonical governance permits after R1 terminal evidence—not whichever external source looks most exciting.
