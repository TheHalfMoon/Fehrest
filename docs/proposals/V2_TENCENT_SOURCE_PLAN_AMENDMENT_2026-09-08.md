# Fehrest V2 Plan Amendment — Tencent Source Convergence — 2026-09-08

**Status:** PLAN AMENDMENT / NON-AUTHORIZING  
**Applies to:** future V2 proposal and any later canonicalization of PR #2  
**Execution effect:** NONE while R1 remains open  
**Canonical frontier:** live `specs/CURRENT.md`  
**Source qualification:** `docs/research/TENCENT_SOURCE_QUALIFICATION_2026-09-08.md`  
**Gap review:** `docs/reviews/V2_TENCENT_SOURCE_GAP_REVIEW_2026-09-08.md`

> This amendment improves the future Fehrest V2 plan using lessons from Tencent/RoMem, Tencent/WeKnora and Tencent/SkillHone while explicitly refusing donor-driven scope expansion. It does not alter the frozen R1-v2 review candidate, authorize sealing/execution, activate Spec 002, authorize product implementation, or merge PR #2.

## 1. Planning decision

The three sources do not justify adding three new subsystems. They expose missing contracts in the existing plan.

The improved program rule is:

```text
USE DONORS TO SHARPEN CONTRACTS
NOT TO MULTIPLY PLATFORMS
```

Therefore:

```text
NEW_TOP_LEVEL_SPEC_IDS=0
EXISTING_SPEC_SEQUENCE_RETAINED=YES
R1_GATE_RETAINED=YES
PR_2_REMAINS_DRAFT_NON_AUTHORIZING=YES
```

## 2. New program invariants to carry into future V2 reconciliation

Any future canonicalization of the V2 proposal MUST preserve these additional invariants unless a separately authorized architecture/security decision explicitly supersedes them.

### P-TS-01 — Temporal rank is never canonical truth

```text
TEMPORAL_RANK != TEMPORAL_TRUTH
DERIVED_VOLATILITY != VALIDITY_INTERVAL
RERANKER_OUTPUT != SUPERSESSION
```

Canonical current/as-of truth is determined by Fehrest-owned temporal/provenance semantics. Temporal ML/graph signals may only rank already-authorized candidates.

### P-TS-02 — Derived edits may not create shadow canonical state

```text
USER_DURABLE_EDIT -> CANONICAL_WRITER_OR_CANONICAL_PROPOSAL
DIRECT_DURABLE_EDIT_OF_DERIVED_PROJECTION=NO
```

Chunks, generated wiki pages, graph summaries and retrieval projections are either disposable or backed by an explicit canonical object/proposal.

### P-TS-03 — Memory promotion is type/risk sensitive

A future memory lifecycle must distinguish influence and evidence requirements. High-influence decisions, constraints, preferences and procedures cannot silently become active from model extraction.

### P-TS-04 — Context residency is a policy with receipts

Resident memory and on-demand recalled memory must be explicit compiler decisions recorded in context receipts, with privacy/token/staleness consequences measurable.

### P-TS-05 — External execution uses one Fehrest admission/receipt authority

Model, web, sandbox, skill and automation runtimes must consume a shared Fehrest execution-admission contract rather than inventing provider-specific authority or retry semantics.

### P-TS-06 — Held-out evaluation is structurally isolated

Any future optimization/evolution system must isolate held-out probes/gold evidence using enforceable process/filesystem/capability boundaries, not prompt instructions.

### P-TS-07 — Decision history is evidence, not memory

Optimization traces, skill PR histories and agent trajectories are evidence. They may seed explicit Memory Proposals, but do not become active memory automatically.

### P-TS-08 — Source reuse requires a standard admission record

No donor code enters production without exact revision/path/rights/attribution/security evidence.

## 3. Spec-map amendments

These are planning amendments to the future V2 proposal. They do not activate the specs.

### 003 — Derived Index and Lexical Retrieval Convergence

Add explicit acceptance requirements:

```text
DERIVED_USER_EDIT_ROUNDTRIP_DEFINED=YES
DERIVED_REBUILD_CANNOT_ERASE_DURABLE_USER_EDIT=YES
PROJECTION_PROVENANCE_COMPLETE=YES
```

