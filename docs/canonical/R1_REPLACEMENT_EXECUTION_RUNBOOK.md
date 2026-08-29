# R1-X1 Replacement Variance Pilot — Execution Runbook

**Status:** ACTIVE R1 EXECUTION RUNBOOK / NON-SCORING  
**Recorded:** 2026-08-28  
**Updated:** 2026-08-29  
**Execution package:** `FEHREST-R1-X1-REPLACEMENT-V10.zip`  
**Package SHA-256:** `67c5f4a943084eef069397468c41c3ec2547660dea212d735394e260f72841a3`

> This runbook records the exact replacement-pilot execution boundary. It does not change the sealed R1 v1.1 protocol, model condition, seed, scoring rule, arm construction, corpus, task set, oracle set, or confirmatory plan.

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

## 2. Preserved V8 and V9 fail-closed attempts

### V8

V8 remains preserved as a failed pre-execution attempt:

```text
V8_PACKAGE=FEHREST-R1-X1-REPLACEMENT-V8.zip
V8_PACKAGE_SHA256=9c53e45e41a0be5766779129a45e55aef4399d02395a1b4309e9d97114bef969
V8_PREPARE_STATUS=FAIL
V8_FAILURE_CLASS=JSONDecodeError
V8_FAILURE_REASON=Unexpected UTF-8 BOM while decoding existing JSON metadata as plain utf-8
V8_OPENAI_API_KEY_CLEARED_FROM_POWERSHELL=YES
V8_MODEL_CALLS_STARTED_AFTER_FAILURE=NO
V8_SCORING_AUTHORIZED=NO
V8_UNBLINDING_AUTHORIZED=NO
V8_CONFIRMATORY_AUTHORIZED=NO
```

The failure occurred in `supervisor.py prepare` after repository/seal verification but before credential capture and before any model call. It therefore produced no scientific observation and did not alter the R1 design.

### V9

V9 changed only metadata decoding in `supervisor.py` so pre-existing BOM-prefixed UTF-8 JSON/JSONL could be interpreted without rewriting their bytes. On the required Windows host, V9 proved that compatibility repair:

```text
V9_PACKAGE=FEHREST-R1-X1-REPLACEMENT-V9.zip
V9_PACKAGE_SHA256=48da655c6e30da77a1073ffa149a360929a407d25ecbb8fb01d4c8a26429ef2a
V9_PREPARE_STATUS=PASS
V9_NO_API_PREPARE_GATE=PASS
V9_INCIDENT_SHA256=3c70cef6cc74304703e46a2135121f06b6a4aa039e366b6edab7d0ecd71063e2
V9_REPLACEMENT_ARMING_MANIFEST_SHA256=a7ae52b503d6c7b66cf03624aa78bd82b0349d5b02e9e0537b6a7985e1eff2ae
V9_REPLACEMENT_MODEL_CALLS_EXECUTED=0
V9_RUNTIME_PHASE=CREATING_ISOLATED_PYTHON_RUNTIME
V9_LAUNCHER_STATUS=FAIL
V9_FAILURE_REASON=Traceback (most recent call last):
V9_OPENAI_API_KEY_CLEARED_FROM_POWERSHELL=YES
V9_MODEL_CALLS_STARTED_AFTER_FAILURE=NO
```

The V9 launcher preserved only the first traceback line in its catch-path `FAILURE_REASON`. The repository therefore does **not** claim an unverified root cause for the runtime-bootstrap failure. The evidence proves only that no-API prepare passed, isolated-runtime creation began, the launcher failed closed there, no model call started after the failure, and the PowerShell environment cleared `OPENAI_API_KEY`.

## 3. V10 launcher/runtime compatibility repair

V10 preserves the V9 `supervisor.py` byte-for-byte:

```text
V9_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
V10_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
SUPERVISOR_BYTE_IDENTITY=PASS
```

V10 changes only `replacement.ps1` runtime bootstrap and diagnostics:

```text
V9_REPLACEMENT_PS1_SHA256=694db9b8cdd484bb788c54f4313426d45c7d69c181331fb18285370a8d09cfae
V10_REPLACEMENT_PS1_SHA256=5c4dec69867f9e281f18218b0d2a62f68b4a7992292a20f8377c3dd929002b46
V10_RUNTIME_BOOTSTRAP=uv venv --clear --python <exact required uv-managed CPython> <isolated venv>
V10_PINNED_SDK_INSTALL=uv pip install --python <isolated python> openai==3.3.0
V10_DIAGNOSTICS=complete uv venv / uv pip / SDK verification stdout+stderr plus PowerShell failure type and stack
CANONICAL_R1_RUNNER_CHANGED=NO
SEALED_REPOSITORY_CONTENT_CHANGED=NO
R1_V1_1_DIGEST_CHANGED=NO
RUNNER_FILESET_CHANGED=NO
EXTERNAL_BUNDLE_CHANGED=NO
MODEL_CHANGED=NO
REASONING_EFFORT_CHANGED=NO
SEED_CHANGED=NO
ARM_CONSTRUCTION_CHANGED=NO
CORPUS_CHANGED=NO
TASK_SET_CHANGED=NO
ORACLE_SET_CHANGED=NO
SCORING_RULE_CHANGED=NO
SESSION_COUNTS_CHANGED=NO
CONFIRMATORY_PLAN_CHANGED=NO
```

