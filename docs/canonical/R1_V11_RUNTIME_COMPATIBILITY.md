# R1 V11 Runtime Compatibility Qualification

**Status:** ACTIVE R1 EXECUTION COMPATIBILITY EVIDENCE / NON-SCORING
**Recorded:** 2026-08-29

This document records only the launcher/runtime compatibility evidence observed before any model call. It does not alter the sealed R1 v1.1 experiment design, model, reasoning effort, seed, arms, corpus, task/oracle set, scoring rules, session counts, or confirmatory plan.

## Preserved V10 attempt

```text
V10_PACKAGE=FEHREST-R1-X1-REPLACEMENT-V10.zip
V10_PACKAGE_SHA256=67c5f4a943084eef069397468c41c3ec2547660dea212d735394e260f72841a3
V10_PREPARE_STATUS=PASS
V10_NO_API_PREPARE_GATE=PASS
V10_UV_EXECUTABLE_FOUND=YES
V10_ISOLATED_PYTHON_RUNTIME=READY
V10_OPENAI_SDK_INSTALL=PASS
V10_OPENAI_SDK_INSTALLED_VERSION=3.3.0
V10_SDK_VERIFY_FAILURE=PYTHON_C_ARGUMENT_QUOTING
V10_SDK_VERIFY_OBSERVED_SOURCE_LINE=import
V10_LAUNCHER_STATUS=FAIL
V10_OPENAI_API_KEY_CLEARED_FROM_POWERSHELL=YES
V10_MODEL_CALLS_STARTED_AFTER_FAILURE=NO
```

The V10 evidence proves `uv venv` created the required Python 3.11.15 environment and `uv pip` installed `openai==3.3.0`. The final SDK import/version verification failed because PowerShell `Start-Process -ArgumentList` passed the Python `-c` payload as split command-line tokens; Python observed only bare `import`, producing a `SyntaxError`. This is launcher verification plumbing only and produced no scientific observation.

## V11 compatibility repair

```text
V11_PACKAGE=FEHREST-R1-X1-REPLACEMENT-V11.zip
V11_PACKAGE_SIZE_BYTES=10257
V11_PACKAGE_SHA256=92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89
V10_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
V11_SUPERVISOR_SHA256=c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7
SUPERVISOR_BYTE_IDENTITY=PASS
```

V11 preserves the V10 uv-based runtime bootstrap and pinned `openai==3.3.0` installation. It changes only SDK verification plumbing: V11 writes a runtime-local UTF-8-without-BOM `verify-openai-sdk.py` containing `import openai` and `print(openai.__version__)`, then executes that script path instead of using Python `-c` through `Start-Process`.

```text
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
SCORING_AUTHORIZED=NO
UNBLINDING_AUTHORIZED=NO
CONFIRMATORY_AUTHORIZED=NO
SPEC_002_ACTIVATED=NO
```

A V11 attempt remains external evidence-dependent. Executor existence or compatibility qualification is not an R1 execution result.
