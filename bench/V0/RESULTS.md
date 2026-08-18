# Benchmark Results — Phase T Context-Adequacy Pilot

```
THESIS_STATUS:            NOT_EVALUATED (PENDING_MODEL_EXECUTION)
ADEQUACY_PILOT_VERDICT:   INCONCLUSIVE — TOO THIN TO SUPPORT THE THESIS
SAMPLE_SIZE_STATUS:       PILOT_ONLY_NOT_POWERED
FIXTURE_TUNED_AFTER_RESULTS: NO
HARNESS_CORRECTED_AFTER_RESULTS: YES — 3 corrections, all recorded below
```

The verdict is `INCONCLUSIVE` **by the rule pre-registered before any result was
seen**, not by later interpretation. [PRE-REGISTRATION.md §6](./PRE-REGISTRATION.md)
states:

> If B5's advantage appears only on classes with a single query each, the result is
> too thin to mean anything and will be reported as inconclusive rather than positive.

Every class in this pilot has exactly one query, and B5's entire margin over the
strongest baseline is one query. The rule applies. It is applied.

---

## 1. Results as measured

| Query | Class | B0 | B1 | B3 | B4 | B5 |
|---|---|---|---|---|---|---|
| Q1 | `CURRENT` | — | OK | OK | OK | OK |
| Q2 | `SUPERSEDED` | — | — | — | OK | OK |
| Q3 | `HISTORICAL` | — | — | — | OK | OK |
| Q4 | `SCOPE` | — | OK | OK | OK | OK |
| Q5 | `CONTRADICTION` | — | — | — | OK | OK |
| Q6 | `ABSENT` | OK | — | OK | — | OK |

| Arm | Adequate | Misleading | Mean bytes |
|---|---|---|---|
| **B0** plain agent | 1/6 | 0/6 | 0 |
| **B1** repo-native docs | 2/6 | 2/6 | 2,805 |
| **B3** lexical retrieval | 3/6 | 2/6 | 2,624 |
| **B4** maintained wiki | **5/6** | 0/6 | 1,370 |
| **B5** Fehrest Core | **6/6** | 0/6 | 3,249 |

Raw output: [results.txt](./results.txt).

---

## 2. Why this is not a win

**B5 beats B4 by exactly one query — Q6, the `ABSENT` class. B0, the do-nothing
baseline, also scores that query.**

That single fact carries most of the interpretation:

1. **The margin is one observation.** One query is not evidence of a capability
   difference. It is evidence that one query behaved a certain way once.
2. **The margin is on a class the empty arm also wins.** `ABSENT` is scored on what
   the context *lacks*. B5 passes because scope filtering removed the edge-project
   material; B0 passes because it has no material at all. The pre-registered metric
   cannot distinguish *precision* from *emptiness* — and a metric that scores the
   do-nothing baseline identically to the system under test is not measuring the
   system under test.
3. **B4 is not far behind on anything else.** A perfectly maintained wiki matched
   Fehrest on `CURRENT`, `SUPERSEDED`, `HISTORICAL`, `SCOPE` and `CONTRADICTION` —
   including the two classes the architecture treats as its distinguishing claims.
4. **B5 costs 2.4× the bytes of B4** for that result (3,249 vs 1,370 mean). Envelope
   metadata is not free, and under a tighter budget B5 would fit fewer items.

**The honest reading: this pilot does not distinguish Fehrest from a well-maintained
wiki.** It shows Fehrest is not *worse*, and it shows both are far better than raw
docs or lexical retrieval. Neither of those is the thesis.

### 2.1 The comparison's largest blind spot

B4's wiki was written to be **perfectly current, with zero maintenance lag**. That
was deliberate and correct as a baseline choice — beating a strawman proves nothing.
But it means the pilot silently assumes away the thing Fehrest's thesis is mostly
about: **the cost of keeping the wiki perfect.**

Fehrest's memories in this harness were also hand-written. So both arms assume a
diligent maintainer, and **maintenance cost was not measured for either.** A
benchmark in which the baseline never drifts cannot detect an advantage that only
appears when it does.

`MAINTENANCE_COST: NOT_MEASURED`. This is the single most important gap in the pilot,
and it is not fixable by adding queries — it needs a different experimental design
in which the corpus evolves and the wiki is updated by a realistic process rather
than by fiat.

---

## 3. Corrections made after seeing results

Three. The pre-registration permits **harness** fixes with pre-fix numbers recorded,
and prohibits **fixture** changes. No document, query, token list or budget was
touched. All three are recorded here with the numbers they changed, because a
correction disclosed only when it flatters the result is not a correction.

| # | What | Direction | Legitimate? |
|---|---|---|---|
| 1 | Emitted `section=` on the wire | **Helped B5** | Spec-conformance fix — see below |
| 2 | B3 stopped feeding whole sentences to an implicit-AND FTS matcher | **Helped B3** | Harness defect: the arm was a strawman |
| 3 | Scope headings counted as labels | **Helped B4, B1, B3** | Scoring defect biased toward Fehrest's formatting |

