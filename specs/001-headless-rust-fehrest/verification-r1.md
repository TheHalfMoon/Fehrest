# Technical Verification-Tail Closeout — Phase T-R1

`SCOPE: THE FOUR GAPS LEFT OPEN BY` [verification.md](./verification.md)
`PRODUCT_THESIS: UNTOUCHED BY THIS DOCUMENT`

Phase T closed with `PASS_WITH_ONE_TOOL_GAP_AND_ONE_HOST_CONSTRAINT`. Four things
were explicitly **not** claimed: formatting conformance, dependency-vulnerability
status, symlink containment on any platform, and any non-Windows behaviour. This
record closes three of them with execution evidence, narrows the fourth, and
documents one prior environment observation that **no longer reproduces**.

Nothing here says anything about the product thesis.

---

## A1 — `cargo fmt --check`

### The gap was a broken component state, not a missing component

Phase T recorded rustfmt as unavailable. The cause was more specific than "not
installed", and the distinction matters because it changes the fix:

```
$ rustup component list --installed
rustfmt-x86_64-pc-windows-msvc          <- rustup believes it is installed

$ cargo fmt --version
error: the 'cargo-fmt.exe' binary, normally provided by the 'rustfmt' component,
is not applicable to the 'stable-x86_64-pc-windows-msvc' toolchain

$ rustup component add rustfmt
info: component rustfmt is up to date   <- and refuses to repair it
```

`rustup`'s manifest and the toolchain's `bin/` directory disagreed: the component was
recorded as present while `cargo-fmt.exe` and `rustfmt.exe` were absent from
`~/.rustup/toolchains/stable-x86_64-pc-windows-msvc/bin/`. `rustup component add` is a
no-op in that state. The repair is remove-then-add:

```bash
rustup component remove rustfmt && rustup component add rustfmt
```

| Field | Value |
|---|---|
| `RUSTFMT_VERSION` | `1.9.0-stable (8bab26f4f6 2026-07-14)` |
| Installed as | **development tooling only** — `Cargo.toml` unchanged |

### The gate failed, and the failure was real

`cargo fmt --check` at `90205c1` **failed**: 52 diff hunks across 12 files.

| File | Hunks |
|---|---|
| `tests/integration.rs` | 13 |
| `src/temporal.rs` | 8 |
| `bench/harness.rs` | 6 |
| `src/context.rs` | 6 |
| `src/cli.rs` | 4 |
| `tests/kill_tests.rs` | 4 |
| `src/locator.rs` | 3 |
| `src/derived.rs`, `src/events.rs`, `src/memory.rs` | 2 each |
| `src/identity.rs`, `src/vault.rs` | 1 each |

Every hunk is standard rustfmt output in one of four classes: line wrapping at the
100-column boundary, removal of redundant braces around single-expression match arms,
trailing-comma normalisation, and one `use` list re-sorted (`TrustLevel` /
`Truncation` swapped — rustfmt sorts case-sensitively, so `Truncation` precedes
`TrustLevel`). No hunk changes a string literal, a numeric constant or control flow.

`cargo fmt` was run. The gate now passes.

### Why this is asserted to be semantics-neutral rather than assumed to be

rustfmt guarantees it, but the guarantee was checked rather than trusted, because this
change touches the exact binary the benchmark is about to freeze:

| Check | Result |
|---|---|
| `fehrest-bench` run **before** formatting, diffed against the committed `bench/results.txt` | byte-identical |
| `fehrest-bench` run **after** formatting, diffed against the same file | **byte-identical** |
| `cargo test` after formatting | 99 passed, 0 failed |
| `cargo clippy --all-targets --all-features -- -D warnings` after formatting | 0 warnings |

The benchmark harness is one of the reformatted files, so a formatting change that
perturbed behaviour would most likely surface there first. It did not.

**One measurable thing did change:** the release binary grew from 2,157,056 to
2,157,568 bytes. That is expected and is not a code change — panic metadata embeds
`file:line`, and reformatting moves lines. It is recorded because an unexplained
512-byte delta in a frozen candidate would otherwise look like one.

---

## A2 — RUSTSEC

`cargo-audit` was not present and was installed as external security tooling. It is
**not** a Fehrest dependency; `Cargo.toml` still declares five direct dependencies.

