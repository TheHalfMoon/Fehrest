# R1-VARIANCE-PILOT-V2 — sealed protocol

```text
STAGE:                              1 of 2
CONFIRMATORY:                       NO
RESULTS_COUNTED_IN_CONFIRMATORY:    NO -- NEVER
MAY_ISSUE_PRODUCT_THESIS_VERDICT:   NO
SEALED_BEFORE_ANY_VARIANCE_DATA:    YES
STATUS:                             AWAITING A QUALIFYING RUNNER
```

The next external model run is **not** the experiment. It is the measurement of how noisy the experiment is. Everything on this page is fixed now, before any variance number exists, so that the confirmatory sample size is computed **mechanically** from a rule rather than chosen after seeing which value makes Fehrest significant.

This is the ceiling-effect successor to the R1-v1 variance pilot. The v1 pilot revealed a ceiling effect (all arms perfect, no variance to detect). This v2 pilot uses the harder R1-v2 task corpus designed to discriminate context strategies for a strong modern agent.

Nothing here changes the corpus, the tasks, the oracles, the scoring rule, the maintenance protocol or arm construction from PREREGISTRATION-V2.md. Preregistration v2 stands unmodified.

---

## 1. Purpose

| Estimates | Validates |
|---|---|
| Run-to-run variance of the primary outcome | That the runner's plumbing actually works end to end |
| Between-task heterogeneity | That maintainer sessions produce parseable, task-blind artefacts |
| Discordant-pair rate for the B5–B4 contrast | That the deterministic scorer survives real model output |
| Maintenance cost distribution | That B-NULL is measurable, so the prompt-answerable exclusion can be applied |
| Context cost distribution | Whether ceiling or floor effects exist |

**It does not test the thesis.** No `PRODUCT_THESIS_PASS` and no `PRODUCT_THESIS_FAIL` may be issued from this stage, whatever the numbers look like.

## 2. Design — frozen

| Parameter | Value | Why this value |
|---|---|---|
| Tasks | **all 30** | The paired-inversion design deliberately makes classes heterogeneous. Estimating pooled variance from a subset would assume the homogeneity the instrument is built to violate |
| Comparison arms | B0, B1, B3, B4, B5 | As preregistered |
| Calibration arm | B-NULL | Required before confirmatory, to apply the prompt-answerable exclusion |
| Maintenance trajectories per maintained arm | **T = 2** | One trajectory gives no maintenance-variance signal at all; two is the minimum that gives one |
| Continuation repeats per (arm, task) | **r = 4** | For maintained arms: 2 runs on each of the 2 trajectories |

Resulting session counts, derived from the benchmark specification:

```
maintenance   3 scenarios × 14 transitions × 3 maintained arms × 2 trajectories  =   252 sessions
continuation  5 arms × 30 tasks × 4 repeats                                  =   600 runs
calibration   1 arm × 30 tasks × 4 repeats                                   =   120 runs
                                                                  TOTAL    =   972 model sessions
```

**Stopping rule: none that depends on the data.** The pilot runs to its fixed size. The only halt condition is a runner-quality gate, defined in §7: if infrastructure failures exceed **10%** of attempted sessions, the pilot is halted and the runner is recorded as inadmissible. That is a decision about the runner, not about the results.

## 3. Randomization — frozen

One seed, recorded in the execution manifest **before** execution and never changed.

```
for repeat_index in 1..=4:                 # outer loop, so drift spreads across all arms
    for task in permute(all_30_tasks, seed, repeat_index):
        for arm in permute([B-NULL,B0,B1,B3,B4,B5], seed, repeat_index, task):
            run(arm, task, repeat_index)
```

Blocked and interleaved: every arm is exercised at every point in wall-clock time. **Running all B5 trials together is prohibited** — provider-side drift over a long run would then be perfectly confounded with the treatment.

The **realized** order is written to `runs/execution-order.jsonl` as it happens and is permanent evidence, because a planned order and an executed order are not the same thing.

## 4. Model identity — frozen

- **One model condition** for every primary-arm run. B0, B1, B3, B4 and B5 all use the same provider, identifier, snapshot, temperature, top-p, max output and reasoning setting.
- **Model:** `gpt-5.6-terra` (same as R1-v1.1 replacement), reasoning effort `medium`, temperature `0.0`, max output `1024` tokens.
- **A stronger model for B5 than for the baselines invalidates the batch.** So does a weaker one.
- If the provider exposes only a floating alias, that is recorded as `MODEL_VERSION_PIN_STATUS=UNAVAILABLE_FLOATING_ALIAS` and the model string the provider reports **per response** is recorded per run, so drift is at least detectable after the fact. It is not recorded as pinned.
- A second model is permitted later as a **separate replication**, with its own manifest. It is never pooled with the primary condition.

