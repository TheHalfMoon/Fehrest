# M. Migration and Schema Evolution Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

A knowledge store intended to hold a decade of a person's thinking will outlive many of its own schemas. Migration is therefore a core subsystem, not an operational afterthought.

---

## 1. Governing rules

1. **Canonical formats evolve additively.** Removing or repurposing a field requires a major version and a migration.
2. **Unknown fields are preserved verbatim.** A newer version's data passing through an older version must survive ([R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).
3. **Fail loudly on incompatibility.** Never silently drop, coerce, or "best-effort" canonical data.
4. **Derived state is never migrated.** It is rebuilt ([I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)). This removes the entire class of derived-schema migration bugs — a direct dividend of the disposability invariant.
5. **Every migration is reversible or explicitly one-way**, and one-way migrations require a pre-migration backup.
6. **Migration is an event** (`schema/migrated`, T1).

---

## 2. Versioned surfaces

| Surface | Version location | Migration |
|---|---|---|
| Vault format | `.fehrest/vault.json` → `format_version` | Explicit, gated |
| Frontmatter schema | Per-file `fehrest_schema` (absent = v1) | Lazy, per-file |
| Event record schema | Per-record `v` field | Read-time upcasting |
| Memory record schema | Per-record `v` field | Read-time upcasting |
| Sidecar schema | `format_version` in file | Lazy, per-file |
| Derived schema | `user_version` pragma | **Rebuild, never migrate** |
| Compiler output | `compiler_version` in package | Not migrated; packages are derived |

Three different strategies appear here deliberately, matched to the data's properties:

- **Event and memory logs use read-time upcasting.** They are append-only and can be enormous; rewriting them would be slow, would break hash chains, and would destroy the tamper-evidence property ([T-4](02-THREAT-MODEL.md#t-4--event-log-tampering)). Old records stay on disk in their original bytes forever and are upcast in memory on read.
- **Files use lazy per-file migration.** A vault of 100K files cannot be migrated atomically without a long unavailable window, and a partial migration must leave a working vault.
- **Derived state is rebuilt.** Always.

---

## 3. Event and memory log evolution

```
{ "v": 1, "seq": 142, "type": "memory/promoted", ... }
```

**Rules.**
- Records are **never rewritten**. Rewriting would invalidate `prev_hash`/`hash` and destroy tamper-evidence.
- An upcast chain `v1 → v2 → v3` runs in memory on read; each step is a pure function with a golden-file test.
- A new event *type* is purely additive. Unknown types encountered by an older reader are **retained and skipped**, never dropped — dropping would silently corrupt history.
- Removing an event type is forbidden. It is deprecated: no longer emitted, still readable, upcast forever.
- The upcast chain is permanent. Deleting an old upcaster makes historical logs unreadable, which is data loss.

> **The permanence of the chain is REOPENED as a question in F1-R2 ([R2-17](reviews/F1-R2-RECONCILIATION.md)) — see [ADR-0015](09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility).** "Support every historical schema forever, in the running binary" creates an **unbounded maintenance and security surface**: each upcaster is rarely-exercised parsing code, operating on old and potentially attacker-influenced data, that can never be deleted — inside the one component whose corruption is unrecoverable ([L §4](11-SECURITY-VERIFICATION-PLAN.md#4-fuzzing)).
>
> **The obvious fix is also wrong.** Bounding the window and dropping old upcasters abandons old-vault readability, which contradicts *the user's knowledge must survive Fehrest itself*. **Both horns are real**, so ADR-0015 frames a study — bounded live runtime window, separate versioned migration tooling, permanently published historical format specifications, mandatory pre-migration backup, migration epochs at major boundaries — and **deliberately does not freeze a policy on R2 evidence**, which consists of no implementation and no schema history.
>
> **The property that must survive whatever is chosen:** a user-owned old vault must not become unreadable *merely because Fehrest evolved*. "Readable via a documented migration tool" is an acceptable narrowing; "readable only if you kept a five-year-old binary" is not.

**Compaction interaction.** Compaction ([D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)) writes new segments and marks old ones superseded while retaining their digests. Compacted-away T2 records are gone by design, but T1 records are never compacted, so the schema-evolution guarantee applies in full to everything permanent.

---

## 4. File-level migration

```yaml
---
id: 0198f2a1-...
fehrest_schema: 2       # absent means 1
---
```

**Lazy strategy.** Migrate a file when it is next written, not on upgrade. Reading tolerates any known version.

Rationale: a 100K-file eager migration is a multi-minute rewrite of the user's entire vault — slow, risky under crash, catastrophic for any sync tool watching the directory, and it touches `mtime` on files the user did not edit. Lazy migration means the vault is immediately usable after upgrade and files migrate as they are touched.

**Cost, stated:** a vault can contain multiple schema versions indefinitely. Readers must therefore support **every** historical version forever. This is the deliberate trade — permanent reader complexity in exchange for never blocking on a bulk rewrite. An explicit "migrate all now" command exists for users who prefer uniformity.

**Whether "forever" means "in the running binary" is now an open question** ([ADR-0015](09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility)). The lazy strategy itself is unaffected either way; what ADR-0015 decides is where the reading capability *lives* once the chain is long.

---

## 5. Compatibility policy

| Change | Version | Old version reading new data |
|---|---|---|
| New optional field | Minor | Preserved verbatim, ignored |
| New event type | Minor | Retained, skipped |
| New memory type | Minor | Retained, not resolved |
| New object type | Minor | Treated as generic object |
| Field becomes required | **Major** | Refuses to load, with a clear message |
| Field removed/repurposed | **Major** | Refuses to load |
| ID scheme change | **Major** | Refuses to load |
| Hash algorithm change | **Major** | Chain verification breaks at the boundary |

**Downgrade.** A vault touched by a newer major version is refused by an older one, with a message naming the required version. Refusal is correct: a silent partial read of a newer vault is how knowledge gets destroyed.

Minor-version downgrade works precisely because of the unknown-field preservation rule. This is why [R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) is a constitutional rule and not a style preference — without it, every minor upgrade becomes a one-way door.

---

## 6. Migration execution

```
1. Detect       compare vault.json format_version to app version
2. Assess       is it forward, backward, major, minor?
3. Backup       required for any major or one-way migration
4. Announce     what will change, what is reversible, estimated time
5. Consent      user confirms (or --yes for automation)
6. Execute      transactional per unit; resumable
7. Verify       post-conditions checked
8. Record       schema/migrated event with from/to and counts
9. Rebuild      derived state invalidated and rebuilt
```

Every migration is **resumable**: progress is recorded, and an interrupted migration continues rather than restarting or leaving a half-state. A migration that cannot be made resumable must be atomic; if it can be neither, it is not permitted.

---

## 7. Failure handling

| Failure | Response |
|---|---|
| Migration interrupted | Resume from recorded progress; vault remains usable |
| A file fails to migrate | Skip, quarantine-report, continue; never abort the whole run |
| Post-condition check fails | Halt, restore from backup, report |
| Disk full mid-migration | Halt cleanly, retain original, report |
| Unknown future version found | Refuse to load; name the required version |
| Corrupt file encountered | Quarantine, continue, report ([N](13-RECOVERY-MODEL.md)) |

The "skip and continue" policy is deliberate: one malformed file must not make an entire vault unmigratable, which would be a denial-of-service on the user's own knowledge via a single bad file.

---

## 8. Testing

- **Golden files** for every historical schema version, committed and never modified. Every upcaster is tested against them.
- **Round-trip:** write with v_new, read with v_old, assert unknown fields survive.
- **Property:** upcasting is idempotent and order-independent along the chain.
- **Fault injection:** interrupt migration at each stage; assert resumability and zero canonical loss.
- **Long-chain:** synthesise a v1 vault, migrate through every version to current, verify content equality.

The long-chain test is the one that catches the failure that only appears after years — an upcaster that works v3→v4 but breaks when the input arrived via v1→v2→v3.

---

## 9. Anticipated migrations

Named now so the mechanism is designed against real cases rather than hypotheticals:

| Likely change | Type | Trigger |
|---|---|---|
| Additional memory types | Minor | Ordinary evolution |
| Additional event types | Minor | New capabilities |
| Embedding model change | Derived only | Rebuild; no migration |
| Sidecar format extension | Minor | Richer annotations |
| **Canonical event log → binary format** | **Major** | If JSONL misses durability/size budgets ([ADR-0001](09-TECHNOLOGY-DECISIONS.md#adr-0001--canonical-state-is-open-files-plus-an-append-only-event-log) reversal) |
| **Sidecar becomes canonical for rich documents** | **Major** | If [H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work) is falsified ([ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated) reversal) |
| Identity scheme change | Major | Only if [ADR-0004](09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque) reverses |

The two major ones correspond exactly to the two ADRs most likely to reverse. That is intentional: the migration mechanism must be strong enough to survive the plan's own most probable changes of mind, or those reversals become impossible in practice and the ADRs' "reverses if" clauses are fiction.
