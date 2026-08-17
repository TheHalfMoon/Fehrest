# Final Verdict

**Date:** 2026-08-17
**Author role:** Principal Architect
**Gate:** Independent adversarial review (GPT-5.6 Sol), then reconciliation, then a second independent review, then GLM-5.3 security review.

---

## Verdict

# `READY_FOR_ADVERSARIAL_REVIEW`

**Justification.** Every architecture gate the brief identified has been resolved against live repository evidence rather than description. The editor gate is decided (dissolved, with two independent converging arguments). The Graphify boundary is decided from measurement. The event model is decided from a specification-grade donor. No gate remains open that would make review premature.

Two decisions are deliberately left OPEN — core language ([ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language)) and desktop shell ([ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell)) — because they turn on founder priorities rather than architectural deduction, and neither is on the critical path for Phases 0–6. Deciding them on my own preference would have been the false confidence this package exists to avoid.

The verdict is not `RESEARCH_GAPS_BLOCK_PLANNING` because the gaps that remain are **experiments scheduled in [Phase 0](15-IMPLEMENTATION-PHASES.md)**, not unknowns that would change the plan's shape. It is not `REDESIGN_REQUIRED_BEFORE_REVIEW` because the redesigns the evidence demanded — BlockSuite, Graphify IDs, DuckDB priority, AFFiNE — have already been made here rather than deferred to a reviewer.

---

## Highest-risk assumptions

Ranked by damage if wrong.

| # | Assumption | Risk | Falsified by |
|---|---|---|---|
| 1 | **Compiled context beats a competent agent with plain file tools** | **Thesis-fatal.** LongMemEval-V2's own reporting shows the best system beating an off-the-shelf coding agent by only **3.2 points** (72.5% vs 69.3%). The margin is genuinely thin | [B-7](10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment) at Phase 6 |
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

1. **The evidence base is measured, not cited.** Cold/warm import times, extraction throughput, installed footprint, confidence distribution, and upstream health were all obtained by running and inspecting the actual code at pinned commits. Four decisions in the founder's brief were changed *because* of measurement ([registry §1](research/FEHREST_SOURCE_REGISTRY.md#1-dispositions-changed-from-the-founders-draft-registry)).

2. **The editor gate is dissolved rather than solved.** Adopting no document model richer than the canonical format makes round-trip an identity function. Two independent arguments — structural impossibility (Markdown has no identity or overlap primitives) and upstream health (a 13-month-stale unreleased mirror) — reach the same decision. Converging independent arguments are much harder to defeat than either alone.

3. **Every invariant has a test.** [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default) through [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) name their enforcing mechanism and their detector. Two were amended precisely because they were unenforceable as written, with the arguments given rather than the changes made quietly.

4. **The security boundary is structural, and its limits are stated.** Capability grants are computed before retrieval and frozen; agents address objects by ID so path traversal is removed at the interface rather than defended at every call site. And the model explicitly distinguishes **boundary** controls from **defence-in-depth** ones, stating plainly that Fehrest bounds privilege, not persuasion. Overclaiming here is the standard failure of agent security documents.

5. **Disposability is load-bearing and it pays for itself.** [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) is what makes `synchronous=NORMAL` safe, makes index corruption an availability problem, makes "delete the derived directory" a support instruction, eliminates derived-schema migration entirely, and makes every index decision reversible. One invariant carrying five consequences is a sign the decomposition is right.

6. **Failure conditions are specific and run both ways.** Seventeen conditions name their trigger, detector, consequence and invalidated documents — including four findings that would *expand* scope. A plan that only lists ways to shrink will only ever be revised downward.

7. **The plan refuses to build the most expensive thing.** No block editor, no CRDT, no graph DB, no vector store, no agent framework. The novel work is confined to bitemporal memory, promotion, context compilation and the agent boundary — small enough to build correctly.

---

## Unresolved blockers

**Blocking Phase 0 exit:**

