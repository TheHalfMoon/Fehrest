# R1 — preregistration v1.1 execution-plumbing amendment

```
PREREGISTRATION_VERSION:             R1-PREREG-v1.1
AMENDMENT_CLASS:                     PRE-OUTCOME EXECUTION PLUMBING ONLY
ORIGINAL_V1_DECLARED_DIGEST:         2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
ORIGINAL_V1_CANONICAL_FILESET_SHA256: c7203d3ff0ccdd859a21841ef0cac25b46c5224cf35980cb02fc0c5a1590e28f
R1_V1_1_CANONICAL_FILESET_SHA256:     5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
R1_X1_RUNNER_FILESET_SHA256:          30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f
BASE_HEAD:                            685b390d93fd58c65b8d9e33f4869c6c986259d3
MODEL_RUNS_OBSERVED_AT_AMENDMENT:     0
VALID_RUNS_OBSERVED_AT_AMENDMENT:    0
SCORING_STATUS:                      NOT_STARTED
PRODUCT_THESIS_STATUS:               NOT_EVALUATED
CONFIRMATORY_STATUS:                 NOT_STARTED
```

This is not a rewrite of preregistration v1. The v1 document and its declared digest
remain historical evidence. This amendment was written before any model request,
response, pilot score, variance estimate, power analysis or confirmatory run existed.

## 1. Why an amendment is required

The external-runner gate exposed execution-plumbing defects that make the sealed
variance pilot impossible to execute faithfully without changing the R1 harness:

1. `build_all` constructs the preregistered arm packages but no command exports them.
2. The runner needs the maintained artefact as of `Ti-1`; reimplementing B5 lifecycle
   folding in Python would create a second treatment implementation.
3. The variance pilot has four continuation repeats per `(arm, task)`, while the v1
   response path and scorer address only one `<arm>/<task>.txt` file.
4. The first X1 runner implementation contained the primitives for execution but its
   `run` command deliberately stopped before orchestration.

All four defects were discovered with `OBSERVED_PILOT_RUNS=0`. Repairing them after
outcomes existed would be a different scientific situation and is not authorized.

## 2. Exact authorized semantic boundary

The following remain byte-identical to the X0 base harness and are verified by
`verify_v1_1.py`:

- scenario parsing and scenario loading;
- task loading and oracle loading;
- maintenance folding semantics;
- `arm_b0`, `arm_b1`, `arm_b3`, `arm_b4`, `arm_b5`;
- response parsing;
- the `score_one` scoring predicate.

The corpus, task roster/prompts, oracles, maintenance protocol, variance design,
repetitions, trajectories, randomization structure, primary outcome and confirmatory
boundary are unchanged.

The v1.1 harness delta is limited to:

- export the bytes already returned by native `build_all`;
- expose a read-only native maintained-state view so the runner does not duplicate B5
  fold/lifecycle semantics;
- preserve each continuation repeat in a separately addressable response file;
- allow the unchanged `score_one` predicate to consume repeated response paths and
  emit repeat-addressed JSONL score records.

No Fehrest product code, product tests, dependency graph, UI, graph, vector, automatic
memory, MCP or branding surface is changed.

## 3. Native package identity requirement

`fehrest-r1 export-packages <state-root> <out-dir>` must call the same `build_all`
implementation used by the instrument. The exporter is forbidden from parsing,
normalizing, reranking, retruncating or reconstructing package content.

`selftest` includes native export checks requiring two independent exports of the same
in-memory `Built` map to be byte-identical to the source strings for every package.
The exporter also emits `PACKAGE-MANIFEST.txt` with one SHA-256 per exported package.
The external runner verifies that manifest before the first continuation request.
The sealed external `BUNDLE-MANIFEST.txt` is also verified as an exact manifest of the
model-facing `bundle/` subtree. Human-only `protocol/` siblings are deliberately not
model-facing and are not entries in that 68-file manifest; the complete archive remains
separately pinned by its archive SHA-256.

## 4. Maintainer-state boundary

`fehrest-r1 maintenance-view` is read-only execution plumbing over the existing
`fold_maintenance` function. For checkpoint `Ti`, the runner requests the view through
`Ti-1`; therefore a resumed run cannot accidentally show the maintainer its own
already-written `Ti` output.

Malformed maintainer JSON receives the single identical-prompt retry already specified
by `MAINTENANCE.md §7`. A second malformed result or a refusal leaves state unchanged.
The raw responses and retry attempts remain immutable evidence. Infrastructure
exclusion is transactional at the maintenance cell: if one maintained arm exhausts
its provider retries for a `(trajectory, scenario, checkpoint)` cell, no maintained
arm's update from that cell is applied. Raw attempts remain preserved.

## 5. Repeat-preserving scoring plumbing

Variance-pilot continuation output is stored as:

```
responses/<NEUTRAL_ARM_ID>/<TASK_ID>/r<NN>.txt
```

The scorer accepts this path in addition to the legacy v1 single-response path. The
actual scoring predicate `score_one` is unchanged. `score-jsonl` merely serializes its
per-response result with the repeat index and response digest so variance analysis can
pair observations without guessing file order.

Continuation infrastructure exclusion is likewise transactional at the frozen
`(task, repeat)` cell. Responses are published into the scorer-visible tree only after
every arm in that cell reaches a terminal task result. If any arm exhausts provider
retries, the whole cell remains absent from scorer input while all raw attempts remain
immutable evidence. Neutral-to-real arm mapping is not written during execution; it is
created only by an explicit post-scoring unblind command.

## 6. Credentialed preflight boundary

The later credentialed preflight contains no R1 corpus, task, oracle or arm package.
It must prove the exact requested model, reasoning effort and max-output setting. It
also probes `temperature`, `top_p` and model `seed` separately; only controls accepted
by the provider and then accepted together in a combined-condition probe may enter the
pilot. Every other control is recorded as `UNAVAILABLE`. The preflight record is
write-once and bound to the exact runner version.

## 7. Canonical digest reconciliation

The eight individual v1 file SHA-256 values exactly match `PREREGISTRATION.md`, but the
published aggregate shell pipeline does not reproduce the declared aggregate
`2645806d...` in this Linux verification environment. Because that value is historical
and was repeatedly reported on the Windows authoring host, v1.1 does **not** overwrite
or reinterpret it.

For v1.1, `seal_digest.py` defines a platform-independent aggregate:

1. use the same eight benchmark files as v1;
2. hash their exact bytes with SHA-256;
3. sort by POSIX path relative to `bench/R1`;
4. serialize each line exactly as `<sha256><two spaces><relative_path><LF>`;
5. SHA-256 the resulting UTF-8/LF manifest bytes.

Applied to the exact X0 Git objects, that rule yields
`c7203d3ff0ccdd859a21841ef0cac25b46c5224cf35980cb02fc0c5a1590e28f`.
Applied to this v1.1 harness amendment, it yields
`5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2`.
This is an audit-format repair, not a scientific-rule change.

The external runner is separately bound by the same canonical manifest rule over
`.gitignore`, `README.md`, `r1_runner.py` and `test_r1_runner.py`, currently
`30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f`.

## 8. Separation from confirmatory execution

Variance-pilot data are never part of the confirmatory dataset. No confirmatory
manifest may be sealed until the fixed 888-session pilot is complete, `psi-hat` is
computed from pilot data, and the preregistered power formula determines `r_conf`.

Nothing in this amendment authorizes a model call. Credentialed preflight is a later,
separate founder gate.
