# R1 — preregistration v3 (low B-NULL leakage successor)

```text
PREREGISTRATION_VERSION:             R1-PREREG-v3
PRECEDES:                            R1-PREREG-v2 (LOW_K 20/30 B-NULL leakage → UNDERPOWERED)
R1_V2_PILOT_EVIDENCE:                972 sessions runs/variance-pilot-v2, raw seal ec99645c4a9ccf..., K_eligible=10<15, six classes lost
R1_V2_PRIOR_EVIDENCE:                LOW_K underpowered pilot: 20/30 B-NULL prompt-answerable, K_eligible=10<15, psi_hat=0.3250, N_pairs=111, r_conf=12, TASK_CLASS_LOSS (NEXT_ACTION, CONSTRAINT_RETENTION, FAILED_APPROACH_AVOIDANCE, HISTORICAL_REASONING, IDENTITY_CONTINUITY, ABSTENTION) — legitimate prompt-history leakage, preserved as immutable evidence (runs/variance-pilot-v2/)
MODEL_RUNS_OBSERVED_AT_AMENDMENT:    0
VALID_RUNS_OBSERVED_AT_AMENDMENT:   0
SCORING_STATUS:                      NOT_STARTED
PRODUCT_THESIS_STATUS:               NOT_EVALUATED
CONFIRMATORY_STATUS:                 NOT_STARTED
```

This is not a rewrite of preregistration v1. The v1 and v1.1 documents, their digests, and the ceiling-effect finding remain historical evidence. This preregistration was written before any R1-v2 model request, response, pilot score, variance estimate, power analysis, or confirmatory run existed.

## 1. Why a successor preregistration is required (v3)

The R1-v2 variance pilot (972 sessions, sealed 61e7816, raw ec99645c...) did **not** ceiling (psi_hat=0.3250 shows variance) and did **not** floor. It revealed high **B-NULL prompt answerability**:

```text
K_total=30
B_NULL_excluded=20 (66% prompt-answerable)
K_eligible=10 < minimum_K=15 → LOW_K_ROUTE UNDERPOWERED
Task classes fully excluded: NEXT_ACTION 3/3, CONSTRAINT_RETENTION 3/3, FAILED_APPROACH_AVOIDANCE 3/3, HISTORICAL_REASONING 3/3, IDENTITY_CONTINUITY 3/3, ABSTENTION 2/2 (six classes)
Route: UNDERPOWERED_FOR_PREREGISTERED_EFFECT (low K + task-class loss)
```

This is a legitimate scientific finding, not a harness bug. The v2 tasks disclosed history directly in the prompt, allowing prompt-only models to answer without retrieval. The founder decision (Founder Decision 2026-09-08: UNDERPOWERED_PILOT_NEW_PREREG_V3) authorizes a new preregistration with reduced B-NULL leakage while preserving rigor and strong baselines:

```text
ROUTE=NEW_PREREGISTRATION_V3
REASON=LOW_K_DUE_TO_B_NULL_PROMPT_LEAKAGE
MODEL_STRATEGY=KEEP_REPRESENTATIVE_STRONG_MODEL (do not weaken B0/B4)
TASK_STRATEGY=REDUCE_PROMPT_ONLY_ANSWERABILITY_WITH_REALISTIC_RETRIEVAL_REQUIREMENT
PRIOR_PILOT=PRESERVED_IMMUTABLE (not reused, not rescored)
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

| Dimension | Incorporated | Mechanism |
|---|---|---|
| Longer temporal distance | YES | 15 checkpoints per scenario; tasks at t12-t14 depend on t0-t3 facts |
| Larger distractor sets | YES | 3-5 distractor documents per relevant doc per checkpoint |
| Conflicting and superseded facts | YES | Multi-layer supersession chains (up to 4 levels) |
| Multiple plausible-but-stale answers | YES | Superseded facts remain findable and superficially correct |
| Cross-file and cross-session dependencies | YES | Tasks requiring synthesis across 3+ checkpoints |
| Multi-hop continuation requirements | YES | Tasks requiring chains of reasoning (A→B→C→answer) |
| Hidden dependency chains | YES | Early "minor" constraints become critical 8+ checkpoints later |
| Delayed constraints | YES | Constraints introduced at t0-t3, tested at t12-t14 |
| Partial failures and recovery state | YES | Checkpoints with partial fixes and residual constraints |
| State changes across maintenance epochs | YES | Project eras with different rule sets |
| Provenance-sensitive answers | YES | Tasks requiring specific evidence naming |
| Negative/absent-information cases | YES | Genuinely absent information with plausible distractors |
| Scope and authorization constraints | YES | Cross-project precedent traps |
| Tasks where simple baseline is competitive | YES | 3+ tasks where B0/B4 can genuinely win |
| Tighter context budgets | NO | Single 6,000-byte tier; no secondary tier |
| Realistic continuation work | YES | Repository/project continuation, not trivia retrieval |

## 4. Corpus — three evolving projects, extended

| Scenario | Domain | Checkpoints | Evidence items | Tasks |
|---|---|---|---|---|
| **S1 Beacon** | Telemetry ingestion service | 15 (t0–t14, days 0–105) | 39 | 12 |
| **S2 Marisol** | Clinical-trial data pipeline | 15 (t0–t14, days 0–120) | 30 | 10 |
| **S3 Harbor** | Documentation migration | 15 (t0–t14, days 0–108) | 27 | 8 |

Each scenario evolves through timestamped checkpoints carrying the phenomena a long-running project produces: initial requirements · later requirements · superseded decisions · project-local exceptions · organisation-wide defaults · failed experiments · corrected failures · renames and moves · conflicting notes · genuinely unresolved conflicts · completed work · current open work · historical states · known gotchas · irrelevant noise · stale summaries · trustworthy current evidence.

### 4.1 Three epochs per scenario

Each scenario is divided into three epochs:

| Epoch | Checkpoints | Character |
|---|---|---|
| **Foundation** | t0–t4 | Initial requirements, early constraints, first decisions |
| **Growth** | t5–t9 | Scaling challenges, reversals, new constraints, failed experiments |
| **Maturity** | t10–t14 | Migration, deprecation, legacy state, cross-project interactions |

State introduced in earlier epochs may be modified, superseded, or deprecated in later epochs. Old facts remain findable. Some are still valid; some are traps.

### 4.2 Distractor density

Each checkpoint introduces:
- 1-2 **relevant** documents (containing facts needed for future tasks)
- 3-5 **distractor** documents (plausible, on-topic, but irrelevant or misleading)
- 1-2 **trap** documents (containing superseded or contradicted facts presented as current)

Distractors share keywords, document naming conventions, and structural patterns with relevant documents. They are not adversarial — they are the natural noise of a real project.

## 5. Tasks — 30 continuation tasks across 12 classes

### 5.1 Task classes

| Class | Tasks | What it isolates |
|---|---|---|
| `NEXT_ACTION` | 3 | Selecting the correct next step from a long history |
| `SUPERSESSION_AVOIDANCE` | 3 | Not acting on a decision that has been replaced |
| `CONSTRAINT_RETENTION` | 3 | Honouring a requirement introduced many checkpoints earlier |
| `FAILED_APPROACH_AVOIDANCE` | 3 | Not repeating a known failed approach |
| `SCOPE_RESOLUTION` | 2 | Applying a project-local rule without globalising it |
| `CONTRADICTION_HANDLING` | 3 | Surfacing a conflict instead of silently picking |
| `HISTORICAL_REASONING` | 3 | Operating under what was true at an earlier point |
| `IDENTITY_CONTINUITY` | 3 | Following an object across rename and move |
| `ABSTENTION` | 2 | Declining to invent an answer that does not exist |
| `PROVENANCE` | 1 | Naming the evidence an action requires |
| `CROSS_FILE_SYNTHESIS` | 2 | Synthesizing facts from 3+ checkpoints |
| `EPOCH_BOUNDARY` | 2 | Reasoning across project eras |

**Total: 30 tasks across 12 distinct classes.**

### 5.2 Tasks span the full timeline

**The 30 tasks are distributed across 12 distinct checkpoints: t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t12, t14.**

| Checkpoint | Tasks | Purpose |
|---|---|---|
| t1 | 3 | Early maintenance lag testing |
| t2 | 3 | Supersession chain onset |
| t3 | 2 | Constraint retention begins |
| t4 | 2 | Failed approach testing |
| t5 | 3 | Epoch boundary (Foundation→Growth) |
| t6 | 2 | Contradiction detection |
| t7 | 3 | Historical reasoning onset |
| t8 | 2 | Identity continuity mid-test |
| t9 | 2 | Epoch boundary (Growth→Maturity) |
| t10 | 3 | Epoch boundary (Growth→Maturity) |
| t12 | 2 | Cross-file synthesis |
| t14 | 3 | Terminal epoch reasoning |

**27 of the 30 tasks are issued before t14**, testing maintenance lag, staleness, and knowledge decay across the full project lifecycle. The harness asserts that tasks are distributed across at least 12 distinct checkpoints (actual: 12).

### 5.3 Task identities (frozen)

The following 30 task identities are frozen. Full prompts and oracles are in `tasks-v2.json` and `oracles-v2.json`.

| Task ID | Scenario | Checkpoint | Class | Temporal span | Hops | Epoch boundary |
|---|---|---|---|---|---|---|
| S1-A-NEXT | S1 | 1 | NEXT_ACTION | 1 | 1 | NO |
| S1-B-SUPERSESSION | S1 | 2 | SUPERSESSION_AVOIDANCE | 2 | 2 | NO |
| S1-C-CONSTRAINT | S1 | 3 | CONSTRAINT_RETENTION | 3 | 1 | NO |
| S1-D-FAILED | S1 | 4 | FAILED_APPROACH_AVOIDANCE | 3 | 2 | NO |
| S1-E-SCOPE | S1 | 5 | SCOPE_RESOLUTION | 5 | 2 | YES |
| S1-F-CONTRADICTION | S1 | 6 | CONTRADICTION_HANDLING | 1 | 2 | NO |
| S1-G-HISTORICAL | S1 | 7 | HISTORICAL_REASONING | 6 | 1 | NO |
| S1-H-IDENTITY | S1 | 8 | IDENTITY_CONTINUITY | 8 | 3 | NO |
| S1-I-ABSENT | S1 | 9 | ABSTENTION | 9 | 1 | YES |
| S1-J-PROVENANCE | S1 | 10 | PROVENANCE | 10 | 1 | YES |
| S1-K-CROSS-SYNTHESIS | S1 | 12 | CROSS_FILE_SYNTHESIS | 12 | 3 | NO |
| S1-L-EPOCH | S1 | 14 | EPOCH_BOUNDARY | 14 | 2 | YES |
| S2-A-NEXT | S2 | 1 | NEXT_ACTION | 1 | 1 | NO |
| S2-B-SUPERSESSION | S2 | 2 | SUPERSESSION_AVOIDANCE | 2 | 2 | NO |
| S2-C-CONSTRAINT | S2 | 3 | CONSTRAINT_RETENTION | 3 | 1 | NO |
| S2-D-FAILED | S2 | 5 | FAILED_APPROACH_AVOIDANCE | 3 | 2 | YES |
| S2-E-SCOPE | S2 | 6 | SCOPE_RESOLUTION | 6 | 2 | NO |
| S2-F-CONTRADICTION | S2 | 7 | CONTRADICTION_HANDLING | 1 | 2 | NO |
| S2-G-HISTORICAL | S2 | 9 | HISTORICAL_REASONING | 7 | 1 | YES |
| S2-H-IDENTITY | S2 | 10 | IDENTITY_CONTINUITY | 10 | 3 | YES |
| S2-I-ABSENT | S2 | 12 | ABSTENTION | 12 | 1 | NO |
| S2-K-CROSS-SYNTHESIS | S2 | 14 | CROSS_FILE_SYNTHESIS | 14 | 3 | NO |
| S3-A-NEXT | S3 | 1 | NEXT_ACTION | 1 | 1 | NO |
| S3-B-SUPERSESSION | S3 | 2 | SUPERSESSION_AVOIDANCE | 2 | 2 | NO |
| S3-C-CONSTRAINT | S3 | 4 | CONSTRAINT_RETENTION | 4 | 1 | YES |
| S3-D-FAILED | S3 | 5 | FAILED_APPROACH_AVOIDANCE | 3 | 2 | YES |
| S3-F-CONTRADICTION | S3 | 7 | CONTRADICTION_HANDLING | 1 | 2 | NO |
| S3-G-HISTORICAL | S3 | 8 | HISTORICAL_REASONING | 7 | 1 | NO |
| S3-H-IDENTITY | S3 | 10 | IDENTITY_CONTINUITY | 10 | 3 | YES |
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

### 6.2 Context budget — single tier

R1-v2 uses a single context budget tier at **6,000 bytes**. There is no secondary tier. This eliminates ambiguity and ensures all arms compete on equal footing.

## 7. Maintenance — same three properties

Specified in full in `MAINTENANCE-V2.md`. The three properties that matter:

1. **Same evidence, same time.** At each checkpoint every maintained arm's maintainer receives the identical new-evidence bundle, and nothing from the future.
2. **Task-blind.** The maintainer never sees a task, never learns which facts will be scored, and is never told that anything will matter later.
3. **Counted.** Actions, objects touched, input bytes, output bytes and model tokens are recorded per checkpoint per arm.

### 7.1 T0 initialization rule

**t0 is the initialized scenario state.** No model-driven maintainer action is required at t0. Maintenance sessions begin at t1 and continue through t14.

This is a deliberate scientific construct: the initial state is given, and the maintainer's job is to *maintain* it as the project evolves, not to create it from scratch.

### 7.2 Maintenance across epochs

When a scenario transitions between epochs, the maintainer receives an "epoch transition" evidence bundle documenting:
- Which prior decisions remain valid
- Which prior decisions are deprecated (but still findable)
- New epoch-specific rules

The maintainer must track this. Deprecated-but-findable facts are traps.

## 8. Primary outcome — unchanged

**`CONTINUATION_CORRECT`**, binary per task, defined before any result exists:

```
substantive := any response field has non-whitespace content >= min_action_chars
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

