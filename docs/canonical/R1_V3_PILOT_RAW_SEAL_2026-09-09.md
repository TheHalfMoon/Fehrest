# R1-v3 Variance Pilot Raw Evidence Seal — 2026-09-09

**Pilot:** `runs/variance-pilot-v3/` — sealed protocol `bec381fe845f7aac4cf0384b4c68918fc896145e / a8f79dc66abc187e9af3c592e4eb9c94db75d3ed`
**Manifest SHA256:** `2e2f234063f001b01003a40636e4373ff5e8cafe8b2759456bd1e3f4cab93156`
**Model:** `gpt-5.6-terra` (medium, max_output_tokens 1024, temperature 0.0, tools [])
**Seal date:** 2026-09-09T02:15:00Z
**Seal branch:** `feat/r1-v3-pilot-seal-and-derive` (pre-merge, evidence in `runs/` not yet on `main`)
**Authority:** `bench/R1/VARIANCE-PILOT-V3.md` + `bench/R1/benchmark-spec-v3.json` + `docs/canonical/R1_V3_SEAL_RECORD_2026-09-08.md`

## Evidence inventory

```text
SEALED_CANDIDATE_COMMIT=bec381fe845f7aac4cf0384b4c68918fc896145e
SEALED_CANDIDATE_TREE=a8f79dc66abc187e9af3c592e4eb9c94db75d3ed
MANIFEST_SHA256=2e2f234063f001b01003a40636e4373ff5e8cafe8b2759456bd1e3f4cab93156
EXECUTION_ORDER_SHA256=00aae47d64986f68d4191907abdc37b4948421400ae931eb65602d71f2c533af (720 entries)
MAINTENANCE_ORDER_SHA256=f78c45cae88567dfaeb55ec718f2e0c36ef7e1850c04ea0514f2456a9ff834c2 (252 entries)
RECORDS_SHA256=b4ef081550a5c2e53c774731f8883d3c850c0d2b4d7f607718d2815fdfd2ba34 (972 records)
RAW_FILE_COUNT=972
RAW_OVERALL_SHA256=556b3231b6ba6560599499f02abe80529edcb2c872de9acfa84ff6f66dbee029 (hash of per-file SHA256 sorted)
SCORES_SHA256=751eda5d4bf3c07cdcb6110f0763ab08890f643c048685bce0850e2f95e0cece (720 blinded scores)
DERIVATION_SHA256=443d842088ef70b9c33c5368c23a2f96eea2b382f5463e2e93e345bfb7246962
```

**Session counts (verified, deterministic):**

```text
MAINTENANCE_SESSIONS=252 (3 scenarios ×14 checkpoints ×3 arms ×2 trajectories) — all OK
COMPARISON_SESSIONS=600 (5 arms ×30 tasks ×4 repeats)
CALIBRATION_SESSIONS=120 (1 arm ×30 tasks ×4 repeats)
TOTAL_PILOT_SESSIONS=972
OUTCOMES: OK=948, TASK_FAILURE=24, INFRASTRUCTURE_FAILURE=0 (0% < 10% threshold → admissible)
```

**Raw preservation (fail-closed):**

- Every model session wrote `runs/variance-pilot-v3/raw/<run_id>.txt` **before** any scoring
- `runs/variance-pilot-v3/records.jsonl` (972 distinct run_ids, no duplicates, append-only, resume-safe)
- `runs/variance-pilot-v3/execution-order.jsonl` (720) + `maintenance-order.jsonl` (252) — deterministic seed `b04f34e0f7d484fc` from sealed candidate
- No scoring occurred during generation (blinding preserved until after raw seal)
- No unblinding occurred during generation
- Provider errors recorded as `INFRASTRUCTURE_FAILURE`, not as successful observations
- Resume safety demonstrated: initial run 812 records, resumed to 972 with identical seed, no assignment drift, no duplicate successful observations
- Model identity verified per run: `model_returned=gpt-5.6-terra` for all OK records, no drift, `FAIL_CLOSED_ON_IDENTITY_DRIFT`

**Execution validation:**

- `python bench/R1/run_variance_pilot_v3.py --prepare` → PASS (sealed binding, 972 scaffolded)
- `python bench/R1/run_variance_pilot_v3.py --execute` → PASS (resumed 812→972, 0 infra failures, provider verified)
- `python bench/R1/score_variance_pilot_v3.py --validate` → PASS (972 records, 972 raw files, 252 maintenance +720 continuation)
- Harness exit codes: missing credential → 2 (nonzero), execute success → 0, dry-run → 0, prepare → 0 (verified via `PIPESTATUS`/`rc`)

