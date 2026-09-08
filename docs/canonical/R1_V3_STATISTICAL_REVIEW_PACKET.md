# R1-v3 Independent Statistical Review Packet

**Status:** `SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08 — HUMAN_REVIEW_OPTIONAL, INTERNAL_QUALIFICATION_GATING`

**Created:** 2026-09-04
**Revised:** 2026-09-07 — convergence repair (branch `review/r1-v2-independent-review-convergence`)
**Amended:** 2026-09-08 — `FOUNDER_DECISION=REMOVE_MANDATORY_HUMAN_INDEPENDENT_REVIEW_GATE` (see `docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md`); `HUMAN_INDEPENDENT_REVIEW=OPTIONAL`, `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`; `INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION`; internal deterministic qualification now gates sealing.

**Candidate binding (WORKING_CANDIDATE at this revision):**
```text
WORKING_CANDIDATE_COMMIT=0d206cac9a6e5ebfe3d47401aa1f081a587af60f
WORKING_CANDIDATE_TREE=6943decf800574906b76b0abd7dc5a3460cef072
REVIEW_CANDIDATE=NOT_YET_FROZEN — packet is WORKING_CANDIDATE for internal qualification only
SEALED_CANDIDATE=NONE
EXECUTION_CANDIDATE=NONE
```
Review must bind to an exact immutable `REVIEW_CANDIDATE` commit/tree + artifact manifest SHA-256 (see `bench/R1/artifact-manifest-v3.json` when generated). If any load-bearing artifact changes after review, `AFFECTED_REVIEW=STALE` and `RE_REVIEW_REQUIRED=YES`.

**Prerequisites (all satisfied for machine validation):**
- R1_V3_MACHINE_VALIDATION=PASS
- R1_V3_VALIDATION_CONVERGENCE=COMPLETE
- R1_V3_MUTATION_TESTING=PASS
- R1_V3_EXACT_HEAD_CI=PASS
- `python bench/R1/validate_v3.py`, `test_validate_v3.py`, `test_scorer.py` all PASS on `0d206ca` (verify-artifacts, test-scorer, test-validator, validate, canonical-equality)
- **Founder governance 2026-09-08:** `INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION`, `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`

**Hard boundaries (must not be violated):**
- R1_V3_MODEL_EXECUTION=PROHIBITED
- R1_V3_VARIANCE_PILOT_EXECUTION=PROHIBITED
- R1_V3_CONFIRMATORY_EXECUTION=PROHIBITED
- R1_V3_UNBLINDING=PROHIBITED
- R1_V3_STATISTICAL_REVIEW=HUMAN_REVIEW_OPTIONAL (mandatory gate SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08)
- R1_V3_STATISTICAL_DESIGN_SELF_AUDIT=REQUIRED (internal 18-section deterministic qualification)
- R1_V3_SCIENTIFIC_DESIGN_SELF_AUDIT=REQUIRED
- SPEC_002_ACTIVATION=PROHIBITED
- PRODUCT_IMPLEMENTATION=PROHIBITED

**Live canonical sources (single source of truth):**
- `bench/R1/benchmark-spec-v3.json` (`statistical_parameters`, `session_arithmetic`, `maintenance_protocol`)
- `bench/R1/PREREGISTRATION-V2.md` §§19–20, 28
- `bench/R1/VARIANCE-PILOT-V2.md` §§6–10
- `bench/R1/MAINTENANCE-V2.md` §§2,4,6–7
- `bench/R1/validate_v3.py` / `bench/R1/test_validate_v3.py` (machine truth)

---

## 0. Canonical symbol table — no symbol is reused

This packet explicitly distinguishes symbols that were previously conflated. One symbol = one concept.

