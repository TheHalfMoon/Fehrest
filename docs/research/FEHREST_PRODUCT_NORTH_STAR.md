# Fehrest Product North Star — Agent Brain and AI-Native Work OS

**Status:** NON-AUTHORIZING PRODUCT NORTH STAR  
**Date:** 2026-09-02  
**Authority:** founder product direction captured for planning; implementation remains gated by `specs/CURRENT.md`, canonical execution order, active Spec Kits, benchmark evidence, security review, and explicit gate authority.

## 1. Purpose

Fehrest is intended to become the durable brain and work operating system for humans and AI agents.

The long-term product is not a memory plugin, a note-taking clone, a chat client, a project tracker, a Git host, or an agent framework. It is the substrate that lets people and agents share durable knowledge, bounded authority, work state, evidence, memory, collaboration, execution, repository history, and continuity without surrendering canonical truth to a model, vendor, hosted service, derived index, transient conversation, IDE, agent runtime, or Git forge.

The north-star formulation is:

> **Fehrest is the Agent Brain and AI-native Work OS: durable local-first project continuity, temporal memory, knowledge, collaboration, execution, planning, repository portability, agent interoperability, and auditable capability control in one coherent system.**

A second formulation defines the experience target:

> **The calm knowledge depth of Notion and Obsidian, the collaboration velocity of Slack and Buzz, the execution discipline of Linear, Git-native interoperability with GitHub-class workflows, and a stronger project brain than any of them — unified by Fehrest-owned canonical truth, provenance, replay, and authority.**

The strategic center is not feature aggregation. It is:

> **durable project continuity + canonical temporal truth + governed action + provenance + replay across disposable agents, models, tools, devices, repositories, IDEs, CLIs, and vendors.**

This document does not authorize implementation while R1 remains open.

```text
ACTIVE_EXECUTION_FRONTIER=R1
R1_SEMANTICS_CHANGED=NO
PRODUCT_BEHAVIOR_CHANGED=NO
UI_IMPLEMENTATION_AUTHORIZED=NO
COLLABORATION_IMPLEMENTATION_AUTHORIZED=NO
SYNC_IMPLEMENTATION_AUTHORIZED=NO
MCP_IMPLEMENTATION_AUTHORIZED=NO
ACP_IMPLEMENTATION_AUTHORIZED=NO
GIT_IMPORT_IMPLEMENTATION_AUTHORIZED=NO
GIT_EXPORT_IMPLEMENTATION_AUTHORIZED=NO
```

## 2. The product thesis, expanded without weakening the original thesis

The existing thesis remains load-bearing:

```text
Agents are disposable. Memory is not.
The user's knowledge must survive Fehrest itself.
```

The expanded product direction adds:

```text
Agents are disposable.
Memory is durable.
Projects outlive repositories.
Authority is explicit.
Work is traceable.
Context is compiled.
Knowledge is portable.
Repositories are portable.
Collaboration is first-class.
Execution is receipted.
The user remains the ultimate owner.
```

Fehrest must make a fresh agent materially more capable because the system can provide the right durable state, current decisions, project history, constraints, procedures, evidence, work graph, repository provenance, and bounded tools without leaking ambient authority or forcing the user to reconstruct project context manually.

A Git repository is one project source, not the whole project brain.

```text
PROJECT != REPOSITORY
GIT_HISTORY != PROJECT_MEMORY
IMPORT != FORK
```

Fehrest should be able to ingest a project from GitHub or another Git source, preserve its exact source provenance, enrich it with durable project understanding, and later export or publish selected work back to GitHub without requiring a remote fork as the prerequisite for local ownership or exploration.

## 3. What Fehrest becomes

The mature product has eight integrated surfaces over one canonical kernel with strongly typed domains.

### 3.1 Brain

The Brain answers:

```text
What exists?
What happened?
What remains true?
What changed?
Why is it true?
What is connected?
What should this agent see?
What may this agent do?
What did this agent actually do?
Where did this project come from?
What changed upstream?
What project memory may now be stale?
```

The Brain includes:

- canonical knowledge;
- event journal;
- temporal memory;
- supersession and contradiction resolution;
- lexical and optional derived retrieval;
- optional graph/vector capabilities only when benchmark-retained;
- deterministic context compilation;
- served-item manifests;
- SelectionTrace;
- provenance;
- replay;
- agent/session grants;
- capability leases;
- execution receipts;
- repository/source provenance;
- upstream-change awareness;
- explicit memory revalidation/invalidation paths.

