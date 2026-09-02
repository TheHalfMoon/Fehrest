# R1 — preregistration v2 (ceiling-effect successor)

```text
PREREGISTRATION_VERSION:             R1-PREREG-v2
PRECEDES:                            R1-PREREG-v1.1 (ceiling effect → UNDERPOWERED)
R1_V2_PRIOR_EVIDENCE:                ceiling effect in R1-v1 variance pilot
MODEL_RUNS_OBSERVED_AT_AMENDMENT:    0
VALID_RUNS_OBSERVED_AT_AMENDMENT:   0
SCORING_STATUS:                      NOT_STARTED
PRODUCT_THESIS_STATUS:               NOT_EVALUATED
CONFIRMATORY_STATUS:                 NOT_STARTED
```

This is not a rewrite of preregistration v1. The v1 and v1.1 documents, their digests, and the ceiling-effect finding remain historical evidence. This preregistration was written before any R1-v2 model request, response, pilot score, variance estimate, power analysis, or confirmatory run existed.

## 1. Why a successor preregistration is required

The R1-v1 variance pilot revealed a **ceiling effect**: all six arms achieved perfect continuation correctness (120/120) across all 30 tasks. The mechanical power-analysis rule correctly identified that the study cannot be powered for the preregistered effect size δ=0.15 because there is no variance to detect.

The ceiling effect is a legitimate scientific finding, but it means the R1-v1 benchmark has no discriminating power at its current difficulty level with the current model. The founder decision at the CEILING_EFFECT_ROUTING gate authorizes a new preregistration with harder task complexity:

```text
ROUTE=NEW_PREREGISTRATION
MODEL_STRATEGY=KEEP_REPRESENTATIVE_STRONG_MODEL
TASK_STRATEGY=INCREASE_DISCRIMINATING_DIFFICULTY
WEAKER_MODEL_ROUTE=NOT_SELECTED
```

## 2. Research question — unchanged

The core Fehrest product thesis is unchanged:

> When a project evolves over time, can a fresh agent continue the work more correctly with Fehrest than with strong simpler context strategies, at a justifiable total maintenance + context cost?

This is not a retrieval benchmark. It measures whether a fresh agent *continues the work correctly*, and what it costs to keep each arm's context correct while the project changes underneath it.

## 3. Design philosophy — difficulty without artificiality

The R1-v1 ceiling arose because each task could be answered from a single fact in a single document. A strong model reading the latest checkpoint's evidence could answer correctly without needing to track supersession chains, resolve conflicts, synthesize across checkpoints, or reason about maintenance lag.

R1-v2 increases difficulty through **legitimate structural complexity** that targets the failure modes Fehrest claims to solve:

| Failure mode | How R1-v2 targets it |
|---|---|
| Stale-use | Multi-layer supersession chains (A→B→C→D) where the most recent document does not contain the answer |
| Missed constraints | Constraints introduced early, tested late (>8 checkpoints), with intervening distractors |
| Scope creep | Cross-scenario precedent traps where one project's exception looks like a general rule |
| Failed approach repetition | Failed approaches revisited with new context that makes them superficially plausible again |
| Identity discontinuity | Objects renamed/moved multiple times across non-contiguous checkpoints |
| Contradiction blindness | Unresolved conflicts that must be flagged, not silently resolved |
| Abstention failure | Genuinely absent information masked by plausible-sounding distractors |
| Provenance loss | Tasks requiring specific evidence naming, with look-alike documents as traps |
| Maintenance drift | State changes across project epochs where old rules no longer apply |
| Context overflow | Dense distractor sets that crowd out relevant facts under budget constraints |

### 3.1 Difficulty dimensions — systematic evaluation

The following candidate difficulty dimensions were evaluated and incorporated:

