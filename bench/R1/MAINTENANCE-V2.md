# R1-V2 — maintenance protocol

`THE SINGLE MOST IMPORTANT CORRECTION OVER V0`

In V0, B4's wiki and B5's memories were both hand-authored to be perfectly current, with zero lag, by someone who already knew the questions. That assumed away most of what Fehrest claims. R1 measures maintenance instead of granting it.

This is the ceiling-effect successor maintenance protocol. It extends R1-v1 maintenance with epoch-transition handling for the extended 15-checkpoint scenarios.

---

## 1. The rule

> **No maintained arm receives an omniscient free update.**

At every checkpoint `Ti`, each maintained arm's maintainer:

1. receives the **same** new-evidence bundle every other maintainer receives;
2. sees **nothing** from `Tj > i`;
3. sees **no task**, and is never told which facts will be scored;
4. decides for itself what, if anything, to change;
5. has every action counted.

B0 and B3 are unmaintained. Their maintenance cost is zero beyond ordinary project work. **This is a real advantage and the benchmark is built to let it win.**

## 2. T0 initialization rule

**t0 is the initialized scenario state.** No model-driven maintainer action is required at t0. Maintenance sessions begin at t1 and continue through t14.

This is a deliberate scientific construct: the initial state is given, and the maintainer's job is to *maintain* it as the project evolves, not to create it from scratch.

**Session arithmetic:**
- 3 scenarios × 14 transitions (t1-t14) × 3 maintained arms (B1, B4, B5) × 2 trajectories = **252 maintenance sessions**

## 3. Maintainer fairness

The maintainer is task-blind. It is not told "this fact will matter later", it never sees an oracle, and it never sees a continuation prompt. The maintenance session's instruction is identical across arms except for the artefact format it edits.

Three failure modes this rules out, all of which V0 permitted:

| Failure mode | Why it is fatal |
|---|---|
| Retrospective wiki | A document written after the questions are known is not a maintained document, it is an answer key |
| Selective diligence | Updating B5 carefully and B4 carelessly makes the comparison meaningless |
| Future knowledge | A maintainer who knows a decision will be reversed writes differently today |

## 4. Session contract

One maintenance session per `(arm, scenario, checkpoint)` for t1 through t14. Fresh and stateless: the maintainer's only memory of previous checkpoints is **the artefact it already produced**, which is the property under test.

Inputs:

| Given | Not given |
|---|---|
| The new evidence introduced at `Ti` | Any evidence from `Tj > i` |
| The arm's current artefact, as of `Ti-1` | Any task, oracle or scoring rule |
| The arm's format instruction | Any statement about future relevance |

Output: the arm's maintenance file for that checkpoint, written to `state/<ARM>/<SCENARIO>/t<NN>.json`. The harness folds `t0..ti` to obtain the arm's state at `Ti`.

**A maintainer may decide to change nothing.** An empty op list is a legitimate, recorded decision that costs one action's worth of attention and no edits. Drift is supposed to be possible.

## 5. Epoch transitions

When a scenario transitions between epochs (Foundation → Growth at t5, Growth → Maturity at t10), the maintainer receives an "epoch transition" evidence bundle documenting:

1. Which prior decisions remain valid
2. Which prior decisions are deprecated (but still findable)
3. New epoch-specific rules
4. Cross-epoch constraints that remain binding

The maintainer must track this. Deprecated-but-findable facts are traps. A decision valid in Foundation may be reversed in Growth. A constraint introduced in Foundation may still bind in Maturity.

### 5.1 Epoch transition evidence format

```json
{
  "epoch_transition": {
    "from_epoch": "foundation",
    "to_epoch": "growth",
    "checkpoint": 5,
    "valid_decisions": ["s1-adr001", "s1-adr003"],
    "deprecated_decisions": ["s1-adr002"],
    "new_rules": ["s1-adr004"],
    "binding_constraints": ["s1-constraint-pii"]
  }
}
```

## 6. File formats

### B1 — repository-native state documents

```json
{
  "evidence_bytes_seen": 4120,
  "files": [
    { "path": "CURRENT_STATE.md", "body": "..." },
    { "path": "AGENTS.md", "body": "..." }
  ]
}
```

Each entry replaces that path wholesale. Omitting a path leaves the previous version standing — which is how a repository document goes stale, and is deliberately possible.

### B4 — maintained wiki

```json
{
  "evidence_bytes_seen": 4120,
  "wiki": "# Beacon — current state\n..."
}
```

One page, replaced wholesale. Omitting `wiki` leaves the previous page unchanged.

### B5 — Fehrest memory operations

```json
{
  "evidence_bytes_seen": 4120,
  "memories": [
    { "op": "add", "id": "s1-adr002", "statement": "...", "mtype": "Decision",
      "project": "beacon", "valid_from": 21, "supersedes": ["s1-adr001"] },
    { "op": "supersede", "id": "s1-adr001", "valid_until": 21 },
    { "op": "conflict", "id": "s1-retention-a" },
    { "op": "retract", "id": "s1-guess" }
  ]
}
```

