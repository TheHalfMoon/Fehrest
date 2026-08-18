# Final Verdict

**Date:** 2026-08-17
**Author role:** Principal Architect
**Phase:** `F1-R2` reconciliation complete
**Next gate:** GPT-5.6 Sol **R2 delta** review → GLM-5.3 security/cyber review → architecture freeze → founder implementation authorization

---

## Verdict

# `F1_R2_RECONCILED_READY_FOR_GPT_DELTA_REVIEW`

**Read [the R2 delta](reviews/F1-R2-RECONCILIATION.md) first.** It carries the finding-by-finding table; this document is the summary.

**Justification.** The 19 Codex findings, as validated by GPT-5.6 Sol, are reconciled: **13 VALID applied in full, 5 PARTIAL applied in their valid portion with the rejected portion argued, 1 NEEDS_EVIDENCE left open with a measurement task.** Three founder decisions are recorded (D-1 Rust; D-2 Spec Kit; D-3 Ponytail), closing [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) and adding two invariants that make it testable.

**Four proposed remedies were rejected while their findings were accepted** ([R2 §3](reviews/F1-R2-RECONCILIATION.md#3-substance-not-accepted--recorded-explicitly)): `10K–100K events/day` as fact, `n ≈ 300+` as a universal sample size, universal `casefold+NFC` path normalisation, and a single total order over the eight epistemic states. Each is recorded with its reasoning, because the difference between "the finding was wrong" and "the fix was wrong" matters to the next reviewer.

The verdict is not `F1_R2_BLOCKED_BY_UNRESOLVED_EVIDENCE`: every open item has a named benchmark and a phase. The two largest — event volume and FTS5 ranking stability — are now *scheduled measurements* rather than *unstated assumptions*, which is strictly better than the position G2 reviewed. It is not `F1_R2_MAJOR_REDESIGN_REQUIRED`: the four-layer architecture, constitutional invariants, plane separation, bitemporal memory and the falsification experiment all survive.

**What changed structurally.** Several mechanisms that were *asserted* are now *specified* — the served-item manifest, checkpoints, derivation lineage, filesystem identity, pending semantics. Several vocabularies that were *conflated* are now *separated* — the four memory axes, the scope dimensions. And **the experiment that decides whether the product should exist now runs before the architecture that depends on it** ([Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice)).

---

<details>
<summary>Prior verdict — <code>F1_R1_RECONCILED_READY_FOR_GPT_REVIEW</code></summary>

> **Two governance corrections applied pre-G2** (after the R1 delta, before GPT-5.6 Sol review):
> 1. **V1 target wedge** is `PROVISIONALLY_ACCEPTED_FOR_PLANNING` / `FOUNDER_RATIFICATION_REQUIRED` — **not** a closed decision.
> 2. **Graph Intelligence** is a `CORE CURRENT PRODUCT HYPOTHESIS` that is `EXPLICITLY FALSIFIABLE` — [F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) now permits redesign **or removal** on benchmark evidence.
>
> No other architecture changes were made. See [reconciliation §10](reviews/F1-R1-RECONCILIATION.md#10-post-r1-governance-corrections-pre-g2).

All 20 validated R1 findings were reconciled. Three factually incorrect F1 claims were retracted **at source** rather than annotated around: the repository-does-not-exist finding, the "BlockSuite is unmaintained" characterisation, and the citation of fixed upstream Graphify bugs as current defects. Three decisions F1 closed prematurely were reopened with **executable gates** rather than argument. Repository identity was closed; the v1 wedge was adopted only as a provisional planning assumption pending founder ratification.

</details>

**What F1 got wrong, stated plainly.** Two errors shared one root cause — **treating an absence of signal as evidence of absence**. A 404 from an unaffiliated token was read as non-existence. A stale mirror was read as a dead project. Both are now corrected, and the registry has a risk schema that separates current from historical state specifically to prevent recurrence ([R1-20](reviews/F1-R1-RECONCILIATION.md)).

The third error was different in kind: F1 built the identity argument on upstream *bugs* rather than upstream *design*. The bugs were fixed; the argument would have collapsed under review. The reconstructed argument rests on properties no upstream fix can remove.

**What F1-R2 found, and it is a different error class.** R2's corrections cluster around **treating an unmeasured number, or an untested engine property, as though it were a finding**: 500 events/day, "< 5 confirmations per active day", FTS5 ranking stability across rebuild histories, and incremental-equals-rebuild convergence. Each had propagated into real decisions — disk budgets, event tiering, a failure condition, a load-bearing digest — **without ever appearing in the Evidence Log with a status label**, which is exactly the mechanism that was supposed to make such claims attackable. The [unmeasured-quantities table](research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2) now exists so the next round can find this class quickly.

Two further R2 findings were structural rather than evidential, and both are worth naming because they were *invisible while the system was only described*: [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) was a **Boundary control with no implementable mechanism**, and the evidence envelope covered **one of seven agent-facing read paths**. Neither shows up in prose. Both show up immediately when you ask what the test would be.

---

## Highest-risk assumptions

Ranked by damage if wrong.

| # | Assumption | Risk | Falsified by |
|---|---|---|---|
| 1 | **Compiled context beats a competent agent with plain file tools — and beats a maintained LLM Wiki** | **Thesis-fatal.** LongMemEval-V2's own reporting shows the best system beating an off-the-shelf coding agent by only **3.2 points** (72.5% vs 69.3%). The margin is genuinely thin, and R2 added a *harder* simple baseline | Indicated by [B-7a](10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) at **Phase T**; decided by [B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark) at Phase 6 |
| 1a | **Event and memory volume is anywhere near 500/day** | Every disk budget, growth projection and event-tiering decision rests on it. A reviewer proposed a figure **200× larger**; neither is measured | [B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) at Phase 0 |
| 1b | **FTS5 ranks a logically identical corpus identically regardless of write history** | A load-bearing deterministic digest sits directly on top of an untested engine property | [B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability) at Phase T / 2 |
| 2 | **Derived state is genuinely rebuildable** ([I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)) | Invalidates the most documents. Index corruption becomes data loss; `synchronous=NORMAL` becomes unsafe; every index decision becomes irreversible | [B-9](10-BENCHMARK-PLAN.md), CI from Phase 2 |
| 3 | **Deterministic promotion captures most durable memory value** ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)) | `AI OFF` degrades from "full product" to "read-only knowledge base" — a positioning failure, not an architecture one | [B-5](10-BENCHMARK-PLAN.md) at Phase 4 |
| 4 | **Extraction scales linearly in file count** ([H-2](research/EVIDENCE_LOG.md#h-2--extraction-scales-linearly-in-file-count)) | Every figure in [O](14-PERFORMANCE-BUDGETS.md) is extrapolated from **776 files on one machine**. Cross-file resolution is plausibly superlinear | [B-1](10-BENCHMARK-PLAN.md) at Phase 0 |
| 5 | **A sidecar boundary sufficiently contains 28 upstream grammars** ([H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path)) | Parser escape reachable from vault content. Fehrest controls none of these parsers | Fuzzing, Phase 3 onward |
| 6 | **Markdown plus sidecars suffices for real knowledge work** ([H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work)) | Editor decision reopens; a major migration follows. Deliberately the cheapest hypothesis to test | Dogfooding, Phase 7 |
| 7 | **Structured `payload` is extractable from real memories** | Below ~30%, deterministic bitemporal resolution covers too little to be the differentiator | [B-4](10-BENCHMARK-PLAN.md) at Phase 4 |
| 8 | **Users accept frontmatter identity injection** | Falls back to an external map with weaker rename survival | Dogfooding ([Q-5](16-OPEN-QUESTIONS.md)) |

---

## Strongest architectural choices

Where I expect the plan to survive attack.

1. **The evidence base is measured, not cited.** Cold/warm import times, extraction throughput, installed footprint, confidence distribution, and upstream health were all obtained by running and inspecting the actual code at pinned commits. Four decisions in the founder's brief were changed *because* of measurement ([registry §1](research/FEHREST_SOURCE_REGISTRY.md#1-dispositions-changed-in-f1-r1)).

2. **The editor gate is dissolved rather than solved.** Adopting no document model richer than the canonical format makes round-trip an identity function. Two independent arguments — structural impossibility (Markdown has no identity or overlap primitives) and upstream health (a 13-month-stale unreleased mirror) — reach the same decision. Converging independent arguments are much harder to defeat than either alone.

3. **Every invariant has a test.** [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default) through [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) name their enforcing mechanism and their detector. Two were amended precisely because they were unenforceable as written, with the arguments given rather than the changes made quietly.

4. **The security boundary is structural, and its limits are stated.** Capability grants are computed before retrieval and frozen; agents address objects by ID so path traversal is removed at the interface rather than defended at every call site. And the model explicitly distinguishes **boundary** controls from **defence-in-depth** ones, stating plainly that Fehrest bounds privilege, not persuasion. Overclaiming here is the standard failure of agent security documents.

5. **Disposability is load-bearing and it pays for itself.** [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) is what makes `synchronous=NORMAL` safe, makes index corruption an availability problem, makes "delete the derived directory" a support instruction, eliminates derived-schema migration entirely, and makes every index decision reversible. One invariant carrying five consequences is a sign the decomposition is right.

6. **Failure conditions are specific and run both ways.** Seventeen conditions name their trigger, detector, consequence and invalidated documents — including four findings that would *expand* scope. A plan that only lists ways to shrink will only ever be revised downward.

7. **The plan refuses to build the most expensive thing.** No block editor, no CRDT, no graph DB, no vector store, no agent framework. The novel work is confined to bitemporal memory, promotion, context compilation and the agent boundary — small enough to build correctly.

---

## Unresolved after F1-R1

**Closed by R1 — no longer blockers:**

| Was blocking | Now |
|---|---|
| ~~Q-1 repository identity~~ | ✅ **CLOSED** — `TheHalfMoon/Fehrest` ([R1-01](reviews/F1-R1-RECONCILIATION.md)) |
| Q-8 v1 target wedge | ⚠️ **NOT closed.** `PROVISIONALLY_ACCEPTED_FOR_PLANNING` / `FOUNDER_RATIFICATION_REQUIRED` ([Q-8](16-OPEN-QUESTIONS.md#q-8--v1-target-wedge-provisionally-accepted-for-planning)) |

> **Governance correction (pre-G2).** An earlier revision recorded Q-8 as RESOLVED. It is a **planning assumption only** and remains an open founder decision. The wedge wording is **not founder-approved**.

**Closed by R2 — founder decisions:**

| Was blocking | Now |
|---|---|
| ~~Q-2 core implementation language~~ | ✅ **CLOSED — Rust** (D-1). [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) `ACCEPTED`; [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) and [I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python) make it testable |
| *(new)* Engineering method | ✅ **CLOSED** — Spec Kit (D-2) + Ponytail (D-3), development governance only ([ADR-0014](09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail), [S](19-ENGINEERING-METHOD.md)) |

**Still blocking Phase 0 exit:**

- **[Q-3](16-OPEN-QUESTIONS.md#q-3--desktop-shell) Desktop shell** ([ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) OPEN). Weak recommendation: Tauri 2. **Explicitly not resolved by D-1** — "the core is Rust, therefore the shell is Tauri" is an association, not an argument. Partly editor-dependent, so genuinely better decided after Phase 3E.
- **[B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement) event-volume measurement** — new in R2, and a gate on freezing any event-tiering, retention, compaction or checkpoint-cadence parameter.

**Opened by R1 — resolved by executable gates, not argument:**

| # | Item | Resolved by |
|---|---|---|
| U-1 | Editor architecture | [Phase 3E](15-IMPLEMENTATION-PHASES.md#phase-3e--editor-bake-off-gate) |
| U-2 | Graph Intelligence runtime shape | [GI-BENCH](10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) |
| U-3 | Round-trip fidelity ceiling per candidate | Phase 3E, P-1…P-6 |

**Founder decisions, later phases:** [Q-1a](16-OPEN-QUESTIONS.md#q-1--repository-identity-closed) (license — *separate from identity*), [Q-4](16-OPEN-QUESTIONS.md#q-4--is-ai-off-a-first-class-product-or-a-compliance-mode) (`AI OFF` positioning), [Q-5](16-OPEN-QUESTIONS.md#q-5--how-intrusive-may-fehrest-be-with-user-files) (frontmatter intrusion), [Q-7](16-OPEN-QUESTIONS.md#q-7--is-the-graph-worth-300-mb) (Graph Intelligence packaging cost — now a *packaging* question, not a capability one).

**Not blockers, but unproven:** hypotheses [H-1](research/EVIDENCE_LOG.md#h-1--fts5--graph-expansion-beats-dense-retrieval-on-personal-vaults) through [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path), each scheduled against a named benchmark.

---

## Documents added in F1-R2

```
docs/19-ENGINEERING-METHOD.md            # Spec Kit + Ponytail governance (D-2, D-3)
docs/20-FUTURE-GATES.md                  # Visual/Canvas · Unified Surface · CRDT · View Engine
docs/reviews/F1-R2-RECONCILIATION.md     # the R2 delta table
```

Modified in F1-R2: `README.md` and every document under `docs/` except `docs/reviews/F1-R1-RECONCILIATION.md`, which is preserved intact as the R1 audit trail. Full list in [R2 §10](reviews/F1-R2-RECONCILIATION.md#10-files).

## Documents added in F1-R1

```
docs/reviews/F1-R1-RECONCILIATION.md    # the delta table for all 20 findings
docs/18-EDITOR-GATE.md                  # prototype bake-off replacing the F1 editor decision
```

## Documents modified in F1-R1

```
README.md                               # repo truth, editor reopened, four-layer model
docs/00-PRODUCT-THESIS.md               # v1 wedge (R1-11), four-layer architecture (R1-12)
docs/01-ARCHITECTURE-CONSTITUTION.md    # G-ID-1..4 (R1-05), I-14 strengthened (R1-13)
docs/03-CANONICAL-DATA-MODEL.md         # layout provisional (R1-17), identity ops (R1-15),
                                        #   round-trip argument retracted (R1-04)
docs/04-DERIVED-DATA-MODEL.md           # canonical/derived split (R1-16), capability vs
                                        #   implementation (R1-06), G-ID schema fields
docs/05-MEMORY-MODEL.md                 # native evidence/trust model (R1-08)
docs/06-AGENT-MODEL.md                  # 7-level trust stratification (R1-13)
docs/08-DONOR-MATRIX.md                 # BlockSuite/CodeMirror/Yjs/AFFiNE reclassified
docs/09-TECHNOLOGY-DECISIONS.md         # ADR-0002 reopened, 0003 provisional, 0004
                                        #   re-grounded, 0012 conditional, 0013 added
docs/10-BENCHMARK-PLAN.md               # GI-BENCH added (R1-07), B-7 thresholds (R1-18)
docs/14-PERFORMANCE-BUDGETS.md          # D2 budgets withdrawn pending GI-BENCH (R1-07)
docs/15-IMPLEMENTATION-PHASES.md        # Phase 3E editor gate added (R1-03)
docs/16-OPEN-QUESTIONS.md               # Q-1 closed (R1-01), Q-8 resolved (R1-11)
docs/17-FAILURE-CONDITIONS.md           # F-3 rewritten (R1-06), F-4/F-5 rewritten (R1-02)
docs/VERDICT.md                         # this document
docs/research/EVIDENCE_LOG.md           # E-0, E-4, E-10 corrected; E-5/E-6 reclassified
docs/research/FEHREST_SOURCE_REGISTRY.md# risk schema (R1-20), SRC-003/004/005/006 reclassified
```

## Documents created in F1 (unchanged in R1)

```
docs/02-THREAT-MODEL.md
docs/07-CONTEXT-COMPILER-SPEC.md
docs/11-SECURITY-VERIFICATION-PLAN.md
docs/12-MIGRATION-SCHEMA-EVOLUTION.md
docs/13-RECOVERY-MODEL.md
```

<details>
<summary>Full F1 inventory</summary>

```
README.md
docs/00-PRODUCT-THESIS.md
docs/01-ARCHITECTURE-CONSTITUTION.md
docs/02-THREAT-MODEL.md
docs/03-CANONICAL-DATA-MODEL.md
docs/04-DERIVED-DATA-MODEL.md
docs/05-MEMORY-MODEL.md
docs/06-AGENT-MODEL.md
docs/07-CONTEXT-COMPILER-SPEC.md
docs/08-DONOR-MATRIX.md
docs/09-TECHNOLOGY-DECISIONS.md
docs/10-BENCHMARK-PLAN.md
docs/11-SECURITY-VERIFICATION-PLAN.md
docs/12-MIGRATION-SCHEMA-EVOLUTION.md
docs/13-RECOVERY-MODEL.md
docs/14-PERFORMANCE-BUDGETS.md
docs/15-IMPLEMENTATION-PHASES.md
docs/16-OPEN-QUESTIONS.md
docs/17-FAILURE-CONDITIONS.md
docs/VERDICT.md
docs/research/FEHREST_SOURCE_REGISTRY.md
docs/research/EVIDENCE_LOG.md
```

</details>

---

## Repository context used

**Canonical repository: `TheHalfMoon/Fehrest`** — private, default branch `main`, size 0, no implementation. Repository identity is **CLOSED** ([R1-01](reviews/F1-R1-RECONCILIATION.md)).

**Environment access limitation:** this session authenticates as `wepld` and cannot read `TheHalfMoon/Fehrest`. The 404 it returns is an authorization signal, not an existence signal — GitHub returns 404 rather than 403 for private repositories precisely to avoid disclosing them. F1 misread this. Recorded as an environment limitation.

**`wepld/Fehrest` is NOT canonical**, is not a fallback, and received nothing.

**No upstream HEAD to report** — the canonical repository is empty (size 0).

**Local commit context:** the planning package lives in a local git repository at `C:\Users\Shehr\OneDrive\Desktop\Fehrest`, branch `main`, whose `origin` now points at `https://github.com/TheHalfMoon/Fehrest.git`. **Nothing has been pushed.**

**Donor commits pinned:**

| Donor | Pinned | Note |
|---|---|---|
| `Graphify-Labs/graphify` | `0738af373af9cf5c95f862cc5f3327fd96b4ea23` (`v8`, 2026-08-16) · PyPI `graphifyy==0.9.45` | Identity issues #550/#811/#1033/#2614 **fixed** at this commit |
| `deepseek-ai/deepseek-harness` | `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca` (`master`, 2026-08-17) | Patterns only |
| `toeverything/AFFiNE` | `b4c8548c09da21b2898443559a5b846f0ccf5dd8` (`canary`, 2026-08-17) | **Source of Candidate B**; `blocksuite/` subtree active through 2026-08-10 |
| `toeverything/blocksuite` | `5cb5cb68471ca692f3c162258f0087cb22fcb82d` (`main`, 2025-07-07) | **Stale mirror — recorded so it is never used** |

---

## Confirmation

I confirm that:

- **No product implementation was performed** in F1, F1-R1 or F1-R2. No source file, module, schema, migration, test or scaffold was created. `cargo new` was not run. The only artifacts are planning documents.
- **No speculative scaffolding was created** to demonstrate progress.
- **No editor prototype was built.** Phase 3E is specified, not executed.
- **No headless proof slice was built.** [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) is defined, not executed.
- **Spec Kit was not initialized and Ponytail was not installed.** Both are recorded as decisions and stood up at Phase 0.
- **No Graphify sidecar was built.** No Graphify port was performed.
- **No Spark, JVM, or any part of a Spark runtime entered v1.** Concepts only ([SRC-100](research/FEHREST_SOURCE_REGISTRY.md#414-apache-spark--study--defer)).
- **The final donor-discovery round adopted no runtime dependency.** 24 sources entered the registry as STUDY, BENCHMARK, DEFER or gate-pending; **17 are `PIN_PENDING_EXTERNAL_VERIFICATION` and no commit hash was guessed** ([R2 §9](reviews/F1-R2-RECONCILIATION.md#9-final-donor-discovery-reconciliation)).
- **Broad donor discovery is now FROZEN.** New sources enter only through a documented gap trigger ([registry §14.9](research/FEHREST_SOURCE_REGISTRY.md#149-research-freeze--now-binding)).
- **No Yjs, vectors, DuckDB, TimesFM, UI or cloud infrastructure was added.**
- **Nothing was merged. Nothing was pushed.** The local `origin` was set to the canonical repository so that any future push targets the right remote and can never default to `wepld/Fehrest`; no push occurred.
- **Implementation is not authorized** and is not claimed to be.
- **The Code Provenance Ledger remains empty**, correctly, because no donor code has been copied or adapted ([registry §11](research/FEHREST_SOURCE_REGISTRY.md#11-code-provenance-ledger)).
- **Live repository truth took precedence over prior conclusions.** Three F1 findings were retracted on re-verification.

---

## Note to GPT-5.6 Sol — R2 delta review

**Read [the R2 delta](reviews/F1-R2-RECONCILIATION.md) first**, and [§3 "Substance NOT accepted"](reviews/F1-R2-RECONCILIATION.md#3-substance-not-accepted--recorded-explicitly) before the delta table. Four proposed remedies were rejected while their findings were accepted; if any of those refusals is wrong, that is the most consequential thing in this round.

The most useful attacks would be on:

1. **The four rejected remedies** ([R2 §3](reviews/F1-R2-RECONCILIATION.md#3-substance-not-accepted--recorded-explicitly)). Is refusing `10K–100K events/day` *and* `500/day` the right call, or is deferring to measurement a way of deferring the decision? Is the platform-aware path key actually implementable, or is `casefold+NFC` wrong-but-shippable while the correct answer is wrong-but-unbuildable?
2. **Whether [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) is genuinely the smallest thesis test.** It carries identity, SQLite, FTS5, bitemporal resolution, the served-item manifest and a bounded compiler. Each is argued necessary; the ensemble is still a substantial build for something meant to fail cheaply.
3. **Whether the four-axis memory model is over-engineered** for a single-user product. [R2-04](reviews/F1-R2-RECONCILIATION.md#4-delta-table) argues the single enum was *invalid*, not merely awkward. If the axes are right but the cost is wrong, what collapses safely?
4. **Whether removing confidence from resolution will produce an unusable abstention rate** ([F-20](17-FAILURE-CONDITIONS.md#f-20--the-four-axis-memory-model-produces-unusable-abstention-rates)). The plan forbids restoring it and demands more evidence-based rungs instead. Is that a principled position or an unfunded mandate?
5. **Whether `pending_advisory` is a safety feature or an attack surface.** An adversary who cannot poison memory may still flood the advisory channel and steer an agent toward the wrong questions. Is "can only cause an agent to stop and ask" a strong enough bound?
6. **[B-7](10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment)'s two-stage design.** Is `INCONCLUSIVE` a genuine safeguard against an underpowered pilot falsely killing the product, or a licence to proceed regardless of what the pilot shows?
7. **The maintained-LLM-Wiki baseline** ([A §8.1](00-PRODUCT-THESIS.md#81-the-maintained-wiki-baseline-and-what-it-demands-added-in-f1-r2)). It is the hardest simple bar in the plan. Is it hard enough, and is the list of what Fehrest must show *beyond* it complete?
8. **Whether the [Editor Gate](18-EDITOR-GATE.md#6-scoring) weights should have been changed rather than marked provisional**, and specifically whether agent editability at 5% is double-counted under fidelity or genuinely under-weighted ([Q-16](16-OPEN-QUESTIONS.md#q-16--editor-gate-weights-and-agent-editability)).
9. **Whether the Event Plane's T1/T2/T3 tiering is over-engineered** for a single-user product — still open, and now explicitly unfrozen pending [B-0](10-BENCHMARK-PLAN.md#b-0--event-volume-measurement).

**Two failure modes are worth attacking directly.** F1's was reading **absence of signal as evidence of absence**. F1-R2's findings clustered on a different one: **an unmeasured number or an untested engine property propagating into decisions without a status label**. If either pattern survives anywhere else in the package, it is the thing most likely to embarrass the next review — and the second is harder to spot, because an assumption stated confidently reads exactly like a finding.