| Dimension | Incorporated | Mechanism |
|---|---|---|
| Longer temporal distance | YES | 15 checkpoints per scenario; tasks at T12-T14 depend on T2-T4 facts |
| Larger distractor sets | YES | 3-5 distractor documents per relevant doc per checkpoint |
| Conflicting and superseded facts | YES | Multi-layer supersession chains (up to 4 levels) |
| Multiple plausible-but-stale answers | YES | Superseded facts remain findable and superficially correct |
| Cross-file and cross-session dependencies | YES | Tasks requiring synthesis across 3+ checkpoints |
| Multi-hop continuation requirements | YES | Tasks requiring chains of reasoning (A→B→C→answer) |
| Hidden dependency chains | YES | Early "minor" constraints become critical 8+ checkpoints later |
| Delayed constraints | YES | Constraints introduced at T2-T4, tested at T12-T14 |
| Partial failures and recovery state | YES | Checkpoints with partial fixes and residual constraints |
| State changes across maintenance epochs | YES | Project eras with different rule sets |
| Provenance-sensitive answers | YES | Tasks requiring specific evidence naming |
| Negative/absent-information cases | YES | Genuinely absent information with plausible distractors |
| Scope and authorization constraints | YES | Cross-project precedent traps |
| Tasks where simple baseline is competitive | YES | 6+ tasks where B0/B4 can genuinely win |
| Tighter context budgets | OPTIONAL | Secondary 4,000-byte tier for sensitivity analysis |
| Realistic continuation work | YES | Repository/project continuation, not trivia retrieval |

## 4. Corpus — three evolving projects, extended

| Scenario | Domain | Checkpoints | Evidence items | Tasks |
|---|---|---|---|---|
| **S1 Beacon** | Telemetry ingestion service | 15 (t0–t14, days 0–105) | 18 | 12 |
| **S2 Marisol** | Clinical-trial data pipeline | 15 (t0–t14, days 0–120) | 14 | 10 |
| **S3 Harbor** | Documentation migration | 15 (t0–t14, days 0–108) | 12 | 8 |

Each scenario evolves through timestamped checkpoints carrying the phenomena a long-running project produces: initial requirements · later requirements · superseded decisions · project-local exceptions · organisation-wide defaults · failed experiments · corrected failures · renames and moves · conflicting notes · genuinely unresolved conflicts · completed work · current open work · historical states · known gotchas · irrelevant noise · stale summaries · trustworthy current evidence.

### 3.1 Three epochs per scenario

Each scenario is divided into three epochs:

| Epoch | Checkpoints | Character |
|---|---|---|
| **Foundation** | t0–t4 | Initial requirements, early constraints, first decisions |
| **Growth** | t5–t9 | Scaling challenges, reversals, new constraints, failed experiments |
| **Maturity** | t10–t14 | Migration, deprecation, legacy state, cross-project interactions |

State introduced in earlier epochs may be modified, superseded, or deprecated in later epochs. Old facts remain findable. Some are still valid; some are traps.

### 3.2 Distractor density

Each checkpoint introduces:
- 1-2 **relevant** documents (containing facts needed for future tasks)
- 3-5 **distractor** documents (plausible, on-topic, but irrelevant or misleading)
- 1-2 **trap** documents (containing superseded or contradicted facts presented as current)

Distractors share keywords, document naming conventions, and structural patterns with relevant documents. They are not adversarial — they are the natural noise of a real project.

## 5. Tasks — 30 continuation tasks across 13 classes

### 5.1 Task classes

