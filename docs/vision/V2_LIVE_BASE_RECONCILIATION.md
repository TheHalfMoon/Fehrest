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