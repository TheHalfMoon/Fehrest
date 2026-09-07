# R1-v2 Independent Scientific Review Packet

**Status:** `PENDING_INDEPENDENT_REVIEW`

**Created:** 2026-09-04
**Revised:** 2026-09-07 — convergence repair (branch `review/r1-v2-independent-review-convergence`)

**Candidate binding (WORKING_CANDIDATE at this revision):**
```text
WORKING_CANDIDATE_COMMIT=0d206cac9a6e5ebfe3d47401aa1f081a587af60f
WORKING_CANDIDATE_TREE=6943decf800574906b76b0abd7dc5a3460cef072
REVIEW_CANDIDATE=NOT_YET_FROZEN — packet is WORKING_CANDIDATE for internal qualification only
SEALED_CANDIDATE=NONE
EXECUTION_CANDIDATE=NONE
```
Review must bind to an exact immutable `REVIEW_CANDIDATE` commit/tree + artifact manifest SHA-256. If any load-bearing artifact changes after review, `AFFECTED_REVIEW=STALE` and `RE_REVIEW_REQUIRED=YES`.

**Prerequisites (machine validation, all satisfied):**
- R1_V2_MACHINE_VALIDATION=PASS
- R1_V2_VALIDATION_CONVERGENCE=COMPLETE
- R1_V2_MUTATION_TESTING=PASS
- R1_V2_EXACT_HEAD_CI=PASS
- `python bench/R1/validate.py`, `test_validate.py`, `test_scorer.py` all PASS on `0d206ca`
- PR #34 merged (`f8a0dd5` = merge, `ec7a1ea` = head) — see sealing procedure for identities

**Hard boundaries (must not be violated):**
- R1_V2_MODEL_EXECUTION=PROHIBITED
- R1_V2_VARIANCE_PILOT_EXECUTION=PROHIBITED
- R1_V2_CONFIRMATORY_EXECUTION=PROHIBITED
- R1_V2_UNBLINDING=PROHIBITED
- SPEC_002_ACTIVATION=PROHIBITED
- PRODUCT_IMPLEMENTATION=PROHIBITED
- R1_V2_SCIENTIFIC_REVIEW=PENDING
- R1_V2_STATISTICAL_REVIEW=PENDING

**Evidence stratification — this packet enforces it:**

| Label | Meaning | R1-v2 value at this revision |
|---|---|---|
| `R1_V1_HISTORICAL_EVIDENCE` | Ceiling-effect finding from the previous R1-v1 / replacement study that motivated R1-v2 | `NO_DETECTABLE_DISCORDANCE` + `CEILING_EFFECT=YES` at 120/120 perfect rates, evidence `SHA256:d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b` — preserved, not overwritten |
| `R1_V2_DESIGN_MOTIVATION` | Harder tasks, structural complexity, epoch handling designed *before* any R1-v2 data to avoid repeating that ceiling | Documented in `PREREGISTRATION-V2.md` §§3–5, §15; `VARIANCE-PILOT-V2.md` §1; `MAINTENANCE-V2.md` §5 |
| `R1_V2_EMPIRICAL_DATA` | Model runs observed under R1-v2 protocol | **`NONE`** — `MODEL_RUNS_OBSERVED_AT_AMENDMENT=0`, `SCORING_STATUS=NOT_STARTED` (PREREG header). No model call has executed under R1-v2. |
| `R1_V2_VARIANCE_PILOT` | Stage-1 execution of 972 sessions to estimate `ψ̂` | **`NOT_EXECUTED`** — protocol sealed, runner not yet qualified, raw evidence does not exist |
| `R1_V2_CONFIRMATORY` | Stage-2 execution at `r_conf` | `NOT_STARTED` — manifest not sealed |

Prior packet phrasing that implied `R1_V2_EMPIRICAL_DATA` already existed is corrected. The only `NO_DETECTABLE_DISCORDANCE` / `CEILING_EFFECT` that exists as data is `R1_V1_HISTORICAL_EVIDENCE`. Do not describe it in a way that implies R1-v2 already produced data.