| Symbol | Canonical name | Value / definition | Source |
|---|---|---|---|
| `TASK_COUNT` | total tasks in bench | `30` | `benchmark-spec-v3.json: session_arithmetic.total_tasks` |
| `K_TOTAL` | total tasks for power analysis before exclusion | `30` | `statistical_parameters.K_total` |
| `B_NULL_EXCLUDED_TASK_COUNT` | number of prompt-answerable tasks to exclude | `0 ≤ n ≤ 30`, computed after variance pilot | `§19.1, §28` |
| `K_ELIGIBLE_TASK_COUNT` | eligible tasks after B-NULL exclusion | `K_TOTAL − B_NULL_EXCLUDED_TASK_COUNT` | `statistical_parameters.K_eligible` |
| `K_ELIGIBLE` | alias for `K_ELIGIBLE_TASK_COUNT` in formulas | same as above | PREREG §20, VARIANCE-PILOT §7 |
| `REPEAT_COUNT` | repeats per (arm, task) | pilot `r=4`; confirmatory `r_conf` | PREREG §§15,18–20 |
| `PAIRING_UNIT` | unit that yields one paired binary observation | **`(task, repeat) pair`** | `statistical_parameters.pairing_unit` |
| `OBSERVATION_PAIR` | paired outcomes for one `PAIRING_UNIT` | `(x_{B5,t,i}, x_{B4,t,i}) ∈ {0,1}²` for fixed `(t,i)` | VARIANCE-PILOT §6 |
| `ARM` | context construction strategy | one of `B-NULL, B0, B1, B3, B4, B5` | `benchmark-spec-v3.json: arms` |
| `ARM_CONTRAST` | ordered pair of arms compared | primary: `B5 vs B4` | PREREG §20 |
| `ARM_CONTRAST_COUNT` | number of pairwise contrasts among eligible comparison arms | `5 choose 2 = 10` for `{B0,B1,B3,B4,B5}` | derived, not a power-analysis input |
| `PSI_HAT` (`ψ̂`) | population discordant-pair rate | `ψ̂ = proportion of (task,repeat) pairs where exactly one of B5,B4 is correct` | `statistical_parameters.psi_hat_population` |
| `N_PAIRS_REQUIRED_BY_POWER` (`N_pairs`) | paired observations required by McNemar power rule | `ceil( (z_{1-α/2}·√ψ̂ + z_{power}·√(ψ̂ − δ²))² / δ² )` | PREREG §20 formula |
| `R_CONF` (`r_conf`) | confirmatory repeats per eligible task | `ceil( N_pairs / K_ELIGIBLE )` | `statistical_parameters.r_conf_formula` |
| `DELTA` (`δ`) | minimum meaningful effect | `0.15` | `statistical_parameters.minimum_meaningful_effect_delta` |
| `ALPHA` (`α`) | two-sided Type I error | `0.05` | `statistical_parameters.alpha` |
| `POWER` | target power | `0.80` | `statistical_parameters.target_power` |
| `R_CONF_MINIMUM` | floor | `3` (below this, per-task variability unobservable) | `r_conf_minimum` |
| `R_CONF_MAXIMUM` | ceiling | `20` (cost ceiling) | `r_conf_maximum` |
| `N_PAIRS_FLOOR` | floor | `90` | `N_pairs_floor` |
| `N_PAIRS_CEILING` | ceiling | `600` | `N_pairs_ceiling` |
| `K_MINIMUM` | minimum eligible tasks for powered study | `15`; if `K_ELIGIBLE < 15 → UNDERPOWERED` | `minimum_K` |

**Explicitly NOT the rule:** `N_pairs ≠ K_ELIGIBLE·(K_ELIGIBLE−1)/2`. That expression is the count of unordered *task pairs* and the count of *arm contrasts* is `ARM_CONTRAST_COUNT`. Neither is the McNemar power-analysis sample requirement. The packet's prior use of `N_pairs=K_eligible*(K_eligible-1)/2` was mathematically inconsistent and is corrected here.

---

## 1. PAIRING_UNIT

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

**Canonical definition:** `PAIRING_UNIT = (task, repeat) pair`.

Each `(task, repeat)` yields one `OBSERVATION_PAIR` = `(score_B5, score_B4)`. Discordance for that unit is `1` iff exactly one of the two scores is `1`. `ψ̂` is the population proportion of discordant `OBSERVATION_PAIR`s.

**Not:** task alone. Not: task-oracle pair alone. The repeat index is load-bearing — without it, `r_conf` cannot be defined.

Verified in `benchmark-spec-v3.json: statistical_parameters.pairing_unit = "(task, repeat) pair"`, PREREG §20 `pairing_unit = (task, repeat) pair`, VARIANCE-PILOT §7 same, and §6 defines per `(task,repeat)` the paired difference. Validator checks `pairing_unit` field presence (not its semantics beyond string); this packet corrects the semantic misuse that treated task count as pair count.

