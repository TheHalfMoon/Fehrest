# R1-v3 Confirmatory Raw Evidence Seal — 2026-09-09

**Confirmatory:** `runs/confirmatory-v3/` — derived from pilot `556b32...` (K_eligible 24, r_conf 8)
**Manifest:** `bench/R1/confirmatory-manifest-v3.json` (1404 sessions, N_pairs 187, psi_hat 0.5417)
**Model:** `gpt-5.6-terra` medium 0.0 1024 (same as pilot, no drift)
**Seal date:** 2026-09-09T03:30:00Z
**Branch:** `feat/r1-v3-terminal-verdict` (pre-merge)
**Authority:** `bench/R1/PREREGISTRATION-V3.md` §§19-20 + `docs/canonical/R1_V3_CONFIRMATORY_PLAN_2026-09-09.md`

## Evidence inventory

```text
CONFIRMATORY_MANIFEST_SHA256=1b8da0d... (bench/R1/confirmatory-manifest-v3.json)
PILOT_DERIVATION_SHA256=443d842088ef70b9c33c5368c23a2f96eea2b382f5463e2e93e345bfb7246962
EXECUTION_ORDER_SHA256=25f076a83ce376c93b668ec08e9a1fcd592fd5569f00f9ebe1f4d39f9aa7ac39 (1152 entries, 24 tasks ×6 arms ×8 repeats)
MAINTENANCE_ORDER_SHA256=f78c45cae88567dfaeb55ec718f2e0c36ef7e1850c04ea0514f2456a9ff834c2 (252 entries)
RECORDS_SHA256=88cd871bf9acd1fd4e5276442f5d6c1a673c9063ab165a2eff97119f6f43a08d (1404 records)
RAW_FILE_COUNT=1404
RAW_OVERALL_SHA256=05443fe6ba7b1e680b9ddaeebcec9859ebd31f3ba6b0187d8942f4a1f99737a0 (hash of per-file SHA256 sorted)
SCORES_SHA256=c432f0cff8a88602f1fc0edfb3c019d5f31ee5844ab23c56278b47ac1630ac64 (1152 blinded scores)
```

**Session counts (verified, deterministic):**

```text
MAINTENANCE_SESSIONS=252 (3×14×3×2) — all OK
COMPARISON_SESSIONS=960 (5×24×8)
CALIBRATION_SESSIONS=192 (1×24×8)
TOTAL_CONFIRMATORY_SESSIONS=1404
OUTCOMES: OK=1387, TASK_FAILURE=17, INFRASTRUCTURE_FAILURE=0 (0% <10% threshold → admissible)
```

**Raw preservation (fail-closed):**

- Every model session wrote `runs/confirmatory-v3/raw/<run_id>.txt` before scoring
- `runs/confirmatory-v3/records.jsonl` (1404 distinct run_ids, resume-safe, 820→1404)
- `runs/confirmatory-v3/execution-order.jsonl` (1152) + `maintenance-order.jsonl` (252) — seed `b04f34e0f7d484fc`
- No scoring during generation, no unblinding, no pooling with pilot
- Model identity verified per run: `model_returned=gpt-5.6-terra` for all OK, no drift

**Validation:**

- `python bench/R1/run_confirmatory_v3.py --prepare` → PASS (1152+252)
- `python bench/R1/run_confirmatory_v3.py --execute` → PASS (resumed 820→1404, 0 infra)
- Raw completeness: 1404 records, 1404 raw files, distinct run_ids, no missing

## Blinded scoring (after raw seal)

Via `scorer.py` (arm-blind):

```text
B-NULL: 192 scores, mean 0.000 (0/192) — no prompt leakage for eligible 24
B0: 192 scores, mean 0.547 (105/192)
B1: 192 scores, mean 0.573 (110/192)
B3: 192 scores, mean 0.547 (105/192)
B4: 192 scores, mean 0.000 (0/192) — floor effect for wiki baseline
B5: 192 scores, mean 0.557 (107/192)
```

No thesis verdict at scoring stage.

## Cost verification

```text
Pilot 972 + Confirmatory 1404 = 2376 <3888 ceiling PASS
r_conf 8∈[3,20], N_pairs 187∈[90,600], K_eligible 24≥15 PASS
```
