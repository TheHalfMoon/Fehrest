# R1 — controlled runner requirements

```
CONTROLLED_RUNNER_STATUS: UNAVAILABLE on the authoring host
```

A model that can answer questions is not a runner. A runner is the thing that makes a
result auditable a year later by someone who does not trust you.

---

## 1. Admissibility

A runner is admissible only if **all** of these hold:

1. **Fresh independent executions.** Every continuation run starts a new session with
   no memory of any prior task, prior arm or prior repeat.
2. **No conversation reuse.** Not between repeats, not between arms, not between tasks.
3. **Configuration is set by the caller**, not by a UI default that can change.
4. **Per-run evidence is captured** to the schema in §3, including the raw response.
5. **Failures are distinguishable** — a provider timeout must not be recordable as a
   wrong answer.

### 1.1 Explicitly not admissible

**An interactive IDE or chat window does not qualify**, even though a model inside it
can answer every task correctly. It fails on session isolation, on configuration
pinning, and on evidence capture. Using one would produce numbers that look like
measurements without being measurements, and the difference is invisible in the
output — which is exactly why the rule is written down rather than left to judgement.

The authoring host has: no API credential, no local runner (`ollama`, `llama.cpp`,
`vLLM`, LM Studio all absent), and no scriptable agent CLI. Several desktop IDE
applications are installed. **None of them is admissible under §1**, so no model was
run and none was simulated.

## 2. Roles

| Role | Session shape |
|---|---|
| `MAINTAINER` | One session per (arm, scenario, checkpoint, trajectory). Sees the checkpoint's new evidence and the arm's current artefact. Task-blind |
| `CONTINUATION_AGENT` | One session per (arm, task, repeat). Sees the arm's context package and the task prompt. Nothing else |

A maintainer session must never receive a task, an oracle, a future checkpoint, or any
statement that a fact will be scored later.

## 3. Per-run record — required schema

One JSON object per run, appended to `runs/<stage>/records.jsonl`.

```json
{
  "run_id": "vp-000431",
  "arm_id": "ARM_C",
  "scenario_id": "S1",
  "task_id": "S1-L-FRESH-SUPERSESSION",
  "checkpoint": 3,
  "repeat_index": 2,
  "trajectory_id": "T1",
  "role": "CONTINUATION_AGENT",

  "model_provider": "...",
  "model_identifier": "...",
  "model_version_or_snapshot": "... | UNAVAILABLE",

  "system_prompt_digest": "sha256:...",
  "user_prompt_digest":   "sha256:...",
  "context_package_digest": "sha256:...",

  "temperature": 0.0,
  "top_p": "... | UNAVAILABLE",
  "seed": "... | UNAVAILABLE",
  "max_output": 1024,
  "reasoning_effort": "... | UNAVAILABLE",

  "tool_set": [],
  "tool_permissions": "none",
  "time_limit_s": 120,

  "start_time": "2026-08-19T10:00:00Z",
  "end_time":   "2026-08-19T10:00:07Z",

  "raw_response_digest": "sha256:...",
  "raw_response_artifact": "runs/variance-pilot/raw/vp-000431.txt",

  "input_token_count":  "... | UNAVAILABLE",
  "output_token_count": "... | UNAVAILABLE",

  "outcome": "OK | TASK_FAILURE | INFRASTRUCTURE_FAILURE",
  "failure_class": "... | null",
  "attempt": 1
}
```

### 3.1 `UNAVAILABLE` is a real value

If the provider does not expose a seed, or a top-p, or token counts, the field is
`UNAVAILABLE`. **It is never omitted, never guessed, and never filled with a default
that implies it was pinned.** A study that claims a pinned seed it never had is worse
than one that admits the seed was unavailable, because only the second can be
correctly discounted by a reader.

`tool_set` is `[]` and `tool_permissions` is `"none"` for every arm. The treatment is
the context condition, not tool access, and no arm may receive a tool another lacks.

## 4. Failure taxonomy — classified before execution

| Class | Kind | Handling |
|---|---|---|
| Provider timeout | `INFRASTRUCTURE_FAILURE` | Retry per §5 |
| Rate limit | `INFRASTRUCTURE_FAILURE` | Back off, retry per §5 |
| Network error | `INFRASTRUCTURE_FAILURE` | Retry per §5 |
| Runner crash | `INFRASTRUCTURE_FAILURE` | Retry per §5 |
| Tool failure | `INFRASTRUCTURE_FAILURE` | Retry per §5 (no arm uses tools, so this should never fire; if it does, the run is suspect) |
| Context-limit exceeded | `INFRASTRUCTURE_FAILURE` | **Not** a task failure. The budget is 6,000 bytes; exceeding a model's context means the runner is misconfigured |
| Empty response | **`TASK_FAILURE`** | Scored. Empty scores 0 by design |
| Malformed response | **`TASK_FAILURE`** | Scored as-is. Not repaired |
| Refusal | **`TASK_FAILURE`** | Scored as-is, and flagged |

The line that matters: **an infrastructure failure is not evidence about an arm; a task
failure is.** Collapsing the two lets a flaky network look like a weak baseline.

## 5. Retry policy — identical for every arm

```
INFRASTRUCTURE_FAILURE : retry up to 2 times, exponential backoff.
                         Still failing -> record EXCLUDED_INFRA, exclude the
                         (task, repeat) cell FOR EVERY ARM, symmetrically.
TASK_FAILURE           : no retry. Ever. It is the result.
```

**Selective retry of Fehrest is prohibited.** So is retrying any single arm because its
answer looked wrong. Every attempt is recorded with its `attempt` index, including the
ones that failed.

## 6. Raw output is immutable

Raw model output is evidence. It is written once, digested, and never edited.

**No manual repair of an answer before scoring, for any reason.** Not to fix a
formatting slip, not to correct an obvious typo, not because the intent was clear.

If the parser needs normalization — trimming whitespace, tolerating a wrapped field —
then all three are preserved:

```
raw/<run_id>.txt              the untouched response
normalized/<run_id>.txt       what the scorer actually read
NORMALIZER_VERSION            the exact normalizer that produced it
```

A normalizer change is a benchmark version change. It requires a new digest and a
rescore of **every** arm, never of one.

## 7. Scoring

```bash
cargo run --bin fehrest-r1 -- score runs/<stage>/responses
```

Responses are laid out as `responses/<ARM_ID>/<TASK_ID>.txt`, where `ARM_ID` is the
**neutral** identifier. The scorer never sees "Fehrest", "wiki" or "baseline", and the
strings do not appear in any model-visible prompt either.

The arm-identity mapping lives in `runs/<stage>/arm-map.json`, is withheld until
scoring is complete, and is then used to unblind.

If human adjudication is ever required, the adjudication record is preserved — who,
when, what was shown, what was decided, and on what grounds. **A deterministic hidden
-test failure is not overturned because the answer looks reasonable.**

## 8. Execution order

The realized order is appended to `runs/<stage>/execution-order.jsonl` as it happens.
A planned order is not evidence; an executed one is. Blocked and interleaved per
[VARIANCE-PILOT.md §3](./VARIANCE-PILOT.md), so provider drift cannot align with arm.