---

## 1. CONSTRUCT_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Tasks measure **continuation correctness**, not trivia retrieval. Each of the 30 tasks is a `what should the maintainer do next?` prompt requiring project continuation under evolving state, not fact lookup. 12 task classes (NEXT_ACTION, SUPERSESSION_AVOIDANCE, CONSTRAINT_RETENTION, FAILED_APPROACH_AVOIDANCE, SCOPE_RESOLUTION, CONTRADICTION_HANDLING, HISTORICAL_REASONING, IDENTITY_CONTINUITY, ABSTENTION, PROVENANCE, CROSS_FILE_SYNTHESIS, EPOCH_BOUNDARY) are derived from structural definitions in `PREREGISTRATION-V2.md` §5.1 and frozen task identities §5.3. Prompt design tests diagnostic reasoning (temporal chaining, supersession, constraint retention, cross-file synthesis, epoch-boundary validity) — see `benchmark-spec-v2.json: tasks[].task_class` and `corpus-manifest-v2.json: evidence.available_from` lineage.

Validator `test_validate.py: TestCanonicalValidation.test_task_classes` verifies 12 distinct classes; `validate.py:_validate_task_class_counts` enforces it.

## 2. DIFFICULTY_WITHOUT_ARTIFICIALITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Complexity is **structural, not linguistic-obscurity** (PREREG §3, §3.1). Mechanisms are legitimate project phenomena:

| Failure mode claimed | How R1-v2 legitimately targets it (without model weakening) |
|---|---|
| Stale-use | Multi-layer supersession chains A→B→C→D where the newest document does not contain the answer |
| Missed constraints | Constraints introduced early (t0–t3), tested late (>8 checkpoints later) with intervening distractors |
| Scope creep | Cross-scenario precedent traps where one project's exception looks like a general rule |
| Failed-approach repetition | Failed approaches revisited with new context that makes them plausible again |
| Identity discontinuity | Objects renamed/moved multiple times across non-contiguous checkpoints |
| Contradiction blindness | Unresolved conflicts that must be flagged, not silently resolved |
| Abstention failure | Genuinely absent information masked by plausible distractors |
| Provenance loss | Tasks requiring specific `evidence_id` naming, with look-alike documents as traps |
| Maintenance drift | State changes across 3 epochs where old rules no longer apply |
| Context overflow | Dense distractor sets (3–5 per relevant doc) that crowd relevant facts under 6000-byte budget |

**Preregistered commitment:** Strong simple baselines B0/B4 are **not weakened** to create separation (PREREG §6.1; VARIANCE-PILOT §1). If difficulty were artificial (adversarial phrasing, hidden instructions), reviewer must REJECT.

See also §7 BASELINE_FAIRNESS and §10 CEILING_RISK for how difficulty is falsifiable without weakening baselines.

## 3. TASK_TIMELINE_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

| Quantity | Value | Source / verification |
|---|---|---|
| `TOTAL_TASKS` | `30` | `benchmark-spec-v2.json: tasks.length`, `session_arithmetic.total_tasks`, PREREG §5.3 frozen |
| `DISTINCT_CHECKPOINTS` | `12` | `t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t12,t14` (t11 absent by design) — validator `len({t.checkpoint})==12` |
| `TASKS_BEFORE_T14` | `27` | `sum(t.checkpoint<14)==27` — PREREG §5.2, validator `_validate_protocol_documents` asserts the prose count matches machine count |
| `CHECKPOINT_SET` | `t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t12,t14` | PREREG §5.2 table |
| `ORACLES` | `30` | 1:1 task mapping via `oracle.task_id` ↔ `task.oracle_id` |
| `CORPUS_EVIDENCE` | `96` | `corpus-manifest-v2.json: evidence.length` |
| `NUM_CLASSES` | `12` | `task_classes` keys; `test_validate` confirms |

