# D. Canonical Data Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Canonical state is state that **cannot be recomputed**. If it is lost, knowledge is lost. Everything else belongs in [E](04-DERIVED-DATA-MODEL.md).

---

## 1. The object model decision

The brief asks whether the right primitive is *"Everything is an Object; views are projections."*

**Recommendation: adopt it, with one correction.** "Everything is an Object" is right as a *storage* model and wrong as a *file* model.

The failure mode of pure object-orientation in a local-first system is that objects stop corresponding to files. Once an object is a row rather than a file, [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default) and [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) die: the vault becomes a database with a directory of exports beside it. Logseq and SiYuan both illustrate the tension — block-level identity is genuinely useful and genuinely expensive to hold in plain text.

So the model is:

> **Every canonical object is a file or a region of a file. Types are metadata. Views are projections. The file is the object's home.**

Concretely: a note, a project, a decision and a person are all the same *kind* of thing — a Markdown file with typed frontmatter. What distinguishes them is a `type` field, not a different storage mechanism, not a different table, and not a different directory requirement.

**Why this beats dedicated first-class types in v1:** the brief lists 16 candidate object kinds. Making each a first-class type means 16 schemas, 16 migrations, 16 editors, and 16 opportunities for a user's real-world object to fit none of them. Making them one type with a discriminator means one schema, one migration path, and a user who can invent `type: recipe` without a Fehrest release.

**The minimum durable object model is therefore three things:**

| Primitive | Count | Why irreducible |
|---|---|---|
| **Object** | 1 type, open `type` discriminator | The unit of knowledge, identity and addressing |
| **Event** | 1 append-only log | What happened; cannot be recomputed |
| **Memory** | 1 bitemporal record type | Assertions with time and provenance; distinct because it has different lifecycle semantics from a document |

Memory is separate from Object rather than being `type: memory` for one reason: memories have **bitemporal validity and supersession**, and objects do not. Collapsing them would force every note to carry `valid_from`/`valid_until`/`supersedes`, which is wrong and expensive. This is argued further in [F §2](05-MEMORY-MODEL.md).

Links, tags, backlinks, tasks, and relationships are **not** primitives — they are derived from object content or expressed as memory. Backlinks in particular are strictly derived ([E](04-DERIVED-DATA-MODEL.md)).

---

## 2. Vault layout

```
<vault>/
├── .fehrest/
│   ├── vault.json                  # CANONICAL  vault id, format version, created_at
│   ├── events/                     # CANONICAL  append-only journal
│   │   ├── 000001.jsonl
│   │   ├── 000001.jsonl.digest
│   │   └── segments.json
│   ├── memory/                     # CANONICAL  memory assertions
│   │   └── 000001.jsonl
│   ├── sidecars/                   # CANONICAL  per-object extension records
│   │   └── <object-id>.json
│   └── derived/                    # DISPOSABLE  safe to delete at any time
│       ├── index.sqlite
│       ├── graph/
│       └── cache/
├── notes/                          # CANONICAL  user files, user-chosen structure
├── projects/
└── attachments/                    # CANONICAL  original bytes, never rewritten
```

Three properties of this layout are deliberate:

1. **`derived/` is inside `.fehrest/` and is the only deletable directory.** A user can `rm -rf .fehrest/derived` as a support instruction and lose nothing. This makes [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) operationally real rather than aspirational.
2. **User files live outside `.fehrest/`, in a structure the user chooses.** Fehrest does not impose a directory taxonomy, because imposing one makes the vault Fehrest-shaped rather than user-shaped.
3. **Canonical machine state (`events/`, `memory/`, `sidecars/`) is separated from canonical user state (`notes/`, `attachments/`).** They have different backup, sync and conflict characteristics, and conflating them is what makes "just put it in git" fail.

---

## 3. Object identity

**Identity is opaque, allocated, and immutable.** Format: **UUIDv7**, rendered lowercase hex with hyphens.

