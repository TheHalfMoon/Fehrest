# Fehrest Product North Star — Agent Brain and AI-Native Work OS

**Status:** NON-AUTHORIZING PRODUCT NORTH STAR  
**Date:** 2026-09-02  
**Authority:** founder product direction captured for planning; implementation remains gated by `specs/CURRENT.md`, canonical execution order, active Spec Kits, benchmark evidence, security review, and explicit gate authority.

## 1. Purpose

Fehrest is intended to become the durable brain and work operating system for humans and AI agents.

The long-term product is not a memory plugin, a note-taking clone, a chat client, a project tracker, or an agent framework. It is the substrate that lets people and agents share durable knowledge, bounded authority, work state, evidence, memory, collaboration, execution, and continuity without surrendering canonical truth to a model, vendor, hosted service, derived index, or transient conversation.

The north-star formulation is:

> **Fehrest is the Agent Brain and AI-native Work OS: durable local-first knowledge, temporal memory, collaboration, execution, planning, agent interoperability, and auditable capability control in one coherent system.**

A second formulation defines the experience target:

> **The calm knowledge depth of Notion and Obsidian, the collaboration velocity of Slack and Buzz, the execution discipline of Linear, and a stronger agent brain than any of them — unified by Fehrest-owned canonical truth, provenance, replay, and authority.**

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
Authority is explicit.
Work is traceable.
Context is compiled.
Knowledge is portable.
Collaboration is first-class.
Execution is receipted.
The user remains the ultimate owner.
```

Fehrest must make a fresh agent materially more capable because the system can provide the right durable state, current decisions, project history, constraints, procedures, evidence, work graph, and bounded tools without leaking ambient authority or forcing the user to reconstruct project context manually.

## 3. What Fehrest becomes

The mature product has seven integrated surfaces over one canonical model.

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
- execution receipts.

### 3.2 Workspace

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

### 3.3 Collaboration

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

### 3.4 Work / Projects

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

### 3.5 Agent Runtime Interoperability

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

### 3.6 Execution

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

### 3.7 Command / Automation Layer

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

## 4. One object model, many views

Fehrest should avoid becoming five disconnected products glued together.

The product should converge on a small number of durable object families with typed relationships and event history. Example conceptual families:

```text
KnowledgeObject
WorkItem
Project
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
View
```

The exact schema is future-spec work, not authorized here.

A Slack-like channel, a Notion-like page, an Obsidian-like note, a Linear-like issue, and an agent run should be able to reference the same project, decision, evidence, and identity graph without duplicating canonical truth.

## 5. The Fehrest differentiation

Fehrest should not win by having more checkboxes than incumbents. It should win because the products it learns from do not share Fehrest's combined invariants.

### 5.1 Versus Slack-class tools

Slack-class tools optimize communication. Fehrest must preserve communication while converting important outcomes into provenance-linked durable state.

Fehrest advantage target:

```text
conversation + canonical decisions + memory + agent context + execution evidence
```

### 5.2 Versus Buzz

Buzz demonstrates a strong human/agent collaboration model, protocol boundaries, agent identity, ACP/MCP integration, signed-event thinking, and hardened tool lifecycle patterns.

Fehrest should learn from those patterns but retain a different center of gravity:

```text
Buzz center: collaborative workspace/event substrate
Fehrest center: durable agent brain/canonical context/authority/evidence substrate
```

Fehrest may later provide collaboration that is competitive with Buzz while preserving stronger separation between evidence and authority, canonical and derived state, capability scope, temporal memory, deterministic context compilation, and replay.

### 5.3 Versus Notion

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

### 5.4 Versus Obsidian

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

### 5.5 Versus Linear

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

### 5.6 Versus standalone agent memory systems

Memory products may retrieve prior information. Fehrest must prove a stronger claim:

> A disposable fresh agent should continue real work more correctly and efficiently because Fehrest compiles bounded, current, provenance-linked state and couples that state to explicit authority and auditable execution.

## 6. Product experience principles

### P-01 — Instant orientation

Opening a project should answer within seconds:

```text
What is this?
What matters now?
What changed recently?
What is blocked?
What decisions are active?
What did agents do?
What needs my attention?
```

### P-02 — One command surface

A global command interface should eventually let a user search, navigate, create, assign, ask, run, approve, review, and inspect without hunting across modules.

### P-03 — Keyboard first, not keyboard only

Power users must be fast. New users must remain oriented.

### P-04 — Calm density

Information-dense does not mean visually noisy. Fehrest should favor calm hierarchy, precise typography, strong focus states, predictable shortcuts, and progressive disclosure.

### P-05 — Agents look like accountable collaborators

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

### P-06 — Nothing important disappears into chat

Important decisions, constraints, tasks, evidence, and memories should be capturable as durable typed state with provenance.

### P-07 — Nothing inferred becomes authority silently

Agent suggestions remain suggestions until canonical policy permits the appropriate promotion path.

### P-08 — Everything critical has receipts

The user should be able to ask:

```text
Why did the agent know this?
Why was it allowed to do this?
What exactly did it execute?
What changed?
Which evidence closed the task?
```

and receive a reconstructable answer.

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
RANK != AUTHORIZATION
RETRIEVED_CONTENT != INSTRUCTION
MODEL_OUTPUT != FACT
CHAT != CANONICAL_STATE
PERMISSION_PROMPT != SANDBOX
REMOTE_SERVICE != CANONICAL_AUTHORITY
AGENT != OWNER
UI != CORE
SYNC != REQUIRED
```

