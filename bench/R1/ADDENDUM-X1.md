# R1 — addendum X1: v1.1 execution-plumbing amendment

```
GATE:                              PHASE_T_R1_X1
BASE_HEAD:                         685b390d93fd58c65b8d9e33f4869c6c986259d3
ORIGINAL_V1_DECLARED_DIGEST:       2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
ORIGINAL_V1_CANONICAL_FILESET:     c7203d3ff0ccdd859a21841ef0cac25b46c5224cf35980cb02fc0c5a1590e28f
R1_V1_1_CANONICAL_FILESET:         5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
R1_X1_RUNNER_FILESET:              30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f
MODEL_EXECUTED:                    NO
OBSERVED_PILOT_RUNS:               0
SCORING_STATUS:                    NOT_STARTED
CONFIRMATORY_STATUS:               NOT_STARTED
PRODUCT_THESIS_STATUS:             NOT_EVALUATED
```

Founder authorization permitted a transparent pre-outcome v1.1 amendment rather than
an invisible reimplementation of the treatment in the Python runner. The amendment is
recorded in [PREREGISTRATION-V1.1.md](./PREREGISTRATION-V1.1.md).

## Defects discovered before any outcome

- native arm packages existed only in memory;
- current B5 maintained state could not be supplied to the next maintainer without
  duplicating lifecycle/supersession semantics outside Rust;
- repeated continuation responses would overwrite/collapse to one task file;
- the initial X1 `run` CLI stopped before orchestration;
- the legacy aggregate digest command is not cross-platform reproducible even though
  all eight individual v1 file hashes match;
- a restart after an infrastructure attempt could not resume its retry chain;
- a continuation response could be published before symmetric cell exclusion was
  known, leaving partial scorer input;
- maintainer JSON wrapper prose could be silently sliced/repaired;
- the arm map could be materialized before blinded scoring;
- sampling-control probe code existed but was not bound to the executed condition;
- the first external-bundle verifier treated human-only `protocol/` files as if they
  were part of the 68-file model-facing manifest; the corrected verifier requires the
  exact 68/68 `bundle/` roster and bytes while keeping `protocol/` outside model input.

All are execution/audit plumbing defects. None changes the scientific treatment or
scoring predicate.

## Implemented repair

- `harness/main.rs`: native `maintenance-view`, native `export-packages`, deterministic
  package manifest, repeat-addressed scorer input, `score-jsonl`, and selftest byte
  identity checks.
- `external-runner/r1_runner.py`: native harness bridge, immutable trajectory state,
  realized-order logging, repeat-preserving output, one maintenance malformed-JSON
  retry, package-manifest verification, restart-safe immutable retry chains,
  transactional cell publication/exclusion, real 168+720 orchestration, explicit
  post-score unblinding, and capability-bound preflight evidence.
- `external-runner/test_r1_runner.py`: 75 tests including native-package integration,
  strict maintainer JSON, repeat preservation, restart-safe retry chains, transactional
  symmetric infrastructure exclusion, control-artifact immutability, package-manifest
  path safety, explicit unblinding and parameter-capability binding.
- `seal_digest.py`: portable benchmark/runner fileset sealing.
- `verify_v1_1.py`: byte-identity guard for frozen Rust semantics and product-scope
  guard.

The X0 base versions of `fold_maintenance`, `arm_b0`..`arm_b5`, `parse_response` and
`score_one` compare byte-identical against the working candidate.

## Current verification status in the ChatGPT execution environment

Passed here:

- archive SHA-256 of the uploaded checkout matched the founder-provided archive;
- HEAD and frozen product source tree matched expected values;
- product diff is empty;
- external bundle SHA-256 remained `17934f84...c321e`;
- `BUNDLE-MANIFEST.txt` digest remained `48394b01...e69ff`, with 68/68 model-facing
  entries matching and no unmanifested file under `bundle/`;
- sealed plan remains 168 maintenance + 720 continuation = 888;
- token envelope remains ~1,384,949 estimated input tokens and 909,312 maximum output
  tokens;
- Python compile passes;
- 75 runner tests pass functionally, with the SDK payload test skipped only because
  the ChatGPT sandbox lacks the `openai` package;
- `verify_v1_1.py` passes every frozen-function and product-scope check;
- no model request was made.

Not yet provable in this sandbox:

- Rust compile / clippy / selftest, because this sandbox has no Rust toolchain and its
  container network cannot fetch one.

A Windows v3 finalizer run subsequently proved all **75/75** external-runner tests with
`openai==3.3.0` isolated in a temporary venv and re-proved the v1.1 semantic freeze,
then stopped at `cargo fmt --check` before compile/test/commit. Rustfmt reported exactly
four formatting-only rewrites in the new execution-plumbing code. The v4 candidate
incorporated exactly those bytes; its Windows run then passed `cargo fmt --check` and
re-proved 75/75 runner tests plus the semantic freeze before `cargo check` exposed one
compile-only diagnostic-format error (`concat!` cannot capture the surrounding `other`)
and six redundant `return` warnings before diverging `std::process::exit(2)` expressions.
No model request, score or commit existed. The v5 candidate changes only those `main()`
execution-plumbing diagnostics/control-flow spellings and updates the canonical fileset
seal; all frozen arm/scorer/maintenance functions remain byte-identical.

The ChatGPT-produced payload leaves its sandbox **uncommitted** because that sandbox
has no Rust toolchain. The supplied local finalizer is fail-closed and may create the
single X1 commit only after the Rust/Python/native-export gates pass. A commit containing
this addendum therefore attests that those local gates passed; the commit SHA is reported
externally rather than written into the commit that identifies itself.
