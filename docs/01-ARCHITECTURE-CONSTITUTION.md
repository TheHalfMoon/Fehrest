# B. Architecture Constitution

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Non-negotiable invariants. Each is stated as a testable property, paired with the mechanism that enforces it and the test that detects violation. An invariant with no test is a slogan; every clause below therefore names its detector.

The founder proposed 15 candidate invariants. **Thirteen are adopted as written. Two are amended** — I-5 and I-12 — because as originally phrased they are either unenforceable or would forbid something the system requires. Both amendments are argued in §3 rather than applied silently.

---

## 1. The invariants

### I-1 — User knowledge exists locally by default
Every canonical artifact resides in a user-designated vault directory on local storage. No canonical state exists only in remote storage, only in a database, or only in application memory.

**Enforced by:** the Knowledge Plane is a directory tree ([D](03-CANONICAL-DATA-MODEL.md)).
**Test:** `test_vault_is_self_contained` — copy the vault directory to a clean machine with no Fehrest configuration; all objects, links, memories and events must be present and readable.

### I-2 — Core functionality requires no network
Ingestion, search, graph construction, memory read/write, context compilation and the agent gateway function with all network interfaces down.

**Enforced by:** no core code path performs I/O to a non-loopback address.
**Test:** `test_offline_full_suite` — the entire core test suite runs in a network-namespace-isolated container with no route to any external host. CI-blocking. Any core test that fails offline is a defect, not an environment issue.

### I-3 — Core functionality requires no Fehrest-hosted service
No core operation contacts a Fehrest-operated endpoint. There is no license check, no activation, no mandatory account, no phone-home.

**Enforced by:** no Fehrest-owned domain appears in any core dependency or configuration default.
**Test:** `test_no_vendor_endpoints` — static scan of the source tree and shipped configuration for Fehrest-controlled hostnames; fails the build on any hit.

### I-4 — Core functionality requires no paid API
Every core capability has a zero-cost local path. Paid providers are accelerators.

**Enforced by:** provider adapters sit behind one seam with a null implementation that is the default.
**Test:** `test_ai_off_mode` — with all provider credentials absent and local inference uninstalled, the full core suite passes.

### I-5 — Canonical artifacts are open, local, and inspectable *(AMENDED)*

**Original:** "Human-readable/open files are canonical wherever practical."

**As adopted:** Every canonical artifact has a **documented open format**, is stored in the vault, and is fully interpretable by a third party using only the published specification. A canonical format may be binary or non-human-readable **only if** (a) its specification is published in-repo, (b) a `fehrest export` implementation converts it to a human-readable form without loss, and (c) that exporter has no dependency on Fehrest-operated infrastructure.

**Enforced by:** a format registry in-repo; a canonical format cannot be introduced without a specification document and a round-trip test.
**Test:** `test_every_canonical_format_has_spec_and_exporter` — enumerate canonical file types on disk; fail if any lacks a registry entry, a specification, or a passing lossless-export test.
**Rationale for amendment:** §3.1.

### I-6 — Derived state is disposable and rebuildable
Deleting the entire derived directory and restarting must produce a functionally identical system, differing only in the time spent rebuilding.

**Enforced by:** derived state lives in a separate directory from canonical state, and no write path treats derived state as an input to canonical state.
**Test:** `test_nuke_and_rebuild_equivalence` — snapshot query results across a fixed query set, delete all derived state, rebuild, re-run; results must match exactly. This is the single most important test in the suite, because it is what makes every other index decision reversible.

### I-7 — Sync is optional
Fehrest never requires synchronisation. The vault is usable, complete and correct on one machine forever.

**Enforced by:** no sync code in core; sync is a later, separately gated capability.
**Test:** absence — no sync module exists in the v1 dependency graph.

### I-8 — Servers are accelerators, never authorities
No remote system may be the source of truth for any canonical artifact, and no remote response may be trusted to resolve a conflict in canonical state.

**Enforced by:** conflict resolution is a local, deterministic function of local canonical state.
**Test:** `test_no_remote_authority` — with a mock remote returning contradictory data, canonical resolution is unchanged.

