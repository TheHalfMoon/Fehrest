# Tencent Source Qualification for Fehrest V2 — 2026-09-08

**Status:** RESEARCH RECORD / NON-AUTHORIZING  
**Change class:** planning input only; no R1 or product execution effect  
**Trigger:** founder-supplied gap-driven source review on 2026-09-08  
**Canonical authority:** live `AGENTS.md`, `specs/CURRENT.md`, and canonical execution governance remain superior

> This record qualifies three external sources as future planning and benchmark inputs. It does not admit a dependency, authorize code reuse, activate a future spec, alter R1, mutate the frozen R1-v2 review candidate, or authorize product implementation.

## 1. Source pins

| Source | Reviewed revision | Rights status at review | Current Fehrest disposition |
|---|---|---|---|
| `Tencent/RoMem` | `39ac1417b4db41ea729e5c3be71ac20de54da993` | No root `LICENSE` found in reviewed repository tree; source-code reuse rights not established | `STUDY + BENCHMARK`; code reuse `NO` |
| `Tencent/WeKnora` | `647848f3954dae34473b8a8d0e0eef5e0fb3a58e` | Root MIT license; repository records separately licensed third-party components | `STUDY + BENCHMARK`; future per-file `ADAPT` candidate |
| `Tencent/SkillHone` | `7d565839fb4dc74f9c77f09ace660e1c0484e048` | MIT | `STUDY + BENCHMARK`; future bounded `ADAPT` candidate |

Upstream links:

- https://github.com/Tencent/RoMem
- https://github.com/Tencent/WeKnora
- https://github.com/Tencent/SkillHone

Revision pins MUST be refreshed before any future load-bearing decision.

## 2. Admission law

```text
SOURCE_FOUND != SOURCE_ADMITTED
PUBLIC_REPOSITORY != REUSE_PERMISSION
INTERESTING_FEATURE != REQUIREMENT
RESEARCH_RESULT != AUTHORIZATION
DONOR_RANK != CANONICAL_AUTHORITY
```

Every future adoption still passes:

```text
requirement
-> necessity / Ponytail gate
-> exact source revision + path
-> license / rights / attribution
-> security and privacy review
-> fair benchmark where material
-> explicit adoption decision
-> authorized implementation
```

No donor may weaken Fehrest's canonical-vs-derived, provenance, temporal, secret, grant, recovery, or local-first invariants.

## 3. RoMem qualification

### 3.1 High-value concepts

RoMem presents temporal memory as a ranking problem with continuous time, a relation-dependent semantic speed gate, and geometric shadowing of temporally obsolete facts. Its public package also includes temporal-memory benchmark runners and comparator implementations/pipelines around systems such as Mem0, Graphiti, HippoRAG and temporal-KGE baselines.

High-value Fehrest questions:

```text
Can relation-dependent temporal scoring improve historical/as-of retrieval?
Can a derived volatility estimate help rank changing facts without mutating canonical truth?
Can temporal reranking reduce contradiction errors over simpler explicit temporal filtering?
Does the added model/embedding/graph complexity improve fresh-agent continuation enough to justify itself?
```

### 3.2 Fehrest mapping

| Capability | Target owner/gate | Disposition |
|---|---|---|
| Continuous-time temporal reranking | future 004 capability experiment, consumed by 006/007 only if retained | `BENCHMARK` |
| Relation volatility / semantic speed estimate | 004 experiment; derived-only if retained | `STUDY + BENCHMARK` |
| Non-destructive treatment of obsolete facts | 006 temporal-memory design comparison | `STUDY` |
| Temporal memory benchmark methodology | 004/009 benchmark design input | `STUDY + BENCHMARK` |
| RoMem implementation code | none until rights established | `DEFER` |

### 3.3 Hard boundaries

```text
TEMPORAL_RANK != TEMPORAL_TRUTH
RELATION_VOLATILITY_SCORE != CANONICAL_FACT
GEOMETRIC_SCORE != AUTHORIZATION
OBSOLETE_FACT != DELETE_HISTORY
MODEL_DERIVED_TIME_SIGNAL != USER_CONFIRMED_MEMORY
```

Fehrest canonical temporal resolution must remain deterministic/auditable from canonical evidence. A RoMem-like signal, if ever retained, is only a replaceable derived retrieval feature.

### 3.4 Rights gate

At the reviewed revision no root `LICENSE` file was found. Therefore:

```text
ROMEM_CODE_COPY=NO
ROMEM_CODE_ADAPTATION=NO
ROMEM_VENDORING=NO
ROMEM_ALGORITHM_STUDY=YES
ROMEM_BLACK_BOX_OR_CLEAN_REIMPLEMENTATION_BENCHMARK=ONLY_AFTER_RIGHTS_AND_SPEC_GATE
```

Do not infer source-code reuse permission from an academic paper, repository visibility, or an organization name.

## 4. WeKnora qualification

### 4.1 High-value concepts

The reviewed WeKnora revision exposes several patterns relevant to Fehrest:

- cross-session long-term memory with categories such as profile, preference, fact, task and interest;
- auto-extraction with a user-confirmation stage rather than silent durable promotion;
- on-demand `search_memory` and a distinction between persistent profile context and recalled situational memory;
- revision history and rollback for wiki/document/chunk surfaces;
- scoped API keys and a principal model;
- workspace RBAC and audit trails;
- session-persistent Docker/E2B/Cube skill sandboxes with configurable network policy;
- skill catalogs, MCP/tool scoping and environment-variable boundaries;
- task queues, worker-pool governance and observability;
- modular retrieval, reranking, storage and provider boundaries.

These are comparison inputs, not proof that WeKnora's exact architecture matches Fehrest's trust model.

### 4.2 Fehrest mapping

