# G. Agent Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

> **Agents are disposable. Memory is not.**

Fehrest is what agents connect *to*. It does not own the agent loop, does not host the model, and does not care which agent connects. Its job is to grant bounded access, serve compiled context, accept provenance-tagged memory, and record everything.

---

## 1. Identity

Three distinct identities, deliberately not interchangeable:

| Identity | Lifetime | Purpose |
|---|---|---|
| **Agent** | Persistent | *Which* system connects — `agent:claude`, `agent:codex`, `agent:local-llama`. Registered once |
| **Session** | One connection | The unit of capability grant, audit and provenance |
| **Actor** | Per event | Who caused a specific event: a session, the user, or Fehrest itself |

Branded, non-interchangeable identifier types are adopted from the donor, which deliberately prevents approval ids from being usable as tool-call or session ids ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)). The reason is concrete: id confusion between an approval and a call is exactly how an approval for one action gets replayed onto another.

```json
{
  "session_id": "0198f3a0-...",
  "agent_id": "agent:claude",
  "started_at": "2026-08-17T14:00:00Z",
  "grant": { "...": "frozen at start, see §2" },
  "parent_session": null
}
```

An agent is **not** authenticated as a user. It has no identity of its own beyond what the user granted it. There is no path by which an agent accrues authority across sessions — every session starts from an explicit grant.

---

## 2. Capabilities

### 2.1 Shape

Cedar's decision shape is adopted — `principal + action + resource + context` ([SRC-042](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)) — without adopting the engine yet. The shape is what provides discipline; the engine is a later, separable decision.

```json
{
  "principal": { "session": "0198f3a0-..." },
  "read":   { "scopes": [{ "kind": "project", "id": "0198..." }] },
  "write":  { "scopes": [{ "kind": "project", "id": "0198..." }],
              "types": ["memory:fact", "memory:gotcha", "memory:procedure"] },
  "actions": ["context.compile", "search.query", "object.read",
              "memory.add", "memory.retrieve", "graph.query"],
  "denied":  ["object.delete", "vault.export", "capability.grant", "shell.execute"],
  "limits":  { "max_objects_per_query": 200, "max_context_tokens": 32000,
               "max_memory_writes_per_session": 50 }
}
```

### 2.2 The rules that make it a boundary

