# F1-R2 Architecture Reconciliation

**Phase:** `F1-R2` ACTIVE
**Date:** 2026-08-17
**Canonical repository:** `TheHalfMoon/Fehrest` (private, `main`, size 0, no implementation)
**Prior state:** F1-R1 package + two pre-G2 governance corrections, local commit `bb6c1251648741c4ca4e436ca4a054a51b771972`
**Next gate:** GPT-5.6 Sol R2 delta review → GLM-5.3 security/cyber review → architecture freeze → founder implementation authorization

**Implementation is NOT authorized. No product code was written in F1, F1-R1 or F1-R2.**

---

## 1. What this document is

A precise delta against the G2-reviewed package, incorporating the **19 Codex findings as validated by GPT-5.6 Sol** plus three new founder decisions.

| Verdict class | Count | Handling |
|---|---|---|
| **VALID** | 13 | Applied in full |
| **PARTIAL** | 5 | Valid portion applied; rejected portion recorded with reasoning |
| **NEEDS_EVIDENCE** | 1 | Left open, with a measurement task and an explicit "not adopted" |
| **REJECTED by validation** | 0 | — |

**The governing discipline of this round.** Several findings arrived with a proposed fix attached. Where the fix was right it was taken; where the fix was **a plausible-looking answer that would have been wrong**, the *finding* was accepted and the *fix* was not. Four such cases are recorded in §3, because a reconciliation that silently adopts a reviewer's remedy is not a reconciliation — it is a transcription.

---

## 2. Founder decisions recorded

### D-1 — Rust is the canonical Fehrest Core language · `ACCEPTED`

