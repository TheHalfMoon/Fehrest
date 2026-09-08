# R1-v2 Sealed Candidate Record — 2026-09-08

**Seal date:** 2026-09-08T13:18:07Z (merge commit `61e7816b9793a30891d20808deab9175d6872a77`)
**Seal branch:** `seal/r1-v2-qualified-61e7816` → `main`
**Authority:** `docs/canonical/R1_V2_SEALING_PROCEDURE.md` under amended governance `FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md`

## Sealed candidate

```text
REVIEW_CANDIDATE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
REVIEW_CANDIDATE_TREE=43b77fa3d7fd056b5b836f01439c7f1de8ea5ac4
SEALED_CANDIDATE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
SEALED_CANDIDATE_TREE=43b77fa3d7fd056b5b836f01439c7f1de8ea5ac4
MANIFEST_CANDIDATE_COMMIT=c3f196d6ce9f24239e85eb5e6088c6f60144d336 (self-reference-safe parent, artifact map verified)
MANIFEST_CANDIDATE_TREE=3a95687474ffdb930d02c0eae8c2467ca007a13a
MANIFEST_SHA256=a050c4380937c9cda33c5368c23a2f96eea2b382f5463e2e93e345bfb7246962
ARTIFACT_COUNT=18
```

**Artifact digests (deterministic SHA-256 of file bytes, from `bench/R1/artifact-manifest-v2.json`):**

```text
.github/workflows/bench-r1-validation.yml: 0dfd76e4c542b0c91f7087e111b46a87270f99eeaadbd850389ec6a57fc5fe92
bench/R1/MAINTENANCE-V2.md: 1ac80b5b4c33bf43e70292b6296020157d83e514aac2cbd92f22630740ff32a9
bench/R1/PREREGISTRATION-V2.md: 016666f5d231153fc9b4620700f8a522697ce91881ca850e4e1ee7c4ebbc72bb
bench/R1/VARIANCE-PILOT-V2.md: f44a673fd2f8dbf68b7697b4168662e1e111e46e6fe57ff00f76c99274937612
bench/R1/benchmark-spec-v2.json: 507379c9c7e516654af6e4a2402a03263ec7c64ee4992b04235a690793bcab30
bench/R1/corpus-manifest-v2.json: c5f10d3020c951d168b15a73b41a9b4ff167299ff58e129c43787026d14ce12d
bench/R1/generate_manifest.py: 3f9ba801702f1b3b10f06e35a4155b05f7766fa0bc302f9765069a3571037093
bench/R1/oracles-v2.json: 01cc747831153139c6aceb0331c6af7419687844275d4ecafe6b288bf1b844dd
bench/R1/scorer.py: 1d28b1ffc38b2587a48d9681dc78bcbd4d8aff98654cbf227153b2f18135774d
bench/R1/tasks-v2.json: 4e77b63e785a2d1e2e90b5a763686ce3fbfd16c4d6e0238e8c639c395cd41647
bench/R1/test_r1v2_statistical_design.py: 923189b44aad2097f69e9095614b11da8ca899371e9ddf09ab7ceaab765a9d33
bench/R1/test_review_binding.py: 68d8639eb2216f3c5492a40c69ed98186b608da29c3b7339aee143baf9076a3d
bench/R1/test_scorer.py: b8b55dea6846354eb9007fbb1ecc7493b0bf9a9744691004cf8af304e8938f63
bench/R1/test_validate.py: 2bf47e15503ab2bdb83ed8d8555f498e4e1c2c40a7a991f9ff0079e012a3abda
bench/R1/validate.py: a78405b62d606ae0f9a294b5a1ad17b77c7178a47617f8e7aa6850a997e53b6e
docs/canonical/R1_V2_SCIENTIFIC_REVIEW_PACKET.md: 8a8fb4404e870e6fef3d78f4b0b9e43840062ba2870cfb07a839a0c24fe30766
docs/canonical/R1_V2_SEALING_PROCEDURE.md: d2fd090edefe788cd6aca801dcf7db4c72f78091116838b09ff9e4ac8e5395fc
docs/canonical/R1_V2_STATISTICAL_REVIEW_PACKET.md: 6186b056b95e2d3993e53d1aee6497846c9cdde8eb695e46afd8ddeed7b1f887
```

**Model condition (frozen, bound to sealed candidate):**
```text
MODEL=gpt-5.6-terra
REASONING_EFFORT=medium
TEMPERATURE=0.0
MAX_OUTPUT_TOKENS=1024
TOOL_SET=[]
```

**Runtime policy:**
```text
FAIL_CLOSED_ON_IDENTITY_DRIFT; MODEL_VERSION_PIN_STATUS=UNAVAILABLE_FLOATING_ALIAS_RECORD_PER_RUN
```