Timeline verified against `benchmark-spec-v2.json`, `tasks-v2.json`, `oracles-v2.json`, `corpus-manifest-v2.json` via field-level canonical-derived equality (`validate.py:_validate_canonical_derived_equality`, `test_validate.py: TestCanonicalDerivedEquality`). `PREREGISTRATION-V2.md` §5.2 states "27 of the 30 tasks are issued before t14" — validator proves that number equals actual count (prevents documentation drift).

## 4. TEMPORAL_LEAKAGE

**Status:** `PENDING_INDEPENDENT_REVIEW`

Corpus manifest encodes `available_from` (= checkpoint) and `available_until` per evidence item. A task at checkpoint `t` may only depend on evidence with `available_from ≤ t`. Validator `_validate_no_future_leakage` rejects any `task.depends_on_evidence` that references future evidence. Mutation test 6 in `validate.py:_validate_mutations` (and `test_validate.py:test_future_evidence_mutation_detected`) corrupts `available_from` to 999 and verifies detection. Structural temporal subtraction is also enforced: `VARIANCE-PILOT-V2.md` §4 maintainer sees nothing from `Tj > i`.

No R1-v2 empirical leakage claim — this is a static design obligation.

## 5. NO_INFORMATION_LEAKAGE

**Status:** `PENDING_INDEPENDENT_REVIEW`

Beyond temporal leakage, **future-evidence vocabulary subtraction** is enforced: distractor/trap documents share keywords and naming conventions but contain no privileged future facts that would shortcut the task. Validator `_validate_evidence_dependencies` + `_validate_corpus` verifies every `depends_on_evidence` / `trap_evidence` / `distractor_evidence` exists in the corpus, and `test_validate.py:test_no_future_leakage` proves no forward reference. Maintainer sessions are task-blind (`MAINTENANCE-V2.md` §3): the maintainer never sees tasks, oracles, or scoring rules and is never told that anything will matter later — so even if a distractor were informative, the maintainer cannot exploit task knowledge.

## 6. NO_ARM_FAVORING

**Status:** `PENDING_INDEPENDENT_REVIEW`

Neutral arm identifiers `B-NULL, B0, B1, B3, B4, B5` contain no evaluative language like "Fehrest" or "baseline" in model-visible prompts. Arm identity is stripped before scorer adjudication (PREREG §14). Same model condition for all arms (`PREREG §11`: `gpt-5.6-terra`, `medium`, `0.0`, `1024`, `[]`). Construction documented in `PREREGISTRATION-V2.md` §6 / `benchmark-spec-v2.json: arms`.

This does **not** mean mechanisms are identical — see §7 for intentionally different maintenance policies. Fairness is *preregistered comparison*, not identical implementation.

## 7. BASELINE_FAIRNESS

**Status:** `PENDING_INDEPENDENT_REVIEW`

Strong simple baselines are **preserved, not weakened** (PREREG §6.1: "B0, B1, B3, B4 are not weakened because they performed well in R1-v1"). The scientific requirement is a *fair preregistered comparison*, not identical mechanism.

Per-arm exact semantics (each row is intentionally different — do not claim equality when policy is deliberately distinct):