`mtype` is one of `Fact`, `Decision`, `Constraint`, `Gotcha`, `State`.

**There is no `basis` field and there will not be one.** `Basis` is core-assigned; every maintainer-written memory is `AgentAsserted`. A maintainer cannot mint `UserAsserted` or `UserConfirmed`, and K-21 asserts that invariant independently of this benchmark.

### 6.1 The adapter is not part of Fehrest

Phase T has **no agent-facing memory-write surface** — the CLI writes canonical objects, not memories. The harness applies these ops through the Rust library.

That adapter is benchmark tooling. It is not evidence that Fehrest has a maintenance interface, and because a real B5 maintainer would have to pay for whatever interface eventually exists, **B5's measured maintenance cost is a lower bound, not an estimate.** This is stated in the protocol too, because it is the kind of caveat that gets dropped when a number is quoted.

## 7. What is counted

| Metric | Definition |
|---|---|
| `MAINTENANCE_ACTIONS` | Discrete edits: one per file write, one per memory op |
| `MAINTENANCE_INPUT_BYTES` | Evidence bytes the maintainer was shown |
| `MAINTENANCE_OUTPUT_BYTES` | Bytes the maintainer wrote |
| `FILES_OR_OBJECTS_TOUCHED` | Distinct artefacts created or modified |
| `MAINTENANCE_MODEL_TOKENS` | Input and output tokens, from the runner |
| `MAINTENANCE_WALL_TIME` | Seconds per session, from the runner |
| `MANUAL_DECISIONS_REQUIRED` | Interventions a human had to make |
| `ERRORS_INTRODUCED` | Maintainer-written claims contradicting the evidence it was shown |
| `STALE_STATE_LEFT_BEHIND` | Claims still asserted as current after their evidence was superseded |
| `EPOCH_TRANSITIONS_MISSED` | Deprecated decisions not removed at epoch boundaries |

The last three are **outcomes of maintenance, not costs**, and are reported separately. An arm that is cheap to maintain because its maintainer skips work will show that in `STALE_STATE_LEFT_BEHIND` and `EPOCH_TRANSITIONS_MISSED`, and the figures must be read together.

`ERRORS_INTRODUCED` and `STALE_STATE_LEFT_BEHIND` are adjudicated against the evidence the maintainer was shown — **never** against the oracles, which the adjudicator does not see.

## 8. Drift is a result, not a bug

If B4's maintainer forgets to remove a superseded decision at `T3` and a task at `T3` punishes it, that is the benchmark working. It is the exact cost V0 assumed away.

Equally: if B5's maintainer writes a memory with a wrong `valid_from`, or forgets to supersede a record, B5 pays for it. **Neither arm gets a corrected artefact after a task is scored.**

### 8.1 Epoch drift

If B4's maintainer fails to remove a deprecated decision at an epoch transition, and a task in the new epoch punishes it, that is the benchmark working. Epoch transitions are not free passes — they require active maintenance.

## 9. Handling a maintenance failure

| Situation | Handling |
|---|---|
| Maintainer produces malformed JSON | Retry **once** with the identical prompt. A second failure is recorded as a maintenance failure and the checkpoint's state is left unchanged |
| Maintainer refuses the task | Recorded as `MANUAL_DECISIONS_REQUIRED += 1`; the checkpoint's state is left unchanged |
| Harness defect discovered mid-run | The batch is invalidated. See the post-result modification policy in PREREGISTRATION-V2.md §31 |

A retry is a **cost**, not a repair: it counts toward that arm's maintenance actions.

## 10. Why B5 could lose this

Recorded now, so the loss is legible if it happens:

- B5's maintenance is **structured**: every memory needs a type, a scope, a valid-from, and supersession edges maintained by hand. B4's maintenance is "edit a paragraph". If the structure costs three times as much to keep correct and buys one extra correct task, B4 wins on the metric that matters.
- Structured maintenance has **more ways to be wrong**. A missing supersession edge is invisible until a task hits it; a stale sentence in a wiki is at least legible to a human reader.
- B5's envelope overhead consumes budget. Under 6,000 bytes it fits fewer items than B4's distilled page, so if the deciding item is the one that did not fit, B5 loses a task B4 wins.
- Epoch transitions add complexity. B5 must track which memories are valid in which epochs, and update `valid_from`/`valid_until` accordingly. B4 just edits text.

These are the mechanisms by which the thesis fails. They are written down before execution so that observing them counts as a prediction met, not as an excuse found.

## 11. V1 maintenance relationship

The R1-v1 maintenance protocol is preserved as historical evidence. This v2 protocol extends it with epoch-transition handling. The v1 protocol and its findings are not overwritten.
