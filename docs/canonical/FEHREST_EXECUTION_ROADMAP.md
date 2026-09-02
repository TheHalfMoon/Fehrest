# Fehrest Execution Roadmap

**Status:** CANONICAL NAVIGATION / EXECUTION GUIDE  
**Purpose:** make the Fehrest program easy for a human or implementation agent to follow without weakening canonical governance.  
**Authority rule:** this roadmap organizes existing and future work; it does not bypass `specs/CURRENT.md`, evidence gates, active specifications, founder-decision gates, or exact-head review requirements.

> **Read this file for sequence. Read `specs/CURRENT.md` for what is executable now.**

---

## 1. North star

Fehrest is the durable project brain and governed work substrate that allows a fresh authorized human or agent to recover the right current context quickly, preserve project learning across disposable models/tools/runtimes, act under explicit authority, and prove what happened.

```text
AGENT_RUNTIME != MEMORY_OWNER
MODEL_PROVIDER != MEMORY_OWNER
IDE != MEMORY_OWNER
REPOSITORY != PROJECT_BRAIN
CANONICAL != DERIVED
EVIDENCE != AUTHORITY
MODEL_OUTPUT != FACT
RETRIEVAL_RANK != AUTHORIZATION
RECEIPT = EVIDENCE
RECEIPT != AUTHORITY
```

The product should remain local-first, AI-off capable, open-format, inspectable, recoverable, portable, and replaceable at every external-provider seam.

---

## 2. How an implementation agent must use this roadmap

At the start of every work session:

1. Fetch exact live `main` and repository governance.
2. Read `AGENTS.md`.
3. Read `specs/CURRENT.md`.
4. Read `docs/00-PRODUCT-THESIS.md` and `docs/01-ARCHITECTURE-CONSTITUTION.md` when architecture is relevant.
5. Read `docs/canonical/EXECUTION_MASTER_PLAN.md`.
6. Read this roadmap.
7. Read the active specification and its task ledger.
8. Inspect open PRs, required CI, reviews, review threads, and evidence gates.
9. Execute only the first dependency-ready task that is genuinely authorized.
10. After every merge or evidence transition, reread `specs/CURRENT.md` and canonical governance before selecting the next task.

Never infer implementation authority from a research document, donor study, roadmap phase, standing approval, issue label, or attractive architecture idea.

---

## 3. Program dependency chain

```text
R1 terminal evidence
        ↓
explicit post-R1 founder route decision when canonical governance requires it
        ↓
Phase 1 — Canonical Core
        ↓
Phase 2 — Derived Index / Lexical Convergence
        ↓
Phase 3A — Graph & Semantic Intelligence Experiment
        ↓
Phase 3B — Graph Integration ONLY if evidence retains it
        ↓
Phase 4 — Temporal Memory Productization
        ↓
Phase 5 — Context Compiler + Agent Gateway + Governed Capability Plane
        ↓
Phase 6 — Full Vertical Proof
        ↓
Phase 7+ — Product Surfaces, Collaboration, Automation, Broader Work OS
```

No later phase is executable merely because it appears here.

---

## 4. Phase 0 — Finish the active R1 thesis gate

### Objective

Complete the currently active R1 experiment without contaminating, scoring early, unblinding early, or mutating the sealed protocol.

### Entry gate

`specs/CURRENT.md` identifies R1 as active.

### Current critical path

```text
replacement variance pilot execution
→ raw seal
→ execution-integrity review
→ blinded pilot scoring
→ power analysis
→ computed confirmatory N
→ confirmatory manifest seal
→ confirmatory execution
→ raw seal
→ blinded scoring
→ scoring seal
→ unblind
→ terminal verdict
```

### Hard rules

- Native eligible Windows execution only where the sealed protocol requires it.
- Do not substitute WSL, Linux, or GitHub Actions for the required host.
- Do not fabricate runtime evidence.
- Do not score or unblind before the canonical gate.
- Preserve invalidated batches as invalidated evidence; never recycle them into scoring.
- Exact artifact identities and hashes must reconcile before closeout.

### Exit gate

A genuine canonical R1 terminal verdict exists and the post-verdict governance chain has completed.

---

## 5. Phase 1 — Canonical Core

### Objective

Build the smallest deterministic Fehrest core that can represent project truth without an LLM, vector database, graph database, remote service, or agent runtime.

### Required capability families

```text
Project identity
Canonical event/state model
Temporal/as-of semantics
Evidence references
Decision records
Authority/grant records
Work/task identity
Supersession/retraction
Deterministic projections
Open export/import format
Integrity verification
```

### Product test

A fresh machine with AI disabled can load a project, reconstruct current canonical state, inspect provenance, query historical/as-of state, and export/recover it deterministically.

