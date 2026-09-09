# T055 — Writer-Capability / Chokepoint Selection (Ponytail)

**Spec:** `002` Slice D — Writer-owned mutation  
**Date:** 2026-09-09  
**Inventory:** `docs/reviews/WRITER_OWNERSHIP_INVENTORY.md`  
**Requirement:** `spec.md` FR2-008 *SHOULD structurally require/prove writer ownership where practical*, FR2-007/009 keep single-writer + no-auto-steal, FR2-010 PID diagnostics not auth.

## Candidates considered

| # | Design | How it proves ownership | Forgability | Read concurrency | Test ergonomics | New dependency | Verdict |
|---|---|---|---|---|---|---|---|
| A | `VaultWriter<'a>(&'a Vault)` newtype with private field, constructed only via `Vault::writer(&self) -> Result<VaultWriter>` that checks `has_write_lock` | Token holds `&Vault` plus private zero-sized; cannot be constructed from arbitrary `String` path because field is private and constructor checks lock | **Not forgeable** from path alone — needs `&Vault` with `WriteLock` present (lock is not cloneable, not forgeable without holding the file lock) | Yes — `Vault::open_read` cannot produce writer, `Vault::open_write` can; readers take no lock, writer holds lock privately | Simple — `let w = v.writer()?; w.add_object(...)` mirrors existing `add_object` shape; `Drop` still owns lock via `Vault` | None — lifetime + newtype only | **SELECT** |
| B | `WriterLease` owned struct holding `PathBuf + WriteLock` file handle separately | Proves by holding `File` handle | Harder to fake (would need open lock file), but holds extra OS handle beyond Vault's existing handle; duplicates state | Readers still independent but lease holder owns handle not Vault | More verbose; lease lifetime not tied to Vault borrow | None | Defer — B duplicates Vault's lock and would require moving WriteLock out |
| C | `Vault::append_event(&self, ...)` chokepoint that checks `has_write_lock` inside and delegates to `EventLog` | Runtime `has_write_lock` bool, not type | Forgeable by constructing `Vault{lock:None}` via unsafe or by calling `EventLog::append` directly on path — no structural block | Readers fine | Trivial | None | **Legacy** — keeps existing `has_write_lock` convention for compat, not structural proof |
| D | `EventLog::for_writer(control_dir: &Path, writer: &VaultWriter)` constructor that binds log to writer at open | Requires writer token to obtain log handle | Not forgeable without writer, but log open currently takes only path — would require refactoring every caller to thread writer even for read-only `read_all`/`verify` | Readers that only `verify` would be forced to acquire writer unnecessarily (violates read concurrency) | Heavier | None | Reject for read path — keep `EventLog::open` for reads, add `append_for_writer` for writes |

## Ponytail decision

```text
REQUIREMENT: canonical mutation must not be callable with read-only &Vault or bare path
ALREADY IN FEHREST: Vault + WriteLock (create_new O_EXCL) exists, so token can borrow it (no new lock framework per plan §4 REUSE)
RUST STD SUFFICIENT: lifetime newtype VaultWriter<'a> with private field + Vault::writer() check proves ownership without new crate (std lifetimes + ownership)
PLATFORM PRIMITIVE: file lock already platform-correct (O_EXCL / CREATE_NEW)
SMALLER CORRECT: A is smaller than B/D because it is a borrow, not an owned lease or log wrapper; C is smaller but only runtime check
```

Decision:

```text
DECISION=KEEP A as primary typed proof + keep C as runtime fallback for compat
NEW_LOCK_FRAMEWORK=NO
NEW_DEPENDENCY=0
```

Implementation (T056):

```rust
pub struct VaultWriter<'a> { vault: &'a Vault, _private: () }
impl Vault {
    pub fn writer(&self) -> Result<VaultWriter<'_>> {
        if !self.has_write_lock() { return Err(Error::Vault("write requires writer ownership; use Vault::writer()".into())) }
        Ok(VaultWriter { vault: self, _private: () })
    }
}
impl<'a> VaultWriter<'a> {
    pub fn vault(&self) -> &'a Vault { self.vault }
    pub fn add_object(&self, rel: &str, title: Option<&str>, project: Option<&str>, body: &str) -> Result<ObjectId> {
        // same allowlist/reserved/LOCATOR checks + atomic_write_file via Vault::add_object_inner
        self.vault.add_object_inner(rel, title, project, body)
    }
    pub fn append_event(&self, log: &EventLog, kind: EventKind, subject: &str, detail: &str) -> Result<Event> {
        log.append_for_writer(self, kind, subject, detail)
    }
}
```

And:

```rust
impl EventLog {
    pub fn append_for_writer(&self, _writer: &VaultWriter<'_>, kind: EventKind, subject: &str, detail: &str) -> Result<Event> {
        self.append(kind, subject, detail) // after verifying _writer vault root matches log path's vault
    }
    fn verify_writer_matches(&self, writer: &VaultWriter) -> Result<()> { /* control_dir == writer.vault().control_dir() */ }
}
```

Visibility:

```text
atomic_write_file : pub -> pub(crate)  (so arbitrary path holder cannot call it outside vault)
atomic_write_file_with_fault : pub -> pub(crate) (test seam stays crate-visible for fault matrix, not pub)
```

This preserves:

```text
second writer fails visibly (WriteLock O_EXCL unchanged)
stale lock never auto-stolen (Drop only removes own file, no stealing)
PID diagnostics in writer.lock content remain diagnostic not auth (FR2-010)
read-only concurrency (open_read → no writer token → reads still succeed)
```

Security non-minimization: `root confinement` + `post-open identity` still checked in `VaultWriter::add_object` via existing `resolve_for_write` + `Locator` + `atomic_write_file`; no bypass via path string.

## What T057-T059 will prove

- T057: direct bypass negative tests — `Vault::open_read(...).writer()` fails, `atomic_write_file` not `pub` outside crate, `EventLog::append_for_writer` without writer fails, exhaustive chokepoint
- T058: second writer still `WriterLocked`, stale file visible, not stolen
- T059: stale-lock diagnostics `writer.lock` content `pid=...` exposed via `Error::WriterLocked {holder, path}` diagnostic only, not auth — no change to `WriteLock::acquire` that would treat PID as permission

No `tempfile`, `fs2`, or lock framework crate needed.
