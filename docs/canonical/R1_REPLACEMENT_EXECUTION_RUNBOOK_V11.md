# R1-X1 Replacement Variance Pilot — V11 Execution Authority Addendum

**Status:** ACTIVE R1 EXECUTION AUTHORITY / NON-SCORING  
**Recorded:** 2026-08-29  
**Supersedes only:** package identity, isolated-runtime bootstrap, and SDK verification plumbing in `docs/canonical/R1_REPLACEMENT_EXECUTION_RUNBOOK.md`.  
**Preserves:** every other R1 v1.1 protocol, evidence-integrity, credential, failure-routing, and post-execution gate in that runbook.

## Active package

```text
FILENAME=FEHREST-R1-X1-REPLACEMENT-V11.zip
SIZE_BYTES=10257
SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
CONTENTS=RUN_THIS_NOW.cmd,replacement.ps1,supervisor.py
```

## Preserved scientific bindings

```text
EXPECTED_HEAD=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
EXPECTED_ARMING_MANIFEST_SHA256=2e360072931ac2adfbdbba94da20d9198f8b24474852429545bcd14cd8653205
EXPECTED_R1_V1_1_DIGEST=5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
EXPECTED_RUNNER_FILESET_SHA256=30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f
EXPECTED_EXTERNAL_BUNDLE_SHA256=17934f84a07afef08e469b0526d343d26e5597ea3455e575b5f9c46ae91c321e
RANDOMIZATION_SEED=r1-x1-f10c4a673c44d412adb9c4f5a495d4c38265ce38301a778128b0fab622ed8a04
MODEL=gpt-5.6-terra
REASONING_EFFORT=medium
REPEATS=4
TRAJECTORIES=2
MAX_OUTPUT=1024
TOTAL_SESSIONS=888
MAINTENANCE_SESSIONS=168
CONTINUATION_SESSIONS=720
```

No sealed scientific binding changes in V11.

## Preserved V10 failure evidence

```text
V10_PREPARE_STATUS=PASS
V10_NO_API_PREPARE_GATE=PASS
V10_UV_EXECUTABLE_FOUND=YES
V10_UV_EXECUTABLE=C:\Users\Shehr\AppData\Local\hermes\bin\uv.exe
V10_ISOLATED_PYTHON_RUNTIME=READY
V10_OPENAI_SDK_INSTALL=PASS
V10_OPENAI_SDK_INSTALLED_VERSION=3.3.0
V10_SDK_VERIFY_STDERR=SyntaxError: invalid syntax
V10_SDK_VERIFY_OBSERVED_SOURCE_LINE=import
V10_FAILURE_REASON=FAIL_CLOSED: OPENAI_SDK_IMPORT_FAILED exit=1
V10_OPENAI_API_KEY_CLEARED_FROM_POWERSHELL=YES
V10_MODEL_CALLS_STARTED_AFTER_FAILURE=NO
```

The observed failure is fully explained by PowerShell `Start-Process -ArgumentList` splitting the Python `-c` payload such that Python received bare `import`. V10 therefore failed in SDK verification plumbing after the runtime and pinned SDK installation had succeeded, before credential capture and before any model call.

## V11 repair boundary

V11 preserves `supervisor.py` byte-for-byte from V10/V9:

```text
V10_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
V11_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
SUPERVISOR_BYTE_IDENTITY=PASS
```

V11 changes only `replacement.ps1` SDK import/version verification:

```text
V11_RUNTIME_BOOTSTRAP=uv venv --python <exact required uv-managed CPython>
V11_PINNED_SDK_INSTALL=uv pip install --python <isolated python> openai==3.3.0
V11_SDK_VERIFY_METHOD=runtime-local verify-openai-sdk.py
V11_SDK_VERIFY_SOURCE_ENCODING=UTF-8_WITHOUT_BOM
V11_SDK_VERIFY_SOURCE=import openai; print(openai.__version__)
PYTHON_DASH_C_USED_FOR_SDK_VERIFY=NO
```

The runtime-local probe is launcher plumbing only and is not part of the sealed repository, corpus, task set, oracle set, arm construction, runner, or raw evidence.

## Required pre-credential success sequence

```text
PREPARE_STATUS=PASS
NO_API_PREPARE_GATE=PASS
UV_EXECUTABLE_FOUND=YES
ISOLATED_PYTHON_RUNTIME=READY
SDK_VERIFY_PROBE_FILE=READY
OPENAI_SDK_VERSION=3.3.0
REPLACEMENT_MODEL_CALLS_EXECUTED=0
WAITING_FOR_REPLACEMENT_PILOT_API_KEY=YES
```

Any failure before the final line remains fail-closed and is not an R1 scientific observation.

## Authorization boundary

```text
SCORING_AUTHORIZED=NO
UNBLINDING_AUTHORIZED=NO
POWER_ANALYSIS_AUTHORIZED=NO
CONFIRMATORY_AUTHORIZED=NO
SPEC_002_ACTIVATED=NO
```

The V11 launcher may execute only the same valid replacement variance pilot already authorized by R1. Successful launcher completion still requires actual result/raw-seal evidence review before Issue #8 may close. All post-execution ordering from the base runbook remains unchanged.
