# R1-X1 Replacement Variance Pilot — Execution Runbook

**Status:** ACTIVE R1 EXECUTION RUNBOOK / NON-SCORING  
**Recorded:** 2026-08-28  
**Execution package:** `FEHREST-R1-X1-REPLACEMENT-V8.zip`  
**Package SHA-256:** `9c53e45e41a0be5766779129a45e55aef4399d02395a1b4309e9d97114bef969`

> This runbook records the exact already-prepared replacement-pilot execution boundary. It does not change the sealed R1 v1.1 protocol, model condition, seed, scoring rule, arm construction, corpus, task set, oracle set, or confirmatory plan.

## 1. Why a replacement exists

The first variance-pilot batch is preserved but scientifically invalid for variance use because concurrent runners corrupted realized execution-order evidence.

The replacement supervisor fail-closes unless the invalidated source batch remains exactly:

```text
SOURCE_BATCH=variance-pilot-599054280a96
SOURCE_RECORD_COUNT=109
SOURCE_RAW_COUNT=109
SOURCE_EXECUTION_ORDER_COUNT=112
DUPLICATE_RECORD_IDS=[]
DUPLICATE_ORDER_IDS=[vm-000021,vm-000022]
ORDER_WITHOUT_RECORD=[vm-000059]
RECORD_WITHOUT_ORDER=[]
SOURCE_BATCH_STATUS=INVALIDATED_INFRASTRUCTURE_CONCURRENCY
SOURCE_BATCH_DISPOSITION=INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE
```

The invalidated batch must not be repaired by deleting, deduplicating, renumbering, or reinterpreting evidence.

## 2. Immutable execution bindings

V8 requires all of these exact bindings before any model call:

```text
EXPECTED_HEAD=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
EXPECTED_ARMING_MANIFEST_SHA256=2e360072931ac2adfbdbba94da20d9198f8b24474852429545bcd14cd8653205
EXPECTED_R1_V1_1_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
EXPECTED_RUNNER_FILESET_SHA256=30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f
EXPECTED_EXTERNAL_BUNDLE_SHA256=17934f84a07afef08e469b0526d343d26e5597ea3455e575b5f9c46ae91c321e
RANDOMIZATION_SEED=r1-x1-f10c4a673c44d412adb9c4f5a495d4c38265ce38301a778128b0fab622ed8a04
RUNNER_VERSION=r1-external-runner/1.1.0
TOTAL_SESSIONS=888
MAINTENANCE_SESSIONS=168
CONTINUATION_SESSIONS=720
```

The replacement must use the same v1.1 protocol:

```text
REPLACEMENT_DESIGN_CHANGE=NO
REPLACEMENT_SEED_CHANGE=NO
REPLACEMENT_MODEL_CONDITION_CHANGE=NO
REPLACEMENT_USES_SAME_V1_1_PROTOCOL=YES
```

## 3. Model/runtime condition

The V8 supervisor invokes the sealed runner with exactly:

```text
model=gpt-5.6-terra
reasoning_effort=medium
repeats=4
trajectories=2
max_output=1024
seed=r1-x1-f10c4a673c44d412adb9c4f5a495d4c38265ce38301a778128b0fab622ed8a04
```

The Windows launcher requires:

```text
Windows host with PowerShell + CIM process inspection
repository path=C:\Users\Shehr\OneDrive\Desktop\Fehrest
repository HEAD=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
repository worktree=CLEAN
Python 3.11 base=C:\Users\Shehr\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe
isolated virtual environment=created under %LOCALAPPDATA%\Fehrest\R1-X1\replacement-runtime-v8
openai SDK=3.3.0 exactly
active r1_runner.py run processes=0
```

The launcher may install `openai==3.3.0` into its isolated replacement runtime if that exact SDK is not already present there. This does not modify repository dependencies.

## 4. Credential boundary

The launcher deliberately clears `OPENAI_API_KEY` before preparation and does not request a credential until every no-API preflight gate passes.

Credential requirements:

```text
API key format begins with sk-
credential is captured only from the user's secure clipboard
credential is never committed to the repository
credential is never written into result evidence
credential is removed from the supervisor environment immediately after the runner returns
credential is removed again in PowerShell finally/catch cleanup
clipboard is overwritten with FEHREST_API_KEY_CAPTURED_REDACTED after capture
```

Do not paste an API key into GitHub, repository files, issues, PRs, logs, or chat transcripts.

## 5. Execution package contents

The verified V8 package contains:

```text
RUN_THIS_NOW.cmd
replacement.ps1
supervisor.py
```

Package identity:

```text
FILENAME=FEHREST-R1-X1-REPLACEMENT-V8.zip
SIZE_BYTES=9245
SHA256=9c53e45e41a0be5766779129a45e55aef4399d02395a1b4309e9d97114bef969
```

