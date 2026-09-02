# Fehrest Source Readiness Registry 2026

**Status:** NON-AUTHORIZING SOURCE / DONOR READINESS RECORD  
**Verified:** 2026-09-02  
**Authority:** planning and evidence only. Presence here does not authorize dependency adoption, code reuse, network access, graph/vector activation, MCP/ACP, UI, automatic memory, or any product behavior while blocked by `specs/CURRENT.md`.

> `SOURCE_FOUND != SOURCE_ADMITTED`  
> `SOURCE_USEFUL != SOURCE_REQUIRED`  
> `BENCHMARK_CANDIDATE != PRODUCTION_DEPENDENCY`

## 1. Why this registry exists

Fehrest already names many external systems across `AGENTS.md`, the canonical execution master plan, benchmark/security documents, the V2 proposal, and current research planning. The live GitHub mirror, however, does not currently contain the older historical `docs/research/EVIDENCE_LOG.md` or `docs/research/FEHREST_SOURCE_REGISTRY.md` paths referenced by several mirrored documents.

That absence is a real source-readiness gap. This file does **not** reconstruct or impersonate those missing historical artifacts. It provides a fresh, dated current-source registry so future work can find the correct upstream systems without guessing.

```text
HISTORICAL_SOURCE_REGISTRY_RECONSTRUCTED=NO
CURRENT_SOURCE_READINESS_REGISTRY_CREATED=YES
MISSING_HISTORICAL_EVIDENCE_MUST_STILL_BE_RECONCILED_WHEN_AVAILABLE=YES
```

## 2. Readiness classes

Each source receives one or more roles:

```text
REFERENCE      architecture or protocol reference
DONOR          implementation patterns worth adapting
BENCHMARK      comparator to run, not merely cite
PROVIDER       replaceable external implementation candidate
INGESTOR       external evidence acquisition/parser candidate
EVALUATION     benchmark/eval infrastructure
SECURITY       isolation/policy/security reference
DEFER          useful but not needed for the first proven wedge
```

Readiness states:

```text
READY_TO_STUDY        canonical source identified; directly useful for design/research
READY_TO_BENCHMARK    comparator is sufficiently concrete to design a fair evaluation
PIN_BEFORE_ADOPTION   immutable revision + license/NOTICE/dependency review required before reuse
SPECIAL_LICENSE       licensing requires additional care before code reuse
MAINTENANCE_ONLY      useful methodology/reference, weak production-dependency candidate
```

## 3. Graph intelligence and Graph-RAG family

### SRC-GRAPH-001 — Graphify

- Canonical source: `https://github.com/Graphify-Labs/graphify`
- Role: `DONOR / BENCHMARK / REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: deterministic local code AST graph extraction, code/docs graph schema ideas, provenance tags, rationale extraction, graph traversal, community structure, review/blast-radius ideas.
- Important property: code extraction is designed around local deterministic tree-sitter processing; modern upstream also exposes a broader multimodal graph surface.
- Do not assume historical Fehrest measurements against an older Graphify snapshot still describe current upstream. Re-run all load-bearing throughput/footprint/grammar claims on an immutable pin.
- Adoption rule: graph output remains derived; Graphify IDs/ranks/paths never become Fehrest identity or authority.

### SRC-GRAPH-002 — Code-Graph-RAG

- Canonical source: `https://github.com/vitali87/code-graph-rag`
- Role: `BENCHMARK / DONOR / REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: code-graph retrieval, Tree-sitter/AST graph methodology, graph-backed code understanding, structural search/edit evaluation, data-flow/blast-radius ideas.
- Key distinction: its database/runtime choices are not automatically compatible with Fehrest local-first core. Prefer methodology and benchmark value before infrastructure adoption.

### SRC-GRAPH-003 — Microsoft GraphRAG

- Canonical source: `https://github.com/microsoft/graphrag`
- Role: `REFERENCE / BENCHMARK`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / MAINTENANCE_ONLY`
- Fehrest use: graph-based context construction, entity/relationship/claim extraction, community summaries, global/local query methodology.
- Current caution: upstream describes the project as largely maintenance mode and research-oriented. Treat it as methodology/comparator, not a default production dependency.
- Cost caution: indexing can require LLM extraction and can be expensive; compare under normalized model-visible budgets and acquisition cost.

### SRC-GRAPH-004 — Graphiti

- Canonical source: `https://github.com/getzep/graphiti`
- Role: `BENCHMARK / REFERENCE / DONOR`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: temporal context graphs, incremental updates, provenance, historical queries, hybrid semantic/keyword/graph retrieval, bitemporal design comparison.
- Critical comparison: Graphiti is particularly relevant to Fehrest memory/temporal-state claims, not only static code graph tasks.
- Boundary: graph-derived facts do not bypass Fehrest evidence/verification/lifecycle semantics.

