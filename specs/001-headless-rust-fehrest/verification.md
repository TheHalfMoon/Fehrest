# Technical Verification Record — Phase T

`TECHNICAL_IMPLEMENTATION: PASS_WITH_ONE_TOOL_GAP_AND_ONE_HOST_CONSTRAINT`

**This record covers SC-001…SC-005 only.** It says nothing about the product thesis.
`cargo test` passing means `TECHNICAL_IMPLEMENTATION_PASS`; it does not mean
`PRODUCT_THESIS_PASS`, and no result below should be read as evidence about the
thesis in either direction.

## Environment

| Field | Value |
|---|---|
| `HOST_OS` | Microsoft Windows 11, build 10.0.26200.9168 |
| `TARGET` | `x86_64-pc-windows-msvc` |
| `RUSTC` | 1.97.1 (`8bab26f4f`, 2026-07-14) |
| `LLVM` | 22.1.6 |
| `REPO_PATH` | `C:\Users\Shehr\OneDrive\Desktop\Fehrest` (OneDrive-synced) |

## SC-001 — build and lint gates

| Gate | Result | Notes |
|---|---|---|
| `cargo check --all-targets` | **PASS** | 0 warnings |
| `cargo clippy --all-targets -- -D warnings` | **PASS** | 0 warnings |
| `cargo test` (dev) | **PASS** | 99 tests, 0 failures |
| `cargo test --release` | **PASS** | 99 tests, 0 failures |
| `cargo fmt --check` | **NOT_RUN** | See tool gap below |
| `cargo build --release` (in-repo target dir) | **BLOCKED** | See host constraint below |
| `cargo build --release` (target dir outside OneDrive) | **PASS** | 2,157,056-byte `fehrest.exe` produced |

**SC-001 is therefore reported as PASS on three of four gates, with `cargo fmt
--check` NOT_RUN rather than passed.** The criterion as written is not fully met and
is not claimed to be.

### Tool gap — `rustfmt` is not installed

```
error: the 'cargo-fmt.exe' binary, normally provided by the 'rustfmt' component,
is not applicable to the 'stable-x86_64-pc-windows-msvc' toolchain
```

`cargo fmt --check` **did not run**. Formatting is therefore unverified, not
verified-and-clean. Nothing was reformatted to hide this. Resolving it is
`rustup component add rustfmt`, which is a host action, not a code change.

### Host constraint — release builds are blocked inside the OneDrive path

```
error: failed to run custom build command for `zmij v1.0.23`
  An Application Control policy has blocked this file. (os error 4551)
```

The same failure occurs for `libsqlite3-sys v0.35.0`. A Windows Application Control
policy blocks **executing newly compiled build-script binaries** out of
`target/release/` under the OneDrive-synced repository path.

The block is path-scoped, not code-scoped. With the target directory outside
OneDrive, the release build and the full release test suite both succeed:

```bash
CARGO_TARGET_DIR=/c/Users/Shehr/AppData/Local/Temp/fehrest-rt cargo build --release
```

This is recorded rather than worked around in-repo: committing a `.cargo/config.toml`
that redirects the target directory would bake one machine's antivirus posture into
the project's build configuration.

**Consequence for the benchmark:** timing measured on a `dev` build would be
unrepresentative, so any latency figure must come from the release binary built via
the path above, and must say so.

## SC-002 — kill tests

| Metric | Value |
|---|---|
| Roster entries | 25 |
| `EXECUTED_AND_PASSED` | 21 |
| `PENDING_NATIVE_EXECUTION` | 1 — K-12 (symlink escape) |
| `DEFERRED_SURFACE_NOT_PRESENT` | 3 — K-01, K-03, K-19 |
| Falsely claimed as `PASS` | 0 |

Full detail, including why a green `cargo test` line for K-12 is not evidence:
[kill-test-status.md](./kill-test-status.md).

**SC-002 as written requires every applicable kill test for an implemented surface to
pass.** K-12's surface *is* implemented, so K-12 is applicable and did not execute.
SC-002 is therefore **PASS with one unexecuted applicable test**, not a clean pass.

## SC-003 — rebuildability

`as8_deleting_derived_state_entirely_and_rebuilding_is_equivalent` deletes
`derived.sqlite` together with any `-wal` / `-shm` companions, asserts the file is
really gone, then rebuilds from canonical files alone and checks:

- canonical object count and conflict count unchanged
- derived object count restored
- lexical query results identical, element by element
- the authority path (`authoritative_project`) returns the same answer, still via
  post-open UUID verification
- the event chain untouched and still `Intact` — events are canonical, not derived
- canonical bytes still verify by identity after the rebuild

**PASS.**

## SC-004 — current-state resolution against known ground truth

The temporal fixture in [tests/integration.rs](../../tests/integration.rs) is
hand-written with its ground-truth table stated **before** any resolver runs against
it, so the test is not circular. Valid-time intervals are half-open
`[valid_from, valid_until)`; `d1` ends exactly where `d2` begins.

| as-of day | expected | result |
|---|---|---|
| 0 | `NO_ANSWER` | `NO_ANSWER` |
| 10 | `d1` (Postgres) | `d1` |
| 39 | `d1` (Postgres) | `d1` |
| 40 | `d2` (SQLite) | `d2` |
| now | `d2` (SQLite) | `d2` |

**PASS — after fixing a real implementation defect that this criterion exposed.**
The resolver admitted candidates through `Memory::is_authoritative`, which answers
"in force *now*". Historical resolution asks "in force *then*". Every `SUPERSEDED`
record was invisible at every point in valid time, making AS-2 structurally
unanswerable. The fix is `temporal::admissible_at`, and the conservative rung —
`SUPERSEDED`/`EXPIRED` admitted only when `valid_until` is recorded — is what keeps
K-10 true. No invariant was weakened and no assertion was relaxed.

## SC-005 — platform honesty

| Claim | Made? |
|---|---|
| `WINDOWS PASS` | Made, and earned: the suite executed natively on Windows 11, and K-13 really constructed a directory junction |
| `MACOS PASS` | **Not made.** `PENDING_MACOS_EXECUTION` |
| `LINUX PASS` | **Not made.** `PENDING_LINUX_EXECUTION` |
| K-12 symlink containment | **Not claimed on any platform.** `PENDING_NATIVE_EXECUTION` |

`FEHREST_REQUIRE_NATIVE_FS=1` exists so an unexecuted filesystem test fails loudly
instead of printing `ok`. On this host that run reports 22 passed / 1 failed, and
that is the honest number.

**PASS.**

## Test inventory

| Suite | Tests |
|---|---|
| Unit (inline `#[cfg(test)]`) | 66 |
| Acceptance (`tests/integration.rs`, AS-1…AS-8 + 2 cross-cutting) | 10 |
| Kill tests (`tests/kill_tests.rs`) | 23 |
| **Total** | **99** |
| Failures | 0 |

## SC-006…SC-008 — thesis criteria

`NOT_YET_EVALUATED`. `bench/harness.rs` is a stub that prints
`benchmark harness: not yet implemented`. T032, T033 and T034 are open. No thesis
claim exists yet, positive or negative.

## Summary of what is not claimed

1. Formatting conformance — `cargo fmt --check` never ran.
2. Symlink containment on any platform — K-12 never executed.
3. Any macOS or Linux behaviour — nothing ran there.
4. Dependency vulnerability status — `cargo-audit` is not installed;
   `RUSTSEC_STATUS = NOT_SCANNED_IN_THIS_ENVIRONMENT`.
5. That Fehrest is secure — 21 named attacks failed, which is a different statement.
6. Anything about the product thesis.
