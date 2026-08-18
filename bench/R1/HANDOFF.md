# R1 — external runner handoff

```
CONTROLLED_RUNNER_STATUS:  UNAVAILABLE on the authoring host
R1_REAL_MODEL_EXECUTION:   NO
NEXT_STAGE:                R1-VARIANCE-PILOT (not confirmatory)
PRODUCT_THESIS_STATUS:     NOT_EVALUATED
```

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
R1_PREREGISTRATION_DIGEST  2645806db31dd92beb390dac78b5e2d2ac210d1407b6f37720eddafa8fa80ae3
```

Recompute and compare before running anything:

```bash
for f in bench/R1/scenarios/*.scn bench/R1/tasks/tasks.json bench/R1/oracles/oracles.json bench/R1/harness/main.rs bench/R1/PROTOCOL.md bench/R1/MAINTENANCE.md; do sha256sum "$f"; done | sha256sum
```

A mismatch means the benchmark changed. **Stop and reconcile; do not run.**

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
# 0. verify before touching anything
cargo run --bin fehrest-r1 -- selftest            # expect: 631 passed, 0 failed
for f in bench/R1/scenarios/*.scn bench/R1/tasks/tasks.json bench/R1/oracles/oracles.json bench/R1/harness/main.rs bench/R1/PROTOCOL.md bench/R1/MAINTENANCE.md; do sha256sum "$f"; done | sha256sum

# 1. regenerate the model-facing bundle
cargo run --bin fehrest-r1 -- bundle              # expect: ORACLE_LEAK_CHECK: CLEAN

# 2. maintenance -- 168 sessions, task-blind, per MAINTENANCE.md
#    3 maintained arms x 2 trajectories x 28 checkpoints
#    writes bench/R1/state/<ARM>/<SCENARIO>/t<NN>.json
#    (the runner drives this; the harness folds the ops)

# 3. continuation -- 720 runs, blocked/interleaved, seeded
#    5 comparison arms x 30 tasks x 4 repeats  = 600
#    B-NULL          x 30 tasks x 4 repeats    = 120
#    writes runs/variance-pilot/responses/<ARM_ID>/<TASK_ID>.txt

# 4. score, blind
cargo run --bin fehrest-r1 -- score runs/variance-pilot/responses
```

Sizes, repeats, trajectories, randomization and the model rules are frozen in
[VARIANCE-PILOT.md](./VARIANCE-PILOT.md). **Do not adjust them after seeing results.**

## 6. Expected output layout

```
runs/variance-pilot/
  records.jsonl              one per-run record, RUNNER.md §3 schema
  execution-order.jsonl      realized order, appended as it happens
  arm-map.json               neutral ARM_ID -> real arm. WITHHELD until scoring is done
  raw/<run_id>.txt           untouched model output -- immutable evidence
  normalized/<run_id>.txt    only if a normalizer was used; keep both + its version
  responses/<ARM_ID>/<TASK_ID>.txt
bench/R1/state/<ARM>/<SCENARIO>/t<NN>.json    maintainer output
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
| Empty, malformed, refusal | `TASK_FAILURE` | **No retry.** Score as-is. It is the result |

**Selective retry of one arm is prohibited.** Raw output is never manually repaired. If
infrastructure failures exceed 10% of attempted sessions, halt: the runner is
inadmissible, and that is a fact about the runner, not about the arms.

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