| Field | Value |
|---|---|
| `CARGO_AUDIT_VERSION` | `cargo-audit-audit 0.22.2` |
| Advisory DB commit | `2f08fbb85332687b721f2f22706d07448369451b` |
| Advisory DB date | `2026-08-18T10:23:07+02:00` — fetched the day of this run |
| Advisories loaded | 1,217 |
| Crates scanned (`Cargo.lock`) | 53 |
| `RUSTSEC_VULNERABILITIES` | **0** |
| `RUSTSEC_WARNINGS` | **0** — no unmaintained, no yanked, no unsound |

Run as `cargo audit --deny warnings`, which exits non-zero on any warning class, and it
exited 0. No advisory was suppressed, no `--ignore` was passed, and **no dependency was
updated** — the scan is against the locked graph exactly as the benchmark candidate
will use it. `cargo audit fix` was not run.

There is nothing to evaluate for applicability, because nothing was reported.

---

## A3 — K-12 symlink escape: **EXECUTED**

Phase T recorded K-12 as `PENDING_NATIVE_EXECUTION` on every platform. **It has now
executed on a real POSIX filesystem and it passes.** The historical non-evidence
observation is preserved unchanged in [kill-test-status.md](./kill-test-status.md);
this section adds to it rather than replacing it.

### Where it ran

| Field | Value |
|---|---|
| Host | WSL2 Ubuntu on the same Windows 11 machine |
| Kernel | `6.18.33.1-microsoft-standard-WSL2` |
| Filesystem | **ext4** on `/dev/sdd` — not `/mnt/c`, not DrvFs, not OneDrive |
| `RUSTC` | `1.97.0 (2d8144b78 2026-07-07)` |
| Symlink capability | **AVAILABLE** — verified by an independent `ln -s` probe before the suite ran |

The worktree was copied to `~/fehrest-linux-verify` on ext4 rather than built over
`/mnt/c`, because DrvFs symlink semantics are a Windows translation layer, and testing
containment against a translation layer would prove nothing about POSIX.

### The result

```bash
FEHREST_REQUIRE_NATIVE_FS=1 cargo test --test kill_tests
# test result: ok. 22 passed; 0 failed
```

`FEHREST_REQUIRE_NATIVE_FS=1` converts a capability skip into a panic. Passing under
that flag is therefore proof the early-return path was **not** taken: the symlink was
really created and the containment assertion really ran.

### Proving the assertion itself, not just the absence of a skip

A test can pass under the flag and still assert something vacuous. So the assertion was
mutated in the disposable Linux copy — inverted to expect a *non*-containment error —
and re-run:

```
thread 'k12_symlink_escape_fails' panicked at tests/kill_tests.rs:368:5:
symlink must be refused by containment, got Containment("symlink not followed: \"link.md\"")
test result: FAILED. 0 passed; 1 failed
```

The mutant fails, and the panic message carries the **real** error value produced by the
real containment path against a real symlink. The original assertion was then restored
and re-verified by digest against the repository copy
(`f1ecbc92e0c16eba55dc18af519111d736fd539b3884f848150182ea1088ffc0`, identical). The
mutation never touched the repository — only the temporary Linux tree.

`K12_WSL_LINUX_EXECUTED_PASS`.

### Windows native symlink is still not executed

```
New-Item -ItemType SymbolicLink ...
ERR: Administrator privilege required for this operation.
```

`HKLM:\...\AppModelUnlock` is absent (Developer Mode off) and the session is not
elevated. Per the standing directive, **neither was changed to make a test pass, and
elevation was not requested.** On Windows the honesty flag still reports the true
state:

```bash
FEHREST_REQUIRE_NATIVE_FS=1 cargo test --test kill_tests
# test result: FAILED. 22 passed; 1 failed  <- k12_symlink_escape_fails
```

`K12_WINDOWS_NATIVE_PENDING_CAPABILITY`. K-13 (junction) executed natively on Windows
and is a **different** attack; it does not substitute for K-12, and no claim of complete
Windows symbolic-link coverage is made.

### Full Linux suite

| Suite | Tests | Result |
|---|---|---|
| Unit | 66 | pass |
| Acceptance | 10 | pass |
| Kill tests | 22 | pass |
| **Total** | **98** | **0 failures** |

98, not 99: `k13_windows_directory_reparse_escape_fails` is `#[cfg(windows)]` and does
not exist on Linux. `cargo check`, `cargo clippy -D warnings` and `cargo fmt --check`
also pass on Linux.