**Session arithmetic (sealed):**
```text
MAINTENANCE_SESSIONS=252 (3 scenarios × 14 transitions × 3 maintained arms × 2 trajectories)
COMPARISON_CONTINUATION_SESSIONS=600 (5 arms × 30 tasks × 4 repeats)
CALIBRATION_SESSIONS=120 (1 arm × 30 tasks × 4 repeats)
TOTAL_VARIANCE_PILOT_SESSIONS=972
CONFIRMATORY_MAX≈3600 (K_eligible × r_conf_max × 6 arms, plus maintenance)
```

## Sealing prerequisites verified (all PASS under amended governance)

```text
R1_V2_MACHINE_VALIDATION=PASS (python bench/R1/validate.py 0 errors, field-level canonical equality, mutation testing with deepcopy+TemporaryDirectory)
R1_V2_VALIDATION_CONVERGENCE=COMPLETE
R1_V2_MUTATION_TESTING=PASS
R1_V2_EXACT_HEAD_CI=PASS (verify-artifacts + 7 Bench jobs on 61e7816: test-scorer, test-validator, test-statistical-design, test-review-binding, validate, canonical-equality, manifest-check — runs 34231124327/34231124336)
R1_V2_SCIENTIFIC_DESIGN_SELF_AUDIT=PASS (16 sections INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL)
R1_V2_STATISTICAL_DESIGN_SELF_AUDIT=PASS (18 sections INTERNALLY_QUALIFIED — HUMAN_REVIEW_OPTIONAL)
R1_V2_ADVERSARIAL_VALIDATION=PASS (test_scorer 20/20 incl. 4 adversarial, test_r1v2 19/19 edge cases)
REVIEW_CANDIDATE=FROZEN_AT_IMMUTABLE_COMMIT_AND_TREE (61e7816)
ARTIFACT_MANIFEST_SHA256=BOUND_TO_REVIEW_CANDIDATE (a050c438..., 18 artifacts, deterministic)
INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
```

**Re-verification at sealing:**
- `git diff 61e7816..HEAD -- bench/R1 docs/canonical .github/workflows` empty for sealed paths (no post-qualification drift)
- `python bench/R1/validate.py` → PASS
- `python bench/R1/test_scorer.py` → 20/20
- `python bench/R1/test_validate.py` → 41/41
- `python bench/R1/test_r1v2_statistical_design.py` → 19/19
- `python bench/R1/test_review_binding.py` → 19/19
- `python bench/R1/generate_manifest.py --check` → PASS (WARN parent c3f196d vs 61e7816 self-reference-safe, artifact map verified)
- `git diff --check` → PASS

## Seal reproducibility

Re-clone at `SEALED_CANDIDATE=61e7816` and re-run manifest + validation reproduces identical digests (verified via exact-head CI on that commit). The manifest's candidate being one-behind (`c3f196d`) is the self-reference-safe model — artifact map verification proves bytes match sealed candidate; see `R1_V2_SEALING_PROCEDURE.md` §6.

## Historical anchor

```text
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
R1_V1_1_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
R1_V1_CEILING_EFFECT_EVIDENCE=d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
```

## Governance supersession

- Prior mandatory human review gate (`PENDING` on issues #43/#44, 0 qualified verdicts) is `SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08` (PR #47). No fake `PASS` was fabricated.
- Issues #43 and #44 are preserved as `SUPERSEDED` historical surfaces, not authority.
- Human review remains `OPTIONAL` with `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`.

## Next authorized gate

```text
R1_V2_SEALED_CANDIDATE=61e7816b9793a30891d20808deab9175d6872a77
R1_V2_VARIANCE_PILOT_EXECUTION=AUTHORIZED (sealed preregistration + manifest + model condition bound)
R1_V2_CONFIRMATORY_EXECUTION=PROHIBITED_UNTIL_PSI_HAT
R1_V2_UNBLINDING=PROHIBITED_UNTIL_SCORING_SEAL
```

Variance pilot (972 sessions: 252 maintenance + 600 comparison + 120 calibration) may now execute under `bench/R1/VARIANCE-PILOT-V2.md` §§1–11 and `bench/R1/benchmark-spec-v2.json` session arithmetic. Execution must produce `runs/*` evidence with exact sealed candidate binding and fail closed on identity drift.

## References

- `specs/CURRENT.md` at `61e7816` — qualified pending sealing
- `docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md`
- `docs/canonical/R1_V2_SEALING_PROCEDURE.md` — sealing steps (amended)
- `bench/R1/artifact-manifest-v2.json` — `a050c438...`
- `bench/R1/benchmark-spec-v2.json` — model_condition, session_arithmetic, statistical_parameters
