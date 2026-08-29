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
→ confirmatory execution path
→ scoring seal
→ unblind
→ terminal verdict
→ founder post-R1 route decision
```

## 2026-08-29 live-base checkpoint

The proposal branch was merge-forwarded after canonical PR #14 authorized the BOM-compatible V9 replacement executor as a parser-only repair of the fail-closed V8 prepare attempt.

```text
CANONICAL_MAIN=d980af8303e038df62f974eec898bc1123f83c77
CANONICAL_MAIN_TREE=6b12dd20d38b48710f9f44de98e4b2bf3f5790de
PRE_MERGE_PROPOSAL_HEAD=a692cb0baf27f4f301d31d86ff6785c158464e8b
MERGE_FORWARD_COMMIT=e80dce50b6fc00c9eff6de90026e48fac981a1bf
MERGE_FORWARD_FIRST_PARENT=a692cb0baf27f4f301d31d86ff6785c158464e8b
MERGE_FORWARD_SECOND_PARENT=d980af8303e038df62f974eec898bc1123f83c77
BEHIND_CANONICAL_MAIN_AFTER_MERGE_FORWARD=0
FORCE_PUSH_USED=NO
REBASE_USED=NO
DESTRUCTIVE_HISTORY_REWRITE_USED=NO
```

The merge-forward adopted canonical `specs/CURRENT.md` and `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK.md` exactly from `main`. The proposal branch does not alter those files relative to canonical main.

Canonical R1 state now records:

```text
R1_REPLACEMENT_EXECUTOR_VERSION=9
R1_REPLACEMENT_EXECUTOR_SHA256=48da655c6e30da77a1073ffa149a360929a407d25ecbb8fb01d4c8a26429ef2a
R1_REPLACEMENT_V8_PREPARE_RESULT=FAIL_CLOSED_BEFORE_MODEL_CALLS
R1_REPLACEMENT_V9_QUALIFICATION=BOM_METADATA_READ_COMPATIBILITY_ONLY
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
```

V8's BOM decode failure occurred before credential capture and before any model call. V9 changes only BOM-compatible reads of pre-existing arming/JSONL metadata while preserving byte hashing and every sealed scientific binding. This does not create an R1 result, does not authorize scoring, and does not change the V2 proposal's authority state.

After this merge-forward, the proposal diff against canonical `main` remains limited to the 19 V2 proposal/research/review files under `docs/**`; it contains no canonical `docs/canonical/**`, `specs/CURRENT.md`, Spec 002, R1 runbook, or product-code diff.

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
