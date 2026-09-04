# R1-v2 Independent Statistical Review Packet

**Status:** `PENDING_INDEPENDENT_REVIEW`

**Created:** 2026-09-04

**Prerequisites (all satisfied):**
- R1_V2_MACHINE_VALIDATION=PASS
- R1_V2_VALIDATION_CONVERGENCE=COMPLETE
- R1_V2_MUTATION_TESTING=PASS
- R1_V2_EXACT_HEAD_CI=PASS
- `python bench/R1/validate.py`, `test_validate.py`, `test_scorer.py` all pass on main
- PR #34 merged into main (commit f8a0dd5)

**Hard boundaries (must not be violated):**
- R1_V2_MODEL_EXECUTION=PROHIBITED
- R1_V2_VARIANCE_PILOT_EXECUTION=PROHIBITED
- R1_V2_CONFIRMATORY_EXECUTION=PROHIBITED
- R1_V2_UNBLINDING=PROHIBITED
- R1_V2_STATISTICAL_REVIEW=PENDING
- Product implementation PROHIBITED

---

## 1. PAIRING_UNIT

**Status:** `PENDING_INDEPENDENT_REVIEW`

The pairing unit is the task. Each task has one oracle (1:1 mapping). 30 tasks × 1 oracle each. The B-NULL arm is excluded from r_conf computation per §28 ordering.

## 2. B_NULL_EXCLUSION_ORDER

**Status:** `PENDING_INDEPENDENT_REVIEW`

B-NULL exclusion must be applied BEFORE computing r_conf. Verified in `PREREGISTRATION-V2.md` §28.1 and `VARIANCE-PILOT-V2.md` §10.1. The validator checks this ordering via `_validate_protocol_documents`. Mutation test for B-NULL ordering drift included in `test_validate.py`.

## 3. K_TOTAL

**Status:** `PENDING_INDEPENDENT_REVIEW`

K_total = 30 (tasks). Verified from `benchmark-spec-v2.json`, `tasks-v2.json`, and `statistical_parameters.K_total`. All 30 tasks have exactly 1 oracle each.

## 4. K_ELIGIBLE

**Status:** `PENDING_INDEPENDENT_REVIEW`

K_eligible = K_total minus excluded tasks. B-NULL is excluded from r_conf computation. Exact K_eligible depends on the exclusion rule specification. Must be computed after B-NULL exclusion is applied.

## 5. PSI_HAT

**Status:** `PENDING_INDEPENDENT_REVIEW`

ψ̂ (psi_hat) is the population effect size estimate. From R1-v1 pilot: ψ̂ = 0.0000 for all arm pairs (ceiling effect). R1-v2 must re-estimate ψ̂ with harder tasks. Current status: PENDING (requires variance pilot data).

## 6. MCNEMAR

**Status:** `PENDING_INDEPENDENT_REVIEW`

McNemar's test for paired nominal data. Used to detect discordant pairs between arms. R1-v1 showed 0 discordant pairs across all contrasts (NO_DETECTABLE_DISCORDANCE). R1-v2 must re-run with the harder task corpus.

## 7. N_PAIRS

**Status:** `PENDING_INDEPENDENT_REVIEW`

N_pairs = K_eligible × (K_eligible - 1) / 2 for pairwise contrasts. With B-NULL excluded, the number of eligible arms is 5 (B0, B1, B3, B4, B5), yielding 10 pairwise contrasts. Each contrast has K_eligible pairs of task-oracle judgments.

## 8. R_CONF

**Status:** `PENDING_INDEPENDENT_REVIEW`

r_conf (confidence in the result) is computed per the formula in `statistical_parameters.r_conf_formula`. The formula accounts for ψ̂, N_pairs, and the B-NULL exclusion. From R1-v1: r_conf was computed but ceiling effects dominated.

## 9. R_CONF_MIN

**Status:** `PENDING_INDEPENDENT_REVIEW`

r_conf_minimum is documented in `statistical_parameters.r_conf_minimum`. Must be satisfied before any product thesis verdict.

## 10. R_CONF_MAX

**Status:** `PENDING_INDEPENDENT_REVIEW`

r_conf_maximum is documented in `statistical_parameters.r_conf_maximum`. Defines the ceiling of confidence achievable with the given sample size.

## 11. LOW_K_ROUTE

**Status:** `PENDING_INDEPENDENT_REVIEW`