### SRC-GRAPH-005 — LightRAG

- Canonical source: `https://github.com/HKUDS/LightRAG`
- Role: `BENCHMARK / REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK`
- Fehrest use: graph + vector retrieval alternative, incremental graph-RAG design, cost/latency comparison against Microsoft GraphRAG and simpler retrieval.
- Rule: benchmark only where workloads are comparable; do not force document-centric GraphRAG into code-graph experiments.

### SRC-GRAPH-006 — tree-sitter

- Canonical source: `https://github.com/tree-sitter/tree-sitter`
- Role: `DONOR / PROVIDER / REFERENCE`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: deterministic code structure extraction substrate if future graph/index experiments require an in-house Rust-native path rather than a Python sidecar.
- Strategic importance: provides a credible escape hatch if Graphify capability is retained but its runtime/dependency shape is rejected.

## 4. Memory, continual learning, and temporal context

### SRC-MEM-001 — Mem0

- Canonical source: `https://github.com/mem0ai/mem0`
- Role: `BENCHMARK / REFERENCE / DONOR`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: memory generation/use evaluation, multi-level memory, token-efficient retrieval, freshness/decay, consolidation research.
- Required comparison: outcome quality per token/cost, stale-memory behavior, temporal correctness, and cross-session continuation.
- Boundary: Mem0-style automatic memory must not bypass Fehrest candidate/verification/promotion gates.

### SRC-MEM-002 — Letta

- Canonical source: `https://github.com/letta-ai/letta`
- Role: `BENCHMARK / REFERENCE / DONOR`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: stateful agents, memory editing, long-lived agent state, skills/subagents, trajectory and continual-learning concepts.
- Critical distinction: Fehrest memory is project-owned and must survive replacement of the agent runtime. Letta is therefore both comparator and architecture contrast.

### SRC-MEM-003 — Hermes Agent

- Canonical source: `https://github.com/NousResearch/hermes-agent`
- Role: `DONOR / BENCHMARK / REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: procedural memory/skills, self-improvement loop, context files, messaging surfaces, multi-provider agent runtime, MCP integration, trajectory generation/compression.
- Boundary: study how a persistent agent learns; do not let runtime-owned memory become the only project memory.

### SRC-MEM-004 — LongMemEval / LongMemEval-V2

- Canonical research source: paper/dataset referenced by the existing Fehrest benchmark plan, including arXiv `2605.12493` for LongMemEval-V2.
- Role: `EVALUATION / BENCHMARK`
- Readiness: `READY_TO_STUDY`; exact dataset/code revision must be pinned before execution.
- Fehrest use: static state, dynamic state, workflow knowledge, environment gotchas, premise awareness, and long-trajectory memory evaluation.
- Rule: benchmark against competent ordinary agents and maintained project artifacts, not weak RAG baselines alone.

## 5. Lexical, vector, hybrid, and retrieval infrastructure

### SRC-RET-001 — Qdrant

- Canonical source: `https://github.com/qdrant/qdrant`
- Role: `PROVIDER / BENCHMARK`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: dense/sparse/multivector and hybrid retrieval at larger scale.
- Boundary: optional derived provider only; never canonical state or authority.

### SRC-RET-002 — Chroma

- Canonical source: `https://github.com/chroma-core/chroma`
- Role: `PROVIDER / BENCHMARK`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: vector/hybrid/full-text comparison and agent-memory ecosystem comparison.

