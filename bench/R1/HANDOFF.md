# R1 — external runner handoff

```
CONTROLLED_RUNNER_STATUS:  v1.1 BUILT -- LOCAL COMMIT IS RUST-GATE-CONDITIONED, NOT EXECUTED
R1_REAL_MODEL_EXECUTION:   NO
NEXT_GATE:                 local gate/commit if absent, then post-commit founder review
NEXT_STAGE_AFTER_GATE:     R1-VARIANCE-PILOT (not confirmatory)
PRODUCT_THESIS_STATUS:     NOT_EVALUATED
```


> **X1 STOP:** This handoff contains the pre-outcome v1.1 execution-plumbing amendment.
> A local X1 commit is permitted only through the fail-closed Rust/Python finalizer.
> Do not issue a model request until that commit exists and receives post-commit founder
> review. The original v1 remains preserved.

Everything needed to run the variance pilot elsewhere. Read
[RUNNER.md](./RUNNER.md) first — a runner that fails §1 there produces numbers that
look like measurements without being measurements.

---

## 1. Sealed bundle

```
Path      bench/R1/bundle/                      (regenerable, not committed)
Archive   bench/R1/dist/r1-external-bundle.tar.gz
Manifest  bench/R1/dist/BUNDLE-MANIFEST.txt     (per-file sha256, 68 entries)
```

| Artefact | SHA-256 |
|---|---|
| `r1-external-bundle.tar.gz` | `17934f84a07afef08e469b0526d343d26e5597ea3455e575b5f9c46ae91c321e` |
| Bundle file-set digest (`sha256` of `BUNDLE-MANIFEST.txt`) | `48394b012ab1cb2bf6c46f8c6b2934ccdd7573b9713de31717031f0ad37e69ff` |

The archive is built with `tar --sort=name --owner=0 --group=0 --numeric-owner
--mtime='UTC 2020-01-01' | gzip -n`, so it is **byte-deterministic** — rebuilding it
reproduces the same hash. Verified.

**It contains no oracles.** Verified by extracting the archive and scanning every
model-facing file for oracle fields: 0 hits. It carries `bundle/` (per-checkpoint
evidence, 30 task prompts with the output contract, `ARMS.txt`, `MANIFEST.txt`), the
protocol documents, and the file manifest. Scoring requires the repository, which holds
`oracles/oracles.json`; the executor must never feed that file to a model.

## 2. Preregistration

```
ORIGINAL_V1_DECLARED_DIGEST           2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
ORIGINAL_V1_CANONICAL_FILESET_SHA256  c7203d3ff0ccdd859a21841ef0cac25b46c5224cf35980cb02fc0c5a1590e28f
R1_V1_1_CANONICAL_FILESET_SHA256      5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2
```

The original v1 aggregate remains historical evidence. X1 found that its published
aggregate shell pipeline is not cross-platform reproducible even though all eight
individual file hashes match. v1.1 therefore uses the explicit canonical manifest
algorithm in `PREREGISTRATION-V1.1.md` and the portable verifier:

```bash
python bench/R1/seal_digest.py benchmark
python bench/R1/seal_digest.py benchmark --git-ref 685b390d93fd58c65b8d9e33f4869c6c986259d3
python bench/R1/verify_v1_1.py
```

A mismatch means the benchmark or frozen semantics changed. **Stop and reconcile; do
not run.**

## 3. Frozen Fehrest identity

```
FEHREST_SOURCE_COMMIT_SHA  5902460c2dfe4912825d2adfe62ae8142399f113
FEHREST_SOURCE_TREE_SHA    501004e0be6630eb2d2a90b196012f9cbb596c5a
```

Verify:

```bash
git rev-parse HEAD:src                 # must equal FEHREST_SOURCE_TREE_SHA
git log -1 --format=%H -- src/         # must equal FEHREST_SOURCE_COMMIT_SHA
git diff --stat 5902460c2dfe4912825d2adfe62ae8142399f113..HEAD -- src/ tests/ Cargo.lock
```

The third command must print nothing. Every commit after the source commit is
benchmark, documentation or research material. `Cargo.toml` changed only inside
`[[bin]]` blocks, adding benchmark binary targets; `[package]`, `[lints.rust]` and
`[dependencies]` are byte-identical.

## 4. Required runner interface

Full specification in [RUNNER.md](./RUNNER.md). The non-negotiables:

- Fresh stateless session per run. No conversation reuse between repeats, arms or tasks.
- One model condition across **all** primary arms. A stronger model for B5 than for the
  baselines invalidates the batch.
- Maintainer sessions are task-blind: no tasks, no oracles, no future checkpoints.
- `tool_set = []`, `tool_permissions = "none"` for every arm.
- One JSON record per run to the §3 schema, including the raw response and its digest.
- Unsupported controls recorded as `UNAVAILABLE`, never as a plausible default.
- **An interactive IDE or chat window is not admissible.**

## 5. Variance-pilot command sequence

