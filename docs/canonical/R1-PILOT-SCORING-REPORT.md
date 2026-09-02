# R1 Variance Pilot — Blinded Scoring Report

```text
PROVENANCE_CLASS=TRANSPLANTED_GOVERNANCE_REPORT
ORIGINAL_SCORE_COMMIT=cef01818bc178366109ef386b40a7c02330015c4
ORIGINAL_SCORE_PARENT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
TRANSPLANT_BRANCH=docs/r1-pilot-scoring-report-ceiling-effect
TRANSPLANT_BASE=a8b57e1293933a5aa134df2ce3bda15310f153c3
TRANSPLANT_DATE=2026-09-02
TRANSPLANT_OPERATOR=founder_authorized_governance_reconciliation
```

This report was originally committed on the historical pre-bootstrap branch
(`origin/historical/r1-v1.1`) as `cef0181`. That branch shares **no common ancestor**
with the live GitHub `origin/main` history. To avoid contaminating the live history,
the report content has been transplanted verbatim onto a fresh branch created from
exact live `origin/main` (`a8b57e1`).

The scientific content below is unchanged from the original commit. References to
`VARIANCE-PILOT.md` and other `bench/R1/` protocol files point to documents on the
historical branch, not to the live GitHub history. See
`docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md` for the full provenance explanation.

**Date:** 2026-09-02T19:25:41Z
**Evidence SHA-256:** d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
**Scoring method:** Deterministic scorer (fehrest-r1 score), arm identity stripped before adjudication

## 1. Per-Arm Primary Score

| Arm | Tasks | Total | OK | Rate |
|-----|-------|-------|-----|------|
| ARM_A | 30 | 120 | 120 | 1.0000 |
| ARM_B | 30 | 120 | 120 | 1.0000 |
| ARM_C | 30 | 120 | 120 | 1.0000 |
| ARM_D | 30 | 120 | 120 | 1.0000 |
| ARM_E | 30 | 120 | 120 | 1.0000 |
| ARM_F | 30 | 120 | 120 | 1.0000 |

## 2. Per-Task Primary Score (first 10)

| Task | Total | OK | Rate |
|------|-------|-----|------|
| S1-A-NEXT | 24 | 24 | 1.0000 |
| S1-B-SUPERSESSION | 24 | 24 | 1.0000 |
| S1-C-CONSTRAINT | 24 | 24 | 1.0000 |
| S1-D-FAILED | 24 | 24 | 1.0000 |
| S1-E-SCOPE | 24 | 24 | 1.0000 |
| S1-F-CONTRADICTION | 24 | 24 | 1.0000 |
| S1-G-HISTORICAL | 24 | 24 | 1.0000 |
| S1-H-IDENTITY | 24 | 24 | 1.0000 |
| S1-I-ABSENT | 24 | 24 | 1.0000 |
| S1-J-FRESH-CONSTRAINT | 24 | 24 | 1.0000 |

## 3. Variance Estimates

**Within-task (run-to-run) variance:** 0.000000 (all arms)
**Between-task variance:** 0.000000 (all arms)

All arms achieved perfect scores on all continuation tasks. This is a **ceiling effect**.

## 4. Discordant Pair Rates

| Pair | Discordant | Total | ψ̂ | Status |
|------|------------|-------|-----|--------|
| ARM_A vs ARM_B | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_A vs ARM_C | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_A vs ARM_D | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_A vs ARM_E | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_A vs ARM_F | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_B vs ARM_C | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_B vs ARM_D | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_B vs ARM_E | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_B vs ARM_F | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_C vs ARM_D | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_C vs ARM_E | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_C vs ARM_F | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_D vs ARM_E | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_D vs ARM_F | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |
| ARM_E vs ARM_F | 0 | 120 | 0.0000 | NO_DETECTABLE_DISCORDANCE |

## 5. Power Analysis

**Parameters:** α=0.05 (z=1.959964), power=0.80 (z=0.841621), δ=0.15

**Result:** NO_DETECTABLE_DISCORDANCE for all arm pairs.

The discordant pair rate ψ̂ = 0.0000 for all comparisons, which is ≤ δ² = 0.0225.
Per VARIANCE-PILOT.md §7: "If ψ̂ ≤ δ² the formula is undefined — that means the arms
almost never disagree, which is itself the answer, and it is reported as
NO_DETECTABLE_DISCORDANCE rather than patched."

## 6. Conclusion

The variance pilot has revealed a **ceiling effect**: all six arms achieved perfect
continuation correctness (120/120) across all 30 tasks. This means:

1. **The benchmark has no discriminating power** at this difficulty level with this model
2. **The confirmatory study is UNDERPOWERED** for the preregistered effect size δ=0.15
3. **No confirmatory N can be computed** because there is no variance to detect

This is a legitimate scientific finding. The pilot has successfully measured the
variance (it is zero), and the mechanical application of the power-analysis rule
correctly identifies that the study cannot be powered for the preregistered effect.

## 7. Recommended Next Steps

Per VARIANCE-PILOT.md §7: "If the formula demands r_conf > 20, the study is declared
UNDERPOWERED_FOR_PREREGISTERED_EFFECT and reported as such."

Options:
1. **Report as UNDERPOWERED** — the tasks may be too easy for this model
2. **Increase task difficulty** — requires a new preregistration (not authorized)
3. **Use a weaker model** — requires a new preregistration (not authorized)
4. **Report the ceiling effect as the finding** — all arms perform equally well

The ceiling effect itself is a finding: at this difficulty level, all context
strategies (including the simplest baseline) perform identically. This suggests
the benchmark needs harder tasks to discriminate between arms.
