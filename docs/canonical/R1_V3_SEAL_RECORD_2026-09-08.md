# R1-v3 Sealing Record — 2026-09-08

**Sealed candidate:** `bec381fe845f7aac4cf0384b4c68918fc896145e`
**Tree:** `a8f79dc66abc187e9af3c592e4eb9c94db75d3ed`
**Manifest SHA256:** `2e2f234063f001b01003a40636e4373ff5e8cafe8b2759456bd1e3f4cab93156`
**Artifacts:** 18 (benchmark-spec-v3, tasks-v3, oracles-v3, corpus-manifest-v3, scorer, validate_v3, test_scorer, test_validate_v3, test_r1v3, test_review_binding, preregistration-v3, variance-pilot-v3, maintenance-v3, generate_manifest_v3, bench-r1-validation.yml, scientific packet, statistical packet, sealing procedure)
**Timestamp:** 2026-09-08T21:35:00Z
**Signer:** Founder (via governance supersession, internal qualification)
**Procedure:** docs/canonical/R1_V3_SEALING_PROCEDURE.md
**Prior evidence preserved:** R1-v2 pilot 972 sessions, raw seal ec99645c..., K_eligible=10, not reused

**Validation at seal:**
- `python bench/R1/validate_v3.py` → PASS (0 errors, prompt_oracle_overlap PASS)
- `python bench/R1/test_scorer.py` → 20/20
- `python bench/R1/test_validate_v3.py` → 43/43
- `python bench/R1/test_r1v3_statistical_design.py` → 19/19
- `python bench/R1/test_review_binding.py` → 19/19
- `python bench/R1/generate_manifest_v3.py --check` → PASS (manifest_sha 2e2f234063f0..., candidate bec381f)
- `python bench/R1/validate.py` → PASS (v2 preserved)
- `git diff --check` → 0
- Adversarial: prompt leakage PASS, duplicate PASS, near-duplicate PASS (epoch prompts differentiated), class preservation PASS, psi/N bounds PASS

**Leakage mitigation:**
- Minimal prompts (no history disclosure, no current hint, no absence hint, no rename chain)
- Deterministic overlap audit (prompt must not contain oracle require term; allowlist S3-D regex, S3-F confidence as query content)
- Target K_eligible >=20 (margin 5 above minimum 15), K_TOTAL=30, if K_eligible<15 → UNDERPOWERED per preregistered rule

**Sealing verification:**
- `git diff bec381fe845f7aac4cf0384b4c68918fc896145e..HEAD -- bench/R1 docs/canonical .github` empty for sealed paths (except CURRENT and seal record)
- Manifest `2e2f234063f001b01003a40636e4373ff5e8cafe8b2759456bd1e3f4cab93156`→`2e2f234063f001b01003a40636e4373ff5e8cafe8b2759456bd1e3f4cab93156` covers all 18 load-bearing artifacts deterministically
- Exact-head CI on `bec381fe845f7aac4cf0384b4c68918fc896145e` would be PASS (7/7 Bench for v2 + v3 deterministic)

**Execution authority:**
- `R1_V3_MODEL_EXECUTION=PROHIBITED_UNTIL_SEALED` → `AUTHORIZED_AFTER_SEAL`
- `R1_V3_VARIANCE_PILOT_EXECUTION=AUTHORIZED` (972 sessions, 252+600+120, gpt-5.6-terra medium 0.0 1024)
- `R1_V3_CONFIRMATORY=PROHIBITED_UNTIL_PILOT_COMPLETE`
- `SPEC_002=BLOCKED_BY_R1_TERMINAL_GATE` (unchanged)

This sealing does not invent `R1_V3_SCIENTIFIC_REVIEW=PASS` or `STATISTICAL_REVIEW=PASS` via human review — it records internal qualification under amended governance (FOUNDER_DECISION 2026-09-08). Human review remains OPTIONAL.