## 2. B_NULL_EXCLUSION_ORDER

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

**Canonical ordering (§28):**
1. Apply `B_NULL_exclusion_rule` — tasks where `B-NULL` scores `>0` are excluded. This yields `K_ELIGIBLE` and `B_NULL_EXCLUDED_TASK_COUNT`.
2. Compute `ψ̂` **using only eligible observations** (see §5 — `PSI_USES_ELIGIBLE_OBSERVATIONS`).
3. Compute `N_pairs` from `ψ̂` and `δ`.
4. Compute `r_conf = ceil(N_pairs / K_ELIGIBLE)` **using `K_ELIGIBLE` as divisor** (see §8 — `R_CONF_USES_K_ELIGIBLE`).

Verified in `PREREGISTRATION-V2.md` §28.1 (step 1 is B-NULL exclusion) and `VARIANCE-PILOT-V2.md` §10 (same ordering). Validator `_validate_protocol_documents` asserts that §28.1 / §10.1 first step mentions `B-NULL`. Mutation test for ordering drift included in `test_validate_v3.py` (protocol-doc search). This packet now also requires `B_NULL_EXCLUSION_BEFORE_PSI` — any power computation that uses ψ̂ before exclusion is INVALID.

## 3. K_TOTAL

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`K_TOTAL = 30`. This is `TASK_COUNT` (=30) at the design stage before any exclusion. Verified from `benchmark-spec-v3.json: statistical_parameters.K_total = 30`, `session_arithmetic.total_tasks = 30`, `tasks-v2.json` length 30, `oracles-v2.json` length 30, and `task_classes` sum 30. All 30 tasks have exactly 1 oracle view (`task.oracle_id` ↔ `oracle.task_id` 1:1, enforced by `_validate_task_oracle_resolution` and `_validate_canonical_derived_equality`).

`K_TOTAL` is distinct from `K_ELIGIBLE`. Do not use `K_TOTAL` as divisor in `r_conf`.

## 4. K_ELIGIBLE_TASK_COUNT

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

```
K_ELIGIBLE_TASK_COUNT = K_ELIGIBLE = K_TOTAL − B_NULL_EXCLUDED_TASK_COUNT
```

- `B_NULL_EXCLUDED_TASK_COUNT` = count of tasks where `B-NULL` scores `>0` in the variance pilot (prompt-answerable tasks). Each such task is excluded from the primary analysis (PREREG §19.1).
- `K_ELIGIBLE_AFTER_B_NULL` must hold: compute eligible set first, then every downstream quantity.
- Exclusion is symmetric across arms — no arm gets a different task set.
- If `K_ELIGIBLE < minimum_K (=15)`, the study is `UNDERPOWERED` for the preregistered effect; no silent `r_conf` inflation beyond `R_CONF_MAXIMUM` may rescue it.

Candidate edge semantics (see §11, §14 for deterministic examples):

| `B_NULL_EXCLUDED_TASK_COUNT` | `K_ELIGIBLE` | Route |
|---|---|---|
| `0` | `30` | nominal |
| `1` | `29` | divisor shrinks by 1 |
| `10` | `20` | material shrinkage; `r_conf` grows |
| `15` | `15` | at `minimum_K` boundary — still powered if formula allows |
| `16` | `14` | `LOW_K_ROUTE` → `UNDERPOWERED` |
| `30` | `0` | `TASK_CLASS_LOSS_ROUTE` extreme → `UNDERPOWERED` |

## 5. PSI_HAT

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`ψ̂` = proportion of `(task, repeat)` pairs where exactly one of `B5` and `B4` is correct.

- Population definition: `statistical_parameters.psi_hat_population`.
- Variance-pilot estimator: `ψ̂ = #{(t,i): x_{B5,t,i} ≠ x_{B4,t,i}} / #{eligible (t,i)}` — denominator is `K_ELIGIBLE × r` (pilot `r=4`), i.e., `PSI_USES_ELIGIBLE_OBSERVATIONS`.
- Primary contrast is `B5 vs B4` (Fehrest vs maintained wiki). Other contrasts (e.g., `B5 vs B0`) may be reported secondarily but do **not** drive `N_pairs` for the confirmatory manifest.