### Donor use

Study Semantica for provenance, bitemporal facts, decision objects, ontology discipline, and conflict semantics. Do not let its graph or ontology become canonical authority by default.

### Exit gate

Canonical truth is deterministic, replayable, corruption-detectable, portable, and independent of derived intelligence providers.

---

## 6. Phase 2 — Derived Index / Lexical Convergence

### Objective

Make canonical state and project artifacts fast to navigate without introducing semantic infrastructure prematurely.

### Build order

```text
exact structured lookup
→ lexical/BM25 search
→ project-native structural summaries
→ deterministic ranking/fusion
→ scope and temporal filters
→ rebuild/reconciliation tooling
```

### Required properties

- Derived indexes are disposable and rebuildable.
- Index corruption cannot corrupt canonical state.
- Retrieval cannot expand authorization.
- Rebuild identity/version is recorded.
- Baseline latency, recall, footprint, and update cost are measured.

### Exit gate

A strong non-graph/non-vector baseline exists for later experiments.

---

## 7. Phase 3A — Graph & Semantic Intelligence Experiment

### Objective

Determine whether graph/semantic complexity earns its operational and cognitive cost.

### Hypotheses must be tested separately

```text
G1 structural code/project retrieval value
G2 temporal-memory graph value
G3 provenance/decision explanation value
G4 ontology/conflict-detection value
G5 graph build/rebuild/incremental/maintenance cost
```

### Comparator family

Use workload-appropriate subsets of:

```text
Fehrest Phase-2 baseline
Aider repo-map
Graphify
Code-Graph-RAG
Graphiti
Semantica
Microsoft GraphRAG
LightRAG
optional Fehrest-native tree-sitter path
```

### Decision rule

Retain only capabilities that materially improve real continuation, retrieval, explanation, conflict detection, or task outcomes under fair latency, token, memory, disk, rebuild, maintenance, security, and portability budgets.

### Exit gate

A written evidence-backed retain/reject decision exists for each graph capability. There is no requirement that Phase 3B happen.

---

## 8. Phase 3B — Graph Integration, only if retained

### Objective

Productize only the graph/semantic capabilities that survived Phase 3A.

### Hard boundaries

```text
GRAPH = DERIVED
ONTOLOGY != CANONICAL_AUTHORITY
INFERRED_FACT != CONFIRMED_FACT
GRAPH_PROVIDER = REPLACEABLE
```

### Exit gate

Retained graph capabilities rebuild from canonical/evidence sources, preserve provenance, and fail without damaging the AI-off core.

---

## 9. Phase 4 — Temporal Memory Productization

### Objective

Make Fehrest remember useful project knowledge across agents and sessions while knowing when remembered knowledge is stale, contradicted, superseded, or unsupported.

### Memory lifecycle

```text
experience / evidence / trajectory
→ candidate memory, procedure, decision, constraint, or gotcha
→ verification
→ durable project memory
→ use
→ source change / contradiction / feedback
→ revalidation / supersession / retraction / consolidation
```

### Memory classes

```text
Canonical Project Memory
Candidate Learning
Agent-local Harness State
Executable Skills / Procedures
Raw Trajectories
Derived Summaries
```

### Continual-learning law

```text
LEARNING_UPDATE_SMALL_AND_REVIEWABLE=YES
LEARNING_UPDATE_EVIDENCE_BACKED=YES
LEARNING_HISTORY_ROLLBACKABLE=YES
BASE_POLICY_NOT_SELF_REWRITABLE=YES
```

Prime Agent, Mem0, Letta, Graphiti, Hermes, and LongMemEval-style evaluations are references/comparators, not automatic dependencies.

### Exit gate

Fresh-agent continuation improves measurably without unacceptable stale-memory or unsupported-memory errors.

---

## 10. Phase 5 — Context Compiler + Agent Gateway + Governed Capability Plane

### Objective

Serve the right authorized project context and capabilities to many disposable agents/runtimes without letting any runtime own project memory or authority.

