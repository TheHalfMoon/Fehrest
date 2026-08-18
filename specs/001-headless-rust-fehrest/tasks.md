# Tasks — Headless Rust Fehrest Thesis-Proof

**Input:** [spec.md](./spec.md) · [plan.md](./plan.md) · [clarify.md](./clarify.md) · [ponytail-gate.md](./ponytail-gate.md)

Vertical slices. Tests live beside behaviour. **No future scaffolding** — no task prepares plugin, UI, graph or collaboration architecture.

---

## Slice 1 — Foundation (T1–T9)

- [x] **T001** `Cargo.toml`: single package `fehrest`, admitted dependencies only, `[lints] unsafe_code = "forbid"`
- [x] **T002** `src/identity.rs`: `ObjectId` newtype over UUIDv7; bounded frontmatter parse/serialize preserving unknown lines byte-for-byte *(CL-04)*
- [x] **T003** `src/vault.rs`: vault root, `is_supported()` allowlist, `.fehrest/`+`.git/` exclusion *(CL-57..60)*
- [x] **T004** `src/vault.rs`: single-writer lock via `create_new`, PID recorded, visible failure, no auto-steal *(CL-51..53)*
- [x] **T005** `src/locator.rs`: root-confined resolution — component rejection, join, open, symlink check, parent-chain verification *(CL-11..15)*
- [x] **T006** `src/locator.rs`: post-open UUID verification from the opened handle; fail closed on mismatch *(CL-16..17)*
- [x] **T007** `src/vault.rs`: scan with duplicate-UUID conflict detection, both paths retained *(CL-18)*
- [x] **T008** `src/derived.rs`: SQLite open with hardening — no extension loading, `trusted_schema=OFF`, vault-rooted path *(CL-20..22)*
- [x] **T009** `src/derived.rs`: schema (objects + FTS5), full rebuild from canonical, corrupt-DB discard *(CL-05, CL-06, CL-23)*
- [x] **T010** `src/derived.rs`: literal FTS `MATCH` construction, input bound, result cap *(CL-25..27)*
- [x] **T011** Tests for slice 1 beside behaviour

## Slice 2 — Memory and time (T10–T12)

- [x] **T012** `src/memory.rs`: memory record with four orthogonal axes, bitemporal fields, scope selector, provenance; `basis` core-assigned *(CL-33, CL-36)*
- [x] **T013** `src/memory.rs`: scope match + dimension-wise intersection + partial-order specificity *(CL-07)*
- [x] **T014** `src/temporal.rs`: five-rung deterministic resolver → winner / `CONTRADICTION` / `NO_ANSWER`; confidence excluded *(CL-29..33)*
- [x] **T015** `src/temporal.rs`: `as-of` historical resolution *(CL-30)*
- [x] **T016** `src/temporal.rs`: supersession graph validation — five invalid-edge classes *(CL-34, CL-35)*
- [x] **T017** `src/events.rs`: hash-chained append-only log, six event types, verification *(CL-37, CL-38)*
- [x] **T018** Tests for slice 2 beside behaviour

## Slice 3 — Envelope and compiler (T13–T15)

- [x] **T019** `src/envelope.rs`: typed `Envelope<T>` with identity, trust, provenance, temporal, supersession, scope, truncation *(CL-42)*
- [x] **T020** `src/envelope.rs`: length-prefixed model-visible serialization; content cannot forge fields *(CL-43, CL-44)*
- [x] **T021** `src/context.rs`: bounded compiler — seed, candidates, temporal filter, scope filter, budget fill *(CL-49)*
- [x] **T022** `src/context.rs`: budget atomicity — `FULL`/`TRUNCATED`/`OMITTED`, envelope never stripped *(CL-47, CL-48)*
- [x] **T023** `src/context.rs`: served-item manifest built in the emit loop; package digest *(CL-39, CL-41)*
- [x] **T024** `src/context.rs`: evidence-claim verification against manifest — in-scope-but-not-served rejected *(CL-40)*
- [x] **T025** `src/lib.rs` resource bounds: request, item, package, event size *(CL-54..56)*
- [x] **T026** `src/cli.rs` + `src/main.rs`: ten subcommands, hand dispatch
- [x] **T027** Tests for slice 3 beside behaviour

## Slice 4 — Kill tests and harness (T16)

- [x] **T028** `tests/kill_tests.rs`: K-02, K-04, K-05, K-06, K-07, K-08, K-10, K-11
- [x] **T029** `tests/kill_tests.rs`: K-12, K-13, K-14, K-15, K-16, K-17, K-18
- [x] **T030** `tests/kill_tests.rs`: K-20, K-21, K-22, K-23, K-24, K-24b
- [x] **T031** `tests/integration.rs`: the eight acceptance scenarios from spec.md
- [x] **T032** `bench/fixtures/`: temporal corpus with ground truth — decisions, supersessions, constraints, gotchas
- [x] **T033** `bench/harness.rs`: arms B0, B1, B3, B4, B5; shared task definition; no metadata leakage *(CL-61..63)*
- [x] **T034** Run harness; record results as measured, including negative *(CL-64, CL-65)*

## Verification

- [x] **T035** `cargo fmt --check`, `cargo check`, `cargo clippy -D warnings`, `cargo test`
- [x] **T036** Checklist verification pass; `analyze.md` and `ponytail-final.md`

---

**Removed before implementation** (would have been unauthorized scaffolding): plugin architecture prep · UI architecture prep · graph extension prep · collaboration support prep · incremental reindex infrastructure · migration framework · config system · logging framework.