And:

```text
AI_OFF remains a valid core mode.
Local single-machine use remains complete.
Export remains possible without Fehrest infrastructure.
A fresh agent can be replaced without losing project memory.
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
retrieval trace
scope assertions
budget accounting
provenance
```

The package must remain bounded and inspectable. More context is not automatically better context.

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
work items
conversations
decisions
people
agents
runs
commits
artifacts
receipts
external evidence
```

Search results are candidates, never authority. Every result must preserve source identity and trust/provenance metadata where relevant.

## 16. Memory model beyond simple recall

Fehrest memory must support more than facts.

Relevant dimensions include:

```text
static state
dynamic state
workflow/procedure
environment gotcha
premise awareness
semantic memory
procedural memory
episodic memory
project decisions
constraints
failure history
user-confirmed preferences
```

External taxonomies may inform research but may not silently replace Fehrest's canonical model.

## 17. A product quality bar higher than feature parity

Fehrest should not ship a mediocre implementation of every inspiration.

A feature is retained only when it satisfies its own bar:

```text
useful
fast enough
secure enough
understandable
recoverable
auditable
accessible
benchmark-justified where load-bearing
coherent with the product
```

If Fehrest cannot deliver a subsystem at a first-class quality level, it should keep that subsystem narrower rather than ship a broad low-quality clone.

## 18. Product sequence — prove the brain before the shell

The current master plan remains authoritative for dependency order.

The strategic convergence is:

```text
R1 — prove the continuation thesis
↓
Canonical Core — durable identity/journal/recovery/mutation boundaries
↓
Derived Retrieval — disposable incremental retrieval
↓
Graph decision — retain only if measured value exists
↓
Temporal Memory — productize durable memory semantics
↓
Context Compiler + Agent Gateway — defining brain interface
↓
Vertical Proof — prove real agent continuation and safe execution
↓
Desktop Product — expose the proven mechanisms
↓
Collaboration / Work OS expansion — only through separately specified gates
```

This document does not reorder these gates.

## 19. Future product expansion gates

Once the current canonical plan permits post-vertical expansion, future specifications should evaluate product families independently rather than admitting them all at once.

Potential gates include:

### Collaboration Gate

Prove channels/threads/agent participation do not corrupt canonical semantics and that collaboration adds measurable workflow value.

### Work Management Gate

Prove a project/work-item layer can remain a coherent projection over Fehrest canonical objects/events instead of becoming a second truth system.

### Structured Knowledge Gate

Evaluate richer database/view/block functionality only if round-trip/open-format/local-first invariants remain intact.

### Sync Gate

Sync must preserve offline completeness, local canonical ownership, deterministic conflict semantics, and export independence.

### Mobile Gate

Only after a concrete usage case demonstrates that mobile materially improves capture, review, approval, notification, or knowledge access.

### Voice Gate

Voice is an input/output surface, not a replacement for evidence or authorization. It enters only with explicit confirmation semantics for load-bearing actions.

## 20. Donor and competitor map

The long-term product should study donors by capability, not brand worship.

```text
Slack      -> collaboration ergonomics, channels, threads, notifications
Buzz       -> human/agent workspace, ACP/MCP, identity, tool lifecycle, event ideas
Notion     -> flexible workspace, structured knowledge, views, polish
Obsidian   -> local ownership, files, links, extensibility, personal knowledge workflows
Linear     -> speed, keyboard UX, work graph, triage, project execution discipline
Aider      -> context/repo-map baseline
Mem0       -> memory comparator
Letta      -> memory/agent comparator
Graphiti   -> temporal graph comparator
OpenHands  -> agent/runtime comparator
mini-SWE   -> inspectable benchmark harness
OpenSandbox/E2B/Daytona -> execution isolation comparators/providers
```

Every adoption remains `USE / ADAPT / STUDY / BENCHMARK / DEFER / REJECT` with provenance and rights review.

## 21. Success metrics

Star count, screenshots, and feature count are secondary. Fehrest succeeds if users and agents demonstrably work better.

Primary product proof dimensions should eventually include:

```text
continuation correctness
time to orient a fresh agent
repeated-mistake reduction
context token efficiency
retrieval precision/recall where relevant
stale-state error rate
permission-escape rate = 0 under defined threat tests
provenance completeness
receipt completeness
recovery correctness
sync correctness when applicable
human task throughput
review latency
agent handoff success
user control/portability
```

The north-star benchmark remains stronger than a demo:

> Destroy the current agent, start a fresh one, provide no hidden chat history, and determine whether Fehrest lets it continue the real project correctly under a fair context and tool budget.

## 22. What must never happen in pursuit of the vision

Do not achieve breadth by sacrificing the properties that make Fehrest worth building.

Forbidden strategic shortcuts include:

```text
making cloud mandatory
making a hosted model authoritative
making a graph/vector index canonical
letting agent content mint permissions
using chat as the only durable project memory
storing secrets in trajectories or receipts
shipping unrestricted agent filesystem/network access by default
claiming replay when evidence is unreconstructable
hiding benchmark failures
activating UI/product expansion to escape a failed core thesis
copying donor code without provenance/license review
building every competitor feature before proving Fehrest's unique value
```

## 23. Product identity

The mature Fehrest should feel like one product, not a bundle of clones.

Its identity is:

```text
LOCAL-FIRST
AGENT-NATIVE
EVIDENCE-BOUND
TEMPORALLY-AWARE
CAPABILITY-SECURE
AUDITABLE
FAST
CALM
PORTABLE
OPEN
```

The central promise is:

> **Your projects remember. Your agents arrive informed. Their authority is bounded. Their work is provable. Your knowledge remains yours.**

## 24. Immediate implication for current work

This north star changes no current R1 behavior and creates no implementation authority.

The immediate obligations are only:

1. keep R1 scientifically sealed and finish it honestly;
2. preserve the product thesis as falsifiable;
3. ensure future specifications do not accidentally optimize a narrow memory component in a way that prevents the larger Agent Brain / Work OS architecture;
4. keep Rust as the correctness/security core, TypeScript as the primary product surface, and Python as optional research/evaluation/provider tooling;
5. treat the Buzz donor study as one input to a broader product architecture, not as the product definition;
6. make every future expansion earn its complexity through explicit specification, security analysis, evidence, and review.

## 25. Final north star

Fehrest should ultimately make this workflow normal:

```text
A person opens a project.
Fehrest already knows the durable state, history, decisions, constraints, work, and evidence.
A new agent joins with an explicit bounded grant.
The agent receives a compact receipted context instead of months of chat.
The person and agent collaborate in the same workspace.
Knowledge, conversation, tasks, code, runs, and decisions stay connected.
The agent executes only what it is authorized to execute.
Every important action leaves evidence.
Another agent can replace it without losing the project brain.
The user can leave Fehrest and still retain the canonical knowledge in open local form.
```

That is the product Fehrest is planning toward.

```text
VISION_DEFINED=YES
VISION_IMPLEMENTATION_AUTHORIZED=NO
CURRENT_FRONTIER_UNCHANGED=R1
```
