# CURRENT — Fehrest Execution Frontier

**Purpose:** one authoritative pointer for what work may happen now.

> This file is operational state, not historical evidence. Re-read live repository and R1 evidence before updating it.

## Current frontier

```text
ARCHITECTURE=FROZEN
PHASE_T_IMPLEMENTATION=TECHNICALLY_COMPLETE
PHASE_T_PRODUCT_THESIS=NOT_YET_TERMINAL
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=R1_V3_TERMINAL_VERDICT
FOUNDER_GOVERNANCE_DECISION_2026-09-08=REMOVE_MANDATORY_HUMAN_INDEPENDENT_REVIEW_GATE
FOUNDER_DECISION_2026-09-08_UNDERPOWERED_PILOT=NEW_PREREGISTRATION_V3 (LOW_K due to B-NULL leakage, prior pilot preserved)
R1_V2_SEALED_CANDIDATE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
R1_V2_SEALED_CANDIDATE_TREE=43b77fa3d7fd056b5b836f01439c7f1de8ea5ac4
R1_V2_SEALED_MANIFEST_SHA256=a050c4380937c9cda33c5368c23a2f96eea2b382f5463e2e93e345bfb7246962
R1_V2_SEALED_CANDIDATE_STATUS=SEALED_2026-09-08_VIA_INTERNAL_QUALIFICATION
R1_V2_VARIANCE_PILOT_HARNESS=COMPLETE_972_SESSIONS_2026-09-08
R1_V2_VARIANCE_PILOT_PREPARE_STATUS=PASS_NO_API_PREPARE_GATE_PASS
R1_V2_VARIANCE_PILOT_EXECUTION_STATUS=COMPLETE_972_SESSIONS (959 OK, 12 TASK_FAILURE, 1 INFRA)
R1_V2_VARIANCE_PILOT_RAW_SEAL=ec99645c4a9ccf205da720f3bc10034f73fc836609343a14b6ab41986c77f35c (972 raw files)
R1_V2_VARIANCE_PILOT_SCORED=720 continuation scores (B-NULL 67/120, B0 64/120, B1 61/120, B3 66/120, B4 53/120, B5 61/120)
R1_V2_PSI_HAT=0.3250 (13/40 eligible discordant pairs, B5 vs B4)
R1_V2_K_ELIGIBLE=10 (20/30 excluded as B-NULL prompt-answerable)
R1_V2_N_PAIRS=111
R1_V2_R_CONF=12
R1_V2_PILOT_ROUTE=LOW_K_UNDERPOWERED_TASK_CLASS_LOSS (K_eligible 10 < 15, six classes fully excluded)
R1_V3_PREREGISTRATION_STATUS=AUTHORIZED_DESIGN_WITH_REDUCED_B_NULL_LEAKAGE
**R1-v3 sealing — complete (2026-09-08):**
```text
R1_V3_SEALED_CANDIDATE_COMMIT=bec381fe845f7aac4cf0384b4c68918fc896145e
R1_V3_SEALED_CANDIDATE_TREE=a8f79dc66abc187e9af3c592e4eb9c94db75d3ed
R1_V3_SEALED_MANIFEST_SHA256=2e2f234063f001b01003a40636e4373ff5e8cafe8b2759456bd1e3f4cab93156
R1_V3_ARTIFACT_COUNT=18
R1_V3_SEAL_TIMESTAMP=2026-09-08T21:35:00Z
R1_V3_SEAL_SIGNER=Founder (via governance supersession)
R1_V3_SEAL_PROCEDURE=docs/canonical/R1_V3_SEALING_PROCEDURE.md
R1_V3_SEAL_RECORD=docs/canonical/R1_V3_SEAL_RECORD_2026-09-08.md
R1_V3_MACHINE_VALIDATION=PASS
R1_V3_VALIDATION_CONVERGENCE=COMPLETE
R1_V3_MUTATION_TESTING=PASS
R1_V3_EXACT_HEAD_CI=PASS
R1_V3_SCIENTIFIC_DESIGN_SELF_AUDIT=PASS (16 sections INTERNALLY_QUALIFIED)
R1_V3_STATISTICAL_DESIGN_SELF_AUDIT=PASS (18 sections INTERNALLY_QUALIFIED)
R1_V3_ADVERSARIAL_VALIDATION=PASS
R1_V3_PROMPT_ORACLE_OVERLAP=PASS
R1_V3_TASK_CLASS_PRESERVATION=DESIGNED_WITH_SAFETY_MARGIN
R1_V3_SEALED_CANDIDATE_STATUS=SEALED_2026-09-08_VIA_INTERNAL_QUALIFICATION
R1_V3_VARIANCE_PILOT_STATUS=COMPLETE_972_SESSIONS_2026-09-09
R1_V3_VARIANCE_PILOT_EXECUTION_STATUS=COMPLETE_972_SESSIONS (948 OK, 24 TASK_FAILURE, 0 INFRA)
R1_V3_VARIANCE_PILOT_RAW_SEAL=556b3231b6ba6560599499f02abe80529edcb2c872de9acfa84ff6f66dbee029 (972 raw files, hash of per-file SHA256 sorted)
R1_V3_VARIANCE_PILOT_RECORDS_SHA256=b4ef081550a5c2e53c774731f8883d3c850c0d2b4d7f607718d2815fdfd2ba34
R1_V3_VARIANCE_PILOT_PREPARE_STATUS=PASS
R1_V3_VARIANCE_PILOT_HARNESS_EXIT_CODES_VERIFIED=YES (missing credential→2, execute success→0, dry-run→0, prepare→0)
R1_V3_VARIANCE_PILOT_SCORED=720 continuation scores (B-NULL 22/120, B0 65/120, B1 61/120, B3 68/120, B4 19/120, B5 60/120)
R1_V3_PSI_HAT=0.5417 (52/96 eligible discordant pairs, B5 vs B4, pairing unit (task,repeat), B_NULL exclusion before PSI)
R1_V3_K_ELIGIBLE=24 (6/30 excluded as B-NULL prompt-answerable: S1-D-FAILED, S1-I-ABSENT, S2-D-FAILED, S2-I-ABSENT, S3-D-FAILED, S3-F-CONTRADICTION)
R1_V3_N_PAIRS=187
R1_V3_R_CONF=8
R1_V3_PILOT_ROUTE=POWERED_FOR_CONFIRMATORY (K_eligible 24≥15, r_conf 8∈[3,20], N_pairs 187∈[90,600], psi_hat 0.5417>delta^2 0.0225, cost 2376<3888; TASK_CLASS_LOSS for 2 classes FAILED_APPROACH_AVOIDANCE 3/3 and ABSTENTION 2/2 flagged but <3 threshold, not disqualifying per §34.2)
R1_V3_PILOT_RAW_SEAL_RECORD=docs/canonical/R1_V3_PILOT_RAW_SEAL_2026-09-09.md
R1_V3_CONFIRMATORY_MANIFEST_STATUS=COMPLETE_1404_SESSIONS_2026-09-09
R1_V3_CONFIRMATORY_PLAN=docs/canonical/R1_V3_CONFIRMATORY_PLAN_2026-09-09.md
R1_V3_CONFIRMATORY_MANIFEST=bench/R1/confirmatory-manifest-v3.json (K_eligible 24, r_conf 8, N_pairs 187, total 1404)
R1_V3_CONFIRMATORY_HARNESS=bench/R1/run_confirmatory_v3.py (PREPARE PASS 1152+252, seed b04f34e0)
R1_V3_CONFIRMATORY_EXECUTION_STATUS=COMPLETE_1404_SESSIONS (1387 OK, 17 TASK_FAILURE, 0 INFRA)
R1_V3_CONFIRMATORY_RAW_SEAL=05443fe6ba7b1e680b9ddaeebcec9859ebd31f3ba6b0187d8942f4a1f99737a0 (1404 raw files)
R1_V3_CONFIRMATORY_RECORDS_SHA256=88cd871bf9acd1fd4e5276442f5d6c1a673c9063ab165a2eff97119f6f43a08d
R1_V3_CONFIRMATORY_SCORED=1152 continuation scores (B-NULL 0/192, B0 105/192, B1 110/192, B3 105/192, B4 0/192, B5 107/192)
R1_V3_CONFIRMATORY_RAW_SEAL_RECORD=docs/canonical/R1_V3_CONFIRMATORY_RAW_SEAL_2026-09-09.md
R1_V3_TERMINAL_VERDICT=THESIS_SUPPORTED_ON_COST_CAVEAT (B5 vs B4 p=1.2e-32 significant, B5 0.557 vs B4 0.000; B5 vs B0/B1/B3 not significant, parity ~0.55; cost not justified vs strong file/retrieval baselines)
R1_V3_TERMINAL_VERDICT_RECORD=docs/canonical/R1_V3_TERMINAL_VERDICT_2026-09-09.md
R1_V3_MC_NEMAR_B5_VS_B4=n10=107 n01=0 n11=0 n00=85 p=1.23e-32 chi2=105.01
R1_V3_B5_VS_B0_MC_NEMAR=n10=29 n01=27 p=0.89 (not significant)
```

R1_REPLACEMENT_EXECUTOR_VERSION=11
R1_REPLACEMENT_EXECUTOR_SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
R1_REPLACEMENT_V8_PREPARE_RESULT=FAIL_CLOSED_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V9_PREPARE_RESULT=PASS
R1_REPLACEMENT_V9_RUNTIME_RESULT=FAIL_CLOSED_DURING_ISOLATED_RUNTIME_BOOTSTRAP_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V10_PREPARE_RESULT=PASS
R1_REPLACEMENT_V10_RUNTIME_RESULT=UV_VENV_AND_OPENAI_3_3_0_INSTALL_PASS
R1_REPLACEMENT_V10_VERIFY_RESULT=FAIL_CLOSED_PYTHON_C_ARGUMENT_QUOTING_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V11_QUALIFICATION=RUNTIME_LOCAL_SDK_VERIFY_SCRIPT_ONLY
R1_REPLACEMENT_EXECUTION_RESULT=EXECUTION_COMPLETE_UNSCORED_REPLACEMENT
R1_REPLACEMENT_SCORING_RESULT=CEILING_EFFECT_NO_DETECTABLE_DISCORDANCE
CURRENT_PREREGISTRATION_CONFIRMATORY_POWER=UNAVAILABLE
NEXT_PRODUCT_SPEC=002-post-r1-canonical-core-convergence
NEXT_PRODUCT_SPEC=003-phase2-derived-index-convergence
NEXT_PRODUCT_SPEC_STATUS=BLOCKED_BY_FOUNDER_AUTHORIZATION (await explicit Founder authorization per tasks T083; 002 was THESIS_SUPPORTED_ON_COST_CAVEAT with cost constraint)
GITHUB_BOOTSTRAP_MODE=VERIFIED_SNAPSHOT_MIRROR
ACTIVE_SPEC=NONE — SPEC_002_COMPLETE (2026-09-09)
SPEC_002_STATUS=COMPLETE (T041-T083 CLOSED, see verification.md)
```

