# R1 — addendum X0: external model execution admission

```
GATE:                        PHASE_T_R1_X0
PREREGISTRATION_V1:          UNCHANGED AND VALID
PREREGISTRATION_V1_DIGEST:   2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
DIGEST_REVERIFIED_AT_X0:     YES
DIGESTED_FILES_MODIFIED:     NONE
```

This is an **addendum**, not an edit. [PREREGISTRATION.md](./PREREGISTRATION.md) is
sealed by the commit that introduced it and has not been touched; none of the six
digested files — the three scenarios, `tasks.json`, `oracles.json`, `harness/main.rs`,
`PROTOCOL.md`, `MAINTENANCE.md` — was modified at this gate. The digest recomputes to
the same value.

Everything below either **adds** a rule that v1 left implicit, or **repairs a
reproducibility defect outside the digest**.

---

## 1. A reproducibility defect was found, proven, and repaired

Found while verifying the frozen implementation identity, not by looking for it.

**The repository had no `.gitattributes`.** On a host with `core.autocrlf=true` — the
Windows default — a fresh checkout produced CRLF files. Measured by checking `HEAD`
out into a separate worktree and running the harness there:

| | Sealed (LF) | Fresh checkout (CRLF) |
|---|---|---|
| V0 B1 mean context bytes | 2,805 | **2,884** |
| V0 B3 mean context bytes | 2,624 | **2,698** |
| V0 B4 mean context bytes | 1,370 | **1,406** |

**The sealed V0 archive was not reproducible from a clean clone.** Its adequacy verdict
was unaffected — 1/6, 2/6, 3/6, 5/6, 6/6 in both regimes — but its byte-cost figures
were checkout-dependent, and its own reproduction instruction was therefore wrong for
anyone who cloned the repository. Recorded as erratum E-3 in
[V0/ARCHIVE.md](../V0/ARCHIVE.md).

### 1.1 R1 was checked and is immune — verified, not assumed

R1's `.scn` parser reads through `str::lines()`, which strips a trailing `\r`, and
reconstructs bodies with `\n`. Line endings are normalised before any byte-budget
decision is made.

That is a claim about code, so it was tested against behaviour:

| Check | Result |
|---|---|
| Full 68-file R1 bundle, built from a CRLF checkout vs the LF worktree | **byte-identical** |
| Instrument pilot in the CRLF checkout | 631 passed, 0 failed |
| Instrument pilot in the LF worktree | 631 passed, 0 failed |

**Preregistration v1 is therefore not invalidated.** The defect did not reach R1's
corpus semantics, task prompts, oracles, scoring rules, maintenance protocol, baseline
behaviour or arm construction.

### 1.2 The repair

`.gitattributes` pinning `* text=auto eol=lf`. It touches no digested file and changes
no benchmark semantics; it makes every checkout byte-identical on every platform,
which is the precondition for a sealed digest meaning anything to an external
executor.

Verified after the fix by checking `HEAD` out into a fresh worktree again: the V0
harness now reproduces `results.txt` **exactly**, and the R1 pilot passes 631/0.

## 2. Platform evidence — two counts, never one

Phase T-R1 reported `SECURITY_KILL_TEST_PENDING_PLATFORM=0 roster entries`. The number
is right and the phrasing invites the wrong reading: "0 pending" sounds like *no
platform evidence is outstanding*, which is false.

From this gate onward they are separate fields:

```
PENDING_KILL_TEST_ROSTER_ENTRIES = 0
PLATFORM_EVIDENCE_PENDING        = WINDOWS_NATIVE_SYMLINK, MACOS_FILESYSTEM
```

| Field | Question it answers | Value |
|---|---|---|
| `PENDING_KILL_TEST_ROSTER_ENTRIES` | Is any roster entry unexecuted **everywhere**? | 0 |
| `PLATFORM_EVIDENCE_PENDING` | Which platforms lack evidence they should have? | Windows native symlink; macOS filesystem |

The first fell from 1 to 0 when K-12 executed on Linux/ext4. **The second has not moved
and will not move on the authoring host**, because Windows symlink creation requires
Developer Mode or elevation, and neither will be enabled to make a test pass.