| Capability family | Target owner/gate | Disposition |
|---|---|---|
| Confirm-before-durable memory | 006 | `STUDY + ADAPT-PATTERN` |
| Memory category/risk differentiation | 006 | `STUDY` |
| Resident vs on-demand memory retrieval | 006/007 | `BENCHMARK` |
| Revision/rollback UX | 010/011; derived-index reconciliation in 003 | `STUDY + ADAPT-PATTERN` |
| Scoped API keys/principals | 007 baseline, 018 org extension | `STUDY + SECURITY-COMPARATOR` |
| Session-persistent sandbox | 007 execution admission foundation; 013/021 consumers | `BENCHMARK` |
| Per-workspace/network policy | 007/018/021 security design | `STUDY + BENCHMARK` |
| MCP/tool scope | 007/014/021 | `STUDY`; no current MCP authority |
| Task queue / worker governance | 007 execution-attempt semantics; provider schedulers consume it | `STUDY` |
| Wiki/knowledge graph | 010/011/012, with derived graph rules from 004/005 | `STUDY` |

### 4.3 Hard boundaries

```text
EXTERNAL_API_KEY != FEHREST_PRINCIPAL_AUTHORITY
WORKSPACE_ROLE != CAPABILITY_LEASE
SANDBOX_NETWORK_POLICY != COMPLETE_AUTHORIZATION
QUEUE_RETRY != SAFE_RETRY
EDITABLE_RETRIEVAL_CHUNK != NEW_HIDDEN_CANONICAL_SOURCE
AUTO_WIKI != CANONICAL_MEMORY
AUTO_EXTRACTED_MEMORY != ACTIVE_HIGH_INFLUENCE_MEMORY
```

Fehrest must preserve stronger admission, receipt, provenance and retry/fencing rules even if a donor surface is simpler.

### 4.4 Rights gate

WeKnora is MIT at repository root, but its license file records third-party components under other licenses. Any future code adaptation requires a file-level provenance record and verification that the relevant file is actually covered by the intended license.

## 5. SkillHone qualification

### 5.1 High-value concepts

SkillHone's most relevant contribution is not a specific model. It is the development/evolution loop:

```text
failure / probe
-> diagnosis
-> candidate whole-skill revision
-> held-out evaluation
-> regression gate
-> issue / branch / PR / merge evidence
-> persistent decision history
```

The reviewed project emphasizes whole-skill-folder optimization (`SKILL.md`, scripts, references and assets), Git-native observability, role separation, and an eval/skill repository split enforced by code paths/filesystem permissions rather than prompt convention.

### 5.2 Fehrest mapping

| Capability | Target owner/gate | Disposition |
|---|---|---|
| Persistent decision history | 021 extension/skill lifecycle; evidence only | `ADAPT-PATTERN` |
| Whole-skill artifact evolution | 021 | `STUDY + BENCHMARK` |
| Held-out eval isolation | 021 benchmark/security requirement | `ADAPT-PATTERN` |
| Regression-gated skill changes | 021 | `ADAPT-PATTERN` |
| Forge-style audit surface | GitHub/hosted surfaces, potentially 022 | `STUDY` |
| Automatic skill optimization | 021 only after explicit authorization/security gates | `DEFER` |

### 5.3 Hard boundaries

```text
OPTIMIZER_OUTPUT != AUTHORIZED_CHANGE
EVAL_PASS != PRODUCT_AUTHORITY
DECISION_HISTORY != CANONICAL_MEMORY
TRAJECTORY != MEMORY
SKILL_REPO != EVAL_REPO
HELD_OUT_PROBE != MODEL_VISIBLE_OPTIMIZATION_CONTEXT
AUTO_EVOLUTION != AUTO_MERGE
```

A future Fehrest skill optimizer must never gain canonical or grant authority merely because it improved a score.

## 6. Comparative priority

Priority means research value, not implementation order:

```text
P1 = RoMem temporal-memory comparator value
P2 = WeKnora memory/authority/sandbox/product-system patterns
P3 = SkillHone eval-isolation and skill-evolution methodology
```

The sources should strengthen Fehrest by forcing sharper contracts, not by increasing feature count.

## 7. Benchmark hypotheses created by this review

Future authorized benchmark work should consider these preregistered-style hypotheses rather than donor popularity:

1. **Temporal ranking hypothesis:** a derived temporal reranker materially improves historical/as-of correctness over explicit canonical temporal filtering plus strong lexical/structured retrieval.
2. **Memory residency hypothesis:** resident profile context plus on-demand situational recall improves continuation quality at lower token/privacy cost than injecting all durable memory.
3. **Promotion-safety hypothesis:** type/risk-specific confirmation reduces false durable-memory promotion without unacceptable review friction.
4. **Revision-integrity hypothesis:** editing a user-facing retrieval/wiki surface never creates hidden canonical divergence and deterministic re-derivation reproduces the visible state.
5. **Execution-safety hypothesis:** capability-bound sandbox execution with durable attempt/receipt/fencing evidence prevents unsafe retry and scope widening under failure.
6. **Skill-evolution hypothesis:** whole-folder optimization with held-out evaluation improves skill outcomes without eval leakage or regression compared with prompt-only rewriting.

Every hypothesis needs a strong simple baseline and kill criterion before implementation.

## 8. Current decision

```text
SOURCE_QUALIFICATION_COMPLETE=YES
DEPENDENCY_ADMISSION=NO
PRODUCT_IMPLEMENTATION_AUTHORIZED=NO
R1_CHANGED=NO
R1_REVIEW_CANDIDATE_CHANGED=NO
ROMEM_CODE_REUSE_AUTHORIZED=NO
WEKNORA_CODE_REUSE_AUTHORIZED=NO
SKILLHONE_CODE_REUSE_AUTHORIZED=NO
```
