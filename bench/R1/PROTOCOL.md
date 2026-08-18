# R1 — Longitudinal Continuation Benchmark: protocol

```
BENCHMARK_ID:      R1
SUPERSEDES:        nothing. V0 asked a different question and is sealed, not replaced
RESEARCH_QUESTION: when a project evolves over time, can a fresh agent continue the
                   work more correctly with Fehrest than with strong simpler context
                   strategies, at a justifiable total maintenance + context cost?
NOT:               a retrieval benchmark
```

V0 measured whether an arm's context *contained* an answer. R1 measures whether a
fresh agent *continues the work correctly*, and what it costs to keep each arm's
context correct while the project changes underneath it.

The two defects that ended V0 are the two things R1 is built around:

| V0 defect | What R1 does |
|---|---|
| The deciding metric scored the empty arm identically to the treatment | No arm is empty. The primary metric cannot be satisfied by silence, on any task type |
| `MAINTENANCE_COST: NOT_MEASURED` — both maintained arms were hand-authored perfectly current | Maintenance is a measured, task-blind, prospective process. Nobody gets a free perfect update |

---

## 1. Corpus — three independent evolving projects

| Scenario | Domain | Checkpoints | Evidence items |
|---|---|---|---|
| **S1 Beacon** | Telemetry ingestion service | 10 (t0–t9, days 0–63) | 15 |
| **S2 Marisol** | Clinical-trial data pipeline | 9 (t0–t8, days 0–80) | 11 |
| **S3 Harbor** | Documentation migration | 9 (t0–t8, days 0–72) | 10 |

Each scenario evolves through timestamped checkpoints and carries, between them, the
phenomena a long-running project actually produces:

initial requirements · later requirements · superseded decisions · project-local
exceptions · organisation-wide defaults · failed experiments · corrected failures ·
renames and moves · conflicting notes · genuinely unresolved conflicts · completed
work · current open work · historical states · known gotchas · irrelevant noise ·
stale summaries · trustworthy current evidence.

Not every event is adversarial. Standup notes about a broken coffee machine and a
dead office plant are in the corpus because real repositories contain them and an
arm that cannot ignore noise is not a useful arm.

**Two traps are deliberately quiet.** S1's `docs/onboarding-summary.md` is a stale
summary that still says "Kafka" and still points at the old repository path; nothing
marks it as stale, exactly as nothing marks the real ones. S1's day-14 experiment
write-up is correct history that becomes misleading if read as current.

Source of truth: `scenarios/*.scn`, one file per scenario, parsed by the harness and
materialised into a vault per checkpoint.

## 2. Checkpoints and the temporal boundary

At checkpoint `Ti` the project consists of exactly the evidence introduced at `t ≤ i`.
**No arm may access information from `Tj > i`, and no maintainer may either.**

This is enforced by construction rather than by filtering: the harness builds a fresh
vault per checkpoint containing only the visible evidence. It is then *verified*
independently — the instrument pilot computes the vocabulary that appears only in
future evidence and asserts none of it occurs in any arm's package.

That check subtracts each arm's **structural vocabulary**, defined as the words the
arm emits at `t0` before any later evidence exists. Section labels and envelope
attributes are output format, not knowledge of the future. Without that subtraction
the check produces false positives on B5, whose compiler emits a `current_decisions`
section label unconditionally — a defect the instrument pilot found and which is
recorded in [PILOT.md](./PILOT.md).

## 3. Tasks — 30 continuation tasks across 11 classes

Tasks require an **action**, not a definition. The output contract asks what you would
do, not what a term means.

| Class | Tasks | What it isolates |
|---|---|---|
| `NEXT_ACTION` | 3 | Selecting the correct next step from a long history |
| `SUPERSESSION_AVOIDANCE` | 6 | Not acting on a decision that has been replaced |
| `CONSTRAINT_RETENTION` | 5 | Honouring a requirement introduced many checkpoints earlier |
| `FAILED_APPROACH_AVOIDANCE` | 5 | Not repeating a known failed approach |
| `HISTORICAL_REASONING` | 2 | Operating under what was true at an earlier point |
| `CONTRADICTION_HANDLING` | 2 | Surfacing a conflict instead of silently picking |
| `ABSTENTION` | 2 | Declining to invent an answer that does not exist |
| `IDENTITY_CONTINUITY` | 2 | Following an object across rename and move |
| `SCOPE_RESOLUTION` | 2 | Applying a project-local rule without globalising it |
| `PROVENANCE` | 1 | Naming the evidence an action requires |
| `CURRENT_STATE_CONTINUATION` | 1 | Acting on brand-new evidence |

### 3.1 Tasks are issued mid-history, not only at the end

**8 of the 30 tasks are issued before their scenario ends**, at `t1`, `t2`, `t3`, `t4`,
`t5` and `t6`.

