# Implementation Plan — Headless Rust Fehrest Thesis-Proof

**Branch**: `001-headless-rust-fehrest` (on `main`) · **Date**: 2026-08-18 · **Spec**: [spec.md](./spec.md) · **Clarify**: [clarify.md](./clarify.md)

## Summary

One Rust package, `fehrest`, exposing a headless CLI. It admits Markdown files into a vault under explicit UUID identity, maintains a rebuildable SQLite+FTS5 derived index, records explicit durable memories with four orthogonal semantic axes and bitemporal fields, resolves current state deterministically, and compiles bounded provenance-labelled context packages with a permanent served-item manifest. Every agent-visible read carries a typed trust envelope. A benchmark harness compares this against four baselines on continuation tasks.

## Technical context

| | |
|---|---|
| **Language** | Rust stable 1.97.1 |
| **Storage** | Canonical: Markdown + YAML frontmatter on disk. Derived: SQLite with FTS5 |
| **Testing** | `cargo test` — unit tests beside behaviour, integration tests in `tests/` |
| **Platform** | Windows 11 native (development host). Linux/macOS via portable code; **platform claims only where executed** |
| **Project type** | Single package, CLI binary + library |
| **Performance** | No budget frozen for Phase T; context compile on a fixture vault should stay interactive (sub-second) |
| **Constraints** | No network, no model, no server, no async, no `unsafe` |
| **Scale** | Fixture vaults of tens to low hundreds of files. Not a scale test |

## Constitution check

| Principle | How the design satisfies it |
|---|---|
| I local-first | No network code path exists. Tests run offline |
| II Rust owns Core | Single Rust package; no other language in the product |
| III open canonical | Canonical = Markdown files the user can read without Fehrest |
| IV path ≠ identity | `ObjectId` is a UUID type; paths are `Locator`, a separate type that cannot be converted into an id |
| V content is evidence | Content is a `String` field inside a typed envelope; never parsed as metadata |
| VI derived has no authority | Scope checks read canonical frontmatter; index rows are hints. Two independent guarantees implemented separately |
| VII temporal separate | `valid_from`/`valid_until` and `recorded_seq` are distinct fields with distinct query paths |
| VIII orthogonal axes | Four separate enums, four separate columns. No combined status type exists |
| IX manifest = emitted | Manifest is built in the emit loop, from what was emitted |
| X envelope everywhere | One `Envelope<T>` type; every agent-visible return is `Envelope`-wrapped |
| XI honest boundaries | No auth subsystem. Docs state OS-account root of trust |
| XII single writer | Lock acquired at vault open for write operations |
| XIII resource safety | Byte caps on input, item, package, event. No quota concept |
| XIV allowlist | `is_supported()` allowlist; `.git`/`.fehrest` excluded |
| XV Ponytail | [ponytail-gate.md](./ponytail-gate.md) |
| XVI gated systems out | No graph/vector/CRDT/MCP/Cedar module exists |
| XVII falsifiable | Benchmark harness reports measured results including negative |

**Violations:** none.

## Project structure

```
Cargo.toml                    single package, no workspace
src/
  main.rs                     CLI entry
  lib.rs                      module wiring, public error type
  vault.rs                    root, admission allowlist, single-writer lock
  identity.rs                 ObjectId (UUIDv7), frontmatter parse/serialize
  locator.rs                  root-confined resolution + post-open verification
  derived.rs                  SQLite schema, hardening, rebuild, FTS5 search
  memory.rs                   memory record, four axes, scope selector
  temporal.rs                 deterministic resolver, supersession graph validation
  events.rs                   hash-chained append-only event log
  envelope.rs                 typed trust envelope + length-prefixed serialization
  context.rs                  bounded compiler, budget atomicity, manifest
  cli.rs                      command dispatch
tests/
  kill_tests.rs               G3 kill tests for implemented surfaces
  integration.rs              end-to-end scenarios from spec.md
bench/
  harness.rs (bin)            baseline comparison harness
  fixtures/                   temporal fixture corpus with ground truth
```

**Structure decision.** One package. No crate split: no security boundary is enforced by crate separation here (the security boundaries are function-level and tested as such), no independent versioning is needed, and no process separation exists. Splitting would be scaffolding.

## Dependency plan

Full records in [dependencies.md](./dependencies.md). Summary:

| Dependency | Why not std |
|---|---|
| `rusqlite` (bundled SQLite) | Implementing SQLite is not a Ponytail option; bundled avoids a system-library dependency and pins the engine |
| `uuid` (v7) | UUIDv7 requires a monotonic time-ordered generator; hand-rolling identity generation is security-sensitive |
| `sha2` | Hash chaining and content hashes; hand-rolling SHA-256 is forbidden by Ponytail's exclusion list |
| `serde` + `serde_json` | Manifest and envelope serialization; hand-rolling JSON escaping is the exact class of bug the envelope exists to avoid |
| `serde_yaml` **rejected** | Frontmatter parsing is a small, bounded, key-value subset — see dependencies.md |

**No async runtime.** No concurrency exists in Phase T beyond the single-writer lock.

## Phase sequence

Implementation follows the frozen T1–T16 order, in four commits:

1. **Foundation** (T1–T9) — vault, identity, conflict, locator, post-open verification, scope, SQLite, rebuild, FTS.
2. **Memory and time** (T10–T12) — explicit memory, resolver, supersession validation, event chain.
3. **Envelope and compiler** (T13–T15) — trust envelope, manifest, bounded compiler.
4. **Tests, kill tests, harness** (T16) — integration, G3 kill tests, benchmark harness.