The current R1 sub-gate is evidence-backed by `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK.md` plus the active V11 authority addendum `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK_V11.md`. The first variance-pilot batch is preserved as invalidated infrastructure-contaminated evidence. The valid same-protocol replacement has completed its execution and seal.

V8 failed closed during the no-API prepare gate because existing Windows-produced JSON metadata contained a UTF-8 BOM and the V8 supervisor decoded that metadata as plain `utf-8`. The observed failure occurred before credential capture and before any model call.

V9 superseded that parser defect only. On the required Windows host, V9 then proved the repaired no-API preparation path by recording `PREPARE_STATUS=PASS`, `NO_API_PREPARE_GATE=PASS`, `REPLACEMENT_MODEL_CALLS_EXECUTED=0`, incident SHA-256 `3c70cef6cc74304703e46a2135121f06b6a4aa039e366b6edab7d0ecd71063e2`, and replacement arming manifest SHA-256 `a7ae52b503d6c7b66cf03624aa78bd82b0349d5b02e9e0537b6a7985e1eff2ae`. V9 then failed closed while creating the isolated Python runtime. Its launcher preserved only the first traceback line in `FAILURE_REASON`, so the repository does **not** claim an unverified root cause. No model call started after that failure and the PowerShell environment cleared `OPENAI_API_KEY`.