**Scope of the Linux claim:** WSL2 is a genuine Linux kernel on a genuine ext4 volume,
which is what the symlink attack needs. It is not bare-metal Linux and it is not a
distribution matrix. macOS remains `PENDING_MACOS_EXECUTION` — nothing has run there and
nothing is claimed.

---

## A4 — Release build: the recorded host constraint **no longer reproduces**

Phase T recorded that `cargo build --release` failed inside the OneDrive-synced repo
path with a Windows Application Control block (`os error 4551`) on the `zmij` and
`libsqlite3-sys` build scripts.

**That failure did not recur.** The in-repo release build now succeeds:

| Configuration | Result | Artefact |
|---|---|---|
| `cargo build --release`, target dir **inside** the OneDrive repo path | **PASS** | `target/release/fehrest.exe`, 2,157,568 bytes |
| `CARGO_TARGET_DIR=C:\Users\Shehr\AppData\Local\Temp\fehrest-rt cargo build --release` | **PASS** | same size |
| `cargo test --release` | **PASS** | 99 passed, 0 failed |

`PROJECT_SOURCE_PATH: C:\Users\Shehr\OneDrive\Desktop\Fehrest`
`RELEASE_BUILD_TARGET_PATH: C:\Users\Shehr\AppData\Local\Temp\fehrest-rt` (and in-repo)

### How to read a failure that stopped failing

The Phase T observation is **not** retracted and **not** deleted. It was a real observed
failure with a real error code. What changed is host state — an Application Control
policy is dynamic, and a block that depended on a binary's reputation or on a policy
refresh can lift without anything in the repository changing.

The honest status is therefore:

> The OneDrive-path release build **failed during Phase T** and **succeeded during
> Phase T-R1**, with no intervening repository change that could explain either. The
> constraint is **environmental and non-deterministic**, not a property of the project.

The practical consequences are unchanged and still hold:

1. No `CARGO_TARGET_DIR` workaround is committed. Baking one machine's antivirus posture
   into the build configuration was wrong when the block was active and is more obviously
   wrong now that it is not.
2. Benchmark latency figures must still come from a release binary and must still say
   which target path produced it — because the block **may return**, and a run that
   silently fell back to a `dev` build would be unrepresentative.

---

## Closeout gate — all gates, both platforms

| Gate | Windows 11 (`x86_64-pc-windows-msvc`) | Linux (WSL2 ext4) |
|---|---|---|
| `cargo check --all-targets` | **PASS** | **PASS** |
| `cargo clippy --all-targets --all-features -- -D warnings` | **PASS** (0 warnings) | **PASS** (0 warnings) |
| `cargo test` | **PASS** — 99/99 | **PASS** — 98/98 |
| `cargo test --release` | **PASS** — 99/99 | not run |
| `cargo fmt --check` | **PASS** | **PASS** |
| `cargo build --release` | **PASS** | not run |
| `cargo audit --deny warnings` | **PASS** — 0 vulns, 0 warnings | n/a (same lockfile) |
| Native filesystem kill tests | K-13 **executed**; K-12 **pending capability** | K-12 **executed** |

### Status token

```
PHASE_T_TECHNICAL_CORE_PASS_WITH_PLATFORM_EVIDENCE_PENDING
```

**`FULL_CROSS_PLATFORM_PASS` is not claimed.** What is missing, precisely:

1. macOS — nothing has ever run there.
2. Windows native symbolic links — K-12 has not executed on Windows.
3. Bare-metal Linux, and any distribution other than the one WSL2 image.

### What is now claimed that was not before

| Phase T | Phase T-R1 |
|---|---|
| Formatting **unverified** | `cargo fmt --check` passes on two platforms |
| `RUSTSEC_STATUS = NOT_SCANNED_IN_THIS_ENVIRONMENT` | 0 vulnerabilities, 0 warnings, against a same-day advisory DB |
| K-12 containment **never executed anywhere** | Executed on ext4; assertion proven live by mutation |
| `PENDING_LINUX_EXECUTION` | 98 tests executed natively on Linux |
| Release build blocked in-repo | Builds in both locations; the block is environmental and intermittent |

Item 5 of Phase T's "what is not claimed" list stands unchanged and always will: **none
of this establishes that Fehrest is secure.** It establishes that 22 named attacks were
constructed and failed.