| Class | Tasks | What it isolates | R1-v2 addition |
|---|---|---|---|
| `NEXT_ACTION` | 3 | Selecting the correct next step from a long history | Unchanged |
| `SUPERSESSION_AVOIDANCE` | 3 | Not acting on a decision that has been replaced | Multi-layer chains |
| `CONSTRAINT_RETENTION` | 3 | Honouring a requirement introduced many checkpoints earlier | Delayed constraints (span >8) |
| `FAILED_APPROACH_AVOIDANCE` | 3 | Not repeating a known failed approach | Revisited with new context |
| `SCOPE_RESOLUTION` | 2 | Applying a project-local rule without globalising it | Cross-scenario precedent |
| `CONTRADICTION_HANDLING` | 3 | Surfacing a conflict instead of silently picking | Unresolved conflicts |
| `HISTORICAL_REASONING` | 3 | Operating under what was true at an earlier point | Unchanged |
| `IDENTITY_CONTINUITY` | 3 | Following an object across rename and move | Multiple renames |
| `ABSTENTION` | 2 | Declining to invent an answer that does not exist | Masked absence |
| `PROVENANCE` | 1 | Naming the evidence an action requires | Look-alike documents |
| `CROSS_FILE_SYNTHESIS` | 2 | **NEW**: Synthesizing facts from 3+ checkpoints | R1-v2 addition |
| `EPOCH_BOUNDARY` | 2 | **NEW**: Reasoning across project eras | R1-v2 addition |

### 5.2 Tasks span the full timeline

**12 of the 30 tasks are issued before their scenario ends**, at t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12.

This tests maintenance lag, staleness, and knowledge decay across the full project lifecycle. The harness asserts that tasks are distributed across at least 8 distinct checkpoints.

### 5.3 Paired tasks in opposite directions

| Pair | Same question, opposite correct answer |
|---|---|
| S1-B (t14) / S1-G (t14, as of day 14) | Broker is Redpanda now; was Kafka then (4-level supersession) |
| S2-B (t14) / S2-G (t14, as of day 30) | Partition key is protocol now; was site then (3-level supersession) |
| S1-L (t4) / S1-B (t14) | Same answer at the moment of change and ten checkpoints later |
| S3-H (t6) / S3-D (t14) | Same constraint, tested for freshness then for retention (span=8) |
| S1-E (t14) / S1-M (t9) | Refuse to export a local exception; refuse to globalise it (cross-scenario) |
| S2-E (t14) / S2-M (t9) | Cross-scenario precedent: S1 rule does not apply to S2 |
| S1-N (t12) / S2-N (t12) | Cross-file synthesis: combine facts from S1 and S2 |

### 5.4 Multi-hop continuation chains

| Chain | Hops | Description |
|---|---|---|
| S1-CHAIN-1 | 3 | Constraint at T2 → modifies decision at T6 → determines valid action at T12 |
| S1-CHAIN-2 | 4 | Failure at T3 → partial fix at T7 → new constraint at T9 → answer at T14 |
| S2-CHAIN-1 | 3 | Requirement at T1 → superseded at T5 → exception at T8 → answer at T13 |
| S3-CHAIN-1 | 3 | Scope rule at T2 → cross-project question at T8 → answer at T14 |

### 5.5 Task identities (frozen)

The following 30 task identities are frozen. Full prompts and oracles are in `tasks/tasks-v2.json` and `oracles/oracles-v2.json`.

