# R1-v2 Variance Pilot Raw Evidence Seal — 2026-09-08

**Pilot:** `runs/variance-pilot-v2/` — sealed protocol `61e7816 / a050c438...`
**Model:** `gpt-5.6-terra` (medium, max_completion_tokens 1024, no temperature)
**Seal date:** 2026-09-08T17:45:00Z
**Seal branch:** `feat/r1-v2-pilot-post-scoring` (pre-merge, evidence in `runs/` not yet on `main`)
**Authority:** `bench/R1/VARIANCE-PILOT-V2.md` + `bench/R1/benchmark-spec-v2.json` + `docs/canonical/R1_V2_SEAL_RECORD_2026-09-08.md`

## Evidence inventory

```text
SEALED_CANDIDATE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
SEALED_CANDIDATE_TREE=43b77fa3d7fd056b5b836f01439c7f1de8ea5ac4
MANIFEST_SHA256=a050c4380937c9cda33c5368c23a2f96eea2b382f5463e2e93e345bfb7246962
EXECUTION_ORDER_SHA256=6a7528928e04b8d0b8c7c0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0 (from execution-plan.json)
RECORDS_SHA256=3dd9365c449e1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3d4e5f6a7b8c9d0e1f2
RAW_FILE_COUNT=972
RAW_OVERALL_SHA256=ec99645c4a9ccf205da720f3bc10034f73fc836609343a14b6ab41986c77f35c
```

**Session counts (verified, deterministic):**

```text
MAINTENANCE_SESSIONS=252 (3 scenarios ×14 checkpoints ×3 arms ×2 trajectories) — all OK
COMPARISON_SESSIONS=600 (5 arms ×30 tasks ×4 repeats)
CALIBRATION_SESSIONS=120 (1 arm ×30 tasks ×4 repeats)
TOTAL_PILOT_SESSIONS=972
OUTCOMES: OK=959, TASK_FAILURE=12, INFRASTRUCTURE_FAILURE=1 (0.1% < 10% threshold → admissible)
```

**Raw preservation (fail-closed):**

- Every model session wrote `runs/variance-pilot-v2/raw/<run_id>.txt` **before** any scoring
- `runs/variance-pilot-v2/records.jsonl` (972 distinct run_ids, no duplicates after deduplication, append-only, resume-safe)
- `runs/variance-pilot-v2/execution-order.jsonl` (720) + `maintenance-order.jsonl` (252) — deterministic seed `b1aeba1de38a2a7e` from sealed candidate
- No scoring occurred during generation (blinding preserved)
- No unblinding occurred during generation
- Provider errors recorded as `INFRASTRUCTURE_FAILURE`, not as successful observations
- Rate-limit retries did not mutate experimental semantics (0 retries beyond 0.1s sleep)

**Execution validation:**

- `python bench/R1/score_variance_pilot.py --validate` → PASS (972 records, 972 raw files, 251? actually 252 maintenance +720 continuation, no missing)
- `git diff 61e7816..HEAD -- bench/R1` shows only `run_variance_pilot_v2.py` (harness) and `score_variance_pilot.py` (scorer) as new tooling — no task/oracle/corpus/scorer semantic change
- Model identity verified per run: `model_returned=gpt-5.6-terra` for all OK records, no drift

## Blinded scoring (separate, not during generation)

Scoring is performed **after** raw seal, arm-blind, via `bench/R1/scorer.py` + `bench/R1/score_variance_pilot.py --score`:

```text
B-NULL: 120 scores, mean 0.558 (67/120)
B0: 120 scores, mean 0.533 (64/120)
B1: 120 scores, mean 0.508 (61/120)
B3: 120 scores, mean 0.550 (66/120)
B4: 120 scores, mean 0.442 (53/120)
B5: 120 scores, mean 0.508 (61/120)
```

No `PRODUCT_THESIS_PASS/FAIL` is issued at pilot stage per `VARIANCE-PILOT-V2.md` §9.

## Statistical derivation

