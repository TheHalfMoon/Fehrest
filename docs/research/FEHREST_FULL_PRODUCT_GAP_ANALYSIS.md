# Fehrest Full Product Gap Analysis and Architecture Corrections

**Status:** NON-AUTHORIZING PRODUCT / ARCHITECTURE RED-TEAM  
**Date:** 2026-09-02  
**Authority:** planning only; implementation remains controlled by `specs/CURRENT.md`, the canonical execution order, active Spec Kits, evidence gates, and required reviews.  
**Active frontier at analysis time:** `R1 / REPLACEMENT_VARIANCE_PILOT_EXECUTION`

> This document intentionally searches for reasons Fehrest could fail even if individual subsystems are well engineered.
>
> It does not authorize UI, collaboration, sync, MCP, ACP, automatic memory, graph, vector, agent execution, or any post-R1 product behavior while those remain blocked.

---

## 1. Executive conclusion

The Fehrest north star is strong, but the product would still fail if it were implemented as a feature union of Slack, Buzz, Notion, Obsidian, Linear, and an agent memory system.

By 2026, incumbents already overlap heavily:

- knowledge workspaces orchestrate internal and external agents;
- collaboration products expose agents as teammates inside channels and DMs;
- issue trackers increasingly let agents triage, implement, review, and automate work;
- coding-agent products already operate multiple agents in parallel;
- memory systems increasingly support temporal reasoning, consolidation, and long-lived learning.

Therefore this is not enough:

```text
Slack + Notion + Obsidian + Linear + agents
```

The stronger product thesis is:

> **Fehrest is the continuity and governed-action substrate for long-lived projects: it preserves what the project knows, what remains true, what work is active, what authority each actor has, why an action was permitted, what was executed, and what evidence proves the result — across disposable agents, models, tools, devices, and vendors.**

The product hierarchy should be:

```text
1. CONTINUITY
2. CANONICAL TRUTH
3. GOVERNED ACTION
4. EVIDENCE / REPLAY
5. HUMAN + AGENT COORDINATION
6. KNOWLEDGE / WORK UX
7. OPTIONAL AUTOMATION / INTELLIGENCE
```

The lower layers must never be allowed to reverse the authority of the higher layers.

---

## 2. The most important strategic correction

### Gap G-001 — Feature aggregation is no longer differentiation

**Severity:** P0  
**Risk:** Fehrest becomes an impressive but replaceable all-in-one workspace.

The market increasingly provides:

```text
agent teammates
agent task automation
workspace-aware retrieval
external agent orchestration
coding from work items
multi-agent supervision
persistent agent memory
MCP integrations
```

Fehrest cannot win by merely having all of those features in one application.

### Correction

Every major feature must strengthen at least one of four Fehrest-native advantages:

```text
CONTINUITY
AUTHORITY
PROVENANCE
REPLAYABILITY
```

A feature that improves none of them is optional product surface, not core architecture.

### Product test

For any proposed feature ask:

```text
Does this help a future human or agent know what is true?
Does this help determine what they may do?
Does this preserve why the state exists?
Does this make the action/result reconstructable or auditable?
```

If all four answers are `NO`, the feature needs a separate product justification.

---

## 3. Product wedge and sequencing

### Gap G-002 — The mature vision is much wider than the initial winning wedge

**Severity:** P0  
**Risk:** scope explosion before Fehrest proves unique value.

The mature Fehrest vision is intentionally broad, but the first product cannot simultaneously win at:

```text
team chat
notes/wiki
project management
agent runtime
memory
search
sync
execution
workflow automation
mobile
voice
```

### Correction — preserve a narrow first wedge

The first proven wedge remains:

> **Long-lived technical/research projects that use multiple AI agents and need durable project continuity across sessions and vendors.**

The initial product loop should be:

```text
project state
→ Fehrest context
→ disposable agent works
→ evidence / events / proposed memories
→ reviewed durable state
→ fresh agent continues
```

Only after this loop beats strong simpler baselines should Fehrest expand into full collaboration/workspace UX.

### Expansion rule

```text
CORE_PROOF_BEFORE_WORKSPACE_BREADTH=YES
```