### Context compiler order

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
→ ContextReceipt
```

### Model-visible reconstruction law

Every load-bearing Fehrest-supplied model-visible input should be reconstructable from:

```text
durable source/event references
+ exact canonical high-water mark
+ compiler/transform identities
+ authorization binding
+ package digest
+ ContextReceipt
```

### Capability plane

A future `CapabilityLease` must bind at least:

```text
principal
agent/session
canonical grant digest
tool + operation
resource/filesystem/network/credential scopes
process/time/cost/output budgets
expiry
parent lease
policy identity
receipt policy
```

Required security properties:

- authenticated lease issuance;
- executor-side signature/authenticity and canonical-grant validation;
- atomic check-and-consume for expiry, budgets, and single-use constraints;
- fail closed when verification or enforcement storage is unavailable;
- subagent scope is subset-only;
- model/tool output cannot mint or expand authority;
- secrets do not enter model context by default.

### Agent interoperability

Pin exact protocol versions before implementation. MCP/ACP capability advertisement is not Fehrest authorization.

### Execution receipts

For every agent-visible or agent-triggered execution:

```text
DISPATCHED must be durably recorded before dispatch
STARTED must be durably recorded when execution begins
one durable terminal receipt must exist for every resolved outcome
```

If receipt persistence is unavailable before dispatch, do not dispatch. If durable terminal persistence fails after dispatch, record/reconcile the run as `INDETERMINATE`; never report success without a durable terminal receipt.

### Exit gate

At least two materially different agent runtimes can continue the same project through Fehrest with equivalent authority boundaries, reconstructable context, and auditable execution evidence.

---

## 11. Phase 6 — Full Vertical Proof

### Objective

Prove the complete Fehrest thesis end-to-end rather than validating isolated subsystems.

### Required scenario

A realistic project is imported or created, evolves over time, accumulates decisions/constraints/evidence, changes agents/runtimes, performs governed actions, survives stale/conflicting information, and is exported/recovered on a fresh environment.

### Required evaluation families

```text
fresh-agent continuation
LongMemEval-style temporal memory
SWE-bench-style repository work where applicable
plain competent agent + files baseline
maintained wiki baseline
Aider repo-map baseline
security/prompt-injection tests
multi-agent conflict tests
cross-runtime continuation
context latency/token/cost
import/export fidelity
backup/restore/corruption recovery
human approval friction
```

### Exit gate

Fehrest demonstrates measurable value over simpler baselines and preserves its security, portability, determinism, and recoverability claims.

---

## 12. Phase 7+ — Product Surfaces and AI-native Work OS

### Objective

Turn the proven project brain into a first-class human/agent work environment without making UI, chat, or hosted services the new source of truth.

### Candidate surfaces

```text
CLI
IDE integrations
Desktop
Web
MCP/ACP adapters
agent workspace
conversation/work channels
tasks/issues/reviews
attention inbox
project map/timeline
decision and evidence views
capability catalog
automation/schedules
multi-agent coordination
local-first collaboration
```

### Work-control lessons to evaluate

Paperclip and Multica are strong references for atomic task claims, heartbeats, budgets, approvals, agent coordination, and automation principal semantics.

Future automation must preserve:

```text
ONE_AUTOMATED_RUN = ONE_RESOLVED_PRINCIPAL
ADMISSION_PRINCIPAL == EXECUTION_PRINCIPAL
TERMINAL_RUN_CANNOT_START_NEW_PRIVILEGED_WORK
```

### Domain-app law

```text
DOMAIN_APP != MEMORY_OWNER
CHAT != CANONICAL_STATE
UI_STATE != CANONICAL_STATE
```

OpenSEO and World Monitor are useful references for agent-consumable domain applications and evidence/source-health surfaces; they are not Fehrest core templates.

---

## 13. External source adoption checklist

No external source becomes a production dependency or copied implementation until all applicable items are complete:

```text
[ ] A real requirement exists.
[ ] The simplest Fehrest-native option was evaluated.
[ ] Repository + immutable revision are pinned.
[ ] Exact copied/adapted paths are recorded.
[ ] License/SPDX/NOTICE/trademark obligations are verified path-by-path.
[ ] Dependency/SBOM delta is recorded.
[ ] Network/filesystem/secret behavior is reviewed.
[ ] Threat model impact is recorded.
[ ] Benchmark justification exists when load-bearing.
[ ] Failure/removal/escape path exists.
[ ] Active specification explicitly authorizes adoption.
[ ] Tests and cross-platform gates pass where applicable.
[ ] Independent exact-head review passes.
[ ] No unresolved actionable review thread remains.
```

```text
SOURCE_FOUND != SOURCE_ADMITTED
SOURCE_USEFUL != SOURCE_REQUIRED
COPYABLE != SHOULD_COPY
BENCHMARK_CANDIDATE != PRODUCTION_DEPENDENCY
```

---

## 14. Donor map for implementers

Use donors to answer bounded questions, not to choose Fehrest architecture by popularity.

| Need | First sources to study | What to extract | What not to inherit automatically |
|---|---|---|---|
| provenance / temporal semantics | Semantica, Graphiti | bitemporal facts, provenance, decisions, conflict semantics | graph as canonical truth |
| code/project structure | Graphify, tree-sitter, Aider | deterministic structure, repo-map baselines | heavy graph infra before benchmark |
| memory / continual learning | Prime Agent, Mem0, Letta, Hermes | lifecycle, refinement, rollback, long-running continuity | runtime-owned canonical memory |
| agent work control | Paperclip, Multica | atomic claims, heartbeats, budgets, approvals | vendor/runtime-specific authority |
| agent protocol boundaries | Buzz, MCP, ACP | protocol separation, permission lifecycle | protocol capability as authorization |
| execution security | ZeroClaw, Buzz, E2B, Daytona | sandbox/provider boundaries, process lifecycle, receipts | process hardening as sandbox proof |
| agent runtime architecture | DeepSeek Harness, Prime Agent | durable events, projections, capability seams, long-running sessions | donor framework as privileged core |
| local gateway / surfaces | OpenClaw, OpenWork | multi-surface gateway, portable capabilities | ambient host authority |
| evidence/source health | World Monitor | freshness, source health, last-good preservation | domain-specific product scope |
| domain apps | OpenSEO | human + MCP/skill surface | domain app owning project memory |
| simple baseline | OpenManus, mini-SWE-agent | understandable agent baseline | baseline limitations as Fehrest requirements |

Licensing details live in the dated source registry and donor study; always revalidate at adoption time.

---

## 15. Definition of Done for every implementation task

A task is not complete because code exists.

Unless the active specification says otherwise, completion requires applicable items below:

```text
[ ] canonical authority confirmed before work
[ ] exact task scope respected
[ ] implementation complete
[ ] tests added/updated
[ ] deterministic/local AI-off behavior preserved where required
[ ] security and authority boundaries tested
[ ] docs/contracts updated
[ ] provenance/license record updated for donor reuse
[ ] focused tests pass
[ ] full required CI passes on exact head
[ ] independent exact-head review completed
[ ] all actionable review threads resolved
[ ] guarded expected-head merge
[ ] post-merge verification
[ ] evidence/task ledger updated canonically
[ ] governance reread selects next dependency-ready task
```

Never mark a task, phase, benchmark, review, or project complete from intention or partial evidence.

---

## 16. Hermes handoff protocol

When Hermes is used as an implementation executor, give it the repository and instruct it to derive work from live canonical truth, not from a pasted stale task list.

Hermes must:

```text
1. inspect exact live main
2. read governance in the order in Section 2
3. state the active frontier and first dependency-ready task
4. refuse later-phase work when the active spec does not authorize it
5. work in a dedicated branch/worktree
6. make the smallest dependency-complete change
7. run required tests and CI
8. preserve donor provenance
9. never fabricate evidence/review/runtime results
10. stop only at a genuine external/evidence/authority gate; otherwise continue through authorized tasks
```

The next-chat founder prompt should therefore point Hermes at this roadmap **and** require live verification of `specs/CURRENT.md`. This prevents a clear roadmap from becoming stale authority.

---

## 17. Navigation index

Read these documents by purpose:

```text
What may execute now?
  specs/CURRENT.md

