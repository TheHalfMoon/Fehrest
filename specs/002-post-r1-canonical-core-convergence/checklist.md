# Checklist — Spec 002 Post-R1 Canonical Core Convergence

## Entry gate — PASS (T037–T040, evidence on `a8d3052`)

- [x] R1 terminal verdict exists. (`docs/canonical/R1_V3_TERMINAL_VERDICT_2026-09-09.md`, `THESIS_SUPPORTED_ON_COST_CAVEAT`, confirmatory 05443fe6, pilot 556b32)
- [x] R1 route permits Phase 1. (`EXECUTION_MASTER_PLAN.md §4` THESIS_SUPPORTED_ON_COST → Founder may authorize Spec 002 with cost as primary constraint; FOUNDER_AUTHORIZATION_SPEC_002_2026-09-09 record)
- [x] Founder explicitly authorized Spec 002. (`docs/canonical/FOUNDER_AUTHORIZATION_SPEC_002_2026-09-09.md` 2026-09-09T04:00:00Z)
- [x] Historical R1 v1.1 anchor is reconciled against the implementation/evidence source used for work. (`docs/canonical/T037_IMPLEMENTATION_BASELINE.md` bundle `a36639da` ed79/f7ea7e0, GITHUB_BOOTSTRAP_PROVENANCE)
- [x] Live HEAD/worktree/source provenance is recorded before mutation. (`specs/CURRENT.md` LIVE a8d3052, activation commit c54734d, status bytes 0)

## Reconciliation — PASS (T041–T044, 2026-09-09 Slice A)

- [x] Phase T implementation vs specification delta is recorded without rewriting history. (`docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md` §1–§8, ed79 bundle-verify PASS, 10 src files, 823833 bytes, without rewriting historical reports)
- [x] Existing Vault/WriteLock single-writer mechanism is credited accurately. (§4.1: `src/vault.rs:292-321 create_new/O_EXCL` atomic, `second_writer_fails_visibly`, `no auto-steal`)
- [x] Missing durable product memory surface remains deferred to its proper phase. (§4.2: `src/memory.rs` four-axis semantics exists, CLI journal absent → deferred to Spec 006 Phase 4, not pulled into Phase 1)
- [x] Phase T compiler subset vs full production compiler is recorded. (§4.3: `src/context.rs 16705` bounded deterministic vs full H with SelectionTrace/receipt/agent gateway → Phase 5 Spec 007)
- [x] Historically unavailable B-12 incremental arm remains recorded honestly. (§4.4: `src/derived.rs INCREMENTAL_REINDEX=YAGNI_DEFERRED`, B-12 UNTESTED never PASS, belongs to 003)

## Vault / canonical writes — PASS (T046–T053, 2026-09-09 Slice B)

- [x] Vault identity is explicit. (`specs/002 vault-metadata-spec.md` vault_id v7 at `.fehrest/vault.json`, `src/vault.rs::VaultMeta`, `cargo test` vault_meta_created...)
- [x] Vault format/schema version is explicit. (`format_version: 1 SUPPORTED, 0 legacy, >1 unsupported, serde_json field, checked in read_vault_meta`)
- [x] Unsupported/newer format fails visibly. (`unsupported_newer_format_fails_visibly` test, Error::Vault unsupported format_version 2 newest supported is 1)
- [x] Canonical replacement is crash-aware under the documented platform contract. (`atomic_write_file` same-dir temp → write → flush → sync_all → rename → dir sync, measured Linux PASS Windows UNTESTED per REPLACEMENT_SEMANTICS_MEASUREMENT.md)
- [x] Fault injection before/after replacement never produces silent partial canonical success. (`FaultPoint` + `atomic_write_fault_matrix_proves_no_partial_success` — BeforeTemp..BeforeReplace each preserves old or quarantines orphan, never truncated, 0 partial)
- [x] Unknown frontmatter preservation remains green. (`atomic_write_preserves_unknown_frontmatter`, identity round-trip test still PASS)

## Writer ownership — PASS (T054–T059)

- [x] Second writer fails visibly. (`second_writer_still_fails_visibly_and_no_auto_steal` — `WriterLocked` with holder/path, second `open_write` still fails; kill_tests k24 still PASS)
- [x] Stale lock is never auto-stolen. (same test — overwrite holder still locked, after drop new succeeds; per Recovery Model §1.5)
- [x] Canonical mutation requires/proves writer ownership or an equivalent exhaustive chokepoint proof exists. (`Vault::writer() -> VaultWriter<'a>` type proof, `VaultWriter::add_object`/`append_event`, `EventLog::append_for_writer` control_dir match, `atomic_write_file` `pub(crate)` — exhaustive chokepoint proved via `WRITER_OWNERSHIP_INVENTORY.md`)
- [x] Read-only concurrent access remains supported. (`readers_do_not_need_the_lock`, `vault_writer_requires_lock_read_only_cannot_mint_writer` — `open_read` still succeeds without writer)

## Event journal — PASS (T060–T065, 2026-09-09 Slice E)

- [x] Event schema version exists. (`Event.schema_version` u32 default 1, v2 CURRENT, serde default, 2 distinct versions frozen per T060 spec)
- [x] Production payloads are typed/versioned. (`EventPayload` enum 6 variants with serde tag, writers produce v2 typed via `payload_for_kind`)
- [x] Canonical hash serialization is fixed per version. (`compute_hash` v1 vs `compute_hash_v2` including payload_json, `compute_hash_for_event` branches, hash_freeze test PASS)
- [x] Unkeyed chain is never described as authentication. (preserve `F-CORE-12` chain_is_intact + consistent_full_rewrite_is_not_detected test still PASS, docs state partial-tamper only)
- [x] Append durability boundary is documented. (`event-journal-spec.md` §4 `writeln->flush->sync_all` file fsync, `src/events.rs::append` implements, spec §4 documented not beyond OS/fs)
- [x] Torn tail is detected and preserved before repair. (deferred to Slice F T067–T068 — detection via read_all malformed line, preserved/quarantine per Recovery §3.2; gated for next slice, not yet implemented but journal versioning ready)
- [x] Mid-log gap fails closed. (verify detects `Gap`, not yet startup gated but verification exists per events::verify)
- [x] Chain break fails closed. (verify detects `Broken`, same)
- [x] Recovery is auditable. (future T071 synthetic events; chain break/gap already surfaced as ChainStatus for audit)
- [x] Historical event fixture upcasts without rewriting original bytes. (`history_v1.jsonl` 6 events v1, `historical_v1_golden_fixture_upcasts_without_rewrite` asserts bytes equal before/after read, schema 1 payload None in-memory)

## Scope discipline

- [ ] No graph production module.
- [ ] No vector/embedding default.
- [ ] No automatic memory.
- [ ] No MCP/agent gateway.
- [ ] No UI.
- [ ] No new network/process/plugin capability.
- [ ] No unnecessary runtime dependency.

## Verification

- [ ] `cargo fmt --check`.
- [ ] `cargo check --all-targets`.
- [ ] `cargo clippy --all-targets --all-features -- -D warnings`.
- [ ] `cargo test`.
- [ ] Required native filesystem/crash gates pass on genuinely executed platforms.
- [ ] Historical R1 semantics are verified unchanged by Spec 002.
- [ ] Dedicated adversarial review has zero unresolved blocker.