**Progression of B5 vs B4 across the three corrections:**

| Stage | B0 | B1 | B3 | B4 | **B5** | Snapshot |
|---|---|---|---|---|---|---|
| Initial run | 1/6 | 1/6 | 1/6 | 4/6 | **5/6** | [results-prefix.txt](./results-prefix.txt) |
| After fixes 1–2 | 1/6 | 1/6 | 2/6 | 4/6 | **6/6** | [results-fix2.txt](./results-fix2.txt) |
| After fix 3 (final) | 1/6 | 2/6 | 3/6 | **5/6** | **6/6** | [results.txt](./results.txt) |

Note the direction of travel: the corrections moved the baselines **up**, from 4/6 to
5/6 for B4 and 1/6 to 3/6 for B3, and narrowed B5's margin from two queries to one.
Two of the three defects were biased in Fehrest's favour, which is why they were
looked for.

### 3.1 Correction 1 — was it thesis rescue?

This one deserves scrutiny, because it is the only correction that helped B5, and it
was made after B5 failed Q5.

**Judgement: conformance, not rescue.** The reasoning, so a reviewer can disagree:

- The gap is against `H §3` of the frozen architecture, which specifies a
  **sectioned** output and states that `contradictions` is a section precisely so the
  agent is told "these two memories conflict and Fehrest cannot decide." That
  requirement predates this benchmark by four phases.
- The implementation had `section` in the manifest but not on the wire. The manifest
  is not shown to the model, so the requirement was unmet.
- **The fix is general.** Every item now carries its section, not only contradictions.
  A change that labelled only the failing case would have been rescue, and was not
  made.
- It is covered by an acceptance-test assertion that stands independently of the
  benchmark ([tests/integration.rs](../../tests/integration.rs), AS-3).

**Reversal condition:** if a reviewer judges that `H §3`'s sectioning applies only to
the manifest and not to model-visible output, then correction 1 is rescue, B5's Q5
result reverts to a failure, and B5 finishes **5/6 — tied with B4**. The conclusion
of this document does not change under that reading: it is `INCONCLUSIVE` either way.

---

## 4. What each arm's failures actually show

| Arm | Failed | Pattern |
|---|---|---|
| **B0** | Q1–Q5 | The floor behaves like the floor. Wins `ABSENT` trivially, because nothing can mislead |
| **B1** | Q2, Q3, Q5, Q6 | Concatenation preserves everything including the superseded ADR, which is 4× longer than its replacement. Two queries received stale material with no label |
| **B3** | Q2, Q3, Q5 | Lexical relevance has no notion of time. It retrieves the longer, better-matching, **wrong** ADR |
| **B4** | Q6 | A single curated page cannot say what it does not cover |
| **B5** | none | See §2 before reading anything into this |

The B1/B3 failures are the clearest signal in the pilot, and they are **not** about
Fehrest: retrieval that ranks by lexical relevance surfaces the superseded decision
because the superseded decision is discussed at greater length. That is a real
property of real repositories, and it is why `SUPERSEDED` and `HISTORICAL` were
included as classes.

---

## 5. What was not measured

1. **The thesis.** No language model ran on any arm's context. Agent continuation
   correctness — the actual product claim — is `PENDING_MODEL_EXECUTION`.
2. **Maintenance cost** (§2.1). The most consequential omission.
3. **Latency.** Nothing was timed. Any future timing must come from a release binary;
   the release build requires a target directory outside the OneDrive-synced repo
   path (see [verification.md](../../specs/001-headless-rust-fehrest/verification.md)).
4. **Scale.** Seven documents, nine memories, six queries. Nothing here says how any
   arm behaves at a thousand documents.
5. **Statistical significance.** Not computed and not computable from n=1 per class.
   No p-value, no confidence interval, no claim.
6. **B2 and B-12.** B2 was never defined in the arm list. B-12's incremental-vs-fresh
   comparison **cannot run** — incremental reindex is `YAGNI_DEFERRED`, recorded as a
   consequence at decision time rather than discovered here.

---

## 6. Conclusion

**The product thesis is neither supported nor falsified by this work.** It was not
tested. What was tested is a necessary precondition, and the precondition holds —
Fehrest's compiled context contained the correct answer, with stale material labelled,
on all six pilot queries.

That is worth exactly what it is worth: Fehrest has not been falsified at the
retrieval layer, on six hand-built queries, against a wiki that never drifts.

**No feature will be added in response to this result.** The pilot's weakness is
experimental design, not missing capability, and the correct next step is a better
experiment — a corpus that evolves over time, a baseline wiki maintained by a
realistic process rather than by fiat, enough queries per class for an effect size to
mean something, and an actual model executing the continuation tasks.

Building more of Fehrest to improve this number would be rescuing a thesis that has
not yet been tested. The directive is explicit, and it is followed here:
**do not rescue a failed thesis** — and equally, do not promote an untested one.