### I-9 — Export does not depend on Fehrest infrastructure
Export runs offline, from the vault alone, with no account and no server.

**Enforced by:** the exporter is a pure function of vault contents.
**Test:** `test_export_offline_from_vault_only` — export a vault in an isolated container; verify completeness against the canonical object inventory.

### I-10 — Agents receive explicitly bounded access
No agent receives ambient authority. Every agent session carries an explicit capability grant enumerating readable scopes, writable scopes and permitted actions. Absence of a grant denies.

**Enforced by:** the authorization check is a single chokepoint every tool invocation passes through, before execution ([G](06-AGENT-MODEL.md)).
**Test:** `test_deny_by_default` — a session with an empty grant is refused every operation, including read. Plus a coverage test asserting no tool handler is reachable without passing the chokepoint.

### I-11 — Agent-generated memories preserve provenance
Every memory records which actor asserted it, from what evidence, in which session, at what time. A memory with no provenance chain cannot be written.

**Enforced by:** provenance fields are non-nullable in the memory schema; writes without them fail.
**Test:** `test_memory_requires_provenance` — attempt to insert a memory with a null actor or empty evidence set; must be rejected at the storage layer, not merely in the UI.

### I-12 — Inference is never silently promoted to fact *(AMENDED)*

**Original:** "Inference must never silently become fact."

**As adopted:** Every memory carries an `epistemic_status` distinguishing `observed` (directly recorded from a primary source), `asserted` (stated by an identified actor), `inferred` (derived by a mechanism), and `unverified`. A transition to a higher-confidence status requires either a new primary evidence link or an explicit human confirmation event, and every transition is recorded as an event. **No mechanism exists to change status without emitting an event.**

**Enforced by:** status transitions are event-sourced; the memory projection derives status from events rather than storing it mutably.
**Test:** `test_status_transitions_are_event_sourced` — mutate status through every available code path; assert a corresponding event exists for each. Property test over random transition sequences asserting projected status always equals event-derived status.
**Rationale for amendment:** §3.2.

### I-13 — Imported and retrieved content is evidence, never authority
Content that enters Fehrest from any source other than a direct user instruction — files, PDFs, web pages, tool results, agent output — is data. It is structurally incapable of altering agent instructions, capability grants, or policy.

**Enforced by:** the instruction plane, knowledge plane and tool-control plane are separate channels. Retrieved content is delivered to models inside a fenced, labelled envelope that the system prompt declares non-authoritative, and capability decisions are computed **before** retrieval and are not re-read from retrieved content ([C](02-THREAT-MODEL.md)).
**Test:** `test_injection_corpus` — an adversarial corpus of documents containing instruction-shaped text must produce zero capability changes and zero unapproved tool executions. AgentDojo-derived. CI-blocking.

**Honest limitation:** this invariant is enforceable for *capability and policy* — those are structural. It is **not** fully enforceable for model *behaviour*: a sufficiently persuasive document may still influence what a model says. The boundary Fehrest guarantees is that influence cannot escalate privilege. Stated plainly because claiming otherwise would be false. See [C §4](02-THREAT-MODEL.md).

### I-14 — Agent-visible state is reconstructable and auditable
Anything ever shown to an agent can be reconstructed exactly from canonical state, with its provenance, at any later time.

**Enforced by:** context packages are content-addressed and their inputs recorded as events; the package is *derivable* from the event log rather than stored as an opaque blob ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns) — derived, not stored).
**Test:** `test_context_package_replay` — for every historical `context/compiled` event, recompile from canonical state and compare digests. Any mismatch is a defect.

### I-15 — Paths are locations; stable IDs are identities
An object's identity is an opaque, allocated identifier that never changes. A path is a mutable attribute. Renaming or moving a file preserves identity, links, memories and history.

