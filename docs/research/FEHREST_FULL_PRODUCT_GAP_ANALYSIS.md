# Fehrest Full Product Gap Analysis and Architecture Corrections

**Status:** NON-AUTHORIZING PRODUCT / ARCHITECTURE RED-TEAM  
**Date:** 2026-09-02  
**Authority:** planning only; implementation remains controlled by `specs/CURRENT.md`, the canonical execution order, active Spec Kits, evidence gates, and required reviews.  
**Active frontier at analysis time:** `R1 / REPLACEMENT_VARIANCE_PILOT_EXECUTION`

> This document intentionally searches for reasons Fehrest could fail even if individual subsystems are well engineered.
>
> It does not authorize UI, collaboration, sync, MCP, ACP, automatic memory, graph, vector, agent execution, Git import/export, hosted storage, or any post-R1 product behavior while those remain blocked.

---

## 1. Executive conclusion

The Fehrest north star is strong, but the product would still fail if it were implemented as a feature union of Slack, Buzz, Notion, Obsidian, Linear, GitHub, and an agent memory system.

By 2026, incumbents already overlap heavily:

- knowledge workspaces orchestrate internal and external agents;
- collaboration products expose agents as teammates inside channels and DMs;
- issue trackers increasingly let agents triage, implement, review, and automate work;
- coding-agent products already operate multiple agents in parallel;
- memory systems increasingly support temporal reasoning, consolidation, and long-lived learning;
- Git forges already dominate repository transport, review, and publication.

Therefore this is not enough:

```text
Slack + Notion + Obsidian + Linear + GitHub + agents
```

The stronger product thesis is:

> **Fehrest is the continuity and governed-action substrate for long-lived projects: it preserves what the project knows, what remains true, what work is active, where the project came from, what authority each actor has, why an action was permitted, what was executed, and what evidence proves the result — across disposable agents, models, tools, devices, repositories, IDEs, CLIs, and vendors.**

The product hierarchy should be:

```text
1. CONTINUITY
2. CANONICAL TRUTH
3. PROJECT PORTABILITY
4. GOVERNED ACTION
5. EVIDENCE / REPLAY
6. HUMAN + AGENT COORDINATION
7. KNOWLEDGE / WORK UX
8. OPTIONAL AUTOMATION / INTELLIGENCE
```

The lower layers must never be allowed to reverse the authority of the higher layers.

---

## 2. Strategic gap set

### Gap G-001 — Feature aggregation is no longer differentiation

**Severity:** P0  
**Risk:** Fehrest becomes an impressive but replaceable all-in-one workspace.

Every major feature must strengthen at least one of:

```text
CONTINUITY
PORTABILITY
AUTHORITY
PROVENANCE
REPLAYABILITY
```

A feature that improves none of them is optional product surface, not core architecture.

### Gap G-002 — The mature vision is much wider than the first winning wedge

**Severity:** P0

The initial wedge remains:

> **Long-lived technical/research projects that use multiple AI agents and need durable continuity across sessions, IDEs, CLIs, repositories, and vendors.**

Initial loop:

```text
import/open project
→ project orientation
→ Fehrest context
→ disposable agent works
→ evidence / events / proposed memories
→ reviewed durable state
→ fresh agent continues
```

```text
CORE_PROOF_BEFORE_WORKSPACE_BREADTH=YES
```

### Gap G-003 — "One object model" can become a universal-object anti-pattern

**Severity:** P0

Correction:

```text
one canonical kernel
+ strongly typed domain objects
+ typed relations
+ typed events
+ many views
```

```text
UNIVERSAL_MUTABLE_PROPERTY_BAG=NO
```

### Gap G-004 — Local-first and Slack-class collaboration are in structural tension

**Severity:** P0

A replication constitution is required before multi-user collaboration implementation. It must define authoritative mutation units, offline writers, causality, conflict representation, export, private/local-only state, and remote-agent behavior without making the server canonical authority.

```text
COLLABORATION_REPLICATION_CONSTITUTION_REQUIRED=YES
```

### Gap G-005 — Memory risks being treated as a store instead of a learning lifecycle

**Severity:** P0

Required lifecycle:

```text
Raw Experience
→ Trajectory / Event Evidence
→ Candidate Memory / Procedure / Gotcha / Decision
→ Verification / Corroboration / Human Confirmation
→ Durable Canonical State
→ Use / Feedback
→ Supersession / Retraction / Consolidation
```

Automatic extraction never skips candidate state.

### Gap G-006 — No explicit safe background consolidation architecture

**Severity:** P1

Consolidation may propose merges, supersession, procedure extraction, recurring gotchas, summaries, and retention candidates, but may not silently rewrite canonical history.

### Gap G-007 — Experiential learning needs a first-class trajectory format

**Severity:** P1

```text
TRAJECTORY != MEMORY
TRAJECTORY != AUTHORITY
```