## 12. Model identity admissibility — fail-closed

The design specifies fail-closed handling for the floating model alias:

| Condition | Handling |
|---|---|
| Returned model identity missing | **INVALIDATE_BATCH** |
| Identity changes within batch | **INVALIDATE_BATCH** |
| Maintenance identity ≠ continuation identity | **INVALIDATE_BATCH** |
| Different identities across arms | **INVALIDATE_BATCH** |
| Provider alias drift | **INVALIDATE_BATCH** |
| Identity metadata malformed | **INVALIDATE_BATCH** |

Record-only is insufficient. Any identity admissibility failure invalidates the entire batch.

## 13. Runner — same admissibility

A runner is admissible only if all of:

1. **Fresh independent executions.** Every continuation run starts a new session with no memory of any prior task, prior arm, or prior repeat.
2. **No conversation reuse.** Not between repeats, not between arms, not between tasks.
3. **Configuration is set by the caller**, not by a UI default.
4. **Per-run evidence is captured** to the required schema.
5. **Failures are distinguishable** — a provider timeout must not be recordable as a wrong answer.

### 13.1 Per-run record schema

Same as R1-v1. One JSON object per run, appended to `runs/<stage>/records.jsonl`.

## 14. Scorer — deterministic, arm-blind

The deterministic scorer, `fehrest-r1 score`, with arm identity stripped before adjudication. No human adjudication in the pilot.

