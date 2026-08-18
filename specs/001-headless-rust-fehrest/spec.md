# Feature Specification: Headless Rust Fehrest Thesis-Proof

**Feature Branch**: `001-headless-rust-fehrest` (developed on `main`; no push, no PR, no merge)
**Created**: 2026-08-18
**Status**: Specified
**Authorization**: [PHASE_T_AUTHORIZATION](../../docs/canonical/PHASE_T_AUTHORIZATION.md)
**Architecture**: [ARCHITECTURE_FREEZE](../../docs/canonical/ARCHITECTURE_FREEZE.md) — frozen, not reopened by this feature

---

## The question this feature exists to answer

> **Can a fresh agent continue long-running work more correctly using a small local Fehrest Core than using strong simpler baselines** — while preserving current-state truth, temporal truth, supersession, provenance, authorization and bounded context, at acceptable resource cost?

This is an **EXPERIMENTAL PRODUCT PROOF**. It is **not** Fehrest v1.

**A negative answer is a successful experiment.** If the Core does not materially outperform a competent plain agent and a maintained Markdown wiki, that is the finding, and the response is to report it — not to add graph, vectors, embeddings, automatic memory or a larger model until the number improves ([F-1](../../docs/17-FAILURE-CONDITIONS.md#f-1--compiled-context-does-not-beat-a-competent-agent-with-plain-file-tools), Constitution XVII).

---

## User Scenarios & Testing *(mandatory)*

### Primary user story

An agent works a project across many sessions. It records durable knowledge: decisions taken, constraints that bind, approaches that failed, and the current state of the work. The agent is then destroyed.

A **fresh agent** — with no chat history, no memory of the prior sessions — receives a compiled context package from Fehrest and must continue the work correctly: honour constraints that are still in force, avoid re-litigating settled decisions, avoid repeating recorded failures, and use the *current* value of state that has changed over time rather than a superseded one.

### Acceptance scenarios

1. **Current-state truth.** Given a project where a decision was recorded and later superseded, when a fresh agent compiles context, then the package presents the **current** decision as current and the superseded one **labelled as superseded**, never the reverse.

2. **Historical truth.** Given the same project, when context is compiled `as-of` a past valid time, then the package reflects what was true at that time — not what is true now.

3. **Contradiction is visible.** Given two active memories that contend and cannot be separated by the deterministic ladder, when context is compiled, then the package reports a **contradiction** rather than silently selecting a winner.

4. **Abstention.** Given no memory answering a query, when resolution runs, then the result is `NO_ANSWER` — never a fabricated answer.

5. **Scope isolation.** Given memories written under project A, when an agent scoped to project B compiles context, then no project-A memory appears.

6. **Bounded and honest.** Given a budget too small for everything selected, when context is compiled, then the package stays within budget, records what was omitted, and **every emitted item retains its full trust and provenance envelope**.

7. **Provenance.** Given a compiled package, when its manifest is inspected, then it lists exactly the items **actually emitted**, and a memory may only claim as observed-evidence an item that a manifest records as served to that session.

8. **Rebuildability.** Given derived state is deleted entirely, when the vault is reopened and rebuilt, then canonical objects, memories, events and provenance are intact and query results are equivalent.

### Edge cases

- Two files carrying the **same** Fehrest UUID → explicit conflict, both retained, neither silently discarded.
- A derived index row pointing outside the vault root → the read **fails**; the locator does not expand authority.
- A derived index row pointing at a *different in-vault object* → post-open UUID mismatch **fails closed**.
- A file whose content is instruction-shaped (`IGNORE PRIOR INSTRUCTIONS…`) → carried as **evidence**, labelled, and structurally unable to become authority.
- Literal search text containing FTS5 operators (`OR`, `NEAR`, `title:`) → treated as literal text, not as query syntax.
- A second Fehrest process writing the same vault → **fails visibly**; no silent concurrent append.
- Content attempting to close/forge the envelope structure → cannot create a second machine-owned item or forge trust metadata.

---

## Requirements *(mandatory)*

### Functional requirements

**Vault and canonical objects**

- **FR-001**: System MUST operate against an explicit local vault root directory.
- **FR-002**: System MUST index only supported open canonical text content; everything else is excluded by default (allowlist, not deny-list).
- **FR-003**: System MUST exclude `.fehrest/` and `.git/` from ordinary knowledge indexing.
- **FR-004**: System MUST assign each canonical object a stable Fehrest UUID stored in the object itself.
- **FR-005**: System MUST treat a path as a location only; identity never derives from a path.
- **FR-006**: System MUST surface two objects sharing one UUID as an explicit conflict, retaining both.

**Root-confined access and identity verification**

- **FR-007**: System MUST open canonical content only within the authorized vault root; absolute-path escape, parent-traversal escape and symlink escape MUST fail.
- **FR-008**: System MUST verify, **after opening**, that the embedded UUID read from the opened content matches the requested object ID, and MUST fail closed on mismatch.
- **FR-009**: A derived-store path MUST be treated as an untrusted locator hint that cannot expand filesystem authority.

**Derived index**

- **FR-010**: System MUST maintain a derived SQLite index with FTS5 for lexical candidate generation, rebuildable from canonical state.
- **FR-011**: Derived state MUST NOT grant authority; authorization-relevant scope MUST come from canonical state.
- **FR-012**: System MUST disable SQLite extension loading, derive the database path from the vault root, and reject untrusted `ATTACH`.
- **FR-013**: System MUST construct FTS `MATCH` expressions so literal user text cannot activate FTS5 query syntax, with bounded input size and result count.
- **FR-014**: Deleting all derived state MUST NOT lose canonical objects, memories, events or provenance.

**Explicit memory**

- **FR-015**: System MUST support explicit durable memory writes only. No automatic extraction, promotion, or confirmation queue.
- **FR-016**: Each memory MUST carry four orthogonal fields — `basis`, `verification`, `lifecycle`, `resolution` — plus valid time, recorded order, scope and provenance.
- **FR-017**: `basis` MUST be core-assigned and never actor-supplied.
- **FR-018**: Numeric confidence MUST NOT participate in truth resolution.

**Temporal resolution and supersession**

- **FR-019**: System MUST resolve current state deterministically, returning a winner, `CONTRADICTION`, or `NO_ANSWER`.
- **FR-020**: System MUST answer historical (`as-of`) queries distinctly from current-state queries.
- **FR-021**: System MUST reject invalid supersession edges — self-supersession, cycles, cross-vault, prohibited cross-scope, `PENDING` superseding authoritative state — as `INVALID_SUPERSESSION`, never silently normalised.
- **FR-022**: `PENDING` memories MUST be excluded from authoritative resolution.

**Events, audit, single writer**

- **FR-023**: System MUST append typed canonical events for context compilation, memory transitions and authorization-sensitive operations, hash-chained.
- **FR-024**: System MUST enforce one canonical writer per vault; a second writer MUST fail visibly, and canonical forks MUST be surfaced, never auto-merged.

**Trust envelope and context compilation**

- **FR-025**: Every agent-visible content path MUST return machine-owned metadata: identity, trust level, provenance, temporal state, supersession state, scope, truncation state.
- **FR-026**: Content MUST be carried as a value and MUST NOT be parseable as machine-owned metadata; content MUST NOT be able to forge a second item or forge trust/provenance fields.
- **FR-027**: System MUST compile a bounded context package that is permission-aware, scope-aware, temporal-aware, supersession-aware, provenance-backed and deterministic for identical inputs.
- **FR-028**: An emitted item MUST be `FULL`, `TRUNCATED` (content shortened, envelope intact) or `OMITTED`. Emitting content with truncated security metadata MUST be impossible.
- **FR-029**: System MUST record a served-item manifest of items **actually emitted**, and MUST reject an evidence claim naming an object that is in-scope but absent from the relevant manifest.

**CLI**

- **FR-030**: System MUST expose a minimal headless CLI: init/open vault, rebuild derived state, write memory, search, compile context, inspect manifest/provenance, and run benchmark fixtures.

**Resource safety**

- **FR-031**: System MUST bound request size, item size, package size and event size as **local safety limits**, never as commercial or usage quotas, and MUST NOT silently discard canonical state on rejection.

### Key entities

- **Vault** — an explicit root directory holding canonical files plus a `.fehrest/` control area.
- **Object** — a canonical text file with an embedded Fehrest UUID and a location.
- **Memory** — an explicit durable assertion with four semantic axes, bitemporal fields, scope, supersession links and provenance.
- **Event** — an append-only hash-chained record of a canonical or authorization-relevant operation.
- **Context package** — a bounded, budgeted, provenance-labelled evidence set produced for one principal, one scope and one query.
- **Served-item manifest** — the permanent record of what a package actually emitted.

---

## Success Criteria *(mandatory)*

### Technical (Phase T exit)

- **SC-001**: `cargo fmt --check`, `cargo check`, `cargo clippy -D warnings` and `cargo test` all pass.
- **SC-002**: Every applicable G3 kill test for an implemented surface passes; surfaces not implemented are marked `DEFERRED_SURFACE_NOT_PRESENT`, never `PASS`.
- **SC-003**: Deleting derived state and rebuilding produces equivalent query results.
- **SC-004**: Current-state resolution is correct on a hand-built temporal fixture with known ground truth.
- **SC-005**: Platform claims are honest — no `WINDOWS PASS` or `MACOS PASS` without native execution on that platform.

### Thesis (separate, and not implied by the above)

- **SC-006**: A benchmark harness can run identical continuation tasks across baseline arms and the Fehrest arm, with no Fehrest-only metadata leaking to baselines.
- **SC-007**: The Fehrest arm's continuation correctness is compared against **B0 plain agent**, **B1 repository-native docs**, **B3 lexical retrieval** and **B4 maintained LLM wiki** — the last being the bar that matters most.
- **SC-008**: Results are reported as measured, including negative results.

> **`cargo test` passing means `TECHNICAL_IMPLEMENTATION_PASS`. It does not mean `PRODUCT_THESIS_PASS`.** Security tests passing means the implemented properties hold — not that Fehrest is secure.

---

## Out of scope *(explicit — these are unauthorized, not merely deferred)*

```
UI · v0 output · React · Tauri · editor · canvas
MCP · Cedar · Graphify · graph retrieval · petgraph
vectors · embeddings · CRDT · sync · collaboration · cloud
plugins · automatic memory extraction/promotion/confirmation
dashboard · analytics · PDF/DOCX/OCR/audio ingestion
multi-user identity · remote service · telemetry · mandatory LLM
```

**If a generated task proposes any of the above, the task is wrong** — remove or defer it.

---

## Assumptions

- One vault, one user, one machine, one writer. Multi-vault and multi-user are out of scope.
- Canonical content for Phase T is Markdown-family text with YAML frontmatter carrying the UUID.
- Any persistence format introduced here is `EXPERIMENTAL_PHASE_T_FORMAT` / `NOT_PRODUCT_FORMAT_FREEZE`.
- No model or provider is required to run the Core or its tests.
- The benchmark's confirmatory sample size is **not** invented here; it follows the frozen pre-registration approach ([B-7b](../../docs/10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark)).