This is not decoration. A benchmark whose every task sits at the final checkpoint
cannot test maintenance lag, staleness or knowledge decay, because there is no future
for an arm to be stale relative to — the arm is asked only about a project that has
stopped moving. The first draft of R1 had exactly that defect and the instrument
pilot's non-vacuity control caught it; the harness now **asserts** that at least one
task is issued before its scenario ends, and fails if that stops being true.

### 3.2 Paired tasks in opposite directions

Several tasks are deliberately inverted against each other so that no single strategy
wins both:

| Pair | Same question, opposite correct answer |
|---|---|
| `S1-B` (t9) / `S1-G` (t9, as of day 14) | Broker is Redpanda now; was Kafka then |
| `S2-B` (t8) / `S2-G` (t8, as of day 30) | Partition key is protocol now; was site then |
| `S1-L` (t3) / `S1-B` (t9) | Same answer at the moment of change and six checkpoints later |
| `S3-H` (t4) / `S3-D` (t8) | Same constraint, tested for freshness then for retention |
| `S1-E` (t9) / `S1-M` (t6) | Refuse to export a local exception; refuse to globalise it |

An arm that only knows the present fails the historical tasks. An arm that only
preserves history fails the current-state tasks. An arm with a maintenance lag of one
checkpoint fails the freshness tasks specifically.

## 4. Arms

Every arm receives the same **6,000-byte** context budget. No arm gets more room.

| Arm | Construction | Maintained |
|---|---|---|
| **B-NULL** | Task prompt only, no project context. **Calibration, not a comparison arm** | no |
| **B0** | Plain project files, **newest checkpoint first**, cut at budget | no |
| **B1** | Repository-native state documents, then the project files underneath | **yes** |
| **B3** | Lexical retrieval through the real FTS index, ranked by distinct term hits, recency-tiebroken. Raw document text only | no |
| **B4** | The maintained wiki page, and nothing else | **yes** |
| **B5** | Fehrest compiled context package at the checkpoint's valid time | **yes** |

### 4.1 B-NULL exists to detect bad tasks

If B-NULL scores on a task, that task is answerable from the prompt alone and is
measuring nothing about context. B-NULL's result is a **task-validity signal**; it is
never reported next to the comparison arms as though it were competing with them.

This also repairs the specific V0 defect. In V0 the floor was an empty context, which
won the deciding class trivially because the metric rewarded emptiness. Here the floor
is the actual project, which can mislead like any other arm, and the empty condition
has been demoted to a calibration instrument.

### 4.2 B0 is ordered by recency on purpose

Path-order concatenation would have made B0 needlessly weak. Recency is the strongest
simple heuristic available at zero maintenance cost, and it is what an engineer
dropped into an unfamiliar repository actually does. **A weakened baseline is not a
baseline.**

### 4.3 B4 must stay strong

The maintained wiki is the comparison that matters. It is not weakened because it
came close in V0. What changes is that it can no longer be written retrospectively
with knowledge of the questions: it is maintained forward in time, task-blind, and
its maintenance is counted.

**R1 must be able to conclude that a maintained wiki is enough.** If it cannot reach
that conclusion in principle, it is biased and its result is worthless.

### 4.4 No metadata reaches a baseline

B0, B1, B3 and B4 see document text only — never envelope headers, trust levels,
lifecycle axes, temporal labels, supersession edges, scope selectors, manifests or
memory records. The harness asserts this on every generated package and the assertion
has a negative control proving it fires.

## 5. Maintenance

Specified in full in [MAINTENANCE.md](./MAINTENANCE.md). The three properties that
matter:

1. **Same evidence, same time.** At each checkpoint every maintained arm's maintainer
   receives the identical new-evidence bundle, and nothing from the future.
2. **Task-blind.** The maintainer never sees a task, never learns which facts will be
   scored, and is never told that anything will matter later.
3. **Counted.** Actions, objects touched, input bytes, output bytes and model tokens
   are recorded per checkpoint per arm.

B0 and B3 have zero maintenance cost beyond ordinary project work. **That is a real
advantage and it is allowed to win.** A simpler baseline that performs nearly as well
at a fraction of the upkeep legitimately defeats the Fehrest thesis.

### 5.1 Fehrest has no agent-facing memory-write surface

Phase T's CLI exposes `init`, `add`, `scan`, `rebuild`, `search`, `read`, `compile`,
`manifest`, `events`, `verify`. **None of them writes a memory.** Memories exist only
through the Rust library API.

So B5's maintainer cannot drive Fehrest directly. It emits a structured maintenance
instruction that the R1 harness applies through the library. That adapter is benchmark
tooling and **is not part of Fehrest**, and it must not be read as evidence that
Fehrest has a maintenance interface.