| Task ID | Scenario | Checkpoint | Class | Temporal span | Hops | Epoch boundary |
|---|---|---|---|---|---|---|
| S1-A-NEXT | S1 | 14 | NEXT_ACTION | 14 | 1 | YES |
| S1-B-SUPERSESSION | S1 | 14 | SUPERSESSION_AVOIDANCE | 14 | 4 | YES |
| S1-C-CONSTRAINT | S1 | 14 | CONSTRAINT_RETENTION | 12 | 1 | YES |
| S1-D-FAILED | S1 | 14 | FAILED_APPROACH_AVOIDANCE | 11 | 2 | YES |
| S1-E-SCOPE | S1 | 14 | SCOPE_RESOLUTION | 14 | 2 | YES |
| S1-F-CONTRADICTION | S1 | 14 | CONTRADICTION_HANDLING | 14 | 3 | YES |
| S1-G-HISTORICAL | S1 | 14 | HISTORICAL_REASONING | 14 | 1 | YES |
| S1-H-IDENTITY | S1 | 14 | IDENTITY_CONTINUITY | 14 | 3 | YES |
| S1-I-ABSENT | S1 | 14 | ABSTENTION | 14 | 1 | YES |
| S1-J-PROVENANCE | S1 | 14 | PROVENANCE | 14 | 2 | YES |
| S1-K-CROSS-SYNTHESIS | S1 | 12 | CROSS_FILE_SYNTHESIS | 10 | 3 | YES |
| S1-L-EPOCH | S1 | 14 | EPOCH_BOUNDARY | 14 | 2 | YES |
| S2-A-NEXT | S2 | 14 | NEXT_ACTION | 14 | 1 | YES |
| S2-B-SUPERSESSION | S2 | 14 | SUPERSESSION_AVOIDANCE | 14 | 3 | YES |
| S2-C-CONSTRAINT | S2 | 14 | CONSTRAINT_RETENTION | 13 | 1 | YES |
| S2-D-FAILED | S2 | 14 | FAILED_APPROACH_AVOIDANCE | 10 | 2 | YES |
| S2-E-SCOPE | S2 | 14 | SCOPE_RESOLUTION | 14 | 2 | YES |
| S2-F-CONTRADICTION | S2 | 14 | CONTRADICTION_HANDLING | 14 | 2 | YES |
| S2-G-HISTORICAL | S2 | 14 | HISTORICAL_REASONING | 14 | 1 | YES |
| S2-H-IDENTITY | S2 | 14 | IDENTITY_CONTINUITY | 14 | 2 | YES |
| S2-I-ABSENT | S2 | 14 | ABSTENTION | 14 | 1 | YES |
| S2-K-CROSS-SYNTHESIS | S2 | 12 | CROSS_FILE_SYNTHESIS | 8 | 3 | YES |
| S3-A-NEXT | S3 | 14 | NEXT_ACTION | 14 | 1 | YES |
| S3-B-SUPERSESSION | S3 | 14 | SUPERSESSION_AVOIDANCE | 14 | 3 | YES |
| S3-C-CONSTRAINT | S3 | 14 | CONSTRAINT_RETENTION | 8 | 1 | NO |
| S3-D-FAILED | S3 | 14 | FAILED_APPROACH_AVOIDANCE | 14 | 2 | YES |
| S3-F-CONTRADICTION | S3 | 14 | CONTRADICTION_HANDLING | 14 | 2 | YES |
| S3-G-HISTORICAL | S3 | 14 | HISTORICAL_REASONING | 14 | 1 | YES |
| S3-H-IDENTITY | S3 | 14 | IDENTITY_CONTINUITY | 14 | 2 | YES |
| S3-L-EPOCH | S3 | 14 | EPOCH_BOUNDARY | 14 | 2 | YES |

## 6. Arms — preserved from R1-v1

Every arm receives the same **6,000-byte** context budget. No arm gets more room.

| Arm | Construction | Maintained |
|---|---|---|
| **B-NULL** | Task prompt only, no project context. **Calibration, not a comparison arm** | no |
| **B0** | Plain project files, **newest checkpoint first**, cut at budget | no |
| **B1** | Repository-native state documents, then the project files underneath | **yes** |
| **B3** | Lexical retrieval through the real FTS index, ranked by distinct term hits, recency-tiebroken. Raw document text only | no |
| **B4** | The maintained wiki page, and nothing else | **yes** |
| **B5** | Fehrest compiled context package at the checkpoint's valid time | **yes** |

### 6.1 Strong simple baselines preserved

B0, B1, B3, and B4 are **not weakened** because they performed well in R1-v1. They remain the same construction. If B4 gives essentially the same continuation quality at lower complexity and reasonable maintenance cost, that is evidence against the current Fehrest thesis, and it gets reported as evidence against.

### 6.2 Secondary context budget tier (optional)

A secondary context budget tier at **4,000 bytes** is optionally available for sensitivity analysis. This tier is used only for post-hoc analysis of budget sensitivity, not for the primary comparison. The primary comparison uses 6,000 bytes.

## 7. Maintenance — same three properties

Specified in full in `MAINTENANCE-V2.md`. The three properties that matter:

1. **Same evidence, same time.** At each checkpoint every maintained arm's maintainer receives the identical new-evidence bundle, and nothing from the future.
2. **Task-blind.** The maintainer never sees a task, never learns which facts will be scored, and is never told that anything will matter later.
3. **Counted.** Actions, objects touched, input bytes, output bytes and model tokens are recorded per checkpoint per arm.

### 7.1 Maintenance across epochs

When a scenario transitions between epochs, the maintainer receives an "epoch transition" evidence bundle documenting:
- Which prior decisions remain valid
- Which prior decisions are deprecated (but still findable)
- New epoch-specific rules

The maintainer must track this. Deprecated-but-findable facts are traps.

## 8. Primary outcome — unchanged

**`CONTINUATION_CORRECT`**, binary per task, defined before any result exists:

```
substantive := non-whitespace length of ACTION >= min_action_chars
require_ok  := every require_all entry matches its named output field
forbid_ok   := no forbid entry matches its named output field
abstain_ok  := ABSTAIN == YES  if the task is an abstention task
               ABSTAIN != YES  otherwise

CONTINUATION_CORRECT := substantive && require_ok && forbid_ok && abstain_ok
```

### 8.1 Silence earns nothing

- An empty response parses to empty fields, so `substantive` is false and the score is 0 on every task type.
- Abstention credit requires an explicit `ABSTAIN: YES` **and** a substantive `ACTION`. A bare `ABSTAIN: YES` scores 0.
- Prose that ignores the output contract scores 0.

## 9. Secondary outcomes — expanded

Tracked separately and **never folded into the primary**:

`STALE_USE` · `FALSE_ABSTENTION` · `MISSED_ABSTENTION` · `CONFLICT_FLAGGED` · `PROVENANCE_GIVEN` · `CROSS_FILE_SYNTHESIS_CORRECT` · `EPOCH_BOUNDARY_CORRECT` · historical correctness · latency · maintenance cost.

**No composite score is computed.** A weighting was not preregistered, and inventing one after seeing results is precisely what the protocol exists to prevent.

## 10. Cost

| Measured | Where |
|---|---|
| `MODEL_INPUT_TOKENS`, `MODEL_OUTPUT_TOKENS` | Per run, from the runner |
| `CONTEXT_BYTES`, `CONTEXT_ITEMS` | Per arm per checkpoint, from the harness |
| `COMPILE_LATENCY` | Release binary only, target path recorded |
| `MAINTENANCE_*` | Per checkpoint per arm, see `MAINTENANCE-V2.md` |
| `STORAGE_GROWTH` | Arm artefact bytes over checkpoints |

**No accuracy figure for B5 may be reported without its cost alongside it.**

## 11. Model condition — frozen

| Parameter | Value |
|---|---|
| **Model** | `gpt-5.6-terra` (same as R1-v1.1 replacement) |
| **Reasoning effort** | `medium` |
| **Temperature** | `0.0` |
| **Max output** | `1024` tokens |
| **Tool set** | `[]` (no tools) |

A stronger model than B5 for the baselines invalidates the batch. So does a weaker one. The same model condition is used for every primary-arm run and every maintainer session.

If the provider exposes only a floating alias, that is recorded as `MODEL_VERSION_PIN_STATUS=UNAVAILABLE_FLOATING_ALIAS` and the model string the provider reports per response is recorded per run.

## 12. Runner — same admissibility

A runner is admissible only if all of:

1. **Fresh independent executions.** Every continuation run starts a new session with no memory of any prior task, prior arm, or prior repeat.
2. **No conversation reuse.** Not between repeats, not between arms, not between tasks.
3. **Configuration is set by the caller**, not by a UI default.
4. **Per-run evidence is captured** to the required schema.
5. **Failures are distinguishable** — a provider timeout must not be recordable as a wrong answer.

### 12.1 Per-run record schema

Same as R1-v1. One JSON object per run, appended to `runs/<stage>/records.jsonl`.

## 13. Scorer — deterministic, arm-blind