**Key distinctions:**
- `PSI_HAT` ∈ `[0,1]`. `ψ̂ = 0` → `NO_DETECTABLE_DISCORDANCE` (see §17).
- `ψ̂` is **not** the number of discordant *tasks*, nor the number of `ARM_CONTRAST`s.
- `ψ̂` is undefined for power purposes when `ψ̂ ≤ δ²` — see §6, §17.

**Current claim:** `R1_V3_EMPIRICAL_PSI_HAT = NONE`. R1-v3 variance-pilot data has not been collected (`R1_V3_VARIANCE_PILOT=NOT_EXECUTED`). R1-v1 pilot `ψ̂ = 0.0000` for all arm pairs is `R1_V1_HISTORICAL_EVIDENCE` only (see scientific packet).

## 6. MCNEMAR

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

Confirmatory analysis is **McNemar's exact test** on paired binary outcomes (PREREG §20, VARIANCE-PILOT §7). The pilot **does not** perform hypothesis testing; it estimates `ψ̂` as input to the power rule.

- Test unit: `OBSERVATION_PAIR` for one `(task,repeat)` under `B5` vs `B4`.
- No pooling across unrelated contrasts; each contrast has its own 2×2 table.
- Pilot reporting: paired difference distribution `d_t = p̂_{B5,t} − p̂_{B4,t}`, `SD(d)`, per-cell rates, but `PRODUCT_THESIS_PASS/FAIL` is PROHIBITED at pilot stage (§9 in both docs).

R1-v1 showed `0` discordant pairs across all contrasts (`NO_DETECTABLE_DISCORDANCE`). That is `R1_V1_HISTORICAL_EVIDENCE`, not R1-v3 data.

## 7. N_PAIRS_REQUIRED_BY_POWER

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

**Correct formula (from `benchmark-spec-v3.json` and PREREG §20):**

```text
N_pairs = ceil( ( z_{1−α/2}·sqrt(ψ̂) + z_{power}·sqrt(ψ̂ − δ²) )² / δ² )
```

where `z_{1−α/2}=1.959964`, `z_{power}=0.841621`, `δ=0.15`, `ψ̂` as defined in §5.

- `N_pairs` is the **required number of `(task, repeat)` observation pairs** for McNemar's test to achieve `power=0.80` at `α=0.05` for effect `δ`.
- Domain: requires `ψ̂ > δ²`. If `ψ̂ ≤ δ²`, the expression under `√(ψ̂ − δ²)` is non-positive → formula undefined → report `NO_DETECTABLE_DISCORDANCE` (see §17), do not patch.
- Bounds: `N_pairs` is then clipped/floored to `[N_pairs_floor=90, N_pairs_ceiling=600]` per VARIANCE-PILOT §7 safety bounds. If the raw formula demands `N_pairs > 600`, the confirmatory would already demand `r_conf > ceiling` for plausible `K_ELIGIBLE` and is reported `UNDERPOWERED_FOR_PREREGISTERED_EFFECT`.

**Incorrect prior mapping (explicitly rejected):**
```text
REJECTED: N_pairs = K_ELIGIBLE·(K_ELIGIBLE−1)/2
```
That counts unordered task pairs. It is not a function of `ψ̂`, `α`, `δ`, or `power`, and it conflates `TASK_COUNT` combinatorics with *statistical power*. It also double-uses `N_pairs` to mean both power-required pairs and arm-contrast count. This packet eliminates that reuse.

## 8. R_CONF

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

```text
r_conf = ceil( N_pairs / K_eligible )
```

- Divisor is `K_ELIGIBLE` (**not** `K_TOTAL = 30`). If B-NULL excludes tasks, the divisor shrinks and `r_conf` grows accordingly. This is the `R_CONF_USES_K_ELIGIBLE` invariant.
- `r_conf` is repeats **per eligible task** needed in the confirmatory so that total confirmatory observation pairs `= K_eligible × r_conf ≥ N_pairs`.
- Bounds: `r_conf` is then bounded to `[R_CONF_MINIMUM=3, R_CONF_MAXIMUM=20]`:
  - `<3 → INCONCLUSIVE (per-task variability unobservable) → raised to 3`
  - `>20 → COST_CEILING → report UNDERPOWERED_FOR_PREREGISTERED_EFFECT, do not relax δ/α`

**Examples (deterministic, static):**

