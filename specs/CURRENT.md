# CURRENT — Fehrest Execution Frontier

**Purpose:** one authoritative pointer for what work may happen now.

> This file is operational state, not historical evidence. Re-read live repository and R1 evidence before updating it.

## Current frontier

```text
ARCHITECTURE=FROZEN
PHASE_T_IMPLEMENTATION=TECHNICALLY_COMPLETE
PHASE_T_PRODUCT_THESIS=NOT_YET_TERMINAL
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=R1_V2_PREREGISTRATION_REBUILD_COMPLETE_AWAITING_REVIEW
R1_REPLACEMENT_EXECUTOR_VERSION=11
R1_REPLACEMENT_EXECUTOR_SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
R1_REPLACEMENT_V8_PREPARE_RESULT=FAIL_CLOSED_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V9_PREPARE_RESULT=PASS
R1_REPLACEMENT_V9_RUNTIME_RESULT=FAIL_CLOSED_DURING_ISOLATED_RUNTIME_BOOTSTRAP_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V10_PREPARE_RESULT=PASS
R1_REPLACEMENT_V10_RUNTIME_RESULT=UV_VENV_AND_OPENAI_3_3_0_INSTALL_PASS
R1_REPLACEMENT_V10_VERIFY_RESULT=FAIL_CLOSED_PYTHON_C_ARGUMENT_QUOTING_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V11_QUALIFICATION=RUNTIME_LOCAL_SDK_VERIFY_SCRIPT_ONLY
R1_REPLACEMENT_EXECUTION_RESULT=EXECUTION_COMPLETE_UNSCORED_REPLACEMENT
R1_REPLACEMENT_SCORING_RESULT=CEILING_EFFECT_NO_DETECTABLE_DISCORDANCE
CURRENT_PREREGISTRATION_CONFIRMATORY_POWER=UNAVAILABLE
NEXT_PRODUCT_SPEC=002-post-r1-canonical-core-convergence
NEXT_PRODUCT_SPEC_STATUS=BLOCKED_BY_R1_TERMINAL_GATE_AND_FOUNDER_AUTHORIZATION
GITHUB_BOOTSTRAP_MODE=VERIFIED_SNAPSHOT_MIRROR
```

The current R1 sub-gate is evidence-backed by `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK.md` plus the active V11 authority addendum `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK_V11.md`. The first variance-pilot batch is preserved as invalidated infrastructure-contaminated evidence. The valid same-protocol replacement has completed its execution and seal.

V8 failed closed during the no-API prepare gate because existing Windows-produced JSON metadata contained a UTF-8 BOM and the V8 supervisor decoded that metadata as plain `utf-8`. The observed failure occurred before credential capture and before any model call.

V9 superseded that parser defect only. On the required Windows host, V9 then proved the repaired no-API preparation path by recording `PREPARE_STATUS=PASS`, `NO_API_PREPARE_GATE=PASS`, `REPLACEMENT_MODEL_CALLS_EXECUTED=0`, incident SHA-256 `3c70cef6cc74304703e46a2135121f06b6a4aa039e366b6edab7d0ecd71063e2`, and replacement arming manifest SHA-256 `a7ae52b503d6c7b66cf03624aa78bd82b0349d5b02e9e0537b6a7985e1eff2ae`. V9 then failed closed while creating the isolated Python runtime. Its launcher preserved only the first traceback line in `FAILURE_REASON`, so the repository does **not** claim an unverified root cause. No model call started after that failure and the PowerShell environment cleared `OPENAI_API_KEY`.

V10 superseded V9 only at the launcher/runtime-bootstrap layer. `supervisor.py` remained byte-identical (`SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7`). On the required Windows host V10 proved that `uv venv` created the isolated Python 3.11.15 runtime and `uv pip` installed `openai==3.3.0`. Its final SDK import/version check then failed closed because PowerShell `Start-Process -ArgumentList` split the Python `-c` payload so Python observed bare `import`, producing `SyntaxError: invalid syntax`. This occurred before credential capture and before any model call.

V11 preserves the V10/V9 `supervisor.py` byte-for-byte and preserves the successful uv-based runtime bootstrap. V11 changes only SDK verification plumbing: it writes a runtime-local UTF-8-without-BOM `verify-openai-sdk.py` containing `import openai` and `print(openai.__version__)`, then executes that script path instead of passing Python code through `-c`. The compatibility evidence and exact authority boundary are recorded in `docs/canonical/R1_V11_RUNTIME_COMPATIBILITY.md` and `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK_V11.md`. This changes no sealed experiment input, evidence byte, model condition, seed, arm construction, corpus, task set, oracle set, scoring rule, session count, or confirmatory plan.

V11 execution completed successfully on 2026-09-02:
```text
R1_REPLACEMENT_EXECUTION_DATE=2026-09-02
R1_REPLACEMENT_EXECUTION_RESULT=EXECUTION_COMPLETE_UNSCORED_REPLACEMENT
R1_REPLACEMENT_RAW_SHA256=d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
R1_REPLACEMENT_RECORDS_COUNT=1036
R1_REPLACEMENT_OK_COUNT=747
R1_REPLACEMENT_TASK_FAILURE_COUNT=288
R1_REPLACEMENT_INFRA_FAILURE_COUNT=1
ISSUE_8_STATUS=CLOSED
ISSUE_11_STATUS=CLOSED
```

