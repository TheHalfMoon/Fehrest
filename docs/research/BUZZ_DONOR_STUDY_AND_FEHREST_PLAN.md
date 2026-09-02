# Buzz Donor Study and Fehrest Integration Plan

**Status:** NON-AUTHORIZING RESEARCH / FUTURE PLANNING  
**Fehrest frontier at study time:** `R1 / REPLACEMENT_VARIANCE_PILOT_EXECUTION`  
**Fehrest base reviewed:** `c64fc4da82b665a40b27b4f4660cb7e64571e6d2`  
**Buzz repository:** `block/buzz`  
**Buzz revision reviewed:** `1c8321cd08feb597f8bcff5195c21148fb3e98ed`  
**Buzz public license:** Apache License 2.0  
**Founder-reported additional source-copy permission:** YES, but future reuse must still preserve auditable source provenance and applicable license/notice obligations.

> This document does not authorize product implementation, MCP integration, UI work, graph/vector work, automatic memory, R1 mutation, scoring, unblinding, or any other action blocked by `specs/CURRENT.md`.
>
> `STUDIED != ADMITTED`  
> `ADAPT CANDIDATE != DEPENDENCY AUTHORIZED`  
> `PLANNED != AUTHORIZED`

---

## 1. Why Buzz matters to Fehrest

Buzz is unusually relevant because it demonstrates several production-grade ideas that intersect with Fehrest's future Phase 5 and Phase 6 goals without requiring Fehrest to become an agent framework or collaboration product.

Buzz's strongest transferable properties are not its social workspace, Nostr relay, or desktop product. They are its hardened agent/runtime boundaries:

```text
ACP client
→ agent runtime
→ permission request
→ MCP tool server
→ bounded execution
```

and its design discipline around:

```text
protocol boundaries
permission correlation
cancellation
process-tree cleanup
bounded output
cross-platform execution
context handoff
agent-first JSON interfaces
```

Fehrest should treat Buzz as a high-value donor for agent interoperability and execution-boundary engineering while preserving Fehrest's core thesis:

```text
Fehrest owns canonical truth, authority, context compilation, provenance, and receipts.
Agent runtimes consume Fehrest outputs; they do not become Fehrest authority.
```

---

## 2. Executive decision

### 2.1 Overall classification

```text
BUZZ_OVERALL=STUDY_AND_SELECTIVE_ADAPT
FULL_FORK=REJECT
FULL_RELAY_ADOPTION=REJECT_FOR_CORE
ACP_AGENT_PATTERNS=ADAPT_CANDIDATE
MCP_TOOL_RUNTIME_PATTERNS=ADAPT_CANDIDATE
PERMISSION_BROKER_PATTERNS=HIGH_PRIORITY_ADAPT_CANDIDATE
PROCESS_LIFECYCLE_PATTERNS=HIGH_PRIORITY_ADAPT_CANDIDATE
CONTEXT_HANDOFF_PATTERNS=STUDY_AND_BENCHMARK
CLI_JSON_CONVENTIONS=ADAPT_CANDIDATE
NOSTR_CORE_DEPENDENCY=DEFER_OR_REJECT_UNLESS_WORKSPACE_REQUIREMENT_EMERGES
BUZZ_DESKTOP=STUDY_ONLY_UNTIL_PHASE_7
```

### 2.2 Strategic conclusion

Fehrest should not become "Buzz with different branding."

The stronger opportunity is:

> **Fehrest becomes the evidence-bound context and capability plane that can safely serve many agent runtimes, including ACP/MCP-compatible agents, without giving any model or external tool authority over canonical state.**

This direction is stronger than a direct Buzz fork because it preserves Fehrest's differentiator: deterministic, auditable, replayable, scope-bound context and authority.

---

## 3. Buzz architecture findings

### 3.1 What Buzz is

Buzz is a Rust monorepo with a relay-centric architecture. The relay is the single source of truth for its workspace. Human actions, agent actions, workflows, git events, and collaboration events are represented as signed Nostr events.