| `K_eligible` | `N_pairs` | raw `r_conf` | bounded `r_conf` |
|---|---|---|---|
| `30` | `90` | `3` | `3` (at floor) |
| `30` | `120` | `4` | `4` |
| `29` | `120` | `5` | `5` (divisor matters) |
| `20` | `400` | `20` | `20` (at ceiling) |
| `20` | `401` | `21` | `→ UNDERPOWERED` |
| `15` | `90` | `6` | `6` (at minimum K) |

See also §11 and §14 for exhaustive static edge cases exercised in `bench/R1/test_r1v3_statistical_design.py`.

## 9. R_CONF_MIN

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`R_CONF_MINIMUM = 3` ( `statistical_parameters.r_conf_minimum` ). Below this, per-task variability is unobservable (with `r=1` the within-task variance is 0; with `r=2` it is minimally estimable but underpowered for heterogeneity). Any raw `r_conf < 3` is raised to `3`. Must be satisfied before any product-thesis verdict.

Machine validation: `_validate_statistical_parameters` asserts `r_conf_minimum == 3`. No post-hoc lowering.

## 10. R_CONF_MAX

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`R_CONF_MAXIMUM = 20` ( `statistical_parameters.r_conf_maximum` ). Cost ceiling. If the bounded formula demands `r_conf > 20`, report `UNDERPOWERED_FOR_PREREGISTERED_EFFECT` (PREREG §20). Do not relax `δ`, `α`, drop task classes, or switch to one-sided test after seeing `ψ̂`.

Machine validation: `_validate_statistical_parameters` asserts `r_conf_maximum == 20`.

## 11. LOW_K_ROUTE

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

If `K_ELIGIBLE < minimum_K (=15)` after `B_NULL_exclusion`, the study is `UNDERPOWERED` for the preregistered `δ`. This is the `LOW_K_ROUTE`.

**Static verification (exercised deterministically without empirical data):**

```text
K_TOTAL=30
K=30 → ELIGIBLE 30 → nominal
K=29 → ELIGIBLE 29 → nominal (divisor 29)
K=20 → ELIGIBLE 20 → nominal variant
K=15 → ELIGIBLE 15 → AT_MINIMUM, still powered if r_conf ≤20
K=14 → ELIGIBLE 14 → UNDERPOWERED (LOW_K_ROUTE)
K=0  → ELIGIBLE 0  → UNDERPOWERED, TASK_CLASS_LOSS_ROUTE extreme
```

R1-v3 design has 30 tasks with 27 before `t14` for maintenance-lag testing, but if B-NULL disproportionately removes early tasks, `K_ELIGIBLE` may fall below 15 even with nominal `TASK_COUNT=30`. The protocol requires honest reporting of `UNDERPOWERED` rather than ad-hoc `r_conf` rescue.

## 12. TASK_CLASS_LOSS_ROUTE

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

If certain task classes are *fully* excluded (e.g., all `ABSTENTION` tasks were prompt-answerable via `B-NULL`, or an entire class shows `ψ̂_class = 0` ceiling), the `TASK_CLASS_LOSS_ROUTE` applies:

- Those classes are excluded from `K_ELIGIBLE` (already via `B_NULL_exclusion` if prompt-answerable) **or** flagged as `CEILING_EFFECT` within class.
- Do not pool heterogeneous classes to hide class-level ceiling — report per-class `ψ̂_class` alongside pooled `ψ̂`.
- If multiple classes are eliminated such that `K_ELIGIBLE < 15`, `LOW_K_ROUTE` supersedes.
- Task design revision for that class would require a **new preregistration**, not a silent substitution.

Deterministic examples for static checks:
- One class fully excluded: e.g., `ABSTENTION (n=2)` removed → `K=28`.
- Multiple classes excluded: e.g., `ABSTENTION (2) + PROVENANCE (1) + SCOPE_RESOLUTION (2) = 5` → `K=25`.
- All 12 classes must be monitored for ceiling; any class with `100%` pass across both `B5`/`B4` repeats is flagged.

No R1-v3 empirical data claimed for this route — these are static design obligations.

## 13. DELTA

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`minimum_meaningful_effect_delta = 0.15` (`δ=0.15`). Smallest effect worth detecting for `B5 vs B4` discordant proportion. Ordered such that `ψ̂ > δ²` is required for the power formula to be defined. Preregistered; must not be adjusted post-hoc to achieve significance or to rescue `r_conf > 20`. Mutation test 8 in `test_validate_v3.py` / `validate_v3.py:_validate_mutations` verifies drift detection for `alpha` (and symmetrically `δ` is covered by field-presence + spec-vs-doc consistency).

