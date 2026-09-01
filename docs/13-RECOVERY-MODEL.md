# N. Recovery Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

What happens after things go wrong. Every scenario the brief names, plus those that follow from the architecture.

---

## 1. Principles

1. **Canonical data loss is never acceptable.** Derived data loss is always acceptable.
2. **Detect, do not assume.** Verify integrity on load; never trust that the last shutdown was clean.
3. **Repair is visible.** Every recovery emits an event; a repaired state is always distinguishable from a clean one.
4. **Partial function beats no function.** A vault with a corrupt graph still opens.
5. **Never destroy to restore consistency.** Quarantine damaged data; do not delete it to make the system balanced.

Principle 5 is the one most often violated in practice. The instinct when finding an unbalanced log is to truncate it. The donor's rationale is adopted directly: a single long session may contain enormous durably-written work, and truncating it to satisfy a bookkeeping property destroys real history ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)).

---

## 2. Startup integrity sequence

Runs on every launch, not only after a suspected crash:

```
1. vault.json present and parseable?        → else: vault recovery (§3.9)
2. format_version compatible?               → else: migrate or refuse (M)
3. event log: last segment intact?          → else: torn-tail repair (§3.2)
4. event log: sequence contiguous?          → else: gap quarantine (§3.3)
5. event log: hash chain valid?             → else: tamper report (§3.4)
6. unterminated sessions?                   → else: synthetic close (§3.5)
7. memory log intact?                       → else: same treatment as events
8. derived DB: integrity_check              → else: rebuild (§3.6)
9. derived freshness vs canonical           → else: incremental catch-up
10. sidecar available?                      → else: graph features hidden
```

Steps 1–7 are blocking: canonical integrity must be established before the vault opens. Steps 8–10 are non-blocking; the app becomes interactive and derived state catches up in the background.

---

## 3. Scenarios

### 3.1 Crash during a file write
**Detection.** Fehrest writes canonical files via temp-file + atomic rename, so a partial file is never visible under the real name. An orphaned temp file indicates an interrupted write.
**Recovery.** The original file is intact. The orphan is quarantined, not deleted. The user is told which edit was lost.
**Canonical loss.** Only the in-flight edit, which was never committed.

### 3.2 Crash during an event append (torn tail)
**Detection.** The final record fails to parse or its hash does not verify.
**Recovery.** Truncate to the last complete valid record, **preserving the torn bytes in a quarantine file** rather than discarding them — the torn record may be forensically meaningful, and discarding evidence to tidy up is exactly principle 5's failure mode. Emit `log/repaired`.
**Canonical loss.** At most one event, which was mid-write.

### 3.3 Sequence gap
**Detection.** `seq` is contiguous by construction; a gap means records were removed or a segment is missing.
**Recovery.** This is **not** normal crash damage — it indicates deletion, a partial restore, or tampering. Do not silently continue. Quarantine the affected segment, report to the user with the gap range, and continue in a degraded mode where replay is marked unreliable for that range.

