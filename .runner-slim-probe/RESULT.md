# Ubuntu Slim Runner Allocation Probe

Status: `FAIL_CLOSED_NO_RUNNER_ALLOCATED`

```text
BRANCH=ops/runner-slim-probe-20260829
PROBE_HEAD=430c75586cb3d256ec8769b3bd34c4ac3cbb68b7
WORKFLOW_RUN_ID=33255385399
RUN_ATTEMPT=1
JOB_ID=99108054364
RUNS_ON=ubuntu-slim
JOB_STATUS=completed
JOB_CONCLUSION=failure
RUNNER_ID=0
RUNNER_NAME=""
EXECUTABLE_STEPS=0
CANONICAL_MAIN_MUTATED=NO
R1_MUTATED=NO
SPEC_002_ACTIVATED=NO
```

The job failed before GitHub allocated a runner. No executable step ran. This probe used the standard private-repository `ubuntu-slim` container runner label as a distinct allocation pool from the previously tested `ubuntu-latest` and `windows-latest` labels.

This result does not identify a billing, policy, capacity, or account-side root cause. It only proves that `ubuntu-slim` was also unavailable for this repository at the recorded attempt.

The workflow file was removed from the branch tip before this result record was added. Do not rerun or reinterpret this branch as R1 execution evidence.