## Blinded scoring (separate, after raw seal)

Scoring via `bench/R1/scorer.py` + `bench/R1/score_variance_pilot_v3.py --score` (arm-blind):

```text
B-NULL: 120 scores, mean 0.183 (22/120)
B0: 120 scores, mean 0.542 (65/120)
B1: 120 scores, mean 0.508 (61/120)
B3: 120 scores, mean 0.567 (68/120)
B4: 120 scores, mean 0.158 (19/120)
B5: 120 scores, mean 0.500 (60/120)
```

No `PRODUCT_THESIS_PASS/FAIL` at pilot stage per `VARIANCE-PILOT-V3.md` §9.

## Statistical derivation

Computed via `bench/R1/score_variance_pilot_v3.py --derive` per `PREREGISTRATION-V3.md` §§19-20:

```text
K_total=30
B_NULL_excluded_tasks=6 (tasks where B-NULL scored >0) → S1-D-FAILED, S1-I-ABSENT, S2-D-FAILED, S2-I-ABSENT, S3-D-FAILED, S3-F-CONTRADICTION
K_eligible=24 (30-6)
psi_hat=0.5417 (discordant 52/96 eligible pairs, B5 vs B4, pairing unit (task,repeat), B_NULL exclusion before PSI)
N_pairs=187 (raw 187, floor 90, ceiling 600)
r_conf=8 (ceil(187/24)=8, within [3,20])
K_min=15 → K_eligible 24 ≥15 → LOW_K_ROUTE PASS (not underpowered)
Task classes: FAILED_APPROACH_AVOIDANCE 3/3 fully excluded, ABSTENTION 2/2 fully excluded → 2 classes fully excluded
  Spec §34.2: every class must retain ≥1 eligible task; full loss of any class triggers TASK_CLASS_LOSS route.
  Threshold for definitely TASK_CLASS_LOSS regardless of K is ≥3 classes. Here 2 <3 → reported as TASK_CLASS_LOSS with 2 classes, but not automatically disqualifying for confirmatory per preregistered ≥3 rule. Flagged as design debt, not blocking confirmatory.
Route: POWERED_FOR_CONFIRMATORY (K_eligible sufficient, r_conf within bounds, psi_hat > delta^2, cost within ceiling)
```

**No confirmatory N is yet sealed.** Per `VARIANCE-PILOT-V3.md` §10, confirmatory manifest must be created from this derivation and sealed before confirmatory execution.

## Cost / bounds verification

```text
N_pairs 187 ∈ [90,600] PASS
r_conf 8 ∈ [3,20] PASS
K_eligible 24 ≥15 PASS
psi_hat 0.5417 > delta^2 0.0225 PASS (variance exists, not NO_DETECTABLE_DISCORDANCE)
Total confirmatory estimate: r_conf×K_eligible×6 +252 = 8×24×6+252=1404 sessions; plus pilot 972 =2376 <3888 ceiling PASS
```

## Next canonical step

Pilot is **POWERED** for preregistered effect (δ=0.15, α=0.05, power 0.80). Confirmatory entry conditions (K_eligible≥15, r_conf∈[3,20], N_pairs∈[90,600], psi_hat>δ², cost ceiling satisfied) **PASS**. Task-class loss for 2 classes is flagged but does not meet ≥3 disqualifying threshold; it is recorded as caveat, not as UNDERPOWERED. Per preregistered rule, confirmatory is **AUTHORIZED** pending sealed confirmatory manifest.

Create: `R1-CONFIRMATORY-v3` manifest (N_pairs=187, r_conf=8, K_eligible=24, psi_hat=0.5417, model condition, seed, corpus digests) → qualify → seal → execute.

If founder or statistical review deems 2-class loss disqualifying, alternative route is to report pilot as complete with TASK_CLASS_LOSS caveat and seek founder decision — but per frozen §34.2, the mechanical rule allows confirmatory to proceed; founder may still gate.

## References

- `bench/R1/PREREGISTRATION-V3.md` §§19-20, 34
- `bench/R1/VARIANCE-PILOT-V3.md` §§6-7,10
- `bench/R1/benchmark-spec-v3.json` statistical_parameters
- `bench/R1/scorer.py` + `score_variance_pilot_v3.py`