1. **Deny by default.** An action absent from `actions` is denied ([I-10](01-ARCHITECTURE-CONSTITUTION.md#i-10--agents-receive-explicitly-bounded-access)). An empty grant permits nothing, including read.
2. **Frozen at session start.** A grant cannot widen in-session. This is what defeats injection-driven escalation: by the time any content is read, the permission set is immutable ([T-1](02-THREAT-MODEL.md#t-1--indirect-prompt-injection-via-imported-document)).
3. **Read and write are separate.** Read access to a scope never implies write access to it.
4. **Subagent grants are strict subsets.** Enforced at creation; delegation can only narrow ([T-14](02-THREAT-MODEL.md#t-14--agent-privilege-confusion-subagent--delegation)).
5. **One chokepoint.** Every tool invocation passes a single authorization function. Enforced by a coverage test asserting no handler is reachable otherwise — a review convention would not survive contact with a growing codebase.
6. **Grants are session-scoped and re-issued, never persisted in reactivatable form** ([T-15](02-THREAT-MODEL.md#t-15--rollback-and-replay-abuse)).

### 2.3 Scopes

`vault` (whole vault — requires explicit user action, never a default) · `project` · `object` · `type` · `time` (a valid-time window).

Scope filtering is applied **during** retrieval at every stage, including graph expansion — never as a post-filter. Graph traversal naturally crosses project boundaries, which is what makes it useful and what makes post-filtering unsafe. Out-of-scope result *counts* are also not leaked, since a count is an oracle ([T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval)).

---

## 3. Tools

Fehrest publishes a small, deliberately narrow tool surface.

| Tool | Access | Notes |
|---|---|---|
| `context.compile` | read | The primary tool. Returns a bounded evidence package ([H](07-CONTEXT-COMPILER-SPEC.md)) |
| `search.query` | read | Lexical + structured, scope-filtered |
| `object.read` | read | **By ID only** |
| `object.list` | read | Metadata only, within scope |
| `memory.retrieve` | read | Temporally resolved |
| `memory.add` | write | Enters as `asserted`; provenance mandatory |
| `memory.update` / `memory.delete` | write | Supersession / retraction — both are events |
| `memory.summary` / `memory.filter` | read | AgeMem's short-term vocabulary ([E-15](research/EVIDENCE_LOG.md#e-15--agemem-is-a-learned-policy-not-a-transplantable-algorithm)) |
| `graph.query` | read | Traversal within scope |
| `object.write` | write | **Requires approval per call.** Never auto-granted |

### 3.1 What Fehrest deliberately does not expose

- **No filesystem tool.** No `read_file`, no `write_file`, no path argument anywhere. Agents address objects by ID; ID→path resolution happens in core. This single decision eliminates the entire path-traversal and symlink attack class at the interface level ([T-7](02-THREAT-MODEL.md#t-7--path-traversal), [T-8](02-THREAT-MODEL.md#t-8--symlink-and-junction-attacks)) rather than defending against it.
- **No shell execution.** Ever, in v1.
- **No network tool.**
- **No raw SQL.**
- **No Graphify MCP passthrough.** The sidecar's own surface (`query_graph`, `get_node`, `god_nodes`, `shortest_path`, `list_prs`, `get_pr_impact`, …) is never re-exported ([E-7](research/EVIDENCE_LOG.md#e-7--graphify-agent-facing-surface)). Re-exporting it would give agents a second, unaudited retrieval path that bypasses the compiler and scope enforcement — and would expose repository/PR tooling irrelevant to a knowledge vault.

The last point generalises: **every additional agent-facing surface is a second path around the boundary.** The tool list stays small on purpose.

### 3.2 Execution pipeline

Adapted from the donor's pre/execute/post structure:

```
request
 → [1] authenticate session
 → [2] AUTHORIZE            ← chokepoint; deny-by-default; grant frozen
 → [3] validate arguments   ← schema; reject paths outright
 → [4] rate/quota check
 → [5] approval if required ← branded ApprovalRequestId; fail closed
 → [6] EXECUTE
 → [7] post-process        ← spill oversized output to a locator
 → [8] record events       ← tool/call + tool/result, immutable
 → response
```

Approval semantics from [E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns): a log-only `asked`/`decided` pair, fail-closed unless explicitly allowed once, and the approval identifier deliberately not interchangeable with the tool-call identifier. Oversized outputs are replaced by an opaque locator, with the donor's two rules adopted verbatim — **the source field is for naming and inspection, not access control**, and **a suggested name is not a path**.

---

## 4. Context delivery and the trust stratification

> **STRENGTHENED IN F1-R1 ([R1-13](reviews/F1-R1-RECONCILIATION.md)).** Model-visible text is **not homogeneous**, and no mechanism may flatten it. Seven levels, per [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable):

| # | Level | Plane | Authority | Writable by |
|---|---|---|---|---|
| 1 | System / owner instruction | instruction | **Authoritative** | Fehrest core only |
| 2 | Trusted Fehrest policy | tool-control | **Authoritative** | Fehrest core only |
| 3 | User instruction | instruction | **Authoritative** | The user, via the UI |
| 4 | Retrieved knowledge (vault) | knowledge | Evidence | Anyone with vault write access |
| 5 | Imported external content | knowledge | **Evidence — assume hostile** | Any source |
| 6 | Tool output | knowledge | **Evidence — assume hostile** | Tools, including remote ones |
| 7 | Agent inference | knowledge | Evidence, marked `INFERRED` | The agent |

**Levels 1–3 may direct behaviour. Levels 4–7 never may**, however authoritative their text sounds. Every item Fehrest emits carries its level, and `test_trust_levels_never_collapsed` asserts no serialisation path erases it.

The distinction between 4 and 5 is not decorative: a note the user wrote and a PDF downloaded last week are both "in the vault," but only one has ever been under the user's editorial control. Collapsing them is how a poisoned import inherits the trust of a personal note.

Everything served to an agent is wrapped in a labelled envelope:

```
<fehrest:evidence
    package="0198f4..."
    compiled_at="2026-08-17T14:05:00Z"
    authority="none">
  <fehrest:item id="0198..." kind="memory" type="constraint"
      trust_level="4" state="USER_CONFIRMED"
      valid_from="2026-06-03" source="0198...#L42">
    Fehrest must never require cloud infrastructure.
  </fehrest:item>
  <fehrest:item id="0198..." kind="excerpt"
      trust_level="5" state="UNRESOLVED"
      source="0198...#p14" origin="import:downloaded-pdf">
    ...imported content, assume hostile...
  </fehrest:item>
</fehrest:evidence>
```

`authority="none"` is machine-readable and consistent across every package; `trust_level` carries the stratification above. The system prompt states that content inside these envelopes is data and that instructions inside it must not be followed.

**This is defence-in-depth, not the boundary.** It is stated here explicitly because conflating the two is the standard error. The actual boundary is that the capability grant was computed before retrieval and cannot change; the envelope only helps a cooperative model behave sensibly ([§1 of the threat model](02-THREAT-MODEL.md#1-governing-principle)).

---

## 5. Transports

| Transport | Status | Notes |
|---|---|---|
| **MCP over stdio** | v1 | Primary. Local process, no network |
| **CLI** (`fehrest context …`) | v1 | Scriptable; same authorization path |
| **MCP over HTTP (loopback)** | Phase 7 | Requires token auth; off by default |
| **SDK** | Post-v1 | — |

**MCP is a transport, not an authorization boundary.** A connected MCP client has no authority until a grant is issued. This is the most commonly violated assumption in the current agent ecosystem and Fehrest's gateway is designed on the opposite assumption ([T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin)).

Because Fehrest speaks MCP, any compliant agent — Claude, Codex, Gemini, GLM, a local model, a future system — connects without Fehrest knowing anything about it. That is the mechanism by which agents become disposable.

---

## 6. Audit and replay

Every session is fully reconstructable from T1/T2 events ([D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)): what was granted, asked, compiled, executed, approved and written.

Three operations:

- **Audit** — "what did `agent:claude` do in project X last week?" Answered from the event log.
- **Replay** — recompile a historical context package and compare digests ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)). Where canonical state has changed since, the mismatch is *reported with the reason*, not hidden: `context/compiled` records the event-sequence high-water mark it was compiled against.
- **Revoke by provenance** — "reject everything `agent:X` asserted in session Y." This is the recovery path for [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning), and it works because provenance is mandatory and unforgeable. Without mandatory provenance, poisoned memory would be unrecoverable — which is why [I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance) is non-negotiable.

Fork and resume are **deferred**. They are useful runtime features, but Fehrest is not the runtime; the agent's own harness owns its loop. Fehrest only needs the durable record.

---

## 7. What Fehrest does not do

| Not Fehrest's job | Whose |
|---|---|
| Run the agent loop | The agent's harness |
| Host or serve models | Provider or local runtime |
| Manage model context windows | The agent |
| Prompt engineering | The agent |
| Execute code or shell commands | The agent's own sandbox |
| Multi-agent orchestration | Out of scope |

Fehrest is memory and context with a boundary. Resisting the pull to become an agent framework is a scope decision that must be defended repeatedly, because every one of the above looks locally reasonable and each would make Fehrest replaceable when the runtime it embedded fell out of fashion — the exact fate the thesis says the memory must survive.

---

## 8. Falsification criteria

| Finding | Consequence |
|---|---|
| Agents cannot work usefully without a filesystem tool | ID-only addressing fails; a scoped, core-mediated file tool must be designed and the traversal class defended directly |
| A grant can be widened in-session by any path | The primary injection boundary is broken; redesign before any release |
| Scope filtering during graph expansion is too slow to be viable | Either expansion is disabled for multi-scope vaults or a scope-partitioned graph is required |
| The approval flow produces so many prompts that users blanket-approve | Approval becomes theatre; re-scope which actions require it |
| Compiled context alone is insufficient and agents always need raw history | The thesis of [H](07-CONTEXT-COMPILER-SPEC.md) is wrong; see [B-7](10-BENCHMARK-PLAN.md) |