Repository operating law
  AGENTS.md

Product thesis
  docs/00-PRODUCT-THESIS.md

Architecture invariants
  docs/01-ARCHITECTURE-CONSTITUTION.md

Canonical dependency program
  docs/canonical/EXECUTION_MASTER_PLAN.md

Easy operator sequence
  docs/canonical/FEHREST_EXECUTION_ROADMAP.md

Whole-project readiness/gaps
  docs/research/FEHREST_FULL_PROJECT_REVIEW_2026.md
  docs/research/FEHREST_FULL_PRODUCT_GAP_ANALYSIS.md

Source and donor selection
  docs/research/FEHREST_SOURCE_READINESS_REGISTRY_2026.md
  docs/research/FEHREST_DONOR_BATCH_2026_09_02.md
  docs/research/BUZZ_DONOR_STUDY_AND_FEHREST_PLAN.md

Project substrate / memory direction
  docs/research/FEHREST_PROJECT_SUBSTRATE_AND_MEMORY_FABRIC.md

Market/product direction
  docs/research/FEHREST_PRODUCT_NORTH_STAR.md
  docs/research/FEHREST_2026_MARKET_EVIDENCE.md
```

---

## 18. Current authority statement

At creation of this roadmap:

```text
ROADMAP_RECORDED=YES
ROADMAP_AUTHORIZES_LATER_PHASES=NO
ACTIVE_EXECUTION_AUTHORITY=DEFER_TO_SPECS_CURRENT
R1_SEMANTICS_CHANGED=NO
PRODUCT_BEHAVIOR_CHANGED=NO
NEW_PRODUCTION_DEPENDENCY_ADMITTED=NO
```

If this roadmap ever conflicts with live canonical governance, **live canonical governance wins**.