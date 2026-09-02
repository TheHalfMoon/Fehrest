# Fehrest Execution Roadmap

**Status:** CANONICAL NAVIGATION / EXECUTION GUIDE  
**Purpose:** provide one dependency-ordered execution map that is easy for a human or implementation agent to follow without weakening repository governance.  
**Current live frontier at this revision:** `R1 / REPLACEMENT_VARIANCE_PILOT_EXECUTION`  
**Authority rule:** this file never authorizes work by itself.

> Read this file for sequence only. Read `specs/CURRENT.md` and the active Spec Kit for what is executable now.

---

## 1. Authority boundary

```text
LIVE_REPOSITORY_TRUTH > HANDOFF
CURRENT_FRONTIER > ROADMAP
ACTIVE_SPEC > FUTURE_PLAN
PLANNED != AUTHORIZED
RESEARCH != AUTHORITY
DONOR_STUDY != DEPENDENCY_ADMISSION
RECEIPT = EVIDENCE
RECEIPT != AUTHORITY
MODEL_CONTENT != AUTHORITY
CANONICAL != DERIVED
```

At this revision:

```text
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
NEXT_PRODUCT_SPEC=002-post-r1-canonical-core-convergence
NEXT_PRODUCT_SPEC_STATUS=BLOCKED_BY_R1_TERMINAL_GATE_AND_FOUNDER_AUTHORIZATION
```

No Phase 1+ product implementation may begin while live canonical governance still reports that block.

---

## 2. Mandatory startup sequence

`AGENTS.md` is the mandatory entry point.

Before changing anything, an implementation agent must read the live repository in the order required by `AGENTS.md`:

1. `specs/CURRENT.md`
2. `docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md`
3. `docs/canonical/EXECUTION_MASTER_PLAN.md`
4. the active or next Spec Kit named by `specs/CURRENT.md`
5. `README.md`
6. relevant reconciled architecture/security/benchmark documents required by the active task

Then inspect:

```text
exact main SHA
working branch/head SHA
open pull requests
required CI/status checks
submitted reviews
all unresolved review threads
active issues/evidence gates
exact task ledger for the active frontier
```

Only after that may the agent select the first dependency-ready task that is genuinely authorized.

After every merge, evidence transition, task closeout, or frontier change, repeat the governance read before selecting successor work.

---

## 3. Program dependency chain

```text
R1 terminal evidence
        ↓
explicit post-R1 founder route decision where canonical governance requires it
        ↓
Phase 1 — Canonical Core Convergence
        ↓
Phase 2 — Derived Index / Lexical Retrieval Convergence
        ↓
Phase 3A — Graph Intelligence Capability Experiment
        ↓
Phase 3B — Optional Graph Integration, only if retained
        ↓
Phase 4 — Temporal Memory Productization
        ↓
Phase 5 — Full Context Compiler + Agent Gateway
        ↓
Phase 6 — Full Vertical Proof
        ↓
Phase 7 — Product Surfaces, only after proof and authorization
```

No later phase is executable because it is documented here.

---

## 4. Current gate — finish R1 without semantic drift

### Objective

Complete the sealed R1 experiment in canonical order without mutating sealed semantics or fabricating runtime evidence.

### Critical path

The exact active sub-gate comes from `specs/CURRENT.md` and the active R1 runbooks. The canonical experiment order remains:

```text
valid replacement variance pilot execution
→ raw evidence seal
→ execution-integrity review
→ blinded pilot scoring when separately authorized
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

- Use the host/runtime required by the sealed protocol.
- Do not substitute WSL, Linux, GitHub Actions, another model condition, another seed, another corpus, or another arm where the sealed protocol requires something else.
- Do not infer success from executor qualification or zero exit code.
- Do not fabricate execution evidence.
- Do not score, unblind, or run confirmatory work before its canonical gate.
- Preserve invalidated batches as invalidated evidence.
- Reconcile exact artifact identities and hashes before any gate closeout.

### Exit

A genuine terminal R1 verdict exists, is recorded canonically, and every required post-verdict founder/governance gate has completed.

---

## 5. Phase 1 — Canonical Core Convergence

**Spec Kit:** `002-post-r1-canonical-core-convergence`  
**Status at this revision:** PREPARED / BLOCKED

### Objective

Turn already-proven canonical mechanisms into a production-grade core without expanding agent-facing authority or derived intelligence.

### Scope after activation

Phase 1 follows the Execution Master Plan and active Spec 002 only. Its dependency-complete capability family includes:

```text
Phase T truth reconciliation
vault identity / format / schema version
atomic and crash-aware canonical replacement
explicit persistence boundary
unsupported-filesystem failure visibility
writer-owned canonical mutation boundary
versioned event envelope
typed event payloads
contiguous sequence + honest hash chain
explicit flush/sync boundary
torn-tail detection/quarantine
mid-log gap and chain-break fail-closed behavior
schema upcasting skeleton
golden old-version fixtures
recovery evidence
```

The following are **not** Phase 1 merely because later architecture needs them:

```text
agent grants / capability leases
MCP/ACP gateway
automation principals
production graph integration
vector default
automatic memory
UI
```

### Exit

Canonical loss under the required fault matrix is zero and all required security/path/identity/resource invariants remain green.

---

## 6. Phase 2 — Derived Index / Lexical Retrieval Convergence

### Objective

Make derived lexical/index state disposable, incremental, deterministic, and independently rebuildable.

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

Hard rules:

```text
DERIVED != AUTHORITY
DERIVED_PATH != FILESYSTEM_AUTHORITY
INDEX_CORRUPTION != CANONICAL_CORRUPTION
REBUILD_IDENTITY_IS_RECORDED=YES
```

Aider repo-map remains a strong simple baseline for code/project workloads where the governing benchmark/specification already authorizes it. Vector systems remain optional future candidates, not defaults.

### Exit

A strong non-graph baseline exists with measured quality, latency, footprint, update cost, and rebuild behavior.

---

## 7. Phase 3A — Graph Intelligence Capability Experiment

### Objective

Determine whether graph complexity materially improves Fehrest outcomes before building production graph infrastructure.

### Frozen comparator family

Use only the comparator set already permitted by canonical freeze/governance unless a valid gap-driven change is recorded:

```text
Fehrest lexical/structured/temporal baseline
Graphify
Code-Graph-RAG
Graphiti where temporal-context-graph semantics match the workload
```

```text
NEW_DONOR_FOUND != COMPARATOR_REQUIRED
DONOR_DISCOVERY_FROZEN=YES
```

Any future donor research itself requires a valid gap-driven trigger before it is conducted or landed in canonical planning. Appearance in chat, founder brainstorming, or external popularity is not sufficient.

Measure task/continuation quality, retrieval quality, build/incremental cost, memory/disk footprint, context tokens, latency, and API cost where applicable.

### Exit

A written evidence-backed retain/reject decision exists. If graph adds no material value at acceptable cost, Phase 3B is skipped.

---

## 8. Phase 3B — Optional Graph Integration

Entry requires Phase 3A to retain a graph capability.

```text
GRAPH = DERIVED
EXTERNAL_GRAPH_ID != FEHREST_IDENTITY
GRAPH_PATH != FILESYSTEM_AUTHORITY
GRAPH_RANK != AUTHORIZATION
GRAPH_BYTES = DISPOSABLE
```

Implement only the smallest replaceable provider boundary required by measured needs.

---

## 9. Phase 4 — Temporal Memory Productization

### Objective

Productize durable project memory while preventing stale, contradicted, or agent-inferred content from becoming silent authority.

A generic candidate flow is insufficient for high-influence objects. Domain/type-specific state machines own promotion.

```text
low-risk candidate
→ evidence verification/corroboration
→ domain-specific promotion gate
→ durable state

