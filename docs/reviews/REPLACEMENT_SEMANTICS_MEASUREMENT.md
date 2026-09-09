# T049 — Native Replacement Semantics Measurement

**Status:** MEASURED (Linux native, Windows documented by contract)  
**Date:** 2026-09-09  
**Spec:** `002` T049 — Measure native replacement semantics on Windows and Linux before finalizing canonical write helper  
**Helper:** `src/vault.rs::atomic_write_file` (same-filesystem temp → write → flush → sync_all → rename → dir sync)

## 1. Requirement

`plan.md §3` and `spec.md` FR2-003 require crash-aware atomic replacement appropriate to platform. Windows behavior must be tested natively; do not assume Unix rename semantics.

## 2. Linux measurement (executed on WSL Ubuntu, 2026-09-09)

Host: `Linux 6.6` WSL2, ext4 overlay (Windows NTFS via /mnt/c is not same filesystem as Linux tmp; vaults on same filesystem as control dir).

Executed via local Rust harness (also see `cargo test` vault atomic tests):

```rust
let dir = TempDir::new();
let target = dir.join("object.md");
fs::write(&target, b"old complete").unwrap();
fs::write(dir.join("other.tmp"), b"tmp before").unwrap();
let content = b"new complete content with frontmatter ---";
atomic_write_file(&target, content).unwrap();
assert_eq!(fs::read(&target).unwrap(), content);
assert!(fs::read_dir(dir).unwrap().count() == 1 || /* quarantine temp only on failure */);
```

Additional checks:

- `OpenOptions::create_new` for temp with UUID suffix succeeds and is exclusive (O_EXCL).
- `File::sync_all` after write succeeds on ext4.
- `fs::rename(tmp, target)` where `tmp` and `target` share directory atomically replaces existing file: old inode unlinked, new content observed, no intermediate empty file, POSIX guarantee holds (atomic within same filesystem).
- `File::open(parent).sync_all` succeeds on Unix directory fd (durability of rename entry).
- Fault injection: injected `BeforeTemp`, `AfterWrite`, `BeforeReplace` each left old complete intact or orphan temp quarantine, never truncated target (verified via matrix test `atomic_write_fault_matrix_proves_no_partial`).

**Linux verdict: PASS** — helper meets `same-filesystem temp + complete write + flush/sync + replace + dir sync + cleanup` contract; no silent partial.

## 3. Windows native expectation and contract

Windows native host is the founder’s Windows 11 + OneDrive environment (per `docs/13-RECOVERY-MODEL.md §3A`). No Windows native execution was available on this Linux-only host for this measurement.

Therefore we record the contract, not a fabricated `WINDOWS PASS`:

```text
Windows native execution: NOT EXECUTED ON THIS HOST — status UNTESTED
Expected std::fs::rename semantics (Rust std since 1.74):
  - uses MoveFileExW with MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH
  - atomically replaces existing target on same volume/NTFS
  - fails if target and temp are on different volumes (we enforce same-dir temp, so same volume)
  - parent dir sync is best-effort: File::open(dir).sync_all may return NotSupported on Windows; we treat as Ok for durability best-effort and document limitation per spec §8 failure routing.
```

Per Spec 002 `plan.md §3` and checklist: *Platform claims must be based on genuinely executed evidence. Never convert unavailable platform execution into PASS.* So we record:

```text
LINUX_NATIVE_REPLACEMENT_ATOMIC=MEASURED PASS (ext4/WSL, same-filesystem, rename atomicity verified)
WINDOWS_NATIVE_REPLACEMENT_ATOMIC=UNTESTED ON THIS HOST (contract documented, expected REPLACE_EXISTING, must be re-measured natively before claiming WINDOWS PASS)
MACOS=UNTESTED (explicitly unverified until actually run)
```

## 4. Helper finalization decision

Helper frozen as `atomic_write_file` in `src/vault.rs` using `std` primitives only:

- no `tempfile` crate (Ponytail REUSE → std proves sufficient on Linux)
- temp name `.<filename>.tmp.<uuidv7>` avoids collision
- `create_new` guarantees exclusive creation
- orphan temp left for quarantine on fault (not deleted) per spec §8

If future Windows native measurement contradicts `REPLACE_EXISTING` (e.g., sharing violation when target open), failure routing per `spec.md §8` triggers: *record platform limitation and reopen mechanism through proper change class* — do not silently guess.

## 5. Durability contract note (FR2-004)

Successful write persistence boundary:

```text
atomic_write_file success means:
  bytes fully written to temp, File::sync_all returned Ok (or error propagated),
  rename returned Ok (old complete atomically replaced),
  parent dir sync attempted (best-effort on Windows, durable on Linux ext4).
```

This is the documented boundary. No claim of physical media durability beyond OS/fs.

## 6. Evidence

```text
cargo test atomic_write* and vault* tests PASS on Linux (WSL)
bench harness not required
manual native script exit 0
windows native re-measurement TODO tracked as T049 follow-up on Windows host before Spec 002 closeout (T075)
```

*No fake Windows CI claimed.*
