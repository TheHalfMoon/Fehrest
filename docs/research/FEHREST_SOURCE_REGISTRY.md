# Fehrest Source Registry

**Status:** CANONICAL RESEARCH REGISTRY
**Date verified:** 2026-08-17
**Purpose:** An auditable record of every external codebase, paper, standard, benchmark and product reference materially considered for Fehrest.

Fehrest must never become an untraceable amalgamation of external implementations. Every material external source is attributable to an exact upstream, and every source from which code may be reused carries an exact pinned commit or version.

**Authority note:** This registry is *evidence*, not authority. Where it conflicts with live repository truth, live truth wins. All measurements backing dispositions live in [EVIDENCE_LOG.md](EVIDENCE_LOG.md); registry entries cite them as `E-n`.

**Pinning rule:** `exact_commit_or_version` must be pinned before any code is copied or adapted. A moving branch (`main`, `master`, `canary`, `v8`) is **not** sufficient provenance for implementation. Two primary donors are pinned to commits below precisely because their default branches move.

---

## Legend

**Classes:** `CODE_DONOR` · `ARCHITECTURE_DONOR` · `PRODUCT_REFERENCE` · `RESEARCH` · `STANDARD` · `BENCHMARK` · `SECURITY_REFERENCE`

**Dispositions:** `USE` (direct dependency / substantially reused) · `ADAPT` (reuse but materially change) · `STUDY` (evidence only, never a dependency) · `BENCHMARK` (evaluate experimentally) · `DEFER` (useful, out of current phase) · `REJECT` (investigated, intentionally excluded)

**Fehrest layers:** `KNOWLEDGE` (canonical files) · `EVENT` (canonical activity log) · `DERIVED` (rebuildable indexes) · `MEMORY` · `AGENT` · `SECURITY` · `INGEST` · `UI` · `SHELL` · `EVAL`

---

## 1. Dispositions changed from the founder's draft registry

Four dispositions in the founder's draft are **contradicted by measurement**. Each is argued in full below and re-decided here. This section exists so a reviewer can find the disagreements immediately instead of hunting for them.