If a UI later exposes editable chunks or generated retrieval artifacts, the edit must route to a canonical owner defined by 010/011 or to a canonical proposal/annotation.

### 004 — Graph Intelligence Capability Experiment

Expand from graph-only intelligence to include optional derived temporal-intelligence comparators where they share the same question: does extra derived structure materially improve outcomes?

Candidate comparator family may include:

```text
strong lexical/structured temporal baseline
explicit Fehrest canonical as-of filtering
Graphify / Code-Graph-RAG / Graphiti where applicable
RoMem-style temporal reranking as a research comparator
```

RoMem source code is not admitted while reuse rights are unproven.

Required measures:

```text
temporal contradiction accuracy
historical/as-of correctness
fresh-agent continuation
retrieval recall/precision
stale-use rate
latency
context tokens
build/update cost
memory/disk footprint
model/API cost
```

Kill rule:

```text
if derived temporal/graph intelligence does not add material value over the strong simple baseline:
  DEFER_OR_REJECT
```

### 005 — Graph Production Integration

If retained, rename the conceptual boundary in future authoring from "graph provider" assumptions to a generic replaceable `DerivedIntelligenceProvider` family where necessary, while keeping graph-specific providers optional.

This is not a requirement to generalize prematurely. The active 005 spec, if ever authorized, should create only the smallest interface justified by the retained 004 evidence.

### 006 — Temporal Memory Productization

Add mandatory design sections:

```text
memory-kind taxonomy
influence/risk classification
promotion matrix
confirmation/corroboration requirements
resident-vs-recalled metadata
revalidation/expiry rules
supersession/retraction rules
contradiction linkage
current/as-of deterministic resolution
```

Minimum promotion-matrix fields:

```text
MEMORY_KIND
INFLUENCE_LEVEL
EVIDENCE_REQUIREMENT
CORROBORATION_REQUIREMENT
HUMAN_CONFIRMATION_REQUIREMENT
REVALIDATION_RULE
SUPERSESSION_RULE
RETRACTION_RULE
```

The taxonomy should be requirement-driven. WeKnora's `profile/preference/fact/task/interest` set is a comparator, not a required Fehrest schema.

Add benchmark cases for:

```text
false preference extraction
stale profile item
contradictory fact
high-influence decision candidate
procedure changed after prior confirmation
historical truth query
current truth query
```

### 007 — Universal Context and Memory Gateway

Strengthen 007 as the semantic owner of both context authorization and the general external-execution admission/receipt foundation.

Add ownership for:

```text
context residency policy
external credential -> principal mapping contract
ExecutionAdmission
ExecutionAttemptId
FencingGeneration
ExecutorAudience
DurableDispatchIntent
TerminalReceipt
IndeterminateExecution
ReconciliationEvidence
```

013/014/021 may add provider-specific metadata but may not redefine authority, attempt identity, safe retry or receipt truth.

Required compiler evidence should record whether a served memory was:

```text
RESIDENT
RECALLED_ON_DEMAND
EXCLUDED_STALE
EXCLUDED_SCOPE
EXCLUDED_BUDGET
EXCLUDED_CONFLICTED
```

### 009 — Trusted Vertical Memory Proof

Expand the vertical proof with source-driven falsification cases:

```text
temporal contradiction with multiple superseded facts
resident-memory overexposure
false durable-memory proposal
revoked-grant sandbox continuation attempt
indeterminate external execution after crash
editable-derived-state roundtrip
```

Add strong comparator families only where applicable; donor presence alone does not mandate benchmark inclusion.

### 010 — Workspace Canonical Object and Open-Format Foundation

Add an explicit generated/derived-content authority model:

```text
GENERATED_DRAFT
USER_SAVED_CANONICAL_DOCUMENT
CANONICAL_ANNOTATION_OR_PROPOSAL
MEMORY_PROPOSAL
APPROVED_MEMORY
DERIVED_REBUILDABLE_VIEW
```

No generated wiki, chunk, graph summary or model-produced document may silently skip those transitions.

### 011 — Personal Notes, Docs and Capture Workspace

Require revision/history UX to display whether the edited surface is canonical, draft or derived.

