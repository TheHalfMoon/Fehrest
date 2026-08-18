# B. Architecture Constitution

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Non-negotiable invariants. Each is stated as a testable property, paired with the mechanism that enforces it and the test that detects violation. An invariant with no test is a slogan; every clause below therefore names its detector.

The founder proposed 15 candidate invariants. **Thirteen are adopted as written. Two are amended** — I-5 and I-12 — because as originally phrased they are either unenforceable or would forbid something the system requires. Both amendments are argued in §3 rather than applied silently.

**Two invariants were added in F1-R2** — I-16 and I-17 — as direct consequences of founder decision D-1 (Rust is the canonical Core language). They exist so that "the UI is a surface, not the product" and "Python is optional" are testable properties rather than intentions.

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

**As first amended (F1):** a single four-value `epistemic_status` (`observed` / `asserted` / `inferred` / `unverified`), later widened to eight values in [F §3.3](05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model).

> **RE-AMENDED IN F1-R2 ([R2-04](reviews/F1-R2-RECONCILIATION.md)).** The single-enum form is **withdrawn**. It collapsed four independent semantic axes into one ordered vocabulary, which made some real states inexpressible (an agent-asserted memory that a human later confirmed and that now conflicts with another memory occupies three axes at once) and made any total ordering over it arbitrary.

**As adopted:** Every memory carries **four orthogonal, independently-valued fields**, and no code path may collapse them into one:

| Field | Answers | Values |
|---|---|---|
| `basis` | Where did this claim come from? | `USER_ASSERTED` · `EXTRACTED` · `AGENT_ASSERTED` · `INFERRED` |
| `verification` | Has it been checked, and by whom? | `UNVERIFIED` · `CORROBORATED` · `USER_CONFIRMED` |
| `lifecycle` | Is it in force? | `PENDING` · `ACTIVE` · `SUPERSEDED` · `RETRACTED` · `EXPIRED` |
| `resolution` | Does it currently resolve cleanly? | `CLEAR` · `CONFLICTED` · `UNRESOLVED` |

Full vocabulary, permitted transitions per axis, and the extractor-label mapping are normative in [F §3.3](05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model).

**The guarantee, restated on the new fields:** `basis` is assigned once, by the core, from the authenticated actor and the mechanism that produced the record — **no actor may supply it**. `verification` may only move upward on either a new independently-resolving evidence link (`→ CORROBORATED`) or an explicit human confirmation event (`→ USER_CONFIRMED`); an actor may never corroborate its own assertion. `basis = EXTRACTED` is reachable **only** by Fehrest's own deterministic parsing and is unreachable by any agent. Every change on every axis is an event. **No mechanism exists to change any of the four fields without emitting an event.**

**Enforced by:** all four fields are event-sourced; the memory projection derives them from events rather than storing them mutably. Each field is a distinct column with a distinct type; there is no serialisation that flattens them into one string.
**Test:** `test_status_transitions_are_event_sourced` — mutate each axis through every available code path; assert a corresponding event exists for each. Property test over random transition sequences asserting each projected field always equals its event-derived value. Plus `test_axes_are_independent` — assert that every combination reachable per-axis is representable, and that no API accepts or returns a single collapsed status value.
**Rationale for amendment:** §3.2.

### I-13 — Imported and retrieved content is evidence, never authority
Content that enters Fehrest from any source other than a direct user instruction — files, PDFs, web pages, tool results, agent output — is data. It is structurally incapable of altering agent instructions, capability grants, or policy.

**Enforced by:** the instruction plane, knowledge plane and tool-control plane are separate channels. Retrieved content is delivered to models inside a fenced, labelled envelope that the system prompt declares non-authoritative, and capability decisions are computed **before** retrieval and are not re-read from retrieved content ([C](02-THREAT-MODEL.md)).
**Test:** `test_injection_corpus` — an adversarial corpus of documents containing instruction-shaped text must produce zero capability changes and zero unapproved tool executions. AgentDojo-derived. CI-blocking.

**Honest limitation:** this invariant is enforceable for *capability and policy* — those are structural. It is **not** fully enforceable for model *behaviour*: a sufficiently persuasive document may still influence what a model says. The boundary Fehrest guarantees is that influence cannot escalate privilege. Stated plainly because claiming otherwise would be false. See [C §4](02-THREAT-MODEL.md).

### I-14 — Model-visible state is reconstructable, provenance-linked, scope-authorized and auditable