The deterministic scorer, `fehrest-r1 score`, with arm identity stripped before adjudication. No human adjudication in the pilot.

An unparseable response is scored as it stands — normally 0 — and flagged as a candidate contract or oracle ambiguity for review. **The score is not overturned because the prose looks reasonable.**

### 13.1 V2 scorer additions

The v2 scorer adds two new oracle field types:

- `require_synthesis`: Requires that the named output field references facts from at least 2 distinct checkpoints.
- `require_epoch`: Requires that the named output field correctly identifies the epoch boundary.

## 14. Variance pilot design — frozen

| Parameter | Value |
|---|---|
| Tasks | all 30 |
| Comparison arms | B0, B1, B3, B4, B5 |
| Calibration arm | B-NULL |
| Maintenance trajectories per maintained arm | T = 2 |
| Continuation repeats per (arm, task) | r = 4 |

Resulting session counts, fixed:

```
maintenance   3 arms x 2 trajectories x 28 checkpoints  =   168 sessions
continuation  5 arms x 30 tasks x 4 repeats            =   600 runs
calibration   B-NULL x 30 tasks x 4 repeats            =   120 runs
                                              TOTAL    =   888 model sessions
```

**Stopping rule: none that depends on the data.** The pilot runs to its fixed size. The only halt condition is a runner-quality gate: if infrastructure failures exceed 10% of attempted sessions, the pilot is halted and the runner is recorded as inadmissible.

## 15. Randomization — frozen

One seed, recorded in the execution manifest **before** execution and never changed.

```
for repeat_index in 1..=4:
    for task in permute(all_30_tasks, seed, repeat_index):
        for arm in permute([B-NULL,B0,B1,B3,B4,B5], seed, repeat_index, task):
            run(arm, task, repeat_index)
```

Blocked and interleaved: every arm is exercised at every point in wall-clock time. Running all B5 trials together is prohibited.

## 16. Seed handling

The randomization seed is recorded in the execution manifest before execution and never changed. If the provider does not expose a seed, the field is `UNAVAILABLE`.

## 17. Repetition structure

- **Variance pilot:** r = 4 repeats per (arm, task)
- **Confirmatory:** r_conf computed from power analysis (see §19)
- **Maximum r_conf:** 20 (cost ceiling)
- **Minimum r_conf:** 3 (per-task variability unobservable below this)

## 18. Exclusion criteria

### 18.1 B-NULL prompt-answerable exclusion

If B-NULL scores on a task, that task is answerable from the prompt alone and is measuring nothing about context. B-NULL's result is a task-validity signal. Tasks where B-NULL scores > 0 are excluded from the primary analysis.

### 18.2 Symmetric infrastructure exclusion

If an infrastructure failure occurs for any (task, repeat) cell, that cell is excluded **for every arm symmetrically**. Selective retry of Fehrest is prohibited.

## 19. Power analysis and confirmatory-N rule — frozen

Confirmatory analysis is McNemar's exact test on paired binary outcomes.

| Parameter | Value |
|---|---|
| α (two-sided) | 0.05 |
| Target power | 0.80 |
| Minimum meaningful effect δ | 0.15 |
| `z_{1−α/2}` | 1.959964 |
| `z_{power}` | 0.841621 |

**The rule, applied mechanically:**

```
N_pairs = ceil( ( z_{1-α/2}·sqrt(ψ̂) + z_power·sqrt(ψ̂ − δ²) )² / δ² )
r_conf  = ceil( N_pairs / 30 )
```

**Safety bounds:**

| Bound | Value | Behaviour at the bound |
|---|---|---|
| `r_conf` minimum | 3 | Below this, per-task variability is unobservable. Raised to 3 |
| `r_conf` maximum | 20 | Cost ceiling |
| `N_pairs` floor | 90 | |
| `N_pairs` ceiling | 600 | |

**If the formula demands r_conf > 20, the study is declared UNDERPOWERED_FOR_PREREGISTERED_EFFECT and reported as such.**