Its current workspace includes focused crates for relay, protocol, database, auth, pub/sub, search, audit, workflows, ACP agent integration, MCP tooling, CLI, media, git signing, voice, Kubernetes integration, and more.

This architecture is coherent for Buzz's goal: a self-hostable human/agent workspace.

It is not automatically the correct architecture for Fehrest.

### 3.2 What Buzz does particularly well

The most valuable implementation properties observed are:

```text
- ACP as the agent-facing protocol boundary
- MCP as the tool-facing protocol boundary
- explicit permission request lifecycle before tool execution
- global cap on pending permission asks
- correlation IDs claimed before wakeup
- late/unknown permission responses ignored safely
- fail-closed behavior on malformed/undeliverable permission responses
- single absolute permission deadline
- cancellation racing every wait path
- abort-safe correlation cleanup
- per-call shell process lifecycle
- process-group / Windows Job Object cleanup
- bounded stdout/stderr presented to the model
- larger retained output artifacts outside the immediate model window
- explicit execution timeouts
- cross-platform shell resolution
- atomic text replacement tool
- context-compaction lifecycle hooks
- agent-first CLI design with machine-readable I/O
```

### 3.3 Where Buzz should not be copied blindly

Buzz's scope has expanded substantially. Its agent subsystem is no longer merely two tiny crates conceptually; it contains large provider, auth, catalog, configuration, capability, permission, wire, handoff, and orchestration modules.

Blind copying would risk importing:

```text
- product assumptions Fehrest does not need
- eager or heavyweight MCP lifecycle choices
- credential-scope complexity
- workspace/relay coupling
- social/messaging semantics
- Nostr-specific identity decisions
- multi-community tenancy concerns
- desktop/UI complexity before Fehrest's proof gates
```

Fehrest must therefore donor-extract by requirement, not by directory.

---

## 4. Donor matrix

| Buzz area | Fehrest classification | Reason | Earliest Fehrest phase where it may matter |
|---|---|---|---|
| `buzz-agent` ACP wire/session lifecycle | ADAPT CANDIDATE | Strong protocol-native agent interface | Phase 5 |
| permission broker | HIGH-PRIORITY ADAPT CANDIDATE | Fail-closed tool-call authorization lifecycle | Phase 5 |
| `buzz-dev-mcp` shell lifecycle | HIGH-PRIORITY ADAPT CANDIDATE | Hardened cancellation/process cleanup/output bounds | Phase 5/6 |
| `read_file` / `str_replace` tool shapes | STUDY / POSSIBLE ADAPT | Minimal, inspectable tool contracts | Phase 5/6 |
| `_Stop` / `_PostCompact` hooks | BENCHMARK | Useful continuity semantics but must not become authority | Phase 5/6 |
| handoff/context compaction | BENCHMARK | Relevant to continuation quality and token cost | Phase 6 |
| model capability normalization | STUDY | Useful provider interoperability, but Fehrest is model-optional | Phase 5/6 |
| `buzz-cli` JSON-first UX | ADAPT CANDIDATE | Good agent/tool interoperability | Phase 5 |
| relay event pipeline | STUDY ONLY | Good event discipline, mismatched to Fehrest core | No default adoption |
| Nostr event identity | DEFER | Only justified by future multi-party workspace requirements | Not in current plan |
| Nostr-signed git | STUDY | Interesting provenance mechanism, not required by current thesis | Future optional research |
| Redis pub/sub | REJECT AS CORE REQUIREMENT | Not needed for deterministic local canonical core | N/A |
| Postgres relay store | REJECT AS CORE REQUIREMENT | Fehrest canonical core must retain its own storage semantics | N/A |
| media / voice / channels | REJECT FOR CORE | Outside Fehrest thesis | Phase 7+ only if product evidence demands |
| Kubernetes backend | DEFER | Deployment concern, not context/core correctness | Post-proof operations |
| Buzz desktop | STUDY ONLY | UI remains blocked until Fehrest Phase 7 entry | Phase 7 |