The mature vision is a destination, not permission to build every surface early.

---

## 4. One canonical model: useful principle, dangerous implementation

### Gap G-003 — "One object model" can become a universal-object anti-pattern

**Severity:** P0  
**Risk:** every entity becomes a bag of properties and semantics become impossible to enforce.

A page, task, decision, message, memory, grant, and execution are not interchangeable even if they share identity, relationships, and event history.

### Correction — use a small kernel plus strongly typed domains

Prefer:

```text
ObjectKernel {
  object_id
  object_type
  created_at
  provenance_root
  lifecycle
}

+ typed domain payload
+ typed relations
+ typed events
```

Do not create one mutable generic object schema that allows arbitrary type changes.

### Required invariants

```text
TYPE_SEMANTICS_ARE_CORE_OWNED=YES
ARBITRARY_PROPERTY_BAG_IS_NOT_AUTHORITY=YES
RELATIONS_HAVE_TYPED_MEANING=YES
DOMAIN_INVARIANTS_SURVIVE_UI_PROJECTIONS=YES
```

Views may be flexible. Canonical semantics must remain strict.

---

## 5. Canonical truth versus collaboration

### Gap G-004 — Local-first and Slack-class collaboration are in structural tension

**Severity:** P0  
**Risk:** a future collaboration server silently becomes canonical authority.

Fehrest promises:

```text
local canonical ownership
single-machine completeness
offline operation
optional sync
```

A collaborative workspace wants:

```text
multiple writers
low-latency shared state
presence
notifications
channels
remote agents
cross-device continuity
```

These goals cannot be reconciled by saying "sync later."

### Correction — define a future replication constitution before collaboration code

The future design must distinguish:

```text
canonical local object
replicated canonical event
remote delivery state
presence/ephemeral state
cache
server-derived index
```

Questions that require explicit answers before multi-user implementation:

1. What is the authoritative mutation unit?
2. Can two devices independently create canonical events while offline?
3. What conflicts are mergeable and what conflicts must remain unresolved?
4. How are ordering and causality represented?
5. Is collaboration event-sourced, CRDT-based, lock-based, or hybrid?
6. How does a user export all shared canonical data without Fehrest infrastructure?
7. How are private/local-only objects represented inside a shared project?
8. Can a hosted agent operate when the owner's primary device is offline without making the host canonical authority?

### Required future gate

```text
COLLABORATION_REPLICATION_CONSTITUTION_REQUIRED_BEFORE_MULTIUSER_IMPLEMENTATION=YES
```

---

## 6. Memory architecture gaps

### Gap G-005 — Memory currently risks being treated as a store instead of a learning lifecycle

**Severity:** P0

Long-lived agent products are moving toward:

```text
memory creation
memory use
consolidation
supersession
skill formation
trajectory learning
background maintenance
```

Fehrest already has stronger provenance and temporal semantics, but needs an explicit learning lifecycle.

### Correction — define the Experience → Candidate → Durable loop

Future conceptual flow:

```text
Raw Experience
  ↓
Trajectory / Event Evidence
  ↓
Candidate Memory / Procedure / Gotcha / Decision
  ↓
Verification / Corroboration / Human Confirmation
  ↓
Durable Canonical State
  ↓
Use / Feedback
  ↓
Supersession / Retraction / Consolidation
```

Automatic extraction never skips candidate state.

### Important distinction

Fehrest should maintain separate objects for:

```text
fact/state memory
procedure/skill
experience/trajectory
decision
preference
constraint
gotcha
```

Do not flatten all durable learning into generic text memories.

---

## 7. Background consolidation

### Gap G-006 — No explicit safe "sleep" / consolidation architecture

**Severity:** P1

Long-lived projects accumulate:

```text
duplicates
stale memories
repeated procedures
contradictions
low-value events
obsolete context
```

Without maintenance, memory quality degrades.

### Correction

Future consolidation may propose:

```text
merge candidates
supersession candidates
procedure extraction
recurring gotchas
summary projections
retention candidates
```

but must preserve:

```text
RAW_EVIDENCE_NOT_REWRITTEN=YES
CANONICAL_PROMOTION_REQUIRES_POLICY=YES
MODEL_CONFIDENCE_NOT_AUTHORITY=YES
CONSOLIDATION_IS_REPLAYABLE_OR_EXPLAINABLE=YES
```

A "memory cleanup" model must never silently rewrite canonical history.

---

## 8. Trajectory model

### Gap G-007 — Agent runs are receipted, but experiential learning needs a first-class trajectory format

**Severity:** P1

Execution receipts answer what happened at action boundaries. They do not by themselves preserve the semantic arc of a long agent run.

### Correction

Define a future open `Trajectory` representation that can normalize sessions from multiple runtimes without making raw vendor transcripts canonical memory.

Conceptual elements:

```text
trajectory_id
runtime identity
model/provider identity
turn/action sequence
context receipt references
tool/execution receipt references
artifacts
reviews
outcome
cost/time
redaction metadata
source fidelity class
```

Trajectory is evidence. Memory is a promoted interpretation of evidence.

```text
TRAJECTORY != MEMORY
TRAJECTORY != AUTHORITY
```

---

## 9. Context compiler gaps

### Gap G-008 — Context quality needs explicit marginal-value economics

**Severity:** P0

"Bounded context" is necessary but insufficient. Fehrest must optimize outcome per unit of context, latency, and cost.

### Correction

For each context package record or derive:

```text
bytes
tokens
selection latency
retrieval latency
model-visible item count
source diversity
freshness
estimated/actual provider cost
outcome contribution when evaluable
```

Benchmark questions:

```text
What is the smallest context that preserves task success?
Which classes of items create negative value?
When does more history hurt?
When does graph/vector retrieval justify its cost?
When does compression preserve or destroy critical constraints?
```

The optimization objective is not maximum recall. It is **correct continuation under bounded resources**.

---

## 10. Context personalization versus determinism

### Gap G-009 — Different agents need different context without sacrificing replay

**Severity:** P1

A coding agent, research agent, planner, reviewer, and support agent should not receive identical project packages.

### Correction

Introduce future explicit `ContextProfile` policy:

```text
profile id/version
role
allowed source classes
allocation policy
recency policy
mandatory items
optional retrievers
compression policy
budget policy
```

Context remains deterministic given:

```text
canonical state
request
grant
context profile
compiler version
retriever generations
budget
```

Personalization must be policy-bound, not hidden model preference.

---

## 11. Agent identity gap

### Gap G-010 — Agent identity needs stronger lifecycle semantics

**Severity:** P0

A visible agent name is not enough. For authorization and audit, Fehrest must distinguish:

```text
logical agent identity
runtime instance
model
provider
host
process/environment
credential principal
human sponsor
session
software version
```

### Correction

Future `AgentIdentityEnvelope` should bind these layers explicitly.

This prevents errors such as treating "Research Agent" running locally today as the same security principal as a hosted copy tomorrow.

### Required rule

```text
DISPLAY_IDENTITY != SECURITY_PRINCIPAL
```

---

## 12. Multi-agent coordination gap

### Gap G-011 — Multiple agents require conflict and ownership control, not only chat

**Severity:** P0

Parallel agents can:

```text
edit the same files
claim the same task
repeat the same research
invalidate each other's assumptions
consume shared budgets
race canonical updates
```

### Correction — add a future coordination plane

Conceptual mechanisms:

```text
task claims with leases
worktree/environment identity
resource reservations
conflict signals
handoff protocol
shared budget accounting
dependency blocking
review ownership
stale-work detection
```

A task claim is not permanent ownership; it is a renewable bounded lease.

For code work, isolated worktrees or equivalent environments should be an adapter-level capability rather than a Git-specific assumption in Core.

---

## 13. Human attention architecture

### Gap G-012 — The north star specifies agents but not enough about human interruption economics

**Severity:** P0

A product with many agents can become an approval-notification machine.

### Correction — make Human Attention a first-class scarce resource

Future system needs an `Attention Inbox` / review plane that groups:

```text
approval requests
blocked agents
high-risk actions
conflicts
review-ready work
decision proposals
memory confirmations
budget exceptions
failed automations
security events
```

Each interruption should carry:

```text
why now
risk
what changes if approved
what happens if ignored
expiry/deadline
relevant evidence
suggested next action
```

### Principle

```text
AGENT_AUTONOMY_SHOULD_REDUCE_HUMAN_COORDINATION_LOAD
```

If adding agents increases operator overhead faster than output, Fehrest fails its purpose.

---

## 14. Approval semantics gap

### Gap G-013 — Binary approval is too weak for long-running automation

**Severity:** P0

Approvals should support more than:

```text
allow once
deny
```

### Correction

Future decisions may include:

```text
allow once
allow this operation class within scope
allow until time/budget limit
allow for this task only
allow with reduced scope
require second reviewer
escalate
pause agent
revoke lease
```

Every approval must bind the exact request or policy transformation it authorizes.

---

## 15. Security and secret architecture

### Gap G-014 — Credential scope is present conceptually but secret custody is under-specified

**Severity:** P0

Need explicit separation between:

```text
secret storage
secret eligibility policy
secret injection
secret use observation
secret redaction
secret rotation/revocation
```

### Correction

Secrets should be represented to agents as capability classes/references, never values.

Execution providers receive secrets only at the narrowest possible boundary.

Receipts record:

```text
credential_class_used
```

not credential material.

Future security design must address:

```text
OS keychain / secret store integration
remote executor secret injection
redaction of stdout/stderr
secret-taint handling in artifacts
clipboard boundaries
crash dump exposure
child-process inheritance
```

---

## 16. Local encryption and device loss

### Gap G-015 — Local-first ownership without encryption/recovery policy is incomplete

**Severity:** P1

If Fehrest becomes the brain of a person's projects, the local vault may contain extremely sensitive knowledge.

### Correction

Future architecture must explicitly choose boundaries for:

```text
at-rest encryption
key custody
hardware-backed keys where available
selective encrypted objects
backup encryption
recovery keys
multi-device key transfer
search/index behavior over encrypted content
```

Encryption must not create a hidden cloud authority requirement.

---

## 17. Retention and evidence explosion

### Gap G-016 — Receipts + trajectories + chats + events can become an unbounded surveillance log

**Severity:** P0

Auditability can destroy usability, storage economics, privacy, and trust if every low-level detail is retained forever.

### Correction — durability tiers are mandatory

Use conceptually:

```text
T1 permanent minimal proof
T2 reconstructable operational detail
T3 ephemeral/debug detail
```

For each evidence class define:

```text
retention default
compaction rule
redaction rule
export behavior
legal/privacy sensitivity
reconstruction guarantee
```

Do not store token streams forever merely because they are observable.

---

## 18. Search architecture gap

### Gap G-017 — One global search needs semantic contracts, not only a common box

**Severity:** P1

Searching work items, knowledge, memory, conversations, decisions, and execution artifacts is not one ranking problem.

### Correction

Global search should use:

```text
federated candidate generation
per-domain ranking
scope filtering before exposure
result-type-aware presentation
explicit provenance/freshness
cross-domain fusion only when justified
```

Do not let a universal relevance score become authority.

Search must expose stale/superseded state honestly.

---

## 19. Work graph gap

### Gap G-018 — Linear-class work requires a richer state machine than generic tasks

**Severity:** P1

Future work objects need explicit distinctions among:

```text
requested work
planned work
ready work
claimed work
in progress
blocked
review ready
verified
closed
cancelled
superseded
```

Evidence-dependent work must identify the closeout contract before execution begins.

### Correction

Conceptual `CompletionContract`:

```text
required test class
required review class
required artifact class
required authority class
required runtime evidence
required benchmark threshold
```

A work item closes only when its contract is satisfied.

---

## 20. Decision architecture gap

### Gap G-019 — Decisions need first-class lifecycle independent of notes and chat

**Severity:** P1

A mature project brain must distinguish:

```text
proposal
accepted decision
rejected alternative
superseded decision
exception
temporary waiver
```

### Correction

A `Decision` should bind:

```text
question
selected option
alternatives
rationale
evidence
scope
effective interval
owner/authority
supersedes
exceptions
review date if needed
```

This is critical for future-agent orientation.

---

## 21. Procedure and skill gap

### Gap G-020 — Procedures should not be modeled as ordinary knowledge pages only

**Severity:** P1

Agents need machine-usable knowledge such as:

```text
how to release
how to run a benchmark
how to recover a database
how to perform review
how to deploy safely
```

### Correction

Future `Procedure` objects should support:

```text
preconditions
steps
required capabilities
expected evidence
failure paths
version
last verified environment
```

This can later bridge knowledge and safe automation without turning prose into implicit executable authority.

---

## 22. Automation gap

### Gap G-021 — Automation must not become a second authority system

**Severity:** P0

Schedules, triggers, workflows, and autonomous agents can accidentally mint authority through configuration.

### Correction

Every automation execution resolves authority from canonical grants at run time.

```text
TRIGGER != AUTHORITY
SCHEDULE != AUTHORITY
WORKFLOW_DEFINITION != AMBIENT_GRANT
```

A workflow may describe desired actions. Capability checks remain mandatory at execution.

---

## 23. Plugin / extension ecosystem gap

### Gap G-022 — A great product needs extensibility without surrendering the trust model

**Severity:** P1

Without extensions Fehrest may be too rigid. With unrestricted plugins it can lose every security invariant.

### Correction

Future extensions require:

```text
manifested capabilities
versioned protocol contract
isolated execution where appropriate
explicit network/filesystem scopes
signed or provenance-bound packages
upgrade review for widened permissions
no direct canonical database mutation
```

Extensions call Core APIs. They do not bypass Core semantics.

---

## 24. Agent marketplace / discovery gap

### Gap G-023 — Multi-agent interoperability needs capability discovery

**Severity:** P2

Users need to know what an agent can actually do before granting access.

Future agent manifests should describe:

```text
identity
runtime protocol
model requirements
tools requested
data scopes requested
network needs
credential classes
cost characteristics
supported tasks
receipt support
sandbox compatibility
```

Claims from agent manifests are descriptive, not trusted authority.

---

## 25. Runtime portability gap

### Gap G-024 — ACP/MCP alone do not guarantee semantic portability

**Severity:** P1

Different agents interpret context, cancellation, approvals, tasks, and tool errors differently.

### Correction

Fehrest needs an adapter conformance suite that tests runtimes against common scenarios:

```text
grant denial
late approval
cancellation
context refresh
handoff
compaction
receipt propagation
tool failure
partial execution
subagent delegation
```

Protocol compatibility is not equivalent to behavioral equivalence.

---

## 26. Remote execution gap

### Gap G-025 — Local-first does not mean all execution should be local

**Severity:** P1

Some jobs need:

```text
GPU
browser isolation
untrusted code sandbox
large builds
long-running workers
special networks
```

### Correction

Remote execution must be an accelerator/provider, never canonical authority.

A remote result must return enough evidence to bind:

```text
executor identity
environment image/digest
input digest
capability lease
artifact digests
network policy
exit state
```

The local core decides what result becomes durable state.

---

## 27. Cost control gap

### Gap G-026 — Agent Brain without resource governance can become economically unpredictable

**Severity:** P0

Need budgets across:

```text
model tokens
API spend
compute time
remote execution
storage
egress
concurrent agents
background jobs
```

### Correction

Budgets belong in policy and capability leases, not only admin dashboards.

The product should support:

```text
per task
per agent
per project
per workspace
per time window
```

with hard and soft limits.

---

## 28. Latency and responsiveness gap

### Gap G-027 — "Best product" requires explicit latency budgets

**Severity:** P1

A powerful workspace that feels slow will lose to narrower incumbents.

Future SLO classes should distinguish:

```text
local navigation
command palette
lexical search
object open
write commit
agent context compile
remote action start
background indexing
```

Performance should be benchmarked against realistic large vaults/projects, not toy fixtures.

---

## 29. Scale model gap

### Gap G-028 — No explicit target scale envelope for the mature system

**Severity:** P1