| Source | Draft disposition | Registry disposition | Deciding evidence |
|---|---|---|---|
| **BlockSuite** | `USE / PROTOTYPE`, Priority **S+** | **DEFER** | [E-10](EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate) — mirror 13.4 months stale; npm unpublished 13.5 months at 0.22.4; 6 unmerged vulnerability branches; real development inside AFFiNE monorepo |
| **Yjs** | `USE / PROTOTYPE` | **DEFER** (healthy, but unnecessary in v1) | [E-11](EVIDENCE_LOG.md#e-11--yjs-and-codemirror-are-healthy-the-crdt-is-not-the-stale-part) — Yjs is fine; single-user MVP has no collaboration requirement to justify a CRDT |
| **AFFiNE** | `ADAPT` | **STUDY** | [E-10](EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate) — split license (`packages/backend`, `packages/common/native` non-MIT); 446 MB app monorepo; no releasable substrate boundary |
| **DuckDB** | `USE FOR DATA INTELLIGENCE`, Priority **S** | **DEFER** | No MVP requirement; §16 of the brief itself declares Data Intelligence out of MVP scope. Priority S contradicts that. |

One source is **added** that the draft registry omits and the architecture now depends on:

| Source | Class | Disposition | Why added |
|---|---|---|---|
| **CodeMirror 6** | `CODE_DONOR` | **USE** | Replaces BlockSuite as the v1 editing surface. MIT, current ([E-11](EVIDENCE_LOG.md#e-11--yjs-and-codemirror-are-healthy-the-crdt-is-not-the-stale-part)). Admitted under Research Freeze rule (2): replaces a weaker existing candidate. |

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
risks:
  - CRITICAL: node IDs are name-derived normalised slugs, unstable under rename and Unicode
    representation, with documented collision history (#550 same-filename collisions, #811,
    #1033, #2614). Mitigation: Fehrest allocates its own opaque IDs; graphify_node_id is a
    derived non-authoritative mapping column, rebuildable (E-4, ADR-0004).
  - Packaging weight: 32 packages / 130 MB site-packages excluding CPython; ~200-300 MB
    installer delta with a bundled runtime (E-3). Mitigation: optional capability install.
  - Startup: 4,451 ms cold import, 276 ms warm (E-6). Mitigation: long-lived sidecar (ADR-0003).
  - AMBIGUOUS confidence measured at 0.0% -- do not build trust logic on it (E-5).
  - Upstream is pre-1.0 (0.9.45) on a moving default branch named v8; API may break.
  - Transitive CVE exposure in the optional HTTP/MCP stack, tracked upstream via pinned
    starlette floors (E-3). Mitigation: independent sidecar update channel.
  - Python parsers process untrusted vault content in-process with 12 worker subprocesses.
    Mitigation: sidecar confinement + parser fuzzing (H-5).
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

### 2.3 CodeMirror 6

```yaml
id: SRC-003
name: CodeMirror 6
class: CODE_DONOR
repository_or_url: https://github.com/codemirror   # @codemirror/* packages published independently
upstream_owner: Marijn Haverbeke
exact_commit_or_version: "@codemirror/state@6.7.1"   # published 2026-07-05; pin full package set at Phase 3
date_verified: 2026-08-17
decision: USE
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

### 3.1 BlockSuite — DEFER (reclassified from S+)

```yaml
id: SRC-004
name: BlockSuite
class: CODE_DONOR
repository_or_url: https://github.com/toeverything/blocksuite
upstream_owner: toeverything
exact_commit_or_version: 5cb5cb68471ca692f3c162258f0087cb22fcb82d   # main HEAD, 2025-07-07 -- 13.4 months stale
npm_version_observed: "@blocksuite/store@0.22.4, last published 2025-07-01"
date_verified: 2026-08-17
decision: DEFER            # was: USE / PROTOTYPE, Priority S+
fehrest_layer: UI
what_we_use: []            # nothing in v1
what_we_do_not_use: [everything, in, v1]
why: >
  Reclassified on maintenance and licensing evidence, not on capability. BlockSuite's own
  repository is a downstream MIRROR of packages developed inside the AFFiNE monorepo -- the
  last five commits are all "chore: sync affine blocksuite to packages" and the sync stopped
  2025-07-07. @blocksuite/store has not been published to npm since 2025-07-01 and remains
  pre-1.0 at 0.22.4. Six renovate/npm-*-vulnerability branches (dompurify, file-type,
  lodash-es, minimatch, simple-git, vite, vitest) are open and unmerged. Real development
  happens inside toeverything/AFFiNE (HEAD 2026-08-17) under a split license.
  Consequence: the round-trip architecture gate CANNOT be cleared against a maintained
  upstream. Clearing it against a frozen mirror would prove a property of a snapshot, not of
  a substrate Fehrest can depend on.
risks_if_adopted_anyway:
  - Fehrest's primary editing substrate would be unmaintained and unreleased from day one
  - Inherited unpatched transitive dependency vulnerabilities
  - Vendoring from a 446 MB application monorepo with no releasable boundary
  - MPL-2.0 on the mirror vs split MIT/other in AFFiNE -- file-level license provenance
    would have to be established per vendored file
reconsider_if: >
  (1) upstream resumes independent releases for two consecutive quarters, OR
  (2) H-4 is falsified -- dogfooding proves Markdown plus documented sidecars genuinely
      cannot express required knowledge work -- AND no maintained alternative exists, OR
  (3) Fehrest decides to vendor a specific frozen subset at a pinned AFFiNE commit with
      per-file license provenance and accepts permanent maintenance ownership.
license: MPL-2.0 (mirror); AFFiNE upstream is split MIT / separate backend license
evidence: [E-10]
```

### 3.2 Yjs — DEFER

```yaml
id: SRC-005
name: Yjs
class: [CODE_DONOR, RESEARCH]
repository_or_url: https://github.com/yjs/yjs
exact_commit_or_version: yjs@13.6.32     # published 2026-08-04
date_verified: 2026-08-17
decision: DEFER
fehrest_layer: KNOWLEDGE
why: >
  Deferred on NECESSITY, not health -- an important distinction. Yjs is MIT and actively
  released. But a single-user, local-first MVP has no collaboration requirement, and a CRDT
  introduces exactly the class of state that Fehrest's canonical-file invariant forbids:
  document state that is authoritative inside the runtime but not expressible in the open file.
  Introducing it before there is a collaborator to synchronise with buys risk with no product.
reconsider_if: Real-time multi-writer collaboration enters scope (post-v1, Phase 8+).
constraint_when_reconsidered: >
  Do not introduce a second CRDT runtime alongside it. Do not combine with Automerge without
  a dedicated ADR proving a need neither satisfies alone.
license: MIT
evidence: [E-11]
```

### 3.3 AFFiNE — STUDY (reclassified from ADAPT)

```yaml
id: SRC-006
name: AFFiNE
class: [PRODUCT_REFERENCE, CODE_DONOR]
repository_or_url: https://github.com/toeverything/AFFiNE
exact_commit_or_version: b4c8548c09da21b2898443559a5b846f0ccf5dd8   # canary, 2026-08-17
date_verified: 2026-08-17
decision: STUDY            # was: ADAPT
fehrest_layer: UI
what_we_use: [workspace UX patterns, document/canvas/database view concepts, local-first app patterns]
what_we_do_not_use: [any code in v1]
why: >
  Downgraded from ADAPT because there is no clean substrate boundary to adapt: the editing
  layer lives inside a 446 MB application monorepo and its license is split -- content under
  packages/backend and packages/common/native falls under a separate license, with MIT
  applying only outside those directories. Adapting code would require per-file license
  provenance for every vendored file. As a product reference it remains valuable.
  Explicitly NOT to be forked and renamed Fehrest.
license: Split -- MIT outside packages/backend and packages/common/native; separate license within
evidence: [E-10]
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

The architecture discovery phase closes when [P Phase 0](../15-IMPLEMENTATION-PHASES.md) exits. After that, a new source may enter this registry **only** if it:

1. closes a documented gap in this registry; or
2. replaces a weaker existing candidate (with the comparison recorded); or
3. falsifies an existing architectural assumption; or
4. provides materially stronger evidence than an incumbent; or
5. is required for security or interoperability.

Each admission requires a registry entry, a named displaced or closed item, and an ADR if it changes a decision. CodeMirror 6 (SRC-003) is admitted under clause 2, displacing BlockSuite.

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