### 3.4 Hash chain break
**Detection.** A record's `prev_hash` does not match its predecessor's `hash`.
**Recovery.** Report as a **potential tampering event** ([T-4](02-THREAT-MODEL.md#t-4--event-log-tampering)), naming the exact record. Do not auto-repair; auto-repairing a tamper indicator destroys the only signal. The vault remains usable; provenance claims for events after the break are marked unverified.
**Honest limit.** This is tamper-evidence, not tamper-resistance. A determined local user can rewrite the whole chain.

### 3.5 Unterminated session (interrupted turn)
**Detection.** `agent/session-start` with no matching `agent/session-end`.
**Recovery.** Append a synthetic `agent/session-end { reason: "interrupted" }` — a reason **no normal producer ever emits**, so a repaired session is permanently distinguishable from a clean one. Never truncate the session's events. Adopted directly from the donor ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)).
**Canonical loss.** None.

### 3.6 Corrupt SQLite (derived)
**Detection.** `PRAGMA integrity_check` at open, or a corruption error at runtime.
**Recovery.** Move the database aside, rebuild D1 from canonical state, resume. No user decision required.
**Impact.** Unavailable for the D1 rebuild window — under 60 s at 10K files ([O](14-PERFORMANCE-BUDGETS.md)). D2 rebuilds in the background afterwards.
**Canonical loss.** None, by [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable). This is the invariant paying for itself: what would be a data-loss incident in a database-canonical design is a scheduled inconvenience here.

### 3.7 Deleted derived index
**Detection.** Files missing at startup.
**Recovery.** Rebuild. This is a **supported operation**, not an error — deleting `.fehrest/derived/` is a documented support instruction.

### 3.8 Interrupted rebuild
**Detection.** A rebuild-progress marker exists without a completion marker.
**Recovery.** Resume from recorded progress. Rebuild is chunked and progress is durable, so a 90-minute 100K-file graph build ([E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)) never restarts from zero. Partial indexes are usable and marked incomplete rather than hidden.

### 3.9 Missing or corrupt `vault.json`
**Detection.** Absent or unparseable.
**Recovery.** Reconstruct from the event log's earliest records, which contain the vault id and creation time. If the log is also gone, the directory is treated as a new vault after **explicit user confirmation** — this is the one place where a wrong automatic decision could orphan an entire history, so it is never automatic.

### 3.10 Concurrent editor (external modification)
**Detection.** Content hash differs from the indexed hash. Hash, never mtime — mtime is unreliable across sync tools and restores, and trusting it enables the provenance race in [T-9](02-THREAT-MODEL.md#t-9--filesystem-race-conditions).
**Recovery.** External modification is **normal and expected** — it is the point of an open vault. Re-index the file, re-anchor sidecar annotations, mark unresolvable anchors orphaned and show them to the user rather than dropping them, emit `object/updated` with `actor: external`.
**Conflict case.** If Fehrest has unsaved in-app changes to the same file, do not merge and do not overwrite: present both versions and let the user choose. Without a CRDT ([ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent)) there is no principled automatic merge, and pretending otherwise silently destroys one side.

### 3.11 Git operations on the vault
**Detection.** Many files change at once; hashes diverge en masse.

> **Mechanism, named in F1-R2 ([SRC-110](research/FEHREST_SOURCE_REGISTRY.md#src-110--gitoxide-gix)).** This scenario requires reading repository state — refs, index, worktree, status, ignore rules — and F1 specified the *behaviour* without naming how. **`gitoxide`/`gix` is the candidate for reading correctness-sensitive Git state through a typed API rather than by parsing shell `git` porcelain output**, which is a documented source of locale, version and encoding defects. Evaluated, not adopted.
>
> **Git remains optional.** [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default) makes the vault an ordinary directory, and most vaults will not be repositories. No code path may make Git mandatory, and a vault with no `.git` must behave identically minus these scenarios.

**Recovery.** Treated as bulk external modification. A debounced full reconciliation scan rather than thousands of individual watcher events — watchers are unreliable under bulk change, and a missed event that silently drops a file from the index is indistinguishable from a suppression attack ([T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes)).
**Specific hazards.** A checkout to a commit before Fehrest existed removes identity frontmatter — files are re-identified and the association reported. `.fehrest/` should be git-ignored by default *except* the event and memory logs if the user wants history versioned; this is a documented choice, with the caveat that git merge conflicts in an append-only log are painful and the default is to ignore the whole directory.

### 3.12 Partial upgrade
**Detection.** Application version and vault version mismatch; or a sidecar version incompatible with the core.
**Recovery.** Version compatibility is checked at startup. A mismatched sidecar is refused and the graph disabled rather than run with an unknown schema — accepting unvalidated extraction output from an unexpected version would violate boundary B2 ([threat model §4](02-THREAT-MODEL.md#4-trust-boundaries)). Migration proceeds per [M](12-MIGRATION-SCHEMA-EVOLUTION.md), resumably.

### 3.13 Sidecar crash or failure to start
**Detection.** Process exit, IPC timeout, or health-check failure.
**Recovery.** Supervisor restarts with exponential backoff. After N consecutive failures, disable graph features, notify the user, and continue. Extraction jobs are idempotent and resumable, so a crash mid-extraction loses only the in-flight file.
**Impact.** Reduced retrieval recall. **The application remains fully usable** — this is the tiering rule in [E §2](04-DERIVED-DATA-MODEL.md#3-tiering) being load-bearing.

### 3.14 Plugin failure
Not applicable to v1 — no plugin system. When plugins arrive, the required properties are: a plugin crash cannot take down core, cannot corrupt canonical state, and cannot escalate capability. The isolation seam is preserved ([SRC-043](research/FEHREST_SOURCE_REGISTRY.md#7-agent-protocol-authorization-isolation)).

### 3.15 Disk full
**Detection.** Write failure.
**Recovery.** Canonical writes fail loudly and the user is told **before** any data is lost — never a silent partial write. Derived rebuilds abort cleanly, retaining the previous index. Fehrest maintains a reserve threshold and refuses to start large derived rebuilds below it, since a rebuild that fills the disk mid-run is worse than no rebuild.

### 3.16 Clock moved backwards
**Detection.** A new event's system timestamp precedes the previous event's.
**Recovery.** `seq` remains monotonic and is the authoritative ordering — timestamps are metadata, not ordering. The anomaly is recorded as an event. Bitemporal resolution ordering ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)) uses `recorded_at` as a tiebreak, so a large backward jump could theoretically invert two memories' precedence; the recorded anomaly makes this diagnosable rather than mysterious.

### 3.17 Vault moved or copied
**Detection.** Vault path differs from the recorded path.
**Recovery.** Normal — paths are locations, not identity ([I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities)). Update the path; nothing else changes. A *copied* vault produces two vaults with the same vault id; on detection, offer to re-identify one. Two vaults with duplicate object IDs would otherwise cause cross-contamination if they were ever merged.

---

## 3A. Hostile filesystem and sync environments

> **ADDED IN F1-R2 ([R2-13](reviews/F1-R2-RECONCILIATION.md)).** §3 models failures of *Fehrest's own operations*. It does not adequately model the environment those operations run in. The founder's own environment is Windows 11 with the vault under **OneDrive** ([E-15 environment](research/EVIDENCE_LOG.md#measurement-environment)) — a case where transient locks, placeholder files and sync-driven rewrites are ordinary rather than exceptional. A recovery model that assumes a quiet local disk is modelling a machine nobody has.

### 3A.1 Transient locks and sharing violations

**Windows in particular** returns sharing violations when another process — an editor, an indexer, an antivirus scanner, a sync client — holds a file open. These are **transient and expected**, not errors.

**Handling.** Bounded retry with exponential backoff and a maximum attempt count, applied to reads and to atomic-rename writes. On exhaustion: **fail the operation loudly, retain the original, and record the failure** — never a partial write, never a silent skip. A file that could not be read is reported as unindexed, not as absent, because "absent" is indistinguishable from a suppression attack ([T-16](02-THREAT-MODEL.md#t-16--corrupted-derived-indexes)).

### 3A.2 Watcher storms

Bulk operations — a `git checkout`, a sync catch-up, a mass rename — generate event volumes that overwhelm a naive watcher, and dropped events are the dangerous outcome.

**Handling.** Debounce and coalesce; **above a threshold, escalate from per-file events to a full reconciliation scan** rather than attempting to process the flood. The watcher is a latency optimisation; **reconciliation is the correctness mechanism** ([E §6](04-DERIVED-DATA-MODEL.md#6-incremental-maintenance)). This is already the rule for [§3.11](#311-git-operations-on-the-vault); R2 generalises it to any bulk source.

### 3A.3 Partial, offline and cloud placeholder files

Cloud sync clients present files that are **not locally present**: OneDrive Files On-Demand and iCloud "optimised storage" leave a placeholder whose metadata exists and whose content requires a network fetch — which may be slow, may prompt, or may fail entirely on a metered or offline connection.

**Handling.** Detect placeholder/offline state **before** reading. A placeholder is **not** an empty file and must never be indexed as one — that would replace real content with nothing in the derived index and, worse, would look like a legitimate edit. Placeholders are recorded as `content_unavailable`, retried later, and **never hydrated implicitly**: silently pulling a user's entire archive down from the cloud because Fehrest wanted to index it is a data-charge and disk-space event the user did not authorise.

### 3A.4 Hard links, symlinks and external modification

- **Symlinks and junctions** are not followed by default ([T-8](02-THREAT-MODEL.md#t-8--symlink-and-junction-attacks)). Unchanged.
- **Hard links**, where the platform supports them, mean one object with two paths. Reconciliation must not treat the second path as a copy: identity comes from the embedded UUID ([D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics)), so a hard link resolves to the same object and the additional path is recorded as an additional location, surfaced to the user rather than silently deduplicated.
- **External modification** is normal and expected ([§3.10](#310-concurrent-editor-external-modification)).

### 3A.5 Sync rollback and conflict patterns

Sync clients resolve conflicts by their own rules, which include creating conflict-copy files, restoring earlier revisions, and rewriting files Fehrest believes are current.

**Handling.** A file whose content returns to a **prior known revision** is a real, observable event: **preserve that fact in provenance** — record that content reverted to a previously-seen hash, with both hashes and the time. **Do not invent user intent.** Fehrest does not know whether a revert was a deliberate restore, a sync conflict resolved against the user, or a backup rollback, and guessing produces a confident and wrong history. It is recorded and surfaced.

Conflict-copy files (`document (conflicted copy).md`, `document 2.md`) that carry a **duplicate embedded UUID** are handled as identity conflicts ([D §3.2](03-CANONICAL-DATA-MODEL.md#32-identity-across-filesystem-operations)): both retained, neither discarded, surfaced for resolution.

### 3A.6 Disk full and concurrent editors

Covered by [§3.15](#315-disk-full) and [§3.10](#310-concurrent-editor-external-modification); listed here because they co-occur with sync pressure far more often than with local-only use.

### 3A.7 Cloud-sync compatibility is an EMPIRICAL GATE, not an assumption

> **What was NOT accepted ([R2-13](reviews/F1-R2-RECONCILIATION.md)).** The review asserted specific behaviours of particular sync clients — guaranteed version-history reset, guaranteed delete-plus-create semantics. **Those claims are not adopted.** They are unverified, they vary by client version, platform, account type and per-folder configuration, and designing recovery around an unverified vendor behaviour is how a recovery model acquires a confident false assumption. Fehrest already made an absence-of-signal error twice in F1; asserting a *presence* of behaviour without testing it is the same error inverted.

**Support is claimed only after measurement.** Before Fehrest states that a sync environment is supported, it must pass the recovery suite **running on**:

| Environment | Status |
|---|---|
| **OneDrive on Windows** | Required before claiming support. The founder's own environment |
| **iCloud Drive on macOS** | Required before claiming support |
| Dropbox, Google Drive, Syncthing, others | Untested. Reported as untested, not as unsupported and not as supported |

**Until a given environment is tested, its status is `UNTESTED`** — which is a statement about Fehrest's knowledge, not about the environment.

### 3A.8 Checkpoint loss

**Detection.** No valid projection checkpoint at startup: absent, digest mismatch, or `schema_version` / `deriver_version` mismatch ([E §11](04-DERIVED-DATA-MODEL.md#11-projection-checkpoints)).
**Recovery.** Discard the invalid checkpoint. Fall back to an older valid checkpoint if one exists; otherwise replay canonical state in full. Record the event.
**Canonical loss.** **None** — checkpoints are derived, non-authoritative and disposable by construction.
**Duration.** Healthy-start budgets are in [O §3](14-PERFORMANCE-BUDGETS.md#3-startup). **The degraded full-replay path is deliberately unbudgeted pending measurement** ([R2-08](reviews/F1-R2-RECONCILIATION.md)); the vault remains readable throughout, since replay rebuilds projections rather than gating access to canonical files.

---

## 4. Backup

Fehrest does not implement backup. It makes the vault **backup-friendly**: ordinary files, no database required for canonical state, no exclusive locks on canonical files, and any file-level backup tool works.

Recommended: back up the whole vault directory, excluding `.fehrest/derived/`. Restoring canonical files plus the event and memory logs is a complete restore.

Fehrest **does** prompt for a backup before any major migration ([M §6](12-MIGRATION-SCHEMA-EVOLUTION.md#6-migration-execution)) and provides `fehrest export` for a Fehrest-independent copy ([I-9](01-ARCHITECTURE-CONSTITUTION.md#i-9--export-does-not-depend-on-fehrest-infrastructure)).

---

## 5. Recovery events

All T1, all permanent:

```
log/repaired          { kind, segment, records_affected, quarantine_path }
log/gap-detected      { from_seq, to_seq }
log/chain-broken      { at_seq }
session/interrupted   { session_id }
index/rebuilt         { scope, reason, duration_ms }
vault/reconstructed   { source }
object/reidentified   { old_id, new_id, reason }
anomaly/clock-regression { previous_ts, observed_ts }
```

Recovery is itself auditable. A user (or reviewer) can ask what has ever gone wrong with this vault and get a complete answer — which is only possible because repair never rewrites history, it appends to it.

---

## 6. Testing

Every scenario above has an automated test using fault injection at a specific point ([L §8](11-SECURITY-VERIFICATION-PLAN.md#8-recovery-tests)). Assertions for all: **zero canonical data loss**, automatic detection, automatic or clearly-guided recovery, and a recorded event.

Chaos testing at Phase 5: random kills, disk-full injection, clock manipulation, concurrent external modification, and bulk git operations, run against a real vault under load.

**Added in F1-R2 — environment testing, on real clients:** the §3A scenarios are exercised against **real OneDrive on Windows and real iCloud Drive on macOS**, not against a simulation. Simulating a sync client tests the simulation. This is the [§3A.7](#3a7-cloud-sync-compatibility-is-an-empirical-gate-not-an-assumption) compatibility gate, and it is what converts "we handle sync" from a claim into a measurement.

---

## 7. What cannot be recovered

Stated plainly, because a recovery document that implies everything is recoverable is misleading:

| Loss | Recoverable? |
|---|---|
| Canonical files deleted outside Fehrest with no backup | **No** |
| Event log deleted with no backup | **No** — history cannot be recomputed |
| Memory log deleted with no backup | **No** |
| Extracted text after the source attachment is deleted | **No** — and deliberately not promoted to canonical ([D §8](03-CANONICAL-DATA-MODEL.md#8-what-is-canonical-definitively)), because silently retaining content the user deleted is worse than losing the extraction |
| An in-flight edit at crash time | No — but it was never committed |
| Sidecar annotations whose anchors no longer resolve | Partially — reported as orphaned, never silently dropped |

The first three are why backup guidance is part of onboarding rather than documentation. Fehrest's canonical state is genuinely the user's responsibility, which is the direct cost of it being genuinely the user's property.
