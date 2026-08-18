# Q. Open Questions and Founder Decisions

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Unresolved decisions, stated openly. Hiding these would make the plan look more finished and be less useful.

Each question records: what is unresolved, why I did not decide it, what depends on it, and my recommendation where I have one.

---

> **Founder decisions recorded in F1-R2:** **D-1** core language — Rust ([Q-2](#q-2--core-implementation-language-closed), [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language)). **D-2** Spec Kit as the specification-driven workflow, and **D-3** Ponytail as the implementation-minimisation discipline — both **development governance, never runtime** ([ADR-0014](09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail), [S](19-ENGINEERING-METHOD.md)).

## Blocking — must be answered before Phase 0 exits

### Q-1 — Repository identity: CLOSED

> **RESOLVED IN F1-R1 ([R1-01](reviews/F1-R1-RECONCILIATION.md)).** F1 recorded this as open because it concluded `TheHalfMoon/Fehrest` did not exist. That conclusion was a **category error** — a 404 from an unaffiliated token against a private repository is indistinguishable from a 404 against a nonexistent one ([E-0](research/EVIDENCE_LOG.md#e-0--canonical-repository-state)).

**CLOSED:** the canonical repository is **`TheHalfMoon/Fehrest`** — private, default branch `main`, size 0, no implementation.

**`wepld/Fehrest` is NOT canonical**, is not a fallback, and receives no planning work.

**Environment note:** this session authenticates as `wepld` and cannot read `TheHalfMoon/Fehrest`. That is an access limitation of the available credential, recorded as such, and is not evidence about the repository.

**What remains open — and must not be conflated with identity:**

| # | Question | Nature |
|---|---|---|
| Q-1a | Open-source license choice | Legal. Donor obligations (Apache-2.0 from Graphify, MIT from others) are compatible with either MIT or Apache-2.0 for Fehrest; a copyleft choice would change the donor analysis |
| Q-1b | Public/private release timing | Commercial |
| Q-1c | Publication strategy | Commercial |

**No longer blocks anything.** The planning package is committed to a local repository whose `origin` now points at `TheHalfMoon/Fehrest`. **Nothing has been pushed**, pending explicit authorization.

### Q-2 — Core implementation language: CLOSED

> **RESOLVED IN F1-R2 — founder decision D-1.** [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) moves from `OPEN` to `ACCEPTED`.

**CLOSED: Rust is the canonical implementation language for Fehrest Core.**

Rust owns all correctness- and security-sensitive product logic — canonical domain model, identity, filesystem reconciliation, write and recovery semantics, storage, migrations, FTS, events and audit, temporal memory, deterministic resolution, retrieval, context compilation, provenance, authorization, agent gateway, MCP server, CLI, recovery, and every security-sensitive boundary.

TypeScript/React may be used for presentation. **No business-critical state semantic may be duplicated in TypeScript.** Python is permitted only behind an explicit optional process boundary, and **canonical Fehrest operation must not require it**.

Made testable by two new invariants: [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) (operable without the UI) and [I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python) (usable without Python).

**Note on how this was closed.** R1 recorded a weak recommendation of Rust and explicitly refused to close on it, because the choice turned on a founder priority. **The founder has now decided it.** It is recorded as a founder decision, not as an architect's inference finally granted permission.

**No longer blocks anything.**

### Q-3 — Desktop shell

**Status.** [ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) is **OPEN — and deliberately not resolved by D-1.** Weak recommendation: Tauri 2, chosen for its capability system as a real boundary (B1), not for bundle size.

**Why D-1 does not settle it.** Tauri is written in Rust and pairs naturally with a Rust core. **That adjacency is exactly why the inference must be refused:** "our core is Rust, therefore our shell is Tauri" is an association, not an argument, and the brief already lists Tauri as "STUDY → likely USE." Inheriting "likely" as a decision is precisely the unearned assumption this package exists to prevent.

**Not on the critical path**, and [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) guarantees it can never become one.

---

## Product-shaping — answer before the phase that depends on them

### Q-4 — Is `AI OFF` a first-class product or a compliance mode?

**The question.** The constitution requires core function without a model ([I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api)). But if deterministic promotion captures much less durable memory than model-assisted promotion ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)), `AI OFF` gives a working but materially thinner product.

**Why it matters.** It determines whether Fehrest is "a memory OS that works offline" or "a memory OS that needs a model, with an offline fallback." Those are different products with different users.

**Measured by.** [B-5](10-BENCHMARK-PLAN.md) at Phase 4.

**Founder decision.** If rules-only recall lands at, say, 50% of model-assisted — is that acceptable as the floor, or does it trigger investment in better deterministic extraction?

### Q-5 — How intrusive may Fehrest be with user files?

**The question.** [ADR-0004](09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque) writes a UUID into frontmatter — Fehrest modifying files the user considers theirs. Mitigated by lazy allocation, but it remains a real intrusion.

**Options.** (a) Frontmatter identity, lazily allocated (recommended — identity travels with the file, survives moves between machines and tools). (b) External path↔id map (no file modification, but identity breaks on external rename and does not travel). (c) User choice at vault creation (most flexible, two code paths forever).

**Recommendation:** (a), with (b) available for users who refuse. **Founder call**, because it is a product-values question about whose files these are.

### Q-6 — What if structured `payload` extraction is rare?

**The question.** Deterministic bitemporal resolution needs `subject`/`predicate` triples. If real memories are mostly unstructured prose, resolution covers a small fraction of them.

**Measured by.** [B-4](10-BENCHMARK-PLAN.md) at Phase 4. Threshold: 30%.

**If below threshold.** Either invest in better structured extraction, or accept prose-first memory with weaker guarantees — which would materially weaken the product's central differentiator ([ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) reversal).

**Related.** `confidence` as a numeric field is a known weakness — LLM-produced confidence is uncalibrated. Fehrest currently uses it only as a last-resort tiebreak ([F §3.1](05-MEMORY-MODEL.md#31-field-semantics-that-carry-weight)). Should it exist at all, or be replaced by an ordinal evidence-strength label?

### Q-7 — Is the graph worth 300 MB?

**The question.** The graph capability costs ~200–300 MB of installer ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)), a second process, a Python dependency tree, and 28 grammars of parser attack surface ([T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities)).

**Measured by.** [B-3](10-BENCHMARK-PLAN.md) ablation at Phase 3.

**Founder decision if the gain is small.** Drop it entirely (simpler, smaller, safer), restrict it to code-only vaults, or keep it as an optional install for users who want it. My recommendation is the optional-install path regardless, since it makes the decision reversible without a rebuild.

### Q-8 — V1 target wedge: PROVISIONALLY ACCEPTED FOR PLANNING

```
V1 TARGET WEDGE:
PROVISIONALLY_ACCEPTED_FOR_PLANNING
FOUNDER_RATIFICATION_REQUIRED
```

> **STATUS CORRECTED PRE-G2.** An earlier revision recorded this as "RESOLVED (candidate)," which read as closer to settled than it is. It is a **planning assumption only**. **This question remains OPEN.**

**Current planning candidate — NOT founder-approved:**

> Fehrest v1 targets **power users, developers, researchers and AI-native knowledge workers who regularly use multiple agents** and need durable local project memory across tools, sessions and model providers.

Such a user plausibly runs several of: Claude, Codex, Gemini, GLM, Cursor, local models, MCP tools. **Fehrest would make memory portable across them** — the defining requirement, and one no incumbent serves.

**Why it is adopted provisionally.** Architecture work needs a coherent target to reason against; leaving the persona blank was a genuine F1 gap. Adopting it as a stated assumption lets design proceed while keeping the decision visibly unmade.

**Architecture consequences that depend on ratification** ([A §4](00-PRODUCT-THESIS.md#4-the-v1-user-wedge)): MCP gateway is v1 rather than deferred; CLI-first through Phase 6; Graph Intelligence stays in v1; local-first is treated as a feature rather than a constraint; rich block editing informs but does not decide the [Editor Gate](18-EDITOR-GATE.md).

**Strongest alternative considered:** general knowledge workers (Obsidian-adjacent). Set aside for v1 because it would make the editor the product, demote the agent gateway, and force direct feature competition with mature incumbents on their strongest axis — while leaving the actual thesis untested. It remains the natural **second** market, and remains a live alternative until ratification.

**What ratification requires.** An explicit founder statement approving (or replacing) the wording above. Until then, no document may describe this wedge as approved, decided, or resolved, and the four architecture consequences above remain contingent.

---

## Architectural — deferred but scheduled

### Q-9 — Event log durability format
JSONL is chosen for inspectability ([ADR-0001](09-TECHNOLOGY-DECISIONS.md#adr-0001--canonical-state-is-open-files-plus-an-append-only-event-log)). At ~1 GB/year for a large vault ([O §8](14-PERFORMANCE-BUDGETS.md)) this may miss budgets. [I-5-as-amended](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) already permits a specified binary format with a lossless exporter. **Decide at Phase 6 with real growth data**, not now.

### Q-10 — Should the event log be versionable in git?
`.fehrest/` is git-ignored by default. Users may want event history versioned — but git merge conflicts in an append-only hash-chained log are painful and could break chain verification. Needs a design if requested.

### Q-11 — Multi-vault
One vault at a time is assumed throughout. Multiple vaults raise cross-vault memory scope, identity collision on copied vaults ([N §3.17](13-RECOVERY-MODEL.md#317-vault-moved-or-copied)), and agent grants spanning vaults. Post-v1, but the scope model should not foreclose it.

### Q-12 — At-rest encryption
Deferred; key custody is the unsolved part, not encryption. Note that it would **not** solve [T-19](02-THREAT-MODEL.md#t-19--local-process-reads-the-vault) (co-resident processes) while Fehrest is running with the vault unlocked.

### Q-13 — Telemetry
The constitution forbids *opaque* telemetry. Is *transparent, opt-in, locally-inspectable* telemetry acceptable? Without any, benchmark tuning depends entirely on the founder's own vault, which is a sample of one. Recommendation: local-only metrics the user can read, with export requiring explicit action — never automatic transmission.

### Q-14 — Sidecar distribution
Bundled Python runtime, or system Python, or a downloaded capability pack? Bundling is ~200–300 MB and needs its own update channel ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)); system Python is smaller but fragile across user environments. Decide at **Phase 3B** — and only if [GI-CAP](10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) retains the capability at Phase 3A. [I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python) bounds the whole question: whatever is chosen, its absence is a degradation.

---

## Added in F1-R2

### Q-15 — Should context packages store bodies, not just manifests?

**The question.** [H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1) adopts a permanent per-item manifest — identity, ordinal, source revision, two hashes — and **deliberately does not store item bodies**, on the grounds that storing bodies means storing the vault repeatedly.

**Why it is open.** The manifest proves *what* was served and detects divergence; it cannot *show* the text once the source revision is gone. For a forensic question — "what exactly did the agent read before it made this decision?" — a hash is an answer only if the content still exists.

**What would settle it.** A storage-and-forensics analysis against [B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement)'s measured volume: how often sources actually disappear, how much body storage would cost at real compilation rates, and whether a bounded window (bodies for N days, manifests forever) is the smallest correct design.

**Not adopted now, and specifically not adopted to close a review finding.** Body storage was considered in F1-R2 and rejected as a *default*: it is a large cost with an unmeasured benefit, and the manifest already closes the [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) gap that made the finding valid. **The manifest is the minimum required mechanism; bodies are an open optimisation.**

### Q-16 — Editor gate weights, and agent editability

**The question.** [Editor Gate §6](18-EDITOR-GATE.md#6-scoring) weights encode a persona's priorities, and that persona ([Q-8](#q-8--v1-target-wedge-provisionally-accepted-for-planning)) is unratified. Separately, **agent editability sits at 5%** — one third of "rich editing capability," a feature set the wedge table calls *not the wedge's core need*, in a product whose thesis is that agents are first-class users of the vault.

**Three possible resolutions**, all founder decisions, due before Phase 3E:
1. Ratify the wedge; keep the current weights.
2. Ratify the wedge; adopt a justified reweighting (most likely raising agent editability).
3. Replace the wedge; re-derive the weights from the new persona.

**Why R2 did not just fix it.** Rewriting weights during a governance reconciliation, to match an unratified persona, on an argument that may double-count properties already scored under fidelity, would mean weights moved for a reason other than evidence — which is exactly what the gate's freezing rule exists to stop. Marked provisional instead ([R2-18](reviews/F1-R2-RECONCILIATION.md)).

### Q-17 — Long-term schema compatibility policy

**The question.** [ADR-0015](09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility). Does the running binary read every schema it ever emitted, forever — an unbounded maintenance and security surface — or does old-vault reading move to separate versioned migration tooling?

**Both horns are real.** The first accumulates rarely-exercised parsing code inside the component whose corruption is unrecoverable. The second risks the promise that a user's decade-old vault stays readable.

**The property that must survive either answer:** a user-owned old vault must not become unreadable *merely because Fehrest evolved*.

**Decided when** the maintenance cost of an upcaster chain is an observation rather than a projection — after the first two real major migrations.

---

## Known weaknesses in this plan

Stated so reviewers do not have to find them:

1. **No implementation velocity data.** Phases have no durations because there is no basis for estimating them ([P §1](15-IMPLEMENTATION-PHASES.md#1-structure)).
1a. **Event and memory volume is unmeasured** ([R2-12](reviews/F1-R2-RECONCILIATION.md)). 500 events/day and 50 memories/day were assumptions that propagated into disk budgets, growth projections and event tiering as though grounded. A reviewer proposed 10K–100K/day; that is also unmeasured. **A 200× disagreement about a load-bearing input is itself the finding.** [B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) measures it at Phase 0.
1b. **Confirmation burden is unmeasured** ([R2-06](reviews/F1-R2-RECONCILIATION.md)). "< 5 confirmations per active day" was an assumption about human behaviour made without observing a human, then cited across three documents as a threshold.
1c. **FTS5 ranking stability across rebuild histories is unverified** ([R2-14](reviews/F1-R2-RECONCILIATION.md)), and a load-bearing deterministic digest sits directly on top of it. [B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability).
2. **C-PROJECT and C-TEMPORAL are self-authored.** The benchmarks that decide the thesis use corpora built by the people who designed the system. Mitigated by pre-written held-out tasks, a second external corpus, and blind grading — not eliminated ([K §7](10-BENCHMARK-PLAN.md#7-known-limitations)).
3. **All performance figures extrapolate from one machine and 776 files.** [H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count) is unproven.
4. **No third-party replication of any retrieval claim.** Every comparative number is vendor-reported or self-measured.
5. **The context compiler's budget priorities are reasoned, not measured.** The ordering in [H §4](07-CONTEXT-COMPILER-SPEC.md#4-pipeline) is an argument, not a finding, and should be re-derived from [B-7](10-BENCHMARK-PLAN.md) failure analysis.
6. **Parser attack surface is accepted, not solved.** 28 upstream grammars, contained by a sidecar boundary whose sufficiency is [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) — unproven.
7. **Windows confinement is the weakest platform and the most likely deployment** ([T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix)).
8. **`AI OFF` viability is unproven** ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)).
9. **No user research.** Nothing here is validated against a real user's behaviour, including the founder's.
10. **The editor decision trades a real product capability for maintainability.** [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated) is well-evidenced on upstream health and structurally argued, but it means v1 ships without block transclusion, inline comments beyond sidecars, or database blocks. A reviewer could reasonably argue this makes v1 uncompetitive with Obsidian, and that argument deserves a real answer rather than a dismissal.

---

## Questions for the adversarial reviewers

Where I most want to be attacked:

1. **Is the three-plane decomposition right, or is the Event Plane over-engineered for a single-user product?** T1/T2/T3 tiering adds real complexity.
2. **Is bitemporality worth its cost, or would valid-time-only serve?** I argue belief archaeology requires both ([F §4.1](05-MEMORY-MODEL.md#41-the-motivating-case-worked)); that argument could be wrong.
3. **Does deferring BlockSuite cripple the product?** I argue the round-trip gate is structurally unpassable and the upstream is unmaintained. The counter — that users will not accept a plain Markdown editor in 2026 — is a product argument I cannot settle with evidence.
4. **Is "no filesystem tool for agents" too strict?** ([ADR-0009](09-TECHNOLOGY-DECISIONS.md#adr-0009--agents-address-objects-by-id-never-by-path)) It removes an entire vulnerability class, but agents are trained on filesystem semantics.
5. **Is the plain-agent baseline in [B-7](10-BENCHMARK-PLAN.md) too harsh?** I do not think so — a memory system that cannot beat an agent with `grep` has not earned its complexity — but it is the criterion most likely to fail.
6. **Is Graphify worth the dependency?** Its measured strengths are code understanding and cost; its prose-QA advantage over dense RAG is unproven and, on the one benchmark reported, absent ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)).
7. **Have I under-weighted the risk that the founder's brief is right and I am wrong about BlockSuite?** The evidence on staleness is unambiguous, but "AFFiNE ships it daily inside their monorepo" is a real counter-argument to "unmaintained."

**Added after F1-R2:**

8. **Is the four-axis memory model over-engineered for a single-user product?** Four independently-valued fields on every memory is more machinery than one enum, and [R2-04](reviews/F1-R2-RECONCILIATION.md) argues the enum was invalid rather than merely awkward. If the axes are right but the *cost* is wrong, what collapses safely — and what does not?
9. **Is `pending_advisory` a safety feature or an attack surface?** [F §5.5](05-MEMORY-MODEL.md#55-pending-confirmation-semantics) argues that unconfirmed candidates must be visible-but-non-authoritative. An attacker who cannot poison memory may still be able to flood the advisory channel and steer an agent toward asking the wrong questions. Is "can only cause an agent to stop and ask" a strong enough bound?
10. **Does the served-item manifest survive contact with realistic volume?** [Q-15](#q-15--should-context-packages-store-bodies-not-just-manifests) and [F-22](17-FAILURE-CONDITIONS.md#f-22--the-served-item-manifest-is-unaffordable). The mechanism closes a real gap; its cost is projected against an event volume nobody has measured.
11. **Is Phase T genuinely the smallest thesis test, or is it already too big?** It carries identity, SQLite, FTS5, bitemporal resolution, the manifest and a bounded compiler. Each is argued as necessary; the ensemble is still a substantial build for something whose purpose is to fail cheaply if the thesis is wrong.