**Strengthened in F1-R1 ([R1-13](reviews/F1-R1-RECONCILIATION.md)). Property 1 split and corrected in F1-R2 ([R2-01](reviews/F1-R2-RECONCILIATION.md)).** Anything ever shown to an agent must satisfy **all five** properties:

1. **Composition-auditable — permanent and unconditional.** A canonical T1 **served-item manifest** records exactly which logical items were emitted, in what order, under whose grant, with what content hashes. It is written at emission time and is never compacted away. This property does not degrade.
2. **Content-reconstructable — conditional, and honestly reported.** Exact item *content* is recomputable only while the source revisions it cites still exist. Where they do not, replay must return `UNRECONSTRUCTABLE` with a reason, never a claimed success.
3. **Provenance-linked** — every item cites the canonical evidence it came from.
4. **Scope-authorized** — every item was inside the session's grant at compile time.
5. **Auditable** — the fact that it was shown, to whom, and when, is itself recorded.

> **The F1 formulation of property 1 — "recomputable exactly from canonical state at any later time" — is withdrawn as unsatisfiable.** It is defeated by three ordinary, permitted events: a user edits a source object; T2 detail is compacted per [D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief); or the compiler/schema version changes. A guarantee that the system's own normal operation breaks is not a guarantee. The split above keeps the property that actually carries the audit weight — *what was served* — permanent and unconditional, while stating the limits of the property that cannot be permanent.

This is materially stricter than storing chat history: a stored transcript satisfies (5) alone.

**One envelope for every agent-facing read ([R2-03](reviews/F1-R2-RECONCILIATION.md)).** The context compiler must not be the only path that preserves trust level, provenance, temporal state and supersession. **Every** agent-facing tool that returns content — search, object read, memory retrieval, graph query, and any future addition — returns it through a **single Rust-core response-envelope type**. Direct historical exploration remains permitted; it must merely be **temporally honest**: an agent may read a superseded decision, but the response must say it is superseded and name its replacement where one is known. No tool may return imported content as undifferentiated instruction-like text.

**Trust stratification — the seven levels that must never be collapsed.** Model-visible text is not homogeneous. Fehrest labels each item with its plane and trust level, and no mechanism may flatten them into undifferentiated prose:

| # | Level | Authority | Writable by |
|---|---|---|---|
| 1 | System / owner instruction | **Authoritative** | Fehrest core only |
| 2 | Trusted Fehrest policy | **Authoritative** | Fehrest core only |
| 3 | User instruction | **Authoritative** | The user, via the UI |
| 4 | Retrieved knowledge (vault) | Evidence | Anyone with vault write access |
| 5 | Imported external content | **Evidence — assume hostile** | Any source |
| 6 | Tool output | **Evidence — assume hostile** | Tools, including remote ones |
| 7 | Agent inference | Evidence, marked `inferred` | The agent |