Closes [ADR-0010](../09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) and [Q-2](../16-OPEN-QUESTIONS.md#q-2--core-implementation-language-closed), both `OPEN` since F1.

Rust owns all correctness- and security-sensitive product logic: canonical domain model, stable identity, filesystem reconciliation, canonical write/recovery semantics, SQLite/storage, migrations, FTS integration, event/audit primitives, temporal memory, deterministic resolution, retrieval, context compilation, provenance, authorization, agent gateway, MCP server, CLI, recovery, and every security-sensitive boundary.

TypeScript/React may be used for presentation. **No business-critical state semantic may be duplicated in TypeScript.** Python may be used only behind an explicit optional process boundary for hypothesis-gated donor capabilities; **canonical operation must not require it.**

**Two new invariants make this testable rather than declarative:**

- **[I-16](../01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)** — if the desktop UI disappears, Fehrest remains operable through its Rust Core and CLI.
- **[I-17](../01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)** — if Python disappears, canonical knowledge, memory and recovery remain usable.

**[ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) (desktop shell) is deliberately NOT resolved.** Tauri 2 remains the leading candidate; "our core is Rust, therefore our shell is Tauri" is an association, not an argument.

### D-2 — GitHub Spec Kit is the canonical specification-driven workflow · `ACCEPTED`

`constitution → specify → clarify → plan → checklist → tasks → analyze → implement → converge`, with a **justified** reduced workflow permitted for small bounded work.

### D-3 — Ponytail is the canonical implementation-minimisation discipline · `ACCEPTED`

Six-question necessity/reuse gate, with a **hard exclusion list** — authorization boundaries, canonical-data integrity, security controls, recovery correctness, provenance, privacy, data-loss prevention, required accessibility, invariant tests.

**Both D-2 and D-3 are development/governance tooling and are NOT runtime dependencies** — enforced by [R-11](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules). Neither was installed, initialized or executed during F1-R2. New documents: [S — Engineering Method](../19-ENGINEERING-METHOD.md), [ADR-0014](../09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail).

---

## 3. Substance NOT accepted — recorded explicitly

Four proposed remedies were rejected while their findings were accepted. Each is recorded here because the difference between "the finding was wrong" and "the fix was wrong" matters to the next reviewer.

### 3.1 G2-M2 — `10K–100K events/day` NOT accepted as fact

The claim is an **unverified estimate**, offered without measurement. It is not adopted.

The existing **500 events/day is equally ungrounded** and is not defended either. Both are reclassified as `UNVALIDATED PLANNING ASSUMPTION`, and [B-0](../10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) measures real multi-agent volume by class at Phase 0.

**A 200× disagreement about a load-bearing input is itself the finding.** Replacing one ungrounded number with a larger ungrounded number would change which decisions are wrong without making any of them right.

### 3.2 G2-H7 — `n ≈ 300+` NOT accepted as a universal sample size

Required n is **derived, not constant**: it depends on paired-vs-independent design, baseline rate, discordance, minimum meaningful effect, α, power, and the primary endpoint. Freezing a guessed n replaces one unjustified number with another.

**Accepted instead:** a pre-registered power analysis produces the sample size ([B-7b](../10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark)). The `+10 point` effect is retained as an *input* to that calculation, not as a substitute for it.

### 3.3 G2-H6 — universal `casefold(path) + NFC(path)` NOT accepted

**Wrong on real systems.** Filesystem equality is a property of the filesystem and its configuration, not of the operating system and not of the string: Linux is case-sensitive, macOS APFS is case-insensitive by default *but can be formatted case-sensitive*, NTFS is case-insensitive by default *but supports per-directory case sensitivity*. Universal casefolded-NFC normalisation **merges two genuinely distinct files on a case-sensitive volume** — a data-integrity failure worse than the one it prevents.

**Accepted instead** ([D §3.3](../03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics)): embedded Fehrest UUID resolved **first**; path comparison demoted to a locator optimisation via a **platform- and volume-aware key, probed rather than assumed**, defaulting to the conservative case- and normalisation-sensitive comparison; original user-visible spelling preserved; path never hashed into an identity.

### 3.4 G2-H1 — a single total order over eight states NOT accepted

The eight R1 states are **not one vocabulary** and cannot be totally ordered without a category error: `EXTRACTED`/`INFERRED` describe origin, `USER_CONFIRMED` describes verification, `SUPERSEDED` describes lifecycle, `CONFLICTED`/`UNRESOLVED` describe resolution.

**Accepted instead** ([F §3.3](../05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model)): four **orthogonal** fields — `basis`, `verification`, `lifecycle`, `resolution`. Ordering an origin against a verification level is not fixed by ordering it more carefully; it is fixed by not doing it.

---

## 4. Delta table

| ID | G2 | GPT verdict | Accepted substance | Rejected / modified | Canonical correction | Files changed | Downstream impact | Status |
|---|---|---|---|---|---|---|---|---|
| **R2-01** | G2-C1 | VALID | Exact recomputation of every historical package is unsatisfiable once sources mutate, T2 compacts, or schemas evolve | Storing full package bodies **not** adopted as the remedy ([Q-15](../16-OPEN-QUESTIONS.md#q-15--should-context-packages-store-bodies-not-just-manifests)) | [I-14](../01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) property 1 split: **permanent composition auditability** via a T1 served-item manifest, and **conditional content reconstructability**. Replay returns `IDENTICAL` / `DIVERGED` / `UNRECONSTRUCTABLE` with a reason | [B I-14](../01-ARCHITECTURE-CONSTITUTION.md), [D §5.2](../03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief), [D §8](../03-CANONICAL-DATA-MODEL.md#8-what-is-canonical-definitively), [H §1](../07-CONTEXT-COMPILER-SPEC.md#1-contract), [H §3.2–3.3](../07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1), [G §6](../06-AGENT-MODEL.md#6-audit-and-replay), [K B-6](../10-BENCHMARK-PLAN.md#b-6--context-compiler), [P Phase 5](../15-IMPLEMENTATION-PHASES.md#phase-5--context-compiler-and-agent-gateway) | Makes T-3 implementable; adds per-item storage cost ([F-22](../17-FAILURE-CONDITIONS.md#f-22--the-served-item-manifest-is-unaffordable)) | ✅ Applied |
| **R2-02** | G2-C2 | VALID | T-3 claimed verification against "what the session was shown"; **no such durable record existed**. It was a Boundary control with no mechanism | — | T-3 rewritten against the R2-01 manifest. Required negative property added: **in-grant but not-served ≠ observed**. `test_provenance_cannot_be_spoofed` must cover that case | [C T-3](../02-THREAT-MODEL.md#t-3--forged-provenance), [C §6](../02-THREAT-MODEL.md#6-controls-summary-by-mechanism), [C §8](../02-THREAT-MODEL.md#8-falsification-criteria-for-this-threat-model), [F §3.1](../05-MEMORY-MODEL.md#31-field-semantics-that-carry-weight), [L §6.4](../11-SECURITY-VERIFICATION-PLAN.md#64-c-poison--memory-poisoning), [K S-8](../10-BENCHMARK-PLAN.md#4-security-benchmarks), [P Phase 4](../15-IMPLEMENTATION-PHASES.md#phase-4--temporal-memory) | A decorative boundary becomes a real one | ✅ Applied |
| **R2-03** | G2-C3 | VALID | The compiler was the only path preserving trust level, provenance, temporal state and supersession — leaving six other agent-facing read tools unlabelled | Direct reads are **not** required to behave like `context.compile`; historical exploration stays permitted | **One Rust-core response envelope for every agent-facing read.** Direct reads must be **temporally honest** (a superseded item says so and names its replacement). `test_no_unlabelled_content_path` over the full surface. B-7 gains a **Fehrest-as-shipped** arm | [B I-14](../01-ARCHITECTURE-CONSTITUTION.md), [B R-9](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules), [G §3](../06-AGENT-MODEL.md#3-tools), [G §4.1–4.2](../06-AGENT-MODEL.md#41-one-envelope-every-read-path), [G §8](../06-AGENT-MODEL.md#8-falsification-criteria), [C §6](../02-THREAT-MODEL.md#6-controls-summary-by-mechanism), [K B-7](../10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment), [L §2.1](../11-SECURITY-VERIFICATION-PLAN.md#21-custom-semgrep-rules--the-invariants-that-decay-silently) | The product is now measured in the configuration users get | ✅ Applied |
| **R2-04** | G2-H1 + G2-L1 | VALID | The epistemic vocabulary mixed origin, verification, lifecycle and resolution; and raw LLM confidence was the final tie-break that forced a winner | **Single total ordering rejected** (§3.4) | Four orthogonal fields (`basis`, `verification`, `lifecycle`, `resolution`), per-axis transitions, extractor labels mapping onto two axes. **`confidence` removed from resolution entirely**; renamed `confidence_diagnostic`. One normative resolver ladder terminating in `CONTRADICTION` | [B I-12](../01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended), [B §3.2](../01-ARCHITECTURE-CONSTITUTION.md#32-why-i-12-was-rewritten), [F §3–§3.3](../05-MEMORY-MODEL.md#3-the-memory-record), [F §4.2](../05-MEMORY-MODEL.md#42-deterministic-resolution), [F §6](../05-MEMORY-MODEL.md#6-supersession), [C T-2](../02-THREAT-MODEL.md#t-2--memory-poisoning), [ADR-0008](../09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution), [L §2.1](../11-SECURITY-VERIFICATION-PLAN.md#21-custom-semgrep-rules--the-invariants-that-decay-silently), [L §5](../11-SECURITY-VERIFICATION-PLAN.md#5-property-testing), [H §6](../07-CONTEXT-COMPILER-SPEC.md#6-optional-ai-stages) | Resolution deterministic but no longer total — `CONTRADICTION` where nothing separates ([F-20](../17-FAILURE-CONDITIONS.md#f-20--the-four-axis-memory-model-produces-unusable-abstention-rates)) | ✅ Applied |
| **R2-05** | G2-H2 | VALID | Scope was an artificial ordered lattice over `vault·project·object·type·time` | — | Orthogonal dimensions. **`time` removed** — it is temporal validity. **`type` reclassified** as a selector. Dimension-wise match and intersection; specificity a **partial** order; incomparable selectors yield `CONTRADICTION`. Vault-global cannot silently override project-local, and requires explicit user authority | [F §3.4](../05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice), [F §4.2](../05-MEMORY-MODEL.md#42-deterministic-resolution), [F §7](../05-MEMORY-MODEL.md#7-retrieval), [G §2.3](../06-AGENT-MODEL.md#23-scopes), [C T-2](../02-THREAT-MODEL.md#t-2--memory-poisoning), [L §5](../11-SECURITY-VERIFICATION-PLAN.md#5-property-testing) | Closes cross-project poisoning by construction | ✅ Applied |
| **R2-06** | G2-H3 | VALID | Unconfirmed candidates had no specified state — either silent authority or total invisibility was reachable | The "< 5 confirmations/day" assumption **not canonised** | `lifecycle: PENDING` specified as **non-authoritative but not hidden**: appears only in `pending_advisory`, may justify ASK/abstention, may never grant, revoke, supersede or become policy ([R-12](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)) | [F §5.4–5.5](../05-MEMORY-MODEL.md#55-pending-confirmation-semantics), [F §9](../05-MEMORY-MODEL.md#9-falsification-criteria), [H §3](../07-CONTEXT-COMPILER-SPEC.md#3-output), [H §4](../07-CONTEXT-COMPILER-SPEC.md#4-pipeline), [O §10](../14-PERFORMANCE-BUDGETS.md#10-human-factor-budgets), [F-17](../17-FAILURE-CONDITIONS.md#f-17--confirmation-fatigue), [L §2.1](../11-SECURITY-VERIFICATION-PLAN.md#21-custom-semgrep-rules--the-invariants-that-decay-silently) | Confirmation burden measured before automation widens | ✅ Applied |
| **R2-07** | G2-H4 + Spark study | VALID | Incremental-vs-rebuild equivalence was asserted with no mechanism able to test it | **Spark itself rejected** — no JVM, runtime, DAG scheduler, Pregel or distributed execution | Derivation registry: `artifact` / `inputs` / `deriver_id` / `deriver_version`. **Lineage as data, not a workflow engine.** Makes `test_incremental_equals_full` and `test_invalidation_completeness` expressible | [E §10](../04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data), [B R-10](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules), [ADR-0016](../09-TECHNOLOGY-DECISIONS.md#adr-0016--derivation-lineage-and-projection-checkpoints), [SRC-100](../research/FEHREST_SOURCE_REGISTRY.md#414-apache-spark--study--defer), [I §5](../08-DONOR-MATRIX.md#5-study--mechanisms-not-vibes), [P Phase 2](../15-IMPLEMENTATION-PHASES.md#phase-2--derived-index-and-lexical-retrieval), [F-19](../17-FAILURE-CONDITIONS.md#f-19--incremental-maintenance-does-not-converge-to-a-rebuild) | Two new load-bearing test properties | ✅ Applied |
| **R2-08** | G2-H5 | **PARTIAL** | Checkpointing was named in a budget and never specified | **"Replay necessarily takes minutes" rejected** — unmeasured. **No degraded-path target invented** | Checkpoints are **derived, non-authoritative, disposable, rebuildable**, carrying log high-water mark, schema version, deriver version, digest. Invalid → discard → older valid → full replay. **Healthy-start and degraded-recovery budgets separated; the degraded one is deliberately unset pending measurement** | [E §11](../04-DERIVED-DATA-MODEL.md#11-projection-checkpoints), [ADR-0016](../09-TECHNOLOGY-DECISIONS.md#adr-0016--derivation-lineage-and-projection-checkpoints), [N §3A.8](../13-RECOVERY-MODEL.md#3a8-checkpoint-loss), [O §9](../14-PERFORMANCE-BUDGETS.md#9-growth-over-time), [O §12](../14-PERFORMANCE-BUDGETS.md#12-what-would-force-redesign) | A named-but-unspecified mechanism becomes specified | ✅ Applied |
| **R2-09** | G2-H6 | VALID | "Case-insensitive filesystems need explicit handling" was a gap, not a specification | **Universal `casefold + NFC` rejected** (§3.3) | Identity-first reconciliation; platform- and volume-aware path key, probed not assumed; original spelling preserved; duplicate IDs surfaced as conflicts; **path never hashed as identity**. Full per-platform test matrix | [D §3.3](../03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics), [D §3.2](../03-CANONICAL-DATA-MODEL.md#32-identity-across-filesystem-operations), [B I-15](../01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities), [L §5](../11-SECURITY-VERIFICATION-PLAN.md#5-property-testing), [P Phase 2](../15-IMPLEMENTATION-PHASES.md#phase-2--derived-index-and-lexical-retrieval) | Prevents silent identity splits on the founder's own platform | ✅ Applied |
| **R2-10** | G2-H7 | **PARTIAL** | The defining benchmark cannot wait until Phase 6; its sample size needs a power analysis | **`n ≈ 300+` rejected as universal** (§3.2) | Two stages: **[B-7a](../10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot)** early headless pilot at the new **[Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice)**, and **[B-7b](../10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark)** pre-registered powered confirmatory study. **Only B-7b may falsify the thesis; a pilot may say `INCONCLUSIVE`** | [K B-7](../10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment), [K §3.1](../10-BENCHMARK-PLAN.md#31-the-baseline-ladder), [K §6](../10-BENCHMARK-PLAN.md#6-gating), [K §7](../10-BENCHMARK-PLAN.md#7-known-limitations), [P §1](../15-IMPLEMENTATION-PHASES.md#1-structure), [P Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice), [P Phase 6](../15-IMPLEMENTATION-PHASES.md#phase-6--vertical-proof), [F-1](../17-FAILURE-CONDITIONS.md#f-1--compiled-context-does-not-beat-a-competent-agent-with-plain-file-tools), [A §11](../00-PRODUCT-THESIS.md#11-what-would-change-this-thesis) | **The largest structural change in R2**: the thesis is tested before the architecture is built | ✅ Applied |
| **R2-11** | G2-M1 | VALID | Spilled locators referenced by canonical audit events had no declared durability; a supported `--reset-derived` could destroy claimed audit substance | Kept minimal — three classes, one constraint, three outcomes | Durability classes `CANONICAL_PERMANENT` / `CANONICAL_COMPACTABLE` / `DERIVED_DISPOSABLE`; **a canonical event may never reference a disposable locator**; resolution returns `PRESENT` / `COMPACTED` / `MISSING` | [D §5.5](../03-CANONICAL-DATA-MODEL.md#55-spilled-locators-have-a-declared-durability-class), [G §3.2](../06-AGENT-MODEL.md#32-execution-pipeline), [L §2.1](../11-SECURITY-VERIFICATION-PLAN.md#21-custom-semgrep-rules--the-invariants-that-decay-silently), [P Phase 5](../15-IMPLEMENTATION-PHASES.md#phase-5--context-compiler-and-agent-gateway) | Extends [R-2](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) from reads to references | ✅ Applied |
| **R2-12** | G2-M2 | **NEEDS_EVIDENCE** | The 500/day assumption is not grounded | **`10K–100K/day` NOT accepted as fact** (§3.1) | Both figures reclassified `UNVALIDATED PLANNING ASSUMPTION`. **[B-0](../10-BENCHMARK-PLAN.md#b-0--event-volume-measurement)** added at Phase 0. **No event-tiering, retention, compaction or checkpoint-cadence parameter may be frozen before it reports** | [O §9](../14-PERFORMANCE-BUDGETS.md#9-growth-over-time), [O §8](../14-PERFORMANCE-BUDGETS.md#8-disk), [O §12](../14-PERFORMANCE-BUDGETS.md#12-what-would-force-redesign), [D §5.2](../03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief), [F §8](../05-MEMORY-MODEL.md#8-growth-and-forgetting), [K B-0](../10-BENCHMARK-PLAN.md#b-0--event-volume-measurement), [K B-10](../10-BENCHMARK-PLAN.md#b-10--scale-and-growth), [P Phase 0](../15-IMPLEMENTATION-PHASES.md#phase-0--foundation-validation), [Evidence Log](../research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2) | **Open pending measurement** | ⏳ Open by design |
| **R2-13** | G2-M3 | **PARTIAL** | Recovery insufficiently models hostile real-world filesystem and sync environments | **Specific OneDrive/iCloud behavioural claims rejected** as unverified | New [N §3A](../13-RECOVERY-MODEL.md#3a-hostile-filesystem-and-sync-environments): sharing violations with bounded retry, watcher storms escalating to reconciliation, cloud placeholders never indexed as empty, hard links, sync reverts preserved in provenance **without inventing intent**, conflict copies with duplicate UUIDs. **Cloud-sync support is an empirical gate — real OneDrive/Windows and iCloud/macOS before any claim** | [N §3A](../13-RECOVERY-MODEL.md#3a-hostile-filesystem-and-sync-environments), [N §6](../13-RECOVERY-MODEL.md#6-testing), [L §8](../11-SECURITY-VERIFICATION-PLAN.md#8-recovery-tests), [F-21](../17-FAILURE-CONDITIONS.md#f-21--cloud-sync-environments-prove-incompatible) | Models the environment the founder actually runs | ✅ Applied |
| **R2-14** | G2-M4 | VALID | FTS5 ranking determinism was an assumption, and a load-bearing digest sits on it | Remedy **deliberately not chosen** — benchmark first | **[B-12](../10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability)**: incremental-route vs fresh-route index over an identical logical corpus, comparing membership, ranking, scores, context selection, manifest and package digest | [K B-12](../10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability), [H §5](../07-CONTEXT-COMPILER-SPEC.md#5-determinism), [H §10](../07-CONTEXT-COMPILER-SPEC.md#10-falsification-criteria), [E §8](../04-DERIVED-DATA-MODEL.md#8-rebuild-semantics), [F-18](../17-FAILURE-CONDITIONS.md#f-18--fts5-ranking-is-not-stable-across-rebuild-histories), [H-6](../research/EVIDENCE_LOG.md#h-6--fts5-ranking-is-stable-across-rebuild-histories-added-f1-r2), [P Phase 2](../15-IMPLEMENTATION-PHASES.md#phase-2--derived-index-and-lexical-retrieval) | An unstated assumption becomes a named, early, empirical gate | ✅ Applied |
| **R2-15** | G2-M5 | VALID | Capability evaluation came **after** production integration, making F-3's removal branch payable only once its cost was sunk | — | **[B-13 GI-CAP](../10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment)** — throwaway static-graph experiment on code-heavy **and** Markdown-heavy corpora — runs at **[Phase 3A](../15-IMPLEMENTATION-PHASES.md#phase-3a--capability-experiment-throwaway)**, before any supervisor, IPC, packaging, Python lifecycle or incremental pipeline exists | [K B-13](../10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment), [K §6](../10-BENCHMARK-PLAN.md#6-gating), [P Phase 3](../15-IMPLEMENTATION-PHASES.md#phase-3--graph-sidecar), [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape), [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost), [Q-14](../16-OPEN-QUESTIONS.md#q-14--sidecar-distribution) | Makes an explicitly falsifiable hypothesis **affordable** to falsify. Status unchanged: capability = falsifiable hypothesis, Graphify = optional candidate | ✅ Applied |
| **R2-16** | G2-M6 | VALID | With AI off, unclassified prose defaulted to `fact` — an **auto-promote** type — silently granting authority in the constitutionally-supported configuration | — | **Uncertainty about type is uncertainty about influence.** Unclassified candidates become `memory_type: unclassified`, `lifecycle: PENDING`, and wait. Nothing is dropped. B-5 gains **type-assignment precision** as a safety metric | [F §5.1](../05-MEMORY-MODEL.md#51-which-stages-are-deterministic), [F §3.2](../05-MEMORY-MODEL.md#32-memory-types), [F §5.4](../05-MEMORY-MODEL.md#54-who-decides), [K B-5](../10-BENCHMARK-PLAN.md#b-5--memory-promotion-quality), [P Phase 4](../15-IMPLEMENTATION-PHASES.md#phase-4--temporal-memory), [H-8](../research/EVIDENCE_LOG.md#h-8--deterministic-rules-can-type-memory-candidates-well-enough-to-gate-promotion-added-f1-r2) | Closes a memory-poisoning path reachable without an attacker | ✅ Applied |
| **R2-17** | G2-L2 | **PARTIAL** | A permanent, ever-growing upcaster chain in the running binary is an unbounded maintenance and security surface | **Abandoning old-vault readability rejected** — it contradicts the product's governing promise | **[ADR-0015](../09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility) opened**, framing a study: bounded live window, separate versioned migration tooling, permanently published historical formats, mandatory pre-migration backup, migration epochs, auditable path to current form. **Policy deliberately not frozen on R2 evidence** | [ADR-0015](../09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility), [M §3](../12-MIGRATION-SCHEMA-EVOLUTION.md#3-event-and-memory-log-evolution), [M §4](../12-MIGRATION-SCHEMA-EVOLUTION.md#4-file-level-migration), [Q-17](../16-OPEN-QUESTIONS.md#q-17--long-term-schema-compatibility-policy) | Open, framed | ⏳ Open by design |
| **R2-18** | G2-L3 | **PARTIAL** | Editor weights encode an **unratified** persona and cannot be presented as fixed | **Weights not rewritten.** Rewriting them to match an unratified wedge, on an argument that may double-count fidelity, would move weights for a reason other than evidence | Weights marked `PROVISIONAL — CONTINGENT ON V1 WEDGE RATIFICATION`; the freezing rule still binds at evaluation. **The agent-editability question raised in full, both sides, as a founder decision due before Phase 3E** | [Editor Gate §6–6.1](../18-EDITOR-GATE.md#6-scoring), [Q-16](../16-OPEN-QUESTIONS.md#q-16--editor-gate-weights-and-agent-editability) | Editor architecture remains `OPEN / PROTOTYPE-GATED` | ✅ Applied |
| **R2-19** | G2-L1 | VALID | *(Merged into R2-04 — raw LLM confidence must not be truth authority)* | — | See R2-04 | — | — | ✅ Applied |

---

## 5. New phase order — headless proof first

```
Phase 0    Foundation validation           (+ B-0 event volume, no product code)
   │
   ▼
Phase T    HEADLESS RUST THESIS-PROOF      ← FIRST AUTHORIZED IMPLEMENTATION
           Rust CLI · Markdown files · UUID identity · SQLite · FTS5
           minimal temporal/supersession · explicit memory writes only
           minimal T1 events · served-item manifest
           deterministic bounded compiler · plain-agent + wiki baselines
           → B-7a reports SIGNAL / NO SIGNAL / INCONCLUSIVE
   │
   ▼
Phase 1–2  Canonical core, derived index   (broaden Phase T's surface)
Phase 3A   GI-CAP capability experiment    ← before any graph integration
Phase 3B   Graph integration               (only if 3A retains the capability)
Phase 3E   Editor bake-off                 (parallel, gated)
Phase 4–5  Memory, compiler, gateway
Phase 6    B-7b confirmatory powered study ← only this may falsify the thesis
Phase 7    Desktop application
```

**Explicitly excluded from Phase T**, unless one becomes strictly required to run the experiment and the requirement is written down first: desktop UI, editor, Graphify production sidecar, vectors, automatic memory promotion, T2/T3 compaction engine, cloud, sync, mobile, marketplace, plugins, Spark, DuckDB, TimesFM.

**Phase T is not a throwaway prototype.** It is a thin vertical cut through the production Core, built to production correctness standards for the surface it covers. Ponytail's question 2 — *does Fehrest already implement it?* — applies to Fehrest's own code before anyone else's.

---

## 6. Source registry updates

| id | Source | Class | Decision | Note |
|---|---|---|---|---|
| [SRC-100](../research/FEHREST_SOURCE_REGISTRY.md#414-apache-spark--study--defer) | Apache Spark | ARCHITECTURE_DONOR / SCALE_REFERENCE | **STUDY / DEFER** | **Adopt:** lineage-as-data; checkpoint as recomputation-depth truncation; bounded batch/backpressure lessons where justified. **Reject for v1:** Spark runtime, JVM, driver/executor, cluster, RDD/DataFrame, Structured Streaming, GraphX/Pregel, DAG scheduler. Deliberately unpinned — concepts read from published design docs, no code relationship |
| [SRC-101](../research/FEHREST_SOURCE_REGISTRY.md#82-andrej-karpathy--llm-wiki) | Andrej Karpathy — LLM Wiki | RESEARCH / ARCHITECTURE_DONOR / PRODUCT_REFERENCE | **FOUNDATIONAL_STUDY** | The lesson: **RAG reconstructs understanding per query; an LLM Wiki maintains an artifact that compounds.** Added as benchmark baseline 5. **No endorsement of Fehrest or Graphify is claimed or established.** Pin an exact gist revision before Phase T |
| [SRC-102](../research/FEHREST_SOURCE_REGISTRY.md#8a1-github-spec-kit) | github/spec-kit | DEVELOPMENT_GOVERNANCE_DONOR | **USE** — development only | `runtime_dependency: NO`. Pin at Phase 0 |
| [SRC-103](../research/FEHREST_SOURCE_REGISTRY.md#8a2-ponytail) | DietrichGebert/ponytail | DEVELOPMENT_AGENT_DISCIPLINE | **USE** — development only | `runtime_dependency: NO`. Pin and **verify license** at Phase 0 |

---

## 7. Closeout validation

| # | Check | Result |
|---|---|---|
| 1 | Rust recorded as ACCEPTED canonical Core language | ✅ [ADR-0010](../09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language), [Q-2](../16-OPEN-QUESTIONS.md#q-2--core-implementation-language-closed) |
| 2 | Desktop shell remains separately open | ✅ [ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) OPEN, explicitly not resolved by D-1 |
| 3 | Spec Kit is development governance, not runtime | ✅ [ADR-0014](../09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail), [R-11](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) |
| 4 | Ponytail is development discipline, not runtime | ✅ Same, plus the hard exclusion list |
| 5 | All agent-facing content paths require one trust/provenance envelope | ✅ [G §4.1](../06-AGENT-MODEL.md#41-one-envelope-every-read-path), [R-9](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules), `test_no_unlabelled_content_path` |
| 6 | Context-compiled events contain a durable served-item manifest | ✅ [H §3.2](../07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1), T1, never compacted |
| 7 | T-3 is implementable against that manifest | ✅ [C T-3](../02-THREAT-MODEL.md#t-3--forged-provenance), including the in-grant-but-not-served negative case |
| 8 | Exact historical content reconstructability no longer claimed after sources vanish | ✅ [I-14](../01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) property 2, `UNRECONSTRUCTABLE` outcome |
| 9 | Basis, verification, lifecycle, conflict not collapsed into one enum | ✅ [F §3.3](../05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model), `no-collapsed-memory-status` |
| 10 | Raw LLM confidence cannot force truth resolution | ✅ [F §4.2](../05-MEMORY-MODEL.md#42-deterministic-resolution), `no-confidence-in-resolution`, property test |
| 11 | Temporal validity not encoded as a scope kind | ✅ [F §3.4](../05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice), `time` removed |
| 12 | Vault-global memory cannot silently contaminate projects | ✅ Specificity partial order; explicit user authority required |
| 13 | Pending confirmation has explicit non-authoritative semantics | ✅ [F §5.5](../05-MEMORY-MODEL.md#55-pending-confirmation-semantics), [R-12](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) |
| 14 | AI-OFF cannot auto-promote unclassified prose | ✅ [F §5.1](../05-MEMORY-MODEL.md#51-which-stages-are-deterministic) |
| 15 | Derived artifacts have explicit derivation/version dependencies | ✅ [E §10](../04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data), [R-10](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) |
| 16 | Incremental-vs-full equivalence is an explicit test property | ✅ `test_incremental_equals_full`, `test_invalidation_completeness` |
| 17 | Checkpoints are derived and non-authoritative | ✅ [E §11](../04-DERIVED-DATA-MODEL.md#11-projection-checkpoints) |
| 18 | Filesystem identity handles Win/macOS/Linux without path-as-identity | ✅ [D §3.3](../03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics) |
| 19 | FTS5 rebuild/ranking stability is an explicit empirical gate | ✅ [B-12](../10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability), [F-18](../17-FAILURE-CONDITIONS.md#f-18--fts5-ranking-is-not-stable-across-rebuild-histories) |
| 20 | Event-volume assumptions marked unvalidated pending measurement | ✅ [B-0](../10-BENCHMARK-PLAN.md#b-0--event-volume-measurement), [Evidence Log](../research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2) |
| 21 | Graph capability validation precedes Graphify production integration | ✅ [Phase 3A](../15-IMPLEMENTATION-PHASES.md#phase-3a--capability-experiment-throwaway) before 3B |
| 22 | The defining benchmark moves substantially earlier | ✅ [B-7a](../10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) at [Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) |
| 23 | Sample size determined by power analysis, not arbitrary n | ✅ [B-7b](../10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark); `n≈300+` explicitly not adopted |
| 24 | Karpathy LLM Wiki included as source and baseline, no endorsement claimed | ✅ [SRC-101](../research/FEHREST_SOURCE_REGISTRY.md#82-andrej-karpathy--llm-wiki), [A §8.1](../00-PRODUCT-THESIS.md#81-the-maintained-wiki-baseline-and-what-it-demands-added-in-f1-r2) |
| 25 | No Spark runtime in v1 | ✅ [SRC-100](../research/FEHREST_SOURCE_REGISTRY.md#414-apache-spark--study--defer) reject list; concepts only |
| 26 | No UI/editor implementation started | ✅ Documentation only |
| 27 | No product code exists | ✅ Zero source files, schemas, migrations, tests or scaffolds |
| 28 | No push occurred | ✅ Local commits only |
| 29 | No merge occurred | ✅ Single branch `main`, linear |
| 30 | Internal Markdown links valid | ✅ Verified mechanically at closeout |

---

## 8. Unresolved after R2

| # | Item | Why open | Resolved by |
|---|---|---|---|
| U-1 | Editor architecture | Requires executable prototype evidence | Phase 3E |
| U-2 | Graph Intelligence runtime shape | Requires GI-CAP then GI-BENCH | B-13, B-11 |
| U-3 | Round-trip fidelity ceiling per candidate | Requires the gate's acceptance suite | Phase 3E |
| U-5 | Desktop shell ([ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell)) | Founder; **not** entailed by D-1 | Founder / Phase 3E |
| U-6 | License and publication timing | Commercial | Founder |
| U-7 | `AI OFF` positioning | Needs B-5 | Phase 4 |
| U-8 | Whether structured `payload` extraction is common enough | Needs B-4 | Phase 4 |
| **U-9** | **Real event and memory volume** ([R2-12](#4-delta-table)) | Neither the 500/day assumption nor the 10K–100K/day estimate is measured | **B-0, Phase 0** |
| **U-10** | **Confirmation burden tolerance** ([R2-06](#4-delta-table)) | "< 5/day" was never measured | B-5 dogfooding |
| **U-11** | **FTS5 ranking stability** ([R2-14](#4-delta-table)) | Never tested; a digest depends on it | B-12, Phase T / 2 |
| **U-12** | **Long-term schema compatibility policy** ([ADR-0015](../09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility)) | Both horns real; R2 evidence insufficient | After two real major migrations |
| **U-13** | **Editor gate weights** ([Q-16](../16-OPEN-QUESTIONS.md#q-16--editor-gate-weights-and-agent-editability)) | Contingent on wedge ratification | Founder, before Phase 3E |
| **U-14** | **Context package bodies vs manifests only** ([Q-15](../16-OPEN-QUESTIONS.md#q-15--should-context-packages-store-bodies-not-just-manifests)) | Needs storage/forensics analysis against measured volume | After B-0 |
| **Q-8** | **V1 target wedge** | `PROVISIONALLY_ACCEPTED_FOR_PLANNING` / `FOUNDER_RATIFICATION_REQUIRED` — **unchanged by R2** | Founder |

**Closed by R2:** U-4 (core implementation language) — founder decision D-1.

---

## 9. Final donor discovery reconciliation

> **The last planned broad donor-discovery round.** Its purpose was to close specific gaps revealed by G2 and by the Rust-first founder decision — not to survey the field. Full records: [registry §14](../research/FEHREST_SOURCE_REGISTRY.md#14-f1-r2-final-donor-discovery-addendum). New gates: [T — Future Capability Gates](../20-FUTURE-GATES.md).

### 9.1 New sources accepted into the registry

**24 entries, in five groups.** Every one is `STUDY`, `BENCHMARK`, `DEFER`, or a candidate pending a gate.

| Group | Sources | Gap closed |
|---|---|---|
| **Rust platform** | gitoxide (SRC-110) · notify-rs (SRC-111) · cap-std (SRC-112) · Cedar for Agents (SRC-113) · **official MCP Rust SDK (SRC-114)** · CommonMark + Rust parsers (SRC-115) · Tantivy trigger (SRC-116) | D-1 made the Core Rust; F1 had specified filesystem, Git, watching, protocol and Markdown behaviour **without naming a mechanism** for any of them |
| **Visual / editing** | Penpot (SRC-120) · AFFiNE/BlockSuite extended scope (SRC-121) · OctoBase & y-octo (SRC-122) | No visual-surface gate existed; AFFiNE's scope beyond the text editor was unrecorded |
| **Local-first / CRDT** | Loro (SRC-130) · Automerge (SRC-131) · Yrs/Yjs (SRC-132) · AppFlowy-Collab (SRC-133) · any-sync/Anytype (SRC-134) · iroh (SRC-135) | [ADR-0012](../09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent) named Yjs and Automerge only; a conditional decision needs a candidate **set**, not a default |
| **Temporal / lineage / provenance** | Jujutsu (SRC-140) · OpenLineage (SRC-141) · in-toto (SRC-142) · DoltLite (SRC-143) | No model for durable undo, conflict-as-state, extensible event facets, or attestable provenance |
| **Retrieval / graph / analytics / memory** | petgraph (SRC-150) · Oxigraph (SRC-151) · Salsa (SRC-152) · Hindsight (SRC-160) · MemOra (SRC-161) · EvoMemBench (SRC-162) · "Total Recall at What Cost?" (SRC-163) · Apache Superset (SRC-170) · JSON Canvas promoted (SRC-171) | External memory benchmarks, cost-aware evaluation, and a view-engine boundary were all absent |

### 9.2 Retained only as benchmark candidates

**Tantivy** (only if FTS5 fails a documented requirement) · **petgraph** (only if GI-CAP retains the graph capability) · **MemOra**, **EvoMemBench**, **Hindsight** (external memory evaluation) · **Loro / Automerge / y-octo / Yrs** (Collaboration/CRDT Gate) · **Penpot / BlockSuite Edgeless / tldraw / Excalidraw** (Visual/Canvas Engine Gate).

### 9.3 Explicitly deferred

**Superset** (until a measured analytics requirement) · **iroh** (until sync is authorized) · **Oxigraph** (export interoperability, not the internal model) · **Salsa** (the validated requirement is a four-field manifest, not a framework) · **DoltLite** · **OctoBase / y-octo** · **DuckDB** (unchanged — and specifically **not** admitted because analytics products use it).

### 9.4 Rejected

**None outright.** Two *proposed uses* were refused: **Salsa as a v1 runtime dependency**, and **Tantivy adopted for being Rust-native rather than because FTS5 failed**. Both refusals are Ponytail, not preference.

### 9.5 Pins still pending

**All 17 pinnable entries in registry §14 are `PIN_PENDING_EXTERNAL_VERIFICATION`.** No live upstream verification was performed for them in this session, and **no commit hash was guessed** — a fabricated pin passes a reviewer's eye and fails at the moment it matters. None may transition to `ADAPT` or `USE` before pinning.

Also unpinned by design: **SRC-100 (Spark)** — concepts read from published design documentation, so a pin would imply a code relationship that does not exist. Still needing a pin before use: **SRC-101 (Karpathy LLM Wiki)** before the baseline harness, and **SRC-102/103 (Spec Kit, Ponytail)** at Phase 0.

### 9.6 License and permission issues requiring later review

| Source | Issue |
|---|---|
| **any-sync / Anytype** (SRC-134) | **Per-repository licensing.** Do not infer that all `anyproto` code is permissive because some components are. Source-specific rights review before any reuse |
| **AFFiNE / BlockSuite** (SRC-121) | Split license — MIT outside `packages/backend` and `packages/common/native`. **Per-file provenance** before any vendoring |
| **AppFlowy-Collab** (SRC-133) | Exact license/provenance/permission review before any code import |
| **Ponytail** (SRC-103) | License unverified at time of writing; must be confirmed before adoption |
| **All of §14** | Licenses recorded as stated by each project and marked `UNVERIFIED_IN_THIS_SESSION` |

**Two names could not be identified:** `OpenPencil` and `Flint`, carried from the founder donor map. No repository, license or capability claim is asserted for either, and neither is a gate candidate until identified and verified.

### 9.7 Confirmations

| Statement | Status |
|---|---|
| **No donor was adopted as a runtime dependency solely due to this discovery round** | ✅ Zero. Every entry is STUDY, BENCHMARK, DEFER, or gate-pending |
| **Broad donor discovery is now FROZEN** | ✅ [Registry §14.9](../research/FEHREST_SOURCE_REGISTRY.md#149-research-freeze--now-binding) — new sources only through a documented gap trigger; research is question-driven, not collection-driven |
| **The Headless Rust Thesis-Proof remains the first future build** | ✅ [Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) unchanged. **No source in §14 moves into it** |
| **No product code was implemented** | ✅ |
| **Nothing was pushed** | ✅ |
| **Nothing was merged** | ✅ |

### 9.8 What this round did NOT change

The registry is **evidence, not the implementation plan**. Adding 24 sources changed no invariant, no ADR outcome, no phase, and no v1 scope commitment. Every future adoption still passes Spec Kit → Ponytail → rights/provenance → benchmark/security → implementation ([S](../19-ENGINEERING-METHOD.md)).

**The risk this section exists to name:** a long candidate list reads as thoroughness and functions as deferred decision-making. Three new gates ([T](../20-FUTURE-GATES.md)) exist so that each cluster of candidates is attached to a question with a failure condition — including *"this capability should not exist"* — rather than accumulating plausibility until someone mistakes presence for a decision.

---

## 10. Files

**Added (2):**

```
docs/19-ENGINEERING-METHOD.md            # Spec Kit + Ponytail governance (D-2, D-3)
docs/reviews/F1-R2-RECONCILIATION.md     # this document
```

**Modified (20):**

```
README.md                                # status, R2 delta, Rust, phase order
docs/00-PRODUCT-THESIS.md                # wiki baseline (section 8.1), Rust, I-16/I-17 in scope
docs/01-ARCHITECTURE-CONSTITUTION.md     # I-12 re-amended, I-14 split + envelope,
                                         #   I-15 path semantics, I-16/I-17 added, R-9..R-12
docs/02-THREAT-MODEL.md                  # T-3 rewritten, T-2/T-5 updated, controls, criteria
docs/03-CANONICAL-DATA-MODEL.md          # section 3.3 filesystem identity, manifest in T1,
                                         #   section 5.5 locator durability, tiering unfrozen
docs/04-DERIVED-DATA-MODEL.md            # section 10 lineage, section 11 checkpoints, FTS5 gate
docs/05-MEMORY-MODEL.md                  # four axes, orthogonal scope, resolver ladder,
                                         #   PENDING semantics, AI-OFF default
docs/06-AGENT-MODEL.md                   # one envelope everywhere, scope dimensions,
                                         #   locator classes, replay outcomes
docs/07-CONTEXT-COMPILER-SPEC.md         # manifest, replay outcomes, pending_advisory, FTS5
docs/08-DONOR-MATRIX.md                  # Spark, Karpathy, baselines, dependency shape
docs/09-TECHNOLOGY-DECISIONS.md          # ADR-0010 ACCEPTED, 0011 note, 0003 sequencing,
                                         #   0008 amended, ADR-0014/0015/0016 added
docs/10-BENCHMARK-PLAN.md                # baseline ladder, B-7a/B-7b, B-0, B-12, B-13,
                                         #   B-5 safety metric, S-8/S-9, gating
docs/11-SECURITY-VERIFICATION-PLAN.md    # 7 new Semgrep rules, property tests, corpora, tests
docs/12-MIGRATION-SCHEMA-EVOLUTION.md    # upcaster-chain permanence reopened -> ADR-0015
docs/13-RECOVERY-MODEL.md                # section 3A hostile filesystem/sync, checkpoint loss
docs/14-PERFORMANCE-BUDGETS.md           # volume unvalidated, split startup budgets,
                                         #   confirmation target de-canonised
docs/15-IMPLEMENTATION-PHASES.md         # Phase T added, Phase 3A/3B split, Rust, method loop
docs/16-OPEN-QUESTIONS.md                # Q-2 closed, Q-3 clarified, Q-15/16/17, weaknesses
docs/17-FAILURE-CONDITIONS.md            # F-1 staged, F-3 trigger, F-17 note, F-18..F-22
docs/18-EDITOR-GATE.md                   # weights provisional, section 6.1 agent editability
docs/VERDICT.md                          # R2 verdict
docs/research/EVIDENCE_LOG.md            # H-6..H-9, unmeasured-quantities table
docs/research/FEHREST_SOURCE_REGISTRY.md # SRC-100..103, new classes, admissions, gaps
```

---

## 11. Confirmation

- **No product code was implemented.** No source file, module, schema, migration, test or scaffold exists. `cargo new` was not run. Spec Kit was not initialized. Ponytail was not installed. Graphify was not installed or ported. The editor bake-off was not run. No Tauri, React, SQLite schema, benchmark harness or headless proof was built.
- **No GLM-5.3 security review was performed here.** That is the gate after GPT-5.6 Sol's R2 delta review.
- **Nothing was pushed. Nothing was merged.** Local commits only, on `main`, `origin` pointing at the canonical repository.
- **Implementation remains unauthorized.**
- **The Code Provenance Ledger remains empty**, correctly.

---

## 12. Verdict

# `F1_R2_RECONCILED_READY_FOR_GPT_DELTA_REVIEW`

All 13 VALID findings applied in full. All 5 PARTIAL findings applied in their valid portion, with the rejected portion recorded and argued. The 1 NEEDS_EVIDENCE finding is left open with a measurement task and an explicit refusal to adopt either competing unmeasured number.

**The verdict is not `F1_R2_BLOCKED_BY_UNRESOLVED_EVIDENCE`:** every open item has a named benchmark and a phase, and none blocks review. Notably, the two largest open items — event volume and FTS5 stability — are now *scheduled measurements* rather than *unstated assumptions*, which is a strictly better position than the one G2 reviewed.

**It is not `F1_R2_MAJOR_REDESIGN_REQUIRED`:** the four-layer architecture, the constitutional invariants, the threat model's plane separation, bitemporal memory, and the falsification experiment all survive. What changed is that several mechanisms which were *asserted* are now *specified* (the manifest, checkpoints, lineage, filesystem identity, pending semantics), several vocabularies which were *conflated* are now *separated* (the four memory axes, scope dimensions), and the experiment that decides the product now runs before the architecture that depends on it.

**The pattern worth naming for the next reviewer.** F1's characteristic error was treating **absence of signal as evidence of absence**. F1-R1 corrected two instances. **F1-R2's corrections cluster around a different error: treating an unmeasured number, or an untested engine property, as though it were a finding** — 500 events/day, "< 5 confirmations/day", FTS5 ranking stability, incremental-equals-rebuild. Each had propagated into decisions without ever appearing in the Evidence Log with a status label. The [unmeasured-quantities table](../research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2) exists to make that class of error visible in future rounds.

**Next gate: GPT-5.6 Sol R2 delta review. Do NOT proceed to GLM-5.3.**
