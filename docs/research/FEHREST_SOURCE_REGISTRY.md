# Fehrest Source Registry

**Status:** CANONICAL RESEARCH REGISTRY
**Date verified:** 2026-08-17
**Purpose:** An auditable record of every external codebase, paper, standard, benchmark and product reference materially considered for Fehrest.

Fehrest must never become an untraceable amalgamation of external implementations. Every material external source is attributable to an exact upstream, and every source from which code may be reused carries an exact pinned commit or version.

**Authority note:** This registry is *evidence*, not authority. Where it conflicts with live repository truth, live truth wins. All measurements backing dispositions live in [EVIDENCE_LOG.md](EVIDENCE_LOG.md); registry entries cite them as `E-n`.

**Pinning rule:** `exact_commit_or_version` must be pinned before any code is copied or adapted. A moving branch (`main`, `master`, `canary`, `v8`) is **not** sufficient provenance for implementation. Two primary donors are pinned to commits below precisely because their default branches move.

---

## Legend

**Classes:** `CODE_DONOR` · `ARCHITECTURE_DONOR` · `PRODUCT_REFERENCE` · `RESEARCH` · `STANDARD` · `BENCHMARK` · `SECURITY_REFERENCE` · `DEVELOPMENT_GOVERNANCE_DONOR` *(F1-R2)* · `DEVELOPMENT_AGENT_DISCIPLINE` *(F1-R2)*