If ψ̂ ≤ δ² the formula is undefined — that means the arms almost never disagree, which is itself the answer, and it is reported as NO_DETECTABLE_DISCORDANCE rather than patched.

## 20. Maximum cost/run bounds

| Bound | Value |
|---|---|
| Maximum model sessions (variance pilot) | 888 |
| Maximum model sessions (confirmatory, r_conf=20) | 3,000 |
| Maximum total model sessions | 3,888 |
| Maximum cost per run | Provider-dependent, recorded |
| Maximum wall time per run | 120 seconds |

## 21. Unblinding procedure

1. Arms are executed under neutral identifiers (ARM_A through ARM_F).
2. The strings "Fehrest", "wiki", and "baseline" do not appear in any model-visible prompt.
3. The arm-identity mapping lives in `runs/<stage>/arm-map.json`, withheld until scoring is complete.
4. After scoring is complete and the scoring seal is recorded, the arm-map is published.
5. Unblinding occurs in a single commit that reveals the mapping and the per-arm scores simultaneously.

## 22. Ceiling/floor handling

### 22.1 Ceiling detection

If the variance pilot reveals ψ̂ ≤ δ² (NO_DETECTABLE_DISCORDANCE), the study is reported as a ceiling effect. This is a legitimate scientific finding and is **not** interpreted as thesis support or falsification.

### 22.2 Floor detection

If all arms score near zero (floor effect), the study is reported as UNDERPOWERED_FOR_DIFFICULTY. Tasks are too hard for any arm, and the benchmark provides no useful signal.

### 22.3 Ceiling-effect response

If a ceiling effect is detected in the R1-v2 variance pilot, the response is:
1. Report as UNDERPOWERED_FOR_PREREGISTERED_EFFECT
2. Do not proceed to confirmatory
3. Report the ceiling effect as the finding
4. Founder decides on next steps (no automatic escalation)

## 23. Terminal verdict mapping

| R1-v2 verdict family | Default route |
|---|---|
| `THESIS_SUPPORTED` | Founder may authorize Spec 002 |
| `THESIS_SUPPORTED_ON_COST` | Founder may authorize Spec 002; preserve cost as a primary design constraint |
| `THESIS_SUPPORTED_ON_SAFETY` | Founder may authorize Spec 002 with stale-use/constraint safety retained as a primary acceptance dimension |
| `THESIS_SUPPORTED_WITH_COST_CAVEAT` | Do not expand expensive capabilities; require explicit founder decision and cost-reduction plan |
| `THESIS_NOT_SUPPORTED` | Trigger F-1 review. Do not begin Spec 002 by default |
| `THESIS_FAIL` | Halt product expansion and perform architecture/product reconsideration |
| `INCONCLUSIVE` | No silent continuation. Founder explicitly chooses extension, limited convergence, or stop |
| `CEILING_EFFECT` | Report as finding. Do not reinterpret as thesis support or falsification. Founder decides on next steps |
| `FLOOR_EFFECT` | Report as finding. Tasks too hard for any arm. Founder decides on next steps |

## 24. Failure routing

| Failure class | Handling |
|---|---|
| Provider timeout | Retry up to 2 times, exponential backoff. Still failing → EXCLUDED_INFRA, exclude cell for every arm |
| Rate limit | Back off, retry up to 2 times |
| Network error | Retry up to 2 times |
| Runner crash | Retry up to 2 times |
| Empty response | TASK_FAILURE. Scored as-is. No retry |
| Malformed response | TASK_FAILURE. Scored as-is. No retry |
| Refusal | TASK_FAILURE. Scored as-is, flagged |
| Context-limit exceeded | INFRASTRUCTURE_FAILURE. Runner misconfiguration |

**Selective retry of Fehrest is prohibited.** Every attempt is recorded with its attempt index.

## 25. Separation from confirmatory data

```
runs/variance-pilot-v2/     <- stage 1 output. NEVER read by confirmatory analysis
runs/confirmatory-v2/       <- stage 2 output, created only after the manifest is sealed
```