### SRC-RET-003 — sqlite-vec

- Canonical source: `https://github.com/asg017/sqlite-vec`
- Role: `PROVIDER / BENCHMARK`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: local embedded vector acceleration with lower operational weight than a server database.
- Caution: maturity must be rechecked at adoption time; older Fehrest documents explicitly treated its release line as immature/alpha.

### SRC-RET-004 — Aider repo map

- Canonical source: `https://github.com/Aider-AI/aider`
- Role: `BENCHMARK / REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK`
- Fehrest use: mandatory strong simple code-context baseline. Fehrest graph/context complexity must earn its cost against repo-map style structural context.

### SRC-RET-005 — LLMLingua

- Canonical source: `https://github.com/microsoft/LLMLingua`
- Role: `BENCHMARK / DONOR`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: prompt/context compression experiments.
- Boundary: original evidence must remain available; compression is a provenance-recorded transform, never canonical rewriting.

## 6. Agent protocols and interoperability

### SRC-PROTO-001 — Model Context Protocol

- Canonical source: `https://github.com/modelcontextprotocol/modelcontextprotocol`
- Current relevant specification family includes `2026-07-28`.
- Role: `REFERENCE / PROVIDER BOUNDARY`
- Readiness: `READY_TO_STUDY / PIN_VERSION_BEFORE_IMPLEMENTATION`
- Fehrest use: tool/resource interoperability across IDEs, CLIs, and agent runtimes.
- Boundary: MCP capability negotiation is not Fehrest authorization. Fehrest grants/leases remain authoritative.

### SRC-PROTO-002 — Agent Client Protocol

- Canonical ecosystem source: Zed/ACP specification and implementations under the Agent Client Protocol ecosystem; exact repository/spec revision must be pinned before Phase 5 implementation.
- Role: `REFERENCE / PROVIDER BOUNDARY`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_IMPLEMENTATION`
- Fehrest use: agent/client interoperability and IDE integration.

### SRC-PROTO-003 — Buzz

- Canonical source: `https://github.com/block/buzz`
- Reviewed immutable revision: `1c8321cd08feb597f8bcff5195c21148fb3e98ed`
- Public license at reviewed revision: Apache-2.0.
- Role: `DONOR / REFERENCE`
- Readiness: `PINNED_RESEARCH_SOURCE`
- Fehrest use: ACP/MCP boundaries, permission lifecycle, process supervision, context handoff, human/agent workspace patterns.
- Detailed record: `docs/research/BUZZ_DONOR_STUDY_AND_FEHREST_PLAN.md`.

## 7. Agent runtimes and software-engineering comparators

### SRC-AGENT-001 — mini-SWE-agent

- Canonical source: `https://github.com/SWE-agent/mini-swe-agent`
- Role: `BENCHMARK / HARNESS REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK`
- Fehrest use: minimal inspectable coding-agent harness to reduce framework confounding in continuation experiments.

### SRC-AGENT-002 — OpenHands

- Canonical source: `https://github.com/All-Hands-AI/OpenHands`
- Role: `BENCHMARK / REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_REUSE`
- License caution: core is open source, but repository licensing has directory-specific exceptions; any code reuse requires path-level license review.
- Fehrest use: richer real-world software agent runtime, sandbox/execution and workspace patterns.

### SRC-AGENT-003 — Hermes Agent

- Reuse `SRC-MEM-003` for agent-runtime comparison so the registry does not create duplicate ownership.

### SRC-AGENT-004 — Aider

- Reuse `SRC-RET-004`; compare both repo-map context and a mature CLI coding workflow where applicable.

## 8. Execution and sandbox providers

### SRC-EXEC-001 — E2B

- Canonical source: `https://github.com/e2b-dev/e2b`
- Role: `PROVIDER / BENCHMARK / SECURITY REFERENCE`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: remote isolated agent execution provider comparison.

### SRC-EXEC-002 — Daytona

