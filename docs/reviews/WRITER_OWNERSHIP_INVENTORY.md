# T054 — Writer-Owned Mutation Inventory

**Spec:** `002` Slice D — Writer-owned mutation  
**Date:** 2026-09-09  
**Input:** `src/` baseline `6bb4e8a` (vault 33856, events 10302, vault meta + atomic write)

## Canonical (irreplaceable) state — per `01-ARCHITECTURE-CONSTITUTION` F-CORE-06 / `04-DERIVED-DATA-MODEL`

| Canonical file | Writer | Current entry point | Lock check | File:line | Risk if bypassed |
|---|---|---|---|---|---|
| `.fehrest/vault.json` identity + `format_version` | vault creation / open migration | `vault::ensure_vault_meta` → `write_vault_meta_atomic` → `atomic_write_file` | **none direct** (called from `Vault::create`/`open_write`/`open_read` before lock is held; identity write is outside writer lock) | `src/vault.rs:389`, `543`, `433` | Path-forged vault identity could mint a vault id distinct from the lock's vault; pre-lock write is intentional for bootstrap but must not allow post-open identity overwrite without writer |
| Vault object markdown `<rel>.md` with frontmatter `id:` | user knowledge | `Vault::add_object(rel, title, project, body)` | `if !has_write_lock -> Err("write requires vault write lock")` convention, not type | `src/vault.rs:283` | Direct `std::fs::write(root.join(rel), ...)` with arbitrary `rel` bypasses allowlist/reserved check and writer check if helper is `pub` |
| `events.jsonl` append-only hash-chained log | audit | `EventLog::append(kind, subject, detail)` | **none** — `EventLog::open` takes `control_dir: &Path` not `&Vault` or writer; any path-holder can append | `src/events.rs:93` | Forked or out-of-order `seq` if two processes interleave appends; hash chain break then requires recovery (§3.3/3.4) |
| `derived.sqlite` + `object_fts` | rebuildable | `Derived::rebuild(&scan.objects)` | `Derived::open(control_dir: &Path)` similar path-not-vault | `src/derived.rs:34` | **Derived is NOT canonical** (I-6 `NON-CANONICAL·REBUILDABLE·UNTRUSTED`); direct rebuild with poisoned path is availability issue, not canonical loss — out of scope for writer-ownership gate |
| `memory.rs` explicit memory struct | in-memory only Phase T | `Memory::new` + caller in-memory Vec; no durable journal file yet | n/a | `src/memory.rs:184` | Not yet durable; Phase 4 journal will be gated |
| CLI `fehrest add` / `fehrest init` | user command | `cli.rs: add` → `Vault::open_write` → `add_object` → `EventLog::append` | inherits Vault check, but `EventLog::append` still free | `src/cli.rs:77` `add` branch, `63` `init` |

## Non-canonical / test-only entry points (not product chokepoints)

| Entry | File | Note |
|---|---|---|
| `fs::write(root.join(".git/config.md"), ...)` in `reserved_dirs_are_excluded` test | `src/vault.rs:351` | Test fixture uses direct fs to simulate reserved-dir content — deliberately not through Vault |
| `atomic_write_file` / `atomic_write_file_with_fault` | `src/vault.rs:433,449` | `pub` helpers currently reachable with arbitrary `target: &Path`; must be restricted to writer-owned callers after T056 |
| `File::create(dir.join("other.tmp"))` etc in fault tests | `src/vault.rs:796` | Test-only, not product |

## Exhaustiveness argument

`grep -Rn "pub fn\|-> Result"` across `src/*.rs` yields:

```text
src/vault.rs: Vault::create, open_write, open_read, scan, add_object, resolve_for_write, ensure_vault_meta, atomic_write_file
src/events.rs: EventLog::open, append, read_all, verify
src/derived.rs: Derived::open, rebuild, search
src/locator.rs: open_confined, read_verified
src/identity.rs: parse, serialize
```

Of these, only `Vault::add_object`, `ensure_vault_meta`/`write_vault_meta_atomic`, and `EventLog::append` mutate canonical bytes. All others are reads or derived. Therefore exhaustive chokepoint is `VaultWriter -> add_object / append_event` plus `atomic_write_file` visibility reduction.

## What T056 must close

```text
T056-1: Make canonical file creation through VaultWriter::add_object structurally owning (cannot be called with &Vault read-only)
T056-2: Make EventLog mutation require VaultWriter proof (EventLog::append_for_writer or VaultWriter::append_event)
T056-3: Reduce atomic_write_file from pub to pub(crate) so arbitrary path holder cannot mint canonical bytes outside Vault
T056-4: Keep Vault::add_object runtime check as compat but document as legacy; exhaustive proof will be via VaultWriter paths + negative tests T057
```

No new lock framework; reuse existing `WriteLock` `create_new(O_EXCL)` — per Ponytail.
