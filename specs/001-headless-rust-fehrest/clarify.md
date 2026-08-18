# Clarification — Headless Rust Fehrest Thesis-Proof

**Status:** COMPLETE · **Date:** 2026-08-18

**Resolution order used** (Constitution, authority order): frozen architecture → G3 security reconciliation → benchmark plan → failure conditions → Ponytail.

**No founder questions were raised.** Every ambiguity below was resolvable from canonical documents. The prompt's excluded-question list (desktop shell, UI aesthetics, editor weights, publication timing, AI-OFF marketing, frontmatter ergonomics) never became necessary to execute the proof.

---

## C-01 — What counts as "supported canonical content"?

**Resolved:** Markdown-family text files (`.md`, `.markdown`) with optional YAML frontmatter.

**Source:** [D §4.1](../../docs/03-CANONICAL-DATA-MODEL.md#41-canonical-formats) lists CommonMark + GFM with YAML frontmatter as the v1 canonical body format; [F-CORE-16](../../docs/canonical/ARCHITECTURE_FREEZE.md#4-frozen-foundational-decisions) requires an allowlist.

**Ponytail:** attachments, PDF, DOCX, OCR and audio are all excluded by the authorization boundary; a broader admission table would be scaffolding for capability that cannot be built.

---

## C-02 — Where does the object UUID live?

**Resolved:** in the file's own YAML frontmatter, key `id`, UUIDv7 lowercase-hyphenated.

**Source:** [D §3](../../docs/03-CANONICAL-DATA-MODEL.md#3-object-identity) — *"Identity is stored in the file's own frontmatter, which is what makes it survive Fehrest's absence."* [ADR-0004](../../docs/09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque) fixes UUIDv7.

**Phase T narrowing:** allocation is **explicit** (`fehrest add`), not lazy-on-observation. Lazy allocation is a UX decision ([Q-5](../../docs/16-OPEN-QUESTIONS.md#q-5--how-intrusive-may-fehrest-be-with-user-files)) that is still open and that the proof does not need.

---

## C-03 — How is root containment achieved without adopting cap-std?

**Resolved for Phase T:** open the file **first**, then verify. Specifically:

1. Reject any locator that is absolute, contains a parent component, or contains a root/prefix component — before touching the filesystem.
2. Join to the vault root and open.
3. **Verify the opened handle's identity** via `std::fs::File` metadata compared against the metadata of a `symlink_metadata` probe, rejecting symlinks/reparse points on the final component.
4. Verify the canonical parent chain resolves inside the root.
5. Post-open, read the embedded UUID and compare to the requested ID.

**Source:** [E §12.1](../../docs/04-DERIVED-DATA-MODEL.md#121-two-independent-guarantees--neither-substitutes-for-the-other) requires containment **and** identity as independent guarantees. [SEC-R14](../../docs/reviews/G3-SECURITY-RECONCILIATION.md) keeps cap-std a **candidate**, not a prerequisite.

**Ponytail:** `std` reaches the contract for Phase T's read surface. If implementation had shown it could not, the correct move was a focused dependency-admission evaluation — not silent adoption. It did not.

---

## C-04 — What is "scope" in Phase T?

**Resolved:** the two dimensions the proof exercises — `vault` (required) and `project` (optional; absent = not project-restricted). `objects` and `object_types` are represented in the selector type but unused by Phase T queries.

**Source:** [F §3.4](../../docs/05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice). Specificity remains a **partial** order; incomparable selectors do not resolve.

**Why not all four:** cross-project poisoning (K-07) and vault-global minting (K-08) are exercised entirely by `vault` + `project`. Implementing unused dimensions would be scaffolding.

---

## C-05 — Which event types are needed?

**Resolved:** six. `vault/created`, `object/registered`, `object/conflict`, `memory/recorded`, `memory/superseded`, `context/compiled`.

**Source:** [Phase T scope F](../../docs/canonical/PHASE_T_AUTHORIZATION.md) — only classes needed to prove context composition, memory transition, authorization-sensitive operations, and to diagnose benchmark failure. [D §5.2](../../docs/03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)'s full T1 vocabulary is **not** implemented; tiering itself stays unfrozen pending [B-0](../../docs/10-BENCHMARK-PLAN.md#b-0--event-volume-measurement).

---

## C-06 — Incremental reindex or full rebuild?

**Resolved:** **full rebuild only.**

```
INCREMENTAL_REINDEX = YAGNI_DEFERRED
```

**Consequence, recorded honestly:** [B-12](../../docs/10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability) compares an incrementally-churned index against a freshly-built one. **With one path, that comparison cannot be made.** What Phase T *can* test — and does — is that two independent full rebuilds of the same corpus produce identical membership, ordering and package digests. The incremental-vs-full property remains **untested, and is reported as untested**, not as passed.

---

## C-07 — How is the trust envelope serialized?

**Resolved:** a typed Rust struct is the envelope; model-visible serialization is **length-prefixed**, not delimiter-based.

**Source:** [G §4.3](../../docs/06-AGENT-MODEL.md#43-two-layers-typed-internal-envelope-canonical-serialization) requires that content cannot close, open or overwrite machine-owned fields, and deliberately does **not** select an encoding family.

**Why length-prefixed:** it discharges the six normative properties **structurally**. With `content_len` preceding the bytes, no byte sequence inside content can terminate the field or begin a sibling — so escaping correctness is not a property of an escaping function that must be right everywhere. A delimiter format would make the guarantee depend on never missing an escape.

**Not claimed:** this stops *structural forgery*. It does nothing about *persuasion* ([C §7.1 item 5](../../docs/02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make)).

---

## C-08 — What does the single-writer lock use?

**Resolved:** an exclusive lock file under `.fehrest/`, created with `create_new` (atomic O_EXCL / CREATE_NEW), carrying the owning PID and start time. A second writer fails visibly with the holder's identity.

**Source:** [D §9](../../docs/03-CANONICAL-DATA-MODEL.md#9-inter-process-single-writer-discipline) requires the property and deliberately leaves the mechanism unfrozen.

**Stale-lock handling:** reported, never silently stolen. [N §1 principle 5](../../docs/13-RECOVERY-MODEL.md#1-principles) — quarantine, do not destroy to restore consistency. A lock whose owner is gone is surfaced to the user with an explicit release command; auto-stealing it would reintroduce exactly the concurrent-writer risk the lock exists to prevent.

---

## C-09 — What is the budget unit?

**Resolved:** **bytes**, not tokens.

**Source:** [H §2](../../docs/07-CONTEXT-COMPILER-SPEC.md#2-interface) requires a named tokenizer for a token budget — *"a budget without a named tokenizer is not a budget."* Phase T has no model requirement (Constitution I), so no tokenizer is available, so a token budget cannot be honest.

**Consequence:** the benchmark reports **bytes** as the context-cost metric and converts to tokens only in the harness, where a tokenizer legitimately exists. The Core never claims a token count it cannot compute.

---

## C-10 — What does the manifest hash cover?

**Resolved:** per item, `source_content_hash` (the canonical bytes read) and `rendered_hash` (the exact emitted fragment); per package, a digest over the ordered manifest entries.

**Source:** [H §3.2](../../docs/07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1).

**Not claimed:** the manifest is hash-chained into the event log, giving **partial-tamper evidence**, not authentication ([C §6.1](../../docs/02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides)). K-05 tests detection of partial modification and asserts nothing stronger.

---

## Deferred with reason (not resolved, because Phase T does not need them)

| Question | Why deferred |
|---|---|
| Lazy vs explicit UUID allocation UX | [Q-5](../../docs/16-OPEN-QUESTIONS.md#q-5--how-intrusive-may-fehrest-be-with-user-files) open; the proof uses explicit |
| Physical storage layout | [ADR-0013](../../docs/09-TECHNOLOGY-DECISIONS.md#adr-0013--storage-layout-provisional) provisional; Phase T layout is `EXPERIMENTAL_PHASE_T_FORMAT` |
| Event tiering (T1/T2/T3) | Unfrozen pending [B-0](../../docs/10-BENCHMARK-PLAN.md#b-0--event-volume-measurement); Phase T writes one durable class |
| Schema compatibility policy | [ADR-0015](../../docs/09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility) open; no migration exists yet |
| Package bodies vs manifests | [Q-15](../../docs/16-OPEN-QUESTIONS.md#q-15--should-context-packages-store-bodies-not-just-manifests) open; manifest is the frozen minimum |
