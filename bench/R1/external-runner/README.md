# R1 external controlled runner

```
RUNNER_VERSION:            r1-external-runner/1.1.0
STATUS:                    BUILT AND TESTED -- NOT EXECUTED
MODEL_EXECUTED:            NO
ORACLES_READ:              NONE
FEHREST_PRODUCT_FILES_CHANGED: NO
```

Benchmark tooling for [VARIANCE-PILOT.md](../VARIANCE-PILOT.md). **It is not part of
Fehrest.** No Rust source, no `Cargo.toml` dependency and no product behaviour changes
because this directory exists. Python is a benchmark-tool requirement only.

---

## 1. What it does

Implements the runner admissibility rules in [RUNNER.md](../RUNNER.md): fresh
independent sessions, caller-set configuration, per-run evidence to the §3 schema, a
failure taxonomy that cannot mistake a provider timeout for a wrong answer, the frozen
symmetric retry policy, immutable raw output, resume without re-running valid work,
and a deterministic manifest and archive.

## 2. What it deliberately does not do

| Not done | Why |
|---|---|
| Score | The scorer is `fehrest-r1 score`, run in the trusted environment against the hidden oracles. The runner never sees an oracle |
| Build arm context packages | Arm construction lives in the digested `harness/main.rs`. A second implementation would measure something other than what was preregistered |
| Normalize, repair or reformat an answer | RUNNER.md §6. Raw output is evidence |
| Accept a key on the command line | `argv` is visible to process inspection and shell history. `OPENAI_API_KEY` from the environment, or nothing |
| Thread conversation state | No `previous_response_id`, no conversation object, `store=False` |

## 3. Credential handling

The key is read from `OPENAI_API_KEY` and used only to construct the SDK client. It is
never placed in a record, a raw file, a manifest, a log line or an archive. `seal`
refuses to produce an archive if `sk-`, `OPENAI_API_KEY` or `Authorization: Bearer`
appears anywhere under the output root, and `--api-key` on the command line is refused
before argument parsing.

The credentialed preflight contains **no R1 benchmark content**. It proves the requested
model, reasoning effort and max-output setting, then probes `temperature`, `top_p` and
model `seed` separately. A control enters the pilot request only when the provider
accepts it and the exact supported-control combination passes a final probe; otherwise
it is recorded as `UNAVAILABLE`. The preflight record is write-once and runner-version
bound.

## 4. Native package and maintenance-state boundary

The v1.1 amendment adds two execution-only native harness surfaces:

```
fehrest-r1 maintenance-view <trajectory-state-dir> <arm> <scenario> <checkpoint>
fehrest-r1 export-packages <state-root> <packages-root>
```

The runner calls those surfaces through `HarnessBridge`. It does **not** implement
`arm_b0`..`arm_b5`, B5 lifecycle/supersession folding, lexical retrieval, context
compilation, truncation, ranking or scoring. `export-packages` writes the exact bytes
already produced by the native `build_all` path plus a SHA-256 manifest.

Package layout is:

```
<packages-root>/T0/{B0,B3}/<SCENARIO>/t<NN>.txt
<packages-root>/{T1,T2}/{B1,B4,B5}/<SCENARIO>/t<NN>.txt
```

Continuation responses preserve every stochastic repeat separately at
`responses/<ARM_ID>/<TASK_ID>/r<NN>.txt`; the native scorer accepts that layout while
keeping `score_one` byte-identical to v1.

## 5. Commands

```bash
export PYTHONPATH=<isolated-openai-root>

python r1_runner.py preflight --model gpt-5.6-terra --reasoning-effort medium \
  --max-output 1024 --preflight-out <scratch>/preflight.json

python r1_runner.py estimate --bundle <extracted>/r1-external --max-output 1024
python r1_runner.py plan --bundle <extracted>/r1-external --seed <SEED>

python r1_runner.py run \
  --bundle <extracted>/r1-external \
  --repo-root <Fehrest-checkout> \
  --state-root <scratch>/state \
  --packages <scratch>/packages \
  --out <scratch>/runs/variance-pilot \
  --preflight-record <scratch>/preflight.json \
  --model gpt-5.6-terra --reasoning-effort medium --seed <SEED>

python r1_runner.py scan --out <scratch>/runs/variance-pilot
python r1_runner.py seal --out <scratch>/runs/variance-pilot

# Only after blinded native scoring has completed:
python r1_runner.py unblind-map --out <scratch>/runs/variance-pilot --seed <SEED>
```

`plan` against the sealed bundle prints `168 + 720 = 888`, matching
[VARIANCE-PILOT.md](../VARIANCE-PILOT.md) §2.

## 6. Execution order

VARIANCE-PILOT.md §3 fixes the loop structure and that one recorded seed drives it. It
does not name a PRNG, so this runner records its choice explicitly:

```
ORDER_ALGORITHM = sha256-keyed-sort/v1
key(item) = sha256(seed | ctx... | item)
```

A keyed sort is reproducible from the seed alone in any language and does not depend on
a runtime's RNG. Continuation order is `repeat -> task -> arm`, so arms are interleaved
and no arm is clustered in wall-clock time. Maintenance checkpoint order is ascending
and is **not** permuted: a maintainer's only memory of earlier checkpoints is the
artefact it already produced.

## 7. Tests

```bash
python test_r1_runner.py
```

75 tests, covering the original sixteen required gates plus v1.1 native-export and
orchestration gates: key never written · oracle exclusion · exact model-facing bundle
manifest verification · bundle digest mismatch ·
independent requests · no `previous_response_id` · duplicate-run refusal · restart-safe
retry-chain resume · corrupted raw detection · wrong model/runner/prompt/context
identity · retry classification · task versus infrastructure failure · transactional
symmetric infrastructure exclusion · immutable control artefacts · package-manifest
path safety · explicit parameter-capability binding · secret scanning · deterministic
manifest/archive. Plus sealed-protocol conformance: session counts, B-NULL share,
order determinism, arm interleaving, trajectory split, tool absence, record
completeness, `UNAVAILABLE` handling, neutral arm ids, maintainer task-blindness and
the temporal boundary.

The tests and review caught multiple runner defects before execution: early `--api-key`
refusal ordering, an unreachable `seal`, gzip filename leakage into the archive digest,
non-strict maintainer JSON repair, repeat-response collapsing, premature arm-map
unblinding, restart replay of infrastructure attempts, partial score inputs after a
symmetric-exclusion trigger, and sampling-control probes that existed but were not bound to the run condition, a
model-facing manifest verifier that incorrectly treated human-only `protocol/` files
as model inputs, and a self-referential `FILE-MANIFEST.txt` that made a second `seal`
change the raw-archive
digest. All were repaired before any model call.

## 8. v1.1 execution-plumbing invariant

The pre-outcome v1.1 amendment is intentionally narrower than a benchmark redesign.
The corpus, tasks, oracles, maintenance semantics, arm builders, response parser and
`score_one` predicate remain frozen. `verify_v1_1.py` compares those Rust function
bodies byte-for-byte against the original X0 HEAD before any commit is accepted.

The runner still performs **no scoring** and never reads `oracles/`. After execution,
`fehrest-r1 score-jsonl` can emit repeat-addressed deterministic score records for the
variance calculation; it delegates every outcome to the unchanged `score_one`.