| Arm | Information access | Update / maintenance policy | Maintenance cost | Context budget | Model condition | Task access | Oracle access |
|---|---|---|---|---|---|---|---|
| **B-NULL** | **Task prompt only, no project context** — 0 evidence bytes | **Not maintained** — no sessions, no state artefact | `0` | none (prompt-only) | `gpt-5.6-terra` / medium / 0.0 / 1024 / [] (same) — retrieved per run | Task prompt only | none (exclusion signal only: `B_NULL_prompt_answerable` tasks are `>0` ⇒ excluded per §19.1) |
| **B0** | **Plain project files, newest checkpoint first, cut at budget** — raw file text only, no Fehrest structure | **Not maintained** — snapshot retrieval only, no cross-checkpoint state | `0` beyond ordinary project work | `6000` bytes, single tier | Same as B5 | Only at continuation time, neutral ID | none (scored blind) |
| **B1** | **Repository-native state documents + project files underneath** — `CURRENT_STATE.md`/`AGENTS.md`-style docs, then files | **Maintained** — 3 scenarios ×14×2 =84 sessions for B1 alone; task-blind, same evidence bundle as other maintained arms, same time | Counted per MAINTENANCE-V2.md §7 (`MAINTENANCE_ACTIONS`, `INPUT_BYTES`, `OUTPUT_BYTES`, `MODEL_TOKENS`, etc.) | `6000` bytes, single tier | Same as B5, same maintainer condition | Task-blind during maintenance; tasks only at continuation | none |
| **B3** | **Lexical retrieval through real FTS index** — ranked by distinct term hits, recency-tiebroken, raw document text only | **Not maintained** — stateless retrieval per task; no maintained artefact (index is derived, disposable) | `0` beyond index build (derived) | `6000` bytes, single tier | Same as B5 | Query = task prompt; retrieval only | none |
| **B4** | **Maintained wiki page, and nothing else** — single page replaced wholesale per checkpoint | **Maintained** — 84 sessions (same schedule as B1/B5); task-blind; same evidence/time; cost is `edit a paragraph` | Counted (see above); typically lower per-session complexity than B5's structured ops | `6000` bytes, single tier | Same as B5 | Task-blind during maintenance; tasks only at continuation | none |
| **B5** | **Fehrest compiled context package at checkpoint's valid time** — memory-typed items (`Fact/Decision/Constraint/Gotcha/State`) with `valid_from/valid_until/supersedes` | **Maintained** — 84 sessions; structured memory ops (`add/supersede/conflict/retract`) with explicit `mtype/project/valid_from/supersedes`; task-blind; same evidence/time; envelope overhead consumes budget | Counted; higher per-session structure cost; measured `MAINTENANCE_ACTIONS` includes each memory op (see MAINTENANCE-V2.md §6); **lower-bound cost** because real B5 would pay for the eventual agent-facing write surface that the benchmark adapter replaces | `6000` bytes, single tier | Same as all other arms — any divergence invalidates batch | Task-blind during maintenance | none |

Key fairness notes:
- B0/B3 unmaintained `cost=0` is a **real advantage** the benchmark is built to let win (MAINTENANCE-V2.md §1).
- B1/B4/B5 share `MAINTENANCE_PROTOCOL §1`: same evidence, same time, task-blind, counted. Selective diligence (updating B5 carefully, B4 carelessly) is prohibited and would be detected via `STALE_STATE_LEFT_BEHIND` / `EPOCH_TRANSITIONS_MISSED` outcomes.
- Do not weaken B0/B4's construction to manufacture separation — if B4 gives essentially the same continuation quality at lower complexity and reasonable maintenance cost, that is **evidence against** the Fehrest thesis (PREREG §6.1, §30, MAINTENANCE-V2.md §10).

## 8. SCORER_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Deterministic scorer `fehrest-r1 score` ("scorer.py"), arm identity stripped before adjudication. No human adjudication in the pilot (PREREG §14; VARIANCE-PILOT §5). Rules (PREREG §8):

```text
substantive := any response field has non-whitespace content >= min_action_chars
require_ok  := every require_all entry matches its named output field
forbid_ok   := no forbid entry matches its named output field
abstain_ok  := ABSTAIN == YES  if task is abstention task
               ABSTAIN != YES  otherwise
CONTINUATION_CORRECT := substantive && require_ok && forbid_ok && abstain_ok
```

Additions in v2 (`require_synthesis`, `require_epoch`) are **not substring-only checks** — scorer verifies corpus-backed checkpoint references and epoch-boundary markers (`PREREG §14.1`, `scorer.py: check_require_synthesis / check_require_epoch`, validator `_validate_scorer_support` + `_validate_scorer_support_strict`). Tests: `test_scorer.py` 20/20 (including 4 adversarial tests), `test_validate.py` corpus-digest and scorer-type checks.

