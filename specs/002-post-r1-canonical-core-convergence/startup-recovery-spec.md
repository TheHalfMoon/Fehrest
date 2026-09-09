# T066–T071 — Startup Integrity and Recovery Spec

**Spec:** `002` Slice F — Startup integrity and recovery  
**Date:** 2026-09-09  
**Input:** `docs/13-RECOVERY-MODEL.md` §2 startup sequence, §3.2 torn tail, §3.3 gap, §3.4 chain break, vault meta + event journal v2

## 1. Startup integrity gating (T066)

`Vault::open_write(root)` must run startup integrity before acquiring writer lock and before mutation. Sequence (blocking per Recovery Model §2 steps 1–7, before mutation):

```text
1. vault.json present and parseable → else Error::Vault vault recovery (§3.9) — currently ensure_vault_meta handles 1–2
2. format_version compatible → else unsupported/newer fails visibly — read_vault_meta already
3. event log: last record intact? → else torn-tail quarantine (T067/T068)
4. event log: sequence contiguous? → else gap quarantine, fail closed (T069)
5. event log: hash chain valid? → else tamper report, fail closed (T070)
6. (memory log) — not yet durable Phase 1 (no file) — skip, but placeholder kept
7. (derived integrity) — non-blocking per Recovery §2 steps 8–10 — not gated for writable open, but derived rebuild covered elsewhere
```

If step 3 finds torn tail at last line, repair is allowed (truncate to last valid, preserve torn bytes). Steps 4–5 fail closed and refuse writable continuation — never normalized as crash damage.

Implementation: `vault::startup_integrity_check(control_dir: &Path) -> Result<StartupReport>` called from `Vault::open_write` before `WriteLock::acquire`. If check returns `NeedRepair`, caller may perform `EventLog::quarantine_torn_tail()` then retry verify. For gap/chain broken, return `Error::Vault` with precise `at_seq`/`from_seq→to_seq`.

`Vault::open_read` does **not** gate on steps 3–5 — reads remain available even with broken log, so user can inspect (partial function beats no function, principle 4). It still validates vault.json.

## 2. Torn final record detection (T067)

Detection: last non-empty line fails JSON parse or fails `prev_hash`/`hash` recompute where `seq` would be `N+1` but truncated. Equivalent to `read_all` returning `Event("malformed event at line i")` where `i == line_count-1`.

Preservation: before repair, copy torn bytes verbatim to quarantine file:

```text
<control_dir>/events.jsonl.torn.<seq_expected_or_last_good+1>.<uuid>.quarantine
```

Content is exact bytes of torn line (including partial JSON). No deletion to tidy up. Forensic bytes preserved before destructive truncation (FR2-021).

## 3. Authorized torn-tail quarantine/recovery (T068)

Repair steps (only for tail):

```text
detect torn bytes → write quarantine file → truncate events.jsonl to last valid line's end offset → fsync file + dir → return Ok
```

After repair, `verify()` reports `Intact` for truncated length. Recovery is auditable: quarantine file path is surfaced via `StartupReport::torn_quarantined(path)` and later via `T071` synthetic event if needed (for now just filesystem artifact).

Mid-log torn (malformed not at end) is **not** torn tail — it is gap/chain damage and must fail closed per T069/T070, not truncated.

## 4. Gap and chain fail-closed (T069/T070)

If `verify()` returns `Gap {from_seq, to_seq}` or `Broken {at_seq}` where `at_seq` is not `events.len()` (i.e., not potential torn tail at end), `open_write` fails with `Error::Vault("event log gap/chain broken at seq … — writable continuation refused — quarantine affected segment")` and does **not** truncate. The vault remains readable but not writable until operator intervenes (quarantine segment preserved, degraded mode per Recovery §3.3/3.4).

Negative test must exist showing Gap/Broken does not normalize as torn.

## 5. Recovery audit (T071)

Per Recovery §5 `log/repaired`, `log/gap-detected`, `log/chain-broken`. For Phase 1 minimal, torn-tail repair creates quarantine file and does not yet emit synthetic `log/repaired` event (that would require writer). After writable open succeeds post-repair, a `log/repaired`-like diagnostic will be appendable; for now audit is filesystem quarantine path.

Future T071 will add `EventPayload::LogRepaired {kind, segment, records_affected, quarantine_path}` via `VaultWriter::append_event`.

## 6. Kill/restart matrices (T072/T073)

T072: fault matrices spanning canonical write (`atomic_write_file` fault points) + event append (`append` flush/sync failure). T073 randomized kill/restart criterion owned by canonical plan — for Phase 1 run kill tests via `cargo test` + bespoke matrix tests: `kill_during_canonical_or_event_preserves_integrity`.

Phase 1 gates will preserve raw evidence under `artifacts/recovery/` if randomized run is executed on demand (not required for Slice F minimal merge).

## 7. No new dependency

Use `std::fs`, `std::io`, `uuid` already present. No `tempfile`.

## 8. Failure routing

```text
torn tail → quarantine + truncate + allow writable
gap → fail closed, do not normalize
chain break → fail closed, do not auto-repair
vault.json corrupt → fail closed
```

Per spec §8 canonical loss → stop before Phase 2.