If K_eligible is too low for statistical power, the LOW_K_ROUTE applies: either increase task count or accept the route as a limitation. R1-v2 has 30 tasks with 27 before t14 for maintenance lag testing.

## 12. TASK_CLASS_LOSS_ROUTE

**Status:** `PENDING_INDEPENDENT_REVIEW`

If certain task classes show ceiling effects (all tasks pass), the TASK_CLASS_LOSS_ROUTE applies: those classes are excluded from analysis or the task design is revised. 12 task classes must be individually monitored for ceiling risk.

## 13. DELTA

**Status:** `PENDING_INDEPENDENT_REVIEW`

minimum_meaningful_effect_delta is documented in `statistical_parameters.minimum_meaningful_effect_delta`. Defines the smallest effect worth detecting. Must be set before variance pilot execution.

## 14. ALPHA

**Status:** `PENDING_INDEPENDENT_REVIEW`

alpha (significance level) is documented in `statistical_parameters.alpha`. Default: 0.05. Must not be adjusted post-hoc to achieve significance. Mutation testing in `test_validate.py` verifies alpha is not silently mutated.

## 15. POWER

**Status:** `PENDING_INDEPENDENT_REVIEW`

target_power is documented in `statistical_parameters.target_power`. Determines required N. Must be computed before confirmatory sample size. Power analysis must use ψ̂ from variance pilot, not assumed values.

## 16. COST_CEILING

**Status:** `PENDING_INDEPENDENT_REVIEW`

Cost ceiling documented in `specs/CURRENT.md`. Context budget: 6000 bytes primary tier. Total variance pilot sessions bounded by session_arithmetic. Maintenance sessions computed as: scenarios × maintained_transitions × maintained_arms × trajectories.

## 17. CEILING_ROUTE

**Status:** `PENDING_INDEPENDENT_REVIEW`

If ceiling effect is confirmed (all arms perfect), the CEILING_ROUTE applies: design harder benchmark. New preregistration required. Do NOT reinterpret as thesis support or falsification. R1-v1 established this route. R1-v2 tasks are designed harder to avoid ceiling.

## 18. FLOOR_ROUTE

**Status:** `PENDING_INDEPENDENT_REVIEW`

If floor effect is confirmed (all tasks fail), the FLOOR_ROUTE applies: reduce difficulty or redesign tasks. Must not be confused with thesis falsification. B-NULL exclusion must be applied before computing r_conf to avoid floor contamination.

---

## Deterministic Worked Examples

### Example 1: Tasks before t14 count

From `tasks-v2.json`:
```python
pre_t14 = sum(1 for t in tasks if t["checkpoint"] < 14)
# Result: 27
# Checkpoint distribution: {1:3, 2:3, 3:2, 4:2, 5:3, 6:2, 7:3, 8:2, 9:2, 10:3, 12:2, 14:3}
# Distinct checkpoints: 12
# Tasks at t14: 3 (t14 checkpoint)
# Tasks before t14: 27
# Tasks at t0: 0 (no t0 checkpoint in the distribution)
```

Verification: `assert pre_t14 == 27` and `assert len({t["checkpoint"] for t in tasks}) == 12`

### Example 2: Canonical equality check

```python
spec_tasks_sorted = sorted(json.dumps(t, sort_keys=True) for t in spec["tasks"])
task_list_sorted = sorted(json.dumps(t, sort_keys=True) for t in tasks)
assert spec_tasks_sorted == task_list_sorted  # True
```

### Example 3: Session arithmetic

From `maintenance_protocol` and `session_arithmetic`:
```python
scenarios = len(spec["scenarios"])  # e.g., S1-S6
transitions = mp["maintained_transitions_per_scenario"]  # 14
maintained = sum(1 for a in spec["arms"].values() if a.get("maintained"))  # 3 (B1, B4, B5)
trajectories = mp["trajectories_per_maintained_arm"]  # 2
expected = scenarios * transitions * maintained * trajectories
actual = sa["maintenance_sessions"]
assert actual == expected
```

---

## Evidence SHA-256s

- Merge commit: `f8a0dd5e9b06e137a53157e99732d71d635f9a0f`
- Implementation commit: `ec7a1eac5d6c45a8d4795b99bd1b41351dd72eef`
- Pre-bootstrap sealed R1 v1.1: `ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c`
- Evidence SHA: `d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b`