## 9. ORACLE_VALIDITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

30 oracles, each mapping to exactly one task (`oracle.task_id` ↔ `task.oracle_id`, 1:1). Fields `require_all`, `forbid`, `trap_present`, `stale_facts`, `correct_facts`, `require_synthesis`, `require_epoch`, `provenance_required` are frozen in `oracles-v2.json` and derived from `benchmark-spec-v2.json: oracles`. Every `derivation_evidence` entry exists in `corpus-manifest-v2.json` (validator `_validate_evidence_dependencies`). `require_all`/`forbid` are field-scoped; `stale_facts`/`correct_facts` distinguish trap vs current. Field-level canonical equality between `benchmark-spec-v2.json: oracles` and `oracles-v2.json` confirmed (`validate.py:_validate_canonical_derived_equality`, `test_validate.py: TestCanonicalDerivedEquality`).

## 10. CEILING_RISK

**Status:** `PENDING_INDEPENDENT_REVIEW`

**Stratification enforced (corrects prior conflation):**

- `R1_V1_HISTORICAL_EVIDENCE`: The **previous R1-v1 / replacement study** (valid replacement execution on 2026-09-02, 1036 records) revealed a **ceiling effect — all arms perfect at 1.000**, `CEILING_EFFECT=YES` (`pilot result = NO_DETECTABLE_DISCORDANCE`, 120/120 across 30 tasks in the legacy pilot). This is immutable prior evidence (`d99c217…`, `specs/CURRENT.md: R1_REPLACEMENT_SCORING_RESULT=CEILING_EFFECT_NO_DETECTABLE_DISCORDANCE`).
- `R1_V2_DESIGN_MOTIVATION`: **Because** of that ceiling, R1-v2 was preregistered to increase discriminating difficulty via structural complexity (PREREG §§3–5; 12 epochs, 8 cross-file synthesis tasks, supersession chains, etc.). No task corpus change is permitted after data is observed.
- `R1_V2_EMPIRICAL_DATA`: **`NONE`**. Variance pilot `NOT_EXECUTED`. No R1-v2 model score exists; therefore no R1-v2 `NO_DETECTABLE_DISCORDANCE` can be claimed yet. The phrase "variance pilot data shows `NO_DETECTABLE_DISCORDANCE`" in the prior packet version **referred to R1-v1**, not R1-v2 — this revision makes that explicit.
- `R1_V2_CEILING_RISK`: The risk that R1-v2 *will also* ceiling is real and acknowledged as a **falsifiable** outcome (see §16). It is **not** preregistered as thesis support or falsification (canonical routing — see §16).

Reviewer instruction: evaluate ceiling risk as *design adequacy*: do the 30 harder tasks, 12 checkpoints, 27-before-t14 maintenance-lag distribution, 3–5 distractors per relevant doc, and 96 evidence items plausibly discriminate context strategies for `gpt-5.6-terra` without being adversarial? That judgment is scientific, not a claim that R1-v2 already ceiled.

## 11. FLOOR_RISK

**Status:** `PENDING_INDEPENDENT_REVIEW`

Floor risk exists if tasks are **too difficult** for any arm (including B5) to answer correctly, yielding near-zero pass rates and `ψ̂ ≈ 0` for a different reason. Like ceiling, floor is `R1_V2_EMPIRICAL` outcome `NOT_YET_OBSERVED` and must not be conflated with thesis falsification.

- Monitor per-arm and per-task pass rates; `R1_V2_EMPIRICAL_DATA=NONE` at this gate.
- `B_NULL_exclusion` must be applied **before** `r_conf` to avoid floor contamination (a task that is both prompt-answerable and floor-hard would otherwise distort `ψ̂` — see statistical packet §2).
- Design mitigation (without weakening baselines): 3+ tasks where B0/B4 can genuinely win (PREREG §3 table, §29 `FLOOR_RISK` checklist). If floor is observed empirically, the benchmark provides no signal for the preregistered `δ` and is reported as `UNDERPOWERED_FOR_DIFFICULTY`; a new preregistration would be required, not a silent difficulty tweak.

