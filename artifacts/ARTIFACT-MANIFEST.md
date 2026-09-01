# Fehrest Repository Artifact Manifest

**Status:** REPOSITORY-OWNED ARTIFACT AUTHORITY RECORD
**Scope:** artifact mirroring/provenance hardening only. This manifest changes no R1 scientific semantics, no sealed experiment input, no scoring authorization, no unblinding authorization, and no Spec 002 activation state.

```text
R1_V1_1_SEMANTIC_MUTATION=NO
SEALED_COMMIT_CHANGE=NO
SEALED_TREE_CHANGE=NO
PREREGISTRATION_CHANGE=NO
MODEL_CHANGE=NO
SEED_CHANGE=NO
ARM_CHANGE=NO
CORPUS_OR_TASK_CHANGE=NO
SCORING_CHANGE=NO
SCORING_AUTHORIZED=NO
UNBLINDING_AUTHORIZED=NO
POWER_ANALYSIS_AUTHORIZED=NO
CONFIRMATORY_AUTHORIZED=NO
SPEC_002_ACTIVATED=NO
```

## Storage method

All load-bearing binaries are stored as single byte-exact Git blobs (no chunking was required; the connected Git transport accepted whole binaries directly). Every path below is excluded from line-ending conversion by `.gitattributes` (`artifacts/** -text`, `scripts/recovery/** -text`), so a fresh checkout from GitHub reproduces the exact canonical bytes.

## Load-bearing artifacts

### 1. Active R1 executor package (V11)

```text
FILENAME=FEHREST-R1-X1-REPLACEMENT-V11.zip
ROLE=ACTIVE_R1_EXECUTOR_PACKAGE
REPOSITORY_PATH=artifacts/r1/v11/FEHREST-R1-X1-REPLACEMENT-V11.zip
SIZE_BYTES=10257
SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
GIT_BLOB_SHA1=c64f2ea918f0d431533bad30c792a51eca98bb1e
CONTENTS=RUN_THIS_NOW.cmd,replacement.ps1,supervisor.py
SEALED_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
SOURCE_PROVENANCE=Canonical V11 authority per docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK_V11.md and docs/canonical/R1_V11_RUNTIME_COMPATIBILITY.md
AUTHORITY_STATUS=CANONICAL_ACTIVE_R1_EXECUTOR_IDENTITY
```

Browseable mirrors (byte-exact extracts of the package members):

```text
artifacts/r1/v11/browseable/RUN_THIS_NOW.cmd      size=1194  blob=49b52a89367d18d6d9334fcafaa64a3ab303648f
artifacts/r1/v11/browseable/replacement.ps1       size=10925 blob=3034959f91be14a4deda996435032ec80d049d0f
artifacts/r1/v11/browseable/supervisor.py         size=20042 blob=67fa65c71c8e509b6f16b3426cda29c71b5b7f9f sha256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
```

### 2. Repository-owned evidence collector (V3)

```text
FILENAME=FEHREST-R1-X1-REPLACEMENT-EVIDENCE-COLLECTOR-V3.zip
ROLE=REPOSITORY_OWNED_EVIDENCE_COLLECTOR_PACKAGE
REPOSITORY_PATH=artifacts/r1/evidence-collector/FEHREST-R1-X1-REPLACEMENT-EVIDENCE-COLLECTOR-V3.zip
SIZE_BYTES=5247
SHA256=eb2207e9f155c29789d75ef708c1aaa81b2a21d61303b0660fb820ea18646bbb
GIT_BLOB_SHA1=f30e37a2644e04eed0a52b48aa4c635845193b9a
CONTENTS=COLLECT_EVIDENCE_NOW.cmd,collect-r1-evidence.ps1,README.txt
SOURCE_PROVENANCE=Canonical evidence-collector identity for post-execution evidence collection
AUTHORITY_STATUS=CANONICAL_EVIDENCE_COLLECTOR_IDENTITY
```

Browseable mirrors:

```text
artifacts/r1/evidence-collector/browseable/COLLECT_EVIDENCE_NOW.cmd   size=290   blob=fadb994d37df7236d4c57841779bfefea75a4b6f
artifacts/r1/evidence-collector/browseable/collect-r1-evidence.ps1    size=14313 blob=9dad6c91288390db9f0e6ea7e2a4c3232c1b103b
artifacts/r1/evidence-collector/browseable/README.txt                 size=1110  blob=4783a7fc26bc47eea3a1083c7ee7b82260708273
```

### 3. Historical Git object authority bundle

