# PR #27 Review Qualification Addendum

**Status:** NON-AUTHORIZING RESEARCH QUALIFICATION RECORD  
**Applies to:** PR #27 research/planning documents  
**Observed live operational base:** `c64fc4da82b665a40b27b4f4660cb7e64571e6d2`  
**PR head reviewed before this addendum:** `50229990fd8231cd71c5982796e993aebb552d1a`  
**Date:** 2026-09-02

## 1. Purpose and precedence

This addendum records the review-driven corrections required to interpret the research and planning material in PR #27 safely.

It does **not** amend `AGENTS.md`, `specs/CURRENT.md`, the sealed R1 protocol, the Architecture Freeze, or the Execution Master Plan. Where any research document in this PR appears to conflict with canonical governance, canonical governance wins.

Within the non-authorizing research material in PR #27, this addendum is the controlling interpretation for the findings below. Earlier broader wording remains preserved in Git history as review evidence; it must not be used to widen implementation authority.

```text
RESEARCH_FINDING != IMPLEMENTATION_AUTHORITY
DONOR_STUDY != DONOR_ADMISSION
PLANNED != AUTHORIZED
MODEL_CONTENT != AUTHORITY
RECEIPT != AUTHORITY
```

The live execution frontier at qualification time remains:

```text
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
NEXT_PRODUCT_SPEC=002-post-r1-canonical-core-convergence
NEXT_PRODUCT_SPEC_STATUS=BLOCKED_BY_R1_TERMINAL_GATE_AND_FOUNDER_AUTHORIZATION
```

No statement in PR #27 authorizes Phase 1 or later product implementation while `specs/CURRENT.md` remains in that state.

---

## 2. Donor-freeze correction

The frozen donor-research rule remains in force.

A founder-supplied repository or an interesting architectural resemblance is not, by itself, a qualifying gap-driven trigger. New donor research may become load-bearing only when the canonical change-control path records an allowed trigger, such as a measured benchmark failure, a security finding, a missing open-source equivalent for an already-authorized requirement, or a new platform-correctness requirement.

Therefore:

```text
BUZZ_STUDY_STATUS=DEFERRED_RESEARCH_LEAD
NEW_2026_DONOR_BATCH_STATUS=DEFERRED_RESEARCH_LEADS
UNGATED_COMPARATOR_EXPANSION=NO
PRODUCTION_DEPENDENCY_ADMISSION=NO
```

Buzz, Semantica, Microsoft GraphRAG, LightRAG, tree-sitter, Paperclip, Multica, Prime Agent, DeepSeek Harness, ZeroClaw, OpenClaw, OpenWork, World Monitor, OpenManus, OpenSEO, and any other newly surfaced source in this PR must not enter a required comparator set, production dependency set, or copied implementation path unless a valid canonical trigger and active specification authorize that use.

The frozen Phase 3A comparator family remains the canonical default until changed through the required review path:

```text
Fehrest lexical/structured/temporal baseline
Graphify
Code-Graph-RAG
Graphiti where workloads match temporal-context-graph semantics
```

Additional systems are optional deferred candidates, not required comparators.

---

## 3. Buzz evidence-status correction

The Buzz repository revision remains pinned for research traceability:

```text
repository=block/buzz
revision=1c8321cd08feb597f8bcff5195c21148fb3e98ed
```

However, PR #27 did not preserve a complete claim-level evidence ledger containing exact source path, symbol, blob identity, inspection command, and observed result for every concrete Buzz implementation statement.

Accordingly, every concrete Buzz implementation claim that lacks those fields is downgraded to:

```text
CLAIM_STATUS=UNVERIFIED_PLANNING_HYPOTHESIS
LOAD_BEARING=NO
IMPLEMENTATION_JUSTIFICATION=NO
```

Before any Buzz-derived requirement or implementation reuse becomes load-bearing, the adopting specification must record at minimum:

```text
upstream repository
immutable revision
exact source/test path
symbol or bounded line range
blob identity when available
inspection command or equivalent reproducible method
observed result
claim status
license/NOTICE review for the exact reused path
Fehrest requirement that motivated the inspection
```

