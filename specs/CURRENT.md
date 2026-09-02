# CURRENT — Fehrest Execution Frontier

**Purpose:** one authoritative pointer for what work may happen now.

> This file is operational state, not historical evidence. Re-read live repository and R1 evidence before updating it.

## Current frontier

```text
ARCHITECTURE=FROZEN
PHASE_T_IMPLEMENTATION=TECHNICALLY_COMPLETE
PHASE_T_PRODUCT_THESIS=NOT_YET_TERMINAL
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=FOUNDER_DECISION_ON_BLINDED_PILOT_SCORING
R1_REPLACEMENT_EXECUTOR_VERSION=11
R1_REPLACEMENT_EXECUTOR_SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
R1_REPLACEMENT_V8_PREPARE_RESULT=FAIL_CLOSED_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V9_PREPARE_RESULT=PASS
R1_REPLACEMENT_V9_RUNTIME_RESULT=FAIL_CLOSED_DURING_ISOLATED_RUNTIME_BOOTSTRAP_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V10_PREPARE_RESULT=PASS
R1_REPLACEMENT_V10_RUNTIME_RESULT=UV_VENV_AND_OPENAI_3_3_0_INSTALL_PASS
R1_REPLACEMENT_V10_VERIFY_RESULT=FAIL_CLOSED_PYTHON_C_ARGUMENT_QUOTING_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V11_QUALIFICATION=RUNTIME_LOCAL_SDK_VERIFY_SCRIPT_ONLY
R1_REPLACEMENT_EXECUTION_RESULT=VALID_UNSCORED_REPLACEMENT
R1_REPLACEMENT_EXECUTION_REVIEW=PASS
BLINDED_PILOT_SCORING_AUTHORIZED=NO
SCORING_STATUS=NOT_STARTED
UNBLINDING_STATUS=NOT_STARTED
POWER_ANALYSIS_STATUS=NOT_PERFORMED
CONFIRMATORY_STATUS=NOT_STARTED
NEXT_PRODUCT_SPEC=002-post-r1-canonical-core-convergence
NEXT_PRODUCT_SPEC_STATUS=BLOCKED_BY_R1_TERMINAL_GATE_AND_FOUNDER_AUTHORIZATION
GITHUB_BOOTSTRAP_MODE=VERIFIED_SNAPSHOT_MIRROR
```

Issue #8 is closed on preserved immutable execution evidence. The V11 replacement execution completed as a valid unscored scientific execution with the disclosed wrapper/result-schema defect and post-hoc result-file augmentation explicitly excluded as scientific evidence. The raw execution archive SHA-256 is:

```text
R1_VARIANCE_PILOT_RAW_SHA256=d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
```

Issue #11 is also closed after execution-integrity review. The review recorded:

```text
EXECUTION_REVIEW=PASS
RAW_EXECUTION_EVIDENCE_ACCEPTED_FOR_BLINDED_SCORING_REVIEW=YES
SCORING_STATUS=NOT_STARTED
UNBLINDING_STATUS=NOT_STARTED
POWER_ANALYSIS_STATUS=NOT_PERFORMED
CONFIRMATORY_STATUS=NOT_STARTED
NEXT_GATE=FOUNDER_DECISION_ON_BLINDED_PILOT_SCORING
```

The valid replacement evidence remains bound to sealed R1 v1.1. The replacement arming manifest produced during the repaired launcher path is not substituted for the sealed source-batch arming-manifest identity. Issue #11 verified the inherited scientific bindings against the sealed source manifest and preserved execution evidence.

The first variance-pilot batch remains preserved as invalidated infrastructure-contaminated evidence and remains prohibited from scoring or variance use.

V8, V9, and V10 remain preserved fail-closed pre-scientific compatibility attempts. They are historical execution-path evidence only and must not be promoted into scientific observations.

Do not infer scoring authorization from Issue #8 or Issue #11 closure. A fresh founder decision at the live evidence-backed gate is still required before blinded pilot scoring may begin.

## Sealed R1 v1.1 historical anchor

The pre-GitHub local repository sealed R1 v1.1 at:

```text
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
R1_V1_1_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
R1_V1_1_PREREGISTRATION_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

GitHub was empty when it was first bootstrapped on 2026-08-28. The GitHub bootstrap commit SHA is not claimed to equal `ed79d8...`.

Treat the SHAs above as immutable historical evidence. Do not rewrite them to match the later GitHub bootstrap history. See `docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md`.

## What is authorized now

Only:

```text
founder review/decision on blinded pilot scoring
non-semantic documentation/evidence reconciliation that leaves sealed R1 semantics unchanged
repository maintenance already authorized by canonical governance
```

No blinded scoring is authorized by this file update itself.

The remaining R1 protocol order is:

```text
founder decision on blinded pilot scoring
→ blinded pilot scoring when explicitly authorized
→ power analysis
→ computed confirmatory N
→ confirmatory manifest seal
→ confirmatory execution
→ raw seal
→ blinded confirmatory scoring
→ scoring seal
→ unblind
→ terminal verdict
```

Do not skip, collapse, or reorder these gates.

## What is blocked

Until the founder explicitly authorizes blinded pilot scoring at the current gate:

```text
blinded pilot scoring                       = BLOCKED
power analysis                              = BLOCKED
confirmatory N / manifest / execution       = BLOCKED
unblinding                                  = BLOCKED
```

Until R1 reaches its terminal verdict and the founder explicitly authorizes the post-R1 route:

```text
specs/002-post-r1-canonical-core-convergence = BLOCKED
Phase 1 product expansion                    = BLOCKED
Phase 2 derived expansion                    = BLOCKED
GI-CAP / graph work                          = BLOCKED
Phase 4 memory productization                = BLOCKED
Phase 5 agent gateway / MCP                  = BLOCKED
automatic memory                             = BLOCKED
vectors                                      = BLOCKED
UI                                           = BLOCKED
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

T037 records the selected implementation baseline and durable recovery bundle. That reconciliation creates no product implementation authority while R1 remains open.

## Update rule

When this frontier changes, update this file in the same commit that records the new authorization/closeout evidence, or in the immediately following documentation-only commit.

Never point `CURRENT` at a phase whose entry criteria are not actually met.
