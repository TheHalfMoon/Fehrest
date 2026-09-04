# R1-v2 Independent Scientific Review Packet

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
- SPEC_002_ACTIVATION=PROHIBITED
- PRODUCT_IMPLEMENTATION=PROHIBITED

---

## 1. CONSTRUCT_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Tasks measure continuation correctness, not trivia retrieval. 12 task classes derived from structural task definitions. Prompt design tests diagnostic reasoning, not memorization.

## 2. DIFFICULTY_WITHOUT_ARTIFICIALITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Complexity from structural depth (temporal spans, required hops, cross-file synthesis, trap evidence). Preregistration v2 increased discriminating difficulty through legitimate structural complexity, not artificial model weakening. Strong baselines B0/B4 preserved.

## 3. TASK_TIMELINE_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

- TOTAL_TASKS=30
- DISTINCT_CHECKPOINTS=12 (t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t12,t14; t11 absent)
- TASKS_BEFORE_T14=27
- CHECKPOINT_SET=t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t12,t14
- ORACLES=30
- CORPUS_EVIDENCE=96
- NUM_CLASSES=12

Timeline verified against `benchmark-spec-v2.json`, `tasks-v2.json`, `oracles-v2.json`, `corpus-manifest-v2.json`. Field-level canonical equality confirmed.

## 4. TEMPORAL_LEAKAGE

**Status:** `PENDING_INDEPENDENT_REVIEW`

Corpus manifest encodes `available_from`/`available_until`/`available_from`. Validator checks future-evidence leakage via `_validate_no_future_leakage`. Mutation test 6 corrupts `available_from` to verify detection.

## 5. NO_INFORMATION_LEAKAGE

**Status:** `PENDING_INDEPENDENT_REVIEW`

Future-evidence vocabulary check implemented. Structural vocabulary subtraction enforced. `_validate_no_future_leakage` rejects tasks depending on evidence unavailable at task checkpoint.

## 6. NO_ARM_FAVORING

**Status:** `PENDING_INDEPENDENT_REVIEW`

Neutral arm identifiers (B-NULL, B0, B1, B3, B4, B5). Same model condition for all arms. Arm construction documented in `PREREGISTRATION-V2.md`. B0/B4 are strong baselines preserved without weakening.

## 7. BASELINE_FAIRNESS

**Status:** `PENDING_INDEPENDENT_REVIEW`

B0 and B4 are maintained at equal strength to B1/B3/B5 for comparison purposes. B-NULL provides the control baseline. Maintenance lag testing covers B4 and B5 only (B0/B3 unmaintained).

## 8. SCORER_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Deterministic scorer (fehrest-r1 score). Arm identity stripped before adjudication. `require_synthesis` and `require_epoch` oracles validated against corpus-backed evidence. `test_scorer.py` includes 4 adversarial tests.

## 9. ORACLE_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

30 oracles, each mapping to exactly one task. Oracle derivation evidence backed by corpus. `require_all`, `forbid`, `trap_present`, `stale_facts`, `correct_facts` fields verified. Field-level canonical equality between `benchmark-spec-v2.json.oracles` and `oracles-v2.json` confirmed.

## 10. CEILING_RISK

**Status:** `PENDING_INDEPENDENT_REVIEW`

R1-v1 pilot revealed ceiling effect (all arms perfect, 1.0000 rates). R1-v2 designed harder tasks to discriminate context strategies. Variance pilot data shows `NO_DETECTABLE_DISCORDANCE`. Ceiling risk is real but acknowledged as a finding, not thesis support.

## 11. FLOOR_RISK

**Status:** `PENDING_INDEPENDENT_REVIEW`

Floor risk exists if tasks are too difficult for the model to answer correctly. Monitor task-level pass rates. B-NULL exclusion must be applied before computing r_conf to avoid floor contamination.

## 12. MAINTENANCE_FAIRNESS

**Status:** `PENDING_INDEPENDENT_REVIEW`

Maintenance protocol: 27 of 30 tasks before t14, distributed across 12 distinct checkpoints. No maintained arm receives an omniscient free update. T0 initialization rule enforced. B0/B3 unmaintained (cost=0). Maintenance sessions derived via session_arithmetic.

## 13. MODEL_IDENTITY_ADMISSIBILITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Fail-closed policy enforced via `model_identity_admissibility`. Conditions: `returned_identity_missing`, `identity_changes_within_batch`, `maintenance_identity_not_equal_continuation_identity`, `different_identities_across_arms`, `provider_alias_drift`, `identity_metadata_malformed` all INVALIDATE_BATCH.

## 14. COST_BOUND

**Status:** `PENDING_INDEPENDENT_REVIEW`

Context budget: 6000 bytes primary tier, null secondary tier. Statistical parameters include target_power, minimum_meaningful_effect_delta, cost_ceiling. K_total=30, K_eligible documented.

## 15. REPRODUCIBILITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

All artifacts deterministic. Validator script (`bench/R1/validate.py`) reproduces checks. `bench/R1/test_validate.py` and `bench/R1/test_scorer.py` are self-contained. CI workflow `.github/workflows/bench-r1-validation.yml` runs exact-head on every PR.

## 16. FEHREST_FALSIFIABILITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

The ceiling effect (`PILOT_RESULT=NO_DETECTABLE_DISCORDANCE`) is a valid finding, not thesis support or falsification. The design harder tasks approach is falsifiable: if R1-v2 also shows ceiling, the thesis is not supported but must be re-evaluated. No silent continuation allowed.

---

## Evidence SHA-256s

- Merge commit: `f8a0dd5e9b06e137a53157e99732d71d635f9a0f`
- Implementation commit: `ec7a1eac5d6c45a8d4795b99bd1b41351dd72eef`
- Pre-bootstrap sealed R1 v1.1: `ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c`
- Evidence SHA: `d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b`