UUIDv7 rather than ULID or a content hash:
- Time-ordered prefix gives locality for index and log scans, which a random UUIDv4 does not.
- Standardised (RFC 9562), so third-party tools can parse it — required by [I-9](01-ARCHITECTURE-CONSTITUTION.md#i-9--export-does-not-depend-on-fehrest-infrastructure).
- Not content-derived, so editing a file cannot change its identity — a content hash would make identity change on every keystroke.
- ULID is equivalent in properties but less standardised; the tie is broken by RFC status.

Identity is stored **in the file's own frontmatter**, which is what makes it survive Fehrest's absence:

```yaml
---
id: 0198f2a1-4c3e-7b21-9f04-3a5c7e8d1b60
type: decision
title: Graphify runs as a sidecar
created: 2026-08-17T14:22:03Z
updated: 2026-08-17T14:22:03Z
---
```

**Consequences, stated because they are the honest costs:**
- Fehrest writes to user files to allocate identity. This is a real intrusion, and it is the price of [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities). Mitigated by allocating lazily — on first *meaningful* interaction, not on first sight — and by making it configurable.
- A file whose frontmatter is stripped by another tool loses identity. Recovery is by content-similarity re-association, presented to the user as a decision, never silently guessed. Specified in [N](13-RECOVERY-MODEL.md).
- Duplicate IDs (from a copied file) are detected at ingest; the later-observed file is re-identified and the event recorded.

**Graphify node IDs are never identities.** They are name-derived normalised slugs with documented collision history ([E-4](research/EVIDENCE_LOG.md#e-4--graphify-node-ids-are-name-derived-not-stable-identities)). They appear only as a derived mapping column, rebuildable on demand. This is enforced by `test_graphify_ids_are_not_identities`.

---

## 4. The Knowledge Plane

### 4.1 Canonical formats

| Format | Role | Spec | Status |
|---|---|---|---|
| CommonMark + GFM | Object body | External spec | v1 |
| YAML frontmatter | Object metadata | In-repo schema | v1 |
| Original attachment bytes | Attachments | N/A — never rewritten | v1 |
| Fehrest Sidecar JSON | Extensions Markdown cannot express | In-repo | v1 |
| JSON Canvas | Canvas objects | `obsidianmd/jsoncanvas`, MIT ([SRC-071](research/FEHREST_SOURCE_REGISTRY.md#9-product-references)) | Phase 6 |
| Event JSONL | Activity log | In-repo | v1 |
| Memory JSONL | Assertions | In-repo | v1 |

Every entry has a specification and a lossless exporter, per [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended).

### 4.2 Frontmatter schema

```yaml
id: <uuidv7>              # required, immutable
type: <string>            # required, open vocabulary; core knows note|project|decision|person|meeting|research
title: <string>           # optional; falls back to H1 then filename
created: <RFC3339>
updated: <RFC3339>
tags: [<string>]          # optional
# type-specific fields are permitted and MUST be preserved verbatim by any Fehrest write
```

**Unknown-field rule (load-bearing):** Fehrest preserves every frontmatter field it does not understand, byte-for-byte, on every write. A version that drops unknown fields silently destroys forward compatibility and user data written by newer versions or other tools. This is [R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) and is tested by `test_unknown_frontmatter_preserved`.

### 4.3 Links

Links are written in the file, in one of two forms: `[[wikilink]]` (Obsidian-compatible, resolved by title/path) or `[text](fehrest://object/<uuid>)` (identity-stable).

The tension is real and worth naming: wikilinks are human-writable and portable to other tools but break on rename; ID links are rename-stable but unreadable and Fehrest-specific.

**Resolution: both are accepted; wikilinks are canonical-as-written and resolved through an alias index.** On rename, Fehrest offers to rewrite inbound wikilinks — an explicit, undoable, event-recorded operation rather than a silent rewrite. ID links need no rewriting.

**Backlinks are never stored in files.** They are derived. Writing backlinks into files creates write amplification, spurious conflicts, and an authority question when the two disagree.

### 4.4 The sidecar format

Sidecars hold what Markdown cannot express **without hiding it**:

```json
{
  "object_id": "0198f2a1-...",
  "format_version": 1,
  "content_hash": "sha256:...",
  "blocks": [
    { "block_id": "01234567-...", "anchor": { "kind": "heading-path", "value": ["Design", "Storage"] } }
  ],
  "annotations": [
    { "id": "...", "kind": "comment", "author": "user", "created": "...",
      "anchor": { "kind": "quote", "quote": "deterministic extraction", "occurrence": 1 },
      "body": "verify against E-5" }
  ],
  "agent_provenance": [
    { "session_id": "...", "actor": "agent:claude", "range_anchor": {...},
      "event_id": "...", "kind": "authored" }
  ]
}
```

Three rules make sidecars safe rather than a hidden-state backdoor:

1. **A sidecar may never contain content.** Content lives in the Markdown. Sidecars carry only *references into* content plus metadata. If a sidecar is deleted, the document is intact and only annotations are lost.
2. **Anchors are content-relative, not offset-based.** Byte offsets break on any edit. Quote-plus-occurrence and heading-path anchors degrade gracefully; an anchor that no longer resolves is marked orphaned and shown to the user, never silently dropped.
3. **`content_hash` records the document state the anchors were computed against**, so staleness is detectable rather than inferred.

This is the mechanism that lets Fehrest support comments, block identity and agent provenance without a proprietary document model — and it is why the round-trip gate can be dissolved rather than solved (§7).

---

## 5. The Event Plane

### 5.1 Design, adopted from the harness

Four patterns are taken from [E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns):

1. **The log is the source of truth; agent-visible history is derived from it and never stored separately.** Replay is re-derivation.
2. **One event type, two backends.** JSONL is canonical; the SQLite copy is derived and rebuildable. There is *no parallel persisted event type*.
3. **Header metadata lives outside the event vocabulary** — format version, vault id, lineage — because storage concerns must not reach derived agent-visible state.
4. **Merge-extensible vocabulary**, so capabilities add event types without forking the core.

### 5.2 Durability tiers — the correction to the brief

The brief asks which events truly belong in durable history and warns against storing noise forever. This is the right instinct, and it is where Fehrest must **diverge** from its donor: the harness stores `assistant/chunk` for token-level replay fidelity, which is correct for a debugging runtime and wrong for a decade-long memory store.

Three tiers:

| Tier | Retention | Contents |
|---|---|---|
| **T1 — Canonical, permanent** | Forever | Facts about knowledge and authority |
| **T2 — Canonical, compactable** | Full detail for N days, then summarised into T1 with the detail dropped | Session mechanics |
| **T3 — Ephemeral** | Never written to the canonical log | Stream chunks, keystrokes, UI state, telemetry |

**T1 — permanent:**
```
object/created      object/updated      object/renamed      object/deleted
memory/promoted     memory/rejected     memory/superseded   memory/confirmed
decision/recorded
agent/session-start agent/session-end
capability/granted  capability/revoked
tool/approval-asked tool/approval-decided
context/compiled            # inputs + digest, NOT the package body
import/ingested             # source, content hash, extractor, version
schema/migrated
```

**T2 — compactable:**
```
agent/step-start    agent/step-end
model/request       model/response      # metadata + digest; body per retention policy
tool/call           tool/result         # oversized bodies spilled, per E-9
memory/candidate                        # rejected candidates compact away; promotions are T1
user/message
```

**T3 — never canonical:** `assistant/chunk` and equivalents.

**Compaction rule:** compaction is itself an event (`log/compacted`) recording what was summarised and the digest of what was removed. Compaction never deletes a T1 event and never breaks the hash chain — it writes a new segment and marks the old one superseded, retaining its digest. So the log remains verifiable after compaction, which naive truncation would destroy.

**Why `context/compiled` stores inputs and a digest rather than the package body:** storing every package body means storing the vault repeatedly. Storing inputs plus a digest satisfies [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable) by *recomputation*, and the digest proves the recomputation matches. This is the harness's derive-don't-store principle applied to context.

**The honest cost:** recomputation requires that canonical state has not changed. When it has, the package is not reproducible byte-for-byte and Fehrest must say so rather than pretend. `context/compiled` therefore records the canonical high-water mark (event sequence number) it was compiled against, so a failed reproduction is explainable rather than mysterious.

### 5.3 Event record

```json
{
  "seq": 142,
  "id": "0198f2a1-...",
  "type": "memory/promoted",
  "ts": "2026-08-17T14:22:03.481Z",
  "actor": { "kind": "agent", "id": "agent:claude", "session": "019..." },
  "scope": { "project": "019..." },
  "payload": { },
  "causation": "019...",
  "prev_hash": "sha256:...",
  "hash": "sha256:..."
}
```

- `seq` is contiguous and monotonic; gaps are corruption ([N](13-RECOVERY-MODEL.md)).
- `ts` is system-assigned. **Actors cannot supply timestamps** — this is what defeats backdating ([T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse)).
- `hash` chains over the canonical serialisation of the record including `prev_hash`, giving tamper-evidence ([T-4](02-THREAT-MODEL.md#t-4--event-log-tampering)).
- `causation` links an event to the event that caused it, which is what makes audit narratable rather than a flat list.

### 5.4 Crash safety

Adopted directly from the donor ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)) because the reasoning transfers exactly:

- A torn final record is truncated to the last complete record; its bytes are preserved in a quarantine file rather than discarded.
- An **unterminated session is never truncated.** It is closed with a synthetic `agent/session-end { reason: interrupted }` — a reason no normal producer ever emits, so a repaired session is always distinguishable from a clean one. The donor's rationale applies verbatim: a single long-horizon session may contain enormous durably-written work, and truncating it to restore balance would destroy real history to satisfy a bookkeeping property.

---

## 6. The Memory Plane

Canonical, stored as append-only JSONL in `.fehrest/memory/`, fully specified in [F](05-MEMORY-MODEL.md).

Memory is canonical because a memory is an *assertion by an actor*, not a computation over documents. It cannot be recomputed from the vault: nothing in the notes records that an agent concluded on 12 June that approach X fails for reason Y.

The projection *of* memory — the current-state resolution — is derived and rebuildable.

---

## 7. Why a rich block CRDT cannot be canonical in v1

This is the architecture gate the brief flags as major. Its resolution changes the plan, so the argument is given in full.

### 7.1 The gate as posed

> Markdown on disk → editor state → edit → serialisation → Markdown → reload. Does this preserve stable identity, formatting, links, backlinks, properties, block references, comments, agent provenance, embedded objects, rich blocks?

### 7.2 The answer: not in general, and the impossibility is structural

Consider what a BlockSuite/Yjs document holds that CommonMark cannot express:

| Editor state | CommonMark equivalent | Loss |
|---|---|---|
| Per-block stable identity | None | Total — block refs break on any edit |
| Overlapping/conflicting marks | Nested emphasis only | Concurrent formatting is lossy — this is precisely Peritext's subject ([SRC-058](research/FEHREST_SOURCE_REGISTRY.md#8-research-canon)) |
| Anchored comments | None | Total |
| CRDT operation history | None | Total — merge capability is destroyed |
| Awareness/presence | None | Total (acceptable — ephemeral) |
| Database/table blocks | GFM tables (no schema, no views) | Severe |
| Embedded object references | Links only | Semantics lost |

So a lossless mapping requires a sidecar carrying block identity, marks, comments and CRDT history. But **once the sidecar carries CRDT history, the sidecar is the document** — the Markdown becomes a lossy human-readable *projection* of the real canonical state, and [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) inverts: the open file is decorative and the opaque file is authoritative.

That is the trap. It is not avoidable by better engineering; it follows from Markdown having no identity or overlap primitives.

### 7.3 The resolution: dissolve the gate

Do not adopt a document model richer than the canonical format. Then round-trip is the **identity function**, not a mapping, and there is nothing to lose.

- Canonical = Markdown bytes. The editor edits *those bytes*.
- Rich affordances that do not require a richer document model — links, backlinks, properties, provenance display, comments — come from sidecars that reference content without owning it (§4.4).
- Features that genuinely require a richer model — block transclusion, concurrent rich-text editing, database blocks — are **deferred**, and their absence is an accepted, stated v1 cost.

### 7.4 Why this is also the maintenance-safe choice

The evidence forces the same conclusion independently. BlockSuite's repository is a downstream mirror whose sync stopped 2025-07-07; `@blocksuite/store` has not been published since 2025-07-01 at pre-1.0 `0.22.4`; six dependency-vulnerability branches are open and unmerged; development happens inside a 446 MB application monorepo under a split license ([E-10](research/EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate)).

Even if the round-trip problem were solvable, it could not be solved *against a maintained upstream* — which means passing the gate would prove a property of a frozen snapshot rather than of a substrate Fehrest could build on.

Two independent lines of reasoning — structural impossibility and upstream health — reach the same decision. See [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--v1-editing-is-markdown-native-blocksuite-is-deferred).

### 7.5 What would reverse this

[H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work): if dogfooding shows users routinely need block transclusion or inline comments that sidecars cannot express, the decision reopens. It is deliberately the cheapest hypothesis in the plan to test — it needs a week of real use, not an infrastructure investment.

---

## 8. What is canonical, definitively

| State | Canonical? | Rebuildable? |
|---|---|---|
| Markdown files + frontmatter | **Yes** | No |
| Attachments | **Yes** | No |
| Event journal (T1/T2) | **Yes** | No |
| Memory assertions | **Yes** | No |
| Sidecars (annotations, block ids, provenance) | **Yes** | No |
| `vault.json` | **Yes** | No |
| Backlinks | No | Yes |
| Graph | No | Yes |
| FTS index | No | Yes |
| Embeddings / communities / summaries / thumbnails | No | Yes |
| Memory current-state projection | No | Yes |
| Event SQLite mirror | No | Yes |
| Context packages | No | Yes (from inputs + digest, §5.2) |

**One documented exception to "derived is always rebuildable":** extracted text from a *deleted* source attachment. If a user deletes the original PDF, its extracted text can no longer be regenerated. Resolution: extracted text is stored in `derived/` and is genuinely lost on rebuild — Fehrest does **not** silently promote it to canonical. The user is warned at deletion time that derived extractions will be lost. Making it canonical would mean Fehrest quietly retaining content the user tried to delete, which is worse than the data loss.