Need planned benchmark classes such as:

```text
10k / 100k / 1m objects
1 / 10 / 100 concurrent agents
1 / 10 / 100 GB canonical vaults
long event histories
large repositories
multi-year projects
```

Fehrest should fail visibly outside supported envelopes rather than silently degrade correctness.

---

## 30. Offline-first UX gap

### Gap G-029 — Offline capability needs visible product semantics

**Severity:** P2

Users should know:

```text
what works offline
what is queued for sync
which agents are unavailable
which evidence is local only
which remote actions are pending
```

Offline should be a first-class state, not an error mode.

---

## 31. Trust UX gap

### Gap G-030 — Strong internal security is insufficient if users cannot understand it

**Severity:** P0

The UI must make authority legible without forcing users to read policy files.

Users need clear answers to:

```text
What can this agent read?
What can it modify?
Which network destinations can it reach?
Which credentials can it use?
What changed since I granted access?
Why is approval needed now?
```

Avoid permission fatigue. Show meaningful semantic scopes, not raw low-level lists by default.

---

## 32. Reversibility gap

### Gap G-031 — Agent actions should be reversible where the underlying domain permits it

**Severity:** P1

Receipts explain an action but do not undo it.

### Correction

Future actions should declare:

```text
REVERSIBLE
COMPENSATABLE
IRREVERSIBLE
```

For reversible mutations, capture enough prior-state identity for safe rollback.

For irreversible actions, approval UX must be stronger.

Never falsely label a compensating action as exact rollback.

---

## 33. Provenance interoperability gap

### Gap G-032 — Fehrest receipts should be exportable, not a proprietary audit island

**Severity:** P2

Define open schemas and optional mappings to standard observability/trajectory formats where useful.

Fehrest remains source-of-truth for its own receipt semantics, but data should be portable.

---

## 34. Import/migration gap

### Gap G-033 — A Work OS must make leaving incumbents easy

**Severity:** P1

Future importers may need to migrate from:

```text
Markdown folders
Obsidian vaults
Notion exports
Slack exports
Linear exports
GitHub issues/discussions
agent transcripts
```

Imported material is evidence and must preserve source provenance.

Do not require users to abandon existing knowledge to try Fehrest.

---

## 35. Export and anti-lock-in gap

### Gap G-034 — Export must include semantics, not only files

**Severity:** P0

A Markdown dump alone does not preserve:

```text
stable identity
decision lifecycle
memory lifecycle
work graph
provenance
event relationships
receipts
```

Future open export must include human-readable content plus documented machine-readable semantic records.

The user should be able to reconstruct their project brain without Fehrest binaries.

---

## 36. Product information architecture gap

### Gap G-035 — Seven surfaces can recreate seven separate applications inside one shell

**Severity:** P1

### Correction — orient around project state and attention, not modules

The mature home experience should likely center on:

```text
NOW       — what needs attention
PROJECT   — current durable state
WORK      — goals/issues/dependencies
KNOWLEDGE — pages/decisions/procedures/memory
ACTIVITY  — humans/agents/events/receipts
AGENTS    — active/delegated work
```

Chat, search, and command should cross those views.

Exact IA remains a future UI design problem, but module silos should be avoided.

---

## 37. Product interaction gap

### Gap G-036 — Agent work needs a review-native UI, not only conversational UI

**Severity:** P0

Users should review structured proposed changes:

```text
code diffs
knowledge edits
work-state transitions
decision promotions
memory promotions
permission changes
automation changes
```

Chat can explain the proposal. It should not be the only representation of it.

---

## 38. Notifications gap

### Gap G-037 — Slack-style notifications will become unbearable with agents

**Severity:** P1

Need semantic notification classes:

```text
FYI
ACTION_REQUIRED
APPROVAL_REQUIRED
RISK
BLOCKED
REVIEW_READY
FAILURE
BUDGET
SECURITY
```

Notification policy should be derived from user/team configuration, never agent preference.

---

## 39. Social/collaboration safety gap

### Gap G-038 — Agents in team conversations create identity and attribution risks

**Severity:** P1

Every agent-authored message must visibly preserve:

```text
agent identity
human sponsor/owner where applicable
runtime class
whether autonomous or directly prompted
source task/run
```

Agents must not impersonate humans.

Generated messages and human-authored messages should remain distinguishable in durable provenance even if UI styling is subtle.

---

## 40. Product metrics gap

### Gap G-039 — Stars, activity, or number of stored memories are not success metrics

**Severity:** P0

Primary product metrics should reflect outcomes such as:

```text
fresh-agent continuation success
time to orientation
repeated-work reduction
human interruption load
context tokens per successful task
cost per successful task
stale-memory error rate
unauthorized-action rate
replay/audit completeness
evidence-backed closeout rate
recovery success
```

Growth metrics matter later. They must not replace outcome metrics.

---

## 41. Evaluation gap

### Gap G-040 — The mature product needs a benchmark portfolio, not one benchmark

**Severity:** P0

R1 appropriately tests the current thesis. Future product qualification should add independent gates for:

```text
continuation quality
context efficiency
memory correctness
staleness/supersession
permission isolation
multi-agent coordination
human review load
execution safety
recovery
search quality
latency
cost
cross-runtime interoperability
```

No single aggregate score should hide a safety regression.

---

## 42. Adversarial product tests

Future product reviews should ask:

### A. The Notion test

If Notion already coordinates external agents inside rich workspace data, why switch?

Required Fehrest answer:

```text
local/open ownership
stronger temporal truth
portable agent continuity
deterministic context compilation
explicit authority
receipted action
vendor independence
```

### B. The Linear test

If Linear can triage, code, review, and automate work, why switch?

Required answer:

```text
work is integrated with durable project memory, knowledge, decisions, provenance, and cross-agent continuity rather than living primarily inside a work tracker
```

### C. The Slack test

If Slack already makes agents teammates in channels, why switch?

Required answer:

```text
conversation is connected to canonical state and governed execution rather than remaining primarily communication context
```

### D. The Letta/Mem0 test

If memory systems already learn across sessions, why switch?

Required answer:

```text
Fehrest combines durable memory with canonical project truth, work state, explicit authority, context receipts, execution receipts, replay, and open ownership
```

### E. The Codex test

If a coding-agent command center already runs many agents in parallel, why switch?

Required answer:

```text
Fehrest survives any one coding-agent runtime and preserves project continuity, grants, evidence, memory, work, and context across all of them
```

If these answers cannot be demonstrated empirically, the product direction must be reconsidered.

---

## 43. Revised product architecture

The north star should be understood as four foundational planes and several product projections.

```text
┌─────────────────────────────────────────────────────────────┐
│ HUMAN / AGENT PRODUCT SURFACES                              │
│ knowledge · work · collaboration · review · command         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ CONTINUITY PLANE                                            │
│ canonical objects · temporal state · decisions · memory     │
│ procedures · work graph · event history                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ CONTEXT / INTERPRETATION PLANE                              │
│ retrieval · temporal resolution · compiler · traces         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ AUTHORITY / ACTION PLANE                                    │
│ grants · leases · approvals · execution providers           │
│ agent identity · budgets · secret boundaries                │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ EVIDENCE / REPLAY PLANE                                     │
│ manifests · receipts · trajectories · artifacts · review    │
│ recovery · retention tiers                                  │
└─────────────────────────────────────────────────────────────┘
```

No product surface bypasses these planes.

---

## 44. Revised durable object families

Future design should investigate at least these typed families rather than a universal bag-of-properties object:

```text
KnowledgeObject
Project
WorkItem
Decision
Procedure
Memory
Conversation
Message
Actor
AgentIdentity
Session
Grant
CapabilityLease
Approval
Automation
Execution
Artifact
Evidence
Trajectory
ContextReceipt
ExecutionReceipt
View
ExternalSource
```

This list is a design candidate, not an authorized schema.

---

## 45. Revised product loops

### Loop 1 — Orientation

```text
open project
→ current state compiled
→ active work + decisions + constraints surfaced
→ human/agent understands what matters now
```

### Loop 2 — Agent work

