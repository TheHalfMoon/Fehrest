# R1-v3 Sealing Procedure

**Status:** `SEALING_PREPARATION_PENDING` — internal-qualification gate (human independent review superseded 2026-09-08)

> `SEALING_PREPARATION_PENDING` means repository-local qualification may be complete while sealing authority is still blocked by internal qualification. The exact immutable `REVIEW_CANDIDATE` is bound outside this self-referential file by `specs/CURRENT.md` and the deterministic artifact manifest after exact-head qualification. This procedure intentionally does not hard-code its own containing commit as "latest main" or as a frozen candidate.
>
> **Founder governance amendment 2026-09-08:** `FOUNDER_DECISION=REMOVE_MANDATORY_HUMAN_INDEPENDENT_REVIEW_GATE` — see `docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md`. `HUMAN_INDEPENDENT_REVIEW=OPTIONAL`, `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`. Issues #43/#44 are `SUPERSEDED_BY_CANONICAL_GOVERNANCE_CHANGE` and are not authority for sealing. Sealing now gates on deterministic internal qualification, not on external human PASS.

**Prerequisites (current truth under amended governance):**
- R1_V3_MACHINE_VALIDATION=PASS
- R1_V3_VALIDATION_CONVERGENCE=COMPLETE
- R1_V3_MUTATION_TESTING=PASS
- R1_V3_EXACT_HEAD_CI=REQUIRED_ON_BOUND_REVIEW_CANDIDATE
- R1_V3_SCIENTIFIC_DESIGN_SELF_AUDIT=REQUIRED (16-section internal qualification via packet + adversarial tests)
- R1_V3_STATISTICAL_DESIGN_SELF_AUDIT=REQUIRED (18-section internal qualification via packet + statistical proofs)
- R1_V3_ADVERSARIAL_VALIDATION=REQUIRED
- REVIEW_CANDIDATE_BINDING_SOURCE=`specs/CURRENT.md` + `bench/R1/artifact-manifest-v3.json` (deterministic manifest, not mandatory issue #43/#44 binding)
- INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
- SEALED_CANDIDATE=NONE
- EXECUTION_CANDIDATE=NONE

---

## 1. Sealing prerequisites (all must be satisfied — fail closed)

```text
R1_V3_MACHINE_VALIDATION=PASS
R1_V3_VALIDATION_CONVERGENCE=COMPLETE
R1_V3_MUTATION_TESTING=PASS
R1_V3_EXACT_HEAD_CI=PASS
R1_V3_SCIENTIFIC_DESIGN_SELF_AUDIT=PASS   (internal: 16-section scientific packet + adversarial validation)
R1_V3_STATISTICAL_DESIGN_SELF_AUDIT=PASS  (internal: 18-section statistical packet + statistical proofs)
R1_V3_ADVERSARIAL_VALIDATION=PASS
REVIEW_CANDIDATE=FROZEN_AT_IMMUTABLE_COMMIT_AND_TREE
ARTIFACT_MANIFEST_SHA256=BOUND_TO_REVIEW_CANDIDATE
R1_V3_CONFIRMATORY_EXECUTION=PROHIBITED   # corrected name — prior draft had R1_V3_V2_CONFIRMATORY_EXECUTION
R1_V3_VARIANCE_PILOT_EXECUTION=PROHIBITED
R1_V3_MODEL_EXECUTION=PROHIBITED_UNTIL_SEALED
R1_V3_UNBLINDING=PROHIBITED
SPEC_002_ACTIVATION=PROHIBITED
PRODUCT_IMPLEMENTATION=PROHIBITED

INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
HUMAN_INDEPENDENT_REVIEW=OPTIONAL
HUMAN_REVIEW_BLOCKING_AUTHORITY=NO
QUALIFIED_HUMAN_REVIEW_EVIDENCE=NONE (no fake PASS)
```

**Sealing CANNOT proceed while any deterministic internal gate is not PASS.** Hermes may `prepare / audit / red-team / test / request / collect / reconcile findings` and now also `self-audit scientific/statistical design via deterministic tests` — internal PASS is recorded via validation suite, not via external human identity. An unavailable external human reviewer is **not** a blocker (per founder decision).

If internal qualification fails, finish every repository-local repair first and record the exact blocker as `CURRENT_AUTHORIZED_LOCAL_WORK=PENDING_REPAIR, BLOCKER=<exact deterministic gate>`.

Human reviewers may still review voluntarily; such review is `OPTIONAL` and `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`. Voluntary review never creates `R1_V3_SCIENTIFIC_REVIEW=PASS` or `R1_V3_STATISTICAL_REVIEW=PASS` by itself unless the founder later reinstates mandatory review.

## 2. Candidate states — precise definitions

| State | Meaning | Binding | Mutable? |
|---|---|---|---|
| `WORKING_CANDIDATE` | Tip of a `governance/*` or `review/*` branch under active repair (e.g., this branch) | branch head — **not** review authority | Yes — commits expected |
| `REVIEW_CANDIDATE` | Exact immutable commit/tree frozen for qualification, with artifact manifest SHA-256 bound | `CANDIDATE_COMMIT` + `CANDIDATE_TREE` + `MANIFEST_SHA256` + per-file `ARTIFACT_SHA256S` | No — any load-bearing change → `AFFECTED_REVIEW=STALE`, `RE_REVIEW_REQUIRED=YES` |
| `SEALED_CANDIDATE` | `REVIEW_CANDIDATE` after internal qualification genuinely `PASS` under amended governance, manifest regenerated, seal commit created via canonical procedure and verified reproducible | seal commit + tree + timestamp/signer, `specs/CURRENT.md` updated | No — post-seal mutation prohibited |
| `EXECUTION_CANDIDATE` | `SEALED_CANDIDATE` plus bound `model_condition`, `runtime_policy`, `reasoning_effort`, `execution_manifest`, and sealed `session_arithmetic` — the only commit permitted to govern `runs/*` | execution manifest digest, model/runtime binding | No — any model/runtime/seed/arm mutation invalidates batch |

Internal/external review binding must be to an **exact immutable `REVIEW_CANDIDATE` commit/tree and artifact manifest** — not to "latest main" generically.

The authoritative candidate identity is external to this file:
- `specs/CURRENT.md` records the operational pointer;
- `bench/R1/artifact-manifest-v3.json` records the deterministic manifest binding;
- prior independent-review issues (#43/#44) are preserved as `SUPERSEDED` historical surfaces, not sealing authority;
- this procedure records the binding law, not a self-referential SHA.

- If qualification approves `WORKING_CANDIDATE` and the branch moves before merge, that approval is **stale** and a fresh exact-head qualification is required.
- If a load-bearing artifact (`bench/R1/*`, `docs/canonical/R1_V3*`, `.github/workflows/bench-r1-validation.yml`) changes after qualification, `AFFECTED_REVIEW=STALE`.

## 3. Sealing steps — canonical order

### Step 1: Scientific Design Self-Audit (internal, deterministic; voluntary human review optional)

- Internal qualification evaluates **all 16 sections** of `docs/canonical/R1_V3_SCIENTIFIC_REVIEW_PACKET.md` (`WORKING_CANDIDATE` → `REVIEW_CANDIDATE` at freeze) via deterministic checks: `bench/R1/test_review_binding.py`, `bench/R1/validate_v3.py`, `bench/R1/test_scorer.py` adversarial tests, and explicit per-section checklist in the packet.
- Each section must be internally `PASS` via recorded deterministic evidence on the **exact `REVIEW_CANDIDATE`** manifest before sealing. Voluntary external human review of the same 16 sections may be recorded as `OPTIONAL` evidence but is not required and does not by itself create sealing authority.
- Any internal `REJECT` or test failure routes to revision and re-qualification (stale-review rule applies).
- Historical independent-review expectation (16 sections via external reviewer) is `SUPERSEDED`; the same 16 sections are now internally gated.

Required sections (same 16, now internally audited): `CONSTRUCT_VALIDITY`, `DIFFICULTY_WITHOUT_ARTIFICIALITY`, `TASK_TIMELINE_VALIDITY`, `TEMPORAL_LEAKAGE`, `NO_INFORMATION_LEAKAGE`, `NO_ARM_FAVORING`, `BASELINE_FAIRNESS`, `SCORER_VALIDITY`, `ORACLE_VALIDITY`, `CEILING_RISK`, `FLOOR_RISK`, `MAINTENANCE_FAIRNESS`, `MODEL_IDENTITY_ADMISSIBILITY`, `COST_BOUND`, `REPRODUCIBILITY`, `FEHREST_FALSIFIABILITY`.

### Step 2: Statistical Design Self-Audit (internal, deterministic; voluntary human review optional)

- Internal qualification evaluates **all 18 sections** of `docs/canonical/R1_V3_STATISTICAL_REVIEW_PACKET.md` on the **exact `REVIEW_CANDIDATE`** via deterministic proofs: `bench/R1/test_r1v3_statistical_design.py` 19 static edge cases, `bench/R1/test_review_binding.py` formula/binding checks, and validator statistical-parameter checks.
- Each section must be internally `PASS` via recorded deterministic evidence. Voluntary external statistical review is `OPTIONAL`.
- Deterministic worked examples (§5 examples, `bench/R1/test_r1v3_statistical_design.py` proofs) must be internally verified.
- `ψ̂`, `N_pairs`, `K_eligible`, `r_conf` interpretations must match the power formulas in §0–§8 — not `K(K−1)/2`, not `ARM_CONTRAST_COUNT`, not `TASK_COUNT` as `N_pairs`.
- `K_eligible` derivation must respect `B_NULL_EXCLUSION_BEFORE_PSI`, `PSI_USES_ELIGIBLE_OBSERVATIONS`, `R_CONF_USES_K_ELIGIBLE` (statistical packet §2).

### Step 3: Preregistration verification

- `bench/R1/PREREGISTRATION-V2.md` matches `benchmark-spec-v3.json` numerically and semantically (12 checkpoints, 27-before-t14, bounds, formulas).
- Validator `_validate_protocol_documents` asserts `27 of 30` prose vs actual count; `_validate_statistical_parameters` asserts `K_total=30`, bounds, formula-field presence.
- No silent post-hoc modification after `REVIEW_CANDIDATE` freeze.

### Step 4: Manifest schema

- `bench/R1/benchmark-spec-v3.json` is the single source of truth.
- Field-level canonical-derived equality confirmed for `tasks`, `oracles`, `corpus` (`validate_v3.py:_validate_canonical_derived_equality`; `test_validate_v3.py: TestCanonicalDerivedEquality`).
- All derived artifacts (`tasks-v2.json`, `oracles-v2.json`, `corpus-manifest-v2.json`) match spec exactly at `REVIEW_CANDIDATE`.

### Step 5: Artifact digest inventory (exact-head CI must be PASS on REVIEW_CANDIDATE)

```text
benchmark-spec-v3.json → field-level equality vs tasks-v2.json / oracles-v2.json / corpus-manifest-v2.json
bench/R1/validate_v3.py: PASS (0 errors)
bench/R1/test_validate_v3.py: 41/41 OK (6 test classes, includes protocol-doc and mutation coverage)
bench/R1/test_scorer.py: 20/20 OK (includes 4 adversarial tests)
bench/R1/test_r1v3_statistical_design.py: PASS (static design edge cases: K=30/29/20/15/14/0, psi_hat thresholds, N_pairs/r_conf bounds, task-class loss)
bench/R1/test_review_binding.py: PASS (candidate freshness, digest binding, packet formula/status checks, internal supersession)
.github/workflows/bench-r1-validation.yml: test-scorer, test-validator, validate, canonical-equality all PASS
.github/workflows/verify-artifacts.yml: verify-artifacts PASS
```

### Step 6: Exact candidate commit/tree binding — no self-reference

The frozen review identity must be obtained mechanically from Git and recorded in `specs/CURRENT.md` plus the deterministic artifact manifest. Do not hand-invent hashes and do not embed a "latest main" identity in this file.

This separation is intentional: a file cannot reliably pin the SHA of the commit that contains its own bytes without creating a self-reference cycle. The deterministic artifact manifest therefore binds artifact bytes and may carry the generator's pre-manifest candidate commit/tree, while the authoritative review surface binds the exact immutable post-qualification commit/tree.

Required binding record:

```text
REVIEW_CANDIDATE_COMMIT=<exact immutable Git commit from CURRENT/manifest>
REVIEW_CANDIDATE_TREE=<exact tree for REVIEW_CANDIDATE_COMMIT>
MANIFEST_CANDIDATE_COMMIT=<candidate_commit recorded by artifact-manifest-v3.json>
MANIFEST_CANDIDATE_TREE=<candidate_tree recorded by artifact-manifest-v3.json>
MANIFEST_SHA256=<manifest_sha256 recorded by artifact-manifest-v3.json>
ARTIFACT_SHA256S=<all 18 deterministic artifact digests>
MODEL_CONDITION=gpt-5.6-terra / medium / 0.0 / 1024 / []
REASONING_EFFORT=medium
RUNTIME_POLICY=FAIL_CLOSED_ON_IDENTITY_DRIFT; MODEL_VERSION_PIN_STATUS=UNAVAILABLE_FLOATING_ALIAS_RECORD_PER_RUN
SESSION_ARITHMETIC=252+600+120=972
```

Binding validity requires all of:

```text
REVIEW_CANDIDATE_COMMIT_EXISTS=YES
REVIEW_CANDIDATE_TREE_MATCHES_COMMIT=YES
MANIFEST_ARTIFACT_MAP_MATCHES_REVIEW_CANDIDATE_BYTES=YES
EXACT_HEAD_CI_ON_REVIEW_CANDIDATE=PASS
INTERNAL_SCIENTIFIC_SELF_AUDIT=PASS
INTERNAL_STATISTICAL_SELF_AUDIT=PASS
INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
```

A docs-only `specs/CURRENT.md` update after the load-bearing candidate is frozen does not stale the candidate. Any change to a load-bearing artifact does.

### Step 7: Do NOT seal

Do NOT seal while any of:
- `R1_V3_MACHINE_VALIDATION != PASS`
- `R1_V3_VALIDATION_CONVERGENCE != COMPLETE`
- `R1_V3_MUTATION_TESTING != PASS`
- `R1_V3_EXACT_HEAD_CI != PASS`
- `R1_V3_SCIENTIFIC_DESIGN_SELF_AUDIT != PASS`
- `R1_V3_STATISTICAL_DESIGN_SELF_AUDIT != PASS`
- `R1_V3_ADVERSARIAL_VALIDATION != PASS`
- `R1_V3_CONFIRMATORY_EXECUTION=PROHIBITED` is the intended state before sealing — confirmatory execution is authorized only from `SEALED_CANDIDATE` via `EXECUTION_CANDIDATE` manifest
- `R1_V3_UNBLINDING=PROHIBITED`
- `SPEC_002_ACTIVATION` would exceed `specs/CURRENT.md` authority
- Product implementation is not authorized
- `ARTIFACT_MANIFEST_SHA256` not bound to `REVIEW_CANDIDATE_COMMIT/TREE`
- Any review-binding validation (`bench/R1/test_review_binding.py`) fails
- Sealing would rely on `R1_V3_SCIENTIFIC_REVIEW=PASS` or `R1_V3_STATISTICAL_REVIEW=PASS` as mandatory human evidence (that gate is superseded — do not require it)

Human-review PENDING status (issues #43/#44) no longer blocks sealing per `FOUNDER_GOVERNANCE_DECISION_2026-09-08`.

## 4. Post-sealing protocol

After internal qualification genuinely `PASS` (recorded deterministic evidence, not fake human PASS) on the exact `REVIEW_CANDIDATE` under amended governance:

1. Re-verify the exact qualified candidate: no qualified artifact changed (`git diff REVIEW_CANDIDATE..HEAD -- bench/R1 docs/canonical .github/workflows` empty for sealed paths).
2. Run all deterministic validation again: `python bench/R1/validate_v3.py`, `python bench/R1/test_validate_v3.py`, `python bench/R1/test_scorer.py`, `python bench/R1/test_r1v3_statistical_design.py`, `python bench/R1/test_review_binding.py`, `git diff --check`.
3. Generate final artifact manifest (`bench/R1/generate_manifest.py`) against the exact `REVIEW_CANDIDATE` commit/tree; record `MANIFEST_SHA256` and per-file digests.
4. Bind exact commit/tree/manifest/model_condition/runtime_policy/session_arithmetic per Step 6.
5. Create final seal through the canonical procedure (commit that records `SEALED_CANDIDATE=REVIEW_CANDIDATE`, seal timestamp, signer, and digest inventory).
6. Verify seal reproducibility: re-clone at `SEALED_CANDIDATE` and re-run manifest + validation — must reproduce identical digests.
7. Update `specs/CURRENT.md` in the same or immediately following documentation-only commit.
8. Continue immediately to the next authorized R1 gate (valid variance-pilot execution is still prohibited until `SEALED_CANDIDATE` + execution manifest + runtime binding are all sealed; see barrier).

## 5. Review law — authority (amended 2026-09-08)

Hermes may:

```text
prepare
audit
red-team
test
request (open issues, ask for review) — optional under new governance
collect (receive reviewer evidence) — optional
reconcile findings (fix, re-test, re-request)
self-audit scientific/statistical design via deterministic suite (now gating)
```

Hermes may **NOT** self-issue:

```text
INDEPENDENT_HUMAN_SCIENTIFIC_REVIEW=PASS  (superseded — no longer required, and never fake)
INDEPENDENT_HUMAN_STATISTICAL_REVIEW=PASS (superseded — no longer required, and never fake)
R1_V3_SCIENTIFIC_REVIEW=PASS as mandatory human evidence
R1_V3_STATISTICAL_REVIEW=PASS as mandatory human evidence
```

An implementation-bot review does not automatically satisfy scientific/statistical independence. An unavailable reviewer is **not** `PASS` and, per amended governance, is **not** a blocker. If internal qualification fails, the failure is a deterministic blocker until repaired; human review absence is not.

Prior law that recorded `CURRENT_AUTHORIZED_LOCAL_WORK=EXHAUSTED, PROJECT_COMPLETE=NO, BLOCKER=INDEPENDENT_*_REVIEWER_UNAVAILABLE` is superseded for this gate. Under new governance, finish every repository-local qualification task and, if all deterministic gates PASS, proceed to sealing.

Human review remains welcome as `OPTIONAL` evidence:

```text
HUMAN_INDEPENDENT_REVIEW=OPTIONAL
HUMAN_REVIEW_BLOCKING_AUTHORITY=NO
QUALIFIED_HUMAN_REVIEW_EVIDENCE=NONE (truthful — no fake identity)
```

## 6. Exact-head CI authority

Exact-head qualification belongs to the immutable `REVIEW_CANDIDATE`, not to a historical `main` SHA copied into this procedure.

At minimum, the bound candidate must have successful evidence for:

```text
verify-artifacts
test-scorer
test-validator
test-statistical-design
test-review-binding
validate
canonical-equality
manifest-check
```

Never carry CI from an older commit as authority for a mutated candidate. `specs/CURRENT.md` and `bench/R1/artifact-manifest-v3.json` must identify the candidate whose CI was actually checked.

## 7. Historical ceiling routing — preserved

Canonical governance (`PREREGISTRATION-V2.md` §§23–24, `VARIANCE-PILOT-V2.md` §11, `specs/CURRENT.md: R1 outcome routing`) states:

```text
CEILING_EFFECT = NOT_THESIS_SUPPORT
CEILING_EFFECT = NOT_THESIS_FALSIFICATION
NO_SILENT_CONTINUATION
```

Do not silently invent `SECOND_CEILING = THESIS_NOT_SUPPORTED` (`SECOND_CEILING` is `NOT_PREREGISTERED`). If a different interpretation is desired for R1-v3, it must be explicitly preregistered and internally qualified before execution (human review optional under new governance).

## 8. References

- `specs/CURRENT.md` — `ACTIVE_R1_SUBGATE`, `R1 outcome routing`, `NEXT_PRODUCT_SPEC`
- `docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md` — supersession authority
- `docs/canonical/EXECUTION_MASTER_PLAN.md` — R1 required order
- `bench/R1/PREREGISTRATION-V2.md` §§19–20, 28 — exclusion ordering, power rule
- `bench/R1/benchmark-spec-v3.json` — statistical_parameters, historical_sealed_ids, arms, session_arithmetic
- `bench/R1/VARIANCE-PILOT-V2.md` §§6–10 — ψ̂ definition, power bounds
- `docs/canonical/R1_V3_SCIENTIFIC_REVIEW_PACKET.md` / `R1_V3_STATISTICAL_REVIEW_PACKET.md` — design surfaces (now internally audited, human review optional)