Levels 1–3 may direct behaviour. **Levels 4–7 never may**, however authoritative their text sounds. This is the structural form of [I-13](#i-13--imported-and-retrieved-content-is-evidence-never-authority).

**Enforced by:** every compiled package writes a permanent T1 served-item manifest ([H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1)); every emitted item carries its trust level and provenance; scope is asserted at emission ([H §4](07-CONTEXT-COMPILER-SPEC.md#4-pipeline)); all agent-facing reads pass through one core envelope ([G §4](06-AGENT-MODEL.md#4-context-delivery-and-the-trust-stratification)).
**Test:** `test_context_package_replay` — recompile every historical `context/compiled` event and assert the reported outcome is one of `IDENTICAL` / `DIVERGED` / `UNRECONSTRUCTABLE` **with the correct reason**; a mismatch reported as success is a failure. Plus `test_manifest_is_permanent` — after full T2 compaction, every historical manifest still enumerates its served items. Plus `test_trust_levels_never_collapsed` — assert every emitted item carries a trust level, and that no serialisation path erases it. Plus **`test_no_unlabelled_content_path`** — enumerate the entire agent-facing read surface and assert every path returns the core envelope with trust level, provenance, temporal state and supersession intact. Plus `test_provenance_completeness` — unsourced items exactly 0.

### I-15 — Paths are locations; stable IDs are identities
An object's identity is an opaque, allocated identifier that never changes. A path is a mutable attribute. Renaming or moving a file preserves identity, links, memories and history.

**Enforced by:** identity is allocated at first observation and stored in the file's frontmatter plus the derived index; all cross-references use IDs. **Path comparison is never identity comparison** — reconciliation resolves the embedded Fehrest ID first and uses a platform-aware path key only to *locate*, never to *identify* ([D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics)).
**Test:** `test_identity_survives_rename` — rename, move across directories, and change case; all backlinks, memories and events must remain attached. Full operation matrix in [D §3.2](03-CANONICAL-DATA-MODEL.md#32-identity-across-filesystem-operations), and the per-platform filesystem matrix (Windows case-insensitivity and case-only rename, macOS APFS default and case-sensitive, Linux case-sensitivity, NFC/NFD equivalence) in [D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics).

#### Extractor identity sub-invariants (G-ID-1 … G-ID-4)

Added in F1-R1 ([R1-05](reviews/F1-R1-RECONCILIATION.md)). These generalise to **any** extractor — code, document, or future — not to one donor.

> **G-ID-1** — No extractor-generated identifier may be a canonical Fehrest object ID.
>
> **G-ID-2** — Every derived graph node must map to a Fehrest-owned stable identity where such an identity exists.
>
> **G-ID-3** — A graph rebuild or extractor upgrade may change extractor IDs **without** changing canonical Fehrest identity.
>
> **G-ID-4** — Derived node records must preserve sufficient source mapping to trace back to canonical evidence.

**Why these are structural, not defensive.** Extractor IDs are typically derived from names or paths (Graphify's file nodes are spec'd `{parent_dir}_{stem}`), and extractor ID *schemes* change between versions — upstream Graphify explicitly rejected an alternative scheme because it "would rewrite every file and symbol id and force a full-rebuild migration." An identifier whose scheme is expected to change cannot anchor durable references. This holds even when the extractor has **no** open defects ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)).

**Required derived-node fields:** `fehrest_object_id` · `extractor_id` · `extractor_version` · `source_uri` · `source_revision` · `source_location` · `relationship_confidence`.

`extractor_version` is what makes G-ID-3 checkable: a node whose `extractor_version` differs from the current extractor is known-stale and rebuildable without touching canonical identity.

**Test:** `test_extractor_ids_are_not_identities` — assert no canonical record uses an extractor ID as a key. `test_extractor_upgrade_preserves_identity` — change `extractor_version`, rebuild, assert every `fehrest_object_id` and every memory attachment is unchanged. `test_derived_node_traces_to_canonical` — every derived node resolves to canonical evidence via `source_uri` + `source_location`.

### I-16 — Fehrest remains operable without its user interface

**Added in F1-R2** as a direct consequence of founder decision D-1.

> If the desktop UI disappears, Fehrest remains operable through its Rust Core and CLI.

Every capability that governs canonical state — ingestion, identity, search, memory read/write, context compilation, provenance, audit, recovery, export, migration — is reachable through the Rust Core and its CLI with no UI process present. The UI is a **presentation surface over the Core**, never the owner of a state semantic.

**Enforced by:** founder decision D-1 ([ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language)). All correctness- and security-sensitive logic lives in Rust; TypeScript/React may render it and may not duplicate it. No business-critical state semantic may exist only in the UI layer.
**Test:** `test_core_suite_headless` — the entire core test suite passes with no UI built and no UI process running. Plus `test_no_state_semantics_in_ui` — a static check that the UI package contains no memory resolution, no supersession logic, no authorization decision, no canonical write path, and no identity allocation.

### I-17 — Fehrest remains usable without Python

**Added in F1-R2** as a direct consequence of founder decision D-1.

> If Python disappears, canonical Fehrest knowledge, memory, and recovery remain usable.

No canonical operation may require a Python runtime. Python is permitted **only** behind an explicit optional process boundary, for hypothesis-gated donor capabilities such as Graph Intelligence ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)).