- Canonical source: `https://github.com/daytonaio/daytona`
- Role: `PROVIDER / BENCHMARK`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / SPECIAL_LICENSE`
- License caution: current public repository is AGPL-3.0; integration is not equivalent to copying source. Re-check obligations before any embedding/modification/distribution.
- Fehrest use: secure elastic persistent sandbox comparison.

### SRC-EXEC-003 — OpenSandbox

- Canonical upstream must be revalidated immediately before benchmark/adoption because multiple projects use this name.
- Role: `PROVIDER / BENCHMARK / SECURITY REFERENCE`
- Readiness: `SOURCE_IDENTITY_REVALIDATION_REQUIRED`
- Fehrest use: strong-isolation, egress and credential-injection comparison described by the canonical master plan.
- No code may be copied until exact repository + revision + license are recorded.

### SRC-EXEC-004 — local Docker / OCI runtime

- Role: `BENCHMARK / PROVIDER`
- Readiness: `READY_TO_BENCHMARK`
- Fehrest use: simple local baseline for isolated execution.
- Boundary: containerization alone is not a complete security claim.

### SRC-EXEC-005 — Buzz dev MCP shell lifecycle

- Reuse pinned `SRC-PROTO-003` as donor for cancellation, output bounds, process groups, Windows Job Objects, and child cleanup.

## 9. Capability security and policy references

### SRC-SEC-001 — cap-std

- Canonical source: `https://github.com/bytecodealliance/cap-std`
- Role: `SECURITY / DONOR`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: Rust capability-oriented filesystem/network APIs and deny-by-construction design.

### SRC-SEC-002 — Cedar

- Canonical source: `https://github.com/cedar-policy/cedar`
- Role: `SECURITY / REFERENCE / POSSIBLE PROVIDER`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: authorization-policy language/engine comparison.
- Boundary: adopting a policy engine cannot weaken Fehrest's canonical grant semantics or single authorization chokepoint.

### SRC-SEC-003 — AgentDojo

- Canonical benchmark source must be pinned before use.
- Role: `SECURITY / EVALUATION`
- Readiness: `READY_TO_STUDY / PIN_DATASET_AND_HARNESS_BEFORE_EXECUTION`
- Fehrest use: prompt-injection/tool-use security benchmark inspiration and adversarial corpus design.

## 10. Document and external-evidence ingestion

### SRC-INGEST-001 — Firecrawl

- Canonical source: `https://github.com/firecrawl/firecrawl`
- Role: `INGESTOR / PROVIDER`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: web acquisition when a measured external-evidence requirement exists.
- Boundary: crawler output is hostile evidence, never instruction or authority.

### SRC-INGEST-002 — Docling

- Canonical source: `https://github.com/docling-project/docling`
- Role: `INGESTOR / BENCHMARK / DONOR`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: PDFs and heterogeneous document parsing, structured document model, local document conversion.
- Strategic fit: strong candidate for Project Capsule evidence ingestion because it preserves more document structure than plain text conversion.

### SRC-INGEST-003 — Microsoft MarkItDown

- Canonical source: `https://github.com/microsoft/markitdown`
- Role: `INGESTOR / BENCHMARK`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK / PIN_BEFORE_ADOPTION`
- Fehrest use: lightweight multi-format conversion baseline.

### SRC-INGEST-004 — LlamaIndex

- Canonical source: `https://github.com/run-llama/llama_index`
- Role: `REFERENCE / INGESTOR / BENCHMARK`
- Readiness: `READY_TO_STUDY`; dependency adoption deferred until a measured requirement exists.
- Fehrest use: connector/parser ecosystem and retrieval workflow comparison, not core authority.

## 11. Local-first collaboration and replication

### SRC-COLLAB-001 — Automerge

- Canonical source: `https://github.com/automerge/automerge`
- Role: `REFERENCE / DONOR / PROVIDER CANDIDATE`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: Rust CRDT core, local-first persistence/sync protocol, concurrent-edit research.
- Boundary: CRDT convergence does not define semantic authority or resolve every domain conflict. Decisions, grants, work-state transitions and provenance may require typed conflict semantics above CRDT mechanics.

### SRC-COLLAB-002 — Yjs

