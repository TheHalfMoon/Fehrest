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

## 2. Storage categories (provisional layout)

> **PROVISIONAL — [R1-17](reviews/F1-R1-RECONCILIATION.md).** The hierarchy below is a **worked illustration**, not a commitment. The *semantic categories* are stable and may be designed against; the *physical layout* is deferred to a successor ADR after the Phase 1–2 storage and recovery prototypes ([ADR-0013](09-TECHNOLOGY-DECISIONS.md#adr-0013--storage-layout-provisional)).

**Semantic categories — stable:**

| Category | Class | Rebuildable? |
|---|---|---|
| Canonical identity | canonical | No |
| Canonical events | canonical | No |
| Canonical explicit memory | canonical | No |
| Canonical content + attachments | canonical | No |
| Schema / version state | canonical | No |
| Derived search index | derived | Yes |
| Derived graph | derived | Yes |
| Derived vectors | derived | Yes |
| Cache (extracted text, thumbnails, summaries) | derived | Yes |

**The one binding layout constraint ([R1-16](reviews/F1-R1-RECONCILIATION.md)):** canonical and derived state must be **separable by directory**, so derived state can be deleted wholesale without touching canonical state.

> ⚠️ **`.fehrest/` is NOT disposable.** It contains canonical event and memory state. Only its **derived subtree** is disposable. Reading "delete `.fehrest/`" as a recovery step would destroy irreplaceable history. See [E §1](04-DERIVED-DATA-MODEL.md#1-two-classes-of-state-inside-fehrest).

**Illustrative layout:**

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

**Extractor IDs are never identities.** Extractor-generated identifiers — Graphify's included — are name- or path-derived and their schemes change across versions ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)). They appear only as a derived mapping column, rebuildable on demand. Enforced by invariants [G-ID-1…G-ID-4](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) and `test_extractor_ids_are_not_identities`.

### 3.2 Identity across filesystem operations

**Added in F1-R1 ([R1-15](reviews/F1-R1-RECONCILIATION.md)).** F1 covered rename and move. The harder cases are copy, duplicate, conflict and restore — where the system must distinguish *the same object in a new place* from *a new object that looks identical*.

**The discriminator is the pair `(embedded id, content hash)` compared against the index**, evaluated at the moment a file is observed:

| Observation | Interpretation | Action |
|---|---|---|
| Known id, new path, old path gone | **Moved** | Update path. Identity, links, memories, history all preserved |
| Known id, new path, **old path still present** | **Copied / duplicated** | Original keeps the id. Copy is re-identified with a fresh id, `object/duplicated` recorded with `derived_from` |
| Known id, same path, different content hash | **Edited** | Update hash, re-index, `object/updated` |
| Unknown id, content matches a known object | **Restored / re-imported** | Offer re-association to the user. **Never silently merge** |
| No id at all | **New or externally stripped** | Allocate lazily; if content strongly matches a known object, offer re-association |
| Two live files, same id | **Conflict** | Both retained. Neither is silently discarded. Surface for resolution; `object/id-conflict` recorded |
| Id absent after `git checkout` to a pre-Fehrest commit | **History rewind** | Re-identify on next write; report the association |

**Operation matrix:**

| Operation | Identity | Notes |
|---|---|---|
| Rename | **Preserved** | Path is an attribute |
| Move across directories | **Preserved** | Same |
| Folder restructuring | **Preserved** | Bulk path update via reconciliation scan |
| Case-only rename | **Preserved** | Case-insensitive filesystems need explicit handling |
| `git checkout` (branch switch) | **Preserved** where frontmatter survives | Bulk external modification ([N §3.11](13-RECOVERY-MODEL.md#311-git-operations-on-the-vault)) |
| `git checkout` to pre-Fehrest commit | **Lost, then re-associated** | Reported, never silently guessed |
| Copy | **New identity for the copy** | Original unaffected |
| Duplicate in place | **New identity** | `derived_from` recorded |
| Merge conflict (both sides edited) | **Preserved, conflict surfaced** | No automatic merge without a CRDT ([ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent)) |
| Restored backup | **Preserved**; rollback checks apply | [T-15](02-THREAT-MODEL.md#t-15--rollback-and-replay-abuse) |
| External editor save | **Preserved** if frontmatter untouched | Hash-detected re-index |
| Import from outside the vault | **New identity**, `import/ingested` with source provenance | Never inherits a foreign id |
| Export | Identity travels in frontmatter | What makes the vault portable |

**Two rules that make this tractable:**

1. **Path hashing does not solve identity** and is not used. Two files with identical content are not the same object; one file at two paths over time is. Only an embedded allocated id distinguishes these.
2. **Ambiguity is surfaced, never guessed.** Copy-vs-move and restore-vs-new are genuinely ambiguous from the filesystem alone. Silently guessing wrong merges two objects' histories — an unrecoverable corruption of exactly the provenance Fehrest exists to protect.

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

Links are written in the file, in one of two forms: `[[wikilink]]` (Obsidian-compatible, resolved by title/path) or a standard Markdown link whose target is `fehrest://object/<uuid>` (identity-stable).

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

**Why `context/compiled` stores inputs and a digest rather than the package body:** storing every package body means storing the vault repeatedly. Storing inputs plus a digest satisfies [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) by *recomputation*, and the digest proves the recomputation matches. This is the harness's derive-don't-store principle applied to context.

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

## 7. The rich-editor ↔ canonical-file question (OPEN)

> **REOPENED IN F1-R1 ([R1-04](reviews/F1-R1-RECONCILIATION.md)).** F1 argued here that lossless round-trip is *structurally impossible* and dissolved the gate by choosing a Markdown-native editor. **That impossibility argument is retracted.** It conflated separable concerns and was never demonstrated. The question is open and is decided by the [Editor Gate](18-EDITOR-GATE.md), not by argument.

### 7.1 The question

> Canonical file on disk → editor state → edit → serialisation → canonical file → reload. What is preserved, what is lost, and is the loss disclosed?

### 7.2 The retracted argument, and why it failed

F1 reasoned: a rich editor holds CRDT operation history; Markdown cannot express it; therefore a lossless sidecar must carry that history; therefore the sidecar becomes the real document and Markdown becomes decorative.

The flaw is the third step. It assumes **CRDT operation history is part of canonical document meaning.** That was asserted, not shown. A CRDT's operation log is the mechanism by which concurrent edits converge — closer to a version-control object database than to the document's content. A git repository's object store is not part of what a source file *means*, and no one concludes from its existence that the working tree is decorative.

### 7.3 Six separable concerns

The correct decomposition, which F1 collapsed:

| # | Concern | Canonical? | Notes |
|---|---|---|---|
| 1 | Semantic document content | **Yes** | The user's knowledge |
| 2 | Structured metadata (properties, types) | **Yes** | Frontmatter today |
| 3 | Stable block identity | **Yes**, where block references exist | Needs a home Markdown lacks |
| 4 | Provenance, comments, annotations | **Yes** | Sidecar (§4.4) |
| 5 | Collaboration history (CRDT ops) | **Not established** | Likely machinery, not meaning |
| 6 | Transient runtime state (selection, presence, undo) | **No** | Uncontroversially ephemeral |

Only concern 5 was ever in dispute, and it is the one F1 assumed rather than tested.

### 7.4 Candidate architecture — to be tested, not adopted

```
note.md
    canonical human-readable content                 (concerns 1, 2)

note.fehrest.json
    canonical structured metadata, only when needed:
      - stable block IDs                             (concern 3)
      - provenance, comments                         (concern 4)
      - metadata for rich objects Markdown cannot express

Y.Doc / CRDT state
    transient or collaboration-specific,
    unless independently proven canonical            (concern 5)
```

**Not adopted.** Recorded so the gate has a concrete hypothesis to falsify.

### 7.5 The proof obligation

Whichever candidate wins must demonstrate, with a running prototype ([18-EDITOR-GATE §4](18-EDITOR-GATE.md#4-the-round-trip-proof-obligation)):

- **P-1** Round-trip fidelity, with every deviation enumerated.
- **P-2** No silent loss — anything unrepresentable is *reported*.
- **P-3** Identity stability across edit, reload, rename, move, external edit.
- **P-4** External-edit tolerance.
- **P-5** Canonical sufficiency — canonical files alone reconstruct the document.
- **P-6** Sidecar boundedness — a sidecar carries **no content**, only references plus metadata; deleting it loses annotations, never the document.

**P-6 is the discriminator.** If a candidate's sidecar must carry document content or operation history to round-trip, F1's concern was real for that candidate. If it need not, the concern was unfounded. That is an experiment, and it is cheap relative to the decision it settles.

### 7.6 What is not open

Whatever wins, the constitution binds it: canonical artifacts stay open, specified, locally readable and losslessly exportable ([I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended)); derived state stays rebuildable ([I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)); unknown fields survive writes ([R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)). A candidate that cannot meet these is eliminated regardless of capability.

**Also not open:** whether Fehrest is a Markdown editor. It is not, under any outcome. The editor is one surface over the [four-layer architecture](00-PRODUCT-THESIS.md#5-the-four-layer-architecture).

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
