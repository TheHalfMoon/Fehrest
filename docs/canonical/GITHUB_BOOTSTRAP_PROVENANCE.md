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

The commit object `ed79d8...` was independently reproduced byte-for-byte from the recovered local tree, parent, author/committer identity, timestamp and message. The recovered tree matched `f7ea7e0...` exactly.

## Recovered historical Git bundle

The recovered historical source and sealed R1 history are preserved in a complete self-contained Git bundle:

```text
BUNDLE_FILENAME=Fehrest-historical-r1-v1.1-ed79.bundle
BUNDLE_SIZE_BYTES=823833
BUNDLE_SHA256=a36639da9731cd4778777e14b980ca04784f9a00890a57d0a3fc10591f54f5f9
ADVERTISED_REF=refs/heads/recovered/r1-v1.1
SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
GIT_BUNDLE_VERIFY=PASS
COMPLETE_HISTORY=YES
```

A fresh materialization from this bundle reproduces the sealed commit/tree with a clean worktree. This recovery evidence closed Spec 002 T037's implementation-baseline reconciliation requirement, but it did **not** publish the original object graph to GitHub and did **not** create product implementation authority.

## Original-history publication state

The operational GitHub snapshot mirror and the recovered historical bundle are distinct facts.

Current publication state:

```text
HISTORICAL_SOURCE_AND_SEAL_RECOVERED=YES
HISTORICAL_GIT_BUNDLE_VERIFIED=YES
HISTORICAL_OBJECT_GRAPH_REACHABLE_ON_GITHUB=NO
SEALED_R1_COMMIT_REACHABLE_ON_GITHUB=NO
SEALED_R1_TREE_REACHABLE_ON_GITHUB=NO
GITHUB_ORIGINAL_HISTORICAL_OBJECT_GRAPH_PUBLISHED=NO
```

Issue #1 tracks this remaining provenance-transport obligation. Closing that issue requires the existing original Git objects to become reachable on GitHub with their historical identities unchanged. An equivalent newly created commit is not a substitute.

The publication gate is separate from the active R1 experiment gate owned by Issue #8. Publishing historical Git objects does not create an R1 execution result, authorize scoring, or activate Spec 002.

## Integrity rule

Never:

```text
replace the historical sealed SHA with a GitHub bootstrap SHA
claim the bootstrap root is the original local history
rewrite R1 evidence to fit the new remote history
recreate historical commits with different identities and call them equivalent
force-push or destructively rewrite operational history to make provenance look linear
use remote-history convenience to weaken benchmark provenance
```

The historical SHAs above remain immutable evidence identifiers.

## Operational rule from bootstrap forward

GitHub `main` is the canonical **operational remote** for planning and future work from the bootstrap forward. Any pre-bootstrap implementation/evidence used for a gate must be reconciled explicitly against its historical anchor before authorization is advanced.

T037 has completed that implementation-baseline reconciliation for Spec 002. Later activation tasks remain governed by the R1 terminal verdict and explicit founder authorization; historical recovery by itself is not authorization.

Read in this order:

1. `AGENTS.md`
2. `specs/CURRENT.md`
3. `docs/canonical/EXECUTION_MASTER_PLAN.md`
4. the active or next Spec Kit named by `specs/CURRENT.md`

## Current effect

```text
GITHUB_BOOTSTRAP_HISTORY=TRANSPARENT_MIRROR_HISTORY
PRE_BOOTSTRAP_R1_SHAS=PRESERVED_AS_HISTORICAL_EVIDENCE
HISTORICAL_SOURCE_RECOVERY=COMPLETE
HISTORICAL_GIT_BUNDLE=COMPLETE_AND_VERIFIED
GITHUB_ORIGINAL_HISTORICAL_OBJECT_GRAPH_PUBLISHED=NO
SPEC_002_T037=CLOSED
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
POST_R1_PRODUCT_IMPLEMENTATION=BLOCKED
```

When the original historical object graph is eventually published, update this record from live GitHub verification. Do not infer publication from bundle existence alone.