The exact required Python base is already a uv-managed CPython installation. V10 delegates creation of the isolated environment and installation of the pinned `openai==3.3.0` SDK to `uv` rather than invoking `python -m venv`. This is launcher/runtime plumbing only. It does not change the scientific executor or any experiment input.

## 4. Immutable execution bindings

V10 requires all of these exact bindings before any model call:

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

## 5. Model/runtime condition

The V10 supervisor invokes the sealed runner with exactly:

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
isolated virtual environment=created under %LOCALAPPDATA%\Fehrest\R1-X1\replacement-runtime-v10
uv executable=resolved from PATH or known per-user uv installation paths
openai SDK=3.3.0 exactly
active r1_runner.py run processes=0
```

V10 creates the isolated runtime through `uv venv` using the exact required Python executable and installs `openai==3.3.0` through `uv pip` when that exact SDK is not already importable inside the isolated runtime. This does not modify repository dependencies.

## 6. Credential boundary

The launcher deliberately clears `OPENAI_API_KEY` before preparation and does not request a credential until every no-API preflight and isolated-runtime gate passes.

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

## 7. Execution package contents

The verified V10 package contains:

```text
RUN_THIS_NOW.cmd
replacement.ps1
supervisor.py
```

Package identity:

```text
FILENAME=FEHREST-R1-X1-REPLACEMENT-V10.zip
SIZE_BYTES=10040
SHA256=67c5f4a943084eef069397468c41c3ec2547660dea212d735394e260f72841a3
```

V10 was constructed from V9 with the exact V9 supervisor and command entrypoint unchanged. Only `replacement.ps1` changed for uv-based isolated-runtime bootstrap and complete diagnostic capture.

## 8. No-API prepare gate

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

Success produces or verifies the write-once incident record and replacement arming manifest with:

```text
PREPARE_STATUS=PASS
SOURCE_BATCH_STATUS=INVALIDATED_INFRASTRUCTURE_CONCURRENCY
REPLACEMENT_MODEL_CALLS_EXECUTED=0
```

Any mismatch fails closed before a credential is accepted.

## 9. Isolated-runtime gate

After prepare and still before credential capture, V10 must establish and verify the runtime:

```text
UV_EXECUTABLE_FOUND=YES
ISOLATED_PYTHON_RUNTIME=READY
OPENAI_SDK_VERSION=3.3.0
REPLACEMENT_MODEL_CALLS_EXECUTED=0
```

Any `uv venv`, `uv pip`, SDK import, or version failure is captured with its complete subprocess stdout/stderr and fails closed before credential capture. Such a failure is infrastructure/runtime evidence only and is not an R1 scientific observation.

## 10. Execution command

The human-facing package entry point is:

```text
RUN_THIS_NOW.cmd
```

It launches `replacement.ps1`, which runs the no-API prepare gate, creates/verifies the isolated Python runtime, captures the secure credential, then invokes:

```text
supervisor.py run
```

The supervisor invokes the sealed external runner only after acquiring the single-runner lock.

## 11. Evidence integrity gates after execution

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

No scoring, power analysis, unblinding, or confirmatory execution occurs in V10.

## 12. Required success artifact

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

## 13. Failure routing

The supervisor records specific fail-closed states, including:

```text
HALTED_OR_INCOMPLETE
HALTED_EVIDENCE_INTEGRITY
HALTED_MODEL_IDENTITY_DRIFT
HALTED_SECRET_SCAN
REVIEW_REPLACEMENT_SUPERVISOR_FAILURE
```

A failed or incomplete replacement is preserved and reviewed. Do not silently retry in a way that deletes attempt evidence or changes the scientific condition.

Pre-API compatibility failures may be superseded only by non-semantic launcher/parser/runtime repairs that preserve all sealed experiment bindings and are separately recorded before execution.

## 14. Current execution blocker

The repository/provenance side is recoverable and verified, but the connected repository execution environment does not supply the required combination of:

```text
user's Windows Fehrest host state
Windows CIM + msvcrt single-runner environment
secure user clipboard credential capture
provider-authenticated OpenAI API execution path for 888 sealed sessions
```

Therefore the next R1 scientific action cannot be truthfully executed by repository-only tooling.

Current state:

```text
R1_REPLACEMENT_EXECUTOR=V10_RUNTIME_BOOTSTRAP_QUALIFIED_FOR_EXTERNAL_ATTEMPT
R1_REPLACEMENT_EXECUTOR_SHA256=67c5f4a943084eef069397468c41c3ec2547660dea212d735394e260f72841a3
R1_REPLACEMENT_V8_RESULT=FAIL_CLOSED_PREPARE_BOM_NO_MODEL_CALLS
R1_REPLACEMENT_V9_RESULT=PREPARE_PASS_THEN_FAIL_CLOSED_RUNTIME_BOOTSTRAP_NO_MODEL_CALLS
R1_REPLACEMENT_EXECUTION_RESULT=NOT_PRESENT
R1_TERMINAL_VERDICT=NOT_VERIFIED
```

## 15. After a successful replacement

Do not jump to product implementation.

The next gate is exactly:

```text
FOUNDER_REVIEW_BEFORE_BLINDED_SCORING
```

Only after the actual sealed replacement result is reviewed may the repository determine whether blinded scoring is authorized under the active R1 protocol. Spec 002 remains blocked until the entire R1 terminal route and its own activation gates close.