No future implementation may cite the narrative donor study alone as proof that Buzz enforces a property.

---

## 4. Capability-lease qualification contract

Any future capability-lease design is valid only if the active specification explicitly authorizes it. If/when authorized, the following security properties are mandatory minimums.

### 4.1 Authenticated issuance and live verification

A lease must be core-issued or otherwise cryptographically/authentically bound to canonical authority. Every execution must validate:

```text
lease authenticity
canonical_grant_digest
live originating session grant
current lease validity
complete parent-lease chain
policy identity
expiry
single-use state where applicable
all applicable budgets
claim/fencing generation where applicable
```

Cancellation, exhaustion, revocation, or supersession of a parent session/lease immediately invalidates and fences every descendant.

A cached derived lease is never independent authority.

### 4.2 Executor enforcement declaration

Every executor must declare, in machine-verifiable form, which restriction dimensions it can actually enforce for the effective runtime profile.

At minimum the declaration covers:

```text
filesystem scope
resource/object scope
network/egress scope
credential injection/use scope
process-tree scope
time limits
cost/resource budgets
output limits
isolation class
```

The core must reject a lease when the selected executor cannot enforce **every requested restriction dimension**. A process-lifecycle-hardened native executor must not be represented as a security sandbox.

### 4.3 Atomic reservation and check-and-consume

Admission must use a core-owned atomic operation that checks and consumes/reserves all applicable constraints together, including project/workspace/task/session/agent/time-window ancestor budgets and single-use constraints.

Concurrent children must not each pass a local budget check and collectively overspend a shared cap.

Actual cost must be settled against the reservation. Unknown or delayed provider cost fails closed or remains conservatively reserved according to an explicitly versioned policy.

Enforcement-store failure is a denial, not a reason to execute optimistically.

### 4.4 Secrets

```text
RAW_SECRET_IN_MODEL_CONTEXT=NO
RAW_SECRET_IN_MEMORY=NO
RAW_SECRET_IN_TRAJECTORY=NO
RAW_SECRET_IN_EVENT_DETAIL=NO
RAW_SECRET_IN_LOG=NO
```

Only opaque credential references/classes may cross the model-facing boundary. Secret values may be injected only inside the qualified executor boundary under an authorized credential scope and must remain excluded from model-visible output.

---

## 5. Execution-receipt qualification contract

For every Fehrest agent-visible or agent-triggered external execution, a durable lifecycle is required.

```text
PREPARED
→ DISPATCHED
→ STARTED
→ terminal receipt
```

`DISPATCHED` is a durable pre-dispatch intent/admission record written **before** the external request can escape the Fehrest boundary.

Every dispatch attempt must carry a unique immutable `attempt_id` plus a monotonic fencing/admission identity into the executor/provider request. Recovery after a crash between `DISPATCHED` and `STARTED` must not blindly retry. Retry is permitted only when the provider/executor supports idempotent admission keyed by that attempt identity or when explicit reconciliation proves that no prior side effect occurred. Otherwise the run becomes `INDETERMINATE` until reconciled.

If durable receipt storage is unavailable before dispatch, do not dispatch.

If persistence fails after dispatch:

```text
REPORT_SUCCESS=NO
AUTO_REPLAY_NON_IDEMPOTENT=NO
STATE=INDETERMINATE_UNTIL_RECONCILED
```

A terminal success may be reported only after its durable terminal receipt exists.

### 5.1 Runtime provenance

The execution receipt must bind materially relevant runtime identity, not only a provider/tool display name. It includes or digests at minimum:

```text
immutable tool/server revision and effective configuration
executor implementation revision
runtime artifact/container/WASI/module/binary identity
host platform/architecture where relevant
isolation-policy/profile identity
which lease dimensions were actually enforced
request/argument digest
principal/session/lease binding
attempt/fencing identity
```

A provider name that can point to different binaries/configurations is insufficient for replay/audit classification.

---

## 6. Work-claim fencing

Future multi-agent task claims require a monotonically increasing claim generation or fencing token.

When claim generation `N+1` supersedes generation `N`, any later patch, receipt, canonical mutation, or external side effect submitted under generation `N` must be rejected at the authoritative acceptance/execution chokepoint.