A retained copy is preserved with the project's 2026-08-28 Fehrest recovery artifacts.

## 6. No-API prepare gate

Before credential capture, `supervisor.py prepare` must verify:

```text
HEAD exact match
worktree clean
bench/R1/verify_v1_1.py PASS
R1 v1.1 canonical digest present
runner fileset digest present
external bundle digest present
source arming digest exact
source preflight digest exact
invalidated source batch counts exact
invalidated duplicate/order anomaly exact
external bundle archive exact
replacement preflight byte-identical to source preflight
```

Success produces a write-once incident record and replacement arming manifest with:

```text
PREPARE_STATUS=PASS
SOURCE_BATCH_STATUS=INVALIDATED_INFRASTRUCTURE_CONCURRENCY
REPLACEMENT_MODEL_CALLS_EXECUTED=0
```

Any mismatch fails closed before a credential is accepted.

## 7. Execution command

The human-facing package entry point is:

```text
RUN_THIS_NOW.cmd
```

It launches `replacement.ps1`, which runs the no-API prepare gate, creates/verifies the isolated Python runtime, captures the secure credential, then invokes:

```text
supervisor.py run
```

The supervisor invokes the sealed external runner only after acquiring the single-runner lock.

## 8. Evidence integrity gates after execution

A runner exit code of zero is not sufficient by itself.

The supervisor additionally requires:

```text
records count == raw count == execution-order count
no duplicate record IDs
no duplicate order IDs
no orphan raw files
no record missing raw file
no execution-order entry without record
no record without execution-order entry
model_returned values are either empty or exactly gpt-5.6-terra
runner reports R1_VARIANCE_PILOT_STATUS=EXECUTION_COMPLETE_UNSCORED
runner reports PLANNED_TOTAL_SESSIONS=888
secret scan PASS
first raw seal PASS
second raw seal PASS
seal digests identical
raw archive exists
raw archive SHA-256 equals the reproducible seal digest
```

No scoring, power analysis, unblinding, or confirmatory execution occurs in V8.

## 9. Required success artifact

The launcher writes the result to:

```text
FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt
```

A genuine successful replacement must contain at minimum:

```text
R1_VARIANCE_PILOT_FINAL_STATUS=EXECUTION_COMPLETE_UNSCORED_REPLACEMENT
SOURCE_BATCH_DISPOSITION=INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE
SECRET_SCAN=PASS
RAW_SEAL_STATUS=PASS
RAW_SEAL_REPRODUCIBILITY=PASS
R1_VARIANCE_PILOT_RAW_SHA256=<actual digest>
OPENAI_API_KEY_CLEARED_FROM_SUPERVISOR=YES
SCORING_STATUS=NOT_STARTED
UNBLINDING_STATUS=NOT_STARTED
POWER_ANALYSIS_STATUS=NOT_PERFORMED
CONFIRMATORY_STATUS=NOT_STARTED
NEXT_GATE=FOUNDER_REVIEW_BEFORE_BLINDED_SCORING
```

The actual result file and raw archive digest are required evidence. The intended success markers in this runbook are not substitutes for them.

## 10. Failure routing

The supervisor records specific fail-closed states, including:

```text
HALTED_OR_INCOMPLETE
HALTED_EVIDENCE_INTEGRITY
HALTED_MODEL_IDENTITY_DRIFT
HALTED_SECRET_SCAN
REVIEW_REPLACEMENT_SUPERVISOR_FAILURE
```

A failed or incomplete replacement is preserved and reviewed. Do not silently retry in a way that deletes attempt evidence or changes the scientific condition.

## 11. Current execution blocker

The repository/provenance side is now recoverable and verified, but the connected repository execution environment does not supply the required combination of:

```text
user's Windows Fehrest host state
Windows CIM + msvcrt single-runner environment
secure user clipboard credential capture
provider-authenticated OpenAI API execution path for 888 sealed sessions
```

Therefore the next R1 scientific action cannot be truthfully executed by repository-only tooling.

Current state:

```text
R1_REPLACEMENT_EXECUTOR=RECOVERED_AND_VERIFIED
R1_REPLACEMENT_EXECUTOR_SHA256=9c53e45e41a0be5766779129a45e55aef4399d02395a1b4309e9d97114bef969
R1_REPLACEMENT_PREPARE_LOGIC=VERIFIED
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
R1_TERMINAL_VERDICT=NOT_VERIFIED
```

## 12. After a successful replacement

Do not jump to product implementation.

The next gate is exactly:

```text
FOUNDER_REVIEW_BEFORE_BLINDED_SCORING
```

Only after the actual sealed replacement result is reviewed may the repository determine whether blinded scoring is authorized under the active R1 protocol. Spec 002 remains blocked until the entire R1 terminal route and its own activation gates close.