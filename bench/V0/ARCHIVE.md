# PHASE_T_ADEQUACY_PILOT_V0 — sealed archive

```
ARCHIVE_ID:              PHASE_T_ADEQUACY_PILOT_V0
STATUS:                  NON_CONFIRMATORY
VERDICT:                 INCONCLUSIVE
PRODUCT_THESIS_EVIDENCE: NONE
THESIS_STATUS:           NOT_EVALUATED
MAINTENANCE_COST:        NOT_MEASURED
MODEL_EXECUTION:         NONE
SEALED_AT:               2026-08-18
SEALED_AGAINST:          90205c1ce7f4d5788fdb8808e0e69106487642fb (results as published)
REPRODUCED_AT:           Phase T-R1, byte-identically, after formatting and relocation
```

This directory is **closed**. It is kept for traceability, not for reuse. Nothing in
it may be edited to make it look better, and nothing in it may be cited as evidence
for or against the product thesis.

The primary documents are unchanged from the run:

| File | What it is |
|---|---|
| [PRE-REGISTRATION.md](./PRE-REGISTRATION.md) | Written before any result was seen. Fixes arms, classes, scoring and the negative-result rules |
| [RESULTS.md](./RESULTS.md) | The result and its interpretation, including the three post-observation corrections |
| [results-prefix.txt](./results-prefix.txt) | **Pre-fix** raw output — the first run, before any correction |
| [results-fix2.txt](./results-fix2.txt) | Raw output after corrections 1–2 |
| [results.txt](./results.txt) | Final raw output, after correction 3 |
| [fixtures/](./fixtures/) | The original corpus (7 documents), the original 6 questions with hand-written ground truth, and the B4 wiki |
| [harness.rs](./harness.rs) | The arm implementations and scorer |

---

## 1. Why this is sealed as non-confirmatory

The pilot asked whether an arm's **context** contains what is needed. The product
thesis is about whether an **agent continues work correctly**. Those are different
questions, and the pre-registration said so before the run:

> Adequacy is **necessary**. Adequacy is **not sufficient.**

No language model executed on any arm. `THESIS_STATUS: NOT_EVALUATED` was fixed in
advance precisely so a good adequacy number could not later be promoted into a
product claim. It is not promoted here.

## 2. The result, and the two facts that hollow it out

| Arm | Adequate | Misleading | Mean bytes |
|---|---|---|---|
| B0 plain agent | 1/6 | 0/6 | 0 |
| B1 repo-native docs | 2/6 | 2/6 | 2,805 |
| B3 lexical retrieval | 3/6 | 2/6 | 2,624 |
| **B4 maintained wiki** | **5/6** | 0/6 | **1,370** |
| **B5 Fehrest Core** | **6/6** | 0/6 | **3,249** |

### 2.1 Why B0 scoring the deciding query invalidates the interpretation

B5's entire margin over B4 is **one query** — Q6, the `ABSENT` class. **B0, the
empty-context floor, also scores that query.**

`ABSENT` is scored on what the context *lacks*: `ADEQUATE := !contains_stale`. B5
satisfies it because scope filtering removed the out-of-project material. B0 satisfies
it because B0 has no material at all. The metric therefore **cannot distinguish
precision from emptiness**, and on the single query that separates the treatment from
the strongest baseline, it assigns the treatment and the do-nothing floor the same
score for opposite reasons.

A margin that rests entirely on a metric which rewards the null arm identically is not
a capability difference. This is the specific reason the verdict is `INCONCLUSIVE`
rather than positive, and it is a defect of the **measurement**, not of any arm.

The pre-registration's §6 rule — *"if B5's advantage appears only on classes with a
single query each, the result is too thin to mean anything"* — applies independently
and reaches the same verdict. Every class held exactly one query.

### 2.2 Cost: B5 paid 2.4× for that margin

| | B4 | B5 | Ratio |
|---|---|---|---|
| Mean context bytes | 1,370 | 3,249 | **2.37×** |
| Adequate | 5/6 | 6/6 | +1 query |
| Misleading | 0/6 | 0/6 | tie |

Envelope metadata, temporal labels and the manifest are not free. Under a tighter
budget B5 fits fewer items, so the byte cost is not merely a reporting detail — it is
a mechanism by which B5 could lose queries B4 wins. The pilot never tested a tighter
budget.

### 2.3 `MAINTENANCE_COST: NOT_MEASURED` — the disqualifying gap

Both maintained arms were hand-authored to be perfectly current:

- **B4's wiki** was written fully up to date, with every superseded decision already
  replaced and zero maintenance lag.
- **B5's memories** were likewise hand-written, already carrying correct temporal and
  scope structure.

So both arms assumed a diligent, omniscient maintainer, and **neither arm's
maintenance was counted.** Fehrest's thesis is largely a claim about what it costs to
keep context correct as a project evolves. A benchmark in which the baseline never
drifts, and in which nobody pays for either arm's upkeep, has assumed away the thing
being claimed.

This is not fixable by adding queries to this fixture. It requires a different design,
which is why V0 is sealed rather than extended.

## 3. The three post-observation corrections

Recorded in full in [RESULTS.md §3](./RESULTS.md) and restated here so the archive is
self-contained. All three were **harness** changes; the pre-registration permits those
with pre-fix numbers recorded, and prohibits fixture changes. No document, query,
token list or budget was touched.

