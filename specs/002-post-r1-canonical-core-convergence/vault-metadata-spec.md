# Vault Identity and Format — Minimal Schema (T046)

**Spec:** `002-post-r1-canonical-core-convergence` Slice B — Vault format and crash-safe canonical writes  
**Tasks:** T046–T048  
**Status:** SPECIFIED FOR IMPLEMENTATION (2026-09-09)  
**Baseline:** `ed79d8e` Phase T (no vault.json) → `format_version=1` product  
**Authority:** `spec.md` FR2-001/FR2-002, `plan.md` §3 vault metadata, `docs/13-RECOVERY-MODEL.md` startup sequence step 1.

## 1. File location

```text
<vault>/.fehrest/vault.json
```

Control directory `.fehrest` already exists per `src/vault.rs` `CONTROL_DIR`. The vault identity file lives there, never indexed as knowledge (F-CORE-16, `RESERVED_DIRS`).

## 2. Schema (v1 — minimal, product freeze)

```json
{
  "vault_id": "018f0d9e-aaaa-7000-8000-000000000000",
  "format_version": 1,
  "created_by_version": "0.0.1-phase-t",
  "created_at": "2026-09-09T06:30:00Z"
}
```

| Field | Type | Required | Semantics |
|---|---|---|---|
| `vault_id` | string (UUID, `Uuid::now_v7()` canonical) | YES | Stable Fehrest vault identity, allocated once at `Vault::create`. Opaque, not derived from path. Copied vaults duplicate this id — caller must re-identify per Recovery §3.17. |
| `format_version` | u32 | YES | Monotonic schema version. `1` is the first product version. Older legacy vaults have no file (implicit `0`). Newer unsupported `>1` must fail visibly. |
| `created_by_version` | string | YES | `Cargo.toml` `version` at creation time (observed via `env!("CARGO_PKG_VERSION")`). Diagnostic, not authority. |
| `created_at` | string ISO8601 | YES | Creation timestamp (UTC, `YYYY-MM-DDTHH:MM:SSZ`). Diagnostic, not ordering. |

No cloud, collaboration, sync, encryption, or multi-user fields are added — per `plan.md` “Do not pre-design cloud/collaboration fields” and Ponytail SHRINK. If future collaboration is ever measured, it gets its own migration and ADR.

Serialization: `serde_json` with pretty? Compact deterministic is not required for this file; we use compact + newline as std. Field order is as above but parser accepts any order (serde). Future version bumps must document canonical hash/serialization if vault_id participates in integrity.

## 3. Compatibility policy

```text
format_version == 1  → CURRENT, open succeeds.
format_version == 0  → LEGACY (no file) — upcastable to 1 on open_write (see §5).
format_version > 1   → UNSUPPORTED/NEWER — open fails visibly:
  Error::Vault("unsupported vault format_version X, newest supported is 1; see docs/migration")
  No guessing, no silent read, no partial index build.
Missing file but directory exists → legacy path (§5).
Corrupt JSON / missing field / invalid UUID → malformed, fail visibly:
  Error::Vault("vault metadata corrupt: ...") — never normalized as empty.
```

Per FR2-002: do not guess a newer format; per Recovery §3.12 partial upgrade: mismatched vault is refused, migration proceeds per `M` not silently.

## 4. Persistence and crash awareness

`vault.json` itself is written via the same crash-aware helper that canonical objects will use (§6):

```text
same-filesystem temp (.fehrest/.vault.json.tmp.<rand> or .goutputstream-like)
→ write complete JSON bytes
→ flush (File::sync_all where supported)
→ rename to vault.json (std::fs::rename — atomic on same filesystem per T049 measurement)
→ parent directory sync where relevant/supported (File::open(.fehrest).sync_all on Unix, best-effort on Windows)
→ cleanup only after outcome known, orphan temp quarantined not deleted
```

Successful `Vault::create` persistence boundary is: `vault.json` durable after rename+dir sync returns without error (FR2-004). This is documented, not promised beyond what OS/fs can establish.

## 5. Legacy handling (Phase T vaults)

Phase T baseline `ed79` has no `vault.json`; it was valid then (`require_vault` checks only `.fehrest` is dir).

Product behavior:

```text
Vault::create(root) → always writes vault.json with fresh vault_id v7, format 1.

Vault::open_write(root) on legacy vault (dir exists, file missing):
  - generate fresh vault_id
  - atomically write vault.json with format 1
  - succeed (migration), no event yet (events deferred to Slice E)
  - this is the upcastable path; it is explicit and visible (new file appears).

Vault::open_read(root) on legacy vault:
  - same as open_write for now (read path also triggers creation) OR
  - alternative is to fail closed until writable migration — we choose auto-create on any open that finds missing file, because read-only vault without identity is still a vault and identity allocation is idempotent.
  Rationale: Ponytail minimal — no separate “migrate” CLI yet; explicit file creation is already a visible migration.
```

A future explicit migration CLI may replace this auto-create, but the behavior is recorded and will be preserved by fixtures (T048).

## 6. Canonical object replacement contract (FR2-003/004 outline — detailed in T050 spec)

Same helper as above will be reused for object writes (`add_object` / future `update_object`):

```text
target = root.join(rel)
temp   = same dir as target, .<name>.tmp.<uuid7>
steps: create_new(temp) → write(content = serialize(frontmatter, body)) → flush → sync_all → rename(temp, target) → dir sync → cleanup
```

Windows measurement (T049) is required before final helper is frozen: document `std::fs::rename` with existing destination on NTFS — expected to succeed via `REPLACE_EXISTING` since Rust 1.74, but measure and record platform limitation if not. No promise stronger than measured.

## 7. What is NOT in this spec

```text
vault name / display name     — derive from frontmatter, not metadata
owner / user id               — OS account is root of trust (F-CORE-11)
sync token / cloud anchor     — deferred, no sync
encryption key id             — deferred
graph/vector sidecar version  — sidecar version check is recovery §3.12 not vault.json
```

Any future field requires `REQUIREMENT → PONYTAIL → LICENSE → SECURITY → BENCHMARK → AUTHORIZATION` before admission, with `format_version` bump and upcast test (T064 golden fixture pattern applied to vault.json too).

## 8. Validation fixtures (T048 preview)

```text
current.json          — format_version 1, valid UUID, pretty minimal fields
older_legacy_missing  — no file, directory only (pre-format Phase T vault)
older_format_0        — {"format_version":0, ...} if ever emitted (not by product)
unsupported_newer_2   — {"vault_id":..., "format_version":2, ...} → must fail
unsupported_newer_99  — future gap
corrupt_truncated     — partial JSON, must fail
corrupt_bad_uuid      — vault_id not UUID, must fail
```

These will be committed under `tests/fixtures/vault/` and exercised by `src/vault.rs` tests.

## 9. No new dependency

Uses existing `serde`/`serde_json`/`uuid` already in `Cargo.toml`. No `tempfile` crate yet; temp handling uses `std::fs::OpenOptions::create_new` + `uuid` suffix (std primitives per Ponytail). If measurement proves Windows needs a helper, dependency decision will be written before adoption (plan §9).

## 10. Migration model placeholder

Full migration per `docs/12-MIGRATION-SCHEMA-EVOLUTION` is `M` not in Spec 002. This spec's `format_version` is the hook for that model; on `>1` failure we report migration required, not auto-migrate.

---

*Evidence for T046: this file committed; implementation in `src/vault.rs` T047 references it; fixtures T048 committed; T049 measurement recorded before helper frozen.*
