# R1 instrument pilot

```
PURPOSE:                 validate the measurement instrument
ESTABLISHES_PRODUCT_SUCCESS: NO -- NEVER
MODEL_EXECUTED:          NO
ARM_SCORES_PRODUCED:     NONE
RESULT:                  631 checks, 0 failed
VARIANCE_ESTIMATE:       UNAVAILABLE_WITHOUT_MODEL_EXECUTION
```

Part O of the directive separates the instrument pilot from the confirmatory run, and
lists what the pilot exists to discover: broken scoring, impossible tasks,
ceiling/floor effects, ambiguous oracles, model-run plumbing errors, baseline leakage,
variance estimates.

This pilot found three real defects and could not produce the last item. Both facts
are below.

Raw output: [pilot-output.txt](./pilot-output.txt). Reproduce with:

```bash
cargo run --bin fehrest-r1 -- selftest
```

---

## 1. What was checked

Counts are emitted by the harness, not asserted here.

| # | Check family | Count | What a failure would mean |
|---|---|---|---|
| 1 | Task/oracle correspondence | 90 | A task with no oracle, an orphan oracle, or a task whose kind disagrees with its oracle's abstention polarity |
| 2 | Answerability and trap reality | 106 | An **impossible task** — the answer is not derivable from evidence visible at that checkpoint — or a **fake trap** whose distractor never appears in the corpus |
| 3 | Scorer validation | 209 | The primary metric rewards the wrong thing |
| 4 | Package construction | 110 | An arm produces nothing, or exceeds the shared budget |
| 5 | Baseline metadata isolation | 56 | Fehrest metadata leaked into a baseline arm, invalidating the comparison |
| 6 | Temporal boundary | 55 | An arm can see the future |
| 7 | Negative controls | 5 | A detector that never fires and therefore proves nothing |
| | **Total** | **631** | |

### 1.1 Scorer validation, in detail

For every one of the 30 tasks, six synthetic responses are scored. **These are not
model outputs and are never reported as arm results** — they exist to prove the scorer
rewards and punishes the right things.

| Synthetic response | Required outcome | Property it protects |
|---|---|---|
| `gold` — satisfies every oracle requirement | scores **1** | The metric is achievable; no task is impossible |
| `stale` — gold plus one forbidden distractor | scores **0** | Acting on superseded or failed material is punished |
| `empty` — the empty string | scores **0** | **Silence earns nothing, on every task type** |
| `abstain_only` — bare `ABSTAIN: YES` | scores **0** | Abstention credit needs a substantive action, not just a refusal |
| `hedge` — fluent prose ignoring the contract | scores **0** | Fluency without the contract is not credit |
| `wrong_abstain` — correct content, inverted abstention | scores **0** | Abstention polarity is enforced in both directions |

This is the V0 defect closed. V0's `ABSENT` class scored `!contains_stale`, which an
empty context satisfied trivially — the do-nothing arm and the treatment received the
same score for opposite reasons. Here the empty response scores zero on all 30 tasks,
including both abstention tasks, and that is asserted rather than argued.

### 1.2 Negative controls

A passing check proves nothing if the detector cannot fail. Each detector is re-run
against a deliberately corrupted input and must fire:

| Control | Asserts |
|---|---|
| Temporal boundary | Injecting future-only vocabulary into a package **is** detected |
| Non-vacuity | Future-only vocabulary actually exists at the tested checkpoint, so the boundary check is not empty |
| Metadata isolation | An injected `<fehrest:item` envelope in a baseline **is** detected |
| Scorer | A fully correct answer with an emptied `ACTION` is **rejected** |

---

## 2. Defects the pilot found

All three were found and fixed **before** preregistration and before any model ran.
That is the correct time and the only reason to run a pilot.

### D-1 · A fake trap

`S2-C-CONSTRAINT` declared `"united states"` as a distractor token. The corpus never
contains that phrase — it says *"the shared warehouse has a US replica"*. The phrase
appears only in the **task prompt**.

A trap that exists only in the prompt tests nothing about context: every arm sees the
prompt. `trap_present` was corrected to the real corpus anchors, `"us replica"` and
`"shared warehouse"`.

