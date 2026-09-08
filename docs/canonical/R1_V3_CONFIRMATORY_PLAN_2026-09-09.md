# R1-v3 Confirmatory Plan — 2026-09-09

**Derived from:** `runs/variance-pilot-v3/statistical-derivation.json` (pilot powered)
**Pilot:** 972 sessions, K_eligible 24, psi_hat 0.5417, N_pairs 187, r_conf 8, raw seal 556b32...
**Manifest:** `bench/R1/confirmatory-manifest-v3.json`
**Model:** `gpt-5.6-terra` medium 0.0 1024 (same as pilot, no drift)
**Seed:** `b04f34e0f7d484fc` (derived from sealed candidate bec381f + manifest 2e2f..., same as pilot, blocked+interleaved)

## Confirmatory session arithmetic (frozen)

```text
K_total=30
B_NULL_excluded=6 (S1-D-FAILED, S1-I-ABSENT, S2-D-FAILED, S2-I-ABSENT, S3-D-FAILED, S3-F-CONTRADICTION)
K_eligible=24
r_conf=8 (ceil(187/24))
N_pairs=187 (from psi_hat 0.5417, delta 0.15, alpha 0.05, power 0.80)
psi_hat=0.5417 (52/96 eligible discordant pairs, B5 vs B4)

Maintenance: 252 (3×14×3×2, task-blind, same evidence bundle per checkpoint)
Comparison continuation: 5×24×8 = 960
Calibration continuation: 1×24×8 = 192
Total continuation: 1152
Total confirmatory: 1404 (252+1152)
Pilot 972 + Confirmatory 1404 = 2376 < 3888 ceiling PASS
```

**Eligible tasks (24):** all 30 minus the 6 B-NULL excluded. The 2 fully excluded classes (FAILED_APPROACH_AVOIDANCE 3/3, ABSTENTION 2/2) are excluded via B-NULL, not via additional filtering. Remaining classes: NEXT_ACTION, SUPERSESSION_AVOIDANCE, CONSTRAINT_RETENTION, SCOPE_RESOLUTION, CONTRADICTION_HANDLING (partial), HISTORICAL_REASONING, IDENTITY_CONTINUITY, PROVENANCE, CROSS_FILE_SYNTHESIS, EPOCH_BOUNDARY — all retain ≥1 eligible task.

**Design debt flagged:** 2 classes fully excluded, but <3 threshold per PREREGISTRATION-V3 §34.2, not disqualifying. Confirmatory remains powered, but task-class coverage caveat recorded.

## Execution order

Blocked and interleaved, deterministic seed `b04f34e0f7d484fc`, same algorithm as pilot but with `r_conf=8` and eligible task set:

```
for repeat_index in 1..=8:
  for task in permute(eligible_24_tasks, seed, repeat_index):
    for arm in permute([B-NULL,B0,B1,B3,B4,B5], seed, repeat_index, task):
      run(arm, task, repeat_index)
```

Maintenance interleaved per checkpoint before continuation at that checkpoint, task-blind.

## Model condition

Same as pilot, fail-closed on drift:

```text
model=gpt-5.6-terra
reasoning_effort=medium
temperature=0.0
max_output_tokens=1024
tools=[]
```

Maintenance and continuation use identical condition.

## Scoring and analysis

- Blinded scoring via `scorer.py` after raw seal (no human adjudication)
- Primary contrast: B5 vs B4 (Fehrest vs maintained wiki) via McNemar exact test on paired (task,repeat) outcomes for eligible tasks only
- Effect size δ=0.15, α=0.05 two-sided, power 0.80 — same as preregistration
- No pooling with pilot data, no rescoring under new rule, no unblinding until scoring seal

## Raw preservation

- `runs/confirmatory-v3/raw/<run_id>.txt` before scoring
- `runs/confirmatory-v3/records.jsonl` (1404 distinct run_ids, resume-safe)
- `runs/confirmatory-v3/execution-order.jsonl` (1152) + `maintenance-order.jsonl` (252)
- Infra threshold 10%, provider identity drift invalidates batch

## Next steps

1. Qualify manifest: `validate_v3.py` PASS, `generate_manifest_v3 --check` PASS, scorer tests PASS, exact-head CI
2. Seal via `docs/canonical/R1_V3_CONFIRMATORY_SEAL_RECORD_*.md` + CURRENT update
3. Execute confirmatory: `python bench/R1/run_confirmatory_v3.py --execute` (requires OPENAI_API_KEY)
4. Raw seal → blinded scoring → score seal → canonical unblinding → terminal R1 verdict

No thesis verdict at this planning stage. This plan is mechanical derivation from pilot, not a result.
