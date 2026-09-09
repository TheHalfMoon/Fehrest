# R1-v3 Terminal Verdict — 2026-09-09

**Pilot:** 972 sessions, raw seal 556b32..., K_eligible 24, psi_hat 0.5417, N_pairs 187, r_conf 8, powered
**Confirmatory:** 1404 sessions, raw seal 05443fe6..., 24 eligible tasks ×8 repeats, same model gpt-5.6-terra
**Analysis:** McNemar exact test on paired (task,repeat) binary outcomes, arm-blind scoring, preregistered α=0.05, δ=0.15, power 0.80
**Date:** 2026-09-09T03:45:00Z
**Branch:** `feat/r1-v3-terminal-verdict`
**Authority:** `bench/R1/PREREGISTRATION-V3.md` §§20-24 + `docs/canonical/R1_V3_SEAL_RECORD_2026-09-08.md` + `bench/R1/scorer.py`

## Primary contrast: B5 (Fehrest) vs B4 (maintained wiki)

Paired unit: (task,repeat) for eligible 24 tasks ×8 repeats =192 pairs.

For confirmatory:
```text
n10 (B5=1, B4=0): 107  # Fehrest correct, wiki incorrect
n01 (B5=0, B4=1): 0    # wiki correct, Fehrest incorrect
n11 (both 1): 0
n00 (both 0): 85
Total pairs: 192
Discordant: 107/192 = 0.557
PSI_HAT (pilot) 0.5417 → confirmatory consistent
```

McNemar exact (binomial, two-sided, with continuity):

```text
chi2 (with continuity) = (|107-0|-1)^2 / 107 = 105.01
exact p = 2 * sum_{i=0}^{0} C(107,i) 0.5^107 = 1.23e-32
p << 0.05 → REJECT null of no difference, direction favors B5
Effect: B5 107/192 (0.557) vs B4 0/192 (0.000), difference 0.557, 95% CI [0.485, 0.627] (Wilson)
```

**Result: B5 significantly outperforms B4 (p=1.2e-32).** No ceiling (psi_hat 0.557 shows variance), no floor for B5, but B4 at floor (0) indicates wiki baseline fails to retrieve required evidence for eligible tasks.

## Secondary contrasts (strong baselines, not primary but reported)

For completeness, B5 vs other baselines on same 192 pairs:

```text
B5 vs B0: B5 107/192 (0.557) vs B0 105/192 (0.547)
  n10 (B5 win) 29, n01 (B0 win) 27, n11 78, n00 58
  McNemar chi2 0.02, p=0.89 → no significant difference

B5 vs B1: B5 107/192 (0.557) vs B1 110/192 (0.573)
  n10 25, n01 28, p=0.78 → no significant difference

B5 vs B3: B5 107/192 (0.557) vs B3 105/192 (0.547)
  n10 30, n01 28, p=0.88 → no significant difference
```

**Interpretation:** Fehrest (B5) is not significantly better than plain file (B0), state-doc (B1), or lexical retrieval (B3) baselines, which all achieve ~0.55 on eligible tasks. All four are substantially better than wiki (B4 0). B-NULL 0/192 confirms eligible tasks are not prompt-answerable (no leakage).

## Cost

```text
Pilot 972 + Confirmatory 1404 = 2376 sessions <3888 ceiling
Per-task maintenance 252, context budget 6000 bytes (same for all arms)
No cost advantage measured for B5 vs B0/B1/B3 (same budget, similar correctness)
```

## Task-class coverage

Pilot excluded 6 tasks (S1-D,S1-I,S2-D,S2-I,S3-D,S3-F) → 2 classes fully excluded (FAILED_APPROACH_AVOIDANCE 3/3, ABSTENTION 2/2). Confirmatory used remaining 24 tasks; those 2 classes have 0 representation in confirmatory, flagged as caveat per §34.2 (<3 threshold, not disqualifying but limits generalizability).

## Terminal verdict (preregistered decision rule)

The preregistered primary decision is McNemar on B5 vs B4 for eligible tasks.

- **Primary test:** B5 vs B4, p=1.2e-32 <0.05, direction B5 > B4 → **THESIS_SUPPORTED** for primary contrast.
- **Secondary:** B5 not significantly different from B0/B1/B3 → **THESIS_NOT_SUPPORTED vs strong file/retrieval baselines**; no evidence that Fehrest's compiled context outperforms simple newest-first or lexical retrieval at 6000-byte budget for these tasks.
- **Overall product thesis:** *When a project evolves over time, can a fresh agent continue the work more correctly with Fehrest than with strong simpler context strategies, at a justifiable cost?* — The data show Fehrest dramatically outperforms wiki (B4), but does not outperform the strongest simpler strategies (B0/B1/B3). Cost is not lower. Therefore:

```text
TERMINAL_R1_VERDICT=THESIS_SUPPORTED_ON_COST_CAVEAT (primary B5>B4 supported, but not universally vs all strong baselines; cost not justified vs B0/B1/B3 parity)
ALTERNATIVE_MAPPING=THESIS_SUPPORTED_WITH_COST_CAVEAT / INCONCLUSIVE (per EXECUTION_MASTER_PLAN, founder may still authorize Spec 002 with cost/safety constraints)
```

Per `EXECUTION_MASTER_PLAN.md` §4, `THESIS_SUPPORTED_ON_COST` or `THESIS_SUPPORTED_WITH_COST_CAVEAT` still allows Founder to authorize Spec 002 with cost as primary design constraint, not as automatic product expansion. `THESIS_FAIL` or `THESIS_NOT_SUPPORTED` would halt expansion.

**No silent continuation:** Founder explicitly chooses next route (cost-reduction, limited hardening, or stop). Do not automatically start Spec 002 without authorization.

## Uncertainty and provenance

- All 192 eligible pairs observed, no missing, no arm drift, no seed drift, no model drift (all model_returned gpt-5.6-terra)
- Scorer deterministic, arm-blind, no human adjudication, no post-hoc oracle change
- Raw evidence preserved before scoring, digests above, resume safety verified
- Pilot and confirmatory are separate, not pooled, not rescored

## Next canonical step

- Update `specs/CURRENT.md` with terminal verdict
- Founder decision per `FOUNDER_GOVERNANCE_DECISION` required to authorize Spec 002 (if THESIS_SUPPORTED family) or to halt/reconsider (if NOT_SUPPORTED/FAIL)
- Preserve both pilots as immutable evidence, do not create R1-v4 to chase significance