- Canonical source: `https://github.com/yjs/yjs`
- Role: `REFERENCE / BENCHMARK`
- Readiness: `READY_TO_STUDY`
- Fehrest use: mature CRDT/editor collaboration comparator.
- Not preferred for correctness-core ownership merely because the frontend ecosystem is strong.

## 12. Evaluation and observability

### SRC-EVAL-001 — SWE-bench

- Canonical source: `https://github.com/SWE-bench/SWE-bench`
- Role: `EVALUATION / BENCHMARK`
- Readiness: `READY_TO_STUDY / READY_TO_BENCHMARK`
- Fehrest use: real-world repository issue solving and reproducible containerized software-engineering evaluation.
- Rule: SWE-bench tests task completion, not Fehrest memory thesis by itself. Use as one workload family inside a broader continuation benchmark portfolio.

### SRC-EVAL-002 — Braintrust SDK

- Canonical source: Braintrust SDK repositories; JS SDK currently under the Braintrust GitHub organization.
- Role: `EVALUATION / OPTIONAL EXPORTER`
- Readiness: `READY_TO_STUDY`
- Fehrest use: eval/tracing exporter reference.
- Boundary: hosted or vendor-specific eval systems never become the only experiment record.

### SRC-EVAL-003 — OpenTelemetry

- Canonical source: `https://github.com/open-telemetry/opentelemetry-specification`
- Role: `REFERENCE / OPTIONAL EXPORTER`
- Readiness: `READY_TO_STUDY`
- Fehrest use: standard observability export; Fehrest still owns local open evidence/trial schema.

### SRC-EVAL-004 — DSPy

- Canonical source: `https://github.com/stanfordnlp/dspy`
- Role: `RESEARCH / BENCHMARK TOOLING`
- Readiness: `READY_TO_STUDY`
- Fehrest use: bounded optimization experiments after benchmark freeze, never self-modifying benchmark authority/security.

## 13. Git/project transport sources

### SRC-GIT-001 — Git itself

- Canonical specification/tooling source: `https://git-scm.com/` and upstream Git source.
- Role: `REFERENCE / TRANSPORT`
- Readiness: `FOUNDATIONAL`
- Fehrest use: exact object semantics, bundles, refs, patches, repository import/export.
- Hard boundary: Fehrest Project identity is above Git repository identity.

### SRC-GIT-002 — gix / gitoxide

- Canonical source: `https://github.com/GitoxideLabs/gitoxide`
- Role: `DONOR / PROVIDER CANDIDATE`
- Readiness: `READY_TO_STUDY / PIN_BEFORE_ADOPTION`
- Fehrest use: Rust-native Git object/transport implementation candidate for no-fork Project Capsule import/export.
- Required evaluation: fidelity, pack/protocol support, performance, Windows behavior, security, and maintenance burden versus invoking system Git/libgit2.

### SRC-GIT-003 — libgit2 / git2-rs

- Canonical sources: `https://github.com/libgit2/libgit2` and `https://github.com/rust-lang/git2-rs`
- Role: `PROVIDER CANDIDATE / BENCHMARK`
- Readiness: `READY_TO_STUDY`
- Fehrest use: mature alternative to gix for repository transport/object operations.

## 14. Source coverage mapped to Fehrest phases

| Fehrest area | Primary source set |
|---|---|
| Canonical core | SQLite/Rust ecosystem, cap-std, Cedar as policy reference |
| Derived lexical/index | Aider repo-map, native FTS/BM25, Chroma/Qdrant/sqlite-vec as optional comparators |
| Graph capability experiment | Graphify, Code-Graph-RAG, Graphiti, Microsoft GraphRAG, LightRAG, tree-sitter |
| Temporal memory | Mem0, Letta, Graphiti, Hermes, LongMemEval-V2 |
| Context compiler | Aider repo-map, LLMLingua, graph/vector comparators, Fehrest-native deterministic compiler |
| Agent gateway | MCP, ACP, Buzz, Hermes, mini-SWE-agent, OpenHands |
| Execution | Buzz dev MCP lifecycle, local Docker, E2B, Daytona, OpenSandbox after identity revalidation |
| External evidence | Firecrawl, Docling, MarkItDown, LlamaIndex |
| Collaboration | Automerge, Yjs, local-first research |
| Git/project substrate | Git, gix/gitoxide, libgit2/git2-rs, GitHub APIs as publication/integration surface |
| Evaluation | LongMemEval-V2, SWE-bench, AgentDojo, Braintrust/OpenTelemetry exporters, Fehrest local trial schema |

