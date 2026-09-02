# Fehrest Donor Batch Study — 2026-09-02

**Status:** NON-AUTHORIZING SOURCE / DONOR RESEARCH  
**Verified:** 2026-09-02  
**Authority:** research and planning only. Nothing in this document authorizes product implementation, dependency adoption, code reuse, graph/vector activation, MCP/ACP, agent runtime work, UI, collaboration, Git import/export, automatic memory, or any R1 mutation.

> `SOURCE_FOUND != SOURCE_ADMITTED`  
> `DONOR_PATTERN != FEHREST_SEMANTIC_OWNER`  
> `COPYABLE != SHOULD_COPY`  
> `PRODUCT_PARITY != ARCHITECTURE_PARITY`

## 1. Batch scope

Founder-supplied sources reviewed in this batch:

```text
semantica-agi/semantica
multica-ai/multica
different-ai/openwork
openclaw/openclaw
koala73/worldmonitor
paperclipai/paperclip
PrimeIntellect-ai/prime-agent
deepseek-ai/deepseek-harness
zeroclaw-labs/zeroclaw
FoundationAgents/OpenManus
every-app/open-seo
```

The final user message contained the last two URLs without a separator. They are treated as two distinct repositories: `FoundationAgents/OpenManus` and `every-app/open-seo`.

## 2. Immutable review anchors

| ID | Repository | Reviewed revision | License posture at reviewed revision | Primary Fehrest value |
|---|---|---|---|---|
| DB-01 | `semantica-agi/semantica` | `909ccf0dedd34b369872e48f0e1fb558580d612e` | MIT | ontology, provenance, deterministic reasoning, decision intelligence, bitemporal/context graph |
| DB-02 | `multica-ai/multica` | `765321f05392bc95750ff5693f62fcc254ad0e94` | custom Multica License: Apache-2.0 text plus material additional restrictions | agents-as-teammates, multi-CLI runtime, issue→run→review, automation principal semantics, attention/inbox |
| DB-03 | `different-ai/openwork` | `7de40102ffedfb3d5955ce520db2e314007efdc1` | MIT outside `ee/`; source-available EE license under `ee/` | portable capabilities, MCP gateway, skills/plugins distribution, desktop/headless workspace, org capability plane |
| DB-04 | `openclaw/openclaw` | `acd861d7c1978dea0dce70787975477c7c482e26` | MIT + third-party notices | gateway/control plane, channels, plugins/skills, device-local assistant, trust boundary patterns |
| DB-05 | `koala73/worldmonitor` | `77676e03d351ce7d8c711eb30ff8235268eea3f5` | AGPL-3.0-only platform; selected thin clients MIT | source catalog, multi-stream intelligence, correlation, freshness, multi-surface SDK/CLI/MCP, trust/data-source UX |
| DB-06 | `paperclipai/paperclip` | `8eaa5caa05e7a36a85a3c04473d879fa83cb98ee` | MIT software | multi-agent organization control plane, atomic task checkout, budgets, approvals, heartbeats, secret injection, portability |
| DB-07 | `PrimeIntellect-ai/prime-agent` | `408e74904bc07434cb50a2882e5ad33a57969bd1` | MIT | continual harness, persistent REPL, durable refinements, goals, heartbeats, direct subagent communication |
| DB-08 | `deepseek-ai/deepseek-harness` | `49a606bc5b5934603f22a26957a07dc799ab0291` | MIT + third-party notices | plugin composition, durable event log, model-visible-means-logged, capability seams, session projection, ACP |
| DB-09 | `zeroclaw-labs/zeroclaw` | `7a919882e34c20a6a7352d29c32ef544a2d56cfd` | MIT OR Apache-2.0; trademark separate | Rust runtime, sandbox/policy, cryptographic tool receipts, channels, SOP engine, ACP, provider/tool/memory seams |
| DB-10 | `FoundationAgents/OpenManus` | `3309bf4e416fb1c74b008f3e86494439a31bad53` | MIT | simple general-agent loop, MCP/browser integration, multi-agent flow reference, browser-computer-use baseline |
| DB-11 | `every-app/open-seo` | `ac9ee482d2b4cd8f472065d6f9b57db35cec560e` | MIT | domain app as agent surface, MCP + skills UX, cost-aware external API use, focused workflow design |

