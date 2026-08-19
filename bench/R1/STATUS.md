# R1 — status

```
R1_PROTOCOL_STATUS:            COMPLETE
R1_CORPUS_STATUS:              COMPLETE -- 3 scenarios, 28 checkpoints, 36 evidence items
R1_MAINTENANCE_PROTOCOL_STATUS: COMPLETE -- specified, not yet executed
R1_SCORING_STATUS:             IMPLEMENTED AND VALIDATED
R1_BLINDING_STATUS:            SPECIFIED -- enforced at execution time
R1_PREREGISTRATION_STATUS:     v1 SEALED; v1.1 PRE-OUTCOME AMENDMENT -- LOCAL COMMIT IS RUST-GATE-CONDITIONED
R1_VARIANCE_PILOT_PROTOCOL:    SEALED -- scientific design unchanged by v1.1
R1_RUNNER_REQUIREMENTS:        SPECIFIED
R1_INSTRUMENT_PILOT_STATUS:    X0 PASS 631/0; v1.1 extends selftest with native-export byte identity
R1_MODEL_RUNNER:               v1.1 CONTROLLED RUNNER BUILT -- NOT EXECUTED
R1_REAL_MODEL_EXECUTION:       NO
R1_VARIANCE_PILOT_STATUS:      NOT_STARTED -- model calls prohibited pending post-commit founder review
CONFIRMATORY_STATUS:           NOT_STARTED
PRODUCT_THESIS_STATUS:         NOT_EVALUATED
```

**NOT READY FOR MODEL EXECUTION — a committed v1.1 is evidence that the local Rust
finalizer gate passed; credentialed preflight still requires post-commit founder review.**


## Gate X1 — pre-outcome execution-plumbing amendment

See [PREREGISTRATION-V1.1.md](./PREREGISTRATION-V1.1.md) and
[ADDENDUM-X1.md](./ADDENDUM-X1.md). X1 repairs native package export, maintained-state
rendering, repeat-preserving response paths, deterministic repeat-addressed score
serialization and runner orchestration. The frozen arm builders, maintenance fold,
response parser and `score_one` predicate remain byte-identical to X0.

No model call is authorized by this amendment. The supplied local finalizer is
fail-closed: it may create the single X1 commit only after Python, Rust, native-export,
fileset, scope and secret gates pass. Therefore an X1 commit containing this document
is itself evidence that those local gates completed; the commit SHA is reported
externally rather than self-referenced here.

---

## Gate X0 — external model execution admission

Three things were added and one defect was repaired. See
[ADDENDUM-X0.md](./ADDENDUM-X0.md) for the full record; the short version:

| | |
|---|---|
| **Two-stage execution frozen** | The next run is [R1-VARIANCE-PILOT](./VARIANCE-PILOT.md), not confirmatory. Its size, repeats, randomization, model rules, variance estimators, α, power, minimum effect, the mechanical confirmatory-N formula and its safety bounds are all sealed **before any variance data exists** |
| **Runner admissibility specified** | [RUNNER.md](./RUNNER.md) — session isolation, per-run evidence schema, failure taxonomy, symmetric retry, immutable raw output, blinded scoring. An interactive IDE is explicitly **not** admissible |
| **Platform fields separated** | `PENDING_KILL_TEST_ROSTER_ENTRIES = 0` and `PLATFORM_EVIDENCE_PENDING = WINDOWS_NATIVE_SYMLINK, MACOS_FILESYSTEM` are now distinct, because a single "0 pending" read as "nothing outstanding", which is false |
| **Reproducibility defect repaired** | The repository had no `.gitattributes`, so a fresh checkout on a `core.autocrlf=true` host produced CRLF and the sealed **V0** results did not reproduce. **R1 was verified immune** — its `.scn` parser normalises through `str::lines()`, and the full 68-file bundle built from a CRLF checkout is byte-identical to the LF one, with the pilot passing 631/0 in both |

**Preregistration v1 was not edited and not invalidated.** No digested file changed and
the digest recomputes to `2645806d…`.

Handoff for an external executor: [HANDOFF.md](./HANDOFF.md).

---

## Why no model ran

This host has no controlled model execution, and the directive is explicit that faking
it is not an option.

| Checked | Found |
|---|---|
| API credentials (`ANTHROPIC*`, `OPENAI*`, `GEMINI*`, `MISTRAL*`, `COHERE*`, `GROQ*`, `TOGETHER*`, `AZURE*`, `HF_*`) | none — `ANTHROPIC_BASE_URL` is set but carries no key |
| Local runners: `ollama`, `llama-server`, `llama-cli`, `lms`, `jan`, `gpt4all`, `vllm` | none installed |
| `ollama` service on `localhost:11434` | no response |
| Scriptable CLI agents on `PATH` | none |

Desktop IDE applications are installed, but none of them is a **controlled** runner:
[PROTOCOL.md §9](./PROTOCOL.md) requires pinned temperature, pinned system
instructions, fresh stateless sessions and per-run token accounting. An interactive
IDE satisfies none of those, and using one would produce numbers that look like
measurements without being measurements.

**The harness contains no code path that fabricates a model response.** `selftest`
prints `ARM_SCORES_PRODUCED: NONE` and refuses to emit an arm score.

## Arm standing

| Arm | Package construction | Maintainer output | Scorable |
|---|---|---|---|
| `B-NULL` | trivial | n/a | needs model |
| `B0` | **working** | none needed | needs model |
| `B1` | **working** | **ABSENT** | no |
| `B3` | **working** | none needed | needs model |
| `B4` | **working** | **ABSENT** | no |
| `B5` | **working** | **ABSENT** | no |

B1, B4 and B5 have no artefact because maintenance is a **model task**, deliberately.
Authoring those artefacts by hand is exactly the V0 mistake — a maintainer who already
knows the tasks is an answer key, not a maintainer.

## What an external executor has to do

1. Verify the committed v1.1 filesets and frozen semantics with `verify_v1_1.py`.
2. Perform the separately authorized credentialed preflight using **no benchmark
   content**; bind the exact model/reasoning/max-output condition and record unsupported
   sampling controls as `UNAVAILABLE`.
3. Execute the fixed 168 task-blind maintenance sessions, then export context packages
   through the native Rust harness.
4. Execute the fixed 720 continuation sessions in the sealed blocked/interleaved order;
   B-NULL is part of that order and is **not** run as a separate early batch.
5. Seal raw evidence before scoring. Score under neutral arm ids, then explicitly
   unblind only after deterministic scoring is complete.
6. Report pilot variance and `psi-hat`, then compute confirmatory N mechanically from
   `VARIANCE-PILOT.md`. Do not start confirmatory until its separate manifest is sealed.

The bundle at `bench/R1/bundle/` is regenerable and therefore not committed. It
contains per-checkpoint evidence, task prompts with the output contract, the arm
roster and a manifest. It does **not** contain the oracles, and `bundle` asserts that
before it exits.

## The one caveat that must travel with any B5 number

Phase T has **no agent-facing memory-write surface**. B5's maintainer emits structured
instructions that the R1 harness applies through the Rust library; that adapter is
benchmark tooling and is not part of Fehrest.

**B5's measured maintenance cost is therefore a lower bound, not an estimate.** A real
B5 maintainer would pay for whatever interface eventually exists. Quoting B5's
maintenance cost without this caveat overstates the result.

## What this is not

A passing instrument pilot says the ruler is straight. **Nothing has been measured with
it.** No arm has a score, no comparison exists, and `PRODUCT_THESIS_STATUS` is
`NOT_EVALUATED` — the same value it has held since Phase T began.