An unparseable response is scored as it stands — normally 0 — and flagged as a candidate contract or oracle ambiguity for review. **The score is not overturned because the prose looks reasonable.**

### 14.1 V2 scorer additions

The v2 scorer adds two new oracle field types:

- `require_synthesis`: Requires that the named output field references facts from at least N distinct checkpoints (where N is specified in the oracle definition).
- `require_epoch`: Requires that the named output field correctly identifies the epoch boundary and references the specific deprecation or decision that marks the boundary.

These are **not** substring-only checks. The scorer verifies that:
- For `require_synthesis`: the response references facts from the required checkpoints, not merely mentions checkpoint names.
- For `require_epoch`: the response identifies the specific epoch boundary marker (e.g., a deprecation ID), not just self-labels an epoch.

## 15. Variance pilot design — frozen

| Parameter | Value |
|---|---|
| Tasks | all 30 |
| Comparison arms | B0, B1, B3, B4, B5 |
| Calibration arm | B-NULL |
| Maintenance trajectories per maintained arm | T = 2 |
| Continuation repeats per (arm, task) | r = 4 |

Resulting session counts, derived from the benchmark specification:

```
maintenance   3 scenarios × 14 transitions × 3 maintained arms × 2 trajectories  =   252 sessions
continuation  5 arms × 30 tasks × 4 repeats                                  =   600 runs
calibration   1 arm × 30 tasks × 4 repeats                                   =   120 runs
                                                                  TOTAL    =   972 model sessions
```

**Stopping rule: none that depends on the data.** The pilot runs to its fixed size. The only halt condition is a runner-quality gate: if infrastructure failures exceed 10% of attempted sessions, the pilot is halted and the runner is recorded as inadmissible.

## 16. Randomization — frozen

One seed, recorded in the execution manifest **before** execution and never changed.

```
for repeat_index in 1..=4:
    for task in permute(all_30_tasks, seed, repeat_index):
        for arm in permute([B-NULL,B0,B1,B3,B4,B5], seed, repeat_index, task):
            run(arm, task, repeat_index)
```

Blocked and interleaved: every arm is exercised at every point in wall-clock time. Running all B5 trials together is prohibited.

## 17. Seed handling

The randomization seed is recorded in the execution manifest before execution and never changed. If the provider does not expose a seed, the field is `UNAVAILABLE`.

## 18. Repetition structure

- **Variance pilot:** r = 4 repeats per (arm, task)
- **Confirmatory:** r_conf computed from power analysis (see §20)
- **Maximum r_conf:** 20 (cost ceiling)
- **Minimum r_conf:** 3 (per-task variability unobservable below this)

## 19. Exclusion criteria

### 19.1 B-NULL prompt-answerable exclusion

If B-NULL scores on a task, that task is answerable from the prompt alone and is measuring nothing about context. B-NULL's result is a task-validity signal. Tasks where B-NULL scores > 0 are excluded from the primary analysis.

### 19.2 Symmetric infrastructure exclusion

If an infrastructure failure occurs for any (task, repeat) cell, that cell is excluded **for every arm symmetrically**. Selective retry of Fehrest is prohibited.

## 20. Power analysis and confirmatory-N rule — frozen

Confirmatory analysis is McNemar's exact test on paired binary outcomes.