No test result changed. The technical pass is neither downgraded nor upgraded:
22 kill tests executed and passed, 0 failed, 3 deferred surfaces absent in Phase T, and
`FULL_CROSS_PLATFORM_PASS` remains unclaimed.

## 3. B5 maintenance cost is a **lower bound** — and what may be concluded from it

Phase T has **no agent-facing memory-write interface**. The CLI writes canonical
objects; memories exist only through the Rust library. B5's maintainer therefore drives
a benchmark-only adapter, and a real product maintainer would pay for whatever
interface eventually exists.

```
B5_MEASURED_MAINTENANCE_COST = LOWER_BOUND
```

This restricts **cost** claims. It does not restrict **continuation-quality**
measurement, which does not depend on how the artefact was written.

### 3.1 Interpretation rule — fixed now, before any number exists

| Observation | What may be concluded |
|---|---|
| **B5 loses on continuation quality** | **Strong negative evidence.** B5 lost while enjoying an artificially favourable maintenance cost. The real cost can only be higher, so the loss cannot be explained away by upkeep |
| **B5 appears cheaper to maintain than B4 or B1** | **No product claim.** R1 alone cannot establish maintenance-cost superiority, because B5's figure excludes an interface that does not exist yet |
| **B5 wins materially on continuation quality** | **Interpretable on its own terms**, independently of the cost caveat — provided the cost figure is reported alongside it and labelled as a lower bound |
| **B5 wins on quality but is more expensive even at the lower bound** | Reported as `THESIS_SUPPORTED_WITH_COST_CAVEAT` per [PREREGISTRATION.md §8](./PREREGISTRATION.md), and the true cost is worse than measured |

The asymmetry is deliberate and it is not favourable to Fehrest: a lower-bound cost can
only make B5 look better than it is, so a **loss** is more trustworthy than a **win**.

## 4. Two-stage execution is now frozen

The next external run is **not** confirmatory. It is
[R1-VARIANCE-PILOT](./VARIANCE-PILOT.md), whose entire protocol — sample size,
repeats, trajectories, randomization, model rules, scorer rule, variance estimators,
power method, α, power, minimum meaningful effect, the mechanical rule that computes
confirmatory N, and the min/max safety bounds — is sealed **before any variance data
exists**.

```
VARIANCE_PILOT_RESULTS_INCLUDED_IN_CONFIRMATORY = NO
```

Pilot data is never pooled into the confirmatory dataset, never reused as extra
observations, and never rescored under a later rule. Confirmatory execution may not
begin until `R1_VARIANCE_PILOT_COMPLETE` **and** `R1_CONFIRMATORY_MANIFEST_SEALED` are
both true.

If the frozen formula demands more runs than the cost ceiling allows, the study is
declared `UNDERPOWERED_FOR_PREREGISTERED_EFFECT` — **not** rescued by lowering the
effect threshold, relaxing α, dropping hard task classes, or going one-sided.

## 5. Runner admissibility

Specified in [RUNNER.md](./RUNNER.md): session isolation, configuration pinning,
per-run evidence schema, failure taxonomy, symmetric retry policy, immutable raw
output, blinded scoring.

**An interactive IDE or chat window is not a controlled runner**, however capable the
model inside it. It fails session isolation, configuration pinning and evidence
capture, and the failure is invisible in the output — which is why it is refused by
rule rather than by judgement.

```
CONTROLLED_RUNNER_STATUS = UNAVAILABLE
```

No credential, no local runner, no scriptable agent CLI on the authoring host. **No
model was executed and none was simulated.**

## 6. What this gate did not do

- Did not modify Fehrest product behaviour. `FEATURES_ADDED = NONE`.
- Did not modify any digested benchmark file.
- Did not edit or reissue preregistration v1.
- Did not execute a confirmatory run.
- Did not produce an arm score, an effect estimate, or a thesis verdict.

`PRODUCT_THESIS_STATUS: NOT_EVALUATED` — unchanged since Phase T began.