---

## 5. Fehrest target architecture informed by Buzz

Buzz reinforces the value of clean protocol boundaries, but Fehrest should add a stricter authority and evidence layer.

The target conceptual stack is:

```text
┌──────────────────────────────────────────────────────────────┐
│ Client / Agent Surfaces                                      │
│ CLI · ACP client · IDE · future desktop · automation         │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Fehrest Agent Gateway                                        │
│ request binding · immutable grant · context receipt          │
│ adapter lifecycle · session scope · replay metadata          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Capability / Permission Plane                                │
│ canonical authority → derived execution lease                │
│ deny-by-default · subset delegation · expiry · budgets       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Tool Protocol Plane                                          │
│ MCP adapters · native adapters · lazy tool-server lifecycle  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Execution Plane                                              │
│ native · container · WASI · remote provider                  │
│ bounded process/output/network/credential scope              │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Evidence Plane                                               │
│ execution receipt · context receipt · selection trace        │
│ artifact hashes · changed resources · replay classification  │
└──────────────────────────────────────────────────────────────┘
```

Fehrest's canonical state remains outside and above this stack. No tool execution, ACP client, MCP server, model output, event stream, or receipt can mint canonical authority.

---

## 6. Capability model: stronger than a yes/no permission prompt

Buzz's permission broker is a strong lifecycle donor, but Fehrest should not stop at a binary `allow/deny` decision.

A future Fehrest capability lease should bind the exact authority projected into one execution context.

Conceptual schema:

```text
CapabilityLease {
    lease_id
    schema_version
    principal_id
    agent_id
    session_id
    tool_provider
    tool_name
    operation_class
    canonical_grant_digest
    resource_scope
    filesystem_scope
    network_scope
    credential_scope
    process_scope
    cost_budget
    time_budget
    output_budget
    issued_at
    expires_at
    parent_lease_id?
    policy_version
    receipt_policy
}
```

Hard rules:

```text
MODEL_CONTENT_CANNOT_MINT_LEASE=YES
TOOL_OUTPUT_CANNOT_EXPAND_SCOPE=YES
SUBAGENT_SCOPE_SUBSET_ONLY=YES
LEASE_EXPIRES=YES
AMBIENT_FULL_MACHINE_AUTHORITY=NO_BY_DEFAULT
SECRETS_IN_CONTEXT=NO
RESOURCE_PATH_FROM_MODEL=NOT_AUTHORITY
```

This should integrate with the already-planned Phase 5 immutable session-grant model instead of creating a parallel authorization system.

---

## 7. Permission broker donor requirements

If Buzz permission-broker code or structure is later adapted, Fehrest should preserve at least these invariants:

```text
P-01 global cap on pending authorization requests
P-02 admission before correlation-state insertion
P-03 abort-safe cleanup of correlation state and capacity
P-04 correlation identity is monotonic/non-reused during process lifetime
P-05 claim/remove before waiter wakeup
P-06 unknown and late responses cannot authorize a new request
P-07 malformed response fails closed
P-08 closed permission-response wire fails closed immediately
P-09 one absolute deadline covers admission + enqueue + response wait
P-10 cancellation races admission, enqueue, and response wait
P-11 non-authorizing outcomes are explicit and model-visible
P-12 policy remains outside the model and tool content
```

Fehrest additions:

```text
P-13 decision binds canonical grant digest
P-14 decision binds exact tool + normalized argument digest
P-15 approval cannot outlive capability lease
P-16 approval result is included in execution receipt
P-17 approval cannot silently widen network/credential/filesystem scope
P-18 replay can distinguish authorized-but-not-executed from executed
```

---

## 8. Lazy MCP lifecycle

Fehrest should improve on the common eager-MCP pattern.

Future MCP servers should be demand-started when practical:

```text
COLD
→ STARTING
→ READY
→ BUSY
→ IDLE
→ HIBERNATED / STOPPED
```

Required behavior:

```text
- per-agent MCP allowlist
- per-session server isolation where required
- no server starts merely because it is globally configured
- idle eviction / hibernation policy
- bounded startup retry
- bounded resident process count
- explicit health state
- credential set isolated by server identity
- environment constructed from explicit allowlist, not ambient inheritance
- MCP process cannot silently become a canonical authority source
```

Benchmark before adopting process-per-session versus shared-safe-server models. Resource footprint, isolation quality, latency, and failure blast radius all matter.

---

## 9. Execution plane

Buzz provides strong native process lifecycle ideas. Fehrest should preserve those properties while supporting multiple execution backends.

Future interface concept:

```rust
trait Executor {
    async fn execute(
        &self,
        request: ExecRequest,
        capability: CapabilityLease,
    ) -> Result<ExecReceipt, ExecError>;
}
```

Possible providers:

```text
NativeExecutor
ContainerExecutor
WasiExecutor
RemoteSandboxExecutor
```

These are provider candidates, not current dependencies.

### 9.1 Minimum native-execution invariants

```text
- timeout on every execution
- cancellation on every execution
- process-tree ownership
- descendant cleanup on success, failure, timeout, cancellation, and drop
- bounded stdout/stderr delivered to model
- larger output artifacts retained separately when needed
- explicit working directory
- no implicit `cd` state between calls
- explicit environment construction
- secret redaction and secret-class tracking
- command and argument size limits
- cross-platform behavior tested on Windows/macOS/Linux
```

### 9.2 Isolation policy

Native execution is not equivalent to sandboxing.

Fehrest must state this explicitly in every provider contract:

```text
PROCESS_LIFECYCLE_HARDENED != SECURITY_SANDBOXED
```

Where strong isolation is required, prefer a separately qualified sandbox provider rather than pretending process-group cleanup provides containment.

---

## 10. Execution receipts

Buzz's bounded execution artifacts combine well with Fehrest's existing receipt-first architecture.

Every future agent-visible or agent-triggered execution should be capable of producing an execution receipt such as:

```text
ExecutionReceipt {
    schema_version
    execution_id
    request_digest
    principal_id
    agent_id
    session_id
    context_receipt_digest?
    capability_lease_digest
    approval_digest?
    tool_provider
    tool_name
    normalized_argument_digest
    executor_provider
    executor_version
    workdir_identity
    started_at
    finished_at
    terminal_status
    exit_code?
    timeout_status
    cancellation_status
    stdout_digest?
    stderr_digest?
    retained_artifact_digests[]
    changed_resource_set_digest?
    network_egress_summary_digest?
    credential_class_set_digest?
    policy_version
}
```

Important distinction:

```text
RECEIPT=EVIDENCE
RECEIPT!=AUTHORITY
```

The receipt proves what Fehrest observed under a given authorization state. It does not retroactively make an unauthorized action valid.

---

## 11. Context handoff and compaction

Buzz's handoff/compaction design is relevant to Fehrest's continuation thesis, but it must be benchmarked rather than adopted by taste.

Future Phase 6 experiment candidates:

```text
A. no compaction until hard context limit
B. deterministic extractive handoff
C. Fehrest context compiler refresh from canonical state
D. model-generated summary with full provenance and explicit derived status
E. hybrid deterministic state + model narrative summary
```

Key Fehrest rule:

```text
SUMMARY_OUTPUT=DERIVED_CONTEXT
SUMMARY_OUTPUT!=CANONICAL_MEMORY
```

A model-generated handoff may never silently become user-confirmed memory or authorization state.

Measure:

```text
continuation correctness
task completion
missed constraints
hallucinated state
recovery after compaction
context tokens
latency
cost
replayability
```

---

## 12. CLI and agent interoperability

Buzz's agent-first JSON CLI is a useful pattern.

Fehrest's future gateway should support stable machine-readable interfaces before polished human UI.

Candidate principles:

```text
- JSON in / JSON out mode
- typed stable envelopes
- explicit schema version
- no ANSI/noise in machine mode
- deterministic exit-code classes
- receipt identity returned on successful context or execution operations
- structured error classes
- no hidden state mutation
- `--json` support for all agent-critical commands
```

Potential adapter targets remain:

```text
ACP
MCP
Codex
Claude Code
Hermes
Zed/JetBrains ACP clients
OpenHands / mini-SWE-agent where useful for evaluation
```

Fehrest should prefer protocol adapters over importing whole agent frameworks.

---

## 13. Nostr and signed event logs

Buzz shows that a signed append-oriented event substrate can unify collaboration, identity, and audit.

That does not mean Fehrest should adopt Nostr now.

Current decision:

```text
NOSTR_FOR_FEHREST_CORE=NOT_JUSTIFIED
```

Reasons:

```text
- Fehrest's current thesis does not require a social/workspace relay
- canonical state already has its own identity and journal requirements
- adding a second identity/event substrate would increase complexity
- Phase 1 requires Fehrest-owned event-journal convergence first
```

Reconsider only if a later measured requirement appears for multi-party signed workspace events, portable agent identity, or federated collaboration where Nostr materially outperforms simpler signed-event designs.

---

## 14. Source-copy and provenance discipline

The public Buzz repository is Apache-2.0. The founder also reports additional permission to copy the full source. Fehrest should nevertheless preserve a strict donor ledger for any future copied or adapted code.

For every copied/adapted file or coherent code fragment, record:

```text
DONOR_REPOSITORY=block/buzz
DONOR_REVISION=<immutable commit>
DONOR_PATH=<path>
DONOR_BLOB_SHA=<git blob when available>
DONOR_LICENSE=Apache-2.0
COPY_MODE=VERBATIM | MODIFIED | STRUCTURAL_ADAPTATION
LOCAL_DESTINATION=<path>
LOCAL_CHANGE_SUMMARY=<summary>
ATTRIBUTION_RETAINED=YES
NOTICE_REVIEW=<status>
SECURITY_REVIEW=<status>
DEPENDENCY_DELTA=<status>
```

Rules:

```text
- never copy from moving `main` without pinning an immutable commit
- preserve required copyright/license/notice material
- mark modified files clearly when required
- do not imply Block sponsorship or endorsement
- do not use Block trademarks as Fehrest branding
- re-review third-party transitive dependencies rather than assuming Buzz's acceptance transfers automatically
- donor permission does not waive Fehrest architecture/security/benchmark gates
```

---

## 15. Proposed future code ownership

If the Phase 5 gateway is later authorized, keep donor-derived concerns separated from canonical core concerns.

Conceptual ownership only:

```text
fehrest-core/
  canonical state
  journal
  identity
  context compiler
  grants
  receipts

fehrest-agent-gateway/
  ACP adapter
  session binding
  capability projection
  approval broker
  MCP lifecycle

fehrest-exec/
  execution provider traits
  native executor
  output/artifact capture
  process lifecycle

fehrest-mcp-adapter/
  MCP protocol integration
  server registry
  lazy lifecycle

fehrest-cli/
  machine-readable user/agent interface
```

This is a planning sketch, not crate authorization.

---

## 16. Security requirements derived from the study

Buzz strengthens several future Fehrest threat-model requirements.

### 16.1 Tool-call authority confusion

Threat:

```text
model emits a plausible tool call
→ system mistakes syntactic validity for authority
```

Required defense:

```text
canonical grant
→ capability projection
→ approval/policy decision where required
→ tool execution
→ receipt
```

### 16.2 Credential bleed between tool servers

Threat:

```text
MCP server A receives credentials intended only for server B
```

Required defense:

```text
CREDENTIAL_ENVIRONMENT=EXPLICIT_ALLOWLIST_PER_SERVER
AMBIENT_SECRET_INHERITANCE=NO_BY_DEFAULT
```

### 16.3 Eager tool-server resource exhaustion

Threat:

```text
configured agents × configured servers
→ resident process explosion
```