| # | Change | Direction | Basis |
|---|---|---|---|
| 1 | Emit `section=` on the model-visible wire, not only in the manifest | **Helped B5** | Conformance to `H §3` of the frozen architecture, which predates the benchmark by four phases. Applied to **every** item, not only the failing case |
| 2 | B3 stopped feeding whole sentences to an implicit-AND FTS matcher | **Helped B3** | The arm was a strawman; a lexical baseline that ANDs every word of a question retrieves nothing |
| 3 | Scope headings counted as labels by the scorer | **Helped B4, B1, B3** | Scoring defect that recognised only Fehrest's label formatting |

**Progression across corrections:**

| Stage | B0 | B1 | B3 | B4 | B5 | Snapshot |
|---|---|---|---|---|---|---|
| Initial | 1/6 | 1/6 | 1/6 | 4/6 | 5/6 | [results-prefix.txt](./results-prefix.txt) |
| After 1–2 | 1/6 | 1/6 | 2/6 | 4/6 | 6/6 | [results-fix2.txt](./results-fix2.txt) |
| After 3 | 1/6 | 2/6 | 3/6 | 5/6 | 6/6 | [results.txt](./results.txt) |

Two of the three corrections raised **baselines**, and the net effect narrowed B5's
margin from two queries to one.

### 3.1 Correction 1 is the one to distrust, and its reversal condition stands

It is the only correction that helped B5, and it was made after B5 failed Q5. The
argued basis is conformance, not rescue — the requirement is older than the benchmark,
and the fix is general rather than targeted at the failing case.

**Reversal condition, preserved:** if a reviewer judges that `H §3`'s sectioning
requirement binds only the manifest and not model-visible output, correction 1 is
rescue, B5's Q5 reverts to a failure, and **B5 finishes 5/6 — tied with B4.**

The verdict is `INCONCLUSIVE` under either reading. That is why the reversal condition
can be stated plainly instead of defended.

## 4. What V0 does establish

Two things, both narrow, both worth keeping:

1. **Lexical relevance has no notion of time.** B1 and B3 surfaced the superseded ADR
   unlabelled — B3 ranked it *above* its replacement, because the reversed decision is
   discussed at four times the length of the decision that replaced it. That is a real
   property of real repositories.
2. **Fehrest was not falsified at the retrieval layer** on six hand-built queries
   against a wiki that never drifts. A necessary precondition holds. It is not the
   thesis.

## 5. What V0 does not establish — restated so it cannot drift

1. Anything about agent continuation. No model ran.
2. Anything about maintenance cost. Not measured, for any arm.
3. Anything about latency. Nothing was timed.
4. Anything about scale. Seven documents, nine memories, six queries.
5. Any statistical claim. `n = 1` per class; no p-value, no interval, no significance.
6. That Fehrest beats a maintained wiki. It did not, in any sense this pilot can
   support.

## 6. Errata — changes made to this directory after the result

Two, both structural, both verified not to change any number.

**E-1 · Formatting (Phase T-R1).** `cargo fmt` was applied repository-wide, including
`harness.rs`. Verified by running the harness before and after and diffing against the
committed `results.txt`: **byte-identical both times.**

**E-2 · Relocation (Phase T-R1).** The pilot moved from `bench/` to `bench/V0/` to make
room for the R1 benchmark. Three mechanical changes were required:

- `harness.rs` fixture root: `bench/` → `bench/V0/`
- `Cargo.toml` bin: `fehrest-bench` → `fehrest-bench-v0`, path updated
- Relative links in `RESULTS.md` re-pointed one level up

Re-run after relocation and diffed against `results.txt`: **byte-identical.**

**No fixture, query, ground-truth token, budget, arm or scored number was changed by
either erratum.**

### Reproduction

```bash
cargo run --bin fehrest-bench-v0
```

Output must equal [results.txt](./results.txt) exactly. If it does not, the archive
has been disturbed and its numbers should not be cited.

### Seal

Digest over the sealed set — `fixtures/**`, `harness.rs`, `results*.txt` — computed as
`find | sort | xargs sha256sum | sha256sum`:

```
23f1f099ecf2cc89cf2496c660c563d6423321f92a95e922d4a2b96ee9a22f8e
```

| File | sha256 (first 16) |
|---|---|
| `fixtures/corpus/adr-0001-datastore.md` | `521dd72ab22eeef7` |
| `fixtures/corpus/adr-0007-datastore-reversal.md` | `23184afc7c11d731` |
| `fixtures/corpus/constraints-core.md` | `d541400521bb3a98` |
| `fixtures/corpus/constraints-edge.md` | `d2dffc10c23a264a` |
| `fixtures/corpus/deploy-debate-a.md` | `618ebec28f7c95d1` |
| `fixtures/corpus/deploy-debate-b.md` | `b7c8a73af8a0444f` |
| `fixtures/corpus/gotcha-index-rebuild.md` | `b8c86064d37c90b6` |
| `fixtures/queries.json` | `369a4ceb3f2ef0a2` |
| `fixtures/wiki.md` | `a325c5a8f73e8911` |
| `harness.rs` | `54a499ffdab2153b` |
| `results-prefix.txt` | `9729fd7613948231` |
| `results-fix2.txt` | `06f9cf7841663166` |
| `results.txt` | `e56babab0c654326` |

## 7. What replaces it

[bench/R1/](../R1/) — a longitudinal continuation benchmark with an evolving corpus,
prospectively maintained baselines under a temporal evidence boundary, measured
maintenance cost, and actual model execution as a precondition for any thesis claim.

R1 exists because of §2.1 and §2.3 of this document, not in spite of them. **No Fehrest
capability was added in response to this result**, and none may be: the pilot's weakness
is experimental design, and building features to raise a number that was never
measuring the thesis would be rescuing a thesis that has not yet been tested.