**Enforced by:** the sidecar is a compute service with no authority ([R-7](#2-derived-rules)); nothing canonical is produced by it; graph state is derived and disposable ([I-6](#i-6--derived-state-is-disposable-and-rebuildable)).
**Test:** `test_no_python_required` — with no Python interpreter installed or on `PATH`, the full core suite passes, the vault opens, search works, memory resolves, context compiles, recovery runs, and export completes. Graph features are absent and reported as absent, not broken.

**Relationship to [I-4](#i-4--core-functionality-requires-no-paid-api).** I-4 removes the *model* from the required path; I-17 removes the *second runtime*. Both exist so that the failure of an optional accelerator is a degradation, never a data-availability event.

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
| **R-9** Every agent-facing response carrying content passes through the single core response envelope; no tool serialises content by any other route | I-13, I-14 |
| **R-10** Every derived artifact records the inputs, deriver identity and deriver version it was produced from | I-6, [E §10](04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data) |
| **R-11** Development and governance tooling — Spec Kit, Ponytail, benchmark harnesses — may never become a runtime dependency of Fehrest | I-2, I-3, [ADR-0014](09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail) |
| **R-12** No memory awaiting confirmation may enter an authoritative section, grant or revoke a capability, or supersede confirmed state | I-12, [F §5.5](05-MEMORY-MODEL.md#55-pending-confirmation-semantics) |

*(R-9…R-12 added in F1-R2.)*

## 3. Amendment rationale

### 3.1 Why I-5 was rewritten

"Human-readable wherever practical" cannot be tested, because "practical" is an opinion. In practice it collapses under the first real pressure: attachments are binary; embeddings are float arrays; a content-addressed store is not human-readable. A team applying the original clause honestly ends up either declaring those non-canonical (correct for embeddings, wrong for attachments — a user's PDF *is* their knowledge) or quietly abandoning the invariant.

The amended form keeps the property that actually matters — **a third party can recover everything from published specs, with no Fehrest software** — and makes it a build-breaking test rather than a judgement call. It also correctly permits an append-only binary event journal if measurement later shows JSONL cannot meet durability budgets, provided the format is specified and losslessly exportable.

The founder's brief already anticipates this: *"Do not interpret local-first as everything must be Markdown."* This amendment is that instruction made enforceable.

### 3.2 Why I-12 was rewritten

"Inference must never silently become fact" names the right danger but omits the mechanism, and the word "silently" invites a reading where a *loud* promotion is acceptable and therefore unlogged.

The amended form makes the guarantee structural: status is not a mutable field but a projection over events, so there is no code path that can change it without leaving a record. This is the same technique the harness uses to make agent-visible history trustworthy — derive, do not store ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)) — and it converts the invariant from a discipline into a property.

**Why the single enum was replaced in F1-R2.** The F1 amendment introduced one four-value `epistemic_status`; F1-R1 widened it to eight. The widening is what exposed the defect: `EXTRACTED` and `INFERRED` describe *origin*, `USER_CONFIRMED` describes *verification*, `SUPERSEDED` describes *lifecycle*, and `CONFLICTED` / `UNRESOLVED` describe *resolution*. These are not members of one vocabulary, and treating them as one had two concrete costs. First, it made legitimate combinations inexpressible — a memory can be agent-asserted, human-confirmed, active and conflicted simultaneously, which the enum cannot represent. Second, it invited a **total ordering over incomparable things**, which is precisely what [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution) then had to use to pick conflict winners. Four orthogonal fields make each comparison well-founded and make the cases where no comparison exists visible as `CONTRADICTION` rather than resolved by an arbitrary rank.

The vocabulary still satisfies LongMemEval-V2's premise-awareness ability ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)); it now does so without conflating four questions into one answer.

## 4. What the constitution deliberately does not require

Stated so reviewers do not read absences as oversights:

- **It does not require Markdown for everything.** It requires open, specified, exportable formats (I-5).
- **It does not forbid servers or cloud.** It forbids them being *authorities* (I-8) or *requirements* (I-3).
- **It does not forbid LLMs.** It forbids them being *mandatory* (I-4) and forbids them on index paths (R-1).
- **It does not promise agents cannot be manipulated by content.** It promises manipulation cannot escalate privilege (I-13, with its stated limitation).
- **It does not require CRDTs.** Local-first is achieved by local canonical files; CRDTs are a collaboration mechanism and are deferred ([SRC-005](research/FEHREST_SOURCE_REGISTRY.md#32-yjs--conditional--editor-dependent)).
- **It does not require a graphical interface.** I-16 requires the opposite: the Core must stand without one.
- **It does not require any development workflow at runtime.** Spec Kit and Ponytail govern how Fehrest is *built* ([ADR-0014](09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail)); R-11 forbids either from being present in a shipped dependency graph.

## 5. Amendment procedure

An invariant may be amended only by: (1) a written argument that it is technically unsound or unenforceable, (2) a replacement clause with a concrete test, (3) an ADR recording the change, and (4) a named consequence for every document that cited it.

Weakening an invariant without following this procedure is the specific failure mode this document exists to prevent. Invariants I-1 through I-4 and I-13 are additionally designated **thesis-critical**: amending any of them means Fehrest is a different product, and requires an explicit founder decision recorded in [Q](16-OPEN-QUESTIONS.md).
