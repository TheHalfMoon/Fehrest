# Benchmark Pre-Registration — Phase T

`PRE_REGISTERED_AT: 2026-08-18` · `BEFORE_ANY_RESULT_WAS_OBSERVED: YES`

This document is written **before** the harness runs. Everything it fixes —
metrics, arms, scoring rules, fixture composition, and the predictions — is fixed
now so that nothing can be adjusted after seeing which way the numbers fall.

> **Failure of the thesis is an acceptable and valuable result.** If the arms come
> back showing Fehrest does not beat a maintained wiki, that is the finding, and it
> gets reported as the finding. No fixture will be re-tuned, no query re-worded, and
> no arm re-weighted after results are seen.

---

## 1. What this harness measures — and what it does not

**It measures context adequacy: does the context an arm hands to an agent contain
what is needed to answer correctly, and does it contain stale or out-of-scope
material presented as current?**

**It does not measure the thesis.** The product thesis is about an *agent's*
continuation correctness. That requires executing a language model on each arm's
context, which **did not happen** and is recorded as `PENDING_MODEL_EXECUTION`.

The relationship between the two is one-directional and worth stating precisely:

| | |
|---|---|
| Context lacks the answer | No agent can reliably produce it. Adequacy is **necessary** |
| Context contains the answer | An agent may still get it wrong. Adequacy is **not sufficient** |

So a strong adequacy result is **not** thesis support; it only means the thesis has
not yet been falsified at the retrieval layer. A weak adequacy result **is**
meaningful negative evidence, because it falsifies a necessary condition.

`THESIS_STATUS` after this harness runs will be `NOT_EVALUATED` regardless of the
numbers. That is fixed now, in advance, so a good adequacy result cannot be quietly
promoted into a thesis claim later.

---

## 2. Arms

Each arm produces a context string under an identical byte budget for an identical
query. The agent-facing budget is **4,000 bytes** for every arm — no arm gets more
room than another.

| Arm | Name | Context construction |
|---|---|---|
| **B0** | Plain agent | Empty context. The floor |
| **B1** | Repository-native docs | Every corpus document concatenated in path order, cut at budget |
| **B3** | Lexical retrieval | FTS5 top-k over the same corpus, ranked by relevance, cut at budget. **Raw document text only** |
| **B4** | Maintained LLM wiki (Karpathy) | A single hand-maintained, fully current distilled page. **The bar that matters most** |
| **B5** | Fehrest Core | Compiled context package: envelopes, temporal labels, scope filter, contradiction section, served-item manifest |

### 2.1 B4 is built to win, not to lose

B4 is the strong baseline and the honest comparison. The wiki in `fixtures/wiki.md`
is written to be **completely current and correct as of the present**: every
superseded decision already replaced by its successor, every constraint stated
plainly, nothing stale left in it.

This is the *most generous possible* assumption for the baseline — a wiki maintained
with perfect diligence and zero lag. Real wikis drift. Giving B4 a perfect one means
any Fehrest advantage that survives is an advantage over the best case, not over a
strawman.

**Prediction, recorded now: B4 should beat or tie B5 on current-state queries.** That
is what a maintained wiki is for. If it does not, the fixture is suspect and I will
say so rather than claim a win.

### 2.2 No Fehrest metadata leaks to baselines

B0, B1, B3 and B4 see **document text only**. They never receive: envelope headers,
trust levels, `basis` / `verification` / `lifecycle` / `resolution` axes, temporal
labels, supersession edges, scope selectors, the manifest, or any memory record.
The harness asserts this at runtime — `assert_no_fehrest_metadata` fails the run if a
baseline context contains any envelope marker. A leak invalidates the comparison, so
it is checked rather than assumed.

---

## 3. Query classes and ground truth

Six classes, chosen because each isolates one dimension the architecture claims to
handle. Ground truth is written by hand in `fixtures/queries.json`, **before** any
arm runs, and is not derived from any arm's output.