Required defense:

```text
lazy start
resident caps
idle eviction
health accounting
per-agent server selection
```

### 16.4 Cancellation leakage

Threat:

```text
agent turn cancelled
→ child process or permission waiter survives
```

Required defense:

```text
abort-safe leases
process-tree ownership
bounded reap
correlation cleanup
```

### 16.5 Tool output as authority

Threat:

```text
tool says "approved" or emits a path
→ model/system treats output as a capability grant
```

Required invariant:

```text
TOOL_OUTPUT=EVIDENCE_ONLY
TOOL_OUTPUT_CANNOT_MINT_AUTHORITY
```

---

## 17. Benchmark plan for Buzz-derived adoption

No donor code should enter production solely because it looks mature.

### 17.1 Permission broker qualification

Test:

```text
late response
unknown response id
duplicate response
malformed response
wire closure
permission timeout
admission saturation
cancellation during admission
cancellation during enqueue
cancellation during response wait
task abort
process-wide pending cap
```

Pass only if every unauthorized or ambiguous case fails closed and no correlation/capacity leak remains.

### 17.2 Native executor qualification

Cross-platform matrix:

```text
Ubuntu
macOS
Windows
```

Cases:

```text
normal exit
non-zero exit
large stdout
large stderr
UTF-8 and binary-ish output boundaries
timeout
cancellation
child process
child + grandchild
shell missing
invalid workdir
secret-shaped output redaction tests
artifact retention limits
```

### 17.3 MCP lifecycle benchmark

Compare:

```text
eager process-per-session
lazy process-per-session
safe shared server
hibernated/restarted server
```

Measure:

```text
startup latency
steady RAM
process count
failure isolation
credential isolation
cleanup correctness
tool-call latency
```

### 17.4 Context handoff benchmark

Use continuation tasks and compare against the Phase 6 baseline ladder. Do not tune on hidden confirmatory tasks.

---

## 18. Integration into the existing Fehrest execution order

This study does **not** change `docs/canonical/EXECUTION_MASTER_PLAN.md` ordering.

It maps onto the existing plan as follows:

### R1

```text
NO CHANGE
```

Buzz research must not affect the sealed experiment, replacement execution, scoring, power analysis, confirmatory work, or terminal verdict.

### Phase 1 — Canonical Core Convergence

```text
NO BUZZ CODE REQUIRED
```

Finish Fehrest-owned vault identity, mutation ownership, and production event journal first.

### Phase 2 / Phase 3 / Phase 4

```text
NO DEFAULT BUZZ DEPENDENCY
```

Derived retrieval, graph decision, and temporal memory remain governed by their own evidence.

### Phase 5 — Context Compiler and Agent Gateway

This is the earliest main adoption point.

Candidate Buzz-derived work:

```text
ACP adapter patterns
permission-broker lifecycle
MCP protocol adapter
lazy MCP server lifecycle
machine-readable CLI conventions
capability-to-tool-call binding
execution receipt binding
```

### Phase 6 — Vertical Proof

Candidate Buzz-derived evaluation work:

```text
native executor provider
context handoff/compaction comparator
ACP runtime interoperability
MCP resource/lifecycle benchmarks
permission adversarial tests
```

### Phase 7 — Desktop

Buzz desktop patterns may be studied only after Phase 7 entry criteria are satisfied. No current UI authority is created.

---

## 19. Fehrest differentiators to protect

Any Buzz-derived implementation must preserve these Fehrest advantages:

```text
1. deterministic AI-OFF canonical core
2. canonical state separate from derived state
3. explicit temporal truth and lifecycle semantics
4. model-visible context bound to receipts
5. immutable session grants
6. scope enforced before retrieval and execution
7. model/tool content cannot mint authority
8. replay classifications are honest: IDENTICAL / DIVERGED / UNRECONSTRUCTABLE
9. donor systems remain replaceable providers
10. benchmark outcomes, not architecture enthusiasm, decide retention
```