**Why it matters:** without this check, one of five `CONSTRAINT_RETENTION` tasks would
have been silently measuring prompt comprehension rather than context retention.

### D-2 · Every task sat at the end of its scenario

The first draft issued all 22 tasks at each scenario's **final** checkpoint. The
non-vacuity control caught it: at the final checkpoint there is no future, so the
temporal-boundary check had nothing to test.

The consequence was far worse than a vacuous assertion. **A benchmark whose every task
sits at the last checkpoint cannot measure maintenance lag, staleness or knowledge
decay** — the arm is only ever asked about a project that has stopped moving. That is
the precise property R1 was created to measure, and the first draft could not measure
it.

Fixed by adding **8 mid-history tasks** at `t1`–`t6`, including several deliberately
issued at the checkpoint where a decision reverses, so an arm whose maintenance lags by
one checkpoint answers with the decision that was replaced that same day. The harness
now **asserts** that at least one task is issued before its scenario ends.

### D-3 · The leakage detector fired on output format

After D-2 was fixed, the temporal-boundary check failed on B5 at four checkpoints,
reporting the leaked token `"current"`.

It was a false positive. Fehrest's compiler emits a `current_decisions` **section
label** unconditionally, and the word "current" happens to appear later in the corpus
in `status-current.md`. The package carried no future knowledge — it carried its own
output format.

Fixed by subtracting each arm's **structural vocabulary**, defined mechanically as the
words that arm emits at `t0`, before any later evidence exists. Anything an arm emits
at the first checkpoint is format, not knowledge.

**Why the fix is principled rather than convenient:** it is derived from the arm's own
behaviour at a checkpoint where the future does not yet exist, it applies identically
to every arm, and it cannot mask real content leakage — content from `Tj > i` cannot
appear in a `t0` package.

---

## 3. What the pilot could not do

### 3.1 No variance estimate

`VARIANCE_ESTIMATE: UNAVAILABLE_WITHOUT_MODEL_EXECUTION`.

Variance in this benchmark is variance **in model behaviour**, and no model ran. The
instrument is deterministic: the same corpus produces the same packages and the same
synthetic scores every time. That determinism is a property of the harness and says
nothing about how much a model's answers vary between runs.

Consequently **the confirmatory sample size cannot be chosen yet**, and it will not be
chosen by looking for the number that makes Fehrest significant. The order is fixed:
model execution → observed variance → power analysis → confirmatory N.

### 3.2 No ceiling or floor effects observed

Ceiling and floor effects are properties of how **arms** score, and no arm has a score.
What the pilot establishes is narrower and worth stating precisely: for every task, a
response satisfying the oracle exists and scores 1, and several plausible wrong
responses score 0. That rules out *impossible* tasks and *trivially satisfiable* tasks.
It does not rule out tasks that every arm happens to pass or every arm happens to fail.

### 3.3 No task-validity result

B-NULL — the calibration arm that detects tasks answerable from the prompt alone —
requires a model. Until it runs, **it is not established that any task actually needs
the project context.** The 30 tasks are constructed to require it, and D-1 shows that
assumption can be wrong in ways only execution will reveal.

### 3.4 No arm is scorable yet

B1, B4 and B5 have no maintainer output, so they have no artefact:

```
B1 S1  ABSENT -- arm cannot be scored until a maintainer runs
B4 S1  ABSENT -- arm cannot be scored until a maintainer runs
B5 S1  ABSENT -- arm cannot be scored until a maintainer runs
   ... same for S2, S3
```

The package-construction checks ran against a deterministic **plumbing** maintainer,
labelled as such in the harness and in the output. It is task-blind and mechanical, it
is not a maintenance strategy anyone would use, and **no score computed over it is
reported as an arm result.** Its only job is to make B1/B4/B5 emit a well-formed
package so the budget, leakage and metadata assertions have something to run against.

---

## 4. Standing

```
R1_INSTRUMENT_PILOT:  PASS
INSTRUMENT_CHECKS:    631 passed, 0 failed
DEFECTS_FOUND:        3 (all fixed before preregistration)
PRODUCT_THESIS:       NOT_EVALUATED
CONFIRMATORY:         NOT_STARTED
```

**A passing instrument pilot is not a result about Fehrest.** It says the ruler is
straight. Nothing has been measured with it.