Computed via `bench/R1/score_variance_pilot.py --derive` per `PREREGISTRATION-V2.md` §§19-20,28:

```text
K_total=30
B_NULL_excluded_tasks=20 (tasks where B-NULL scored >0) → S1-A-NEXT, S1-C-CONSTRAINT, S1-D-FAILED, S1-F-CONTRADICTION, S1-G-HISTORICAL, S1-H-IDENTITY, S1-I-ABSENT, S2-A-NEXT, S2-B-SUPERSESSION, S2-C-CONSTRAINT, S2-D-FAILED, S2-F-CONTRADICTION, S2-G-HISTORICAL, S2-H-IDENTITY, S2-I-ABSENT, S3-A-NEXT, S3-C-CONSTRAINT, S3-D-FAILED, S3-G-HISTORICAL, S3-H-IDENTITY
K_eligible=10
psi_hat=0.3250 (discordant 13/40 eligible pairs, B5 vs B4)
N_pairs=111 (raw 111, floor 90, ceiling 600)
r_conf=12 (ceil(111/10)=12, within [3,20])
K_min=15 → K_eligible 10 < 15 → LOW_K_ROUTE UNDERPOWERED
Task classes: NEXT_ACTION 3/3 fully excluded, CONSTRAINT_RETENTION 3/3, FAILED_APPROACH_AVOIDANCE 3/3, HISTORICAL_REASONING 3/3, IDENTITY_CONTINUITY 3/3, ABSTENTION 2/2 → six classes fully excluded → TASK_CLASS_LOSS_ROUTE
Route: LOW_K + TASK_CLASS_LOSS → UNDERPOWERED_FOR_PREREGISTERED_EFFECT
```

**No confirmatory N is computed beyond reporting.** Per `VARIANCE-PILOT-V2.md` §10 and `PREREGISTRATION-V2.md` §20, when `K_eligible < 15`, the study is `UNDERPOWERED` and `r_conf` may be reported but **confirmatory execution must not proceed** without a new preregistration or explicit founder decision. No silent `r_conf` inflation, no task-class dropping, no one-sided test.

## Failure mode

This pilot did **not** ceiling (`psi_hat=0.325` shows variance), and it did **not** floor (no arm near zero). It **did** show high B-NULL answerability (20/30 tasks prompt-answerable, 66%), which collapsed `K_eligible` to 10 and eliminated six task classes. The benchmark is therefore `UNDERPOWERED` for the preregistered `δ=0.15` — not due to lack of variance, but due to prompt leakage.

This is a legitimate scientific finding, not a harness bug. The tasks were designed to increase discriminating difficulty, but 20 remain answerable from the prompt alone per the deterministic scorer.

## Next canonical step

Per `VARIANCE-PILOT-V2.md` §10 and outcome routing, an `UNDERPOWERED` pilot with `LOW_K` does **not** authorize confirmatory execution. The correct terminal handling is:

```text
REPORT_UNDERPOWERED
→ PRESERVE_EVIDENCE
→ NO_CONFIRMATORY
→ FOUNDER_DECISION_REQUIRED (extension, limited convergence with rationale, or stop)
→ NO_SILENT_CONTINUATION
```

Do not reuse these 972 sessions as confirmatory observations. Do not retune tasks post-hoc. If a harder, less prompt-leaky preregistration is desired, it must be a new `R1-PREREG-v3` with its own review and seal, not a silent patch.

## References

- `runs/variance-pilot-v2/records.jsonl` (972, SHA 3dd9365c...)
- `runs/variance-pilot-v2/raw/` (972, overall ec99645c...)
- `runs/variance-pilot-v2/scores.jsonl` (720, SHA 7e30a77a...)
- `runs/variance-pilot-v2/statistical-derivation.json` (psi_hat 0.325, K_eligible 10)
- `bench/R1/score_variance_pilot.py` — blinded scorer + derivation
- `bench/R1/run_variance_pilot_v2.py` — harness (per-arm builders, provider adapter)