Pilot runs are not pooled, not reused as extra confirmatory observations, and not re-scored under a later rule.

## 26. Required pilot report

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

**Prohibited outputs at this stage:** `PRODUCT_THESIS_PASS`, `PRODUCT_THESIS_FAIL`, and any statement of the form "B5 beat B4". Effect estimates are reported as inputs to a power analysis, with their uncertainty, and nothing else.

## 27. Then, and only then

1. Compute r_conf mechanically from §19. No judgement, no adjustment.
2. Apply the B-NULL exclusion from §18.1.
3. Create **R1-CONFIRMATORY-v2** — a new immutable manifest carrying the computed N, the power-analysis digest, the model condition, the runner version, the corpus, task, scorer and baseline digests, the frozen Fehrest identity, the randomization seed and the execution-plan digest.
4. Seal it. **Then** run the confirmatory stage.

Confirmatory execution may not begin until both `R1_VARIANCE_PILOT_V2_COMPLETE` and `R1_CONFIRMATORY_MANIFEST_V2_SEALED` are true.

## 28. Benchmark-design review checklist

Before execution, the following checklist must be independently reviewed:

| Check | Status | Evidence |
|---|---|---|
| CONSTRUCT_VALIDITY | PENDING | Tasks measure continuation correctness, not trivia retrieval |
| DIFFICULTY_WITHOUT_ARTIFICIALITY | PENDING | Complexity from structural depth, not linguistic obscurity |
| NO_INFORMATION_LEAKAGE | PENDING | Future-evidence vocabulary check; structural vocabulary subtraction |
| NO_ARM_FAVORING | PENDING | Neutral arm identifiers; same model condition for all arms |
| BASELINE_FAIRNESS | PENDING | B0 recency-ordered; B4 maintained wiki; both unweakened |
| SCORER_VALIDITY | PENDING | Deterministic, field-scoped, arm-blind |
| ORACLE_VALIDITY | PENDING | Each oracle has derivable_from and trap_present assertions |
| CEILING_RISK | PENDING | Multi-layer supersession and cross-file synthesis reduce ceiling risk |
| FLOOR_RISK | PENDING | 6+ tasks where B0/B4 can genuinely win |
| COST_BOUND | PENDING | r_conf ≤ 20; maximum 3,888 total sessions |
| REPRODUCIBILITY | PENDING | Seeded randomization; per-run evidence capture; immutable raw output |

## 29. What Fehrest has to show

It does not need to win everything. A meaningful thesis needs evidence that the extra structure buys something material — better continuation at similar cost, similar continuation at much lower maintenance cost, better stale-decision avoidance at acceptable cost, or accuracy that holds up better as project age and churn increase.

**If B4 gives essentially the same continuation quality at lower complexity and reasonable maintenance cost, that is evidence against the current Fehrest thesis, and it gets reported as evidence against.**

No feature will be added in response to any R1-v2 result. `GRAPH=NO` `VECTORS=NO` `AUTO_MEMORY=NO` `RERANKER=NO` `MCP=NO` `UI=NO`.

## 30. Post-result modification policy

Per the immutable-evidence governance rule:

1. Raw model output is written once, digested, and never edited.
2. No manual repair of an answer before scoring, for any reason.
3. If a harness defect is discovered mid-run, the batch is invalidated.
4. Post-hoc modifications preserve originals, record SHA-256s, classify versions, and disclose.

## 31. R1-v1 ceiling-effect preservation

The R1-v1 ceiling effect is preserved as immutable prior evidence:

```text
R1_V1_CEILING_EFFECT_EVIDENCE=SHA256:d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
R1_V1_CEILING_EFFECT_COMMIT=cef01818bc178366109ef386b40a7c02330015c4
R1_V1_CEILING_EFFECT_RESULT=NO_DETECTABLE_DISCORDANCE
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
```

The failed-to-discriminate study is not overwritten, retroactively modified, rescores, or reused as confirmatory observations. It is input to the R1-v2 design, not data for tuning individual answers.