## 12. MAINTENANCE_FAIRNESS

**Status:** `PENDING_INDEPENDENT_REVIEW`

Protocol: `MAINTENANCE-V2.md` (R1-V2). Summary per `benchmark-spec-v2.json: maintenance_protocol` and session arithmetic:

- **Same evidence, same time.** At each checkpoint `Ti` (t1–t14), every maintained arm's maintainer receives the identical new-evidence bundle and nothing from `Tj > i`.
- **Task-blind.** The maintainer never sees a task, never learns which facts will be scored, and is never told that anything will matter later (§3).
- **Counted.** `MAINTENANCE_ACTIONS`, `MAINTENANCE_INPUT_BYTES`, `MAINTENANCE_OUTPUT_BYTES`, `FILES_OR_OBJECTS_TOUCHED`, `MAINTENANCE_MODEL_TOKENS`, `MAINTENANCE_WALL_TIME`, `MANUAL_DECISIONS_REQUIRED`, `ERRORS_INTRODUCED`, `STALE_STATE_LEFT_BEHIND`, `EPOCH_TRANSITIONS_MISSED` recorded per checkpoint per arm (§7).
- **No omniscient free update.** No maintained arm receives a hand-authored perfectly-current artefact (§1). Drift is a **result, not a bug** (§8).
- **T0 initialization rule.** `t0` is given state; maintenance begins at `t1` (14 transitions per scenario → `3×14×3×2=252` sessions). Harness folds `t0..ti` to arm state at `Ti` (§2, §4).
- **Epoch transitions** (Foundation→Growth at t5, Growth→Maturity at t10) carry explicit `valid_decisions`/`deprecated_decisions`/`new_rules` bundles; the maintainer must actively remove deprecated decisions (§5). Deprecated-but-findable facts are traps; `EPOCH_TRANSITIONS_MISSED` is reported alongside accuracy.
- **B0/B3 unmaintained, cost=0** beyond ordinary project work — a real advantage the benchmark is built to let win (§1, §10).
- **B1/B4/B5 per-arm differences are load-bearing and documented in §7** — do not claim "equal mechanisms" when maintenance complexity is intentionally different (structured memory ops vs wiki paragraph). Fairness is preregistered *comparison under equal evidence/time/task-blindness*, not identical implementation.

Validator `_validate_maintenance_arithmetic` and `_validate_session_arithmetic` prove `252 + 600 + 120 = 972` total variance-pilot sessions.

## 13. MODEL_IDENTITY_ADMISSIBILITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Fail-closed policy enforced via `model_identity_admissibility` (`benchmark-spec-v2.json: model_identity_admissibility`). Conditions and handling (PREREG §11–12, VARIANCE-PILOT §4.1):

| Condition | Handling |
|---|---|
| `returned_identity_missing` | `INVALIDATE_BATCH` |
| `identity_changes_within_batch` | `INVALIDATE_BATCH` |
| `maintenance_identity_not_equal_continuation_identity` | `INVALIDATE_BATCH` |
| `different_identities_across_arms` | `INVALIDATE_BATCH` |
| `provider_alias_drift` | `INVALIDATE_BATCH` |
| `identity_metadata_malformed` | `INVALIDATE_BATCH` |

`MODEL_CONDITION` is frozen (`gpt-5.6-terra`, `medium`, `0.0`, `1024`, `[]`). A stronger or weaker model for any arm invalidates the batch. If the provider exposes only a floating alias, `MODEL_VERSION_PIN_STATUS=UNAVAILABLE_FLOATING_ALIAS` and per-run reported identity is recorded — but still `INVALIDATE_BATCH` on drift (validator `_validate_model_identity_policy` and `_validate_model_condition`).