If a visible user edit is durable, it must be backed by a canonical mutation/proposal before success is reported.

### 013 — AI Provider Runtime and Ask Fehrest

Treat any model/tool sandbox as a consumer of 007 execution admission.

Add provider/runtime requirements:

```text
MODEL_RUNTIME != AUTHORITY
SANDBOX_LIVENESS != GRANT_LIVENESS
SECRET_BYTES_NEVER_MODEL_VISIBLE
FAILURE_STATUS != SAFE_RETRY
```

A provider may expose queueing/concurrency controls, but Fehrest attempt identity and fencing remain authoritative.

### 014 — External Evidence and WebMCP

Require every action-capable web/tool invocation to consume 007 execution admission and produce a durable receipt where side effects are possible.

Read-only evidence acquisition still preserves source snapshot identity/freshness and cannot mint authority.

### 018 — Organization Identity, Policy and Admin Foundation

Add explicit API/service credential mapping requirements:

```text
external API key -> Fehrest principal mapping
key rotation/revocation
service account lifecycle
organization policy extension
credential scope audit
```

No external credential identifier becomes canonical principal identity.

### 021 — Extension, Automation and Connector Platform

Expand 021 to own a future skill artifact/evolution lifecycle.

Candidate entities/contracts:

```text
SkillPackage
SkillRevision
SkillSourceProvenance
SkillCapabilityRequirements
SkillRuntimeCompatibility
SkillEvalBinding
SkillReleaseState
SkillRollbackTarget
```

Mandatory evolution law:

```text
skill change
-> isolated candidate revision
-> held-out evaluation
-> regression/security checks
-> review
-> authorized release
```

No auto-merge merely because an optimizer improves a metric.

Eval isolation must be enforceable:

```text
skill/optimizer access != held-out gold access
```

SkillHone is a methodology comparator and possible future pattern donor, not a dependency admission.

## 4. Cross-spec ownership correction

Future reconciliation of `CROSS_SPEC_INVARIANTS_AND_OWNERSHIP.md` should add these responsibilities:

| Responsibility | Owner | Consumers |
|---|---|---|
| Canonical temporal truth/current-as-of resolution | 006 | 007/009/012/013 |
| Derived temporal rank/volatility | 004 experiment; 005 conditional provider | 007/012/013 |
| Memory promotion risk matrix | 006 | all memory proposal producers |
| Resident vs on-demand context policy | 007 | 009/013/019/020 |
| General execution admission/fencing/receipt | 007 | 013/014/021 |
| External credential -> Fehrest principal mapping | 007 baseline; 018 org extension | 013/014/021 |
| Canonical/derived edit transition | 010 + 003 projection rules | 011/012/019 |
| Skill package/evolution lifecycle | 021 | 013/019/022 |
| Held-out skill-eval isolation | 021 | skill optimization systems |
| Skill decision history evidence | 021 | 006 proposal producer only |

## 5. New benchmark program requirements

The future benchmark plan should contain separate evidence families rather than one composite score.

### B-TEMP — Temporal truth and retrieval

Measure:

```text
current fact correctness
as-of correctness
supersession handling
contradiction handling
stale-use rate
retrieval quality
```

Comparator ladder:

```text
canonical explicit time filter + lexical/structured retrieval
optional graph/temporal derived providers
```

The simplest adequate method wins.

### B-MEM-PROMOTE — Memory promotion safety

Measure:

```text
false promotion
missed useful promotion
human review burden
time to confirmation
high-influence error rate
retraction/revalidation correctness
```

### B-CONTEXT-RESIDENCY — Resident versus recalled context

Measure:

```text
continuation correctness
privacy exposure
stale exposure
tokens
latency
cost
```

### B-EXEC — External execution safety

Fault/adversarial matrix:

```text
crash after durable dispatch intent
provider timeout after side effect
worker retry
revocation while sandbox alive
network scope downgrade
credential rotation
session expiry
provider duplicate completion
```

Success requires durable and unambiguous side-effect disposition.

### B-SKILL-EVOLVE — Skill evolution

Compare:

```text
prompt-only rewrite
whole-skill-folder candidate changes
```

under held-out evaluation with structural leakage prevention.

