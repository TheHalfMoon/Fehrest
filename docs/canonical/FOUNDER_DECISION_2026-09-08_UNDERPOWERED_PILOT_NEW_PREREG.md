# Founder Decision — Underpowered Variance Pilot (LOW_K) → New Preregistration

**Date:** 2026-09-08T18:00:00Z
**Decision ID:** `FOUNDER_DECISION=UNDERPOWERED_PILOT_NEW_PREREG_V3`
**Authority:** Founder (Class E — product thesis/founder direction per `AGENTS.md` §5)
**Branch:** `governance/underpowered-pilot-founder-decision`
**Live base:** `bda84de20194cc00ec03cb0b6dd217d651031456`
**Pilot evidence:** `runs/variance-pilot-v2/` — 972 sessions, raw seal `ec99645c...`, 20/30 B-NULL excluded, K_eligible=10

## Pilot finding

```text
K_total=30
B_NULL_excluded=20 (66% prompt-answerable)
K_eligible=10 < minimum_K=15 → LOW_K_ROUTE UNDERPOWERED
psi_hat=0.3250 (13/40 discordant B5 vs B4, not ceiling, not floor)
N_pairs=111, r_conf=12 (within bounds, but K too low)
Task classes fully excluded: NEXT_ACTION 3/3, CONSTRAINT_RETENTION 3/3, FAILED_APPROACH_AVOIDANCE 3/3, HISTORICAL_REASONING 3/3, IDENTITY_CONTINUITY 3/3, ABSTENTION 2/2 → TASK_CLASS_LOSS
Route: UNDERPOWERED_FOR_PREREGISTERED_EFFECT
```

The pilot **did not** ceiling (`psi_hat=0.325` shows variance) and **did not** floor (no arm near zero). It **did** show high B-NULL answerability, collapsing `K_eligible` and eliminating six task classes. The benchmark as currently preregistered is therefore `UNDERPOWERED` for `δ=0.15` — not due to lack of variance, but due to prompt leakage.

This is a legitimate scientific finding, not a harness bug. The tasks were designed to increase discriminating difficulty over R1-v1, but 20 remain answerable from the prompt alone per the deterministic scorer.

## Decision

```text
ROUTE=NEW_PREREGISTRATION_V3
REASON=LOW_K_DUE_TO_B_NULL_PROMPT_LEAKAGE
PRIOR_PILOT_EVIDENCE=PRESERVED_AS_IMMUTABLE (runs/variance-pilot-v2/, raw seal ec9964..., 972 sessions, not reused as confirmatory)
CONFIRMATORY_EXECUTION=AUTHORIZED_ONLY_AFTER_NEW_PREREGISTRATION_SEAL
SILENT_CONTINUATION=NO
```

**Authorized:**

1. Design `R1-PREREG-v3` with **harder, less prompt-leaky tasks** that reduce B-NULL answerability while preserving the sealed statistical design (pairing unit, McNemar, N_pairs formula, R_CONF bounds, etc.).
2. Preserve the `UNDERPOWERED` pilot as immutable prior evidence — do not overwrite, retroactively modify, or reuse its observations as confirmatory.
3. Repository-local governance, specification, design, static validation, review (now optional per 2026-09-08 supersession), CI, and sealing work for the new preregistration.
4. Strong simple baselines remain unweakened — do not weaken B0/B4 to create separation.

**Not authorized:**

- Executing a confirmatory with `K_eligible=10` (violates `minimum_K=15`)
- Silently dropping task classes or relaxing `δ/α` to rescue `r_conf`
- Reusing pilot sessions as confirmatory observations
- Activating Spec 002 merely because the pilot was underpowered

## New R1 Review Policy (unchanged from 2026-09-08 supersession)

```text
HUMAN_INDEPENDENT_REVIEW=OPTIONAL
HUMAN_REVIEW_BLOCKING_AUTHORITY=NO
ENGINEERING_VALIDATION_REQUIRED=YES
DETERMINISTIC_TESTS_REQUIRED=YES
EXACT_CANDIDATE_BINDING_REQUIRED=YES
MANIFEST_VALIDATION_REQUIRED=YES
EXACT_HEAD_CI_REQUIRED=YES
SCIENTIFIC_DESIGN_SELF_AUDIT_REQUIRED=YES
STATISTICAL_DESIGN_SELF_AUDIT_REQUIRED=YES
ADVERSARIAL_VALIDATION_REQUIRED=YES
FAIL_CLOSED_ON_TEST_OR_DESIGN_FAILURE=YES
```

New preregistration will be sealed via internal qualification, not mandatory external human review.

## Change-control class

Class E (product thesis/founder direction) per `AGENTS.md` §5. This decision does not change the Architecture Freeze F-CORE* non-negotiables; it authorizes a new preregistration to address prompt leakage, not a product behavior mutation.

## Preservation

- Pilot evidence `runs/variance-pilot-v2/` (972, raw seal ec9964..., 720 scores, derivation) remains immutable and is **not** used for confirmatory.
- Sealed candidate `61e7816 / a050c43...` and its manifest remain the authority for the pilot; new preregistration will derive from it without mutating its bytes.
- Deterministic binding, manifest, stale-review, and fail-closed protections remain.

## Next gate

```text
ACTIVE_R1_SUBGATE=R1_V3_PREREGISTRATION_DESIGN_AUTHORIZED
NEXT_ACTION=DESIGN_R1_PREREG_V3_WITH_REDUCED_B_NULL_LEAKAGE
```

Follow `AGENTS.md` engineering method: SPEC → CLARIFY → PLAN → CHECKLIST → TASKS → ANALYZE → PONYTAIL → IMPLEMENT → TEST → BENCHMARK → SECURITY → REVIEW → CONVERGE. New preregistration must be validated via `bench/R1/validate.py`, `test_*`, `generate_manifest --check`, and exact-head CI before sealing.

## References

- `runs/variance-pilot-v2/statistical-derivation.json` — K_eligible 10, LOW_K, TASK_CLASS_LOSS
- `docs/canonical/R1_V2_PILOT_RAW_SEAL_2026-09-08.md` — raw seal ec9964...
- `bench/R1/benchmark-spec-v2.json` — K_total 30, pairing unit (task,repeat), N_pairs formula
- `docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md` — prior supersession