## 15. Major source gaps discovered by this audit

### GAP-SRC-001 — missing historical evidence/source registry bytes

Several mirrored documents reference historical `docs/research/EVIDENCE_LOG.md` and `docs/research/FEHREST_SOURCE_REGISTRY.md`, but those files are not present in current GitHub `main` or PR #27.

Action:

```text
DO_NOT_RECONSTRUCT_HISTORICAL_CONTENT_FROM_MEMORY
SEARCH_RECOVERY_BUNDLES_OR_ORIGINAL_SOURCE
RECONCILE_WHEN_BYTES_ARE_AVAILABLE
UNTIL_THEN_USE_THIS_DATED_CURRENT_REGISTRY_FOR_NEW_RESEARCH_ONLY
```

### GAP-SRC-002 — Graphify source drift

Existing Fehrest documents contain measurements/claims against an earlier Graphify state, while current Graphify upstream has materially expanded its language/feature surface.

Action: every load-bearing Graphify benchmark must record exact immutable upstream revision and rerun measurements.

### GAP-SRC-003 — OpenSandbox identity ambiguity

The master plan names OpenSandbox, but the exact intended canonical upstream is not safely identified in the currently mirrored source record.

Action: do not benchmark or reuse code until repository/revision/license are fixed in evidence.

### GAP-SRC-004 — ACP pin missing

ACP is strategically important but must be pinned to an exact current protocol specification/repository before implementation design.

### GAP-SRC-005 — no current dependency-rights manifest for the broader donor portfolio

Before any code reuse, create per-adoption provenance records containing:

```text
source_id
repository
revision/tag
license SPDX
NOTICE obligations
copied/adapted paths
upstream copyright headers
modification notice requirement
dependency/SBOM snapshot
security review
benchmark justification
active spec authority
```

## 16. Adoption gate for every external source

No source moves from research to production without:

```text
1. REQUIREMENT EXISTS
2. SIMPLEST NATIVE OPTION EVALUATED
3. EXACT SOURCE + IMMUTABLE REVISION PINNED
4. LICENSE / NOTICE / TRADEMARK OBLIGATIONS VERIFIED
5. DEPENDENCY AND SBOM SURFACE RECORDED
6. SECURITY / TRUST BOUNDARY REVIEWED
7. BENCHMARK RUN WHEN LOAD-BEARING
8. FAILURE / REMOVAL PATH DEFINED
9. ACTIVE SPEC AUTHORIZES ADOPTION
10. EXACT-HEAD INDEPENDENT REVIEW PASSES
```

## 17. Final source-readiness statement

The project now has a current actionable source map spanning graph intelligence, GraphRAG, temporal memory, vector/lexical retrieval, protocols, agent runtimes, execution sandboxes, security policy, ingestion, local-first collaboration, evaluation and Git/project transport.

The registry deliberately does **not** claim that every source is a dependency or that every upstream claim is locally reproduced.

```text
SOURCE_DISCOVERY_COVERAGE=STRONG
SOURCE_ROLE_MAPPING=READY
GRAPH_SOURCE_FAMILY=READY_FOR_FUTURE_FAIR_BENCHMARK_DESIGN
MEMORY_SOURCE_FAMILY=READY_FOR_FUTURE_FAIR_BENCHMARK_DESIGN
AGENT_PROTOCOL_SOURCE_FAMILY=READY_FOR_FUTURE_PHASE5_DESIGN
PROJECT_TRANSPORT_SOURCE_FAMILY=READY_FOR_FUTURE_DESIGN
HISTORICAL_EVIDENCE_RECONCILIATION=STILL_REQUIRED_WHEN_BYTES_AVAILABLE
PRODUCTION_ADOPTION_AUTHORIZED=NO
ACTIVE_FRONTIER_CHANGED=NO
```
