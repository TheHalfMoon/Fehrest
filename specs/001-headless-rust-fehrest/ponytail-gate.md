# PONYTAIL_PHASE_T_GATE

**Status:** COMPLETE (pre-implementation) · **Date:** 2026-08-18

Every non-trivial capability classified `KEEP` / `SHRINK` / `REUSE` / `DELETE` / `DEFER`, answering in order: does it need to exist for Phase T? · already implemented? · Rust `std`? · platform primitive? · approved dependency? · smaller solution? · then minimum correct code.

> **Exclusion list — Ponytail may never minimise:** authorization · vault containment · UUID identity verification · durable-state correctness · recovery · audit integrity · provenance · security metadata · bounds · platform correctness · required tests.
>
> On those paths, question 1 is answered **yes by the constitution**, and only *how small* is open.

---

## KEEP — needed, minimum form

| Capability | Q1 needed? | Answer | Minimum form |
|---|---|---|---|
| Vault root + admission allowlist | Yes — FR-001..003, F-CORE-16 | std | One `is_supported()` extension check + two reserved-prefix exclusions |
| Object identity (UUIDv7 in frontmatter) | Yes — FR-004, F-CORE-04 | `uuid` crate (excluded from minimisation: identity) | Newtype over `Uuid`, one generator call |
| Duplicate-UUID conflict | Yes — FR-006, K-11 | std | A `HashMap<ObjectId, Vec<Locator>>` check during scan; conflict is a returned error, both paths retained |
| Root-confined resolution | Yes — FR-007, **exclusion list: containment** | std | Component rejection → join → open → `symlink_metadata` check → canonical parent-chain check |
| Post-open UUID verification | Yes — FR-008, **exclusion list: identity verification** | std | Read from the opened handle, parse frontmatter, compare, fail closed |
| SQLite derived index | Yes — FR-010 | `rusqlite` | One table + one FTS5 virtual table. No ORM, no migration framework |
| SQLite hardening | Yes — FR-012, **exclusion list: security** | rusqlite flags | Open flags without extension loading; `trusted_schema=OFF`; vault-rooted path |
| Literal FTS query construction | Yes — FR-013, K-17 | std | Quote-and-escape into a phrase; length bound; result cap |
| Explicit memory record | Yes — FR-015..018 | std types | Four enums, bitemporal fields, scope struct, provenance struct |
| Deterministic resolver | Yes — FR-019, the thesis | std | The five-rung ladder from F §4.2, terminating in `CONTRADICTION` |
| Supersession graph validation | Yes — FR-021, K-10 | std | Cycle detection via visited-set walk; five invalid-edge classes |
| Event chain | Yes — FR-023, **exclusion list: audit integrity** | `sha2` | Append JSONL line with `prev_hash`/`hash`; six event types |
| Single-writer lock | Yes — FR-024, K-24, **exclusion list: durable-state correctness** | std `create_new` | Lock file with PID; visible failure; no auto-steal |
| Trust envelope | Yes — FR-025..026, **exclusion list: security metadata** | std + serde | One generic `Envelope<T>`; length-prefixed model-visible form |
| Context compiler | Yes — the thesis itself | std | Identity seed → FTS candidates → temporal filter → scope filter → budget fill → manifest |
| Budget atomicity | Yes — FR-028, K-20, **exclusion list: bounds** | std | Measure envelope + content; if envelope alone exceeds remaining, `OMITTED` |
| Served-item manifest | Yes — FR-029, F-CORE-09 | serde | Built inside the emit loop from emitted items |
| Resource bounds | Yes — FR-031, K-24b, **exclusion list: bounds** | std | Four constants + explicit errors |
| CLI | Yes — FR-030 | std `env::args` | Hand-rolled dispatch; ~10 subcommands |

---

## SHRINK — needed, smaller than specified elsewhere