### 3.2 Project Substrate

The Project Substrate makes repository and project state portable without reducing Fehrest to a Git host.

Target capabilities, when separately specified and authorized:

- import from GitHub or other Git remotes without requiring a fork;
- preserve exact Git object/source identity;
- snapshot, mirror, or explicitly track upstream;
- keep local Fehrest project identity stable even when repository location changes;
- relate multiple repositories to one Fehrest project;
- compare and reconcile upstream changes;
- identify project memories/procedures/decisions potentially invalidated by upstream changes;
- export Git repositories, bundles, patches, branches, or publish to GitHub explicitly;
- export Fehrest semantic project state independently from Git hosting.

The defining distinction is:

```text
Git stores repository history.
Fehrest preserves project understanding.
```

See `docs/research/FEHREST_PROJECT_SUBSTRATE_AND_MEMORY_FABRIC.md`.

### 3.3 Workspace

The Workspace is the human-facing knowledge environment:

- pages and documents;
- Markdown-native canonical editing;
- structured properties;
- backlinks;
- references;
- attachments;
- collections/views as projections;
- project spaces;
- saved searches;
- temporal history;
- knowledge relationships;
- agent-visible and private scopes;
- exportable open data.

The inspiration is the usability of Notion and Obsidian, but canonical semantics remain Fehrest-native and open.

### 3.4 Collaboration

The Collaboration surface provides Slack/Buzz-class coordination without making chat the source of truth:

- channels;
- threads;
- DMs;
- mentions;
- reactions;
- agent participants;
- presence;
- notifications;
- huddles/voice when separately justified;
- decisions captured from conversations;
- links from conversation to canonical objects, tasks, runs, commits, and evidence.

Critical distinction:

> Conversation is coordination evidence, not canonical truth by default.

A chat message may propose a decision. Canonical promotion requires the appropriate authenticated mechanism and provenance event. Retrieved conversation text can never mint capability authority.

### 3.5 Work / Projects

The Work surface targets Linear-class execution discipline:

- projects;
- initiatives;
- issues;
- milestones;
- cycles;
- dependencies;
- status;
- assignees;
- priorities;
- labels;
- roadmaps;
- work queues;
- triage;
- command menus;
- fast keyboard-first operation;
- agent-created proposals with explicit provenance;
- evidence-linked completion.

A task is not complete because an agent says it is complete. Fehrest should be able to bind completion to the expected evidence class: tests, artifacts, review, commit, deployment, user decision, benchmark, or another named gate.

### 3.6 Agent Runtime Interoperability

Fehrest is not required to own the reasoning loop. It becomes the brain and capability plane that many agent runtimes can use.

Target runtime families include, when separately evaluated and authorized:

```text
Codex
Claude Code
Hermes
OpenCode
Goose
Zed/ACP clients
JetBrains/ACP clients
custom agents
local models
hosted models
```

The preferred interoperability direction is protocol-first:

```text
ACP for agent/client interoperability where applicable
MCP for tool interoperability where applicable
Fehrest-native capability and receipt semantics remain authoritative
```

No external protocol may weaken Fehrest's canonical authority boundary.

### 3.7 Execution

Fehrest should eventually make agents useful, not merely informed.

Execution providers are replaceable and policy-bound:

```text
NativeExecutor
ContainerExecutor
WasiExecutor
RemoteSandboxExecutor
future provider adapters
```

The execution plane owns:

- process lifecycle;
- cancellation;
- timeout;
- output bounds;
- filesystem scope;
- network scope;
- credential scope;
- cost limits;
- environment identity;
- artifacts;
- execution receipts.

The architecture must preserve:

```text
PROCESS_LIFECYCLE_HARDENED != SECURITY_SANDBOXED
```

Permission prompts alone are not a sandbox.

### 3.8 Command / Automation Layer

Fehrest should expose the same underlying capabilities through multiple surfaces:

```text
CLI
TUI when useful
Desktop
Web when separately authorized
IDE adapters
agent tools
automation/workflows
voice as an optional input/output surface
```

The headless Rust core remains complete without a graphical interface.

## 4. One canonical kernel, strongly typed domains, many views

Fehrest should avoid becoming five disconnected products glued together, but it must also avoid a universal-property-bag anti-pattern.

The product should converge on a small canonical kernel with strongly typed domain objects, typed relationships, and event history. Example conceptual families:

```text
KnowledgeObject
WorkItem
Project
RepositorySource
Decision
Memory
Conversation
Actor
Agent
Session
Grant
CapabilityLease
Execution
Artifact
Evidence
ExternalSource
Trajectory
View
```

The exact schema is future-spec work, not authorized here.

A Slack-like channel, a Notion-like page, an Obsidian-like note, a Linear-like issue, a GitHub repository, and an agent run should be able to reference the same project, decision, evidence, and identity graph without duplicating canonical truth.

```text
ONE_CANONICAL_KERNEL=YES
STRONGLY_TYPED_DOMAINS=YES
UNIVERSAL_MUTABLE_PROPERTY_BAG=NO
```

## 5. The Fehrest differentiation

Fehrest should not win by having more checkboxes than incumbents. It should win because the products it learns from do not share Fehrest's combined invariants.

### 5.1 Versus GitHub-class forges

GitHub-class platforms excel at Git hosting, review, issues, CI integration, and public collaboration.

Fehrest must add:

- project identity above one repository;
- no-fork local import and exploration;
- durable project memory;
- temporal decisions and supersession;
- context compilation;
- agent continuity across providers;
- governed execution;
- execution/context receipts;
- upstream-aware memory revalidation;
- semantic project export beyond Git objects.

Fehrest is not required to replace GitHub. The initial strategy is additive:

```text
keep GitHub
keep your IDE
keep your CLI agent
add Fehrest
```

GitHub can remain the publication/collaboration surface while Fehrest becomes the durable project brain.

### 5.2 Versus Slack-class tools

Slack-class tools optimize communication. Fehrest must preserve communication while converting important outcomes into provenance-linked durable state.

Fehrest advantage target:

```text
conversation + canonical decisions + memory + agent context + execution evidence
```

### 5.3 Versus Buzz

Buzz demonstrates a strong human/agent collaboration model, protocol boundaries, agent identity, ACP/MCP integration, signed-event thinking, and hardened tool lifecycle patterns.

Fehrest should learn from those patterns but retain a different center of gravity:

```text
Buzz center: collaborative workspace/event substrate
Fehrest center: durable project brain/canonical context/authority/evidence substrate
```

Fehrest may later provide collaboration that is competitive with Buzz while preserving stronger separation between evidence and authority, canonical and derived state, capability scope, temporal memory, deterministic context compilation, and replay.

### 5.4 Versus Notion

Notion-class products excel at flexible knowledge and structured workspace UX.

Fehrest must add:

- local-first canonical ownership;
- open durable formats;
- agent-safe context delivery;
- temporal memory;
- explicit provenance;
- capability control;
- deterministic compilation;
- execution receipts;
- vendor-independent portability.

### 5.5 Versus Obsidian

Obsidian-class products excel at local knowledge ownership and linked notes.

Fehrest must add:

- first-class machine memory;
- temporal resolution;
- canonical event history;
- agent grants;
- context compilation;
- work state;
- collaboration;
- evidence-bound execution;
- multi-agent interoperability.

### 5.6 Versus Linear

Linear-class products excel at fast, opinionated work execution.

Fehrest must add:

- deep project memory;
- canonical knowledge;
- conversations;
- agent participants;
- evidence-linked completion;
- context generated from the actual project state;
- decision provenance;
- execution receipts.

### 5.7 Versus standalone agent memory systems

Memory products may retrieve prior information. Fehrest must prove a stronger claim:

> A disposable fresh agent should continue real work more correctly and efficiently because Fehrest compiles bounded, current, provenance-linked state and couples that state to explicit authority and auditable execution.

## 6. Product experience principles

### P-01 — Instant orientation

Opening a project should answer within seconds:

```text
What is this?
Where did it come from?
What matters now?
What changed recently?
What is blocked?
What decisions are active?
What did agents do?
What needs my attention?
```

### P-02 — Seconds-to-context, not history dumping

An authorized agent should receive the complete relevant working context for a task quickly, while retaining immediate drill-down access to deeper authorized evidence.

Planning targets should eventually measure warm-local orientation and context compilation in seconds, with explicit P50/P95 latency, constraint-miss, stale-state, provenance, and token-efficiency metrics.

```text
FAST_CONTEXT != FULL_HISTORY_DUMP
```

### P-03 — One command surface

A global command interface should eventually let a user search, navigate, create, assign, ask, run, approve, review, import, compare upstream, and publish without hunting across modules.

### P-04 — Keyboard first, not keyboard only

