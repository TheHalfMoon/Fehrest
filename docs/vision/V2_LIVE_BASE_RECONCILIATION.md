# V2 Live Base Reconciliation

**Status:** DRAFT / NON-AUTHORIZING  
**Recorded:** 2026-08-28  
**Updated:** 2026-08-29  
**Proposal:** Fehrest V2  
**Canonical execution frontier:** R1

This record updates the V2 proposal's evidence assumptions after the historical governance and implementation reconciliation work merged to operational `main`.

## Live evidence now available

The following historical identities have been independently recovered and reproduced exactly:

```text
HISTORICAL_BASE_HEAD=685b390d93fd58c65b8d9e33f4869c6c986259d3
HISTORICAL_BASE_TREE=bdc9bed15505692f4a56084949116c4a9f62eafe
R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
R1_V1_1_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
R1_V1_1_PREREGISTRATION_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

The historical Architecture Freeze / Constitution source set has also been recovered and conservatively reconciled against the operational bootstrap governance. The historical sealed implementation tree and R1 verifier have been independently reproduced and verified.

Therefore the original V2 PR statement that historical implementation/governance provenance had not yet been reconciled is now stale.

## Updated gate state

```text
G-CONST=RECONCILED_CONSERVATIVELY
G-PROV=HISTORICAL_SOURCE_AND_SEAL_RECOVERED
G-PROV-GITHUB-ORIGINAL-HISTORY=NOT_YET_PUBLISHED
G-R1=OPEN
G-V2=NOT_CANONICALIZED
```

This does **not** authorize V2 implementation.

The blocking execution chain remains:

```text
valid replacement R1 variance pilot
→ raw evidence seal
→ execution review
→ blinded scoring when authorized
→ power analysis
→ confirmatory N
→ confirmatory manifest seal
→ confirmatory execution
→ raw seal
→ blinded scoring
→ scoring seal
→ unblind
→ terminal verdict
→ founder post-R1 route decision
```

## 2026-08-29 live-base checkpoint

The proposal branch was merge-forwarded from the then-current proposal head to canonical `main` after PR #16 authorized V11 as SDK-verification plumbing only. No rebase, force update, or destructive history rewrite was used.

```text
CANONICAL_MAIN=ca0bfa61de6cf92e5e6758731126e8274404de67
CANONICAL_MAIN_TREE=c97ae0eb53be97c35c62ba7c6c956c9e95f01f1e
PRE_MERGE_PROPOSAL_HEAD=0f200ad999a37805708d4ad18052cae6298effac
MERGE_FORWARD_COMMIT=34a95950704a83db34f25a4e3570aaaa787db58f
MERGE_FORWARD_FIRST_PARENT=0f200ad999a37805708d4ad18052cae6298effac
MERGE_FORWARD_SECOND_PARENT=ca0bfa61de6cf92e5e6758731126e8274404de67
BEHIND_CANONICAL_MAIN_AFTER_MERGE_FORWARD=0
FORCE_PUSH_USED=NO
REBASE_USED=NO
DESTRUCTIVE_HISTORY_REWRITE_USED=NO
```

The merge-forward adopted the following canonical R1 authority files byte-identically from `main`:

```text
specs/CURRENT.md
docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK.md
docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK_V11.md
docs/canonical/R1_V11_RUNTIME_COMPATIBILITY.md
```

Canonical R1 state now records:

```text
R1_REPLACEMENT_EXECUTOR_VERSION=11
R1_REPLACEMENT_EXECUTOR_SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
R1_REPLACEMENT_V8_PREPARE_RESULT=FAIL_CLOSED_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V9_PREPARE_RESULT=PASS
R1_REPLACEMENT_V9_RUNTIME_RESULT=FAIL_CLOSED_DURING_ISOLATED_RUNTIME_BOOTSTRAP_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V10_PREPARE_RESULT=PASS
R1_REPLACEMENT_V10_RUNTIME_RESULT=UV_VENV_AND_OPENAI_3_3_0_INSTALL_PASS
R1_REPLACEMENT_V10_VERIFY_RESULT=FAIL_CLOSED_PYTHON_C_ARGUMENT_QUOTING_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V11_QUALIFICATION=RUNTIME_LOCAL_SDK_VERIFY_SCRIPT_ONLY
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
```

V10 proved the uv-managed isolated runtime and pinned `openai==3.3.0` installation, then failed closed because PowerShell split the Python `-c` verification payload so Python received bare `import`. V11 preserves the V10/V9 supervisor byte-for-byte and changes only SDK verification plumbing by executing a runtime-local UTF-8-without-BOM `verify-openai-sdk.py` instead of Python `-c`.

No V11 scientific execution result or raw seal is present in canonical repository truth. These compatibility facts do not close R1, authorize scoring, or change the V2 proposal's authority state.

After this merge-forward, the intended proposal diff against canonical `main` remains limited to the 19 V2 proposal/research/review files under `docs/**`; canonical `docs/canonical/**`, `specs/CURRENT.md`, Spec 002, and product code are inherited from `main` and are not proposal changes.

## V2 proposal disposition

The proposal remains useful as future Class E product direction, but it must remain:

```text
DRAFT=YES
CANONICAL=NO
IMPLEMENTATION_AUTHORIZED=NO
CURRENT_CHANGED=NO
SPEC_002_ACTIVATED=NO
```

Any future canonical adoption must use the actual R1 terminal verdict and the recovered frozen architecture as inputs. It may not rely on the older assumption that those historical sources were unavailable.

## No semantic widening

This reconciliation does not change:

- the V2 product vision;
- the proposed Rust-first semantic ownership model;
- the one-active-spec rule;
- the requirement that graph/vector/AI remain behind evidence and authorization gates;
- the prohibition on using derived state as authority;
- the R1 experiment semantics.

It only refreshes the proposal's provenance assumptions to match live repository truth.
