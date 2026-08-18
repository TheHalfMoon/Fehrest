# Ponytail — Final Pass (post-implementation)

`PONYTAIL_FINAL: PASS_WITH_TWO_RECORDED_DEVIATIONS`

The pre-implementation gate ([ponytail-gate.md](./ponytail-gate.md)) was a set of
promises. This is the audit of whether the code kept them. Both deviations found
are toward **less** code than promised, which still has to be recorded — a gate you
only check when it flatters you is not a gate.

## What was actually built

| Measure | Value |
|---|---|
| `PRODUCTION_LINES` | 2,488 |
| `INLINE_TEST_LINES` | 1,125 |
| `EXTERNAL_TEST_LINES` | 1,581 |
| `TEST_TO_PRODUCTION_RATIO` | 1.09 : 1 |
| `PACKAGES` | 1 |
| `DIRECT_DEPENDENCIES` | 5 |
| `BINARY_TARGETS` | 2 at Phase T (`fehrest`, `fehrest-bench`). **3 since Phase T-R1**: `fehrest`, `fehrest-bench-v0`, `fehrest-r1` — both benchmark binaries are research tooling and neither is part of the product surface |
| `UNSAFE_BLOCKS` | 0 (`unsafe_code = "forbid"` at the crate root) |
| `COMPILER_WARNINGS` | 0 |
| `CLIPPY_WARNINGS` (`--all-targets -D warnings`) | 0 |

Per-module production lines, largest first: `vault` 326 · `context` 304 ·
`temporal` 279 (+297 test) · `cli` 280 · `memory` 243 · `derived` 218 ·
`envelope` 192 · `identity` 185 · `locator` 152 · `lib` 123 · `main` 16.

`temporal.rs` carries more test than production code. That is the correct shape for
the module where a wrong answer is silent — a resolver that picks a plausible winner
instead of reporting `CONTRADICTION` fails without any symptom.

## DELETE list — verified absent, not merely unused

Each row was grepped across `src/`, `bench/` and `Cargo.toml`.

| Deleted capability | Verified | Evidence |
|---|---|---|
| `serde_yaml` | **absent** | No occurrence. Frontmatter is a 185-line bounded parser in `identity.rs` |
| Trait abstraction over the derived store | **absent** | `Derived` is a concrete struct; no `dyn`, no store trait |
| `ContextCompilerBuilder` | **absent** | `context::compile(&req, &items)` is the only construction path |
| Async runtime | **absent** | No `async`, no `tokio` |
| Migration framework | **absent** | No occurrence of `migrat*`. Derived state is rebuilt, never migrated |
| Logging framework | **absent** | No `log::`, no `tracing`. Diagnostics are `eprintln!` |
| Config file support | **absent** | Vault root is a CLI argument; no config reader exists |
| Incremental reindex | **absent** | Only `rebuild()` exists. The three `incremental` hits are comments recording the deferral and its consequence |
| `clap` | **absent** | One hit, in a comment naming the decision. Dispatch is hand-written in `cli.rs` |

A case-insensitive first pass flagged `log::` in `cli.rs` and `events.rs`. Both are
`EventLog::` — a false positive from the search, not a framework. Recorded because a
clean audit that silently drops its own false positives is not auditable.

## SHRINK list — measured against the promise

| Capability | Promised Phase T form | Built | Verdict |
|---|---|---|---|
| Memory types | 5 | 5 (`Fact`, `Decision`, `Constraint`, `Gotcha`, `State`) | **kept** |
| Event vocabulary | 6, one durability class | 6 | **kept** |
| Context sections | 6 | 6 | **kept** |
| CLI surface | 10 subcommands | 10 (`init` `add` `scan` `rebuild` `search` `read` `compile` `manifest` `events` `verify`) | **kept** |
| Scope selector | `vault` + `project` implemented; `objects` / `object_types` **present in the type, unused** | `vault` + `project` only — the unused dimensions were **not added** | **deviation D-1** |

### Deviation D-1 — unused scope dimensions were not carried

The gate allowed two dimensions to exist in the type while unused. The code does not
carry them.

This is the stricter reading of the same principle: an unused field is scaffolding
whether or not a gate blessed it, and a `Scope` with two dead fields would have made
`specificity_cmp` harder to reason about at exactly the point where partial-order
correctness matters (K-07, K-08). Adding them later is a struct field and a match
arm. **Reversal condition:** the first Phase-T requirement that needs object-level
or type-level scope. None has appeared.

### Deviation D-2 — one capability grew after the gate

`temporal::admissible_at` was added during implementation, replacing a direct call to
`Memory::is_authoritative` in the resolver's admission filter. It is +14 production
lines.

It is not a new feature. Acceptance scenario AS-2 (historical truth) was
**structurally unanswerable** without it: `is_authoritative` answers "in force now",
and using it for `as-of` queries made every superseded record invisible at every
point in valid time, including the interval it actually governed. The addition is the
minimum that makes an already-specified requirement reachable. **It was not added to
make a test pass** — it was added because the test proved the implementation was
wrong, and the alternative was deleting the requirement.

## Exclusion-list audit — nothing on the forbidden list was built

| Forbidden in Phase T | Present? |
|---|---|
| MCP server or client | No |
| Graph / Graphify / extraction | No |
| Vectors or embeddings | No |
| Automatic memory extraction or promotion | No |
| UI, editor, Tauri, React, v0 output | No |
| Plugin system | No |
| Collaboration or sync | No |
| Network I/O of any kind | No |
| Cedar / policy engine | No |
| `cap-std` | No |
| Telemetry | No |
| Commercial quota, tier, trial or lifetime limit | No — all bounds in `limits` are resource-safety bounds |

The last row is the one worth restating: `MAX_OBJECT_BYTES`, `MAX_STATEMENT_BYTES`,
`MAX_EVENT_BYTES`, `MAX_PACKAGE_BYTES`, `MAX_QUERY_BYTES` and `MAX_SEARCH_RESULTS`
exist so a hostile or runaway input cannot exhaust the machine. None of them counts
usage over time, and none of them can be raised by paying.

## Dependency admission — re-audited against what was actually used

| Crate | Version | Admitted for | Used for that? |
|---|---|---|---|
| `rusqlite` | 0.37.0 | Derived store + FTS5, bundled SQLite | Yes — `derived.rs` only |
| `serde` | 1.0.229 | Event and manifest serialization | Yes |
| `serde_json` | 1.0.151 | JSONL event records, manifest | Yes |
| `sha2` | 0.10.9 | Content hashes, event chain | Yes |
| `uuid` | 1.24.1 | UUIDv7 object identity | Yes |

`DIRECT_DEPENDENCIES = 5`, unchanged from admission. No dependency was added during
implementation. Four candidates rejected at the gate (`clap`, `serde_yaml`,
`cap-std`, Cedar) remain rejected and absent.

`RUSTSEC_STATUS = NOT_SCANNED_IN_THIS_ENVIRONMENT` — `cargo-audit` is not installed
here, so no vulnerability claim is made about these versions in either direction.

## What this pass does not claim

1. That the code is minimal. It claims the gate's specific promises were kept, and
   names the two places the result differs.
2. That 2,488 lines is the right size. It is the size that made the eight acceptance
   scenarios and 21 kill tests executable.
3. That the thesis holds. Nothing here measures the product question, and a
   well-shaped implementation of a false thesis is still a false thesis.
