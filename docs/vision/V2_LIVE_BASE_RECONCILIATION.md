# V2 Live Base Reconciliation

**Status:** DRAFT / NON-AUTHORIZING  
**Recorded:** 2026-08-28  
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

The proposal branch was merge-forwarded again after canonical provenance transport qualification merged through PR #13.

```text
CANONICAL_MAIN=8f364c10244b4dce6f8b3d027184e7b4c10107b9
CANONICAL_MAIN_TREE=a3a18360b62ef19cc0134a70476d1a2f221b4c73
PRE_MERGE_PROPOSAL_HEAD=18a48fc03afd3c906c3ef0606f6a75411967a1c1
MERGE_FORWARD_COMMIT=8c9c3078b686b5ea430b5d8cc0c58f3ff1a82ae2
MERGE_FORWARD_FIRST_PARENT=18a48fc03afd3c906c3ef0606f6a75411967a1c1
MERGE_FORWARD_SECOND_PARENT=8f364c10244b4dce6f8b3d027184e7b4c10107b9
BEHIND_CANONICAL_MAIN_AFTER_MERGE_FORWARD=0
FORCE_PUSH_USED=NO
REBASE_USED=NO
DESTRUCTIVE_HISTORY_REWRITE_USED=NO
```

Before the merge-forward, the only path present on canonical `main` and absent from the proposal branch was the PR #13 update to `docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md`. The merge-forward adopted that canonical blob without editing it.

After the merge-forward, the proposal diff against canonical `main` contains only the 19 V2 proposal/research/review files under `docs/**`; it contains no `docs/canonical/**`, `specs/CURRENT.md`, Spec 002, R1 runbook, or product-code diff.

Canonical provenance now records that both fresh hosted-runner transport and model-mediated Git Data text reconstruction were fail-closed / unsuitable for exact historical object publication. This strengthens provenance evidence only. It does not close historical publication Issue #1, does not create an R1 result, and does not change the V2 proposal's authority state.

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