**Dispositions:** `USE` (direct dependency / substantially reused) · `ADAPT` (reuse but materially change) · `STUDY` (evidence only, never a dependency) · `BENCHMARK` (evaluate experimentally) · `DEFER` (useful, out of current phase) · `REJECT` (investigated, intentionally excluded) · `FOUNDATIONAL_STUDY` *(F1-R2 — shapes the product's framing and supplies a benchmark baseline; never a dependency)*

> **A `USE` disposition on a `DEVELOPMENT_*` class means "used to build Fehrest", never "shipped in Fehrest."** Development tooling is forbidden from any runtime dependency graph by [R-11](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules). The distinction is recorded in the legend because the word `USE` would otherwise carry a meaning it does not have for those entries.

**Fehrest layers:** `KNOWLEDGE` (canonical files) · `EVENT` (canonical activity log) · `DERIVED` (rebuildable indexes) · `MEMORY` · `AGENT` · `SECURITY` · `INGEST` · `UI` · `SHELL` · `EVAL`

---

## 0. Risk classification schema (added in F1-R1)

> **ADDED IN F1-R1 ([R1-20](../reviews/F1-R1-RECONCILIATION.md)).** F1's risk fields did not distinguish *current* from *historical* upstream problems. That omission directly caused both of its evidential errors: citing fixed Graphify bugs as live defects, and reading a stale distribution mirror as an unmaintained project.

Every donor risk record must separate six fields:

| Field | Meaning | Rule |
|---|---|---|
| `current_verified_state` | True at the pinned commit, verified this session | Must carry a verification date |
| `historical_issue` | A problem that existed and shaped the design | Must be marked historical |
| `fixed_issue` | Resolved upstream, with the fixing version | **Must never be cited as a current risk** |
| `unresolved_issue` | Live at the pinned commit | The only class that justifies a mitigation |
| `architectural_lesson` | The durable, defect-independent principle | Must survive upstream fixing everything |
| `fehrest_mitigation` | What Fehrest does | Must trace to an unresolved issue or a lesson — never to a fixed one |

**The test that matters:** an `architectural_lesson` must hold *even if every upstream bug is fixed*. F1's identity argument failed it. The reconstructed argument rests on design properties instead ([E-4](EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)).

**Second lesson, from the BlockSuite error:** repository-level health signals are unreliable when a project vendors its own packages. Verify the *subtree where development happens*, not the repository that mirrors it.

---

## 1. Dispositions changed in F1-R1

Two rounds of change are recorded. **F1** changed four dispositions from the founder's draft. **F1-R1 then corrected two of those changes** and reclassified two more, on evidence F1 missed.

### 1.1 Corrections to F1 (⚠️ F1 was wrong)

| Source | Draft | F1 | **R1** | Why F1 was wrong |
|---|---|---|---|---|
| **BlockSuite** | `USE`, S+ | ❌ **DEFER** ("unmaintained") | **CANDIDATE B** in the [Editor Gate](../18-EDITOR-GATE.md) | F1 measured the *standalone mirror* and concluded the editor was dead. `AFFiNE/blocksuite/…` is actively developed through 2026-08-10 ([E-10.1](EVIDENCE_LOG.md#e-101--the-evidence-f1-missed-the-affine-subtree-is-active)) |
| **CodeMirror 6** | *absent* | ❌ **USE** (decided) | **CANDIDATE A** in the Editor Gate | F1 decided the editor by argument rather than prototype ([R1-03](../reviews/F1-R1-RECONCILIATION.md)) |

### 1.2 Reclassifications in R1

| Source | F1 | **R1** | Reason |
|---|---|---|---|
| **Yjs** | DEFER (flat) | **CONDITIONAL / EDITOR-DEPENDENT** | Arrives with Candidate B if it wins; deferred otherwise. Collaboration must not be added to justify it ([R1-09](../reviews/F1-R1-RECONCILIATION.md)) |
| **AFFiNE** | STUDY | **STUDY + source of Candidate B** | Split license and monorepo size are real costs, but it is where the maintained editor lives |

### 1.3 Confirmed from F1

| Source | Disposition | Reason |
|---|---|---|
| **Graphify** | **ADAPT** — one implementation of a core, **explicitly falsifiable** product hypothesis | Identity conclusion unchanged, evidence re-grounded ([E-4](EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)). Runtime shape pending GI-BENCH. Capability itself removable on evidence ([F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)) |
| **DuckDB** | **DEFER** | Data Intelligence outside MVP by the brief's own scope |

---

## 2. Primary code donors

### 2.1 Graphify

```yaml
id: SRC-001
name: Graphify
class: [CODE_DONOR, ARCHITECTURE_DONOR, BENCHMARK]
repository_or_url: https://github.com/Graphify-Labs/graphify
upstream_owner: Graphify-Labs (Safi Shamsi and contributors)
exact_commit_or_version: 0738af373af9cf5c95f862cc5f3327fd96b4ea23   # branch v8, 2026-08-16T21:12:56+01:00
pypi_version: graphifyy==0.9.45
date_verified: 2026-08-17
decision: ADAPT            # not USE: consumed as a sidecar, boundary-wrapped, IDs rejected
fehrest_layer: DERIVED
relevant_upstream_paths:
  - graphify/extract.py          # AST extraction, dispatch table
  - graphify/extractors/         # per-language extractors
  - graphify/build.py            # extraction dicts -> NetworkX graph
  - graphify/cluster.py          # community detection
  - graphify/cache.py            # incremental extraction cache
  - graphify/ids.py              # ID normalisation -- STUDIED, NOT ADOPTED AS IDENTITY
  - graphify/security.py         # validate_url / validate_graph_path / sanitize_label
  - graphify/validate.py         # extraction-schema validation
  - graphify/watch.py            # filesystem watch + debounce
  - graphify/analyze.py          # god_nodes, graph_diff, import cycles
planned_fehrest_paths:
  - sidecar/graphify-host/       # process supervisor, IPC, lifecycle, resource caps
  - core/derived/graph/          # Fehrest-side graph ingestion + ID mapping
what_we_use:
  - Deterministic tree-sitter AST extraction across 28 bundled grammars
  - The {nodes, edges, relation, confidence} extraction schema as a wire contract
  - EXTRACTED / INFERRED confidence labelling
  - source_file + source_location provenance back to exact lines
  - Incremental extraction cache and filesystem-watch debounce semantics
  - graph_diff as the basis for incremental derived-index updates
  - security.py path-confinement and label-sanitisation patterns as prior art
what_we_do_not_use:
  - graphify/ids.py as an identity authority -- see risks
  - The MCP surface in serve.py (query_graph, get_node, get_neighbors, get_community,
    god_nodes, graph_stats, shortest_path, list_prs, get_pr_impact, triage_prs) -- Fehrest
    publishes its own scoped surface and never re-exports this one (E-7)
  - PR/repository tooling (list_prs, get_pr_impact, triage_prs) -- out of product scope
  - LLM-assisted semantic extraction paths and per-provider extras (llm.py, kimi/openai/
    anthropic/gemini/bedrock/ollama extras) -- violates the no-mandatory-LLM invariant
  - Neo4j / FalkorDB exporters -- would introduce a mandatory graph database
  - graphify-out/ as an output location -- Fehrest owns its own derived directory
why: >
  Measured deterministic extraction at ~18.4 files/s producing 97.2% EXTRACTED-confidence
  edges with line-level provenance and zero LLM cost (E-5, E-8). Reimplementing 60,202 lines
  across 28 grammars is not justified when the upstream is Apache-2.0 and actively developed.
current_verified_state:                  # verified 2026-08-17 at pinned commit
  - Identity layer is actively maintained and hardened: one `graphify.ids` module,
    guarded by contract + hypothesis property tests; `_disambiguate_colliding_node_ids`
    actively salts colliding ids apart.
  - Pre-1.0 (0.9.45) on a moving default branch named `v8`.
  - 32 packages / 130 MB site-packages excluding CPython.
  - Cold import ~4,451 ms / warm ~276 ms (PRELIMINARY, single environment).
fixed_issue:                             # MUST NOT be cited as current risk (R1-05)
  - "#2614 Turkish U+0130 idempotency -- FIXED in 0.9.40 (2026-08-11)"
  - "#811 Unicode collapse -- FIXED (NFKC + casefold + re.UNICODE)"
  - "#1033 AST-vs-semantic node-id mismatch -- FIXED at the relative-path remap chokepoint"
  - "#550 same-filename collisions -- ROOT CAUSE FIXED; four hand-synced copies unified
     into graphify.ids with property tests"
historical_issue:
  - The above formed a recurring 'ghost node' bug class that motivated the unified ids module.
    Historical only. F1 wrongly cited these as live defects; retracted in R1-05.
unresolved_issue:
  - Pre-1.0 API stability on a moving branch; API may break between versions.
  - Transitive CVE exposure in the optional HTTP/MCP stack (tracked upstream via pinned
    starlette floors, E-3).
  - Python parsers process untrusted vault content across worker subprocesses (H-5 unproven).
  - Incremental updates can retain stale derived edges until a forced rebuild.
architectural_lesson:                    # holds even if upstream fixes everything
  - Extractor IDs are name/path-derived BY DESIGN (file nodes spec'd `{parent_dir}_{stem}`)
    and extractor ID SCHEMES change across versions -- upstream explicitly rejected an
    alternative scheme because it "would rewrite every file and symbol id and force a
    full-rebuild migration". An identifier whose scheme is expected to change cannot
    anchor durable references. This is a property of extractors in general, not of Graphify.
  - Extractor confidence vocabularies are inputs to a trust model, never a trust model.
fehrest_mitigation:
  - G-ID-1..G-ID-4 invariants; Fehrest-owned UUIDv7 identity; extractor_id + extractor_version
    as rebuildable derived mapping only (ADR-0004, E §5.3).
  - Native evidence/trust model; extractor labels map in, unknown labels degrade to
    UNRESOLVED (F §3.3, R1-08).
  - Optional capability install for packaging weight; independent update channel.
  - Read-only, path-confined, no-credential, no-network worker; parser fuzzing (H-5).
  - Runtime shape PROVISIONAL pending GI-BENCH (R1-07).
update_strategy: >
  Pin to the commit above. Track upstream monthly. Re-pin only after (a) the extraction-schema
  contract test passes, (b) the ID-mapping rebuild test passes, and (c) dependency audit is
  clean. Never auto-update the sidecar with the application.
license: Apache-2.0, with MIT-licensed prior contributions retained in LICENSE-MIT
permission_status: >
  Permissive open-source terms. Apache-2.0 obligations: preserve LICENSE, NOTICE and
  attribution on any copied or adapted file; patent grant inherited. Founder states explicit
  reuse permission exists; that does not remove the attribution obligation.
provenance_notes: >
  Any adapted file must carry a header naming upstream repo, this commit, original path, and
  the modification summary, and must be recorded in the Code Provenance Ledger (section 9).
evidence: [E-1, E-2, E-3, E-4, E-5, E-6, E-7, E-8]
```

### 2.2 DeepSeek Harness

```yaml
id: SRC-002
name: DeepSeek Harness
class: [ARCHITECTURE_DONOR, CODE_DONOR]
repository_or_url: https://github.com/deepseek-ai/deepseek-harness
upstream_owner: deepseek-ai
exact_commit_or_version: 99f6f02fecdb7dff40c3fbc9470f5907c29f74ca   # master, 2026-08-17T19:03:17+08:00
date_verified: 2026-08-17
decision: ADAPT            # patterns only; explicitly NOT a runtime dependency
fehrest_layer: [EVENT, AGENT, SECURITY]
relevant_upstream_paths:
  - packages/core/session/src/types.ts     # SessionEventMap, SessionHeader
  - docs/subsystems/session.md             # append-only log, derived message history
  - docs/subsystems/persistence.md         # JSONL/SQLite dual backend, crash repair
  - docs/subsystems/approval.md            # branded ApprovalRequestId, fail-closed
  - docs/subsystems/spill.md               # oversized output -> opaque locator
  - docs/subsystems/sandbox.md             # SandboxMode vocabulary, platform backends
  - docs/subsystems/scope.md               # opaque ScopeKey identity
  - docs/subsystems/invariants.md          # package-owned runtime invariant registry
  - native/landlock-run/                   # Linux Landlock runner
planned_fehrest_paths:
  - core/event/            # append-only typed event log
  - core/event/recover/    # non-truncating crash repair
  - core/agent/approval/   # approval request/decide audit pair
  - core/agent/scope/      # capability scoping
what_we_use:
  - Append-only typed event log as the single source of truth, with agent-visible message
    history DERIVED from it and never stored separately; replay = re-derivation
  - One event type with two interchangeable backends and NO parallel persisted event type
  - Non-truncating crash repair: close an orphaned open turn with a synthetic terminator
    (reason `interrupted`) that no normal producer ever emits
  - Storage metadata (format version, cwd, lineage, seed boundary) held in a header OUTSIDE
    the event vocabulary so it never reaches derived agent-visible state
  - Merge-extensible event vocabulary so plugins add event types without forking the core
  - Branded, deliberately non-interchangeable identifiers for approvals vs tool calls vs sessions
  - Approval as a log-only asked/decided audit pair that fails closed unless explicitly allowed
  - Oversized payloads replaced by an opaque locator, with the documented rules
    "source is for naming and inspection, not access control" and "a suggested name is not a path"
  - Honest partial-enforcement reporting from sandbox backends instead of claiming uniform safety
  - Package-owned runtime invariants attributable to the owning module, asserting over
    authoritative event streams rather than service presence
what_we_do_not_use:
  - Cordis as a runtime framework -- would make an external meta-framework load-bearing for
    a system whose thesis is that it must outlive its dependencies
  - The TypeScript agent loop, plugin runtime, model adapters, compaction engine
  - apps/cli and apps/web
  - The sandbox vocabulary as a complete boundary: it governs filesystem effects ONLY, and
    the Windows ACL backend self-reports partial enforcement. Fehrest must specify network
    egress control independently (Threat Model T-11).
why: >
  This is the most directly applicable architecture donor in the registry. Its event-sourcing,
  crash-repair, approval-audit and identifier-branding patterns are exactly the problems
  Fehrest's Event Plane and Agent Gateway must solve, and they are documented at
  specification quality across 45 subsystem documents.
risks:
  - Pattern transplant across languages (TypeScript -> Rust/whatever Fehrest chooses) loses
    the compile-time guarantees that declaration merging and branded types provide. Mitigation:
    reproduce guarantees with the host language's type system plus runtime invariant checks.
  - Temptation to adopt Cordis "because the architecture is elegant". Explicitly rejected.
  - Upstream moves fast (HEAD same-day as measurement); documentation may drift from the pin.
update_strategy: >
  No dependency to update. Re-read the pinned subsystem docs before implementing each
  corresponding Fehrest subsystem. Record any pattern divergence in the relevant ADR.
license: MIT
permission_status: Permissive. MIT attribution required for any copied code.
provenance_notes: >
  Pattern adoption is recorded in ADR-0005 with the exact subsystem document cited. If any
  literal code is copied, it enters the Code Provenance Ledger with MIT attribution.
evidence: [E-9]
```

### 2.3 CodeMirror 6 — Candidate A

> **RECLASSIFIED IN F1-R1 ([R1-03](../reviews/F1-R1-RECONCILIATION.md)).** F1 recorded this as a settled `USE`. It is a **candidate** that must win the [Editor Gate](../18-EDITOR-GATE.md) on measured evidence, not a decision.

```yaml
id: SRC-003
name: CodeMirror 6
class: CODE_DONOR
repository_or_url: https://github.com/codemirror   # @codemirror/* packages published independently
upstream_owner: Marijn Haverbeke
exact_commit_or_version: "@codemirror/state@6.7.1"   # published 2026-07-05; pin full set at Phase 3E
date_verified: 2026-08-17
decision: CANDIDATE_A      # was F1: USE (decided)
resolved_by: Editor Gate (ADR-0002)
current_verified_state:
  - MIT, actively maintained. The archived codemirror/dev meta-repo is not the runtime;
    the @codemirror/* packages ship independently and are current.
strengths_to_test: [Markdown-native editing, canonical bytes ARE the document model,
                    external-file compatibility, low dependency weight, small install]
risks_to_expose: [rich blocks must be built separately, no page/canvas primitives inherited,
                  tables/databases/rich embeds may need substantial custom work,
                  block-level identity has no native home]
fehrest_layer: UI
relevant_upstream_paths: ["@codemirror/state", "@codemirror/view", "@codemirror/language", "@codemirror/search"]
planned_fehrest_paths:
  - ui/editor/
what_we_use:
  - Text editing surface over Markdown, where the document model IS the canonical bytes
  - Decoration/widget layer for rendering links, backlinks and provenance affordances
  - Incremental parsing for syntax-aware editing
what_we_do_not_use:
  - Any hidden document state that is not reconstructable from the canonical file
why: >
  Selecting a Markdown-native editing surface makes canonical round-trip an identity function
  rather than a lossy mapping, which dissolves the round-trip architecture gate instead of
  attempting to solve it (ADR-0002). MIT, current, no CRDT requirement, no block model to
  serialise. The archived codemirror/dev meta-repo is not the runtime; the packages are live.
risks:
  - No block-level identity, transclusion, or inline comments out of the box. These are the
    features BlockSuite would have supplied. Mitigation: documented sidecar for identity and
    annotations; features gated behind H-4 falsification.
  - Rich editing expectations from the founder's AFFiNE/Obsidian references are not met in v1.
    This is an explicit, stated MVP cost, not an oversight.
update_strategy: Pin the full package set in a lockfile at Phase 3. Standard npm audit cadence.
license: MIT
permission_status: Permissive.
provenance_notes: Ordinary dependency; no code copying anticipated.
evidence: [E-11]
```

---

## 3. Deferred and rejected editing substrates

### 3.1 BlockSuite — Candidate B in the Editor Gate

> **RECLASSIFIED IN F1-R1 ([R1-02](../reviews/F1-R1-RECONCILIATION.md)).** F1 deferred BlockSuite as "unmaintained." **That was wrong.** F1 measured the standalone mirror and missed that the editor is actively developed inside AFFiNE.

```yaml
id: SRC-004
name: BlockSuite
class: CODE_DONOR
repository_or_url: https://github.com/toeverything/AFFiNE   # blocksuite/ subtree -- NOT the standalone mirror
upstream_owner: toeverything
exact_commit_or_version: PIN AT PHASE 3E    # AFFiNE canary observed at b4c8548c (2026-08-17)
superseded_source: >
  toeverything/blocksuite @ 5cb5cb68471ca692f3c162258f0087cb22fcb82d (main, 2025-07-07).
  STALE MIRROR -- do NOT evaluate or vendor this. npm @blocksuite/store@0.22.4 last
  published 2025-07-01.
date_verified: 2026-08-17
decision: CANDIDATE_B      # was F1: DEFER; was draft: USE/PROTOTYPE S+
fehrest_layer: UI
current_verified_state:
  - AFFiNE blocksuite/ subtree received commits through 2026-08-10, including
    "feat(editor): improve select perf" (#15353), "feat(editor): code block line
    numbers" (#15376), "fix(mobile): keyboard padding" (#15365), "chore: bump
    typescript 7" (#15465), and "chore: bump up js-yaml v5 [SECURITY]" (#15385).
  - The editor implementation is ACTIVELY MAINTAINED.
historical_issue:
  - The standalone toeverything/blocksuite repository stopped syncing 2025-07-07.
  - Six renovate/npm-*-vulnerability branches are open and unmerged ON THAT MIRROR.
fixed_issue:
  - Security dependency bumps land in the maintained AFFiNE tree (#15385), so the
    "unpatched transitive vulnerabilities" argument applies to the mirror, not to the
    code that would actually be vendored.
unresolved_issue:
  - No independent release channel; vendoring from a 446 MB application monorepo.
  - Coupling to AFFiNE-specific infrastructure is unmeasured.
  - Split license: MIT applies OUTSIDE packages/backend and packages/common/native.
    Per-file license provenance required for every vendored file.
  - Maintenance burden if Fehrest diverges from upstream.
architectural_lesson:
  - Repository-level health signals are unreliable when a project vendors its own
    packages. Verify the subtree where development happens, not the mirror.
what_we_evaluate:
  - Block architecture; Page + Edgeless primitives; rich blocks; databases/data views;
    editing interaction model; canonical-file round-trip behaviour (P-1..P-6).
what_we_do_not_evaluate:
  - The stale standalone package, under any circumstances.
fehrest_mitigation:
  - Evaluated only through the Editor Gate against a pinned AFFiNE commit.
  - Eliminated on packaging grounds if extraction proves untenable (F-5) -- a DIFFERENT
    and legitimate reason, to be recorded precisely if it occurs.
license: AFFiNE split -- MIT outside packages/backend and packages/common/native
evidence: [E-10, E-10.1]
```

### 3.2 Yjs — CONDITIONAL / EDITOR-DEPENDENT

> **RECLASSIFIED IN F1-R1 ([R1-09](../reviews/F1-R1-RECONCILIATION.md)).** F1's flat `DEFER` was too coarse: whether a CRDT enters v1 is a **consequence of the Editor Gate**, not an independent choice.

```yaml
id: SRC-005
name: Yjs
class: [CODE_DONOR, RESEARCH]
repository_or_url: https://github.com/yjs/yjs
exact_commit_or_version: yjs@13.6.32     # published 2026-08-04
date_verified: 2026-08-17
decision: CONDITIONAL      # was F1: DEFER
resolved_by: Editor Gate (ADR-0002) via ADR-0012
fehrest_layer: KNOWLEDGE
current_verified_state:
  - MIT licensed, actively released (13.6.32, 2026-08-04). NO maintenance objection.
conditional_outcomes:
  - if_candidate_B_wins: >
      Yjs arrives AS PART OF the editing substrate. Not a separate adoption decision.
      The gate's ADR must then specify which CRDT state is canonical, which is
      collaboration-specific, and which is transient (18-EDITOR-GATE section 4).
  - if_candidate_A_or_C_wins: >
      Yjs stays deferred until collaboration or sync independently justifies it.
hard_constraint: >
  Collaboration must NOT be added to the MVP in order to justify a CRDT. If a CRDT
  arrives, it arrives because the winning editor uses it for local document state.
unresolved_issue:
  - Whether CRDT operation history is canonical document meaning is OPEN, not settled
    (R1-04). F1 assumed it was; that assumption is retracted.
constraint_when_adopted: >
  One CRDT runtime only. Do not combine with Automerge without a dedicated ADR proving
  a need neither satisfies alone.
license: MIT
evidence: [E-11]
```

### 3.3 AFFiNE — STUDY + source of Candidate B

> **RECLASSIFIED IN F1-R1 ([R1-02](../reviews/F1-R1-RECONCILIATION.md)).** AFFiNE is not only a product reference — it is **where the maintained BlockSuite editor lives** ([SRC-004](#31-blocksuite--candidate-b-in-the-editor-gate)).

```yaml
id: SRC-006
name: AFFiNE
class: [PRODUCT_REFERENCE, CODE_DONOR]
repository_or_url: https://github.com/toeverything/AFFiNE
exact_commit_or_version: b4c8548c09da21b2898443559a5b846f0ccf5dd8   # canary, 2026-08-17
date_verified: 2026-08-17
decision: STUDY + SOURCE_OF_CANDIDATE_B
fehrest_layer: UI
current_verified_state:
  - Actively developed; canary HEAD 2026-08-17.
  - Contains blocksuite/ as an in-repo subtree (affine, framework, playground,
    integration-test), which receives ongoing editor feature and security work.
what_we_study: [workspace UX, document/canvas/database view concepts, local-first app patterns]
what_we_may_vendor: >
  ONLY the blocksuite/ subtree, ONLY at a pinned commit, ONLY if it wins the Editor Gate,
  and ONLY with per-file license provenance established first.
what_we_do_not_use:
  - The application itself. Fehrest is NOT an AFFiNE fork -- explicitly rejected.
  - Anything under packages/backend or packages/common/native (separate license).
unresolved_issue:
  - Split license: MIT applies only OUTSIDE packages/backend and packages/common/native.
    Per-file provenance is mandatory before any vendoring.
  - 446 MB monorepo; extraction cost and coupling depth are unmeasured (Phase 3E measures).
  - No independent release channel for the editor subtree.
architectural_lesson:
  - A project can be simultaneously an unusable dependency (no releases) and a viable
    code donor (maintained subtree). These require separate assessments.
license: Split -- MIT outside packages/backend and packages/common/native; separate license within
evidence: [E-10, E-10.1]
```

### 3.4 Automerge — STUDY

```yaml
id: SRC-007
name: Automerge
class: [ARCHITECTURE_DONOR, RESEARCH]
repository_or_url: https://github.com/automerge/automerge
exact_commit_or_version: UNPINNED   # study only; pin before any code use
date_verified: 2026-08-17
decision: STUDY
fehrest_layer: KNOWLEDGE
what_we_use: [local-first model, sync protocol design, history and branching concepts]
why: Conceptual input to the eventual sync ADR. Not a v1 dependency.
constraint: Do not combine with Yjs in the initial editing architecture absent demonstrated need.
```

---

## 4. Storage and retrieval

| id | Source | Class | Version / pin | Disposition | Layer | Rationale | Evidence |
|---|---|---|---|---|---|---|---|
| SRC-010 | **SQLite** | CODE_DONOR / STANDARD | pin at Phase 1 (bundled) | **USE** | DERIVED | Local structured derived state and the non-canonical event mirror. Ubiquitous, embedded, crash-tested, public domain. | E-9 |
| SRC-011 | **SQLite FTS5** | CODE_DONOR | ships with SQLite | **USE** | DERIVED | Lexical retrieval baseline. Retrieval must function with zero embeddings; BM25 is the floor Fehrest must beat before adding vectors. | E-8 |
| SRC-012 | **sqlite-vec** | CODE_DONOR | `v0.1.10-alpha.4` / stable `v0.1.9` | **BENCHMARK**, must remain optional | DERIVED | Candidate embedded ANN. Current release line is **alpha**; last push 2026-05-18. Alpha status alone forbids it being required. | E-12 |
| SRC-013 | **USearch** | CODE_DONOR | pin at benchmark time | **BENCHMARK** | DERIVED | Alternative embedded ANN. Apache-2.0, active. Compare against sqlite-vec on the same corpus. | E-12 |
| SRC-014 | **Tantivy** | CODE_DONOR | pin if adopted | **BENCHMARK** (contingent) | DERIVED | Evaluate **only if** FTS5 fails measured budgets in [O](../14-PERFORMANCE-BUDGETS.md). MIT, pushed day-of-measurement. Adding it before FTS5 fails is unjustified complexity. | E-12 |
| SRC-015 | **LanceDB** | CODE_DONOR | — | **DEFER** | DERIVED | Multimodal/high-scale local vectors. Do not make mandatory until the simpler stack demonstrably fails. | — |
| SRC-016 | **FAISS** | CODE_DONOR / BENCHMARK | — | **STUDY** | DERIVED | Reference implementation for ANN quality comparison. Not an embedded-desktop candidate. | — |
| SRC-017 | **CozoDB** | ARCHITECTURE_DONOR | — | **STUDY** | DERIVED | Embedded relational + Datalog graph querying. Interesting; not canonical storage without separate proof. | — |
| SRC-018 | **DuckDB** | CODE_DONOR | — | **DEFER** (was: USE, Priority S) | DERIVED | Downgraded: the brief places Data Intelligence outside MVP, so a Priority-S disposition contradicts the scope. Revisit when dataset/analytics objects enter scope. | — |
| SRC-019 | **NetworkX** | CODE_DONOR (transitive) | `>=3.4` via Graphify | **USE** (inside sidecar only) | DERIVED | Graphify's in-memory graph representation. Confined to the sidecar; never Fehrest's canonical or query-time structure. | E-3 |

**Registry-level invariant:** no entry in this section may become required for core function except SQLite and FTS5. Vectors and alternative engines are accelerators.

### 4.14 Apache Spark — STUDY / DEFER

> **ADDED IN F1-R2 ([R2-07](../reviews/F1-R2-RECONCILIATION.md)).** Recorded because a concept was taken from it, and the registry's purpose is that every material external influence is attributable. **Fehrest takes concepts from Spark and none of its machinery.**

```yaml
id: SRC-100
name: Apache Spark
class: [ARCHITECTURE_DONOR, SCALE_REFERENCE]
repository_or_url: https://github.com/apache/spark
upstream_owner: The Apache Software Foundation
exact_commit_or_version: UNPINNED
  # STUDY only. Concepts are read from published design documentation, not from
  # source. Section 11 CI rule 2 forbids any transition to ADAPT/USE without
  # pinning first -- and no such transition is anticipated.
date_verified: 2026-08-17
decision: STUDY / DEFER
fehrest_layer: DERIVED
adopt_concepts:
  - "Lineage as DATA: a derived artifact records what it was derived FROM and
     by WHICH deriver version. Fehrest's derivation registry (E section 10) is
     this idea and nothing else."
  - "A checkpoint as truncation of RECOMPUTATION DEPTH, not as a source of
     truth. This is exactly why Fehrest checkpoints are derived,
     non-authoritative and disposable (E section 11)."
  - "Bounded batch and backpressure lessons WHERE JUSTIFIED -- applicable to
     resumable background rebuilds, not adopted wholesale."
reject_for_v1:
  - Spark runtime
  - JVM requirement
  - driver/executor architecture
  - cluster execution
  - RDD / DataFrame as a runtime dependency
  - Structured Streaming runtime
  - GraphX / Pregel dependency
  - DAG scheduler
  - lazy distributed recomputation
why_not_more: >
  Fehrest is a single-user local-first desktop system whose largest v1 target is
  100K files on one machine (O section 2). Spark solves distributed execution over
  cluster-scale data. The scale mismatch is several orders of magnitude, and the
  governing principle -- "the user's knowledge must survive Fehrest itself" --
  is directly contradicted by acquiring a JVM and a cluster computing framework
  as load-bearing dependencies. This is the same argument that rejected Cordis
  (ADR-0005): elegance is not a reason to take a dependency.
architectural_lesson:
  - "A system can be an excellent source of ONE idea and a catastrophic source of
     an architecture. Adopting a concept is not adopting a runtime, and the
     registry must record which of the two happened."
overstatement_guard: >
  No claim is made that Spark's designers endorse this use, that Fehrest
  implements Spark semantics, or that lineage-as-data originates with Spark.
  Fehrest takes a framing, credits where it read it, and implements its own
  minimal Rust-native version.
license: Apache-2.0
evidence: []
```

---

## 5. Ingestion

| id | Source | Class | Version / pin | Disposition | Layer | Rationale | Evidence |
|---|---|---|---|---|---|---|---|
| SRC-020 | **Google Magika** | CODE_DONOR | pin at Phase 4 | **USE** | INGEST | Content-based type detection *before* dispatching a parser. Security-relevant: extension-based dispatch is a parser-confusion attack surface (T-12). Apache-2.0, active. | E-13 |
| SRC-021 | **Docling** | CODE_DONOR | pin at Phase 4 | **ADAPT** (optional capability) | INGEST | High-fidelity local document extraction. MIT, 64,911 stars, pushed day-of-measurement. Must be an optional install: it carries a heavy ML dependency tree that would otherwise violate the offline/no-model floor. | E-13 |
| SRC-022 | **Microsoft MarkItDown** | CODE_DONOR | pin at Phase 4 | **ADAPT** (fallback) | INGEST | Lightweight conversion path when Docling is not installed. MIT. Lower fidelity, far lower weight. | E-13 |
| SRC-023 | **Mozilla PDF.js** | CODE_DONOR | pin at Phase 5 | **USE** (rendering only) | UI | PDF *rendering*. Explicitly not the knowledge-extraction pipeline. | — |
| SRC-024 | **PaddleOCR** | CODE_DONOR | — | **DEFER** | INGEST | Optional local OCR for scanned documents. Not v1. | — |
| SRC-025 | **whisper.cpp** | CODE_DONOR | — | **DEFER** | INGEST | Optional local transcription. Not v1. | — |
| SRC-026 | **tree-sitter** | CODE_DONOR | `>=0.23,<0.26` via Graphify | **USE** (via sidecar) | DERIVED | Code parsing. Consumed through Graphify rather than integrated directly, to avoid maintaining 28 grammar bindings ourselves. | E-3 |

**Registry-level invariant:** every ingestion path must record provenance back to the original source bytes (content hash + byte offsets or page/line locators). An extractor that cannot produce provenance is not eligible for adoption.

---

## 6. Local AI (all optional by constitution)

| id | Source | Class | Disposition | Layer | Rationale | Evidence |
|---|---|---|---|---|---|---|
| SRC-030 | **llama.cpp** | CODE_DONOR | **USE as optional provider** | MEMORY / AGENT | Optional local inference, embeddings, reranking, classification. MIT, pushed day-of-measurement. Fehrest must pass its full core test suite with this absent. | E-13 |
| SRC-031 | **ONNX Runtime GenAI** | CODE_DONOR | **BENCHMARK** | MEMORY | Candidate alternative local runtime. Compare startup, memory and throughput before choosing. | — |
| SRC-032 | **Commercial model APIs** (Claude, Codex, Gemini, GLM, …) | — | **USE as optional BYOK providers** | AGENT | No single commercial provider may be embedded in the architecture. Provider adapters sit behind one replaceable seam. | — |

---

## 7. Agent protocol, authorization, isolation

| id | Source | Class | Disposition | Layer | Rationale | Evidence |
|---|---|---|---|---|---|---|
| SRC-040 | **Model Context Protocol** | STANDARD | **USE** | AGENT | Fehrest exposes bounded memory/context capabilities over MCP. **MCP is a transport, not an authorization boundary** — authorization is enforced inside Fehrest before any tool executes. | E-7 |
| SRC-041 | **Tauri 2 capabilities** | CODE_DONOR / SECURITY_REFERENCE | **STUDY → likely USE** | SHELL | Desktop least-privilege boundary between webview and native core. Apache-2.0, active. Adoption confirmed by ADR at Phase 3, not assumed now. | E-13 |
| SRC-042 | **AWS Cedar** | CODE_DONOR / SECURITY_REFERENCE | **ADAPT** (model), **DEFER** (engine) | SECURITY | Adopt the `principal + action + resource + context` decision shape for the capability model. Embedding the engine is a separate, later decision. Apache-2.0, active. | E-13 |
| SRC-043 | **Wasmtime / WASI Component Model** | CODE_DONOR / STANDARD | **DEFER** | SECURITY | Candidate isolation boundary for future untrusted plugins. Not needed until third-party plugins exist; a plugin system is explicitly out of MVP. | E-13 |
| SRC-044 | **Landlock / bwrap / Seatbelt / Windows restricted tokens** | SECURITY_REFERENCE | **STUDY → ADAPT** | SECURITY | Platform confinement primitives, reached via the harness's documented backends. Note the honest upstream limits: filesystem effects only, Windows partially enforced. | E-9 |

---

## 8. Research canon

Papers are evidence, not authority. Each entry states what Fehrest takes and what it explicitly does not.

| id | Source | Class | Identifier | Disposition | What Fehrest takes | What Fehrest rejects |
|---|---|---|---|---|---|---|
| SRC-050 | **Local-first Software** (Kleppmann et al.) | RESEARCH | — | **STUDY / ALIGN** | The seven ideals as a design test; "the network is an optimisation" framing | Its assumption that CRDTs are the natural substrate — Fehrest defers CRDTs (SRC-005) |
| SRC-051 | **LongMemEval** | BENCHMARK | ICLR 2025, `xiaowu0162/LongMemEval` | **BENCHMARK** | Information extraction, temporal reasoning, knowledge updates, abstention as test axes | Using LongMemEval-S at n=50 as an acceptance threshold — the interval is ±~12 pp (E-8) |
| SRC-052 | **LongMemEval-V2** | BENCHMARK | arXiv `2605.12493`; HF `xiaowu0162/longmemeval-v2` | **BENCHMARK — primary** | The five measured abilities as the memory model's specification: static state recall, dynamic state tracking, workflow knowledge, environment gotchas, premise awareness. Latency as a co-equal metric. | Taking 72.5%/48.5%/69.3% as reproduced — VENDOR-REPORTED until re-run locally |
| SRC-053 | **MemGPT** | RESEARCH | — | **STUDY** | Tiered memory, paging between working and long-term context | Virtual-context paging as a requirement — Fehrest's compiler is a deterministic pipeline, not an LLM-managed pager |
| SRC-054 | **A-MEM (Agentic Memory)** | RESEARCH | — | **STUDY** | Zettelkasten-style memory linking and evolution; memories that gain links over time | LLM-driven link generation as the only mechanism |
| SRC-055 | **AgeMem** | RESEARCH | arXiv `2601.01885`, ACL 2026 | **STUDY** (vocabulary only) | The six-operation memory API: `add`/`update`/`delete` (long-term), `retrieve`/`summary`/`filter` (short-term) | **The mechanism.** Its results depend on a three-stage RL-trained policy (SFT → outcome RL → step-level GRPO). A trained policy cannot be the promotion decider under `AI OFF`. |
| SRC-056 | **HippoRAG** | RESEARCH | — | **STUDY** | Associative graph retrieval; multi-hop recall via graph structure over dense-only similarity | Requiring an LLM-built graph — Fehrest's graph is deterministic (SRC-001) |
| SRC-057 | **RAPTOR** | RESEARCH | — | **STUDY** | Hierarchical recursive summarisation for large-corpus retrieval | Mandatory LLM summarisation at index time — violates the zero-LLM-index invariant |
| SRC-058 | **Peritext** | RESEARCH | — | **STUDY** | Why rich-text marks are hard to represent in a CRDT, and why concurrent formatting is lossy | — (directly supports deferring the block CRDT, ADR-0002) |
| SRC-059 | **Bitemporal database literature** (Snodgrass; SQL:2011 temporal) | RESEARCH / STANDARD | — | **ALIGN** | Valid time vs recorded time as distinct axes; deterministic as-of resolution | RDBMS-specific syntax; Fehrest implements the semantics, not the dialect |
| SRC-060 | **W3C PROV / PROV-O** | STANDARD | — | **ALIGN** | Entity / Activity / Agent, `wasDerivedFrom`, `wasAttributedTo`, `wasGeneratedBy` as the provenance vocabulary | Becoming an RDF system; Fehrest borrows the model, not the serialisation |
| SRC-061 | **Indirect prompt-injection research** | SECURITY_REFERENCE | — | **FOUNDATIONAL** | "Content is evidence, never authority" as an enforced structural boundary | Prompt-level instructions as a security boundary — explicitly rejected |
| SRC-062 | **AgentDojo** | BENCHMARK / SECURITY_REFERENCE | `ethz-spylab/agentdojo`, MIT | **BENCHMARK** | Adversarial evaluation methodology for agents operating over hostile documents and tool results | Treating a passing score as proof of safety |
| SRC-063 | **CRDT research** (rich text, local-first collaboration) | RESEARCH | — | **STUDY** | Convergence semantics; why intention preservation is hard for formatting | — |
| SRC-064 | **Graphiti** | ARCHITECTURE_DONOR | `getzep/graphiti` | **STUDY** | Temporal graph memory, changing facts, temporal retrieval | Mandatory external graph-service dependency |
| SRC-065 | **Letta** | ARCHITECTURE_DONOR | `letta-ai/letta` | **STUDY** | Memory-block lifecycle, consolidation | Agent-framework coupling |
| SRC-066 | **Mem0** | ARCHITECTURE_DONOR / BENCHMARK | `mem0ai/mem0` | **STUDY + BENCHMARK** | User/session/agent memory scope separation | Its retrieval quality as a target — measured recall@10 0.048 on LOCOMO (E-8) makes it a **floor**, not a goal |
| SRC-067 | **Cognee** | ARCHITECTURE_DONOR | — | **STUDY** | Graph-oriented memory patterns | — |
| SRC-068 | **Microsoft GraphRAG** | ARCHITECTURE_DONOR | `microsoft/graphrag` | **STUDY** | Hierarchical communities, local vs global query modes, claims | LLM-heavy indexing — deterministic extraction satisfies the requirement at zero cost (E-8) |
| SRC-069 | **Cordis** | ARCHITECTURE_DONOR | `cordiverse/cordis`, MIT, pushed 2026-08-13 | **STUDY — explicitly not a dependency** | Plugin composition, reversible effects, scoped services, effect-scoped disposal | Cordis itself. Making an external meta-framework load-bearing contradicts "the user's knowledge must survive Fehrest itself." | E-13 |

### 8.2 Andrej Karpathy — LLM Wiki

> **ADDED IN F1-R2.** The original "LLM Wiki" gist. Added to the research canon as a **FOUNDATIONAL_STUDY**: it names the distinction Fehrest's thesis rests on, and it supplies the strongest *simple* baseline the benchmark plan has.

```yaml
id: SRC-101
name: Andrej Karpathy -- LLM Wiki (original gist)
class: [RESEARCH, ARCHITECTURE_DONOR, PRODUCT_REFERENCE]
upstream_owner: Andrej Karpathy
exact_commit_or_version: PIN AT RESEARCH FREEZE
  # Registry pinning rule: a specific gist revision must be pinned before the
  # baseline harness is built (Phase T). No code is copied from it; the pin
  # exists so the BASELINE is reproducible, per section 12.
date_verified: 2026-08-17
decision: FOUNDATIONAL_STUDY
fehrest_layer: [KNOWLEDGE, MEMORY, EVAL]

the_lesson:
  - "RAG repeatedly RECONSTRUCTS understanding from raw sources on every query."
  - "The LLM-Wiki pattern instead creates a PERSISTENT, MAINTAINED, INTERLINKED
     knowledge artifact that COMPOUNDS over time."
  - "That second framing is much closer to Fehrest's thesis than any RAG variant,
     and it is achievable with a directory of Markdown files and no system."

what_fehrest_takes:
  - The framing above, which sharpens what Fehrest is actually claiming.
  - A benchmark baseline: raw sources + a maintained Markdown wiki + explicit
    links + ordinary agent search/read (K section 3.1, baseline 5).

what_fehrest_must_therefore_prove:
  # This is the obligation the baseline creates. Beating a plain agent while
  # tying a maintained wiki would mean the value is in HAVING a maintained
  # artifact -- a materially smaller product than the one described in A.
  - measurable value from temporal state
  - measurable value from supersession
  - measurable value from provenance
  - measurable value from deterministic context compilation
  - measurable value from the agent experience
  - measurable value from optional Graph Intelligence

what_fehrest_does_not_claim:
  - >
    NO ENDORSEMENT IS CLAIMED OR IMPLIED. Karpathy has not endorsed Fehrest,
    Graphify, Graph Intelligence, or any architectural position in this package.
    No such endorsement is established, and none may be asserted anywhere in
    this repository. The pattern is used as a BASELINE and a FRAMING -- as
    something to beat and to think with -- never as an authority.

architectural_lesson:
  - "The strongest competitor to a complex system is often a simple discipline
     practised consistently. A benchmark plan whose baselines are all weak
     measures only that they were weak."
license: not applicable -- no code reused
evidence: []
```

---

## 8A. Development and governance tooling

> **ADDED IN F1-R2** for founder decisions D-2 and D-3. **Everything in this section is used to BUILD Fehrest and ships in nothing.** [R-11](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) makes that a build-breaking rule rather than an intention. Full method: [S — Engineering Method](../19-ENGINEERING-METHOD.md); decision: [ADR-0014](../09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail).

### 8A.1 GitHub Spec Kit

```yaml
id: SRC-102
name: GitHub Spec Kit
class: DEVELOPMENT_GOVERNANCE_DONOR
repository_or_url: https://github.com/github/spec-kit
upstream_owner: GitHub
exact_commit_or_version: PIN AT PHASE 0
  # Pinned when the workflow is stood up. Not installed during F1-R2.
date_verified: 2026-08-17
decision: USE                    # as DEVELOPMENT tooling only
fehrest_layer: not applicable -- development workflow, no runtime layer
runtime_dependency: NO           # R-11: build fails if it reaches a shipped graph
what_we_use:
  - The specification-driven lifecycle:
    constitution -> specify -> clarify -> plan -> checklist -> tasks
                 -> analyze -> implement -> converge
  - Full production lifecycle where appropriate; a justified reduced workflow
    for small bounded work, with the justification recorded on the change.
what_we_do_not_use:
  - Spec Kit as runtime architecture. It is a development workflow; treating it
    as architecture is a category error.
  - Its constitution stage as a SECOND source of invariants. Fehrest's
    invariants live in B (01-ARCHITECTURE-CONSTITUTION.md) and nowhere else;
    the Spec Kit constitution is derived from them.
why: >
  Fehrest is built largely by AI coding agents against a specification-heavy
  planning package. Without an artifact binding code to specification, drift is
  detected only at review -- the most expensive point. See ADR-0014.
not_yet_done: >
  NOT installed, NOT initialized, and NO implementation workflow executed during
  F1-R2. Stood up at Phase 0.
license: MIT
```

### 8A.2 Ponytail

```yaml
id: SRC-103
name: Ponytail
class: DEVELOPMENT_AGENT_DISCIPLINE
repository_or_url: https://github.com/DietrichGebert/ponytail
upstream_owner: DietrichGebert
exact_commit_or_version: PIN AT PHASE 0
date_verified: 2026-08-17
decision: USE                    # as DEVELOPMENT agent discipline only
fehrest_layer: not applicable -- development discipline, no runtime layer
runtime_dependency: NO           # R-11; and never installed as runtime code
what_we_use:
  - The implementation-minimisation / reuse-first necessity gate:
    1 does this need to exist?  2 does Fehrest already implement it?
    3 Rust std/core or a platform primitive?  4 an approved dependency?
    5 a smaller implementation?  6 then the minimum correct solution.
what_ponytail_must_never_minimise:      # the list IS the decision
  - authorization boundaries
  - canonical-data integrity
  - security controls
  - recovery correctness
  - provenance
  - privacy
  - data-loss prevention
  - required accessibility
  - invariant tests
why_the_exclusions_are_load_bearing: >
  A minimisation discipline applied by an agent optimising for less code will,
  given the chance, argue that an authorization chokepoint "does not need to
  exist" -- answering the gate's own question 1 in the affirmative. Each such
  argument is locally plausible and globally catastrophic. On excluded paths the
  answer to question 1 is FIXED by the constitution; the gate governs only HOW.
not_yet_done: >
  NOT installed into the project, and specifically NOT installed as runtime code.
  Stood up at Phase 0 as development tooling.
license: verify at pin time before any adoption
```

---

## 9. Product references

Recorded as **specific mechanisms**, never as "inspiration."

| id | Source | Disposition | Specific mechanism studied |
|---|---|---|---|
| SRC-070 | **Obsidian** | STUDY | Vault semantics; files remain useful without the app; backlink computation; `[[wikilink]]` resolution; local plugin model; graph view; keyboard-first command palette |
| SRC-071 | **JSON Canvas** | **ALIGN / USE** (deferred to Phase 6) | Open canvas file format (`obsidianmd/jsoncanvas`, MIT, active). Candidate canonical representation for canvas objects — adopted as the format when canvas ships, not as an MVP feature |
| SRC-072 | **Linear** | STUDY | Keyboard-first interaction; issue/project hierarchy; instant command surfaces; optimistic local state |
| SRC-073 | **Logseq** | STUDY | Block-level identity in a plain-text file; outliner-native storage; block references and their file-format cost |
| SRC-074 | **SiYuan** | STUDY | Block-level database over local files; local-first with optional sync |
| SRC-075 | **AppFlowy** | STUDY | Local-first database/board views over a native core; Rust core + web UI split |
| SRC-076 | **Airtable** | STUDY | One dataset, many views; interface/view separation; relational structured-data UX |
| SRC-077 | **Teable / Baserow / NocoDB** | STUDY | Open implementations of spreadsheet-database UX |
| SRC-078 | **Plane** | STUDY | Open project/work-management data model |
| SRC-079 | **Microsoft Data Formulator** | DEFER | Agentic data exploration; transformation lineage; data-thread concept |
| SRC-080 | **Apache Superset** | STUDY / DEFER | Semantic metrics layer; dataset/dashboard separation |
| SRC-081 | **Google TimesFM** | DEFER | Local forecasting over user datasets. Explicitly outside the long-memory core |
| SRC-082 | **Cytoscape.js** | DEFER (was PROTOTYPE) | Graph exploration rendering. Graph explorer is cut from MVP; see [P](../15-IMPLEMENTATION-PHASES.md) |
| SRC-083 | **xyflow / React Flow** | STUDY | Node-graph interaction for agent/workflow visualisation |
| SRC-084 | **Excalidraw** | STUDY | Canvas interaction, gestures, export |
| SRC-085 | **tldraw** | STUDY | Canvas runtime design. **Constraint:** do not introduce a second canvas runtime |
| SRC-086 | **draw.io** | STUDY | Structured diagrams, shape libraries, connectors, import/export |

---

## 10. Security verification toolchain

Each tool receives its own pinned record when adopted in [L](../11-SECURITY-VERIFICATION-PLAN.md).

| id | Source | Disposition | Role |
|---|---|---|---|
| SRC-090 | **CodeQL** | USE | Static analysis in CI |
| SRC-091 | **Semgrep** | USE | Rule-based static analysis, custom Fehrest invariant rules |
| SRC-092 | **OSV-Scanner** | USE | Dependency vulnerability scanning across ecosystems |
| SRC-093 | **cargo-audit / cargo-deny** | USE | Rust advisory + license/duplicate policy |
| SRC-094 | **npm audit / pnpm audit** | USE | JS ecosystem advisories |
| SRC-095 | **pip-audit** | USE | Python sidecar advisories — required given the 32-package sidecar tree (E-3) |
| SRC-096 | **cargo-fuzz / libFuzzer** | USE | Parser and event-log fuzzing |
| SRC-097 | **ClusterFuzzLite** | DEFER → USE at Phase 4 | Continuous fuzzing in CI once parsers land |
| SRC-098 | **proptest / hypothesis** | USE | Property tests for bitemporal resolution and ID stability |
| SRC-099 | **Sigstore / SLSA provenance** | DEFER | Release supply-chain attestation before public distribution |

---

## 11. Code provenance ledger

Machine-auditable, appended at the moment code is copied or adapted — never reconstructed later.

**Current state: EMPTY. No code has been written or adapted. No implementation has been performed.**

Required schema:

```yaml
- donor: Graphify-Labs/graphify
  upstream_commit: "0738af373af9cf5c95f862cc5f3327fd96b4ea23"
  upstream_path: "graphify/extract.py"
  fehrest_path: "<DESTINATION>"
  use: "adapted"            # verbatim | adapted | reimplemented-from-reading
  modifications:
    - "<DESCRIPTION>"
  license_obligation: "Apache-2.0: retain LICENSE + NOTICE, state changes"
  imported_at: "<DATE>"
  verified_by: "<REVIEWER>"
```

**Enforcement (CI, from Phase 1):**
1. Every file containing donor-derived code carries a machine-readable provenance header.
2. A CI job fails the build if a header references a donor/commit pair absent from this ledger.
3. A CI job fails the build if a ledger entry references a `fehrest_path` that no longer exists.
4. `NOTICE` propagation for Apache-2.0 donors is verified mechanically.

Requirement 3 is what prevents the ledger from decaying into fiction as files move.

---

## 12. Research freeze

> **NOW BINDING AND TIGHTENED — see [§14.9](#149-research-freeze--now-binding).** F1-R2's [donor discovery addendum](#14-f1-r2-final-donor-discovery-addendum) is the **last planned broad discovery round**. `FEHREST BROAD DONOR DISCOVERY: FROZEN`. The clauses below remain the admission rule; §14.9 states the discipline that makes them enforceable — research becomes **question-driven, not collection-driven**.

The architecture discovery phase closes when [P Phase 0](../15-IMPLEMENTATION-PHASES.md) exits. After that, a new source may enter this registry **only** if it:

1. closes a documented gap in this registry; or
2. replaces a weaker existing candidate (with the comparison recorded); or
3. falsifies an existing architectural assumption; or
4. provides materially stronger evidence than an incumbent; or
5. is required for security or interoperability.

Each admission requires a registry entry, a named displaced or closed item, and an ADR if it changes a decision. CodeMirror 6 (SRC-003) is admitted under clause 2, displacing BlockSuite.

**Admissions in F1-R2**, each under a named clause:

| id | Source | Clause | Justification |
|---|---|---|---|
| SRC-100 | Apache Spark | **3** — falsifies an existing assumption | F1 asserted incremental-vs-rebuild equivalence with no mechanism that could test it; lineage-as-data supplies one ([R2-07](../reviews/F1-R2-RECONCILIATION.md)) |
| SRC-101 | Karpathy — LLM Wiki | **1** — closes a documented gap | The benchmark plan had no *maintained-knowledge-artifact* baseline, only RAG variants and a plain agent. That was the missing strong simple alternative |
| SRC-102 | GitHub Spec Kit | **1** — closes a documented gap | No specification-to-code binding existed; founder decision D-2 |
| SRC-103 | Ponytail | **1** — closes a documented gap | No implementation-minimisation discipline existed; founder decision D-3 |

None displaces an incumbent, because none had one. SRC-102 and SRC-103 are development tooling and change no runtime disposition.

---

## 13. Known registry gaps

Stated openly rather than discovered by a reviewer:

1. **Many `STUDY` entries are unpinned.** Acceptable — `STUDY` cannot produce code. Any transition to `ADAPT`/`USE` requires pinning first. Enforced by §11 CI rule 2.
2. **LongMemEval-V2 figures are not reproduced.** They are read from the paper. They must not become acceptance thresholds until re-run locally (E-14).
3. **Graphify's benchmark is self-authored.** Disclosed and treated as VENDOR-REPORTED (E-8).
4. **No license scan has been run on the transitive Python sidecar tree** (32 packages). Required before distribution; scheduled in [L](../11-SECURITY-VERIFICATION-PLAN.md).
5. **Docling's ML dependency weight is unmeasured.** Its optional-vs-required classification depends on that measurement.
6. **Tauri is not yet confirmed as the shell.** Listed `STUDY → likely USE`; a genuine ADR is owed at Phase 3 rather than an assumption inherited from the brief.
7. **No third-party replication exists for any retrieval claim in this registry.** Every comparative number is either vendor-reported or self-measured.
8. **SRC-101 (Karpathy — LLM Wiki) is unpinned.** Acceptable under gap 1's rule while it is `FOUNDATIONAL_STUDY` and no code is reused, but the **baseline harness must pin an exact gist revision before Phase T**, or baseline 5 is not reproducible and the comparison it supports is not admissible ([K §1 principle 6](../10-BENCHMARK-PLAN.md#1-principles)).
9. **SRC-102 and SRC-103 are unpinned and their licenses unverified.** Both are pinned and license-checked at Phase 0, before either is stood up. Ponytail's license in particular is unverified at the time of writing and must be confirmed before adoption.
10. **SRC-100 (Spark) is deliberately unpinned and must stay that way.** Concepts are read from published design documentation; a pin would imply a code relationship that does not exist and is not anticipated.
11. **Every source in [§14](#14-f1-r2-final-donor-discovery-addendum) is `PIN_PENDING_EXTERNAL_VERIFICATION`** — 29 entries covering 24 new projects, the remainder being restatements or promotions of existing entries. No live upstream verification was performed for them in the F1-R2 session, and **no commit was guessed**. None may transition to `ADAPT` or `USE` until pinned and license-verified; §11 CI rule 2 enforces this once implementation begins.
12. **Every license in §14 is `UNVERIFIED_IN_THIS_SESSION`**, recorded as stated by the project. Two require *per-repository* review rather than per-project: **any-sync / Anytype** (SRC-134 — do not infer uniform permissive licensing across `anyproto` components) and **AFFiNE** (SRC-121 — split license, per-file provenance required before vendoring).
13. **`OpenPencil` and `Flint` are now identified** ([§14.11](#1411-externally-verified-identifications-2026-08-18)) — `open-pencil/open-pencil` and `microsoft/flint-chart`, both with externally observed revisions from 2026-08-18. **Neither was verified in this environment**, and both remain `STUDY`-class gate candidates rather than adopted anything. *(This gap is closed as an identification; the verification gap in item 11 still applies.)*
14. **SRC-161 (MemOra), SRC-162 (EvoMemBench) and SRC-163 ("Total Recall at What Cost?") are named only.** Exact identifiers, versions and venues are unverified, and **no figure from any of them may be cited until they are**.

---

## 14. F1-R2 final donor discovery addendum

> **ADDED IN F1-R2, and this is the LAST planned broad donor-discovery round.** Every entry below closes a **documented gap** revealed by G2 or by the Rust-first founder decision (D-1). None was added for completeness. After this section, [§12 Research Freeze](#12-research-freeze) becomes binding in its stricter form (§14.9).
>
> ```
> THE DONOR REGISTRY IS EVIDENCE. IT IS NOT THE IMPLEMENTATION PLAN.
> ```
>
> **The presence of a source here authorizes nothing** — not dependency adoption, not code copying, not runtime integration, not porting, not feature implementation. Every future adoption still passes Spec Kit → Ponytail → rights/provenance → benchmark/security → implementation ([S](../19-ENGINEERING-METHOD.md)).

### 14.0 Pinning status for this addendum

**No exact commit in this section was verified in this session.** Live upstream verification was not performed for these sources, so **every entry is marked `PIN_PENDING_EXTERNAL_VERIFICATION` rather than carrying a guessed revision.** Fabricating a plausible-looking commit hash would be worse than having none: it would pass a reviewer's eye and fail at the moment it mattered.

Per the [pinning rule](#legend), no entry below may transition to `ADAPT` or `USE` until an exact revision is pinned and its license verified. §11 CI rule 2 enforces this mechanically once implementation begins.

**Licenses are recorded as stated by the projects and are `UNVERIFIED_IN_THIS_SESSION`.** Each requires confirmation at pin time, per source, before any code is imported.

#### Pin-verification semantics — two distinct labels

> **Added pre-GLM.** Six entries were **externally verified by GPT-5.6 Sol on 2026-08-18** and now carry observed revisions. **This environment still could not fetch them**, so the distinction is recorded rather than blurred:

| Label | Meaning |
|---|---|
| `EXTERNALLY_VERIFIED_BY_GPT_2026_08_18` | Repository identity, and where stated the license and revision, were observed by an external reviewer on that date. **Not verified here.** |
| `VERIFIED_IN_CLAUDE_ENVIRONMENT` | Observed directly in this session by a recorded command. Applies to the F1 measurements in [E-1](EVIDENCE_LOG.md#e-1--graphify-pinned-version-and-license)–[E-13](EVIDENCE_LOG.md#e-13--supporting-donors-and-standards-verified-live), **not** to anything in §14. |
| `PIN_PENDING_EXTERNAL_VERIFICATION` | Neither. Unchanged for every §14 entry not listed below. |

**An externally observed revision is a pin candidate, not a verified pin.** It is sufficient to remove the *"unidentified"* status and to give a reviewer something exact to check; it is **not** sufficient to authorise code import, which still requires the rights review in [§11](#11-code-provenance-ledger) against a revision confirmed in the build environment.

---

### 14.1 Rust platform and standard implementations

These close the gap opened by D-1: a Rust Core needs Rust answers to filesystem, Git, watching and protocol problems that F1 had specified only abstractly.

#### SRC-110 — gitoxide (`gix`)

```yaml
id: SRC-110
name: gitoxide / gix
class: [CODE_DONOR, ARCHITECTURE_DONOR, PLATFORM_REFERENCE]
repository_or_url: https://github.com/GitoxideLabs/gitoxide
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / BENCHMARK / LIKELY_SELECTIVE_USE
fehrest_layer: [KNOWLEDGE, DERIVED]
gap_closed: >
  G2-H6 / R2-09 and N section 3.11 require correct handling of Git operations on the
  vault -- checkout, switch, reset, merge, case-changing checkouts. F1 specified
  the BEHAVIOUR and never named a mechanism for reading repository state.
what_we_may_use:
  - Repository detection; refs; index; worktrees; status; diffs
  - Merge semantics inspection; ignore rules; attributes; pathspecs
  - Git object identity as a READ-ONLY input to reconciliation
what_we_will_not_use:
  - Git as Fehrest storage or as the event log (ADR-0001 already rejected this)
  - Any code path that makes Git MANDATORY. Fehrest must work for an ordinary
    non-Git local folder, and most vaults will be exactly that.
architectural_question_to_answer: >
  Should Fehrest read correctness-sensitive repository state through gix APIs
  rather than by parsing shell `git` output? Parsing porcelain output is a
  documented source of locale, version and encoding defects, and this is a
  correctness-sensitive path -- N section 3.11 treats a missed bulk change as
  indistinguishable from an index-suppression attack (T-16).
risks:
  - Large dependency surface for a capability that is optional to the product.
  - Ponytail question 3 applies first: how much of this is answered by a
    reconciliation scan that ignores Git entirely?
license: MIT OR Apache-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-111 — notify-rs

```yaml
id: SRC-111
name: notify
class: [CODE_DONOR, PLATFORM_REFERENCE]
repository_or_url: https://github.com/notify-rs/notify
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: LIKELY_IMPLEMENTATION_CANDIDATE -- SUBJECT TO PHASE 1/2 PROTOTYPE
fehrest_layer: DERIVED
gap_closed: >
  E section 6 and N section 3A require filesystem watching with debounce, storm
  escalation and hostile-environment tolerance, with no named mechanism.
what_we_may_use:
  - Cross-platform notification backends (Windows, macOS, Linux) and polling fallback
  - Debouncing ecosystem conventions
binding_invariant:
  - |
    FILESYSTEM WATCH EVENTS ARE HINTS. THEY ARE NOT CANONICAL TRUTH.

    Correct:   watch event -> schedule reconciliation -> scan + identity
               reconciliation -> canonical conclusion
    Forbidden: watch event -> blind canonical mutation

    This is already Fehrest's position (E section 6: "detected by hash comparison on
    a scan, not by trusting the watcher"), and adopting a watcher library must not
    quietly invert it. A watcher is a LATENCY OPTIMISATION; reconciliation is the
    CORRECTNESS MECHANISM.
evaluation_gate: >
  Must be evaluated against the hostile filesystem cases in N section 3A -- sharing
  violations, watcher storms, cloud placeholder files, sync-driven reverts.
license: CC0-1.0 / Artistic-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-112 — cap-std

```yaml
id: SRC-112
name: cap-std
class: [SECURITY_DONOR, CODE_DONOR, ARCHITECTURE_DONOR]
repository_or_url: https://github.com/bytecodealliance/cap-std
exact_commit_or_version: de1d389d726c9adf45fc0d7fc4066224ebf68212
pin_status: EXTERNALLY_VERIFIED_BY_GPT_2026_08_18   # NOT verified in this environment
date_verified: 2026-08-18 (external reviewer)
decision: STUDY / SECURITY_BENCHMARK / ADOPTION_CANDIDATE
fehrest_layer: SECURITY
status_note: >
  NOT marked as an accepted runtime dependency in F1-R2. GLM-5.3 evaluates whether
  this or another Rust-native capability strategy materially improves the boundary.
gap_closed: >
  T-7 and T-8 are currently defended by validation-plus-discipline inside core.
  ADR-0009 removes agent-supplied paths at the INTERFACE, which is strong; it does
  not reduce core's own AMBIENT filesystem authority.
architecture_to_study: |
  Wanted:    agent request -> Fehrest authorization -> vault capability
                           -> filesystem operation
  Not this:  agent request -> arbitrary PathBuf -> ambient filesystem authority
what_we_may_use:
  - Capability-oriented filesystem access; directory-rooted authority
  - Traversal-resistant filesystem APIs
  - Alignment with WASI/Wasmtime capability models (SRC-043), which keeps the
    deferred plugin-isolation seam coherent
boundary_discipline:
  - "A capability-oriented API is CONFINEMENT. It is not authorization (Cedar,
     SRC-113), not a process sandbox, and not prompt-injection resistance. These
     are four separate controls and Fehrest must not let one be cited as another."
license: Apache-2.0 WITH LLVM-exception / Apache-2.0 / MIT (UNVERIFIED_IN_THIS_SESSION)
security_note: >
  An externally observed revision is NOT evidence that the confinement model is
  sufficient for Fehrest. GLM-5.3 evaluates that independently.
evidence: []
```

#### SRC-113 — Cedar for Agents *(extends [SRC-042](#7-agent-protocol-authorization-isolation))*

```yaml
id: SRC-113
name: Cedar for Agents
class: [SECURITY_DONOR, CODE_DONOR, AUTHORIZATION_REFERENCE]
repository_or_url: https://github.com/cedar-policy/cedar-for-agents
also_retained: https://github.com/cedar-policy/cedar   # SRC-042
exact_commit_or_version: 84f030ab9ea3e6f0fff3e387250cffff3ebfb2f8
pin_status: EXTERNALLY_VERIFIED_BY_GPT_2026_08_18   # NOT verified in this environment
date_verified: 2026-08-18 (external reviewer)
decision: STUDY / ADAPT / STRONG_IMPLEMENTATION_CANDIDATE
fehrest_layer: SECURITY
gap_closed: >
  SRC-042 adopted Cedar's DECISION SHAPE and deferred the engine, on the argument
  that v1's policy space is small enough for a hand-written evaluator. Cedar for
  Agents is specifically about AGENT and MCP TOOL authorization, which is exactly
  Fehrest's chokepoint (G section 2). It is evidence that the deferral should be
  re-examined -- not evidence that it was wrong.
what_we_may_use:
  - principal + action + resource + context, already adopted as the shape
  - Schema generation and policy modelling around agent tool surfaces
  - Deny-by-default policy formulation
  - An explicit ALLOW / DENY / ASK layer -- ASK matters to Fehrest because
    F section 5.5 PENDING items and G section 3.2 approvals both need a third outcome
what_we_will_not_use:
  - Cedar as a SANDBOX. It answers "is this permitted?", never "can this process
    reach that file?"
boundary_discipline:
  - |
    authorization  !=  filesystem confinement  !=  process sandbox
                   !=  prompt-injection resistance
    Four controls. Fehrest maintains them explicitly and never cites one as another.
open_question: >
  Whether embedding a policy engine beats an auditable hand-written evaluator for
  v1's policy space. Decided at Phase 5, not here. Ponytail question 5 applies: an
  auditable 200-line evaluator may still be the right answer.
security_note: >
  UPSTREAM EXISTENCE IS NOT PROOF OF SECURITY. An externally verified repository and
  revision establish that the project is real and locatable -- nothing about whether
  its authorization model is correct for Fehrest, correctly configured, or free of
  bypasses. GLM-5.3 must review the authorization model INDEPENDENTLY, and the
  decision below remains NOT-YET-ACCEPTED.
license: Apache-2.0 (EXTERNALLY_OBSERVED_2026_08_18; not verified in this environment)
evidence: [E-13]
```

#### SRC-114 — Official MCP Rust SDK

```yaml
id: SRC-114
name: Model Context Protocol -- official Rust SDK
class: [STANDARD_IMPLEMENTATION, CODE_DONOR, INTEROPERABILITY_REFERENCE]
repository_or_url: https://github.com/modelcontextprotocol/rust-sdk
exact_commit_or_version: 38428f66bc679ad73ce3c4de729c90af64bc9aac
pin_status: EXTERNALLY_VERIFIED_BY_GPT_2026_08_18   # NOT verified in this environment
date_verified: 2026-08-18 (external reviewer)
decision: PREFERRED_IMPLEMENTATION_CANDIDATE
fehrest_layer: AGENT
gap_closed: >
  D-1 makes the Core Rust and G section 5 makes MCP-over-stdio a v1 transport. F1
  named the protocol (SRC-040) without naming an implementation, which under a Rust
  Core silently implied writing one.
architectural_direction: |
  Official MCP Rust SDK
        -> Fehrest MCP adapter
        -> Fehrest authorization + trust envelope   (G section 2, G section 4.1)
        -> Fehrest Core
what_we_may_use:
  - Native Rust MCP server; client where needed; tools; resources; protocol types;
    transport handling
what_we_will_not_use:
  - A proprietary Fehrest MCP protocol stack, UNLESS the official SDK fails a
    documented requirement. Ponytail question 4 applies directly.
unchanged_invariant:
  - "MCP IS A TRANSPORT, NOT AN AUTHORIZATION BOUNDARY (T-13). Adopting the official
     SDK changes the implementation and changes nothing about the boundary: the
     adapter sits BELOW Fehrest authorization in the diagram above, never beside it."
license: MIT (UNVERIFIED_IN_THIS_SESSION)
evidence: [E-7]
```

#### SRC-115 — CommonMark specification and Rust parsers

```yaml
id: SRC-115
name: CommonMark specification + Rust Markdown parsers
class: [STANDARD, CODE_DONOR, INTEROPERABILITY_REFERENCE]
standard: https://spec.commonmark.org/          # specification + conformance tests
candidates:
  - https://github.com/raphlinus/pulldown-cmark
  - https://github.com/kivikakk/comrak
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: USE_STANDARD / BENCHMARK_PARSERS
fehrest_layer: KNOWLEDGE
gap_closed: >
  D section 4.1 declares "CommonMark + GFM" canonical with the note "external spec"
  and names no parser and no conformance obligation. Under a Rust Core that is an
  unmade decision on the single most load-bearing format in the product.
binding_rule:
  - "FEHREST MARKDOWN SEMANTICS MUST BE SPECIFICATION-BACKED. Fehrest does not
     invent undocumented Markdown behaviour, and any deviation from CommonMark/GFM
     is documented in the format registry (I-5) or it is a defect."
evaluation_criteria:                            # by measurement, not popularity
  - CommonMark conformance against the official test suite
  - GFM requirements actually used by the corpus (tables, task lists, strikethrough)
  - Frontmatter coexistence -- must not consume or mangle YAML frontmatter
  - SOURCE OFFSETS -- required by D section 4.4 sidecar anchors and by the
    `link.line` provenance column in E section 4
  - AST shape adequate for link extraction and heading-path anchors
  - Incremental parsing needs, if any
  - Malformed and hostile input behaviour (C-MALFORMED, T-17)
  - Performance at the O section 4.2 incremental budget
  - Round-trip / source preservation -- R-8, and the Editor Gate's test 18
    (a one-word change must produce a minimal reviewable diff)
what_we_will_not_use:
  - Popularity as a selection criterion
license: CommonMark spec CC-BY-SA; parsers MIT / BSD-2-Clause (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-116 — Tantivy *(same source as [SRC-014](#4-storage-and-retrieval); this entry adds the R2 trigger)*

```yaml
id: SRC-116
name: Tantivy
class: [CODE_DONOR, SEARCH_REFERENCE, BENCHMARK_CANDIDATE]
repository_or_url: https://github.com/quickwit-oss/tantivy
decision: BENCHMARK / DEFER
status: >
  SQLITE FTS5 REMAINS THE DEFAULT FEHREST CORE HYPOTHESIS. Unchanged by D-1.
becomes_relevant_only_if:                       # a documented FAILURE, not a preference
  - "B-12 shows FTS5 ranking is unstable across rebuild histories and no FTS5
     configuration fixes it (F-18)"
  - "B-9 equivalence cannot be achieved with FTS5"
  - "Large-vault latency misses the O section 5 budgets"
  - "Indexing throughput misses the O section 4 budgets"
  - "Language/tokenisation capability proves genuinely insufficient for the corpus"
ponytail_note:
  - "DO NOT introduce Tantivy simply because it is Rust-native. Ponytail requires
     SQLite FTS5 to FAIL A DOCUMENTED REQUIREMENT FIRST. 'Written in our language'
     is not a requirement; it is a preference wearing one's clothes."
license: MIT
evidence: [E-12]
```

---

### 14.2 Visual, canvas and editing surfaces

These feed two gates: the existing [Editor Gate](../18-EDITOR-GATE.md) and the new **Visual/Canvas Engine Gate** ([T §2](../20-FUTURE-GATES.md#2-visualcanvas-engine-gate)).

#### SRC-120 — Penpot

```yaml
id: SRC-120
name: Penpot
class: [CODE_DONOR, ARCHITECTURE_DONOR, INTEROPERABILITY_REFERENCE, PRODUCT_REFERENCE]
repository_or_url: https://github.com/penpot/penpot
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / BENCHMARK / SELECTIVE_ADAPT
fehrest_layer: UI
gate: Visual/Canvas Engine Gate (T section 2) -- Phase 8+, not v1
what_we_study:
  - Open-standard visual document architecture
  - SVG / CSS / HTML / JSON interoperability
  - Visual object and scene semantics
  - Design tokens; components and variants
  - Layout / grid / flex behaviour
  - Plugin architecture; API architecture; MCP integration
  - Inspect / design-to-code workflow
  - Collaboration correctness
  - Large-canvas performance and mutation handling
  - Security lessons from a mature collaborative editor
what_we_will_not_do:
  - Adopt the Penpot server or runtime wholesale
  - Turn Fehrest into a Figma clone. Fehrest is not a design tool; a canvas is one
    projection over the object model (A section 5), never the product
  - Add server infrastructure because Penpot uses it. Penpot is a hosted
    collaborative application; Fehrest is local-first with ZERO MANDATORY SERVICES
    (I-2, I-3). Their infrastructure follows from a requirement Fehrest does not have.
most_transferable_lesson: >
  Open-standard visual interchange (SVG/JSON) as the canonical artifact rather than
  a proprietary scene format -- the visual-surface form of I-5.
license: MPL-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-121 — AFFiNE / BlockSuite, extended scope *(extends [SRC-004](#31-blocksuite--candidate-b-in-the-editor-gate), [SRC-006](#33-affine--study--source-of-candidate-b))*

```yaml
id: SRC-121
name: AFFiNE / BlockSuite -- extended scope
class: [CODE_DONOR, ARCHITECTURE_DONOR, PRODUCT_REFERENCE, LOCAL_FIRST_REFERENCE]
repository_or_url: https://github.com/toeverything/AFFiNE
exact_commit_or_version: see SRC-006 (canary b4c8548c, 2026-08-17); PIN AT PHASE 3E
decision: STUDY / BENCHMARK / SELECTIVE_ADAPT
maintenance_status_restated:                    # R1-02, reaffirmed in F1-R2
  - |
    THE STANDALONE HISTORICAL BlockSuite REPOSITORY DOES NOT REPRESENT THE
    MAINTENANCE STATUS OF THE IMPLEMENTATION.

    The maintained AFFiNE monorepo contains:
        blocksuite/affine
        blocksuite/framework
        blocksuite/integration-test
        blocksuite/playground
    and related BlockSuite code.

    F1 measured the mirror and concluded the editor was dead. That error is
    corrected and stays corrected (E-10.1).
relevant_to:
  - Local-first knowledge workspace architecture
  - Docs + edgeless canvas integration; page <-> canvas transitions
  - Block / object model; linked pages
  - Database / multi-view blocks
  - Journals; local-first persistence; collaboration
  - Import / export; rich object editing
gates:
  - "Text Editor Gate: FIRST-CLASS CANDIDATE (Candidate B, 18-EDITOR-GATE)"
  - "Visual/Canvas Engine Gate: BlockSuite Edgeless is a candidate (T section 2)"
  - "Unified Surface Test: the primary evidence FOR a shared substrate (T section 3)"
unresolved_issue:                               # unchanged from SRC-004 / SRC-006
  - Split license -- MIT applies outside packages/backend and packages/common/native.
    Per-file provenance required before any vendoring.
  - 446 MB monorepo; extraction cost and coupling depth unmeasured.
  - No independent release channel for the editor subtree.
independence_invariant:
  - "THE CANONICAL FEHREST CORE REMAINS RUST-OWNED AND INDEPENDENT of AFFiNE,
     BlockSuite, Electron, and any cloud/server runtime. Whatever wins the Editor
     Gate is a SURFACE over the Core (I-16), never the Core."
license: Split -- MIT outside packages/backend and packages/common/native
evidence: [E-10, E-10.1]
```

#### SRC-122 — OctoBase and y-octo

```yaml
id: SRC-122
name: OctoBase / y-octo
class: [ARCHITECTURE_DONOR, CODE_DONOR]
repository_or_url:
  - https://github.com/toeverything/OctoBase
  - https://github.com/toeverything/y-octo
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / DEFER
fehrest_layer: KNOWLEDGE
studied_separately_from_affine: true             # deliberately -- these are Rust upstreams
relevance:
  - Rust local-first storage
  - CRDT engine architecture
  - Collaborative persistence
  - Native/web synchronisation boundaries
  - Thread-safe Yjs-compatible semantics
hard_constraint:
  - |
    DO NOT INTRODUCE CRDT OR COLLABORATION INTO THE THESIS-PROOF MVP.
    Yjs / y-octo / OctoBase remain CONDITIONAL until a collaboration or editor
    requirement EMPIRICALLY requires them (ADR-0012). Collaboration must never be
    added to the MVP in order to justify a CRDT (R1-09) -- and now, equally, a
    Rust-native CRDT must not be adopted merely because it is Rust-native.
gate: Collaboration/CRDT Gate (T section 4)
license: verify per repository at pin time (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

---

### 14.3 Local-first and CRDT candidates

All feed the **Collaboration/CRDT Gate** ([T §4](../20-FUTURE-GATES.md#4-collaborationcrdt-gate)). **No CRDT is authorized for the Headless Thesis-Proof.**

| id | Source | Class | Decision | What Fehrest studies | Explicitly not taken |
|---|---|---|---|---|---|
| SRC-130 | **Loro** — `loro-dev/loro` | CODE_DONOR / ARCHITECTURE_DONOR / LOCAL_FIRST_REFERENCE | **STUDY / BENCHMARK / DEFER** | Rust-native collaborative structures; text and rich text; map/list/tree state; version and history inspection; sync; local-first operation | Adoption on the grounds of being Rust-native. Collaboration introduced because a donor supports it |
| SRC-131 | **Automerge** — `automerge/automerge` *(extends [SRC-007](#34-automerge--study))* | ARCHITECTURE_DONOR / CODE_DONOR / LOCAL_FIRST_REFERENCE | **STUDY / BENCHMARK / DEFER** | Local-first document semantics; sync protocol; durable collaborative state; version/history concepts; Rust implementation lessons | **No automatic preference.** F1 listed Automerge alone; R2 makes it one candidate among four |
| SRC-132 | **Yrs / Yjs** *(see [SRC-005](#32-yjs--conditional--editor-dependent))* | CODE_DONOR / RESEARCH | **CONDITIONAL — editor-dependent** | Reference semantics; arrives with Candidate B if it wins the Editor Gate | Adoption independent of the Editor Gate |
| SRC-133 | **AppFlowy-Collab** — `AppFlowy-IO/AppFlowy-Collab`<br>**License: `AGPL-3.0`** *(externally observed 2026-08-18)*<br>Revision `be5aa89b4aeafd4e7159e92b86784c02caaa85ce` | CODE_DONOR / ARCHITECTURE_DONOR / LOCAL_FIRST_REFERENCE / PRODUCT_REFERENCE | **STUDY / SELECTIVE_ADAPT / DEFER** *(posture unchanged)* | A Rust collaborative substrate shared across **document, database and folder/workspace** object types; persistence plugins; history; import/export; Yrs integration | **CODE REUSE: RIGHTS / PROVENANCE REVIEW REQUIRED.** AGPL-3.0 is a copyleft licence whose obligations differ materially from the permissive licences elsewhere in this registry. **Do not infer permissive reuse from the project being open source.** Architecture study is unaffected |
| SRC-134 | **any-sync / Anytype** — `anyproto/any-sync` | ARCHITECTURE_DONOR / LOCAL_FIRST_REFERENCE / P2P_REFERENCE / PRODUCT_REFERENCE | **STUDY** | Local-first object architecture; P2P sync; encrypted collaboration; offline-first knowledge workspace; object-oriented knowledge UX | **Licenses must be treated PER REPOSITORY.** Do not infer that all Anytype code is permissively licensed because some anyproto components are. Source-specific rights review before any reuse |
| SRC-135 | **iroh** — `n0-computer/iroh` | ARCHITECTURE_DONOR / CODE_DONOR / P2P_REFERENCE | **STUDY / DEFER** | Rust P2P networking; content-addressed transfer; QUIC; NAT traversal; gossip; local-first device sync | Any sync infrastructure before the core thesis passes. **Fehrest v1 remains local and single-device capable** ([I-7](../01-ARCHITECTURE-CONSTITUTION.md#i-7--sync-is-optional)) |

**All pins `PIN_PENDING_EXTERNAL_VERIFICATION`; all licenses `UNVERIFIED_IN_THIS_SESSION`.**

**SRC-133 is the most decision-relevant entry in this table, and not for its CRDT.** AppFlowy-Collab is direct evidence about whether **one shared collaborative substrate across several object types** is maintainable in practice — which is the [Unified Surface Test](../20-FUTURE-GATES.md#3-unified-surface-test) question, and the practical form of Fehrest's own *"Everything is an Object; views are projections"* ([D §1](../03-CANONICAL-DATA-MODEL.md#1-the-object-model-decision)).

> **AppFlowy-Collab's licence changes what may be taken from it, and only that** *(corrected pre-GLM)*. Its repository licence was externally observed as **AGPL-3.0** on 2026-08-18. F1-R2 recorded "exact license/provenance review required" generically; the specific fact matters, because AGPL-3.0 is **copyleft**, not permissive, and every other code-donor licence in this registry is MIT, Apache-2.0, MPL-2.0 or public domain.
>
> **What is unaffected:** reading the design, and reasoning about whether a shared substrate is maintainable. Studying an architecture is not reuse.
> **What is gated:** any code import whatsoever. `CODE REUSE: RIGHTS / PROVENANCE REVIEW REQUIRED`, and that review must reach a founder-level licensing decision rather than an engineering one, since Fehrest's own licence is still open ([Q-1a](../16-OPEN-QUESTIONS.md#q-1--repository-identity-closed)).
> **What must not be inferred:** that open source implies permissive reuse. That inference is how a copyleft obligation enters a codebase unnoticed.
>
> The `STUDY / SELECTIVE_ADAPT / DEFER` posture is **unchanged** — this correction records a constraint on a future action, not a new decision.

---

### 14.4 Temporal, history and lineage

#### SRC-140 — Jujutsu

```yaml
id: SRC-140
name: Jujutsu (jj)
class: [ARCHITECTURE_DONOR, CODE_DONOR, PRODUCT_REFERENCE]
repository_or_url: https://github.com/jj-vcs/jj
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / SELECTIVE_ADAPT
fehrest_layer: EVENT
gap_closed: >
  N section 3 specifies recovery from FAILURES. It does not specify durable
  user-visible UNDO, nor how a user asks "how did the system reach this state?" --
  and D section 5.3 causation exists precisely to make audit narratable, with no
  model of what a user does with that narrative.
what_we_study:
  - Operation-log concepts as distinct from content history
  - Historical state inspection
  - Undo semantics that survive restart
  - Concurrent operation handling
  - Git coexistence
principle_to_study:
  - |
    CONFLICT != CORRUPTION

    A conflict may be VALID REPRESENTABLE STATE that stays visible until resolved.
    Fehrest already holds this position in three places, and arrived at it
    independently each time:
      - F section 3.3: CONFLICTED is a first-class resting state, not an error
      - D section 3.2: duplicate IDs are retained and surfaced, never silently resolved
      - N section 3.10: concurrent edits present both versions rather than merging
    Jujutsu is prior art for making that representable rather than exceptional, and
    is worth studying for how a system STORES a conflict, not how it reports one.
what_we_will_not_do:
  - Use Jujutsu as Fehrest storage
  - Require jj to operate Fehrest
  - Turn Fehrest into a VCS
  - Copy Git/Jujutsu semantics into MEMORY without validating domain fit. A memory
    conflict and a text merge conflict are not the same object - F section 4.2
    resolves by evidence, not by three-way merge.
license: Apache-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-141 — OpenLineage

```yaml
id: SRC-141
name: OpenLineage
class: [STANDARD_REFERENCE, ARCHITECTURE_DONOR, LINEAGE_REFERENCE]
repository_or_url: https://github.com/OpenLineage/OpenLineage
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY
fehrest_layer: EVENT
what_we_study:
  - The separation - Run / Job / Dataset / Event / Facets
  - Possible mapping onto Fehrest Agent Experience -
        Session / Task / Tool invocation / Artifact / Event / Metadata facets
  - "EXTENSIBLE FACETS AS AN ALTERNATIVE TO AN EVER-GROWING MONOLITHIC EVENT SCHEMA"
why_this_matters_now: >
  D section 5.2 vocabulary is already 20+ event types across three tiers, R2-12
  leaves the tiering unfrozen pending B-0, and M section 5 forbids ever removing an
  event type. A facet model is the alternative to a schema that can only grow, and
  it interacts directly with the ADR-0015 unbounded-upcaster-chain concern.
what_we_will_not_use:
  - OpenLineage runtime dependencies
  - Data-pipeline terminology imported into a human knowledge product without
    checking that the concepts transfer
license: Apache-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-142 — in-toto attestations

```yaml
id: SRC-142
name: in-toto attestation framework
class: [STANDARD_REFERENCE, SECURITY_REFERENCE, PROVENANCE_REFERENCE]
repository_or_url: https://github.com/in-toto/attestation
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / SELECTIVE_ADAPT
fehrest_layer: [SECURITY, MEMORY]
what_we_study:
  - Authenticated claims; subject digests; typed predicates
  - Actor/tool evidence; cryptographically verifiable provenance concepts
possible_future_shape:
  - "subject / claim / actor / evidence hashes / optional signature - as an eventual
     extension of the Fehrest provenance envelope and the served-item manifest
     (H section 3.2), both of which already carry subject identity, actor and content
     hashes and lack only the attestation framing"
what_we_will_not_do:
  - "Impose software-supply-chain terminology blindly on human knowledge and memory.
     A memory is an ASSERTION BY AN ACTOR (F section 2), not a build artifact, and the
     analogy fails at the point where a build is reproducible and a human judgement
     is not. Adopt only the transferable provenance PROPERTIES."
relationship_to_t4:
  - "T-4 states plainly that Fehrest provides TAMPER-EVIDENCE, not tamper-resistance,
     because key material would live on the same machine. Signatures do not change
     that for a local single-user system; they would matter for a future multi-device
     or shared-vault case."
license: Apache-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

#### SRC-143 — DoltLite

```yaml
id: SRC-143
name: DoltLite
class: [ARCHITECTURE_DONOR, VERSIONING_REFERENCE]
repository_or_url: https://github.com/dolthub/doltlite
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / DEFER
fehrest_layer: DERIVED
what_we_study:
  - Content-addressed structured storage
  - Branching structured state; historical queries; merge/versioning semantics
what_we_will_not_do:
  - "Make the Fehrest SQLite store a Git-like database. ADR-0006 confines SQLite to
     DERIVED state precisely so that its corruption is an availability problem;
     versioning a derived store would be versioning something that is rebuilt by
     definition."
license: Apache-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

---

### 14.5 Retrieval, graph and semantic interoperability

| id | Source | Class | Decision | Gate / trigger | Explicitly not taken |
|---|---|---|---|---|---|
| SRC-150 | **petgraph** — `petgraph/petgraph` | CODE_DONOR / GRAPH_REFERENCE | **BENCHMARK / DEFER** | **Only if the Graph Intelligence capability gate passes** ([B-13 GI-CAP](../10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment)) | Selection before Graph Intelligence earns inclusion. Premature Graphify porting — [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) still forbids it |
| SRC-151 | **Oxigraph** — `oxigraph/oxigraph` | INTEROPERABILITY_REFERENCE / CODE_DONOR / SEMANTIC_WEB_REFERENCE | **STUDY / DEFER** | Future RDF / SPARQL / JSON-LD export and import | **RDF as the canonical internal model.** [SRC-060](#8-research-canon) already takes W3C PROV vocabulary while refusing to become an RDF system; this entry does not reopen that |
| SRC-152 | **Salsa** — `salsa-rs/salsa` | ARCHITECTURE_DONOR / RUST_INCREMENTAL_COMPUTATION_REFERENCE | **STUDY / DEFER** | Lessons for parsing, link extraction, FTS and graph projections | **Salsa as a v1 runtime dependency** — see the note below |

**All pins `PIN_PENDING_EXTERNAL_VERIFICATION`; all licenses `UNVERIFIED_IN_THIS_SESSION`.**

**On petgraph — the possible future separation:**

```
Graphify       ->  extraction / donor capability        (Python, optional, gated)
Fehrest Rust   ->  graph representation and traversal   (if native suffices)
```

That split is only worth evaluating **after** GI-CAP retains the capability. Choosing a graph library for a capability that has not earned inclusion is work spent on a hypothesis.

**On Salsa — the temptation this entry exists to name.** Its model (canonical inputs → derived queries → memoized outputs → selective invalidation) is a **superset** of what [R2-07](../reviews/F1-R2-RECONCILIATION.md) actually validated, which is the much smaller:

```
derivation manifest  +  incremental == full-rebuild property testing
```

**Do not replace a static dependency manifest with a generic incremental-computation framework** unless measured complexity requires it. The manifest is four fields ([E §10](../04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data)); a framework is an architecture. Ponytail question 5 applies with unusual force here, precisely because the framework is genuinely elegant and would be genuinely easy to justify after the fact.

---

### 14.6 Memory research and benchmarks

| id | Source | Class | Decision | What Fehrest takes | Discipline |
|---|---|---|---|---|---|
| SRC-160 | **Hindsight** — `vectorize-io/hindsight` | RESEARCH / ARCHITECTURE_DONOR / BENCHMARK_REFERENCE / MEMORY_REFERENCE | **STUDY / BENCHMARK** | World knowledge vs agent experience; entity/state summaries; evolving beliefs; **retain / recall / reflect** lifecycle; structured memory beyond vector snippets | Benchmark claims are **`UPSTREAM_CLAIM`** until independently validated — the same rule that governs [E-8](EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks) and [E-14](EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target) |
| SRC-161 | **MemOra** | BENCHMARK / RESEARCH | **BENCHMARK** | Memory updates; invalid and obsolete memory; forgetting; avoiding influence from superseded state | Tests the Fehrest question directly: **can it avoid using a memory that was once true and no longer is?** — [B-4](../10-BENCHMARK-PLAN.md#b-4--temporal-and-supersession-correctness)'s stale-memory metric, sourced externally rather than self-authored |
| SRC-162 | **EvoMemBench** | BENCHMARK / RESEARCH | **BENCHMARK** | Episodic vs cross-episode memory; knowledge vs execution experience; comparison against long-context strategies | Used deliberately as **contrary evidence** against assuming one memory strategy wins every workload |
| SRC-163 | **"Total Recall at What Cost?"** | RESEARCH / BENCHMARK_REFERENCE | **STUDY** | Memory systems must be compared on **more than accuracy** | Expands evaluation to correctness **plus** context tokens, latency, CPU, disk growth, model-call count and provider cost ([K §5](../10-BENCHMARK-PLAN.md#5-harness-requirements)) |
| SRC-062 | **AgentDojo** *(existing entry, scope extended)* | SECURITY_BENCHMARK / RESEARCH / ATTACK_REFERENCE | **STUDY / BENCHMARK** | Indirect prompt injection; malicious tool content; adversarial retrieved evidence; agent manipulation | Extended with **Fehrest-specific attack classes** — [L §6](../11-SECURITY-VERIFICATION-PLAN.md#6-adversarial-corpora) |

**SRC-161, SRC-162 and SRC-163 are identified by name in the founder addendum only.** Exact identifiers, versions and venues are `PIN_PENDING_EXTERNAL_VERIFICATION`, and **no figure from any of them may be cited in this package until verified.**

**A standing rule for this table, and it has already cost this project once:** benchmark conclusions are not copied without checking methodology. [E-8](EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks) is the worked example — a 76% vs 76% "result" at n=50 whose 95% interval is roughly ±12 points, which means it distinguishes nothing.

---

### 14.7 Data, analytics and view engines

#### SRC-170 — Apache Superset

```yaml
id: SRC-170
name: Apache Superset
class: [ARCHITECTURE_DONOR, CODE_DONOR, PRODUCT_REFERENCE, ANALYTICS_REFERENCE]
repository_or_url: https://github.com/apache/superset
exact_commit_or_version: PIN_PENDING_EXTERNAL_VERIFICATION
date_verified: not verified in this session
decision: STUDY / DEFER / SELECTIVE_ADAPT
fehrest_layer: UI                          # a future View Engine, not v1
supersedes_entry: SRC-080                  # promotes a one-line reference to a full record
what_we_study:
  - Separation of SEMANTIC DATA DEFINITIONS from VISUAL PRESENTATION
  - Reusable metrics and dimensions; dataset abstraction
  - Chart/view PLUGIN ARCHITECTURE, including the separate chart plugin packages,
    as a donor for a future Fehrest View Engine
  - Dashboard composition; SQL and data exploration UX
  - Caching concepts; programmatic API boundaries
  - Permission-aware analytics; broad data-source abstraction
future_fehrest_principle_it_supports:
  - |
    CANONICAL OBJECTS  !=  VIEWS

    A dashboard, chart, table or timeline is a PROJECTION over canonical or derived
    data, never the canonical knowledge itself. This is the D section 1 position
    (views are projections) extended to the analytics surface, and it is why an
    analytics layer can be added later without touching a canonical record.
distinguished_from_data_formulator:        # SRC-079 - different problems, both deferred
  - "Data Formulator: AGENTIC EXPLORATORY analysis - branching investigations, Data Threads"
  - "Superset: DURABLE SEMANTIC analytics - reusable metrics/dimensions, charts, dashboards"
what_we_will_not_do:
  - Superset as a Fehrest runtime dependency
  - Introduce Python because of Superset (I-17 forbids it being required at all)
  - Introduce Redis / Celery / server infrastructure
  - Introduce a mandatory database server
  - Introduce DuckDB into the MVP because analytics products use it
  - Build dashboards before the Headless Rust Thesis-Proof passes
  - Create a plugin marketplace in v1
constraints_any_future_analytics_layer_must_preserve:
  - ZERO MANDATORY SERVICES
  - LOCAL-FIRST
  - RUST-OWNED CORE
  - OPEN DATA
  - REBUILDABLE DERIVED VIEWS
deferred_until: >
  A MEASURED user or product requirement justifies a Data/Analytics layer. Not a
  founder intuition, and not because the architecture would accommodate it.
license: Apache-2.0 (UNVERIFIED_IN_THIS_SESSION)
evidence: []
```

**The two previously unidentified names are now identified** — see [§14.11](#1411-externally-verified-identifications-2026-08-18). `OpenPencil` is `open-pencil/open-pencil` and `Flint` is `microsoft/flint-chart`, both with revisions externally observed on 2026-08-18. Neither was verified in this environment, and neither is adopted.

---

### 14.8 JSON Canvas — visual interchange *(promotes [SRC-071](#9-product-references))*

```yaml
id: SRC-171
name: JSON Canvas
class: [STANDARD, INTEROPERABILITY_REFERENCE, PRODUCT_REFERENCE]
repository_or_url: https://github.com/obsidianmd/jsoncanvas
exact_commit_or_version: PIN AT PHASE 8    # SRC-071 verified MIT and active at E-13
decision: ADOPT_AS_VISUAL_INTERCHANGE_CANDIDATE
fehrest_layer: KNOWLEDGE
role: >
  The open interoperability baseline for visual and canvas documents. EVEN IF
  another engine wins the Visual/Canvas Engine Gate - Penpot, AFFiNE Edgeless,
  tldraw, Excalidraw or an unidentified candidate - Fehrest preserves an open
  portable representation wherever the format can express the required semantics.
  This is I-5 applied to the visual surface: the ENGINE is replaceable, the
  CANONICAL FORMAT must stay open and specified.
honest_limit:
  - "DO NOT force all advanced visual semantics into JSON Canvas if doing so would
     DESTROY INFORMATION. Lossy canonicalisation is worse than an honest sidecar."
  - "If richer semantics are later required, document extension and sidecar rules
     under the D section 4.4 sidecar discipline: the sidecar carries references and
     metadata, never content, and deleting it loses annotations rather than the
     document."
license: MIT
evidence: [E-13]
```

---

### 14.9 Research freeze — now binding

```
FEHREST BROAD DONOR DISCOVERY:  FROZEN
```

**This addendum is the last planned broad discovery round.** From here a new source may be admitted **only** through a documented gap trigger — [§12](#12-research-freeze), tightened:

| # | Admission trigger |
|---|---|
| 1 | Closes a documented architectural, security or product gap |
| 2 | Materially replaces a weaker existing candidate, with the comparison recorded |
| 3 | Falsifies an existing assumption |
| 4 | Supplies missing primary evidence, a standard, or a benchmark |
| 5 | Is required to address a validated security or recovery problem |

**Research becomes question-driven, not collection-driven.**

| Acceptable future research | Unacceptable |
|---|---|
| *"FTS5 failed B-12; benchmark Tantivy."* | *"Search for 100 more knowledge apps."* |
| *"GLM-5.3 found a path-confinement weakness; evaluate cap-std."* | *"Add another framework because it looks interesting."* |
| *"GI-CAP passed; investigate the minimum Rust graph runtime."* | *"Copy a subsystem before its requirement exists."* |
| *"Collaboration became a ratified requirement; execute the CRDT Gate."* | *"Add a donor because a competitor uses it."* |

**This does not mean Fehrest stops learning.** It means every future source arrives attached to a question that already exists.

**Ponytail applies to the registry itself:** prefer fewer proven dependencies and smaller interfaces. A registry entry is not a plan, and a long candidate list is not thoroughness — it is deferred decision-making with better formatting.

---

### 14.10 What this addendum did NOT change

Stated explicitly, because a large donor round is exactly where scope creep enters disguised as diligence:

| Unchanged | Still true after §14 |
|---|---|
| **First future build** | [Phase T — Headless Rust Thesis-Proof](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice). No donor in this section moves into it |
| **Runtime dependency set** | **Zero donors were adopted as runtime dependencies by this round.** Every entry is STUDY, BENCHMARK, DEFER, or a CANDIDATE pending a gate |
| **The v1 scope exclusions** | UI, canvas, editor, CRDT, sync, production graph sidecar, vectors, automatic promotion, analytics, dashboards, plugins, cloud, mobile — all still excluded ([A §9](../00-PRODUCT-THESIS.md#9-scope-commitments)) |
| **Constitutional invariants** | None amended. I-16 and I-17 in particular bound every UI-adjacent and Python-adjacent entry above |
| **The Core** | **Rust-owned, and independent of AFFiNE, BlockSuite, Electron, Penpot, Superset, and any cloud or server runtime** |

---

### 14.11 Externally verified identifications (2026-08-18)

> **ADDED PRE-GLM.** Six entries were verified by an external reviewer on 2026-08-18 and now carry exact repository identities and observed revisions. **This environment could not fetch any of them**, so every entry below is `EXTERNALLY_VERIFIED_BY_GPT_2026_08_18` and **not** `VERIFIED_IN_CLAUDE_ENVIRONMENT` (§14.0). **No decision, disposition or posture changed.**

| Source | Repository | Observed revision | License | Status |
|---|---|---|---|---|
| **OpenPencil** | `open-pencil/open-pencil` | `15bd0ba19f02d0e889068817c0888640e2d4fa04` | not observed | **STUDY / BENCHMARK / ADAPT** — Visual/Canvas Engine Gate candidate |
| **Microsoft Flint** | `microsoft/flint-chart` | `34ef4516554b323a740a426bd1a1e6ba31ee8245` | MIT *(GitHub metadata)* | **STUDY / DEFER** — future visualization/data donor only |
| **Cedar for Agents** ([SRC-113](#src-113--cedar-for-agents-extends-src-042)) | `cedar-policy/cedar-for-agents` | `84f030ab9ea3e6f0fff3e387250cffff3ebfb2f8` | Apache-2.0 | **SECURITY DONOR / STRONG IMPLEMENTATION CANDIDATE / NOT YET ACCEPTED** |
| **cap-std** ([SRC-112](#src-112--cap-std)) | `bytecodealliance/cap-std` | `de1d389d726c9adf45fc0d7fc4066224ebf68212` | not re-observed | **SECURITY DONOR / ADOPTION CANDIDATE / NOT ACCEPTED YET** |
| **Official MCP Rust SDK** ([SRC-114](#src-114--official-mcp-rust-sdk)) | `modelcontextprotocol/rust-sdk` | `38428f66bc679ad73ce3c4de729c90af64bc9aac` | not re-observed | **PREFERRED PROTOCOL IMPLEMENTATION CANDIDATE** |
| **AppFlowy-Collab** ([SRC-133](#143-local-first-and-crdt-candidates)) | `AppFlowy-IO/AppFlowy-Collab` | `be5aa89b4aeafd4e7159e92b86784c02caaa85ce` | **AGPL-3.0** | **STUDY / SELECTIVE_ADAPT / DEFER** — code reuse gated on rights review |

#### SRC-180 — OpenPencil

```yaml
id: SRC-180
name: OpenPencil
class: [CODE_DONOR, PRODUCT_REFERENCE, INTEROPERABILITY_REFERENCE]
repository_or_url: https://github.com/open-pencil/open-pencil
exact_commit_or_version: 15bd0ba19f02d0e889068817c0888640e2d4fa04
pin_status: EXTERNALLY_VERIFIED_BY_GPT_2026_08_18   # NOT verified in this environment
date_verified: 2026-08-18 (external reviewer)
decision: STUDY / BENCHMARK / ADAPT
fehrest_layer: UI
gate: Visual/Canvas Engine Gate (T section 2) -- Phase 8+, not v1
status_correction: >
  F1-R2 recorded this name as unidentified and therefore not a gate candidate.
  It is now identified and IS a candidate in the Visual/Canvas Engine Gate. It is
  NOT promoted to a runtime dependency, and nothing about canvas being deferred
  changes.
what_we_will_not_do:
  - Treat identification as adoption. A gate candidate is a question, not a choice.
  - Un-defer canvas. A section 8+ candidate does not move a section 8+ feature.
license: not observed -- MUST be established before any code import
evidence: []
```

#### SRC-181 — Microsoft Flint

```yaml
id: SRC-181
name: Microsoft Flint (flint-chart)
class: [ARCHITECTURE_DONOR, PRODUCT_REFERENCE, ANALYTICS_REFERENCE]
repository_or_url: https://github.com/microsoft/flint-chart
exact_commit_or_version: 34ef4516554b323a740a426bd1a1e6ba31ee8245
pin_status: EXTERNALLY_VERIFIED_BY_GPT_2026_08_18   # NOT verified in this environment
date_verified: 2026-08-18 (external reviewer)
decision: STUDY / DEFER
fehrest_layer: UI                          # a future View Engine, not v1
category: >
  Visualization language / chart specification system with agent-oriented usage.
why_it_is_interesting_to_fehrest: >
  A DECLARATIVE CHART SPECIFICATION is a projection description, not a projection.
  That is the same shape as the View Engine Gate principle -- canonical objects
  are not views (T section 5) -- and an agent-oriented specification language is
  directly relevant to a product whose primary non-human user is an agent.
what_we_will_not_do:
  - Adopt it, or any charting system, before a MEASURED analytics requirement
    exists (T section 5). Identification does not open the View Engine Gate.
  - Introduce a visualization dependency into the Headless Thesis-Proof.
license: MIT (GitHub metadata, externally observed 2026-08-18; confirm at pin time)
evidence: []
```

**What this subsection did not do.** It closed an identification gap and nothing else. No disposition moved, no gate opened, no candidate was promoted, and **no source here is a runtime dependency**. The [research freeze](#149-research-freeze--now-binding) remains active: these two entries were already in the registry as named-but-unidentified, so identifying them admits no new source.