**Maintainer model:** the same condition as continuation, across all three maintained arms. Task-blind per MAINTENANCE-V2.md: no future checkpoints, no tasks, no oracles, no scoring targets, and no statement that anything will matter later.

### 4.1 Model identity admissibility — fail-closed

| Condition | Handling |
|---|---|
| Returned model identity missing | **INVALIDATE_BATCH** |
| Identity changes within batch | **INVALIDATE_BATCH** |
| Maintenance identity ≠ continuation identity | **INVALIDATE_BATCH** |
| Different identities across arms | **INVALIDATE_BATCH** |
| Provider alias drift | **INVALIDATE_BATCH** |
| Identity metadata malformed | **INVALIDATE_BATCH** |

## 5. Scorer — frozen

The deterministic scorer, `fehrest-r1 score`, with arm identity stripped before adjudication. **No human adjudication in the pilot.**

An unparseable response is scored as it stands — normally 0 — and flagged as a candidate contract or oracle ambiguity for review. **The score is not overturned because the prose looks reasonable.** Flagged items are reported in §9 as `ORACLE_AMBIGUITIES` and are input to a possible benchmark version bump, not a retroactive rescore.

### 5.1 V2 scorer additions

The v2 scorer adds oracle field types beyond the v1 baseline:

- `require_synthesis`: Requires that the named output field references facts from at least N distinct checkpoints (where N is specified in the oracle definition).
- `require_epoch`: Requires that the named output field correctly identifies the epoch boundary and references the specific deprecation or decision that marks the boundary.

These are **not** substring-only checks. The scorer verifies that:
- For `require_synthesis`: the response references facts from the required checkpoints, not merely mentions checkpoint names.
- For `require_epoch`: the response identifies the specific epoch boundary marker (e.g., a deprecation ID), not just self-labels an epoch.

## 6. Variance estimators — frozen

Let `x_{a,t,i} ∈ {0,1}` be the primary outcome for arm `a`, task `t`, repeat `i`.

| Quantity | Estimator |
|---|---|
| Per-cell rate | `p̂_{a,t} = mean_i x_{a,t,i}` |
| Within-task (run-to-run) variance | pooled `p̂_{a,t}(1 − p̂_{a,t})` over cells |
| Between-task heterogeneity | sample variance of `p̂_{a,t}` across `t`, within arm |
| Paired difference | `d_t = p̂_{B5,t} − p̂_{B4,t}` |
| Effect uncertainty | `SD(d)` across the 30 tasks |
| **Discordant-pair rate** | `ψ̂` = proportion of (task, repeat) pairs where exactly one of B5, B4 is correct |

`ψ̂` is the quantity that drives the sample-size formula. It is defined here, before it is observed.

## 7. Power analysis and the confirmatory-N rule — frozen

Confirmatory analysis is McNemar's exact test on paired binary outcomes, as preregistered in PREREGISTRATION-V2.md §20.

**Fixed criteria:**

| Parameter | Value |
|---|---|
| α (two-sided) | **0.05** |
| Target power | **0.80** |
| Minimum meaningful effect δ | **0.15** — unchanged from preregistration v1 §8 |
| `z_{1−α/2}` | 1.959964 |
| `z_{power}` | 0.841621 |

**Design values:**

| Parameter | Value |
|---|---|
| K_total (total tasks) | 30 |
| B_NULL_exclusion_rule | Tasks where B-NULL scores > 0 are excluded |
| K_eligible | K_total minus number of excluded tasks (computed after pilot) |
| ψ̂ (discordant-pair rate) | Proportion of (task, repeat) pairs where exactly one of B5, B4 is correct |
| Pairing unit | (task, repeat) pair |
| N_pairs formula | `ceil( (z_{1-α/2}·sqrt(ψ̂) + z_power·sqrt(ψ̂ − δ²))² / δ² )` |
| r_conf formula | `ceil( N_pairs / K_eligible )` |
| r_conf minimum | 3 |
| r_conf maximum | 20 |
| N_pairs floor | 90 |
| N_pairs ceiling | 600 |
| Minimum K_eligible | 15 (if fewer than 15 tasks remain after exclusion, study is UNDERPOWERED) |

**The rule, applied mechanically:**

```
N_pairs = ceil( (z_{1-α/2}·sqrt(ψ̂) + z_power·sqrt(ψ̂ − δ²))² / δ² )
r_conf  = ceil( N_pairs / K_eligible )     # K_eligible, not 30
```

**The divisor is K_eligible (not 30).** If B-NULL excludes tasks, the divisor shrinks accordingly.

**Safety bounds, fixed now:**