If donor reuse weakens one of these, donor reuse loses.

---

## 20. Future adoption gates

Buzz-derived code becomes eligible only after all applicable gates pass:

```text
G1 requirement exists in an active authorized spec
G2 Ponytail necessity gate says custom/adaptation work is justified
G3 exact donor revision/path/blob provenance recorded
G4 license/notice review PASS
G5 dependency delta reviewed
G6 threat-model impact reviewed
G7 smallest useful donor slice selected
G8 implementation remains within active spec authority
G9 unit/property/adversarial tests PASS
G10 cross-platform qualification PASS where relevant
G11 benchmark shows acceptable value/cost
G12 independent review PASS
G13 convergence confirms no unnecessary donor coupling
```

No full-tree copy is the default.

---

## 21. Concrete post-R1 planning backlog

This backlog is deliberately dormant while R1 remains open.

```text
BZZ-001 Re-verify Buzz donor revision and current architecture before Phase 5 planning
BZZ-002 Build exact donor provenance ledger for selected files only
BZZ-003 Specify Fehrest CapabilityLease schema
BZZ-004 Specify tool-call authorization state machine
BZZ-005 Specify ExecutionReceipt schema and binding rules
BZZ-006 Benchmark permission-broker design with adversarial concurrency cases
BZZ-007 Specify lazy MCP lifecycle and per-agent server selection
BZZ-008 Define explicit per-server credential environment contract
BZZ-009 Define Executor provider trait and native provider contract
BZZ-010 Cross-platform process-tree cleanup experiment
BZZ-011 Define ACP adapter boundary without importing agent-framework authority
BZZ-012 Define JSON CLI envelope/exit-code contract
BZZ-013 Benchmark context handoff/compaction alternatives
BZZ-014 Decide whether any Buzz code should be copied verbatim versus structurally reimplemented
BZZ-015 Only after evidence: admit the minimum donor slice into the active implementation spec
```

Task identifiers in this research document are planning labels only. They are not Spec Kit task authority.

---

## 22. Non-goals

This study does not authorize Fehrest to become:

```text
- a Slack replacement
- a Nostr social relay
- a git forge
- a voice/video product
- a general workflow SaaS
- a Kubernetes orchestration platform
- an agent framework that owns canonical truth
```

Fehrest may interoperate with such systems later while keeping its own boundary narrow.

---

## 23. Final recommendation

Use Buzz aggressively as a **donor of hardened boundary engineering**, not as a product template.

Highest-value future extraction order:

```text
1. permission broker invariants
2. process-tree / cancellation / bounded-output execution patterns
3. ACP session/wire adapter patterns
4. MCP lifecycle and tool-server boundaries
5. machine-readable CLI conventions
6. context handoff ideas as benchmark candidates
7. selected desktop patterns only after Phase 7 authorization
```

Keep outside Fehrest core unless a future requirement proves otherwise:

```text
Nostr relay
social/channel model
media/voice
workflow workspace
multi-community tenancy
Kubernetes deployment machinery
full Buzz agent product stack
```

The target is not maximum code reuse. The target is maximum verified leverage with minimum new authority surface.

```text
DONOR_VALUE > DONOR_COMPLEXITY
OR
DONOR=REJECT
```

---

## 24. Current authority statement

At the time of this study:

```text
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
BUZZ_RESEARCH_RECORDED=YES
BUZZ_PRODUCTION_DEPENDENCY_ADMITTED=NO
BUZZ_CODE_COPIED_INTO_PRODUCT=NO
MCP_IMPLEMENTATION_AUTHORIZED=NO
ACP_IMPLEMENTATION_AUTHORIZED=NO
AGENT_GATEWAY_IMPLEMENTATION_AUTHORIZED=NO
UI_IMPLEMENTATION_AUTHORIZED=NO
R1_SEMANTICS_CHANGED=NO
PRODUCT_BEHAVIOR_CHANGED=NO
```

The next executable Fehrest action remains the live R1 gate from `specs/CURRENT.md`.