| Class | What it isolates | Correct behaviour |
|---|---|---|
| `CURRENT` | Plain current-state recall | Return the current answer |
| `SUPERSEDED` | A reversed decision where the *old* one is discussed at greater length | Return the new answer; the old one must not appear as if current |
| `HISTORICAL` | Truth at a past point in time | Return what was true then |
| `SCOPE` | A constraint that belongs to project A only | Answering for project B must not surface it |
| `CONTRADICTION` | Two active, inseparable claims | Surface the conflict; do not silently pick |
| `ABSENT` | Nothing in the corpus answers | Abstain |

### 3.1 Scoring — fixed now

Per query, per arm, the context is scored:

| Field | Definition |
|---|---|
| `contains_correct` | Every token in the query's `must_contain` list appears in the context |
| `contains_stale` | Any token in `stale_tokens` appears in the context |
| `stale_is_labelled` | Every occurrence of a stale token is accompanied, within the same item, by a marker identifying it as superseded, historical or out-of-scope |
| `misleading` | `contains_stale && !stale_is_labelled` |
| `bytes` | Length of the context in bytes |

**Primary metric, `ADEQUATE`:**

| Class | `ADEQUATE` is true when |
|---|---|
| `CURRENT`, `SUPERSEDED`, `HISTORICAL`, `SCOPE` | `contains_correct && !misleading` |
| `CONTRADICTION` | Both contending claims present **and** the conflict marked |
| `ABSENT` | `!contains_stale` — the context must not offer a confident-looking wrong answer |

`ABSENT` is deliberately scored on what the context *lacks*. An arm cannot win it by
retrieving something plausible; only by retrieving nothing misleading.

**Secondary metric:** `MISLEADING_RATE` — the share of queries where the arm supplies
stale or out-of-scope material with nothing marking it as such. This is tracked
separately because handing an agent a confidently wrong answer is a different and
worse failure than handing it nothing.

### 3.2 Fehrest can lose these

Recorded in advance, so the losses are legible when they happen:

- On `CURRENT`, B4's single curated paragraph may be more compact than B5's envelope
  overhead, and B5 spends bytes on metadata that B4 does not.
- On `ABSENT`, B0 wins trivially — an empty context is never misleading. B0 is
  expected to score 1.0 on this class and 0.0 on every other. That is not a defect in
  the benchmark; it is the shape of the floor.
- B5's envelope overhead means it fits fewer items in the same budget. If the answer
  is in the item that did not fit, B5 loses a query that B1 or B3 wins.

---

## 4. Sample size — explicitly NOT a powered study

`SAMPLE_SIZE_STATUS: PILOT_ONLY_NOT_POWERED`

The fixture holds a small hand-built corpus and a small hand-built query set. **This
is a pilot, not a powered experiment**, and no significance test will be computed
from it.

A final sample size requires a power analysis, and a power analysis requires an
effect-size estimate that does not exist yet — no prior run of this comparison has
been made. Inventing a sample size now would be inventing the number the founder's
directive forbids inventing. The correct order is: pilot → observed effect size →
power analysis → final N. This document covers the pilot only.

Consequently the results section will report **counts and proportions, with no
p-values, no confidence intervals, and no claim of significance.**

---

## 5. Fixture-tuning prohibition

After the first run:

- No document may be added, removed or reworded.
- No query may be added, removed or reworded.
- No `must_contain` or `stale_tokens` list may be edited.
- No budget may be changed.
- No arm may be added or dropped.

If a defect in the *harness* (not the fixture) is found — a scoring bug, a leak in
the metadata assertion — it may be fixed, and the fix must be recorded in the results
document along with the pre-fix numbers. Any change to the *fixture* invalidates the
pre-registration and requires a new one, clearly marked as a second registration with
the first one's results already known.

---

## 6. What a negative result looks like

Stated now so it cannot be reinterpreted later:

- **If B4 matches or beats B5 across all six classes**, the thesis is not supported
  at the retrieval layer, and the correct conclusion is that a maintained wiki is
  sufficient and Fehrest's additional machinery does not earn its complexity.
- **If B5 wins only on `CURRENT`**, the thesis is not supported — that is the class a
  wiki already covers, and winning it proves nothing about temporal reasoning.
- **If B5's advantage appears only on classes with a single query each**, the result
  is too thin to mean anything and will be reported as inconclusive rather than
  positive.

None of these outcomes will be answered by adding features. The directive is explicit
and is restated here: **do not rescue a failed thesis.**