| Capability | Full architecture | Phase T form | Why |
|---|---|---|---|
| Scope selector | Four dimensions ([F §3.4](../../docs/05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice)) | `vault` + `project` implemented; `objects`/`object_types` present in the type, unused | K-07 and K-08 are fully exercised by two dimensions. Implementing unused dimensions is scaffolding |
| Event vocabulary | 20+ types across three tiers ([D §5.2](../../docs/03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)) | Six types, one durability class | Tiering is unfrozen pending B-0. Implementing a tiering engine against an unmeasured volume is guessing |
| Memory types | Ten + `unclassified` ([F §3.2](../../docs/05-MEMORY-MODEL.md#32-memory-types)) | Five: `fact`, `decision`, `constraint`, `gotcha`, `state` | These five carry the benchmark's measured dimensions. The rest add vocabulary without adding a tested property |
| Context sections | Twelve ([H §3](../../docs/07-CONTEXT-COMPILER-SPEC.md#3-output)) | Six: constraints, state, decisions, gotchas, superseded, contradictions | Matches the benchmark's measured dimensions exactly |
| CLI surface | Full product CLI | Ten subcommands | "Do not build a giant CLI" |

---

## REUSE

| Need | Reused from |
|---|---|
| SHA-256 | `sha2` — hand-rolling forbidden (audit integrity) |
| UUIDv7 | `uuid` — hand-rolling forbidden (identity) |
| SQLite + FTS5 | `rusqlite` bundled |
| JSON | `serde_json` — hand-rolling escaping forbidden (security metadata) |
| Frontmatter parsing | **Not** reused — see DELETE below |

---

## DELETE — considered and removed

| Considered | Deleted because |
|---|---|
| `serde_yaml` for frontmatter | A general YAML parser is a large parsing surface over attacker-influenced content (T-17) to gain nothing over a ~40-line bounded subset parser. **This is choosing the smaller attack surface, not minimising a control** |
| Trait abstraction over the derived store | One implementation. A trait would be scaffolding for a swap that is not planned |
| `ContextCompilerBuilder` | One construction path. A builder for one shape is ceremony |
| Async runtime | No concurrency exists |
| Migration framework | No schema history exists. Derived state is rebuilt, never migrated ([M §1 rule 4](../../docs/12-MIGRATION-SCHEMA-EVOLUTION.md#1-governing-rules)) |
| Logging framework | `eprintln!` reaches the requirement. A framework is a dependency for a diagnostic |
| Config file support | The vault root is a CLI argument. Config is a product concern |
| Incremental reindex | `YAGNI_DEFERRED` — full rebuild only. **Recorded consequence:** B-12's incremental-vs-fresh comparison cannot run, and is reported as untested rather than passed |
| `clap` | Ten subcommands with simple arguments. Hand dispatch is ~60 lines and removes a proc-macro dependency tree |

---

## DEFER — real, not now

| Deferred | Gate |
|---|---|
| Graph, vectors, embeddings | [GI-CAP B-13](../../docs/10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) — capability must earn integration |
| Automatic memory extraction/promotion | [B-5](../../docs/10-BENCHMARK-PLAN.md#b-5--memory-promotion-quality); unauthorized in Phase T |
| MCP, Cedar | Later multi-actor authorization gate |
| CRDT, sync, collaboration | [Collaboration/CRDT Gate](../../docs/20-FUTURE-GATES.md#4-collaborationcrdt-gate) |
| UI, editor, canvas | UI gate; unauthorized |
| cap-std | Re-evaluate if std proves insufficient — it did not |
| T2/T3 compaction | Pending [B-0](../../docs/10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) |
| PDF/DOCX/OCR/audio ingestion | Future ingestion gates |

---

## Exclusion-list audit

Confirming nothing on the protected list was minimised away:

| Protected | Present in Phase T? |
|---|---|
| Authorization | Yes — scope check before emission, deny-by-default |
| Vault containment | Yes — independent of identity verification |
| UUID identity verification | Yes — post-open, from the opened handle |
| Durable-state correctness | Yes — single-writer lock, atomic writes |
| Recovery | Yes — derived state rebuildable; canonical survives derived deletion |
| Audit integrity | Yes — hash-chained event log |
| Provenance | Yes — evidence links + served-item manifest |
| Security metadata | Yes — envelope on every agent-visible read, budget-atomic |
| Bounds | Yes — four resource limits, explicit errors |
| Platform correctness | Yes — per-platform path tests, honest status marking |
| Required tests | Yes — kill tests are implementation gates, not documentation |

**`PONYTAIL_GATE_COMPLETE = YES`**