## 14. ALPHA

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`alpha = 0.05` two-sided. Must not be adjusted post-hoc to achieve significance (PREREG §20; VARIANCE-PILOT §7). One-sided post-hoc switch prohibited. Mutation testing in `validate_v3.py:_validate_mutations` test 8 and `test_validate_v3.py:test_statistical_rule_mutation_detected` verifies `alpha` drift is detected. All derivations reference `z_{1−α/2}=1.959964`.

## 15. POWER

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

`target_power = 0.80`. Determines `N_pairs` via the formula in §7. Power analysis must use `ψ̂` **from the variance pilot's eligible observations** (`PSI_USES_ELIGIBLE_OBSERVATIONS`), not assumed values or `R1_V1_HISTORICAL_PSÎ=0.0000`.

## 16. COST_CEILING

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

Context budget: `6000` bytes primary tier, `secondary_tier_bytes=null` (single tier — `benchmark-spec-v3.json: context_budget`). Pilots bounded by `session_arithmetic`:

```text
maintenance_sessions = scenarios × maintained_transitions_per_scenario × maintained_arms × trajectories_per_maintained_arm
                     = 3 × 14 × 3 × 2 = 252
comparison_continuation_sessions = 5 × 30 × 4 = 600
calibration_sessions             = 1 × 30 × 4 = 120
total_variance_pilot_sessions    = 972
confirmatory_max (bounded)       ≈ K_eligible × r_conf_max × (comparison_arms + calibration_arms)
                               ≤ 30 × 20 × 6 = 3600 (plus 252 maintenance if re-run; per PREREG §21 max 3888)
```

Maintenance sessions computed as `scenarios × maintained_transitions × maintained_arms × trajectories` (MAINTENANCE-V2.md §2, §4). Validator `_validate_maintenance_arithmetic` and `_validate_session_arithmetic` prove the arithmetic.

## 17. CEILING_ROUTE

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

If the **R1-v3 variance pilot** reveals `ψ̂ ≤ δ²` (`NO_DETECTABLE_DISCORDANCE`), the study is reported as a ceiling effect:

```text
CEILING_EFFECT = YES
PRODUCT_THESIS_PASS = NOT_AUTHORIZED
PRODUCT_THESIS_FAIL = NOT_AUTHORIZED
REPORT = UNDERPOWERED_FOR_PREREGISTERED_EFFECT (if r_conf>20) or NO_DETECTABLE_DISCORDANCE (if ψ̂≤δ²)
CONTINUATION = FOUNDER_DECISION_REQUIRED (no silent continuation)
```

Canonical governance states (§23 in PREREG, VARIANCE-PILOT §11):

```text
CEILING_EFFECT = NOT_THESIS_SUPPORT
CEILING_EFFECT = NOT_THESIS_FALSIFICATION
NO_SILENT_CONTINUATION
SECOND_CEILING_THESIS_NOT_SUPPORTED = NOT_PREREGISTERED (must not be silently invented)
```

R1-v1 established this routing; R1-v3 tasks are designed harder to avoid ceiling but **no R1-v3 ceiling outcome may be claimed before `R1_V3_VARIANCE_PILOT=EXECUTED` and `R1_V3_EMPIRICAL_PSŶ=OBSERVED`**. Do not reuse `R1_V1_HISTORICAL_EVIDENCE` (`NO_DETECTABLE_DISCORDANCE` in v1 at 1.000 rates) as if it were `R1_V3_EMPIRICAL_DATA`.

## 18. FLOOR_ROUTE

**Status:** `INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL_PER_FOUNDER_DECISION_2026-09-08`

If **all arms score near zero** (floor effect), the study is reported as `UNDERPOWERED_FOR_DIFFICULTY`. Tasks are too hard for any arm, and the benchmark provides no useful signal for the preregistered `δ`.

- Must not be confused with `THESIS_FAIL` or `THESIS_SUPPORTED`.
- `B_NULL_EXCLUSION_BEFORE_PSI` still applies — floor contamination from prompt-answerable tasks must not inflate `ψ̂` or mask true floor.