Every future code-reuse decision must refresh the target path, exact revision, license, NOTICE/third-party notices, dependency surface, and security posture.

## 3. Executive conclusion

This donor batch materially strengthens Fehrest's future plan, but it also confirms that Fehrest must **not** become an agent runtime or productivity-suite collage.

The strongest architecture remains:

```text
Fehrest owns:
  canonical temporal project state
  project identity and portability
  durable memory lifecycle
  evidence and provenance
  authority / capability leases
  context compilation and receipts
  semantic export / recovery

Replaceable runtimes and surfaces provide:
  agent loops
  channels
  UI
  plugins
  MCP/ACP
  execution providers
  graph providers
  domain applications
```

This batch adds five especially important ideas to the Fehrest design backlog:

```text
1. PROVENANCE AS A FIRST-CLASS GRAPH / DECISION OBJECT
2. ONE RESOLVED PRINCIPAL PER AUTOMATED RUN
3. MODEL-VISIBLE INPUT MUST BE RECONSTRUCTABLE FROM DURABLE EVENTS
4. ATOMIC TASK CLAIM + BUDGET + EXECUTION OWNERSHIP FOR MULTI-AGENT WORK
5. CONTINUAL LEARNING MUST BE SMALL, REVIEWABLE, EVIDENCE-BACKED, AND ROLLBACKABLE
```

## 4. Detailed donor findings

### DB-01 — Semantica

**Study/benchmark/adapt priority:** VERY HIGH.

Semantica describes itself as graph-native infrastructure for context and accountable AI. Relevant capabilities include context graphs, knowledge graphs, first-class decision records, W3C PROV-O provenance, SHACL/OWL/SKOS ontology governance, conflict detection, bitemporal facts, deterministic forward chaining/Rete/Datalog/SPARQL reasoning, graph analytics, and polyglot RDF/LPG storage.

Strong Fehrest donor value:

```text
DecisionRecord as typed object
Evidence → Fact → Decision provenance chains
Conflict detected instead of silently overwritten
Bitemporal fact representation
Ontology validation and constrained vocabularies
Explainable deterministic inference outside the LLM
Source-preserving entity deduplication
```

Required Fehrest boundary:

```text
ONTOLOGY != CANONICAL AUTHORITY
INFERRED FACT != CONFIRMED FACT
GRAPH PATH != AUTHORIZATION
REASONING OUTPUT != USER GRANT
```

Semantica should be added to the future Phase 3 graph/semantic experiment as an **orthogonal structured-semantics comparator**, not blindly grouped with document GraphRAG systems. It may also influence Phase 4 memory validation and Phase 5 explanation/provenance surfaces.

Potential Fehrest-native superior design:

```text
Canonical typed state
+ provenance graph
+ temporal validity
+ deterministic policy/ontology validation
+ derived inference
+ explicit confirmation/supersession lifecycle
```

rather than making the graph database itself canonical truth.

### DB-02 — Multica

**Study priority:** VERY HIGH.  
**Code-copy posture:** RESTRICTED / SPECIAL LICENSE.

Multica is a workspace where human teammates assign issues to many agent CLIs. Its current README describes 26 agent runtimes, local daemons, squads, skills, projects, execution logs, token usage, review gates, inbox, retries/timeouts, self-hosting, multiple Git hosts, channels, desktop/mobile, CLI/API, and agent permissions.

Its reviewed head is unusually valuable because the current commit documents a real authorization failure class in scheduled automation: admission and execution could resolve different humans/principals. Upstream corrected this by making one immutable trigger creator principal the single answer used by admission, task stamping, delegation, and workspace membership checks; terminal runs are also blocked from spending authority.

This yields a direct Fehrest invariant:

```text
ONE_AUTOMATED_RUN = ONE_RESOLVED_PRINCIPAL
ADMISSION_PRINCIPAL == EXECUTION_PRINCIPAL
DELEGATED_SCOPE <= ORIGINATING_PRINCIPAL_SCOPE
TERMINAL_RUN_CANNOT_START_NEW_PRIVILEGED_WORK
TRIGGER_CONFIG_EDITOR != AUTOMATIC_AUTHORITY_OWNER
```

This is a high-value security donor for Fehrest's future automation, capability lease, and agent gateway specifications.

License caution is material: the reviewed `LICENSE` is not plain Apache-2.0. It adds restrictions on third-party hosted services/commercial embedding and branding/attribution. Treat Multica primarily as **study/benchmark** unless a later path-level rights review says otherwise.

### DB-03 — OpenWork

**Study priority:** HIGH.

OpenWork's strongest Fehrest contribution is the idea that capabilities can be created once and consumed from Codex, Claude Code, Cursor, OpenCode, and other MCP clients. Its remote MCP exposes capability search and execution, while the desktop product is optional. It also supports organization-level capability publishing, skills/plugins, shared/per-user connections, and headless operation.

Fehrest adaptation targets:

```text
Capability Catalog
Capability Search
Capability Assignment
Portable Skill / MCP Connection metadata
Desktop optional; headless first-class
Same project brain consumable from existing agent clients
```

But Fehrest must differ at the authority boundary:

```text
DISCOVERABLE_CAPABILITY != AUTHORIZED_CAPABILITY
ASSIGNED_SKILL != CAPABILITY_LEASE
MCP_CONNECTION != SECRET_ACCESS
```

License caution: everything outside `ee/` is MIT at the reviewed revision; `ee/` has a separate source-available enterprise license. Any donor extraction must be path-specific.

### DB-04 — OpenClaw

**Study priority:** HIGH.

OpenClaw is a local gateway-centered assistant connecting model providers, sessions, tools, events, channels, companion apps, plugins and skills. Its architecture is valuable for multi-surface continuity and channel/device integration.

Fehrest donor targets:

```text
local Gateway / control-plane UX
channel adapters
pairing / sender trust
plugin and skill distribution
control UI + CLI + TUI over one local service
device nodes and companion surfaces
```

Important contrast: OpenClaw's main-session tools can run with host authority unless sandboxing is configured. Fehrest should default more strongly toward capability-bounded execution and explicit receipts for project-changing actions.

Long-term relationship:

```text
OpenClaw can be an Agent Runtime / Surface
Fehrest should remain the durable project brain underneath it
```

### DB-05 — World Monitor

**Study priority:** MEDIUM-HIGH, mainly for intelligence ingestion and source UX.  
**Code-copy posture:** AGPL CAUTION.

World Monitor is not a direct Fehrest product analog. Its value is in operating a high-volume multi-source intelligence system: curated feeds, attributed source catalogs, cross-stream correlation, freshness-aware data, local AI, several product variants from one codebase, MCP/REST/CLI/SDK access, and public agent discovery manifests.

Fehrest donor targets:

```text
SourceCatalog with provenance/licensing/freshness posture
cross-source event correlation
last-good-data preservation instead of empty overwrite
strict-vs-absent source read semantics
multi-surface API/CLI/SDK/MCP parity
agent discovery manifests
source health / freshness visualization
```

The reviewed head itself contains valuable integrity logic: distinguish a genuinely empty upstream result from a parse-clean-but-invalid empty result, preserve last-good rows, and fail strict reads rather than treating remote failure as first-run absence.

Fehrest equivalent:

```text
EMPTY_EVIDENCE != SOURCE_FAILURE
ABSENT != UNREADABLE
NEW_EMPTY_RESULT_CANNOT_SILENTLY_ERASE_LAST_GOOD_CANONICAL_EVIDENCE
```

Platform code is AGPL-3.0-only; thin client packages have MIT exceptions. Reuse must be path/license specific.

### DB-06 — Paperclip

**Study priority:** VERY HIGH.

Paperclip is a control plane for teams of AI agents with goal hierarchy, budgets, governance, heartbeats, atomic task checkout, agent coordination, secrets, workspaces/worktrees, adapters, schedules and audit trails.

High-value Fehrest donor concepts:

```text
atomic task checkout
single-assignee execution lock
agent budgets and hard stops
goal ancestry carried with work
heartbeat/schedule execution
orphaned-run recovery
secret injection separated from ordinary context
company/project/goal/task scoped accounting
portable organization/agent/skill templates
```

Fehrest should **not** adopt Paperclip's organization model as its canonical project brain. Instead Paperclip strengthens Fehrest's future `Work / Coordination / Attention / Budget` domains.

Critical Fehrest extension:

```text
Paperclip: task context continuity
Fehrest: task context + project memory + canonical decisions + temporal truth + evidence + portable brain
```

Paperclip is MIT at the reviewed revision, making selective donor extraction legally simpler than several alternatives, subject to provenance and third-party review.

### DB-07 — Prime Agent

**Study priority:** VERY HIGH for memory and long-running agents.

Prime Agent combines an RLM persistent Python environment with a Continual Harness that stores supplemental prompts, memories, skill descriptions and reusable subagent specifications. `/refine` applies small evidence-backed updates with recorded snapshots/rollback; the base system prompt remains immutable. It also provides persistent goals, daemon-backed continuity, heartbeats, schedules, bounded autonomous mode, and direct agent-to-agent communication.

This is highly aligned with Fehrest's brain thesis.

Adopt as research principles:

```text
LEARNING_UPDATE_SMALL_AND_REVIEWABLE=YES
LEARNING_UPDATE_EVIDENCE_BACKED=YES
LEARNING_HISTORY_ROLLBACKABLE=YES
BASE_POLICY_NOT_SELF_REWRITABLE=YES
GOAL_STATE_FIRST_CLASS=YES
BACKGROUND_CONTINUITY_WITH_BUDGETS=YES
```

But Fehrest must keep the distinction:

```text
SESSION_HARNESS_STATE != PROJECT_CANONICAL_MEMORY
AGENT_REFINEMENT != AUTO_PROMOTION_TO_PROJECT_TRUTH
```

Prime Agent also explicitly warns that its process isolation is not a security sandbox; this supports Fehrest's executor/sandbox separation.

### DB-08 — DeepSeek Harness

**Study priority:** VERY HIGH as an architecture donor.

DeepSeek Harness uses an everything-is-a-plugin architecture built on Cordis. Services, typed events and reversible effects compose through plugin contexts. Its session event log is the source of model history, and it enforces a crucial invariant: **model-visible means logged**. Session projections fold committed events incrementally; capability seams separate service definitions/providers/consumers; tools use guarded pre/execute/post pipelines; ACP is a first-class profile.

This is one of the strongest donors in the whole Fehrest source set.

Direct Fehrest principles:

```text
MODEL_VISIBLE_FEHREST_INPUT => RECONSTRUCTABLE_FROM_DURABLE_RECORD
LIVE_EXTENSION_EVENT != DURABLE_FACT
PROJECTION != SOURCE_OF_TRUTH
CAPABILITY_PROVIDER_SWAP != SEMANTIC_OWNER_SWAP
SESSION_EVENT_SCHEMA_VERSIONED=YES
```

Fehrest should adapt the **event/projection/capability-seam discipline**, not the entire Cordis plugin framework by default.

Because upstream is developer preview with breaking changes, copy/adoption should only occur from an immutable pin and after dependency/security review.

### DB-09 — ZeroClaw

**Study priority:** VERY HIGH for Rust runtime/security patterns.

ZeroClaw is a layered Rust workspace with provider, channel, tool, memory, config, sandbox and hardware crates. It exposes a gateway, dashboard and ACP integration, supports event-triggered SOPs, and documents supervised risk modes, OS-level sandboxing, workspace boundaries and cryptographic tool receipts.

This is an excellent Rust donor for Fehrest's Phase 5/6 boundaries.

Key patterns to study:

```text
risk-classified tool operations
approval gates
Landlock / Bubblewrap / Seatbelt / Docker provider boundaries
cryptographic tool receipts
provider/channel/tool traits
ACP IDE integration
resumable SOP runs
```

Strong conceptual overlap with Fehrest execution receipts makes comparative study mandatory before inventing our own receipt wire format.