- **[Q-1](16-OPEN-QUESTIONS.md#q-1--which-repository-is-canonical) Canonical repository, visibility and license.** `TheHalfMoon/Fehrest` does not exist; `wepld/Fehrest` is empty. Founder decision.
- **[Q-2](16-OPEN-QUESTIONS.md#q-2--core-implementation-language) Core language** ([ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) OPEN). Weak recommendation: Rust core + TypeScript UI.
- **[Q-3](16-OPEN-QUESTIONS.md#q-3--desktop-shell) Desktop shell** ([ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) OPEN). Weak recommendation: Tauri 2.

**Blocking later phases:** [Q-4](16-OPEN-QUESTIONS.md#q-4--is-ai-off-a-first-class-product-or-a-compliance-mode) (`AI OFF` positioning), [Q-5](16-OPEN-QUESTIONS.md#q-5--how-intrusive-may-fehrest-be-with-user-files) (frontmatter intrusion), [Q-7](16-OPEN-QUESTIONS.md#q-7--is-the-graph-worth-300-mb) (is the graph worth 300 MB), **[Q-8](16-OPEN-QUESTIONS.md#q-8--what-is-v1s-target-user) (who is v1 for — unanswered anywhere, and it changes real decisions)**.

**Not blockers, but unproven:** all five hypotheses [H-1](research/EVIDENCE_LOG.md#h-1--fts5--graph-expansion-beats-dense-retrieval-on-personal-vaults) through [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path), each scheduled against a specific benchmark.

---

## Documents created

All new. Nothing modified — the repository was empty.

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

---

## Repository HEAD used

**There is none, and this is a finding rather than an omission.**

- `TheHalfMoon/Fehrest` — **HTTP 404. Does not exist.** `TheHalfMoon` is a user account with 8 repositories, none named Fehrest.
- `wepld/Fehrest` — exists, public, created 2026-08-02, **empty**: `HTTP 409 "Git Repository is empty"`, zero branches, zero bytes.
- Local working directory — empty and not a git repository at session start.

A local git repository was initialised on branch `main` to hold this package. **Nothing has been pushed to any remote.**

**Donor commits pinned for this analysis:**

| Donor | Pinned |
|---|---|
| `Graphify-Labs/graphify` | `0738af373af9cf5c95f862cc5f3327fd96b4ea23` (branch `v8`, 2026-08-16) · PyPI `graphifyy==0.9.45` |
| `deepseek-ai/deepseek-harness` | `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca` (`master`, 2026-08-17) |
| `toeverything/blocksuite` | `5cb5cb68471ca692f3c162258f0087cb22fcb82d` (`main`, **2025-07-07**) |
| `toeverything/AFFiNE` | `b4c8548c09da21b2898443559a5b846f0ccf5dd8` (`canary`, 2026-08-17) |

---

## Confirmation

I confirm that:

- **No product implementation was performed.** No source file, module, schema, migration, test or scaffold was created. The only artifacts are planning documents.
- **No speculative scaffolding was created** to demonstrate progress.
- **Nothing was merged.** Nothing was pushed. No remote was created or modified.
- **Implementation is not authorized** and is not claimed to be.
- **The Code Provenance Ledger is empty**, correctly, because no donor code has been copied or adapted ([registry §11](research/FEHREST_SOURCE_REGISTRY.md#11-code-provenance-ledger)).
- **The prompt was not treated as authoritative over live repository truth.** Four of its dispositions were changed on measurement, and its named repository was found not to exist.

---

## Note to the reviewers

The most useful attacks would be on:

1. **[B-7](10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment)'s methodology** — the corpus is self-authored, and that is the plan's weakest methodological point.
2. **Whether the plain-agent baseline is the right bar.** I argue it is the only honest one; a memory system that cannot beat `grep` has not earned its complexity.
3. **Whether deferring BlockSuite makes v1 uncompetitive.** The evidence on staleness is unambiguous, but "AFFiNE ships it daily inside their monorepo" is a genuine counter-argument to "unmaintained," and the product consequence — no block transclusion, no inline comments, no database blocks — is real.
4. **Whether the Event Plane's T1/T2/T3 tiering is over-engineered** for a single-user product.
5. **Whether bitemporality earns its complexity**, or valid-time-only would serve.

I have tried to write this to survive review rather than to persuade. Where I was uncertain I said so; where the founder's brief was contradicted by measurement I said that too, with the measurement attached.
