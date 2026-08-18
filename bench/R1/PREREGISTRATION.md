# R1 — preregistration v1

```
PREREGISTRATION_VERSION: R1-PREREG-v1
WRITTEN:                 before any confirmatory result exists
MODEL_EXECUTED_AT_TIME_OF_WRITING: NO
CONFIRMATORY_RESULTS_OBSERVED:     NONE
R1_PREREGISTRATION_DIGEST: 2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
```

This document fixes the analysis before the data exists. Everything it decides —
arms, tasks, oracles, scoring, decision rules, exclusions, stopping conditions — is
decided **now**, so that nothing can be adjusted after seeing which way the numbers
fall.

> **A result against the thesis is an acceptable and valuable outcome.** If a
> maintained wiki turns out to be enough, that is the finding, and it is reported as
> the finding. No task will be re-worded, no arm re-weighted, no threshold moved.

---

## 1. Frozen implementation under test

| Field | Value |
|---|---|
| `FEHREST_CANDIDATE_SRC_TREE` | `501004e0be6630eb2d2a90b196012f9cbb596c5a` |
| `FEHREST_CANDIDATE_LOCKFILE` | `1e06c6080bc23760196f61589bbfd5f31c3a3761` |
| Last commit touching `src/` | `5902460` — the formatting closeout |

The candidate is identified by the **git tree hash of `src/`** rather than by a branch
HEAD, because HEAD moves for documentation and benchmark commits that do not change
the implementation. The tree hash changes if and only if the implementation changes.

If a security or correctness fix alters behaviour, that is a **new candidate tree, a
new preregistration version, and a new run.** Formatting-only changes are still
recorded: the formatting commit that produced this tree is `5902460`, and its
semantics-neutrality evidence is in
[verification-r1.md §A1](../../specs/001-headless-rust-fehrest/verification-r1.md).

## 2. The preregistered bundle and its digest

`R1_PREREGISTRATION_DIGEST` is `sha256` over the sorted per-file `sha256` set of:

| File | sha256 |
|---|---|
| `scenarios/S1-beacon.scn` | `7bea239903d56e1b…` |
| `scenarios/S2-marisol.scn` | `2e628f1c22a9feb5…` |
| `scenarios/S3-harbor.scn` | `c91a92a2191a6e75…` |
| `tasks/tasks.json` | `9a30bd04aef96526…` |
| `oracles/oracles.json` | `2628e41930b66af7…` |
| `harness/main.rs` | `642f7fae22b87459…` |
| `PROTOCOL.md` | `f076ff16c074ab87…` |
| `MAINTENANCE.md` | `694fae2c9d6ffa60…` |

```
2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
```

Recompute with:

```bash
for f in bench/R1/scenarios/*.scn bench/R1/tasks/tasks.json bench/R1/oracles/oracles.json bench/R1/harness/main.rs bench/R1/PROTOCOL.md bench/R1/MAINTENANCE.md; do sha256sum "$f"; done | sha256sum
```

**This document is not in its own digest** — it cannot be. It is sealed instead by the
git commit that introduces it, which cannot be altered without rewriting history.

## 3. Corpus and checkpoints

3 scenarios · 28 checkpoints · 36 evidence items · 30 tasks · 30 oracles.

| Scenario | Checkpoints | Days | Task checkpoints |
|---|---|---|---|
| S1 Beacon | t0–t9 | 0–63 | t1, t2, t3, t6, t9 |
| S2 Marisol | t0–t8 | 0–80 | t3, t4, t8 |
| S3 Harbor | t0–t8 | 0–72 | t4, t5, t8 |

**8 of 30 tasks are issued before their scenario ends.** This is fixed now because it
is the property that makes maintenance lag measurable, and because the first draft of
this benchmark lacked it — see [PILOT.md](./PILOT.md) D-2.

## 4. Arms and budget

`B-NULL` (calibration) · `B0` · `B1` · `B3` · `B4` · `B5`. Construction is fixed in
[PROTOCOL.md §4](./PROTOCOL.md); implementation is in the digested `harness/main.rs`.

**Budget: 6,000 bytes, identical for every arm.** No arm receives more room, and no
arm receives a tool another lacks.

## 5. Maintenance

Fixed in [MAINTENANCE.md](./MAINTENANCE.md), which is inside the digest. The binding
commitments: same evidence bundle to every maintainer, nothing from the future,
task-blind, every action counted, and no corrected artefact after a task is scored.

## 6. Primary outcome

`CONTINUATION_CORRECT`, binary per task:

```
CONTINUATION_CORRECT := substantive && require_ok && forbid_ok && abstain_ok
```

Definitions are in [PROTOCOL.md §6](./PROTOCOL.md) and implemented in `score_one`.

**An empty or contract-less response scores 0 on every task type, including
abstention.** Asserted by the instrument pilot across all 30 tasks, with negative
controls.

**Primary comparison: B5 versus B4.** B4 is the strongest baseline and the comparison
that decides the thesis. B0, B1 and B3 are reported but are not the primary contrast.

## 7. Secondary outcomes

`STALE_USE` · `FALSE_ABSTENTION` · `MISSED_ABSTENTION` · `CONFLICT_FLAGGED` ·
`PROVENANCE_GIVEN` · historical-class accuracy · latency · maintenance cost.

Reported separately. **No composite score.** A weighting was not preregistered and one
will not be invented afterwards.

## 8. Decision rule — fixed now

