# T060 — Event Journal Versioning and Compatibility Spec

**Spec:** `002` Slice E — Versioned event journal (T060–T065)  
**Date:** 2026-09-09  
**Input:** `src/events.rs` 10302 (v0 Phase T, 6 EventKind, `detail: String` free-form, unkeyed hash `seq|kind|subject|detail|prev`)

## 1. Historical schema (v1 — frozen, golden)

Phase T `events.jsonl` line is:

```json
{"seq":1,"kind":"VaultCreated","subject":"vault","detail":"","prev_hash":"00…","hash":"ab…"}
```

- `kind` 6 variants: `VaultCreated, ObjectRegistered, ObjectConflict, MemoryRecorded, MemorySuperseded, ContextCompiled`
- `detail` is free-form string (path, empty, etc.), bounded `MAX_EVENT_BYTES 16KiB`
- No `schema_version` field; implicit `v=1` for compat
- Hash canonical string per `compute_hash`: `format!("{seq}|{kind:?}|{subject}|{detail}|{prev}")`
- Chain: `seq` contiguous 1..N, `prev_hash` chains, `GENESIS 64×0`

This is the historical golden fixture (T064) — bytes never rewritten to read.

## 2. Next versioned envelope (v2 — minimal, product)

Product Phase 1 schema:

```rust
struct Event {
  schema_version: u32, // 1 for legacy/detail, 2 for typed
  seq: u64,
  kind: EventKind,
  subject: String,
  detail: String,                 // kept for v1 compat + v2 fallback text (typed payload is authoritative for v2)
  payload: Option<EventPayload>,  // Some for v2, None for v1 golden
  prev_hash: String,
  hash: String,
}

#[derive(Serialize,Deserialize)]
#[serde(tag="type", content="data")]
enum EventPayload {
  VaultCreated { vault_id: String },
  ObjectRegistered { object_id: String, path: String },
  ObjectConflict { object_id: String, paths: Vec<String> },
  MemoryRecorded { memory_id: String, memory_type: String },
  MemorySuperseded { superseded_id: String, by_id: String },
  ContextCompiled { context_id: String, digest: String, omitted: usize },
}
```

Rules:

- Writer must produce `schema_version=2` with `Some(payload)` typed per kind; `detail` is populated as human-readable fallback (e.g., path) but **not authoritative** for v2 — hash includes both for freeze.
- Historical v1 lines missing `schema_version` and `payload` are read as `schema_version=1, payload=None, detail` free-form. No migration rewrite of file bytes.
- `schema_version` is explicit per FR2-011; payload is typed per FR2-012 (not indefinitely expanding detail string). Only Phase 1 needed variants are included; future variants add new enum arms with version bump, not free-form detail growth.
- Serde JSON: unknown `kind` string → malformed, not guessed; unknown payload variant → malformed.

## 3. Canonical hash freeze (T062)

Per-version frozen serialization (never inherited from serializer that could change):

```text
v1: payload = format!("{seq}|{kind:?}|{subject}|{detail}|{prev}")   // exactly Phase T string, as before
v2: payload = format!("{seq}|{kind:?}|{subject}|{detail}|{payload_json}|{prev}")
      where payload_json = serde_json::to_string(&payload).unwrap() with sorted keys (serde_json deterministic for this enum)
      // Alternative frozen: Hash field order seq,kind,subject,detail,payload,prev each with separator |
```

This file freezes the order. Changing order invalidates chain verification; new schema version would get new rule, not retroactive change.

*Note:* Phase T computed hash without payload; v2 includes payload_json so typed fields participate in integrity (tamper of payload breaks recompute). v1 historical hash is recomputed via v1 rule, v2 via v2 rule — verifier selects by `schema_version`.

## 4. Durability boundary (T063)

Success per `append`/`append_for_writer` means:

```text
events.jsonl line bytes fully written (writeln!),
File::flush(),
File::sync_all() where supported (propagated error, not silently ignored),
(no parent dir sync for append — file append not rename — best-effort fsync on file only)
Return Ok(Event) only after sync_all succeeds.
```

This is documented,不 promise beyond OS/fs. For crash consistency see Slice F torn-tail handling.

## 5. Golden fixture (T064)

Committed under `tests/fixtures/events/history_v1.jsonl` — 6 lines covering each kind as v1 (no schema_version). plus `tests/fixtures/events/current_v2.jsonl` — same 6 events as v2 typed.

Historical bytes are never rewritten by read-time upcasting; upcasting is in-memory `Event` → `Event {payload: Some(...)}` if original had no payload but detail can be inferred? Actually historical v1 upcast is `payload=None` with `detail` preserved; code that needs typed view on historical v1 will receive `payload=None` and must fall back to `detail`.

## 6. Upcasting (T065)

`read_all()` parses each line as `serde_json::Value` first:

- if field `schema_version` missing → treat as `1`, `payload=None`, keep `detail`
- if `schema_version==1` → same
- if `schema_version==2` → deserialize typed `payload`, validate kind↔payload variant match (mismatch → malformed)

No file rewrite. `read_all()` returns `Vec<Event>` where each `Event` may have `payload=None` for v1 history; `verify()` uses per-event `schema_version` to select hash recompute rule.

## 7. No new dependency

Reuse `serde`/`serde_json`/`sha2` already pinned. No protobuf.

## 8. Migration model placeholder

Full migration per `docs/12-MIGRATION-SCHEMA-EVOLUTION` not in Spec 002. This spec's `schema_version` is the hook; on read, v1 is valid and returned as-is; writers produce v2.