A future open trajectory representation should normalize sessions from multiple runtimes while preserving source-fidelity and receipt references.

### Gap G-008 — Context quality needs marginal-value economics

**Severity:** P0

Fehrest must optimize correct continuation per token, latency, cost, and human interruption—not maximum retrieval volume.

### Gap G-009 — Different agents need different context without sacrificing replay

**Severity:** P1

Future `ContextProfile` policy should bind role, source classes, recency, mandatory items, optional retrievers, compression policy, and budgets. Personalization remains deterministic given canonical state + policy + compiler version + budget.

### Gap G-010 — Agent identity needs security-grade lifecycle semantics

**Severity:** P0

Distinguish logical agent identity, runtime instance, model, provider, host, environment, credential principal, human sponsor, session, and software version.

```text
DISPLAY_IDENTITY != SECURITY_PRINCIPAL
```

### Gap G-011 — Multiple agents require coordination control, not only chat

**Severity:** P0

Need task-claim leases, resource reservations, environment/worktree identity, conflict signals, shared budgets, dependency blocking, review ownership, handoff, and stale-work detection.

### Gap G-012 — Human attention is a scarce resource and needs its own plane

**Severity:** P0

A future Attention Inbox should group approvals, blocked agents, conflicts, review-ready work, decision proposals, memory confirmations, budget exceptions, failed automations, and security events with clear risk and consequence summaries.

### Gap G-013 — Binary approval is too weak for long-running automation

**Severity:** P0

Support bounded approval forms such as once, operation-class within scope, task-only, time/budget-limited, reduced scope, second reviewer, pause, escalate, and revoke.

### Gap G-014 — Secret custody is under-specified

**Severity:** P0

Separate secret storage, eligibility policy, injection, use observation, redaction, rotation, and revocation. Agents receive references/classes, not secret values.

### Gap G-015 — Local-first ownership without encryption/recovery policy is incomplete

**Severity:** P1

Future work must define at-rest encryption, key custody, backups, recovery keys, multi-device transfer, and index/search behavior without hidden cloud authority.

### Gap G-016 — Receipts + trajectories + chats + events can become an unbounded surveillance log

**Severity:** P0

Durability tiers are mandatory:

```text
T1 permanent minimal proof
T2 reconstructable operational detail
T3 ephemeral/debug detail
```

### Gap G-017 — Global search needs semantic contracts, not one opaque score

**Severity:** P1

Use federated candidate generation, per-domain ranking, scope filtering before exposure, typed presentation, and explicit provenance/freshness.

### Gap G-018 — Automation can become an authority bypass

**Severity:** P0

```text
TRIGGER != AUTHORITY
AUTOMATION_SCOPE <= CREATOR_AUTHORIZED_SCOPE
```

### Gap G-019 — Cost and resource governance must be first-class

**Severity:** P0

Budgets should cover provider spend, runtime minutes, CPU/GPU, egress, storage growth, agent concurrency, context tokens, and artifact retention at workspace/project/agent/task/session levels.

### Gap G-020 — Trust UX must expose actual scope, not vague labels

**Severity:** P0

Users must understand what an agent can see, change, execute, contact, and which credentials/cost budgets it may use.

### Gap G-021 — Open files alone are insufficient anti-lock-in

**Severity:** P0

Semantic export must preserve stable identity, typed objects/relations, decisions, supersession, work state, provenance, evidence links, agent/session identity, receipts, and repository/source relationships.

### Gap G-022 — Agent work needs review-native surfaces, not chat-only review

**Severity:** P0

Review must support code patches, knowledge changes, decision proposals, memory proposals, work closeout, automation changes, and capability changes with before/after, evidence, provenance, risk, and authority impact.

### Gap G-023 — Product metrics can optimize the wrong behavior

**Severity:** P0

Prefer continuation success, time to useful orientation, constraint miss rate, stale-memory error, human interruption per successful task, evidence completeness, cross-runtime continuation, import-to-first-value, export fidelity, and recovery success over raw message/memory/turn counts.

### Gap G-024 — One continuation benchmark is insufficient

**Severity:** P0

Future benchmark portfolio should separately test memory correctness, temporal state, context selection, continuation, security boundary, injection resistance, multi-agent conflicts, approval friction, cost, latency, recovery, export fidelity, import integrity, upstream reconciliation, and cross-IDE/CLI portability.

### Gap G-025 — One Git repository cannot be the project boundary

**Severity:** P0

```text
PROJECT != REPOSITORY
```

A project may contain multiple repositories, docs, research, infrastructure, work items, artifacts, conversations, and evidence.

### Gap G-026 — Requiring a GitHub fork before local exploration creates unnecessary remote ownership and friction

**Severity:** P0

Support future no-fork import with explicit snapshot, mirror, tracked-upstream, bundle, patch, and local-directory modes.

```text
IMPORT != FORK
```

### Gap G-027 — Git history cannot carry the whole project brain

**Severity:** P0