| Bound | Value | Behaviour at the bound |
|---|---|---|
| `r_conf` minimum | **3** | Below this, per-task variability is unobservable. Raised to 3 |
| `r_conf` maximum | **20** | Cost ceiling |
| `N_pairs` floor | 90 | |
| `N_pairs` ceiling | 600 | |
| `K_eligible` minimum | 15 | If K_eligible < 15, report as UNDERPOWERED |

**If the formula demands `r_conf > 20`, the study is declared `UNDERPOWERED_FOR_PREREGISTERED_EFFECT` and reported as such.** It is *not* rescued by lowering δ, by relaxing α, by dropping the harder task classes, or by switching to a one-sided test.

If `ψ̂ ≤ δ²` the formula is undefined — that means the arms almost never disagree, which is itself the answer, and it is reported as `NO_DETECTABLE_DISCORDANCE` rather than patched.

## 8. Separation from confirmatory data

```
runs/variance-pilot-v2/     <- stage 1 output. NEVER read by confirmatory analysis
runs/confirmatory-v2/       <- stage 2 output, created only after the manifest is sealed
```

Pilot runs are **not** pooled, **not** reused as extra confirmatory observations, and **not** re-scored under a later rule. The confirmatory dataset begins empty after the manifest is sealed.

## 9. Required pilot report

Reported in full, whichever way it comes out:

```
PILOT_RUN_COUNT                 RUNS_PER_ARM
VALID_RUNS                      INFRA_FAILURES              TASK_FAILURES
PER_ARM_PRIMARY_SCORE_DISTRIBUTION
PER_ARM_VARIANCE                BETWEEN_TASK_VARIANCE
PAIRWISE_EFFECT_ESTIMATES       DISCORDANT_PAIR_RATE (psi-hat)
MAINTENANCE_COST_DISTRIBUTION   CONTEXT_COST_DISTRIBUTION
CEILING_EFFECT                  FLOOR_EFFECT
SCORER_FAILURES                 ORACLE_AMBIGUITIES
B_NULL_PROMPT_ANSWERABLE_TASKS  (exclusion list, applied before confirmatory)
POWER_ANALYSIS_INPUTS           COMPUTED_CONFIRMATORY_N
```

**Prohibited outputs at this stage:** `PRODUCT_THESIS_PASS`, `PRODUCT_THESIS_FAIL`, and any statement of the form "B5 beat B4". Effect estimates are reported as *inputs to a power analysis*, with their uncertainty, and nothing else.

## 10. Then, and only then

1. Apply the B-NULL exclusion from PREREGISTRATION-V2.md §19.1. This yields K_eligible, N_pairs and r_conf.
2. Compute `r_conf` mechanically from §7. No judgement, no adjustment.
3. Create **R1-CONFIRMATORY-v2** — a new immutable manifest carrying the computed N, the power-analysis digest, the model condition, the runner version, the corpus, task, scorer and baseline digests, the frozen Fehrest identity, the randomization seed and the execution-plan digest.
4. Seal it. **Then** run the confirmatory stage.

Confirmatory execution may not begin until both `R1_VARIANCE_PILOT_V2_COMPLETE` and `R1_CONFIRMATORY_MANIFEST_V2_SEALED` are true.

## 11. V1 ceiling-effect relationship

The R1-v1 variance pilot revealed a ceiling effect. This v2 pilot uses a harder task corpus designed to discriminate context strategies. The v1 ceiling-effect finding is preserved as immutable prior evidence and is not overwritten, retroactively modified, rescore, or reused as confirmatory observations.

```text
R1_V1_CEILING_EFFECT_EVIDENCE=SHA256:d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
R1_V1_CEILING_EFFECT_COMMIT=cef01818bc178366109ef386b40a7c02330015c4
R1_V1_CEILING_EFFECT_RESULT=NO_DETECTABLE_DISCORDANCE
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
```

If this v2 pilot also reveals a ceiling effect, the response is:
1. Report as UNDERPOWERED_FOR_PREREGISTERED_EFFECT
2. Do not proceed to confirmatory
3. Report the ceiling effect as the finding
4. Founder decides on next steps (no automatic escalation)

## 12. Artifact manifest

The R1-v2 benchmark is defined by the following authoritative artifacts:

| Artifact | Path | Description |
|---|---|---|
| Benchmark spec | `bench/R1/benchmark-spec-v2.json` | Single source of truth |
| Task table | `bench/R1/tasks-v2.json` | 30 frozen tasks |
| Oracle table | `bench/R1/oracles-v2.json` | 30 frozen oracles |
| Corpus manifest | `bench/R1/corpus-manifest-v2.json` | 96 evidence objects |
| Scorer | `bench/R1/scorer.py` | Deterministic v2 scorer |
| Validator | `bench/R1/validate.py` | Machine validator |
| Tests | `bench/R1/test_scorer.py` | Scorer unit tests |

All artifacts are generated from `benchmark-spec-v2.json`. No authoritative number is manually duplicated across files.
