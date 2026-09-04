# R1-v2 Sealing Procedure

**Status:** `PREPARATION_COMPLETE`

**Prerequisites:**
- R1_V2_SCIENTIFIC_REVIEW=PENDING_INDEPENDENT_REVIEW
- R1_V2_STATISTICAL_REVIEW=PENDING_INDEPENDENT_REVIEW
- R1_V2_MACHINE_VALIDATION=PASS
- R1_V2_VALIDATION_CONVERGENCE=COMPLETE
- PR #34 merged into main (commit ae155e5)

---

## 1. Sealing Prerequisites (all must be satisfied)

```text
R1_V2_SCIENTIFIC_REVIEW=PENDING_EXTERNAL  → must become PENDING_EXTERNAL_APPROVED
R1_V2_STATISTICAL_REVIEW=PENDING_EXTERNAL → must become PENDING_EXTERNAL_APPROVED
R1_V2_V2_CONFIRMATORY_EXECUTION=PROHIBITED
R1_V2_UNBLINDING=PROHIBITED
PRODUCT_IMPLEMENTATION=PROHIBITED
```

**Sealing CANNOT proceed while either review is PENDING_INDEPENDENT_REVIEW or PENDING_EXTERNAL.**

## 2. Sealing Steps

### Step 1: Independent Scientific Review
- External reviewer must evaluate all 16 sections of `R1_V2_SCIENTIFIC_REVIEW_PACKET.md`
- Each section must move from `PENDING_INDEPENDENT_REVIEW` to `PENDING_EXTERNAL_APPROVED`
- If any section is rejected, the protocol must be revised and re-reviewed

### Step 2: Independent Statistical Review
- External reviewer must evaluate all 18 sections of `R1_V2_STATISTICAL_REVIEW_PACKET.md`
- Each section must move from `PENDING_INDEPENDENT_REVIEW` to `PENDING_EXTERNAL_APPROVED`
- Deterministic worked examples must be independently verified
- ψ̂, r_conf, K_eligible must be computed from actual data, not assumed

### Step 3: Preregistration Verification
- `bench/R1/PREREGISTRATION-V2.md` matches `benchmark-spec-v2.json` exactly
- All numerical claims (27 of 30 tasks before t14, 12 checkpoints, 30 oracles, 96 evidence) verified
- No silent post-hoc modifications to preregistration

### Step 4: Manifest Schema
- `bench/R1/benchmark-spec-v2.json` is the single source of truth
- Field-level canonical equality confirmed for tasks, oracles, corpus
- All derived artifacts (`tasks-v2.json`, `oracles-v2.json`, `corpus-manifest-v2.json`) match spec exactly

### Step 5: Artifact Digest Inventory
```text
benchmark-spec-v2.json tasks/oracles/corpus fields: field-level equality verified
bench/R1/validate.py: PASS (0 errors)
bench/R1/test_validate.py: 41/41 OK
bench/R1/test_scorer.py: 20/20 OK
.github/workflows/bench-r1-validation.yml: test-scorer, test-validator, validate, canonical-equality all PASS
```

### Step 6: Exact Candidate Commit/Tree Binding
- Merge commit: `ae155e5` (latest main)
- Previous merge: `f8a0dd5` (PR #34 merge)
- Implementation commit: `ec7a1ea`
- Pre-bootstrap sealed R1 v1.1: `ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c`
- Evidence SHA: `d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b`

### Step 7: Do NOT Seal
Do NOT seal while:
- `R1_V2_SCIENTIFIC_REVIEW=PENDING` (any variant)
- `R1_V2_STATISTICAL_REVIEW=PENDING` (any variant)
- `R1_V2_V2_CONFIRMATORY_EXECUTION=PROHIBITED`
- `R1_V2_UNBLINDING=PROHIBITED`
- Product implementation is not authorized

## 3. Post-Sealing Protocol

After both reviews are externally approved:

1. Update `specs/CURRENT.md` to reflect sealing completion
2. Record exact seal timestamp and signer
3. Create seal manifest with SHA-256 of all sealed artifacts
4. Bind seal to exact commit tree
5. Do NOT modify sealed artifacts post-sealing

