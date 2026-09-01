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

Current publication state (updated 2026-09-01 after live verification):

```text
HISTORICAL_SOURCE_AND_SEAL_RECOVERED=YES
HISTORICAL_GIT_BUNDLE_VERIFIED=YES
HISTORICAL_OBJECT_GRAPH_REACHABLE_ON_GITHUB=YES
SEALED_R1_COMMIT_REACHABLE_ON_GITHUB=YES
SEALED_R1_TREE_REACHABLE_ON_GITHUB=YES
GITHUB_ORIGINAL_HISTORICAL_OBJECT_GRAPH_PUBLISHED=YES
```

Issue #1 is closed with verified evidence (see below). Closing that issue required the existing original Git objects to become reachable on GitHub with their historical identities unchanged; no equivalent substitute commit was created.

The publication gate is separate from the active R1 experiment gate owned by Issue #8. Publishing historical Git objects does not create an R1 execution result, authorize scoring, or activate Spec 002.

## Transport qualification evidence — 2026-08-29

Two repository-native transport paths were exercised and preserved as negative evidence without mutating canonical `main` or the sealed R1 experiment.

### GitHub-hosted runner probe

A temporary branch from canonical `main` tested fresh `windows-latest` and `ubuntu-latest` jobs rather than relying only on the earlier historical workflow.

```text
PROBE_BRANCH=ops/runner-probe-20260829
PROBE_TRIGGER_HEAD=ea32166bde9c75086f7ce61746a27730e455c0e2
PROBE_RUN_ID=33250476412
WINDOWS_JOB_ID=99095174621
WINDOWS_EXECUTABLE_STEPS=0
UBUNTU_JOB_ID=99095174732
UBUNTU_EXECUTABLE_STEPS=0
JOB_LOG_BLOBS_CREATED=NO
PROBE_CLOSEOUT_HEAD=a224092c837695877f75b36181446ee5961fc69f
PROBE_CLOSEOUT_WORKFLOW_PRESENT=NO
CANONICAL_MAIN_MUTATED_BY_PROBE=NO
```

Both jobs failed before any executable step was reported and no job log blob was created. This evidence proved that GitHub-hosted runner transport was unavailable for this repository at the time of the probe. It did **not** prove a specific account-side root cause such as billing, policy, or capacity, because the available connected interface did not expose a qualifying diagnostic beyond the pre-step failure state.

### Runner availability re-probe — 2026-09-01

The same probe workflow was re-run against the original probe head:

```text
RE_PROBE_RUN_ID=33250476412
RE_PROBE_DATE=2026-09-01
WINDOWS_JOB=success
UBUNTU_JOB=success
GITHUB_HOSTED_RUNNERS_AVAILABLE=PASS
```

Both jobs completed successfully. Runner availability is therefore a live, changing platform condition — the 2026-08-29 negative result was preserved as evidence and is now superseded by this positive result. A repository-native `verify-artifacts` CI workflow was added to canonical `main` to enforce artifact identity on every push/PR (`.github/workflows/verify-artifacts.yml`).

### Git Data text-transfer probe

The connected Git Data API can create Git blobs, but model-mediated transfer was tested against a known historical governance blob and failed byte identity.

```text
HISTORICAL_PATH=.specify/memory/constitution.md
EXPECTED_HISTORICAL_BLOB_SHA=eb427abed358fefb2a12890748e5c9ececa68c0b
CONNECTOR_CREATED_BLOB_SHA=fc643fde784d7606ba0a2cade6deca43fd6d0f62
BLOB_SHA_MATCH=NO
HISTORICAL_TEXT=Neither substitutes for the other.
TRANSFERRED_TEXT=Neether substitutes for the other.
MISMATCHED_BLOB_REFERENCED_BY_TREE_OR_REF=NO
CANONICAL_MAIN_MUTATED_BY_PROBE=NO
```

The recovered Git bundle independently verifies the expected historical blob SHA and historical text. Because the connector-created blob differed, no remaining historical blobs were transferred by that method and the mismatched object was never attached to a tree, commit, branch, tag, or canonical path.

Therefore repository-native text reconstruction is disqualified as a provenance publication mechanism. The historical gate still requires transport of the existing Git objects themselves, preserving the original commit, tree and blob identities. The prepared normal non-force publication package remains the safe path when an execution environment with direct authenticated Git network access is available.

## Publication evidence — 2026-09-01

The historical object graph was published with the repository-owned fail-closed publisher `scripts/recovery/publish-historical-objects.ps1` (tooling mirrored in #19, output-indexing repair in #20). The publisher verified the exact bundle SHA-256, cloned it into a disposable area, ran `git fsck --full --strict`, verified the sealed commit/tree, then performed a normal non-force push and re-read the remote ref.

```text
PUBLICATION_DATE=2026-09-01
BUNDLE_SHA256=a36639da9731cd4778777e14b980ca04784f9a00890a57d0a3fc10591f54f5f9
DESTINATION_REF=refs/heads/historical/r1-v1.1
REMOTE_REF_SHA=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
TREE_ENTRY_COUNT=171
HISTORICAL_PARENT=685b390d93fd58c65b8d9e33f4869c6c986259d3
HISTORICAL_AUTHOR_COMMITTER=Abdulaziz <alshehriofficial@gmail.com> @ 2026-08-19T15:02:32Z
FORCE_PUSH_USED=NO
REBASE_USED=NO
DESTRUCTIVE_HISTORY_REWRITE_USED=NO
OPERATIONAL_MAIN_MUTATED=NO
```

Independent GitHub API re-verification after publication:

```text
REF_TYPE=commit
TREE_REACHABLE=YES (f7ea7e0... resolved via /git/trees with recursive=1)
PREREGISTRATION_FILESET_DIGEST_RECHECK=PASS
  method=sha256 over sorted "{sha256(blob_content)}  rel\n" manifest of the 8
  benchmark files (bench/R1/seal_digest.py rule), blobs fetched from GitHub API
  result=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
  match_with_sealed_anchor=YES
```

Repository completeness (artifact mirroring) evidence: `artifacts/ARTIFACT-MANIFEST.md`; the V11 executor, evidence collector and historical bundle are reconstructible byte-for-byte from GitHub-only bytes (`scripts/recovery/verify-artifacts.ps1` → PASS on a fresh clone of merged `main`; issues #18 closed via PR #19/#20).

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
GITHUB_ORIGINAL_HISTORICAL_OBJECT_GRAPH_PUBLISHED=YES
HISTORICAL_REF=refs/heads/historical/r1-v1.1 (=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c)
ISSUE_1=CLOSED_WITH_VERIFIED_EVIDENCE
ISSUE_18=CLOSED_WITH_VERIFIED_EVIDENCE
REPOSITORY_ARTIFACT_SELF_CONTAINMENT=YES
SPEC_002_T037=CLOSED
ACTIVE_EXECUTION_FRONTIER=R1
ACTIVE_R1_SUBGATE=REPLACEMENT_VARIANCE_PILOT_EXECUTION
POST_R1_PRODUCT_IMPLEMENTATION=BLOCKED
```

Publication of the historical object graph does not create an R1 execution result and does not authorize scoring, unblinding, power analysis, confirmatory execution, or Spec 002 activation.

When the original historical object graph is eventually published, update this record from live GitHub verification. Do not infer publication from bundle existence alone.