R1-v3 floor risk is the designed counterpart to v1 ceiling risk (PREREG §3, §§23.2–23.3).

---

## Deterministic worked examples (static design checks — no empirical data)

All examples are static arithmetic from the preregistered rule, exercised in `bench/R1/test_r1v3_statistical_design.py` without model execution.

### Example 1: Tasks before t14 count (canonical-derived equality)

From `tasks-v2.json`:
```python
pre_t14 = sum(1 for t in tasks if t["checkpoint"] < 14)
# Result: 27
# Checkpoint distribution: {1:3, 2:3, 3:2, 4:2, 5:3, 6:2, 7:3, 8:2, 9:2, 10:3, 12:2, 14:3}
# Distinct checkpoints: 12 (t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t12,t14; t11 absent)
# Tasks at t14: 3
# Tasks before t14: 27
# Tasks at t0: 0 (no t0 checkpoint in the distribution)
```
Verification: `assert pre_t14 == 27` and `assert len({t["checkpoint"] for t in tasks}) == 12`

### Example 2: Canonical equality check

```python
spec_tasks_sorted = sorted(json.dumps(t, sort_keys=True) for t in spec["tasks"])
task_list_sorted = sorted(json.dumps(t, sort_keys=True) for t in tasks)
assert spec_tasks_sorted == task_list_sorted  # True (field-level)
```

### Example 3: Session arithmetic

From `maintenance_protocol` and `session_arithmetic`:
```python
scenarios = len(spec["scenarios"])  # 3
transitions = mp["maintained_transitions_per_scenario"]  # 14
maintained = sum(1 for a in spec["arms"].values() if a.get("maintained"))  # 3 (B1, B4, B5)
trajectories = mp["trajectories_per_maintained_arm"]  # 2
expected = scenarios * transitions * maintained * trajectories  # 252
actual = sa["maintenance_sessions"]
assert actual == expected
```

### Example 4: K_eligible edge cases (static)

```python
for excluded, eligible, route in [
    (0, 30, "nominal"),
    (1, 29, "nominal"),
    (10, 20, "nominal variant"),
    (15, 15, "AT_MINIMUM"),
    (16, 14, "UNDERPOWERED_LOW_K"),
    (30, 0,  "UNDERPOWERED_TASK_CLASS_LOSS_EXTREME"),
]:
    assert eligible == 30 - excluded
    if eligible < 15:
        assert route.startswith("UNDERPOWERED")
```

### Example 5: psi_hat edge cases (static thresholds)

Let δ=0.15, δ²=0.0225.

```python
delta=0.15; delta2=delta**2  # 0.0225
for psi_hat, expected_route in [
    (0.0,          "UNDEFINED_NO_DETECTABLE_DISCORDANCE"),
    (0.0225,       "UNDEFINED_NO_DETECTABLE_DISCORDANCE (psi_hat==delta2)"),
    (0.0226,       "DEFINED_JUST_ABOVE_THRESHOLD"),
    (0.10,         "DEFINED_MODERATE"),
    (0.50,         "DEFINED_LARGE"),
]:
    if psi_hat <= delta2:
        # formula undefined: sqrt(psi_hat - delta2) invalid
        assert "UNDEFINED" in expected_route
    else:
        raw_n = (1.959964*psi_hat**0.5 + 0.841621*(psi_hat - delta2)**0.5)**2 / delta2
        assert raw_n > 0
```

### Example 6: N_pairs floor/ceiling and r_conf min/max (static)

```python
# raw pairs computed from Example 5, then:
def bounded_r_conf(n_pairs, k_eligible):
    raw = (n_pairs + k_eligible - 1)//k_eligible if k_eligible else float("inf")
    if raw < 3: return 3
    if raw > 20: return "UNDERPOWERED_FOR_PREREGISTERED_EFFECT"
    return raw

assert bounded_r_conf(90, 30) == 3          # at floor
assert bounded_r_conf(89, 30) == 3          # raised to minimum
assert bounded_r_conf(600, 30) == 20        # at ceiling with max eligible
assert bounded_r_conf(601, 30) == "UNDERPOWERED_FOR_PREREGISTERED_EFFECT"
assert bounded_r_conf(90, 14) == 7          # K below minimum still yields r, but LOW_K_ROUTE already UNDERPOWERED
```