```text
GIT_HISTORY != PROJECT_MEMORY
FEHREST_SEMANTIC_STATE_MUST_NOT_CORRUPT_GIT_OBJECT_IDENTITY
```

### Gap G-028 — Upstream movement can invalidate project memory

**Severity:** P0

Memory/procedures/decisions should retain evidence/source dependencies so upstream changes can produce explicit revalidation candidates.

```text
MEMORY_WITHOUT_INVALIDATION_PATH_IS_INCOMPLETE
```

### Gap G-029 — Import does not imply publish authority

**Severity:** P0

Publishing must always be explicit and separately authorized.

```text
IMPORT != PUBLISH_AUTHORITY
REMOTE_TARGET != CANONICAL_OWNER
```

### Gap G-030 — Without an open project-level format Fehrest can become the new lock-in

**Severity:** P0

Define a future open versioned `ProjectCapsule` or equivalent format preserving source provenance and semantic project state while keeping derived indexes rebuildable.

### Gap G-031 — "Whole context in seconds" is ambiguous and can become history dumping

**Severity:** P0

Target complete **relevant working context** in seconds, with immediate drill-down into deep authorized history.

```text
Working Continuity Layer
Deep Project Memory
```

```text
FAST_CONTEXT != FULL_HISTORY_DUMP
```

### Gap G-032 — Literal "never forget" is not an honest systems guarantee

**Severity:** P0

Promise testable guarantees:

```text
NO_SILENT_FORGETTING_OF_CANONICAL_STATE=YES
RETENTION_IS_EXPLICIT=YES
LOSS_IS_DETECTABLE=YES
SUPERSESSION_IS_PRESERVED=YES
UNRECONSTRUCTABLE_IS_REPORTED_HONESTLY=YES
RECOVERY_IS_FIRST_CLASS=YES
```

### Gap G-033 — A project brain without tested disaster recovery is not durable memory

**Severity:** P0

Need canonical inventory, content-addressed integrity checks, backup verification, restore drills, corruption detection, partial-loss classification, and portable recovery bundles.

### Gap G-034 — If the best context only works in one UI or agent, Fehrest has recreated vendor lock-in

**Severity:** P0

Same brain must be consumable through CLI, MCP, ACP adapters, local API/IPC, SDKs, and context exports where appropriate.

```text
IDE != MEMORY_OWNER
AGENT_RUNTIME != MEMORY_OWNER
MODEL_PROVIDER != MEMORY_OWNER
```

### Gap G-035 — Seconds-to-context fails if every query scans multi-year history

**Severity:** P0

Use deterministic incremental projections and a fast working-continuity index, with provenance-linked deep retrieval. Large-project benchmarks are mandatory.

### Gap G-036 — GitHub-only ingestion misses the actual project

**Severity:** P1

Future importers should support papers, PDFs, web docs, local files, meeting notes, workspace exports, issue trackers, terminal logs, benchmarks, and artifacts under the same evidence/provenance boundary.

### Gap G-037 — Calling Fehrest "storage" can encourage opaque blob-store design

**Severity:** P1

Storage is a property, not the category. Differentiated value is accumulated, portable, provenance-linked project understanding.

### Gap G-038 — Trying to replace GitHub too early would destroy focus

**Severity:** P0

```text
GITHUB_FIRST_CLASS=YES
GITHUB_EXCLUSIVE=NO
GITHUB_REPLACEMENT_REQUIRED=NO
```

Fehrest should initially work beside GitHub and earn centrality through project continuity.

### Gap G-039 — Broad vision needs a simple compounding adoption flywheel

**Severity:** P0

```text
Import any project
→ instant orientation
→ useful agent/human work
→ durable learning + evidence
→ next session starts smarter
→ switch IDE/model without losing brain
→ reconcile upstream
→ publish when desired
```

### Gap G-040 — Optimizing recall alone creates a confidently stale brain

**Severity:** P0

Measure stale-memory errors, unsupported-memory rate, supersession correctness, revalidation latency, and source-change invalidation precision/recall.

---

## 3. Final architecture correction set

The mature Fehrest target should preserve:

```text
PROJECT != REPOSITORY
REPOSITORY != PROJECT_BRAIN
GIT_HISTORY != PROJECT_MEMORY
IMPORT != FORK
IMPORT != PUBLISH_AUTHORITY
FAST_CONTEXT != FULL_HISTORY_DUMP
MEMORY != UNCHECKED_SUMMARY
REMEMBERING != VALIDITY
IDE != MEMORY_OWNER
AGENT_RUNTIME != MEMORY_OWNER
MODEL_PROVIDER != MEMORY_OWNER
REMOTE != CANONICAL_OWNER
```

The strongest final positioning is:

> **GitHub can host the repository. Fehrest should remember the project.**

and:

> **Fehrest should make a fresh authorized human or agent able to continue a long-lived project correctly within seconds of arriving, while preserving the full durable project brain across tools and vendors.**