However:

```text
ZEROCLAW_TOOL_RECEIPT != FEHREST_EXECUTION_RECEIPT
```

Fehrest's receipt must additionally bind canonical project state, capability lease/grant digest, context receipt, evidence/artifact digests, and project/work identity.

License is permissive dual MIT/Apache-2.0, while trademark rights are separate.

### DB-10 — OpenManus

**Study priority:** MEDIUM.

OpenManus is intentionally simple compared with newer control-plane/harness donors. It remains useful as a minimal general-agent baseline and browser/computer-use integration reference. Current upstream supports a default Browser Use MCP server, terminal execution, MCP mode and an unstable multi-agent flow.

Fehrest use:

```text
simple general-agent benchmark
browser-use / computer-use integration baseline
MCP tool composition example
minimal multi-agent flow comparator
```

Do not adopt its simple API-key configuration or direct agent execution model as Fehrest's security architecture. MIT licensed at reviewed revision.

### DB-11 — OpenSEO

**Study priority:** MEDIUM, but strategically useful for ecosystem design.

OpenSEO is a focused domain product that makes its capabilities available both to humans and AI agents through MCP and reusable skills. Its architecture shows how a vertical application can become an agent-usable capability package without requiring the agent to own the app.

Fehrest implication:

> Fehrest should eventually make **projects and domain tools agent-addressable**, while keeping domain apps replaceable.

Donor targets:

```text
MCP + Skills paired UX
focused workflow packages
BYO external API credential model
cost-aware provider usage
self-host + hosted symmetry
agent-installable skill metadata
```

This can influence Fehrest Hub / extension distribution later. It is not core brain infrastructure.

MIT licensed at reviewed revision.

## 5. Cross-source architecture corrections

### 5.1 Automation principal semantics become a P0 requirement

Multica's active authorization fix demonstrates that scheduled/event-driven work needs one resolved principal across admission and execution.

Future Fehrest automation spec must define:

```text
AutomationDefinition.creator_principal
AutomationRevision.editor_principal
AutomationRun.resolved_principal
AutomationRun.capability_lease
AutomationRun.trigger_evidence
AutomationRun.expiry
```

Editing an automation is not silently equivalent to taking over its future authority.

### 5.2 Event log and context receipt must converge

DeepSeek Harness establishes a strong operational rule: model-visible inputs are reconstructable from the session log. Fehrest already requires receipts. The stronger future rule should be:

```text
MODEL_VISIBLE_FEHREST_INPUT
=> durable source/event references
=> exact transform/compiler version
=> capability/grant binding
=> package digest
=> ContextReceipt
```

A transcript alone is insufficient; the receipt binds project state and authority.

### 5.3 Graph plan expands from retrieval to semantics/provenance

Semantica means Phase 3A should not ask only:

```text
Does graph improve retrieval?
```

It should test separate hypotheses:

```text
G1 structural code/project retrieval value
G2 temporal-memory graph value
G3 provenance/decision explanation value
G4 ontology/conflict-detection value
G5 graph cost / rebuild / incremental burden
```

A negative result on G1 must not automatically falsify G3/G4, but no hypothesis may silently authorize a production graph dependency.

### 5.4 Multi-agent coordination plan strengthens

Paperclip + Multica together support a future Fehrest coordination primitive set:

```text
TaskClaimLease
ExecutionLock
ResourceReservation
BudgetReservation
ReviewOwnership
BlockedOn relation
AgentHeartbeat
RunPrincipal
RunCapabilityLease
RunReceipt
AttentionItem
```

This is stronger than chat-based multi-agent coordination.

### 5.5 Continual learning must be explicit supplemental state

Prime Agent strengthens Fehrest's distinction between immutable base policy and evolving supplemental learning. Future Fehrest should preserve:

```text
Base invariants / policy
Canonical project memory
Candidate learning
Agent-local supplemental harness state
Executable skills
```

as separate classes with separate promotion and review rules.

### 5.6 Source health is a first-class brain property

World Monitor's source-preservation logic reinforces Fehrest's stale-memory work:

```text
SOURCE_UNAVAILABLE != NEGATIVE FACT
EMPTY_PARSE != VALID_EMPTY_SOURCE
LAST_GOOD_EVIDENCE may remain visible with freshness warning
```

Every durable memory that depends on external evidence should be able to surface source health/freshness.

### 5.7 Domain applications should plug into the brain, not own it

OpenSEO demonstrates the long-term ecosystem model:

```text
Fehrest Brain
  ↕ capabilities / evidence / work / receipts
Domain App or MCP Provider
```

not:

```text
Domain App owns memory
```

## 6. Updated donor priority tiers

### Tier A — must study before relevant Fehrest specifications

```text
Semantica
Paperclip
Prime Agent
DeepSeek Harness
ZeroClaw
Multica (architecture/security study; license caution)
Buzz
Graphify
Graphiti
Mem0
Letta
```

### Tier B — strong supporting donors / comparators

```text
OpenClaw
OpenWork
Code-Graph-RAG
Aider
OpenHands
Hermes Agent
Automerge
Docling
E2B
Daytona
```

### Tier C — targeted patterns, ecosystem or vertical-product references

```text
World Monitor
OpenManus
OpenSEO
Microsoft GraphRAG
LightRAG
Firecrawl
LlamaIndex
```

Tier does not imply dependency selection.

## 7. Future source-specific benchmark additions

When canonical governance reaches the relevant phases, add bounded experiments for:

```text
Semantica:
  provenance / ontology / decision explanation vs Fehrest-native typed baseline

Paperclip + Multica:
  duplicate-work prevention
  task-claim race behavior
  automation principal propagation
  approval burden
  budget hard-stop correctness

Prime Agent:
  evidence-backed continual refinement
  cross-session workflow learning
  rollback / stale-refinement behavior

DeepSeek Harness:
  model-visible-input replay completeness
  event-log/projection recovery
  plugin/capability swap behavior

ZeroClaw:
  receipt semantics
  sandbox/provider portability
  risk-policy and approval friction

World Monitor:
  source-health/freshness handling
  last-good evidence preservation
  source-catalog UX
```

## 8. Licensing and reuse matrix

```text
Semantica      MIT                         selective reuse feasible after pin/provenance review
Paperclip      MIT                         selective reuse feasible after pin/provenance review
Prime Agent    MIT                         selective reuse feasible after pin/provenance review
DeepSeek DSH   MIT + third-party notices   selective reuse feasible after notices/dependency review
ZeroClaw       MIT OR Apache-2.0            selective reuse feasible; preserve notices/trademark separation
OpenClaw       MIT + third-party notices   selective reuse feasible after notices review
OpenManus      MIT                         selective reuse feasible after pin/provenance review
OpenSEO        MIT                         selective reuse feasible after pin/provenance review
OpenWork       MIT except ee/              path-level license boundary mandatory
World Monitor  AGPL platform               study/integrate carefully; code embedding may trigger AGPL obligations
Multica        custom restricted license   architecture study preferred unless separate rights review permits reuse
```

This is a repository planning summary, not legal advice. Exact file-level licensing and notices must be reverified before reuse.

## 9. Current authority statement

```text
ACTIVE_EXECUTION_FRONTIER=R1
R1_SEMANTICS_CHANGED=NO
PRODUCT_BEHAVIOR_CHANGED=NO
DONOR_BATCH_RECORDED=YES
DONOR_CODE_COPIED_INTO_PRODUCT=NO
NEW_PRODUCTION_DEPENDENCY_ADMITTED=NO
GRAPH_IMPLEMENTATION_AUTHORIZED=NO
MEMORY_IMPLEMENTATION_AUTHORIZED=NO
MCP_IMPLEMENTATION_AUTHORIZED=NO
ACP_IMPLEMENTATION_AUTHORIZED=NO
AUTOMATION_IMPLEMENTATION_AUTHORIZED=NO
MULTI_AGENT_IMPLEMENTATION_AUTHORIZED=NO
UI_IMPLEMENTATION_AUTHORIZED=NO
```

The next executable Fehrest action remains whatever live `specs/CURRENT.md` permits.