Single-writer serialization alone does not solve stale-owner execution.

---

## 7. High-influence memory promotion

Typed domain state machines, not a generic object lifecycle, own promotion rules.

Candidate memories that can influence authority, decisions, constraints, preferences, procedures, or other high-impact project behavior remain non-authoritative until the domain-specific human gate required by canonical security/threat invariants has completed.

```text
AUTOMATED_CORROBORATION != HUMAN_CONFIRMATION
AGENT_DERIVED_DECISION != CANONICAL_DECISION
AGENT_DERIVED_CONSTRAINT != CANONICAL_CONSTRAINT
```

Verification/corroboration may improve evidence quality but must not bypass mandatory human confirmation.

The shared object envelope may carry generic archival/deletion metadata, but domain lifecycle states remain typed and separately authorized.

---

## 8. Model-visible context qualification

By the Phase 5 gate, **every Fehrest-produced model-visible package** must be reconstructable and auditable. There is no `load-bearing` exemption.

Each package binds:

```text
request identity/digest
principal/session/grant binding
canonical high-water mark
source/event/object references
compiler/policy/transform identities
derived-generation bindings where used
emitted content/package digest
ContextReceipt
```

Search results, tool-read packages, summaries, auxiliary snippets, and any other Fehrest-produced model-visible payload are included.

---

## 9. Automation authority preservation

A trigger is never authority.

Every scheduled/conditional automation must preserve its originating creator principal and an explicit delegated automation sub-scope that is a subset of that principal's live canonical authority.

```text
ONE_AUTOMATED_RUN = ONE_RESOLVED_PRINCIPAL
ADMISSION_PRINCIPAL == EXECUTION_PRINCIPAL
TRIGGER_EDIT != AUTHORITY_TRANSFER
```

Editing schedule/trigger configuration does not transfer authority ownership. A future run must re-resolve the originating principal and delegated sub-scope against live canonical authority; expired/revoked/superseded authority fails closed.

---

## 10. Project-substrate portability and recovery corrections

### 10.1 Dirty working state is irreplaceable unless captured

A clean checkout and index state derivable from preserved Git objects are rebuildable. Uncommitted working-tree bytes, staging/index deltas, untracked files, local patches, unresolved merge state, and other unpublished work are not derivable from repository history and must be treated as irreplaceable capsule data when the user asks for complete project preservation.

A capsule/export that does not capture those bytes/states must fail closed for a `COMPLETE` claim or declare an explicit `INCOMPLETE_DIRTY_STATE` status.

### 10.2 External Git/LFS/submodule payload completeness

Gitlinks and LFS pointer blobs are not the referenced source payload.

For every resolved submodule/LFS/external Git payload needed for an offline-complete capsule, preserve a rooted/canonical source identity, exact resolved revision/content digest, size, and content-addressed payload. If payload bytes are intentionally unavailable or external, record that fact explicitly and prohibit a `FULLY_RECONSTRUCTIBLE_OFFLINE` claim.

Relative workspace-only paths are insufficient for external repositories located outside the project root.

### 10.3 Publish authority binds destination and payload

Any future publish grant must bind and later revalidate:

```text
canonical provider
account/principal
repository identity
normalized endpoint
exact destination ref
operation class
force/update policy
exact object-set/patch/content digest
```

Remote renaming/reconfiguration between approval and execution must invalidate the operation unless the bound canonical destination identity remains equivalent under an explicit verified rule.

### 10.4 Immediate invalidation quarantine

When upstream change or contradiction invalidates an active memory/procedure/decision, the object enters `PENDING_REVALIDATION` (or an equivalent typed suspect state) immediately and is excluded from ordinary active context before human review completes. The original historical object remains preserved for audit.

### 10.5 Self-contained semantic export

A semantic export must carry a content-addressed transitive-closure manifest. All permitted canonical targets referenced by evidence/source/supersession/invalidation/decision/scope/receipt/attachment relationships must either be included by immutable identity or explicitly classified as intentionally external/unavailable.

Round-trip fidelity tests must reject silent dangling references.