Let **Δ** = paired difference in `CONTINUATION_CORRECT` between B5 and B4.
Let **M** = B5 maintenance cost ÷ B4 maintenance cost, reported on both actions and
output bytes; the *larger* ratio governs.
Let **S** = paired difference in `STALE_USE` (B4 − B5), so positive means B5 is safer.

| Condition | Verdict |
|---|---|
| Δ ≥ +0.15, 95% CI lower bound > 0, and M ≤ 2.0 | `THESIS_SUPPORTED` |
| \|Δ\| < 0.10 with CI containing 0, and M ≤ 0.5 | `THESIS_SUPPORTED_ON_COST` |
| \|Δ\| < 0.10, and S ≥ +0.15 with CI lower bound > 0, and M ≤ 2.0 | `THESIS_SUPPORTED_ON_SAFETY` |
| Δ ≥ +0.15 but M > 2.0 | `THESIS_SUPPORTED_WITH_COST_CAVEAT` — better but expensive, **not** a clean win |
| \|Δ\| < 0.10 and 0.5 < M ≤ 2.0 and S < +0.15 | `THESIS_NOT_SUPPORTED` — **a maintained wiki is enough** |
| Δ ≤ −0.10 | `THESIS_FAIL` |
| anything else | `INCONCLUSIVE` |

A secondary analysis, also fixed now: **continuation correctness as a function of
project age.** If B5's advantage grows with checkpoint index while B4's decays, that
is the longitudinal claim and it is testable by comparing early-checkpoint tasks
(t1–t6) against late-checkpoint tasks (t8–t9). It is reported whichever way it comes
out, and it does **not** override the table above.

## 9. Statistical analysis

- **Test:** McNemar's exact test on paired binary outcomes, B5 versus each baseline.
- **Interval:** 95% CI on the paired difference in proportions.
- **Multiplicity:** four baseline comparisons; Holm correction across them. The
  primary contrast B5–B4 is reported both corrected and uncorrected.
- **Unit of analysis:** one task-run. Repeats of the same task are averaged to a
  per-task rate before pairing, so repeats do not inflate n.
- **No interim analysis. No optional stopping.** The full preregistered N is run, then
  analysed once.

### 9.1 Sample size is deliberately not fixed yet

`CONFIRMATORY_N: NOT_YET_DETERMINED`.

A power analysis needs a variance estimate; a variance estimate needs model execution;
no model has run. Fixing N now would be inventing the number.

The order is fixed and binding: **model execution → observed variance → power analysis
→ confirmatory N.** N will **not** be chosen by searching for the value that makes
Fehrest significant, and the power analysis will be recorded in preregistration v2
alongside the model identity before any confirmatory run begins.

## 10. What v2 must add before confirmatory execution

These cannot be fixed now because the information does not exist on this host:

| Field | Why it is open |
|---|---|
| `MODEL_IDENTITY` | No controlled runner is available. A model cannot be preregistered before it is chosen |
| `TEMPERATURE` / reasoning config | Depends on the model |
| `REPEATS_PER_TASK` | Depends on observed variance |
| `CONFIRMATORY_N` | Depends on the power analysis |
| `RANDOMIZATION_SEED` | Recorded at execution time, in the run manifest |

**v2 is a new version with a new digest**, created before confirmatory execution and
after nothing but pilot data. v1 is retained unchanged.

## 11. Exclusion criteria

Fixed now, and **symmetric across arms in every case**:

1. **Transport failure.** A run that fails to return after two retries is excluded and
   recorded. Its task is excluded **for every arm**, never for one.
2. **Prompt-answerable task.** A task on which `B-NULL` scores above 50% is excluded
   for all arms. B-NULL is scored **first and blind** to the comparison arms, so this
   exclusion cannot be made after seeing who it helps.
3. **Maintenance failure.** Recorded as a cost, not an exclusion. A checkpoint whose
   maintainer failed leaves the artefact unchanged and the arm pays for it.

**No arm-specific exclusion exists and none may be added.** A task is never dropped
because an arm did badly on it.

## 12. Post-result modification policy

Once the first confirmatory result is observed:

- **No treatment-specific code change.** None.
- If an implementation or harness defect is found: mark the affected runs invalid,
  document the defect, repair it, create a new benchmark version, recompute the
  digest, and **rerun every affected arm.**
- **Never selectively rerun only Fehrest.**

V0 disclosed three post-result harness corrections, two of which had favoured Fehrest.
That disclosure is why the pilot for R1 was run before preregistration rather than
after results: the three defects in [PILOT.md](./PILOT.md) were found and fixed with
no result in existence to bias the fixing.

## 13. What a negative result looks like

Stated now so it cannot be reinterpreted later:

- **If B4 matches B5 within 10 points at comparable maintenance cost**, the thesis is
  not supported and the correct conclusion is that a maintained wiki is sufficient and
  Fehrest's additional structure does not earn its complexity.
- **If B5 wins only on `CURRENT_STATE_CONTINUATION`**, the thesis is not supported —
  that is the class a wiki already covers.
- **If B5 wins but costs more than twice B4 to maintain**, that is reported as a
  cost-caveated result, not a win.
- **If B0 — plain files, zero maintenance — is within 10 points of B5**, the entire
  maintained-context premise is in question, and that is reported as the headline.

None of these outcomes will be answered by adding features. `GRAPH=NO` `VECTORS=NO`
`AUTO_MEMORY=NO` `RERANKER=NO` `MCP=NO` `UI=NO`.

**Do not rescue a failed thesis, and do not promote an untested one.**