```text
work item
→ grant
→ context receipt
→ bounded execution
→ artifacts/receipts
→ review
→ evidence-backed closeout
```

### Loop 3 — Durable learning

```text
experience
→ evidence/trajectory
→ candidate memory/procedure/decision
→ verification
→ durable state
→ future context
```

### Loop 4 — Collaboration

```text
conversation
→ proposal
→ structured review
→ canonical promotion when authorized
```

### Loop 5 — Automation

```text
trigger
→ resolve current canonical authority
→ derive bounded lease
→ execute
→ receipt
→ review/escalation if required
```

These loops should be more important than feature-page completeness.

---

## 46. Roadmap correction

The existing execution order should remain intact while R1 is open. After product-thesis proof and authorized activation, future planning should avoid jumping directly from context/memory into full Slack/Notion/Linear breadth.

A safer conceptual maturity sequence is:

```text
A. canonical core
B. derived retrieval
C. optional structural intelligence decision
D. temporal memory/product learning
E. context + authority gateway
F. vertical continuation proof
G. agent coordination + human review plane
H. local-first product workspace
I. replication/collaboration proof
J. team collaboration
K. richer automation/ecosystem
L. optional mobile/voice/enterprise surfaces
```

The exact future Spec Kit sequence remains governed by canonical planning; this document does not reorder it by itself.

---

## 47. Product quality bar

"Best product" should mean all of the following, not feature count:

```text
FAST
CALM
LOCAL-FIRST
OPEN
RECOVERABLE
AUDITABLE
AGENT-NATIVE
HUMAN-CONTROLLABLE
MODEL-INDEPENDENT
EVIDENCE-BOUND
SECURE-BY-DEFAULT
PORTABLE
REVERSIBLE-WHERE-POSSIBLE
MEASURABLY_USEFUL
```

A beautiful interface over unverifiable agent behavior is not success.

A perfect audit system that makes ordinary work painful is not success.

A powerful agent brain that cannot export its data is not success.

A collaboration layer that requires Fehrest servers to preserve canonical truth is not success.

---

## 48. P0 gaps that must be closed before the mature product can be considered coherent

```text
G-001 differentiation beyond feature aggregation
G-002 initial wedge / scope discipline
G-003 typed canonical model instead of universal object
G-004 local-first collaboration / replication constitution
G-005 explicit durable learning lifecycle
G-008 context marginal-value economics
G-010 security-grade agent identity
G-011 multi-agent coordination
G-012 human attention plane
G-013 richer approval semantics
G-014 secret custody/injection/redaction
G-016 evidence retention tiers
G-021 automation cannot mint authority
G-026 resource/cost governance
G-030 trust UX
G-034 semantic anti-lock-in export
G-036 review-native interaction
G-039 outcome-based product metrics
G-040 benchmark portfolio
```

These are product-architecture requirements, not current implementation tasks.

---

## 49. Things Fehrest should deliberately not optimize for

```text
maximum number of integrations
maximum number of agents running
maximum memory retained
maximum context size
maximum automation
maximum UI surfaces
maximum language count
maximum cloud dependence
maximum feature parity
```

Instead optimize for:

```text
correct continuation
low coordination overhead
bounded authority
high-quality durable state
fast orientation
low stale-state error
reproducible action
portable ownership
```

---

## 50. Final correction to the north star

The mature Fehrest product should still feel like the best parts of Slack, Buzz, Notion, Obsidian, and Linear, but that is an experience comparison, not the architecture thesis.

The architecture thesis is:

> **Fehrest is the durable continuity, authority, and evidence substrate for human-and-agent work. It turns project knowledge, decisions, memory, work state, conversations, and execution into a portable project brain that can safely survive and coordinate disposable agents.**

The product promise remains:

> **Your projects remember. Your agents arrive informed. Their authority is bounded. Their work is provable. Your knowledge remains yours.**

The stronger strategic test is:

> **If every model, agent vendor, hosted service, derived index, and Fehrest UI were replaced tomorrow, would the project's durable knowledge, current truth, work state, decisions, provenance, and evidence remain usable and understandable?**

For Fehrest, the required answer is:

```text
YES
```