**Enforced by:** identity is allocated at first observation and stored in the file's frontmatter plus the derived index; all cross-references use IDs.
**Test:** `test_identity_survives_rename` — rename, move across directories, and change case; all backlinks, memories and events must remain attached. Plus `test_graphify_ids_are_not_identities` — assert no canonical record uses a Graphify node ID as a primary key, since those IDs are name-derived and collision-prone ([E-4](research/EVIDENCE_LOG.md#e-4--graphify-node-ids-are-name-derived-not-stable-identities)).

---

## 2. Derived rules

These follow from the invariants and are listed because violating them is the usual way an invariant dies quietly.

| Rule | Follows from |
|---|---|
| **R-1** No LLM call may occur on an indexing, ingestion or startup path | I-2, I-4 |
| **R-2** No canonical write may depend on a derived read | I-6 |
| **R-3** No user-visible feature may be reachable *only* with AI enabled unless it is labelled optional | I-4 |
| **R-4** Every schema change ships with a forward migration and a documented downgrade outcome | I-5, I-9 |
| **R-5** The event log is append-only; correction is a new compensating event, never mutation | I-14 |
| **R-6** No component may hold ambient filesystem authority over the whole vault; access is scope-mediated | I-10 |
| **R-7** The sidecar is a computation service with no authority — it cannot write canonical state | I-8, I-6 |
| **R-8** Any format Fehrest writes must be readable by a future version, and must fail loudly rather than silently drop unknown fields | I-5, [M](12-MIGRATION-SCHEMA-EVOLUTION.md) |

## 3. Amendment rationale

### 3.1 Why I-5 was rewritten

"Human-readable wherever practical" cannot be tested, because "practical" is an opinion. In practice it collapses under the first real pressure: attachments are binary; embeddings are float arrays; a content-addressed store is not human-readable. A team applying the original clause honestly ends up either declaring those non-canonical (correct for embeddings, wrong for attachments — a user's PDF *is* their knowledge) or quietly abandoning the invariant.

The amended form keeps the property that actually matters — **a third party can recover everything from published specs, with no Fehrest software** — and makes it a build-breaking test rather than a judgement call. It also correctly permits an append-only binary event journal if measurement later shows JSONL cannot meet durability budgets, provided the format is specified and losslessly exportable.

The founder's brief already anticipates this: *"Do not interpret local-first as everything must be Markdown."* This amendment is that instruction made enforceable.

### 3.2 Why I-12 was rewritten

"Inference must never silently become fact" names the right danger but omits the mechanism, and the word "silently" invites a reading where a *loud* promotion is acceptable and therefore unlogged.

The amended form makes the guarantee structural: status is not a mutable field but a projection over events, so there is no code path that can change it without leaving a record. This is the same technique the harness uses to make agent-visible history trustworthy — derive, do not store ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)) — and it converts the invariant from a discipline into a property.

It also introduces the four-value `epistemic_status` vocabulary, which the memory model needs anyway to satisfy LongMemEval-V2's premise-awareness ability ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)).

## 4. What the constitution deliberately does not require

Stated so reviewers do not read absences as oversights:

- **It does not require Markdown for everything.** It requires open, specified, exportable formats (I-5).
- **It does not forbid servers or cloud.** It forbids them being *authorities* (I-8) or *requirements* (I-3).
- **It does not forbid LLMs.** It forbids them being *mandatory* (I-4) and forbids them on index paths (R-1).
- **It does not promise agents cannot be manipulated by content.** It promises manipulation cannot escalate privilege (I-13, with its stated limitation).
- **It does not require CRDTs.** Local-first is achieved by local canonical files; CRDTs are a collaboration mechanism and are deferred ([SRC-005](research/FEHREST_SOURCE_REGISTRY.md#32-yjs--defer)).

## 5. Amendment procedure

An invariant may be amended only by: (1) a written argument that it is technically unsound or unenforceable, (2) a replacement clause with a concrete test, (3) an ADR recording the change, and (4) a named consequence for every document that cited it.

Weakening an invariant without following this procedure is the specific failure mode this document exists to prevent. Invariants I-1 through I-4 and I-13 are additionally designated **thesis-critical**: amending any of them means Fehrest is a different product, and requires an explicit founder decision recorded in [Q](16-OPEN-QUESTIONS.md).
