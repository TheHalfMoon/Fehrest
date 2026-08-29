# Hosted Runner Probe — 2026-08-29

Status: `BLOCKED_BEFORE_RUNNER_EXECUTION`

This temporary branch records a bounded runner-allocation probe only. It is not historical publication evidence and does not advance R1.

```text
BASE_MAIN=d3ba3bd505c2df00389c6a7014cd130972160491
PROBE_COMMIT=ea32166bde9c75086f7ce61746a27730e455c0e2
WORKFLOW_RUN=33250476412
WORKFLOW_CONCLUSION=FAILURE
WINDOWS_JOB=99095174621
WINDOWS_JOB_CONCLUSION=FAILURE
WINDOWS_EXECUTABLE_STEPS=NONE
WINDOWS_LOG_BLOB=NOT_CREATED
UBUNTU_JOB=99095174732
UBUNTU_JOB_CONCLUSION=FAILURE
UBUNTU_EXECUTABLE_STEPS=NONE
UBUNTU_LOG_BLOB=NOT_CREATED
MAIN_CHANGED=NO
R1_CHANGED=NO
FORCE_PUSH_USED=NO
REBASE_USED=NO
```

Both `windows-latest` and `ubuntu-latest` failed before any executable step was allocated. This rules out the prior historical workflow commit and runner OS choice as sufficient explanations for the Fehrest hosted-runner failure.

The connected Git Data API can create byte-exact blobs and trees, but its commit-creation action does not expose arbitrary historical author/committer identity and timestamp fields. Therefore it cannot recreate the sealed historical commit `ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c` exactly. A different commit identity is not acceptable for Issue #1.

The probe workflow is removed at this branch tip so this temporary branch cannot accidentally become an execution route. Issue #1 remains authoritative.