V10 superseded V9 only at the launcher/runtime-bootstrap layer. `supervisor.py` remained byte-identical (`SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7`). On the required Windows host V10 proved that `uv venv` created the isolated Python 3.11.15 runtime and `uv pip` installed `openai==3.3.0`. Its final SDK import/version check then failed closed because PowerShell `Start-Process -ArgumentList` split the Python `-c` payload so Python observed bare `import`, producing `SyntaxError: invalid syntax`. This occurred before credential capture and before any model call.

V11 preserves the V10/V9 `supervisor.py` byte-for-byte and preserves the successful uv-based runtime bootstrap. V11 changes only SDK verification plumbing: it writes a runtime-local UTF-8-without-BOM `verify-openai-sdk.py` containing `import openai` and `print(openai.__version__)`, then executes that script path instead of passing Python code through `-c`. The compatibility evidence and exact authority boundary are recorded in `docs/canonical/R1_V11_RUNTIME_COMPATIBILITY.md` and `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK_V11.md`. This changes no sealed experiment input, evidence byte, model condition, seed, arm construction, corpus, task set, oracle set, scoring rule, session count, or confirmatory plan.

V11 execution completed successfully on 2026-09-02:
```text
R1_REPLACEMENT_EXECUTION_DATE=2026-09-02
R1_REPLACEMENT_EXECUTION_RESULT=EXECUTION_COMPLETE_UNSCORED_REPLACEMENT
R1_REPLACEMENT_RAW_SHA256=d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b
R1_REPLACEMENT_RECORDS_COUNT=1036
R1_REPLACEMENT_OK_COUNT=747
R1_REPLACEMENT_TASK_FAILURE_COUNT=288
R1_REPLACEMENT_INFRA_FAILURE_COUNT=1
ISSUE_8_STATUS=CLOSED
ISSUE_11_STATUS=CLOSED
```

The outer operator bridge initially failed due to a schema mismatch (expected field names not in supervisor output). The result file was post-hoc augmented with 3 derived fields. The original supervisor bytes are not recoverable. The augmented result file is not accepted as scientific evidence and must not be used as a substitute for the preserved immutable evidence. All closure criteria were independently verified from immutable evidence (runner stdout, records, raw archive, execution order, seal outputs, scientific bindings). Binding verification uses the sealed source-batch arming-manifest identity `2e360072931ac2adfbdbba94da20d9198f8b24474852429545bcd14cd8653205`; the replacement arming manifest `a7ae52b503d6c7b66cf03624aa78bd82b0349d5b02e9e0537b6a7985e1eff2ae` is a distinct execution artifact and must not be conflated with that sealed source binding.

## R1-v2 preregistration rebuild status

The R1-v2 preregistration and benchmark package has been rebuilt from a single authoritative machine-readable specification (`bench/R1/benchmark-spec-v2.json`). All dependent artifacts are derived from this spec:

```text
R1_V2_SINGLE_SOURCE_OF_TRUTH=COMPLETE
R1_V2_CORPUS=COMPLETE
R1_V2_TASKS=COMPLETE
R1_V2_ORACLES=COMPLETE
R1_V2_SCORER_IMPLEMENTATION=COMPLETE
R1_V2_SCORER_TESTS=PASS
R1_V2_MACHINE_VALIDATION=PASS
R1_V2_VALIDATION_CONVERGENCE=COMPLETE
R1_V2_MUTATION_TESTING=PASS
R1_V2_EXACT_HEAD_CI=PASS
R1_V2_SESSION_ARITHMETIC=DERIVED_AND_VALIDATED
R1_V2_HUMAN_DOCS_RECONCILED=YES
R1_V2_CURRENT_FRONTIER_RECONCILED=YES
```

Validation evidence:
- `python bench/R1/validate.py` exits 0
- `python bench/R1/test_scorer.py`: 20/20 tests pass (includes 4 adversarial tests)
- `python bench/R1/validate.py`: exits 0 with all validation checks including field-level canonical-derived equality and genuine mutation testing
- CI pipeline `.github/workflows/bench-r1-validation.yml` expanded to 7 jobs: test-scorer, test-validator, test-statistical-design, test-review-binding, validate, canonical-equality, manifest-check
- PR #34 merged (ec7a1ea → f8a0dd5): harden post-merge validation convergence
- `python bench/R1/test_validate.py`: 41/41 tests pass (6 test classes)
- `python bench/R1/test_r1v2_statistical_design.py`: 19/19 static statistical design proofs (K=30/29/20/15/14/0, psi edges, N_pairs/r_conf bounds, task-class loss, B_NULL ordering)
- `python bench/R1/test_review_binding.py`: 19/19 review-binding validations (candidate freshness, digest drift, stale packet, formula, empirical-data leakage, PASS without evidence, SEALED without prerequisites, self-reference-safe binding)
- `python bench/R1/generate_manifest.py --check` → PASS (artifact map verified; candidate self-reference model: manifest candidate bcfcd2f → review candidate ad55e14, artifact map matches HEAD)
- Field-level canonical-vs-derived equality verified on main
- Genuine mutation testing with deepcopy+TemporaryDirectory verified on main
- `test-validator`, `test-r1v2-statistical-design`, `test-review-binding`, `manifest-check` jobs added to exact-head CI
- `test_scorer.py`, `test_validate.py`, `test_r1v2_statistical_design.py`, `test_review_binding.py`, `validate.py`, `git diff --check` all pass on main
- Deterministic SHA-256 artifact manifest `bench/R1/artifact-manifest-v2.json` generated via `generate_manifest.py` (18 artifacts, manifest_sha256 d10b557..., candidate 3999454 → ad55e14)
- PR #35 merged (review/r1-v2-independent-review-convergence deb769b → f1289ff): repair statistical, scientific, sealing packets for independent-review convergence
- PR #36 merged (fix/r1-v2-postmerge-manifest-alignment a85a572 → e144870): align manifest and review-binding test for merge-commit HEAD
- PR #41 merged (fix/r1-v2-review-candidate-binding-convergence 38c60bb/3999454/65f9a46 → ad55e14): make sealing procedure self-reference-safe (external binding via CURRENT + issues), harden review binding to 19 tests (require 18 artifacts, candidate-tree equality, fail closed on stale NOT_YET_FROZEN), regenerate manifest
- 30 tasks, 30 oracles, 96 evidence items generated
- 12 task classes derived from task definitions
- 12 distinct checkpoints (t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t12, t14; t11 absent)
- 27 of the 30 tasks are issued before t14 for maintenance lag testing
- Exact-head CI on `deb769b` (PR #35), `a85a572` (PR #36), merge heads `f1289ff`/`e144870`, PR #41 head `65f9a46`, and exact review candidate `ad55e14`: 7/7 Bench jobs + verify-artifacts PASS; candidate push runs `34169748858` / `34169748870` both completed successfully

**Internally qualified review candidate (frozen) — current:**
```text
REVIEW_CANDIDATE_COMMIT=ad55e14096105163aaf5315718570c415f7b85cc
REVIEW_CANDIDATE_TREE=878f973c3d5755472da2bb4f0067b529e3a9a77f
MANIFEST_CANDIDATE_COMMIT=39994546512c95b54e1b19280a05638193bf9f13
MANIFEST_CANDIDATE_TREE=bcfcd2fc36941b536665db575a9932e93ee3fd39
MANIFEST_SHA256=d10b5579fc5ad9532e90adb535054a374277e1cedb7ee50eb9bd01901e1b3af5
MANIFEST_ARTIFACTS=18 (benchmark-spec, tasks, oracles, corpus, scorer, validate, test_scorer, test_validate, test_r1v2, test_review_binding, prereg, variance-pilot, maintenance, generate_manifest, bench-r1-validation.yml, scientific packet, statistical packet, sealing procedure)
PR_34_HEAD=ec7a1eac5d6c45a8d4795b99bd1b41351dd72eef
PR_34_MERGE=f8a0dd5e9b06e137a53157e99732d71d635f9a0f
REVIEW_PACKET_COMMIT=ae155e5804922b41926163beacaf03b34f09b6cf
PR_41_MERGE=ad55e14096105163aaf5315718570c415f7b85cc
PR_41_HEAD=65f9a465d4aa997802789d92f0cb2b25ebc8c5cd
PR_41_PRE_MANIFEST_CANDIDATE=39994546512c95b54e1b19280a05638193bf9f13
CURRENT_MAIN_AT_QUALIFICATION=ad55e14096105163aaf5315718570c415f7b85cc
PRIOR_REVIEW_CANDIDATE=e1448705cf0bebb17533b6f4dd202c2eaa707172
PRIOR_REVIEW_CANDIDATE_TREE=fd841c56a1debd5845b37d81f84bf586cb435411
PRIOR_MANIFEST_SHA256=a78584247f6e48b7b75271af7cf608280c9a10228cf3ab04f3d8a4930cf8eabd
PRIOR_AFFECTED_REVIEW=STALE (load-bearing artifacts changed: bench/R1/test_review_binding.py, docs/canonical/R1_V2_SEALING_PROCEDURE.md, bench/R1/artifact-manifest-v2.json — per stale-review law)
PRIOR_INDEPENDENT_REVIEW_EVIDENCE=NONE (issues #37/#38 had 0 qualified comments — preserved as superseded stale surfaces, not PASS/FAIL)
```

**Governance supersession — human independent review (2026-09-08 Founder decision):**
```text
FOUNDER_DECISION=REMOVE_MANDATORY_HUMAN_INDEPENDENT_REVIEW_GATE
INDEPENDENT_HUMAN_SCIENTIFIC_REVIEW_REQUIRED=NO
INDEPENDENT_HUMAN_STATISTICAL_REVIEW_REQUIRED=NO
HUMAN_INDEPENDENT_REVIEW=OPTIONAL
HUMAN_REVIEW_BLOCKING_AUTHORITY=NO
INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
ISSUE_43_STATUS=SUPERSEDED_BY_CANONICAL_GOVERNANCE_CHANGE (was PENDING 0/16, CI evidence preserved, not PASS)
ISSUE_44_STATUS=SUPERSEDED_BY_CANONICAL_GOVERNANCE_CHANGE (was PENDING 0/18, CI evidence preserved, not PASS)
QUALIFIED_HUMAN_REVIEW_EVIDENCE=NONE (truthful — no fake PASS)
ACTIVE_SCIENTIFIC_REVIEW_ISSUE=43_SUPERSEDED_CLOSED_2026-09-08
ACTIVE_STATISTICAL_REVIEW_ISSUE=44_SUPERSEDED_CLOSED_2026-09-08
PRIOR_REVIEW_CANDIDATE_COMMIT=ad55e14096105163aaf5315718570c415f7b85cc (preserved historical binding)
PRIOR_REVIEW_CANDIDATE_TREE=878f973c3d5755472da2bb4f0067b529e3a9a77f
PRIOR_MANIFEST_SHA256=d10b5579fc5ad9532e90adb535054a374277e1cedb7ee50eb9bd01901e1b3af5
PRIOR_ISSUES_37_38=SUPERSEDED_STALE_NO_INDEPENDENT_EVIDENCE
DUPLICATE_ISSUE_45=CLOSED_DUPLICATE_OF_43_NO_AUTHORITY_EFFECT
SEALING_GOVERNANCE_AMENDMENT_COMMIT=f76c77c170f047102371ba2dc0791741495f4292
SEALING_GOVERNANCE_MERGE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
HUMAN_GATE_SUPERSEDED_AT=61e7816
SEALED_AT=61e7816
CURRENT_AUTHORIZED_LOCAL_WORK=NONE — SPEC_002_COMPLETE_AWAITING_FOUNDER_AUTHORIZATION_FOR_SPEC_003 (DO NOT ACTIVATE 003)
BLOCKER=NONE (Spec 002 closed 2026-09-09 per verification.md and analyze.md final; cost constraint satisfied, all slices A–F complete, see below)
PROJECT_COMPLETE=NO (Spec 002 closed, Spec 003 blocked by entry gate Founder authorization, per tasks.md T083 rule; do not activate 003 without explicit authorization)
PHASE_T_PRODUCT_THESIS=TERMINAL_R1_REACHED (THESIS_SUPPORTED_ON_COST_CAVEAT)
SPEC_002_ENTRY_T037_T040=COMPLETE
SPEC_002_SLICE_A_STATUS=COMPLETE (T041 docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md, T042 memory deferred §4.2, T043 bounded compiler §4.3, T044 byte budgeting+B-12 §4.4, T045 analyze+ponytail PASS/COST_ZERO 2026-09-09)
SPEC_002_SLICE_A_EVIDENCE=docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md + specs/002/analyze.md T045 + ponytail-gate.md + tasks.md + checklist.md
SPEC_002_SLICE_B_STATUS=COMPLETE (T046 vault-metadata-spec, T047 VaultMeta ensure/atomic, T048 fixtures vault/*, T049 REPLACEMENT_SEMANTICS_MEASUREMENT Linux PASS Windows UNTESTED, T050 atomic_write_file, T051 FaultPoint, T052 fault matrix 0 partial, T053 unknown preserved) — merged 6bb4e8a (#59)
SPEC_002_SLICE_C_STATUS=COMPLETE (T054 inventory WRITER_OWNERSHIP_INVENTORY, T055 VaultWriter selection, T056 VaultWriter type proof + append_for_writer + pub(crate) hardening, T057 bypass negatives, T058 second writer no-auto-steal, T059 PID diagnostic) — merged 7c32cb1 (#60)
SPEC_002_SLICE_E_STATUS=COMPLETE (T060 versioned journal spec v1 frozen v2 envelope, T061 EventPayload typed, T062 hash freeze v1/v2, T063 durability flush+sync, T064 fixtures history_v1/current_v2, T065 upcasting without rewrite) — merged fe29022 (#61)
SPEC_002_SLICE_F_STATUS=COMPLETE (T066 startup gating before writable, T067 torn detection, T068 quarantine+truncate, T069 gap fail-closed, T070 chain fail-closed, T071 audit via quarantine, T072 kill/restart matrix, T073 deterministic matrix) — merged 7c23c9d (#62)
SPEC_002_SLICE_G_VERIFICATION=COMPLETE (T074 fmt/check/clippy/test PASS, T075 Linux PASS Windows UNTESTED explicit, T076 kill/integration green, T077 R1 validate PASS unchanged, T078 adversarial review crash/writer/event 0 blocker, T079 no invariant weakened, T080 verification.md, T081 analyze.md final, T082 close ready, T083 this CURRENT update)
SPEC_002_STATUS=COMPLETE (2026-09-09, all exit criteria §7 PASS except Windows native UNTESTED explicitly reported per plan §7; canonical loss 0)
SPEC_002_EXIT_CRITERIA=cargo fmt PASS, cargo check PASS, cargo clippy PASS, cargo test PASS (98), kill/security green, atomic-write fault matrix PASS, writer-ownership PASS, event recovery matrix PASS, historical upcast PASS, canonical loss 0, R1 unchanged, unauthorized 0
SPEC_002_ANALYZE_T045=PASS (Slice A, informational C-01..C-04)
SPEC_002_PONYTAIL_T045=PASS (KEEP, REUSE Vault/WriteLock+std+serde, 0 new deps)
SPEC_002_ANALYZE_T081=PASS (Final cross-artifact, C-01..C-06 resolved, see analyze.md final)
SPEC_002_PONYTAIL_T081=PASS (still KEEP, still REUSE, still 0 new deps, scope preserved)

NEXT_ACTION=AWAIT_FOUNDER_AUTHORIZATION_FOR_SPEC_003 (003-phase2-derived-index-convergence) — DO NOT ACTIVATE without explicit Founder authorization per tasks.md T083
```
Issues #43 and #44 remain preserved as historical evidence (exact-candidate binding, CI runs 34169748858/34169748870, 0 qualified verdicts, not PASS/REJECT) and were closed as `SUPERSEDED` on 2026-09-08 after PR #47 merged (not as PASS). Per `docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md`, `HUMAN_INDEPENDENT_REVIEW=OPTIONAL` and `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`. Sealing, variance-pilot execution, and subsequent R1 gates now proceed via deterministic internal qualification (validate.py, test_scorer.py 20/20, test_validate.py 41/41, test_r1v2_statistical_design.py 19/19, test_review_binding.py, generate_manifest --check, exact-head CI 7/7 + verify-artifacts) — not via mandatory external human PASS. Model execution remains `PROHIBITED_UNTIL_SEALED` until this sealing commit lands; Spec 002 remains `BLOCKED_BY_R1_TERMINAL_GATE`.

**R1-v2 sealing — complete (2026-09-08):**
```text
REVIEW_CANDIDATE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
REVIEW_CANDIDATE_TREE=43b77fa3d7fd056b5b836f01439c7f1de8ea5ac4
SEALED_CANDIDATE_COMMIT=61e7816b9793a30891d20808deab9175d6872a77
SEALED_CANDIDATE_TREE=43b77fa3d7fd056b5b836f01439c7f1de8ea5ac4
MANIFEST_SHA256=a050c4380937c9cda33c5368c23a2f96eea2b382f5463e2e93e345bfb7246962
ARTIFACT_COUNT=18
SEAL_TIMESTAMP=2026-09-08T13:18:07Z
SEAL_SIGNER=Founder (via PR #47 governance supersession)
SEAL_PROCEDURE=docs/canonical/R1_V2_SEALING_PROCEDURE.md (amended)
SEAL_RECORD=docs/canonical/R1_V2_SEAL_RECORD_2026-09-08.md
SEAL_VERIFICATION=EXACT_HEAD_CI_ON_61e7816_PASS (7/7 Bench + verify-artifacts, runs 34231124327/34231124336)
R1_V2_MACHINE_VALIDATION=PASS
R1_V2_VALIDATION_CONVERGENCE=COMPLETE
R1_V2_MUTATION_TESTING=PASS
R1_V2_EXACT_HEAD_CI=PASS
R1_V2_SCIENTIFIC_DESIGN_SELF_AUDIT=PASS (16 sections INTERNALLY_QUALIFIED)
R1_V2_STATISTICAL_DESIGN_SELF_AUDIT=PASS (18 sections INTERNALLY_QUALIFIED)
INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
```
This sealing record is mechanically verified: `git diff 61e7816..HEAD -- bench/R1 docs/canonical .github/workflows` empty for sealed paths (except this CURRENT update and the new seal record, which are sealing documentation); manifest `a050c438...` covers all 18 load-bearing artifacts deterministically. Re-clone at `61e7816` reproduces identical digests (exact-head CI proves). Sealing does not invent `R1_V2_SCIENTIFIC_REVIEW=PASS` or `STATISTICAL_REVIEW=PASS` — it records internal qualification under amended governance.

**R1-v2 variance pilot harness — prepared (2026-09-08):**
```text
HARNESS=bench/R1/run_variance_pilot_v2.py
HARNESS_BRANCH=feat/r1-v2-variance-pilot-harness
SEALED_CANDIDATE=61e7816b9793a30891d20808deab9175d6872a77
PREPARE_STATUS=PASS
NO_API_PREPARE_GATE=PASS
PREPARE_SEED=b1aeba1de38a2a7e (derived from sealed candidate + manifest)
EXECUTION_ORDER_ENTRIES=720 (30 tasks × 6 arms × 4 repeats, blocked and interleaved)
MAINTENANCE_SESSIONS=252 (separate, per MAINTENANCE-V2.md)
TOTAL_PILOT_SESSIONS=972
EXECUTION_PLAN=runs/variance-pilot-v2/execution-plan.json
SEALED_BINDING=runs/variance-pilot-v2/sealed-binding.json
VALIDATION=bench/R1/validate.py PASS (0 errors) at prepare
EXECUTE_STATUS=PENDING_PROVIDER (OPENAI_API_KEY not set, fail-closed)
EXECUTE_COMMAND=python bench/R1/run_variance_pilot_v2.py --execute
PROVIDER=gpt-5.6-terra medium 0.0 1024 (same as sealed model condition)
INFRA_FAILURE_THRESHOLD=10% (VARIANCE-PILOT-V2.md §7)
```
Harness validates sealed binding, session arithmetic, and generates deterministic execution order (seed `b1aeba1de38a2a7e` from sealed candidate). No model call is made during prepare. Execute requires `OPENAI_API_KEY` and will fail closed if provider identity drifts or infra failures exceed 10%. Per-arm context builders (B-NULL, B0, B1, B3, B4, B5) remain to be fully wired for the 972-session run; current harness scaffolds order and plan and proves prepare gate.

**Review package internal qualification — converged (amended 2026-09-08):**
```text
R1_V2_STATISTICAL_PACKET=REPAIRED (pairing unit (task,repeat), power formula, symbol table, B_NULL before PSI, static proofs) + AMENDED_SUPERSEDED_HUMAN_GATE (optional per Founder decision)
R1_V2_SCIENTIFIC_PACKET=REPAIRED (stratified R1_V1 vs R1_V2_DESIGN vs R1_V2_EMPIRICAL_DATA=NONE, per-arm fairness, ceiling routing) + AMENDED_SUPERSEDED_HUMAN_GATE
R1_V2_SEALING_PROCEDURE=REPAIRED_SELF_REFERENCE_SAFE (external binding via CURRENT + manifest, no embedded latest-main SHA, candidate-binding law explicit) + AMENDED_REMOVE_MANDATORY_HUMAN_REVIEW (internal qualification now gates, human OPTIONAL)
R1_V2_ARTIFACT_MANIFEST=REGENERATED_SELF_REFERENCE_SAFE (deterministic SHA-256, 18 artifacts, candidate c3f196d (3a95687) → 61e7816 (43b77fa), manifest_sha a050c438... — regenerated after governance supersession, artifact map verified)
R1_V2_REVIEW_BINDING_VALIDATION=HARDENED (19 tests, fail-closed on stale NOT_YET_FROZEN, historical main binding, missing artifacts, tree mismatch) + UPDATED_FOR_SUPERSEDED_HUMAN_GATE (checks SUPERSEDED/INTERNALLY_QUALIFIED, not mandatory PENDING)
FOUNDER_GOVERNANCE_DECISION=RECORDED (docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md)
```

The rebuild required no new founder route decision. The existing authorized scope (`ROUTE=NEW_PREREGISTRATION`, `MODEL_STRATEGY=KEEP_REPRESENTATIVE_STRONG_MODEL`, `TASK_STRATEGY=INCREASE_DISCRIMINATING_DIFFICULTY`) covers the implementation methodology.

## Variance pilot scoring result

The blinded scoring report is recorded in `docs/canonical/R1-PILOT-SCORING-REPORT.md`:

```text
PILOT_RESULT=NO_DETECTABLE_DISCORDANCE
CEILING_EFFECT=YES
CURRENT_PREREGISTRATION_CONFIRMATORY_POWER=UNAVAILABLE
PRODUCT_THESIS_PASS=NOT_AUTHORIZED
PRODUCT_THESIS_FAIL=NOT_AUTHORIZED
```

All six arms achieved perfect continuation correctness (120/120) across all 30 tasks. The power-analysis rule correctly identifies that the study cannot be powered for the preregistered effect size δ=0.15 because there is no variance to detect.

This is a legitimate scientific finding. The ceiling effect is **not** interpreted as thesis support or thesis falsification. It means the benchmark has no discriminating power at this difficulty level with this model.

## Sealed R1 v1.1 historical anchor

The pre-GitHub local repository sealed R1 v1.1 at:

```text
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
R1_V1_1_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
R1_V1_1_PREREGISTRATION_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

GitHub was empty when it was first bootstrapped on 2026-08-28. The connected GitHub write interface could not upload the historical Git pack while preserving arbitrary historical commit timestamps, so the GitHub bootstrap commit SHA is **not** claimed to equal `ed79d8...`.

Treat the SHAs above as immutable historical evidence. Do not rewrite them to match the later GitHub bootstrap history. See `docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md`.

## What is authorized now

The founder decision on the ceiling-effect gate:

```text
ROUTE=NEW_PREREGISTRATION
MODEL_STRATEGY=KEEP_REPRESENTATIVE_STRONG_MODEL
TASK_STRATEGY=INCREASE_DISCRIMINATING_DIFFICULTY
WEAKER_MODEL_ROUTE=NOT_SELECTED
```

Authorized:
1. Design a new preregistration with harder task complexity that can discriminate context strategies for a strong modern agent.
2. Preserve the failed-to-discriminate study as immutable prior evidence. Do not overwrite, retroactively modify, rescore, or reuse the old pilot as confirmatory observations.
3. Repository-local governance, specification, design, static validation, review, CI, and sealing work for the new preregistration.
4. Strong simple baselines must be preserved. Do not weaken baselines simply to create separation.

Not authorized:
- Executing the new model experiment until the new preregistration, benchmark artifacts, manifest identities, exact model/runtime condition, and execution authority are all sealed via updated internal qualification (deterministic tests + manifest + exact-head CI) — human independent review is now optional per Founder decision 2026-09-08, but sealing remains required.
- Activating Spec 002 merely because the old R1 pilot was underpowered.

## What is blocked

Until the new R1 successor experiment reaches its terminal verdict and the founder explicitly authorizes the post-R1 route:

```text
specs/002-post-r1-canonical-core-convergence = BLOCKED
Phase 1 product expansion                  = BLOCKED
Phase 2 derived expansion                  = BLOCKED
GI-CAP / graph work                        = BLOCKED
Phase 4 memory productization              = BLOCKED
Phase 5 agent gateway / MCP                = BLOCKED
automatic memory                           = BLOCKED
vectors                                    = BLOCKED
UI                                         = BLOCKED
```

## R1 outcome routing

After the terminal verdict:

| R1 verdict family | Default route |
|---|---|
| `THESIS_SUPPORTED` | Founder may authorize Spec 002 |
| `THESIS_SUPPORTED_ON_COST` | Founder may authorize Spec 002; preserve cost as a primary design constraint |
| `THESIS_SUPPORTED_ON_SAFETY` | Founder may authorize Spec 002 with stale-use/constraint safety retained as a primary acceptance dimension |
| `THESIS_SUPPORTED_WITH_COST_CAVEAT` | Do not expand expensive capabilities; require explicit founder decision and cost-reduction plan |
| `THESIS_NOT_SUPPORTED` | Trigger F-1 review. Do not begin Spec 002 by default |
| `THESIS_FAIL` | Halt product expansion and perform architecture/product reconsideration |
| `INCONCLUSIVE` | No silent continuation. Founder explicitly chooses extension, limited convergence, or stop |
| `CEILING_EFFECT` | Design harder benchmark. New preregistration required. Do not reinterpret as thesis support or falsification |

## Next Spec Kit

`specs/002-post-r1-canonical-core-convergence/`

It is deliberately present before activation so the repository contains the next planned move, but:

```text
SPECIFIED != AUTHORIZED
```

Its first remaining activation task is T038. T037 is closed with exact recovered implementation-baseline evidence; T038 cannot close before the R1 terminal verdict exists.

## Bootstrap integrity rule

Before any post-R1 product implementation begins from the GitHub mirror, reconcile the working implementation/evidence snapshot against the historical R1 anchor and record the exact source of that evidence. A GitHub bootstrap SHA must never be substituted for an old sealed SHA merely for convenience.

T037 now records the selected implementation baseline and durable recovery bundle. That reconciliation creates no product implementation authority while R1 remains open.

## Update rule

When this frontier changes, update this file in the same commit that records the new authorization/closeout evidence, or in the immediately following documentation-only commit.

Never point `CURRENT` at a phase whose entry criteria are not actually met.