### 10.6 Recovery freshness and rollback detection

Backups/capsules require monotonic backup generation plus canonical/event high-water marks. Restore must compare against an independently retained expected head when one exists.

If a fresh device cannot establish whether a self-consistent capsule is the latest generation, the system must surface `FRESHNESS_UNVERIFIED` and require explicit acknowledgement before representing the restore as current.

No derived index may expose canonical state beyond the restored canonical/event frontier. Derived rows beyond the frontier are invalidated/rebuilt.

### 10.7 Cold/rebuild context SLOs

Warm-state latency alone is insufficient. Future acceptance tests must measure at least:

```text
first import
cold start
missing/corrupt derived index
incremental backlog
schema upgrade
restore on a fresh device
rebuild under load
```

Measure time to the first provenance-complete degraded context as well as full rebuild completion. If no safe canonical/derived generation can answer, fail closed rather than serving an unmarked stale generation.

---

## 11. Historical-source reconciliation

The previously described historical research files are not unavailable. The verified historical object graph is reachable at `historical/r1-v1.1` and contains:

```text
docs/research/EVIDENCE_LOG.md
blob=ca4f101532d57508ec9d63c9c866bab3cc22ed3d
status=CANONICAL MEASUREMENT RECORD (historical R1 source)

docs/research/FEHREST_SOURCE_REGISTRY.md
blob=8f5535b7e1435590cea487e678ed62e86a29f66f
status=CANONICAL RESEARCH REGISTRY (historical R1 source)
```

These bytes are reconciled into the 2026 review as **historical evidence**, not as a replacement for live operational truth. Their historical claims remain bound to their own verification dates, corrections, and evidence identifiers. Current decisions must still reverify stale load-bearing external-source facts before use.

The earlier PR narrative that these bytes were not currently present in the GitHub mirror is therefore superseded by this reconciliation record.

---

## 12. Phase-6 transport/order correction

The Execution Master Plan remains authoritative for phase order.

If the Phase 6 vertical proof requires project import/export, fresh-device capsule restoration, or Git transport fidelity as a required gate, then the bounded specification and implementation necessary for that trial must be authorized and completed **before** the Phase 6 trial executes. It must not be deferred until a later Phase 7+ product-surface specification.

Conversely, if canonical governance keeps a transport/capsule subsystem deferred, Phase 6 must not claim that subsystem's fidelity as a required proof gate.

No research document in PR #27 may silently reorder this dependency.

---

## 13. Market-evidence immutability correction

Mutable vendor/product/index/landing pages in `FEHREST_2026_MARKET_EVIDENCE.md` are classified as:

```text
DISCOVERY_LEAD_ONLY
LOAD_BEARING=NO
```

A future decision may rely on such a source only after preserving immutable identity sufficient to reconstruct what was observed, for example:

```text
immutable commit/version/permalink when available
or archived snapshot/content-addressed capture
content digest
retrieved_at/observed_at timestamp
source status
verification method
```

A mutable root URL plus a later verification date is not reproducible evidence of what the page said on 2026-09-02.

---

## 14. Qualification checklist for PR #27

PR #27 may be called qualified only when all of the following are true on one exact head:

```text
[ ] canonical roadmap follows AGENTS.md mandatory read order
[ ] roadmap preserves live R1 blocking state
[ ] Phase 1 contains only work authorized by canonical Phase 1 / Spec 002
[ ] ungated new donors are deferred, not required comparators/dependencies
[ ] high-influence memory promotion retains required human confirmation
[ ] every Fehrest-produced model-visible package is receipted by the Phase 5 gate
[ ] lease execution requires per-dimension enforceability and live parent-chain validation
[ ] raw secrets are unconditionally excluded from model-visible context/log/memory/trajectory
[ ] dispatch/retry semantics are crash-safe and fenced
[ ] automation preserves originating authority
[ ] research evidence-status corrections above are incorporated into review disposition
[ ] current CI/checks pass on the exact head
[ ] independent exact-head review has completed
[ ] no unresolved actionable review thread remains
```

Until those conditions are evidenced, the PR is a candidate under review, not a qualified canonical change.