## 14. COST_BOUND

**Status:** `PENDING_INDEPENDENT_REVIEW`

Context budget: `6000` bytes primary tier, `secondary_tier_bytes=null` (single tier — `benchmark-spec-v2.json: context_budget`, validator `_validate_context_budget`). Statistical power prior: `target_power=0.80`, `minimum_meaningful_effect_delta=0.15`, `alpha=0.05`. Session costs: `maintenance_sessions=252`, `comparison_continuation_sessions=600`, `calibration_sessions=120`, `total_variance_pilot_sessions=972` (proved arithmetic). `r_conf` ceiling `20` and `total 3888` max (PREREG §21) bound confirmatory cost. **No B5 accuracy claim without its cost** (PREREG §10).

## 15. REPRODUCIBILITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

All artifacts deterministic. Single source of truth `benchmark-spec-v2.json`; derived `tasks-v2.json`, `oracles-v2.json`, `corpus-manifest-v2.json` field-level equality verified (validator `_validate_canonical_derived_equality`, `test_validate.py: TestCanonicalDerivedEquality`). Randomized order is seeded and interleaved, realized order written to `runs/execution-order.jsonl`; randomization spec in `benchmark-spec-v2.json: randomization`. Validator script `bench/R1/validate.py`, tests `bench/R1/test_validate.py` (41 tests, 6 classes) and `bench/R1/test_scorer.py` (20 tests) are self-contained and included in exact-head CI `.github/workflows/bench-r1-validation.yml` (5 jobs: `test-scorer`, `test-validator`, `validate`, `canonical-equality`, plus `verify-artifacts`). Current head `0d206ca` CI verified `PASS` for `verify-artifacts` and Bench R1 Validation.

## 16. FEHREST_FALSIFIABILITY

**Status:** `PENDING_INDEPENDENT_REVIEW`

Fehrest's thesis is **explicitly falsifiable** (PREREG §§23–24, §30; VARIANCE-PILOT §11; `F-1` in `docs/17-FAILURE-CONDITIONS.md`):

- A ceiling effect (no detectable discordance) is **not thesis support** and **not thesis falsification** — it is `NO_DETECTABLE_DISCORDANCE` / `CEILING_EFFECT` / `UNDERPOWERED_FOR_PREREGISTERED_EFFECT` reported as the finding. `NO_SILENT_CONTINUATION` — founder explicitly chooses extension, limited hardening, or stop.
- A second ceiling in R1-v2 is **not silently re-routed** as `THESIS_NOT_SUPPORTED`. Canonical governance (`PREREG §24`, `VARIANCE-PILOT §11`, `specs/CURRENT.md: R1 outcome routing`) distinguishes:
  ```text
  CEILING_EFFECT       → report as finding; design harder benchmark; new preregistration required; NOT thesis support/falsification
  THESIS_NOT_SUPPORTED → trigger F-1 review; do not begin Spec 002 by default
  THESIS_FAIL          → halt product expansion
  ```
  `SECOND_CEILING = THESIS_NOT_SUPPORTED` is **not preregistered** (`SECOND_CEILING = THESIS_NOT_SUPPORTED` is `NOT_PREREGISTERED`) and must not be invented. If a different interpretation were desired for R1-v2, it would require an explicitly preregistered and independently reviewed amendment **before** execution (statistical packet §17).