```bash
# 0. verify the amendment; create/accept its local commit before any credentialed call
python bench/R1/verify_v1_1.py
cargo fmt --check
cargo check
cargo clippy -- -D warnings
cargo test
cargo run --bin fehrest-r1 -- selftest            # extended v1.1 selftest; require 0 failed

# 1. regenerate the model-facing bundle
cargo run --bin fehrest-r1 -- bundle              # expect: ORACLE_LEAK_CHECK: CLEAN

# 2. credentialed preflight is a separate founder gate. It uses no R1 benchmark
#    content and binds model/reasoning/max-output plus supported sampling controls.
#    Only after it passes may the v1.1 runner drive the fixed 168+720 pilot.
#
#    maintained state: <scratch>/state/{T1,T2}/<ARM>/<SCENARIO>/t<NN>.json
#    native packages:  <scratch>/packages/<TRAJECTORY>/<ARM>/<SCENARIO>/t<NN>.txt
#    responses:        <scratch>/runs/variance-pilot/responses/<ARM_ID>/<TASK_ID>/r<NN>.txt

# 3. after execution completes, seal raw/neutral evidence BEFORE scoring/unblinding
python bench/R1/external-runner/r1_runner.py seal --out <scratch>/runs/variance-pilot

# 4. score while arm identity is still withheld. score_one is unchanged from v1.
cargo run --bin fehrest-r1 -- score-jsonl <scratch>/runs/variance-pilot/responses <scratch>/runs/variance-pilot/score-records.jsonl
cargo run --bin fehrest-r1 -- score <scratch>/runs/variance-pilot/responses

# 5. only after blinded scoring completes, materialize the neutral -> real map
python bench/R1/external-runner/r1_runner.py unblind-map --out <scratch>/runs/variance-pilot --seed <SEALED_SEED>
```

Sizes, repeats, trajectories, randomization and the model rules are frozen in
[VARIANCE-PILOT.md](./VARIANCE-PILOT.md). **Do not adjust them after seeing results.**

## 6. Expected output layout

```
<scratch>/runs/variance-pilot/
  records.jsonl                         one per-attempt record, RUNNER.md §3 schema
  execution-order.jsonl                 realized provider-attempt order
  execution-plan.json                   sealed neutral plan; arm map withheld
  package-binding.json                  native package manifest -> execution plan binding
  excluded-cells.json                   symmetric infrastructure exclusions
  raw/<run_id>.txt                      untouched model output -- immutable evidence
  responses/<ARM_ID>/<TASK_ID>/r<NN>.txt  complete scorer-visible cells only
  FILE-MANIFEST.txt                     deterministic self-excluding raw manifest
  arm-map.json                          ABSENT until explicit post-score unblind
<scratch>/state/{T1,T2}/<ARM>/<SCENARIO>/t<NN>.json
<scratch>/packages/<TRAJECTORY>/<ARM>/<SCENARIO>/t<NN>.txt
```

## 7. Verification commands

```bash
cargo run --bin fehrest-r1 -- selftest        # instrument still sound
cargo run --bin fehrest-bench-v0              # must reproduce bench/V0/results.txt exactly
cargo test                                    # 99 on Windows, 98 on Linux
sha256sum bench/R1/dist/r1-external-bundle.tar.gz
```

The V0 reproduction is a live tripwire for the line-ending defect repaired at this gate
(addendum X0 §1). If it stops matching, check `.gitattributes` before anything else.

## 8. Failure and retry rules

| Class | Kind | Action |
|---|---|---|
| Timeout, rate limit, network, crash, tool failure, context-limit exceeded | `INFRASTRUCTURE_FAILURE` | Retry ≤2 with backoff. Still failing → exclude that (task, repeat) cell **for every arm** |
| Empty, malformed, refusal in continuation | `TASK_FAILURE` | **No retry.** Score as-is. It is the result |
| Malformed maintainer JSON | `TASK_FAILURE` | One identical-prompt retry per MAINTENANCE.md §7; then state unchanged |

**Selective retry of one arm is prohibited.** Raw output is never manually repaired.
Infrastructure exclusion is transactional: a failed maintenance cell advances no
maintained arm, and a failed continuation `(task, repeat)` cell publishes no arm into
scorer input. If exhausted infrastructure cells exceed 10% of attempted cells, halt:
the runner is inadmissible, and that is a fact about the runner, not about the arms.

## 9. Prohibited at this stage

- Issuing `PRODUCT_THESIS_PASS` or `PRODUCT_THESIS_FAIL` from the variance pilot.
- Pooling pilot runs into the confirmatory dataset.
- Starting confirmatory execution before `R1_VARIANCE_PILOT_COMPLETE` **and**
  `R1_CONFIRMATORY_MANIFEST_SEALED`.
- Choosing confirmatory N by anything other than the mechanical formula in
  [VARIANCE-PILOT.md §7](./VARIANCE-PILOT.md).
- Adding a Fehrest feature in response to any result.

## 10. Credentials

None are included, and none belong in this archive or in any run record. Provide the
runner's credential through its own environment. Per-run records store the model
identifier and digests — **never a key**.