This is a finding, not a workaround: a system whose upkeep requires an adapter that
does not exist yet has a maintenance cost this benchmark **cannot fully observe**, and
B5's measured maintenance cost is therefore a **lower bound**. Recorded here so the
result is read with it rather than around it.

`Basis` is core-assigned and the maintenance schema has no field for it. Every
maintainer-written memory is `AgentAsserted`. A maintainer cannot mint user authority;
K-21 asserts that invariant independently.

## 6. Primary outcome

**`CONTINUATION_CORRECT`**, binary per task, defined before any result exists:

```
substantive := non-whitespace length of ACTION >= min_action_chars
require_ok  := every require_all entry matches its named output field
forbid_ok   := no forbid entry matches its named output field
abstain_ok  := ABSTAIN == YES  if the task is an abstention task
               ABSTAIN != YES  otherwise

CONTINUATION_CORRECT := substantive && require_ok && forbid_ok && abstain_ok
```

Field-scoped matching matters: forbidding "Kafka" in `DECISION` punishes acting on the
superseded broker, while still allowing an arm to name it correctly under `EVIDENCE`
or `UNRESOLVED`. A whole-output match would punish accurate reasoning.

### 6.1 Silence earns nothing

The V0 metric gave the empty arm credit. This one cannot:

- An empty response parses to empty fields, so `substantive` is false and the score is
  0 on **every** task type.
- Abstention credit requires an explicit `ABSTAIN: YES` **and** a substantive `ACTION`.
  A bare `ABSTAIN: YES` scores 0.
- Prose that ignores the output contract scores 0.

All four cases are asserted in the instrument pilot against synthetic responses, and
the assertions have negative controls.

## 7. Secondary outcomes

Tracked separately and **never folded into the primary**:

`STALE_USE` · `FALSE_ABSTENTION` · `MISSED_ABSTENTION` · `CONFLICT_FLAGGED` ·
`PROVENANCE_GIVEN` · historical correctness · latency · maintenance cost.

**No composite score is computed.** A weighting was not preregistered, and inventing
one after seeing results is precisely what the protocol exists to prevent.

## 8. Cost

| Measured | Where |
|---|---|
| `MODEL_INPUT_TOKENS`, `MODEL_OUTPUT_TOKENS` | Per run, from the runner |
| `CONTEXT_BYTES`, `CONTEXT_ITEMS` | Per arm per checkpoint, from the harness |
| `COMPILE_LATENCY` | Release binary only, target path recorded |
| `MAINTENANCE_*` | Per checkpoint per arm, see [MAINTENANCE.md](./MAINTENANCE.md) |
| `STORAGE_GROWTH` | Arm artefact bytes over checkpoints |

**No accuracy figure for B5 may be reported without its cost alongside it.**

## 9. Model execution

Required. Not optional, and not substitutable.

- Fresh stateless session per run. No conversational memory crosses runs.
- Within a comparison batch: same model, same system instructions, same task prompt,
  same temperature and reasoning configuration, same tool permissions, same time
  limit, same output contract.
- **Only the context condition differs.** No arm gets a tool another arm lacks unless
  that tool is the treatment itself.
- Arms are executed under neutral identifiers. The strings "Fehrest", "wiki" and
  "baseline" do not appear in any model-visible prompt.
- Outputs are scored by a deterministic scorer with arm identity stripped.

`R1_MODEL_RUNNER: NONE_AVAILABLE` on this host — no API credential, no local runner.
See [STATUS.md](./STATUS.md). **The harness has no code path that fabricates a model
response.**

## 10. Pilot and confirmatory are separate

| | Instrument pilot | Confirmatory |
|---|---|---|
| Purpose | Find broken scoring, impossible tasks, ambiguous oracles, leakage, plumbing errors | Test the thesis |
| Establishes product success | **No. Never.** | Yes, or falsifies it |
| Status | **PASS** — 631 checks, [PILOT.md](./PILOT.md) | `NOT_STARTED` |

Confirmatory sample size requires a power analysis, which requires a variance estimate,
which requires model execution. It does not exist yet and **will not be chosen by
looking for the number that makes Fehrest significant.**

## 11. What Fehrest has to show

It does not need to win everything. A meaningful thesis needs evidence that the extra
structure buys something material — better continuation at similar cost, similar
continuation at much lower maintenance cost, better stale-decision avoidance at
acceptable cost, or accuracy that holds up better as project age and churn increase.

**If B4 gives essentially the same continuation quality at lower complexity and
reasonable maintenance cost, that is evidence against the current Fehrest thesis, and
it gets reported as evidence against.**

No feature will be added in response to any R1 result. `GRAPH=NO` `VECTORS=NO`
`AUTO_MEMORY=NO` `RERANKER=NO` `MCP=NO` `UI=NO`.