Measure:

```text
held-out quality
regression rate
eval leakage
security violations
change size
review burden
rollback success
```

## 6. Source-specific adoption gates

### RoMem

```text
CURRENT=STUDY/BENCHMARK
CODE_REUSE=NO_UNTIL_RIGHTS_PROVEN
```

Adopt no provider/code until:

```text
exact license/permission basis proven
004 requirement exists
strong simple baseline frozen
benchmark shows material gain
cost/security acceptable
```

### WeKnora

```text
CURRENT=STUDY/BENCHMARK
FUTURE_ADAPT=PER_FILE_ONLY_AFTER_PROVENANCE
```

Do not adopt its full stack. Select individual patterns only when Fehrest requirements demand them.

### SkillHone

```text
CURRENT=STUDY/BENCHMARK
FUTURE_ADAPT=METHOD/PATTERN_FIRST
```

Prefer clean Fehrest-owned implementation of eval isolation and decision-history semantics unless a later source-level reuse gate proves direct adaptation necessary.

## 7. Plan-level gap closure

After this amendment, the new source-driven gaps have an owner without adding a dependency cycle:

```text
TG_01_TEMPORAL_RANK_TRUTH=OWNED
TG_02_RELATION_VOLATILITY=OWNED
TG_03_PROMOTION_POLICY=OWNED
TG_04_CONTEXT_RESIDENCY=OWNED
TG_05_DERIVED_EDIT_SHADOW_STATE=OWNED
TG_06_EXECUTION_ADMISSION_RECEIPT=OWNED
TG_07_EXTERNAL_PRINCIPAL_MAPPING=OWNED
TG_08_QUEUE_IDEMPOTENCY_FENCING=OWNED
TG_09_SKILL_ARTIFACT_LIFECYCLE=OWNED
TG_10_HELD_OUT_EVAL_ISOLATION=OWNED
TG_11_DECISION_HISTORY_VS_MEMORY=OWNED
TG_12_GENERATED_WIKI_AUTHORITY=OWNED
TG_13_PERSISTENT_SANDBOX_REVOCATION=OWNED
TG_14_SOURCE_ADMISSION_RECORD=OWNED
```

## 8. Priority correction

The sources improve priorities as follows without changing execution authority:

```text
FIRST: finish current R1 honestly
THEN: post-R1 canonical core if authorized
THEN: strong deterministic retrieval baseline
THEN: evidence-driven temporal/graph intelligence experiment
THEN: temporal memory productization with explicit promotion policy
THEN: context + execution-admission foundation
THEN: vertical proof
THEN: broader workspace/AI/tools
LATER: safe skill evolution/automation platform
```

This avoids building a sophisticated self-evolving agent ecosystem before Fehrest proves the core memory/context thesis.

## 9. PR #2 reconciliation requirement

PR #2 (`docs/fehrest-founder-vision-v2`) remains a valuable draft but predates the current R1 state and this source review.

Before PR #2 may ever become ready/mergeable for canonicalization, it must be reconciled forward against live `main` and this amendment.

Required future reconciliation:

```text
R1_TERMINAL_RESULT_RECONCILED=YES
LIVE_MAIN_RECONCILED=YES
TENCENT_SOURCE_AMENDMENT_RECONCILED=YES
TG_01_TO_TG_14_OWNERSHIP_REFLECTED=YES
STALE_R1_CLAIMS=0
IMPLEMENTATION_AUTHORITY_NOT_IMPLIED=YES
```

Do not merge PR #2 while R1 is open.

## 10. Final plan state

```text
TENCENT_SOURCE_PLAN_AMENDMENT=PREPARED
SOURCE_STUDY_COMPLETE=YES
SOURCE_CODE_DEPENDENCY_ADMISSION=NO
NEW_TOP_LEVEL_SPEC_IDS=0
NEW_GAPS_WITH_OWNER_OR_GATE=14/14
R1_CHANGED=NO
R1_REVIEW_CANDIDATE_CHANGED=NO
SPEC_002_ACTIVATED=NO
PRODUCT_IMPLEMENTATION_AUTHORIZED=NO
PR_2_MERGE_AUTHORIZED=NO
```