high-influence decision / constraint / preference / procedure candidate
→ evidence verification/corroboration
→ PENDING
→ explicit required human confirmation
→ durable active state
```

Hard rules:

```text
AUTOMATED_CORROBORATION != HUMAN_CONFIRMATION
AGENT_DERIVED_DECISION != CANONICAL_DECISION
AGENT_DERIVED_CONSTRAINT != CANONICAL_CONSTRAINT
TRAJECTORY != MEMORY
SUMMARY != CANONICAL_MEMORY
```

Source changes, contradictions, or invalidation immediately move affected active objects into a typed suspect / `PENDING_REVALIDATION` state that is excluded from ordinary active context until revalidated.

---

## 10. Phase 5 — Full Context Compiler + Agent Gateway

This phase owns the production context compiler and authorization gateway. It is not part of Phase 1.

### Deterministic compiler

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

### Model-visible package law

By the Phase 5 gate, **every Fehrest-produced model-visible package MUST have a permanent receipt and served-item manifest** sufficient to audit exactly what Fehrest attempted to supply and under which authority/policy state.

Each receipt/manifest binds at minimum:

```text
request identity/digest
principal/session/grant binding
canonical high-water mark
source/event/object references
compiler/policy/transform identities
derived-generation bindings where used
package/content digest when retained
served-item identities/digests
ContextReceipt
```

Exact content reconstruction is conditional on the referenced source revision/body still being retained and permitted by canonical retention rules. When exact reconstruction is impossible, replay MUST return an explicit `UNRECONSTRUCTABLE` result rather than fabricating or silently substituting content.

There is no exemption for search results, tool reads, summaries, auxiliary snippets, or other Fehrest-produced model-visible payloads from the permanent receipt/manifest requirement.

### Capability-lease security contract

If an active specification authorizes a `CapabilityLease`, it must bind at least:

```text
principal
agent/session
canonical grant digest
tool + operation
resource/filesystem/network/credential/process scopes
cost/time/output/resource budgets
expiry
parent lease
policy identity
receipt policy
claim/fencing generation where applicable
```

At issuance, every descendant lease MUST be a monotonic attenuation of every ancestor across all authority dimensions. It may narrow tool/action, filesystem, network, credential, process, budget, time, and resource scope; it may never widen any dimension.

Every execution must:

1. verify lease authenticity and the canonical grant digest;
2. revalidate the live originating session and the complete live parent chain;
3. revalidate per-dimension attenuation against every parent in that chain;
4. reject descendants immediately when any parent is cancelled, exhausted, revoked, superseded, or no longer contains the child scope;
5. use a core-owned atomic check-and-reserve/check-and-consume across all applicable ancestor budgets and single-use constraints;
6. require the selected executor to declare enforceability per requested restriction dimension;
7. reject the lease when the executor cannot enforce every requested restriction;
8. fail closed when the enforcement store is unavailable.

```text
PROCESS_LIFECYCLE_HARDENED != SECURITY_SANDBOXED
```

### Secrets

Raw secrets never enter model-visible context, memory, trajectories, event detail, or logs.

Only opaque credential references/classes may reach the model-facing boundary. Secret material may be injected only inside the qualified executor boundary under a valid credential scope.

### Execution receipts and crash fencing

Every agent-visible or agent-triggered external execution uses a durable lifecycle:

```text
PREPARED
→ DISPATCHED   # durable pre-dispatch intent
→ STARTED
→ terminal receipt
```

No dispatch occurs if durable receipt storage is unavailable.

Every dispatch carries a unique immutable attempt identity plus the required fencing/admission identity into the executor/provider request. A crash after `DISPATCHED` and before `STARTED` does **not** permit blind retry. Retry requires idempotent admission keyed by the attempt identity or explicit reconciliation proving no prior side effect. Otherwise the result is `INDETERMINATE` until reconciled.

A durable terminal receipt binds materially relevant runtime provenance, including immutable tool/server revision/configuration, executor revision, runtime artifact, platform where relevant, isolation-policy identity, and the lease dimensions actually enforced.

Success is never reported without a durable terminal receipt.

---

## 11. Phase 6 — Full Vertical Proof

### Objective

Prove the complete Fehrest thesis end-to-end before UI/product-surface expansion.

Use preregistered applicable baselines and freeze the evaluation before tuning.

Required proof families may include:

```text
fresh-agent continuation
LongMemEval-style temporal memory
repository work where applicable
plain competent agent + files
strong repository-native documentation
Aider repo-map
security / prompt-injection
cross-runtime continuation
multi-agent conflict/fencing
context latency/token/cost
backup/restore/corruption recovery
human approval friction
```

If the vertical proof requires Git import/export, project-capsule restore, or fresh-device transport fidelity, the bounded specification and implementation needed for that trial must be authorized and completed **before** the trial. A subsystem may not be deferred to Phase 7 while simultaneously being required to pass Phase 6.

Do not build a sandbox platform merely to run the proof; qualify/adapt a provider only when the active specification authorizes it.

### Exit

Fehrest demonstrates measurable value over strong simpler baselines while preserving security, portability, determinism, and recoverability. If the defining proof fails its preregistered criteria, do not route around it by starting UI work.

---

## 12. Phase 7 — Product surfaces

Hard entry requires the canonical Phase 6 proof gate plus any editor/founder authorization required by live governance.

The UI remains presentation. Headless Rust Core remains authoritative.

Potential surfaces such as CLI, IDE, desktop, web, MCP/ACP adapters, collaboration, schedules, and automation are future work only when explicitly authorized.

### Automation authority law

A trigger is never authority.

Every scheduled/conditional run preserves the originating creator principal and an explicit delegated automation sub-scope that is a subset of that principal's live canonical authority.

```text
ONE_AUTOMATED_RUN = ONE_RESOLVED_PRINCIPAL
ADMISSION_PRINCIPAL == EXECUTION_PRINCIPAL
TRIGGER_EDIT != AUTHORITY_TRANSFER
TERMINAL_RUN_CANNOT_START_NEW_PRIVILEGED_WORK
```

Editing trigger/schedule configuration does not transfer authority. Each future run re-resolves the originating principal and delegated scope against live canonical state and fails closed when authority has expired, been revoked, or been superseded.

---

## 13. Donor and adoption discipline

The Architecture Freeze remains controlling.

New donor research itself requires a valid gap-driven trigger before investigation begins or research bytes are landed in canonical planning.

If a valid trigger exists, record it before research. Before any external implementation becomes load-bearing or is copied/adopted, the active specification must also record as applicable:

```text
trigger identity and change-control class
real authorized requirement
simplest Fehrest-native option considered
immutable upstream revision
exact reused/adapted paths
claim-level evidence when architecture behavior is load-bearing
license/SPDX/NOTICE/trademark review
security/dependency/SBOM impact
benchmark justification where load-bearing
failure/removal path
cross-platform gates where applicable
independent exact-head review
```

```text
SOURCE_FOUND != SOURCE_ADMITTED
SOURCE_USEFUL != SOURCE_REQUIRED
COPYABLE != SHOULD_COPY
BENCHMARK_CANDIDATE != PRODUCTION_DEPENDENCY
```

---

## 14. Project portability and recovery invariants

Any future complete project capsule/export must preserve irreplaceable unpublished state, not merely Git-reconstructible state.

```text
clean checkout/index derivable from preserved objects = rebuildable
uncommitted bytes/staging deltas/untracked files/local patches = irreplaceable unless captured
```

Submodules, Git LFS payloads, and external Git repositories require resolved revision/content identity plus content payload for an offline-complete claim, or an explicit incomplete/external classification.

Semantic export must preserve a content-addressed transitive closure of permitted canonical references or explicitly classify intentionally external/unavailable targets.

Backups require monotonic generation/high-water marks and rollback/freshness detection. A self-consistent older backup must not be silently represented as current.

Cold-start, restore, missing-index, schema-upgrade, backlog, and rebuild-under-load paths require explicit SLOs in the specification that owns them.

---

## 15. Definition of Done

A task is not complete because code or documentation exists.

Unless the active specification says otherwise, applicable completion evidence includes:

```text
[ ] live canonical authority reverified before work
[ ] first dependency-ready authorized task selected
[ ] scope stayed inside active frontier/spec
[ ] implementation/documentation complete
[ ] focused tests/checks pass
[ ] full required CI passes on exact head
[ ] security/authority invariants verified
[ ] provenance/license evidence recorded where applicable
[ ] independent exact-head review completed
[ ] every actionable review thread resolved
[ ] guarded expected-head merge when separately authorized
[ ] post-merge verification
[ ] owning task/evidence ledger updated only after evidence exists
[ ] governance reread selects the next authorized dependency
```

Never claim PASS, QUALIFIED, MERGED, CLOSED, or COMPLETE without exact evidence.

---

## 16. Hermes execution protocol

When Hermes executes Fehrest work, it must derive the task from **live repository truth**, not from a pasted stale task list.

Hermes must:

1. verify exact live `main`, current branch, open PRs, CI, reviews, review threads, and issues;
2. read `AGENTS.md`, then follow its mandatory file order exactly;
3. state the active frontier and first dependency-ready authorized unit;
4. refuse Phase 1+ implementation while R1 remains open/blocked;
5. use a dedicated branch/worktree for implementation work;
6. make the smallest dependency-complete change;
7. run required local gates and exact-head CI;
8. preserve sealed R1 evidence and historical identifiers exactly;
9. obey the donor-research freeze and preserve provenance for any already-authorized source use;
10. never fabricate runtime evidence, qualification, review, authority, or completion;
11. resolve review findings only after verifying the current head actually addresses them;
12. after each completed unit, reread live governance and continue only to the next genuinely authorized dependency.

The current Hermes starting point is the live R1 replacement-variance-pilot frontier, **not** Spec 002 implementation, unless `specs/CURRENT.md` has changed by the time Hermes starts.

---

## 17. Fast navigation index

```text
What may execute now?
  specs/CURRENT.md

Repository operating law
  AGENTS.md

Bootstrap/provenance constraints
  docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md

Canonical program order
  docs/canonical/EXECUTION_MASTER_PLAN.md

Easy dependency map
  docs/canonical/FEHREST_EXECUTION_ROADMAP.md

Active implementation detail
  the active Spec Kit named by specs/CURRENT.md

Architecture/security/benchmark details
  read only the reconciled documents required by the active task
```

---

## 18. Current authority statement

At this roadmap revision:

```text
ROADMAP_RECORDED=YES
ROADMAP_AUTHORIZES_LATER_PHASES=NO
ACTIVE_EXECUTION_AUTHORITY=DEFER_TO_SPECS_CURRENT_AND_ACTIVE_SPEC
R1_SEMANTICS_CHANGED=NO
PRODUCT_BEHAVIOR_CHANGED=NO
NEW_PRODUCTION_DEPENDENCY_ADMITTED=NO
UNGATED_DONOR_RESEARCH_ADMITTED=NO
```

If this roadmap ever conflicts with live canonical governance, **live canonical governance wins**.