- If **B4 gives essentially the same continuation quality at lower complexity and reasonable maintenance cost**, that is **evidence against** the Fehrest thesis and is reported as such (PREREG §§6.1, 30; MAINTENANCE-V2.md §10 "Why B5 could lose this"). `THESIS_NOT_SUPPORTED` and `THESIS_FAIL` remain distinct terminal verdicts under PREREG §24.
- No composite score is computed; weighting was not preregistered (PREREG §9). Effect estimates are reported as power-analysis inputs with uncertainty, not as product claims.
- No feature will be added in response to any R1-v2 result (`GRAPH=NO`, `VECTORS=NO`, `AUTO_MEMORY=NO`, etc. — PREREG §30).
- `R1_V1_HISTORICAL_EVIDENCE` (`NO_DETECTABLE_DISCORDANCE` at 1.000) belongs to the previous study and is preserved as the motivation for R1-v2's harder corpus, not as evidence that R1-v2 already failed. `R1_V2_EMPIRICAL_DATA=NONE` must be preserved in any falsifiability discussion.

---

## Per-arm baseline fairness summary (normative)

See §7 table. In addition, explicitly:

- **No arm is intentionally weakened** to create separation (PREREG §6.1). B0 (newest-file-first cut) and B4 (maintained wiki) remain the same strong constructions that performed well in R1-v1. If they tie or beat B5, that is the thesis failing on its merits.
- **Information access, maintenance cost, and context budget are captured per §7** and are not interchangeable. Equality is required for: `model_condition`, `reasoning_effort`, `temperature`, `max_output`, `tool_set`, `context_bytes budget (6000)`, `evidence bundle per checkpoint`, `task-blindness`, and counting. Inequality is intentional for: `artefact format`, `retrieval mechanism`, `maintenance operation complexity`, and `derived-index vs memory structure`.
- `VARIANCE-PILOT-V2.md` §1 and `MAINTENANCE-V2.md` §10 record why B5 could lose despite structural sophistication — that loss must be legible as a prediction met.

---

## Evidence identities (mechanically generated — do not hand-edit)

```text
CANDIDATE_COMMIT=0d206cac9a6e5ebfe3d47401aa1f081a587af60f  # WORKING — will be pinned to REVIEW_CANDIDATE at freeze
CANDIDATE_TREE=6943decf800574906b76b0abd7dc5a3460cef072   # WORKING — will be pinned to REVIEW_CANDIDATE_TREE at freeze
REVIEW_PACKET_COMMIT=ae155e5804922b41926163beacaf03b34f09b6cf  # prior packet-only commit — NOT PR #34 merge
PR_34_HEAD=ec7a1eac5d6c45a8d4795b99bd1b41351dd72eef
PR_34_MERGE=f8a0dd5e9b06e137a53157e99732d71d635f9a0f
CURRENT_MAIN=0d206cac9a6e5ebfe3d47401aa1f081a587af60f
PRE_BOOTSTRAP_SEALED_R1_V1_1=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
PRE_BOOTSTRAP_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
PREREGISTRATION_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
ISSUE_8_STATUS=CLOSED
ISSUE_11_STATUS=CLOSED
R1_V1_CEILING_EVIDENCE_SHA256=d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
```
When `REVIEW_CANDIDATE` is frozen, `CANDIDATE_COMMIT`/`CANDIDATE_TREE` will be updated to the exact immutable candidate and `bench/R1/artifact-manifest-v2.json` will carry `MANIFEST_SHA256` and per-file `ARTIFACT_SHA256S`.

---

## References

- `bench/R1/benchmark-spec-v2.json` — arms, context_budget, model_identity_admissibility, task/oracle definitions
- `bench/R1/PREREGISTRATION-V2.md` — §§3–6, 8, 11–15, 19–20, 24, 28–30
- `bench/R1/VARIANCE-PILOT-V2.md` — §§1–10
- `bench/R1/MAINTENANCE-V2.md` — §§1–10
- `bench/R1/scorer.py` / `bench/R1/test_scorer.py`
- `bench/R1/validate.py` / `bench/R1/test_validate.py` (41 tests)
- `bench/R1/test_r1v2_statistical_design.py` — static statistical edge cases (paired with statistical packet)
- `bench/R1/test_review_binding.py` — review-binding invariants
- `specs/CURRENT.md` — `ACTIVE_R1_SUBGATE`, `R1 outcome routing`, `CEILING_EFFECT` definition