Power users must be fast. New users must remain oriented.

### P-05 — Calm density

Information-dense does not mean visually noisy. Fehrest should favor calm hierarchy, precise typography, strong focus states, predictable shortcuts, and progressive disclosure.

### P-06 — Agents look like accountable collaborators

An agent should have visible:

- identity;
- runtime/model/provider;
- current grant;
- active task;
- working context;
- tool calls;
- receipts;
- artifacts;
- cost/time where available;
- review state.

### P-07 — Nothing important disappears into chat

Important decisions, constraints, tasks, evidence, and memories should be capturable as durable typed state with provenance.

### P-08 — Nothing inferred becomes authority silently

Agent suggestions remain suggestions until canonical policy permits the appropriate promotion path.

### P-09 — Everything critical has receipts

The user should be able to ask:

```text
Why did the agent know this?
Why was it allowed to do this?
What exactly did it execute?
What changed?
Which evidence closed the task?
```

and receive a reconstructable answer.

### P-10 — No silent forgetting

Fehrest should never promise impossible perfect memory. It should instead guarantee that durable canonical state is not silently discarded, retention is explicit, loss is detectable, supersession is preserved, and unreconstructable historical content is reported honestly.

```text
NO_SILENT_FORGETTING=YES
```

## 7. Language and platform architecture

The intended language roles are:

### Rust — correctness and control plane

Rust owns security- and correctness-sensitive semantics:

```text
canonical state
journal/recovery
identity
memory state transitions
authorization
capability leases
context compiler
agent gateway
repository/source provenance
Git import/export integrity boundaries
protocol adapters where core-sensitive
execution supervision
receipts
provenance
CLI core
local services
sync semantics if ever authorized
```

### TypeScript — primary product surface

TypeScript/React may own:

```text
desktop/web UI
interaction state
view composition
rich product surfaces
non-authoritative client projections
SDK ergonomics
```

UI cannot become canonical authority.

### Python — research and optional AI boundary

Python remains valuable for:

```text
benchmarks
evaluation
analysis
research experiments
provider prototypes
model-assisted optional transforms
```

Python is not required for Fehrest Core correctness.

### Other languages

Dart, Swift, Kotlin, or other languages enter only when a separately proven mobile/native requirement justifies them. Language count is not a product metric.

## 8. Architecture laws for the mature product

The following must remain true even if the product becomes large:

```text
CANONICAL != DERIVED
EVIDENCE != AUTHORITY
PATH != IDENTITY
PROJECT != REPOSITORY
GIT_HISTORY != PROJECT_MEMORY
IMPORT != FORK
IMPORT != PUBLISH_AUTHORITY
RANK != AUTHORIZATION
RETRIEVED_CONTENT != INSTRUCTION
MODEL_OUTPUT != FACT
CHAT != CANONICAL_STATE
PERMISSION_PROMPT != SANDBOX
REMOTE_SERVICE != CANONICAL_AUTHORITY
AGENT != OWNER
IDE != MEMORY_OWNER
AGENT_RUNTIME != MEMORY_OWNER
MODEL_PROVIDER != MEMORY_OWNER
UI != CORE
SYNC != REQUIRED
```

And:

```text
AI_OFF remains a valid core mode.
Local single-machine use remains complete.
Export remains possible without Fehrest infrastructure.
A fresh agent can be replaced without losing project memory.
A repository can move without destroying Fehrest project identity.
```

## 9. Capability model target

Future agent execution should use explicit leases rather than ambient authority.

Conceptual shape:

```text
CapabilityLease {
  principal
  agent
  session
  tool
  operation
  object_scope
  filesystem_scope
  network_scope
  credential_scope
  process_scope
  cost_budget
  time_budget
  output_budget
  issued_at
  expires_at
  policy_version
  canonical_grant_digest
}
```

Security properties:

```text
deny by default
subagent grant ⊆ parent grant
content cannot widen grant
retrieval cannot widen grant
model cannot mint grant
credentials are separately scoped
expiry is enforced by Core
receipt binds the lease used
```

## 10. Execution receipt target

Every material agent execution should eventually be able to emit an evidence record containing enough information to audit the action without storing secrets.

Conceptual fields:

```text
execution_id
agent_id
session_id
request_digest
tool_id
tool_version
arguments_digest
capability_lease_digest
approval_record
executor_identity
working_scope
started_at
finished_at
exit_status
stdout_digest
stderr_digest
artifact_digests
changed_object_ids
changed_file_digests
network_egress_summary
credential_classes_used
resource_usage
result_class
```