### Example 7: r_conf uses K_eligible, not K_total

```python
n_pairs = 120
assert (n_pairs + 30 - 1)//30 == 4   # if incorrectly using K_TOTAL
assert (n_pairs + 29 - 1)//29 == 5   # correct with one exclusion — concrete divisor effect
# Rejected: using K_TOTAL when K_ELIGIBLE=29 underpowers the confirmatory by 1 repeat/task
```

### Example 8: One task class fully excluded

```python
# e.g., ABSTENTION class has 2 tasks
k_total=30; ab_excluded=2
assert k_total - ab_excluded == 28  # remaining classes still evaluable
# Must not pool heterogeneous ceiling-masked classes to hide class-level ceiling:
# report psi_hat per class alongside pooled psi_hat
```

### Example 9: Multiple classes excluded

```python
excluded_tasks = 2 + 1 + 2  # ABSTENTION(2)+PROVENANCE(1)+SCOPE_RESOLUTION(2)=5
assert 30 - excluded_tasks == 25
# If excluded_tasks=16 → K=14 → LOW_K_ROUTE
```

---

## Evidence identities (mechanically generated — do not hand-edit)

These are computed by `bench/R1/generate_manifest.py` (deterministic SHA-256 of file bytes). Values at `WORKING_CANDIDATE` will be refreshed when `REVIEW_CANDIDATE` is frozen and bound to `bench/R1/artifact-manifest-v3.json`.

```text
CANDIDATE_COMMIT=0d206cac9a6e5ebfe3d47401aa1f081a587af60f  # WORKING — will be pinned to REVIEW_CANDIDATE at freeze
CANDIDATE_TREE=6943decf800574906b76b0abd7dc5a3460cef072   # WORKING — will be pinned to REVIEW_CANDIDATE_TREE at freeze
MODEL_CONDITION=gpt-5.6-terra / medium / 0.0 / 1024 / []
REASONING_EFFORT=medium
RUNTIME_POLICY=WARN-ON-FLOATING-ALIAS, FAIL_CLOSED_ON_DRIFT (PREREG §11–12)
SESSION_ARITHMETIC=252+600+120=972 (variance pilot)
ARTIFACT_SHA256S=see bench/R1/artifact-manifest-v3.json
MANIFEST_SHA256=see bench/R1/artifact-manifest-v3.json
R1_V1_HISTORICAL_IDENTITIES: R1_V1_CEILING_EFFECT_EVIDENCE=d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b, R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
```

---

## Review-binding invariants (enforced by `bench/R1/test_review_binding.py`)

- Candidate commit/tree in packets must equal manifest's `candidate_commit`/`candidate_tree`.
- Every artifact SHA-256 listed in manifest must equal the current file SHA-256 on the review head.
- Packet must contain correct `TASK_COUNT=30`, `ORACLE_COUNT=30`, `EVIDENCE_COUNT=96`, `CHECKPOINT_COUNT=12`, `SESSION_COUNT=972` where stated.
- Packet must reference the correct power formulas `N_pairs=ceil((z…))` and `r_conf=ceil(N_pairs/K_eligible)` — not `K(K-1)/2`.
- Packet must state `R1_V3_EMPIRICAL_DATA=NONE` and `R1_V3_VARIANCE_PILOT=NOT_EXECUTED` — never imply R1-v3 already produced data.
- `INDEPENDENT_HUMAN_REVIEW_REQUIREMENT` is `SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08` — human `PENDING` no longer blocks sealing; `R1_V3_SCIENTIFIC_DESIGN_SELF_AUDIT` and `R1_V3_STATISTICAL_DESIGN_SELF_AUDIT` must be `PASS` via deterministic tests, and `SEALED` claim without those prerequisites fails validation.

---

## References

- `bench/R1/benchmark-spec-v3.json` — statistical_parameters
- `bench/R1/PREREGISTRATION-V2.md` §§19–20, 28
- `bench/R1/VARIANCE-PILOT-V2.md` §§6–10
- `bench/R1/MAINTENANCE-V2.md` §§2,4
- `bench/R1/validate_v3.py` — `_validate_protocol_documents`, `_validate_maintenance_arithmetic`, `_validate_session_arithmetic`, `_validate_statistical_parameters`
- `bench/R1/test_r1v3_statistical_design.py` — static edge-case proof (no model execution)
