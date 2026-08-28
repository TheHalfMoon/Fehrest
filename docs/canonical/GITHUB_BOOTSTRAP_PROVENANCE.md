# GitHub Bootstrap Provenance

**Bootstrap date:** 2026-08-28  
**Remote:** `TheHalfMoon/Fehrest`

## Why this record exists

The GitHub repository was empty when the execution plan was installed. The Fehrest implementation and sealed R1 evidence already existed in a local Git repository. The connected GitHub write interface available during bootstrap could create files/commits but could not upload a raw Git pack while preserving arbitrary historical author/committer timestamps.

Therefore the first GitHub commit is a **bootstrap/mirror history**. It is not claimed to be the historical local sealed commit.

## Pre-bootstrap sealed local anchor

```text
LOCAL_R1_V1_1_SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
LOCAL_R1_V1_1_SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
LOCAL_R1_V1_1_PARENT=685b390d93fd58c65b8d9e33f4869c6c986259d3
R1_V1_1_PREREGISTRATION_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

Before bootstrap, the commit object `ed79d8...` was independently reproduced byte-for-byte from the recovered local tree, parent, author/committer identity, timestamp and message. The recovered tree matched `f7ea7e0...` exactly.

## Integrity rule

Never:

```text
replace the historical sealed SHA with a GitHub bootstrap SHA
claim the bootstrap root is the original local history
rewrite R1 evidence to fit the new remote history
use remote-history convenience to weaken benchmark provenance
```

The historical SHAs above remain evidence identifiers.

## Operational rule from bootstrap forward

GitHub `main` becomes the canonical **operational remote** for planning and future work from the bootstrap forward. Any pre-bootstrap implementation/evidence used for a future gate must be reconciled explicitly against its historical anchor before authorization is advanced.

Read in this order:

1. `AGENTS.md`
2. `specs/CURRENT.md`
3. `docs/canonical/EXECUTION_MASTER_PLAN.md`
4. the active Spec Kit

## Current effect

```text
GITHUB_BOOTSTRAP_HISTORY=TRANSPARENT_MIRROR_HISTORY
PRE_BOOTSTRAP_R1_SHAS=PRESERVED_AS_HISTORICAL_EVIDENCE
ACTIVE_EXECUTION_FRONTIER=R1
POST_R1_PRODUCT_IMPLEMENTATION=BLOCKED
```