Secrets must never be written into receipts.

## 11. Context is the bridge between Brain and Agent

The defining Fehrest mechanism remains context compilation.

A strong future package may include, as authorized and relevant:

```text
project identity
repository/source identity
current goals
active decisions
superseded decisions needed for explanation
constraints
known gotchas
open work
recent meaningful activity
relevant conversations
relevant knowledge objects
procedures
selected memories
upstream changes relevant to current state
retrieval trace
scope assertions
budget accounting
provenance
```

The package must remain bounded and inspectable. More context is not automatically better context.

The performance objective is:

> **complete relevant working context in seconds, deep evidence on demand, and no hidden loss of durable canonical state.**

## 12. Collaboration architecture principle

Fehrest should support synchronous and asynchronous collaboration without making the collaboration server the owner of user knowledge.

Future collaboration must answer:

```text
What is canonical locally?
What is replicated?
What is merely cached?
Who may mutate what?
How are conflicts represented?
How does a user leave with all canonical data?
How does AI OFF behave?
How does single-machine mode remain complete?
```

No collaboration implementation may silently overturn I-1, I-2, I-7, I-8, or I-9.

A replication constitution is required before multi-user collaboration implementation.

## 13. From conversation to durable knowledge

Fehrest should eventually support explicit promotion flows such as:

```text
conversation -> proposed decision -> reviewed decision -> active canonical decision
conversation -> proposed memory -> verified memory -> active memory
agent finding -> evidence record -> human/automated verification -> accepted state
agent task result -> execution receipt -> review -> task closeout evidence
```

The promotion mechanism, not the model's confidence, determines canonical status.

## 14. Agent-native work model

Agents should be able to participate in project execution while remaining bounded.

A mature agent can potentially:

```text
read authorized project context
search authorized knowledge
inspect repository/upstream state
inspect work items
propose tasks
claim eligible tasks
execute bounded tools
create patches
run tests
post evidence
request review
respond to review
hand work to another agent
summarize a run
propose memories/decisions
```

But:

```text
agent cannot silently widen scope
agent cannot self-approve protected actions
agent cannot promote retrieved content into authority
agent cannot claim completion without required evidence
agent cannot rewrite canonical history to hide failure
```

## 15. Search and command model

One search experience should eventually span authorized subsets of:

```text
knowledge
memory
projects
repositories
work items
conversations
decisions
agents
executions
artifacts
evidence
```

Global search should federate typed domain results rather than collapse all domains into one opaque ranking contract.

## 16. The winning first wedge

The mature destination is broad. The initial wedge remains intentionally narrow:

> **Long-lived technical and research projects that use multiple AI agents and need durable continuity across sessions, IDEs, CLIs, repositories, and model vendors.**

The initial proof loop is:

```text
import or open project
→ compile project context
→ disposable agent works
→ evidence / events / candidate learning
→ reviewed durable state
→ fresh agent continues
```

Workspace breadth follows proof. It does not precede it.

```text
CORE_PROOF_BEFORE_WORKSPACE_BREADTH=YES
```

## 17. Adoption and distribution

Fehrest should not require users to abandon their existing tools.

The initial adoption posture is:

```text
keep GitHub
keep your IDE
keep your CLI
keep your preferred agent/model
add Fehrest as the durable brain
```

A future user should be able to:

```text
find any useful GitHub project
import it into Fehrest without forking
understand it quickly
work with any authorized agent
retain everything important learned by the project
reconcile upstream changes
publish selected work back to GitHub when desired
```

The product earns centrality through compounding project memory and continuity rather than lock-in.

## 18. Product success tests

Fehrest should eventually be judged by outcomes including:

```text
fresh-agent continuation success
cross-runtime continuation success
time to first useful project orientation
context compile P50/P95
constraint miss rate
stale-memory error rate
provenance completeness
human interruption per successful agent task
upstream reconciliation correctness
semantic export fidelity
recovery success
import-to-first-value time
```

The north-star outcome question is:

> **How often can a fresh authorized human or agent continue a real long-lived project correctly, quickly, and with less reconstruction work because Fehrest exists?**

## 19. Final promise

The product promise remains:

> **Your projects remember. Your agents arrive informed. Their authority is bounded. Their work is provable. Your knowledge remains yours.**

And the repository/project relationship is summarized by:

> **GitHub can host the repository. Fehrest should remember the project.**