```text
FILENAME=Fehrest-historical-r1-v1.1-ed79.bundle
ROLE=HISTORICAL_GIT_OBJECT_AUTHORITY_BUNDLE
REPOSITORY_PATH=artifacts/recovery/historical-r1-v1.1/Fehrest-historical-r1-v1.1-ed79.bundle
SIZE_BYTES=823833
SHA256=a36639da9731cd4778777e14b980ca04784f9a00890a57d0a3fc10591f54f5f9
GIT_BLOB_SHA1=fba4aa77a6e4a87a9a23a73962cc5ef0b308855c
ADVERTISED_REF=refs/heads/recovered/r1-v1.1
SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
SOURCE_PROVENANCE=Complete self-contained Git bundle recovered from the pre-bootstrap local repository; the load-bearing historical object authority per docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md
AUTHORITY_STATUS=CANONICAL_HISTORICAL_OBJECT_AUTHORITY
```

### 4. Publication tooling

```text
FILENAME=publish-historical-objects.ps1
ROLE=HISTORICAL_BUNDLE_PUBLISHER_TOOL
REPOSITORY_PATH=scripts/recovery/publish-historical-objects.ps1
GIT_BLOB_SHA1=c1f3edac481a8b3fab7c54cb77f117e12ae0595f
RUNTIME_REQUIREMENT=PowerShell 7+ (pwsh). Under Windows PowerShell 5.1 the EAP=Stop + native-stderr + 2>&1 combination turns harmless git progress lines (e.g. "Cloning into ...") into a terminating NativeCommandError and halts the publisher.
LAYOUT_REQUIREMENT=The publisher resolves the bundle next to itself (ScriptRoot). Before running from a repo checkout, place the bundle alongside it, e.g. copy artifacts/recovery/historical-r1-v1.1/Fehrest-historical-r1-v1.1-ed79.bundle next to scripts/recovery/publish-historical-objects.ps1, or run from any temp directory holding both files.
SOURCE_PROVENANCE=Repository-native fail-closed publisher: verifies bundle SHA-256, clones to a disposable bare work area, runs git fsck --full --strict, verifies SEALED_COMMIT/SEALED_TREE, then performs a normal non-force push of refs/heads/recovered/r1-v1.1 to refs/heads/historical/r1-v1.1 and re-reads the remote ref
AUTHORITY_STATUS=REPOSITORY_OWNED_PUBLICATION_TOOLING
```

```text
FILENAME=verify-artifacts.ps1
ROLE=ARTIFACT_IDENTITY_VERIFIER_TOOL
REPOSITORY_PATH=scripts/recovery/verify-artifacts.ps1
SOURCE_PROVENANCE=Repository-native fail-closed verifier for every identity in this manifest
AUTHORITY_STATUS=REPOSITORY_OWNED_VERIFICATION_TOOLING
```

## Ordered parts

```text
ORDERED_PARTS_USED=NO
REASON=Direct whole-binary Git transport succeeded; no chunked reconstruction path is required.
```

## Reconstruction procedure

From a fresh clone of this repository (GitHub-only bytes):

1. `git clone https://github.com/TheHalfMoon/Fehrest.git`
2. All authority bytes are already present at the paths above; no assembly step is needed.
3. Optionally extract each ZIP with any standard extractor to obtain its member scripts.

## Verification procedure

From a fresh checkout of the repository root:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/recovery/verify-artifacts.ps1
```

The verifier fails closed unless, for every path above, the exact size, SHA-256 (where recorded), and Git blob identity match this manifest, and the `supervisor.py` member inside the V11 zip is byte-identical to the sealed supervisor identity. A successful run prints `FEHREST_ARTIFACT_VERIFICATION_STATUS=PASS`.

For the historical bundle, before any publication attempt (requires PowerShell 7+):

```text
# stage the bundle next to the publisher, then run it
copy artifacts/recovery/historical-r1-v1.1/Fehrest-historical-r1-v1.1-ed79.bundle scripts/recovery/
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/recovery/publish-historical-objects.ps1
del scripts/recovery/Fehrest-historical-r1-v1.1-ed79.bundle
```

The publisher verifies the bundle SHA-256, clones from the bundle into a disposable area, runs `git fsck --full --strict`, verifies the sealed commit/tree identities, then performs a normal non-force push of `refs/heads/recovered/r1-v1.1` to `refs/heads/historical/r1-v1.1` and re-reads the remote ref. It never force-pushes, rebases, or rewrites history, and it never mutates operational `main`.

## Prior outer recovery ZIP (provenance only, not mirrored)

```text
FILENAME=FEHREST-HISTORICAL-OBJECT-PUBLISH-V2.zip
SIZE_BYTES=827017
SHA256=a7c759273047294444ddb0477b9f84b6b729f590e818a7df0f53066c4256320e
ROLE=PRIOR_TRANSPORT_PROVENANCE_ONLY
MIRRORED_INTO_REPOSITORY=NO
REASON=The ZIP container is not the historical Git identity. The exact embedded bundle plus repository-native reconstruction/publication tooling are present above, which is what reproduces the object graph. Per the repository-completeness gate, the outer convenience ZIP need not be duplicated once those are present.
```

## Authority boundary

Mirroring these artifacts creates no R1 execution result and authorizes no scoring, unblinding, power analysis, confirmatory execution, or Spec 002 activation. Executor existence and qualification are not R1 evidence.