The outer operator bridge initially failed due to a schema mismatch (expected field names not in supervisor output). The result file was post-hoc augmented with 3 derived fields. The original supervisor bytes are not recoverable. The augmented result file is not accepted as scientific evidence and must not be used as a substitute for the preserved immutable evidence. All closure criteria were independently verified from immutable evidence (runner stdout, records, raw archive, execution order, seal outputs, scientific bindings). Binding verification uses the sealed source-batch arming-manifest identity `2e360072931ac2adfbdbba94da20d9198f8b24474852429545bcd14cd8653205`; the replacement arming manifest `a7ae52b503d6c7b66cf03624aa78bd82b0349d5b02e9e0537b6a7985e1eff2ae` is a distinct execution artifact and must not be conflated with that sealed source binding.

## R1-v2 preregistration rebuild status

The R1-v2 preregistration and benchmark package has been rebuilt from a single authoritative machine-readable specification (`bench/R1/benchmark-spec-v2.json`). All dependent artifacts are derived from this spec:

```text
R1_V2_SINGLE_SOURCE_OF_TRUTH=COMPLETE
R1_V2_CORPUS=COMPLETE
R1_V2_TASKS=COMPLETE
R1_V2_ORACLES=COMPLETE
R1_V2_SCORER_IMPLEMENTATION=COMPLETE
R1_V2_SCORER_TESTS=PASS
R1_V2_MACHINE_VALIDATION=PASS
R1_V2_SESSION_ARITHMETIC=DERIVED_AND_VALIDATED
R1_V2_HUMAN_DOCS_RECONCILED=YES
R1_V2_CURRENT_FRONTIER_RECONCILED=YES
```

Validation evidence:
- `python bench/R1/validate.py` exits 0
- `python bench/R1/test_scorer.py`: 20/20 tests pass (includes 4 adversarial tests)
- `python bench/R1/validate.py`: exits 0 with all validation checks including field-level canonical-derived equality and genuine mutation testing
- CI pipeline `.github/workflows/bench-r1-validation.yml` added: test-scorer, validate, canonical-equality jobs
- 30 tasks, 30 oracles, 96 evidence items generated
- 12 task classes derived from task definitions
- 12 distinct checkpoints (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t12, t14; t11 absent)
- 27 of the 30 tasks are issued before t14 for maintenance lag testing

**Pending independent review:**
```text
R1_V2_SCIENTIFIC_REVIEW=PENDING
R1_V2_STATISTICAL_REVIEW=PENDING
```

The rebuild required no new founder route decision. The existing authorized scope (`ROUTE=NEW_PREREGISTRATION`, `MODEL_STRATEGY=KEEP_REPRESENTATIVE_STRONG_MODEL`, `TASK_STRATEGY=INCREASE_DISCRIMINATING_DIFFICULTY`) covers the implementation methodology.

## Variance pilot scoring result

The blinded scoring report is recorded in `docs/canonical/R1-PILOT-SCORING-REPORT.md`:

```text
PILOT_RESULT=NO_DETECTABLE_DISCORDANCE
CEILING_EFFECT=YES
CURRENT_PREREGISTRATION_CONFIRMATORY_POWER=UNAVAILABLE
PRODUCT_THESIS_PASS=NOT_AUTHORIZED
PRODUCT_THESIS_FAIL=NOT_AUTHORIZED
```

All six arms achieved perfect continuation correctness (120/120) across all 30 tasks. The power-analysis rule correctly identifies that the study cannot be powered for the preregistered effect size δ=0.15 because there is no variance to detect.

This is a legitimate scientific finding. The ceiling effect is **not** interpreted as thesis support or thesis falsification. It means the benchmark has no discriminating power at this difficulty level with this model.

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

The founder decision on the ceiling-effect gate:

```text
ROUTE=NEW_PREREGISTRATION
MODEL_STRATEGY=KEEP_REPRESENTATIVE_STRONG_MODEL
TASK_STRATEGY=INCREASE_DISCRIMINATING_DIFFICULTY
WEAKER_MODEL_ROUTE=NOT_SELECTED
```

Authorized:
1. Design a new preregistration with harder task complexity that can discriminate context strategies for a strong modern agent.
2. Preserve the failed-to-discriminate study as immutable prior evidence. Do not overwrite, retroactively modify, rescore, or reuse the old pilot as confirmatory observations.
3. Repository-local governance, specification, design, static validation, review, CI, and sealing work for the new preregistration.
4. Strong simple baselines must be preserved. Do not weaken baselines simply to create separation.

Not authorized:
- Executing the new model experiment until the new preregistration, benchmark artifacts, manifest identities, exact model/runtime condition, and execution authority are all sealed and independently reviewed.
- Activating Spec 002 merely because the old R1 pilot was underpowered.

## What is blocked

Until the new R1 successor experiment reaches its terminal verdict and the founder explicitly authorizes the post-R1 route:

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
| `CEILING_EFFECT` | Design harder benchmark. New preregistration required. Do not reinterpret as thesis support or falsification |

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