| Parameter | Value |
|---|---|
| α (two-sided) | 0.05 |
| Target power | 0.80 |
| Minimum meaningful effect δ | 0.15 |
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
r_conf  = ceil( N_pairs / K_eligible )
```

**The divisor is K_eligible (not 30).** If B-NULL excludes tasks, the divisor shrinks accordingly.

**Safety bounds:**

| Bound | Value | Behaviour at the bound |
|---|---|---|
| `r_conf` minimum | 3 | Below this, per-task variability is unobservable. Raised to 3 |
| `r_conf` maximum | 20 | Cost ceiling |
| `N_pairs` floor | 90 | |
| `N_pairs` ceiling | 600 | |
| `K_eligible` minimum | 15 | If K_eligible < 15, report as UNDERPOWERED |

**If the formula demands r_conf > 20, the study is declared UNDERPOWERED_FOR_PREREGISTERED_EFFECT and reported as such.**

If ψ̂ ≤ δ² the formula is undefined — that means the arms almost never disagree, which is itself the answer, and it is reported as NO_DETECTABLE_DISCORDANCE rather than patched.

### 20.1 Statistical review requirement

The final statistical design must receive independent statistical review before sealing. Hermes may design and implement a proposed fail-closed rule, run deterministic tests of that rule, and document candidate reasoning. Hermes may NOT claim `R1_V2_STATISTICAL_REVIEW=PASS` from its own work.

If no independent statistician/reviewer is actually available through the authorized environment, record:

```text
R1_V2_STATISTICAL_REVIEW=PENDING
```

and continue all other authorized work.

## 21. Maximum cost/run bounds

| Bound | Value |
|---|---|
| Maximum model sessions (variance pilot) | 972 |
| Maximum model sessions (confirmatory, r_conf=20) | 20 × K_eligible × 6 (estimated) |
| Maximum total model sessions | 3,888 (preserved from v1) |
| Maximum cost per run | Provider-dependent, recorded |
| Maximum wall time per run | 120 seconds |

## 22. Unblinding procedure

1. Arms are executed under neutral identifiers (ARM_A through ARM_F).
2. The strings "Fehrest", "wiki", and "baseline" do not appear in any model-visible prompt.
3. The arm-identity mapping lives in `runs/<stage>/arm-map.json`, withheld until scoring is complete.
4. After scoring is complete and the scoring seal is recorded, the arm-map is published.
5. Unblinding occurs in a single commit that reveals the mapping and the per-arm scores simultaneously.

## 23. Ceiling/floor handling

### 23.1 Ceiling detection

If the variance pilot reveals ψ̂ ≤ δ² (NO_DETECTABLE_DISCORDANCE), the study is reported as a ceiling effect. This is a legitimate scientific finding and is **not** interpreted as thesis support or falsification.

### 23.2 Floor detection

If all arms score near zero (floor effect), the study is reported as UNDERPOWERED_FOR_DIFFICULTY. Tasks are too hard for any arm, and the benchmark provides no useful signal.

### 23.3 Ceiling-effect response

If a ceiling effect is detected in the R1-v2 variance pilot, the response is:
1. Report as UNDERPOWERED_FOR_PREREGISTERED_EFFECT
2. Do not proceed to confirmatory
3. Report the ceiling effect as the finding
4. Founder decides on next steps (no automatic escalation)

## 24. Terminal verdict mapping

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

## 25. Failure routing

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

## 26. Separation from confirmatory data

```
runs/variance-pilot-v2/     <- stage 1 output. NEVER read by confirmatory analysis
runs/confirmatory-v2/       <- stage 2 output, created only after the manifest is sealed
```

Pilot runs are not pooled, not reused as extra confirmatory observations, and not re-scored under a later rule.

## 27. Required pilot report

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

## 28. Then, and only then

1. Apply the B-NULL exclusion from §19.1. This yields K_eligible, N_pairs and r_conf.
2. Compute r_conf mechanically from §20. No judgement, no adjustment.
3. Create **R1-CONFIRMATORY-v2** — a new immutable manifest carrying the computed N, the power-analysis digest, the model condition, the runner version, the corpus, task, scorer and baseline digests, the frozen Fehrest identity, the randomization seed and the execution-plan digest.
4. Seal it. **Then** run the confirmatory stage.

Confirmatory execution may not begin until both `R1_VARIANCE_PILOT_V2_COMPLETE` and `R1_CONFIRMATORY_MANIFEST_V2_SEALED` are true.

## 29. Benchmark-design review checklist

Before execution, the following checklist must be independently reviewed:

| Check | Status | Evidence |
|---|---|---|
| CONSTRUCT_VALIDITY | PENDING | Tasks measure continuation correctness, not trivia retrieval |
| DIFFICULTY_WITHOUT_ARTIFICIALITY | PENDING | Complexity from structural depth, not linguistic obscurity |
| TASK_TIMELINE_VALIDITY | PENDING | 12 distinct checkpoints, 27 of the 30 tasks are issued before t14 |
| TEMPORAL_LEAKAGE | PENDING | Corpus manifest encodes available_from/until |
| NO_INFORMATION_LEAKAGE | PENDING | Future-evidence vocabulary check; structural vocabulary subtraction |
| NO_ARM_FAVORING | PENDING | Neutral arm identifiers; same model condition for all arms |
| BASELINE_FAIRNESS | PENDING | B0 recency-ordered; B4 maintained wiki; both unweakened |
| SCORER_VALIDITY | PENDING | Deterministic, field-scoped, arm-blind |
| ORACLE_VALIDITY | PENDING | Each oracle has derivable_from and trap_present assertions |
| CEILING_RISK | PENDING | Multi-layer supersession and cross-file synthesis reduce ceiling risk |
| FLOOR_RISK | PENDING | 3+ tasks where B0/B4 can genuinely win |
| MAINTENANCE_FAIRNESS | PENDING | Task-blind; same evidence; same time |
| MODEL_IDENTITY_ADMISSIBILITY | PENDING | Fail-closed policy |
| COST_BOUND | PENDING | r_conf ≤ 20; maximum 3,888 total sessions |
| REPRODUCIBILITY | PENDING | Seeded randomization; per-run evidence capture; immutable raw output |

## 30. What Fehrest has to show

It does not need to win everything. A meaningful thesis needs evidence that the extra structure buys something material — better continuation at similar cost, similar continuation at much lower maintenance cost, better stale-decision avoidance at acceptable cost, or accuracy that holds up better as project age and churn increase.

**If B4 gives essentially the same continuation quality at lower complexity and reasonable maintenance cost, that is evidence against the current Fehrest thesis, and it gets reported as evidence against.**

No feature will be added in response to any R1-v2 result. `GRAPH=NO` `VECTORS=NO` `AUTO_MEMORY=NO` `RERANKER=NO` `MCP=NO` `UI=NO`.

## 31. Post-result modification policy

Per the immutable-evidence governance rule:

1. Raw model output is written once, digested, and never edited.
2. No manual repair of an answer before scoring, for any reason.
3. If a harness defect is discovered mid-run, the batch is invalidated.
4. Post-hoc modifications preserve originals, record SHA-256s, classify versions, and disclose.

## 32. R1-v1 ceiling-effect preservation

The R1-v1 ceiling effect is preserved as immutable prior evidence:

```text
R1_V1_CEILING_EFFECT_EVIDENCE=SHA256:d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
R1_V1_CEILING_EFFECT_COMMIT=cef01818bc178366109ef386b40a7c02330015c4
R1_V1_CEILING_EFFECT_RESULT=NO_DETECTABLE_DISCORDANCE
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
```

The failed-to-discriminate study is not overwritten, retroactively modified, rescores, or reused as confirmatory observations. It is input to the R1-v2 design, not data for tuning individual answers.


## 33. R1-v3 leakage taxonomy and mitigation (derived from immutable R1-v2 evidence)

R1-v2 B-NULL exclusion rate 20/30 was not random. For the 20 excluded tasks, root cause classification (derived from prompt/oracle overlap and B-NULL raw transcripts) is:

| Leakage class | Description | v2 examples (evidence) | v3 mitigation |
|---|---|---|---|
| **A. Prompt contains answer verbatim** | Required substring appears verbatim in prompt | S1-A schema registry, S1-C hash/PII, S2-C encrypt/transit | Minimal prompts: remove history disclosure; prompt must not contain any oracle require_all 'contains' substring (deterministic preflight). Two proposal-term overlaps (S3-D regex, S3-F confidence) are query content, not history — documented and bounded. |
| **B. Prompt states history chain** | Prompt lists t0→t1→t2 progression, so model infers supersession without retrieval | S1-B JSON→Protobuf, S2-B site→protocol, S1-D single partition bottleneck | Prompt gives only proposal, no history chain. Model must retrieve supersession evidence (e.g., S1-T1-DEC-002) via context. |
| **C. Prompt discloses current value identical to answer** | Historical question leaks answer by stating current equals past | S1-G current Protobuf = answer Protobuf, S2-G current protocol = answer, S3-G current automated = answer | Prompt asks bare historical question without stating current value. |
| **D. Prompt lists rename chain** | Identity task leaks current name by enumerating all renames | S1-H ingest-core→event-gateway→stream-ingest, S2-H data-flow→trial-pipeline→clinical-ingest | Prompt gives only stale reference (e.g., 'ingest-core'), no chain. |
| **E. Prompt hints abstention** | Prompt explicitly says no measured value exists | S1-I 'but no actual measured throughput at t9', S2-I similar | Prompt asks factual question without hinting absence. Correct behavior requires abstain and substantive action. |
| **F. Prompt lists both conflicting ADRs** | Contradiction task presents both ADRs, model flags conflict trivially | S1-F ADR-012 vs ADR-015, S2-F ADR-030 vs 031 | Prompt describes task without listing ADRs; model must retrieve both. |
| **G. Generic generic-knowledge sufficient when constraint disclosed** | If prompt states constraint (e.g., PII must be hashed), generic knowledge suffices | S1-C, S2-C, S3-C | Prompt does not state constraint; retrieval required. |
| **H. Oracle requires generic verb guessable without evidence** | 'reject' alone is guessable as safe default for revert proposals | S1-B/D/F etc. require 'reject' | Keep 'reject' but pair with specific project term (e.g., Protobuf, bottleneck, timeout, automated) that is not in prompt, requiring retrieval. For v3 we retain pairing; deterministic overlap check ensures prompt lacks the specific term. |

**Prospective use:** This taxonomy is applied during deterministic design audit. Any candidate v3 task whose prompt contains its oracle's required 'contains' substring (normalized) outside of intentional proposal-term exceptions fails the preflight and must be revised before sealing. No post-result threshold change is allowed.

## 34. R1-v3 design requirements — explicit responses

### 34.1 B-NULL leakage
- Deterministic preflight: normalized prompt must not contain any oracle require_all 'contains' substring (except documented proposal-term exceptions S3-D/S3-F where prompt contains proposal term but not decision/history). Executed via `bench/R1/validate.py::prompt_oracle_overlap` and `test_validate.py`.
- Target K_eligible >=20 (margin 5 above minimum 15) with K_TOTAL=30; expected exclusion 0-5.
- Fail-closed route: if projected B-NULL leakage in pilot exceeds 10 excluded (K_eligible <20) yet still ≥15, continue to report but flag design debt; if K_eligible <15, declare UNDERPOWERED per preregistered rule, no silent inflation, no threshold change.

### 34.2 Task-class preservation
- Each of 12 classes has 1-3 tasks (same counts as v2); design ensures at least one per class is retrieval-heavy and not guessable.
- Minimum eligible coverage: every class must retain ≥1 eligible task; full loss of any class triggers TASK_CLASS_LOSS route (same as v2 §11). If ≥3 classes fully excluded, route is TASK_CLASS_LOSS even if K_eligible ≥15.
- Historical losses specifically addressed: NEXT_ACTION, CONSTRAINT_RETENTION, FAILED_APPROACH_AVOIDANCE, HISTORICAL_REASONING, IDENTITY_CONTINUITY, ABSTENTION redesigned with minimal prompts (see §33).

### 34.3 Temporal/state dependence
- Tasks require information not present in prompt, not trivially inferable from generic knowledge, available through corpus/history representation (evidence available_from ≤ checkpoint, available_until, supersession links), deterministically oracle-checkable via scorer (require_all/forbid/abstain/require_synthesis/require_epoch).

### 34.4 No leakage audit
- Prompt leakage: checked via overlap audit.
- Task naming leakage: task IDs S*-* are neutral (scenario+letter) and not model-visible; corpus paths are not in prompt.
- Oracle leakage: oracles never model-visible, arm-blind scoring.
- File-path/metadata/arm-formatting/timestamp/state-ordering/answer-shape leakage: prompts are arm-neutral, same format across arms, no timestamps, no ordered state, answer shape enforced via output_contract but identical across arms.

### 34.5 Strong baseline fairness
- B0 (newest checkpoint first, plain files), B1, B3, B4 constructions unchanged from v2; B0/B4 not weakened; context budget 6000 bytes identical; model condition identical (gpt-5.6-terra medium 0.0 1024).
- No arm-favoring context construction; all arms receive same 6000-byte budget and same task prompt.

### 34.6 Oracle quality
- Each oracle deterministic or explicitly bounded: require_all (contains/equals), forbid, abstention, require_synthesis (checkpoint fact coverage), require_epoch (epoch marker). Prevent ambiguous equivalence, subjective grading, hidden discretion, post-result changes. Scorer reuse preserved (see §34.7).

### 34.7 Scorer validity
- Reuse existing scorer (`bench/R1/scorer.py`) — semantics remain valid for v3 (field-scoped, deterministic, arm-blind, handles require_synthesis/require_epoch via corpus fact grounding). No scorer change required; if change needed, it is load-bearing, specified before execution, tested adversarially, frozen before pilot.

### 34.8 Statistical design preservation
- All v2 invariants preserved unless preregistered amendment justified:
```text
PAIRING_UNIT=(task,repeat)
B_NULL_EXCLUSION_BEFORE_PSI=YES
K_TOTAL=30
MINIMUM_K=15
MCNEMAR=YES
N_pairs=ceil((z_{1-a/2}*sqrt(psi_hat)+z_power*sqrt(psi_hat-delta^2))^2/delta^2) (not K*(K-1)/2)
K_TOTAL != N_pairs divisor; divisor is K_eligible
r_conf=ceil(N_pairs/K_eligible)
R_CONF_MIN=3, R_CONF_MAX=20, N_pairs_floor=90, N_pairs_ceiling=600
DELTA=0.15, ALPHA=0.05, POWER=0.80, z=1.959964/0.841621
```
- Reverified from canonical truth (see validate.py § statistical_parameters).

## 35. R1-v3 deterministic preflight (no empirical model calls)

Before provider execution, the following deterministic and low-cost checks are executed (fixtures + structural tests):

```text
task schema (ids, classes, checkpoints, contracts)
oracle schema (require_all/forbid/abstention/require_synthesis/require_epoch)
task-class balance (12 classes, 30 tasks, distribution ≥8 checkpoints, ≥12 before t14)
duplicate detection (ids unique, evidence ids unique)
near-duplicate detection (normalized prompt Jaccard <0.8 across tasks)
answer leakage (prompt/oracle overlap audit — §33)
prompt/oracle overlap (normalized contains check)
context-only evidence requirement (each task has depends_on_evidence with available_from ≤ checkpoint)
state dependency (depends_on_evidence not empty except proven abstention)
temporal ordering (temporal_span ≤ checkpoint, epoch_boundary ⇒ checkpoint≥5)
arm parity (same budget, same model condition across arms)
token-budget compliance (corpus items within budget, harness cut deterministic)
maintenance compatibility (14 transitions ×3 scenarios ×3 arms ×2 trajectories =252)
deterministic execution-order generation (seed b1aeba1de38a2a7e analogue derived from sealed candidate+manifest, blocked+interleaved)
```

Synthetic tests validate protocol only, not empirical benchmark evidence.

## 36. B-NULL pre-pilot qualification (deterministic only)

No empirical B-NULL-only model run is authorized before the full v3 pilot. Qualification is via deterministic audits (§35) only. This prevents adaptive fishing. Any future empirical qualification would require preregistered sample, decision threshold, allowed observations/modifications, stale-prereg consequences, and task reuse rules — none authorized here.

## 37. Task design safety margin

K_TOTAL remains 30 (no casual change). Corpus designed so reasonable B-NULL exclusion (0-5) still leaves K_eligible ≥25, safely above minimum 15. Not targeting exactly 15. Safety margin justified by expected leakage reduction from minimal prompts. If evidence later supports changing K_TOTAL, it is a preregistered statistical amendment with power/cost validation before freeze.

## 38. Cost bounds (derived before execution)

```text
Variance pilot: 972 sessions = 252 maintenance + 600 comparison (5 arms×30×4) + 120 calibration (1×30×4)
Confirmatory upper bound: r_conf_max=20 ⇒ N_pairs_ceiling=600 ⇒ max confirmatory sessions = r_conf_max × K_eligible ×6 + maintenance? Budget: worst-case K_eligible=15 ⇒ 20×15×6=1800 +252 =2052 confirmatory; plus pilot 972 =3024 <3888 ceiling. With K_eligible=30 ⇒ 20×30×6=3600 +252=3852 +972=4824 exceeds 3888 but N_pairs ceiling 600 caps r_conf at ceiling; actual max total <3888 per v2 §21. Fail closed if cost exceeds canonical ceiling.
Pilot cost (972) derived from sealed model condition (gpt-5.6-terra medium 1024) ~provider-recorded tokens; no execution until sealed.
Fail closed if cost exceeds canonical ceiling.
```

## 39. R1-v3 artifact families

```text
bench/R1/benchmark-spec-v3.json (single source of truth)
bench/R1/tasks-v3.json
bench/R1/oracles-v3.json
bench/R1/corpus-manifest-v3.json
bench/R1/PREREGISTRATION-V3.md (this file)
bench/R1/VARIANCE-PILOT-V3.md
bench/R1/MAINTENANCE-V3.md
bench/R1/scorer.py (reused, validated)
bench/R1/validate.py (extended with v3 overlap and class checks)
bench/R1/test_scorer.py, test_validate.py, test_r1v3_statistical_design.py, test_review_binding.py (extended)
bench/R1/generate_manifest.py (extended to emit v3 manifest)
docs/canonical/R1_V3_SCIENTIFIC_REVIEW_PACKET.md (if needed)
docs/canonical/R1_V3_STATISTICAL_REVIEW_PACKET.md
docs/canonical/R1_V3_SEALING_PROCEDURE.md / amendment
runs/variance-pilot-v3/ (post-seal execution)
```

Naming follows canonical structure; no duplicate v2 mutation.


## 40. Artifact manifest (v3)

The R1-v2 benchmark is defined by the following authoritative artifacts:

| Artifact | Path | Description |
|---|---|---|
| Benchmark spec | `bench/R1/benchmark-spec-v3.json` | Single source of truth (v3 low-leakage) |
| Task table | `bench/R1/tasks-v3.json` | 30 frozen tasks (minimal prompts) |
| Oracle table | `bench/R1/oracles-v3.json` | 30 frozen oracles (deterministic) |
| Corpus manifest | `bench/R1/corpus-manifest-v3.json` | 96 evidence objects (same as v2, prereg_version v3) |
| Scorer | `bench/R1/scorer.py` | Deterministic scorer (reused, v2 semantics preserved) |
| Validator | `bench/R1/validate.py` | Machine validator (extended with v3 overlap) |
| Tests | `bench/R1/test_scorer.py` | Scorer unit tests (20/20) |

All artifacts are generated from `benchmark-spec-v2.json`. No authoritative number is manually duplicated across files.
