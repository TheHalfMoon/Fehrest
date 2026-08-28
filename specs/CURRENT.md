# CURRENT — Fehrest Execution Frontier

**Purpose:** one authoritative pointer for what work may happen now.

> This file is operational state, not historical evidence. Re-read live repository and R1 evidence before updating it.

## Current frontier

```text
ARCHITECTURE=FROZEN
PHASE_T_IMPLEMENTATION=TECHNICALLY_COMPLETE
PHASE_T_PRODUCT_THESIS=NOT_YET_TERMINAL
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
R1_REPLACEMENT_EXECUTOR_SHA256=9c53e45e41a0be5766779129a45e55aef4399d02395a1b4309e9d97114bef969
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
NEXT_PRODUCT_SPEC=002-post-r1-canonical-core-convergence
NEXT_PRODUCT_SPEC_STATUS=BLOCKED_BY_R1_TERMINAL_GATE_AND_FOUNDER_AUTHORIZATION
GITHUB_BOOTSTRAP_MODE=VERIFIED_SNAPSHOT_MIRROR
```

The current R1 sub-gate is evidence-backed by `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK.md`. The first variance-pilot batch is preserved as invalidated infrastructure-contaminated evidence. The valid same-protocol replacement has not yet produced its required execution result or raw seal.

Do not infer success from the existence of the executor.

## Sealed R1 v1.1 historical anchor

The pre-GitHub local repository sealed R1 v1.1 at:

```text
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
R1_V1_1_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
R1_V1_1_PREREGISTRATION_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

GitHub was empty when it was first bootstrapped on 2026-08-28. The connected GitHub write interface could not upload the historical Git pack while preserving arbitrary historical commit timestamps, so the GitHub bootstrap commit SHA is **not** claimed to equal `ed79d8...`.

Treat the SHAs above as immutable historical evidence. Do not rewrite them to match the later GitHub bootstrap history. See `docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md`.

## What is authorized now

Only work already authorized by the active R1 protocol and non-semantic documentation/planning that leaves R1 semantics and product behavior unchanged.

The R1 protocol owns:

```text
variance pilot
→ pilot seal
→ blinded scoring when authorized
→ power analysis
→ confirmatory N
→ confirmatory manifest seal
→ confirmatory execution
→ blinded scoring
→ unblinding
→ terminal verdict
```

The active sub-gate is the valid replacement variance-pilot execution. The replacement must retain the sealed v1.1 design, seed and model condition and must produce actual execution evidence before the frontier can advance.

## What is blocked

Until R1 reaches its terminal verdict and the founder explicitly authorizes the post-R1 route:

```text
specs/002-post-r1-canonical-core-convergence = BLOCKED
Phase 1 product expansion                  = BLOCKED
Phase 2 derived expansion                  = BLOCKED
GI-CAP / graph work                        = BLOCKED
Phase 4 memory productization              = BLOCKED
Phase 5 agent gateway / MCP                = BLOCKED
automatic memory                           = BLOCKED
vectors                                    = BLOCKED
UI                                         = BLOCKED
```

## R1 outcome routing

After the terminal verdict:

| R1 verdict family | Default route |
|---|---|
| `THESIS_SUPPORTED` | Founder may authorize Spec 002 |
| `THESIS_SUPPORTED_ON_COST` | Founder may authorize Spec 002; preserve cost as a primary design constraint |
| `THESIS_SUPPORTED_ON_SAFETY` | Founder may authorize Spec 002 with stale-use/constraint safety retained as a primary acceptance dimension |
| `THESIS_SUPPORTED_WITH_COST_CAVEAT` | Do not expand expensive capabilities; require explicit founder decision and cost-reduction plan |
| `THESIS_NOT_SUPPORTED` | Trigger F-1 review. Do not begin Spec 002 by default |
| `THESIS_FAIL` | Halt product expansion and perform architecture/product reconsideration |
| `INCONCLUSIVE` | No silent continuation. Founder explicitly chooses extension, limited convergence, or stop |

## Next Spec Kit

`specs/002-post-r1-canonical-core-convergence/`

It is deliberately present before activation so the repository contains the next planned move, but:

```text
SPECIFIED != AUTHORIZED
```

Its first remaining activation task is T038. T037 is closed with exact recovered implementation-baseline evidence; T038 cannot close before the R1 terminal verdict exists.

## Bootstrap integrity rule

Before any post-R1 product implementation begins from the GitHub mirror, reconcile the working implementation/evidence snapshot against the historical R1 anchor and record the exact source of that evidence. A GitHub bootstrap SHA must never be substituted for an old sealed SHA merely for convenience.

T037 now records the selected implementation baseline and durable recovery bundle. That reconciliation creates no product implementation authority while R1 remains open.

## Update rule

When this frontier changes, update this file in the same commit that records the new authorization/closeout evidence, or in the immediately following documentation-only commit.

Never point `CURRENT` at a phase whose entry criteria are not actually met.
