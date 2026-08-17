# F1-R1 Architecture Reconciliation

**Phase:** `F1-R1` ACTIVE
**Date:** 2026-08-17
**Canonical repository:** `TheHalfMoon/Fehrest` (private, `main`, size 0, no implementation)
**Prior state:** F1 planning package, local commits `463e213` → `dd38f55`
**This reconciliation:** local commit `a8a1b4c` (not pushed)
**Next gate:** GPT-5.6 Sol delta review

**Implementation is NOT authorized. No product code was written in F1 or F1-R1.**

> **Amended pre-G2:** two governance corrections were applied after this delta was written — the v1 wedge is provisional (not decided), and Graph Intelligence is explicitly falsifiable. They **supersede** the corresponding rows in §2 and §4 below, which are left intact as the R1 audit trail. See [§10](#10-post-r1-governance-corrections-pre-g2).

---

## 1. What this document is

A precise delta against the F1 planning package, incorporating 20 validated review findings. It is not a re-plan. Valid prior work is preserved; three classes of defect are corrected:

| Class | Count | Nature |
|---|---|---|
| **INCORRECT** | 3 | Factually wrong claims that must not survive into review |
| **OVERSTATED** | 4 | Directionally right, evidentially over-claimed |
| **REOPENED** | 3 | Closed too early; returned to gated/open |
| **VALID** | 10 | Confirmed; strengthened where the review asked |

**Three F1 conclusions were wrong and are retracted outright:** the repository-does-not-exist finding, the "BlockSuite is unmaintained" characterisation, and the citation of fixed upstream Graphify bugs as current defects. Each is corrected at the source, not annotated around.

---

## 2. Delta table

| ID | Prior claim | Verdict | Evidence | Required correction | Files changed | Downstream impact | Status |
|---|---|---|---|---|---|---|---|
| **R1-01** | `TheHalfMoon/Fehrest` does not exist (404); `wepld/Fehrest` is the only reachable Fehrest; repository identity is an unresolved founder decision | **INCORRECT** | 404 reproduced, but authenticated account is `wepld`; `TheHalfMoon` private repos are invisible to it. `users/TheHalfMoon/repos?type=all` returns only public entries. Founder asserts existence: private, `main`, size 0 | Canonical repo is `TheHalfMoon/Fehrest`. Repository identity **CLOSED**. 404 recorded as environment access limitation. `wepld/Fehrest` explicitly non-canonical. Only release timing / license / publication remain open | [E-0](../research/EVIDENCE_LOG.md#e-0--canonical-repository-state), [README](../../README.md), [VERDICT](../VERDICT.md), [Q-1](../16-OPEN-QUESTIONS.md#q-1--repository-identity-closed) | Removes a Phase 0 blocker | ✅ Applied |
| **R1-02** | BlockSuite is stale ⇒ CodeMirror 6 is the v1 editor ([ADR-0002](../09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated) decided) | **OVERSTATED → REOPENED** | `toeverything/blocksuite` standalone mirror last synced 2025-07-07 (**confirmed**). But `toeverything/AFFiNE` `blocksuite/` subtree is **actively developed**: commits through 2026-08-10 including `feat(editor): improve select perf` (#15353), `feat(editor): code block line numbers` (#15376), `chore: bump up js-yaml v5 [SECURITY]` (#15385). The *distribution path* is stale; the *implementation* is not | ADR-0002 reclassified `OPEN / PROTOTYPE-GATED`. Candidates A (CodeMirror 6), B (maintained AFFiNE BlockSuite subtree), C (ProseMirror/Tiptap/Milkdown, only if a real gap) | [ADR-0002](../09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated), [E-10](../research/EVIDENCE_LOG.md#e-10--blocksuite-distribution-is-stale-the-implementation-is-not-editor-gate), [18-EDITOR-GATE](../18-EDITOR-GATE.md), [D §7](../03-CANONICAL-DATA-MODEL.md#7-the-rich-editor--canonical-file-question-open), [I](../08-DONOR-MATRIX.md), [SRC-003/004/006](../research/FEHREST_SOURCE_REGISTRY.md) | **Adds Phase 3E editor bake-off.** Phase 7 scope now gate-dependent | ✅ Applied |
| **R1-03** | No executable editor gate; decision made on architectural argument | **VALID (gap)** | F1 decided the editor without a prototype | New [Editor Gate](../18-EDITOR-GATE.md): common corpus, 24-item acceptance suite, weighted scoring model, ADR-producing | [18-EDITOR-GATE](../18-EDITOR-GATE.md), [P Phase 3E](../15-IMPLEMENTATION-PHASES.md#phase-3e--editor-bake-off-gate) | New gated phase before Phase 7 | ✅ Applied |
| **R1-04** | Lossless rich-editor ↔ Markdown round-trip requires preserving CRDT history ⇒ the sidecar becomes canonical ⇒ Markdown becomes decorative | **OVERSTATED** | The claim conflated six separable concerns. CRDT operation history is collaboration machinery, not document meaning. Not established that it must be canonical | Retract the impossibility argument. Separate the six concerns; specify the proof the Editor Gate must produce. Candidate `note.md` + `note.fehrest.json` architecture presented as a **candidate to test**, not adopted | [D §7](../03-CANONICAL-DATA-MODEL.md#7-the-rich-editor--canonical-file-question-open), [ADR-0002](../09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated), [18-EDITOR-GATE §4](../18-EDITOR-GATE.md#4-the-round-trip-proof-obligation) | Removes a false constraint on Candidate B | ✅ Applied |
| **R1-05** | Graphify node IDs carry documented same-filename collisions (#550), Unicode collapse (#811), Turkish idempotency failure (#2614) — cited in present tense | **INCORRECT (evidence) / VALID (conclusion)** | CHANGELOG at pinned commit: #2614 fixed in **0.9.40 (2026-08-11)**; #811 fixed (NFKC + casefold + `re.UNICODE`); #1033 fixed; #811/#550/#1033/#1104 root cause resolved by unifying four copies into `graphify.ids` with contract + hypothesis property tests. `_disambiguate_colliding_node_ids` actively salts collisions apart in current code | Retract present-tense bug citations. Re-ground the invariant on **structure, not defects**: file IDs are spec'd `{parent_dir}_{stem}` — path-derived by construction — and upstream explicitly rejected extension-aware IDs because they would "rewrite every file and symbol id and force a full-rebuild migration". Add invariants **G-ID-1..4** | [E-4](../research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect), [B §1](../01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities), [ADR-0004](../09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque), [README](../../README.md) | Conclusion unchanged; **evidence is now stronger** | ✅ Applied |
| **R1-06** | Plan risked conflating Graphify implementation cost with graph-intelligence product importance; [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) offered "drop the graph entirely" | **PARTIALLY_VALID** | Graph Intelligence is thesis-critical; Graphify is one candidate implementation | Split explicitly: `GRAPH_INTELLIGENCE_CAPABILITY = CORE`; `GRAPHIFY_PYTHON_RUNTIME = REPLACEABLE CANDIDATE`. F-3 no longer permits dropping the capability — only replacing the implementation | [A §4](../00-PRODUCT-THESIS.md#5-the-four-layer-architecture), [E §4](../04-DERIVED-DATA-MODEL.md#5-graph-intelligence-capability-vs-implementation), [I](../08-DONOR-MATRIX.md), [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape), [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) | Protects thesis from an implementation-cost cascade | ⚠️ Applied, then **SUPERSEDED by [G-02](#g-02--graph-intelligence-is-explicitly-falsifiable)** |
| **R1-07** | 100K files ≈ 90 min presented in budget tables as a system property | **OVERSTATED** | Single machine, single corpus (Graphify's own source, 776 files), Windows, cold cache. Linear extrapolation only | Label all figures `PRELIMINARY / SINGLE-ENVIRONMENT / SINGLE-CORPUS`. Remove extrapolations from budget tables; replace with `TBD — pending GI-BENCH`. Define **GI-BENCH** matrix (4 vault sizes × 5 corpus types × 10 operations × concurrency) as prerequisite to any runtime/packaging decision | [E-5](../research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary), [E-6](../research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-preliminary), [O](../14-PERFORMANCE-BUDGETS.md), [K GI-BENCH](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix), [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) | **ADR-0003 downgraded from decided to provisional-pending-GI-BENCH** | ✅ Applied |
| **R1-08** | `AMBIGUOUS = 0%` ⇒ treat confidence as effectively two-level; memory trust vocabulary partly inherited from Graphify | **VALID** | One corpus proves nothing about ambiguity in general | Fehrest defines a **native evidence/trust model** with explicit states and transitions. Extractor labels **map into** it, never define it | [F §3.3](../05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model), [E §4.2](../04-DERIVED-DATA-MODEL.md#52-the-wire-contract) | Trust model no longer donor-coupled | ✅ Applied |
| **R1-09** | Yjs = DEFER (global) | **PARTIALLY_VALID** | If Candidate B wins the Editor Gate, Yjs arrives as part of the substrate | Reclassify `CONDITIONAL / EDITOR-DEPENDENT`. Collaboration must **not** be added to MVP to justify Yjs | [SRC-005](../research/FEHREST_SOURCE_REGISTRY.md#32-yjs--conditional--editor-dependent), [ADR-0012](../09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent), [I](../08-DONOR-MATRIX.md) | Tied to Editor Gate outcome | ✅ Applied |
| **R1-10** | DuckDB/TimesFM/Data Formulator/Superset deferred | **VALID** | — | Preserve. Keep in registry as research history; do not expand slice 1 | none (confirmed) | None | ✅ Confirmed |
| **R1-11** | "Who is v1 for" left vague ([Q-8](../16-OPEN-QUESTIONS.md#q-8--v1-target-wedge-provisionally-accepted-for-planning)) | **VALID (gap)** | Materially affects architecture | Adopt default wedge: power users, developers, researchers, AI-native knowledge workers running **multiple agents across providers**, needing portable durable project memory. Recorded as founder-decision candidate with the strongest alternative stated | [A §3](../00-PRODUCT-THESIS.md#4-the-v1-user-wedge), [Q-8](../16-OPEN-QUESTIONS.md#q-8--v1-target-wedge-provisionally-accepted-for-planning) | Confirms MCP-first, CLI-first ordering; keeps graph in v1 | ⚠️ Applied, then **SUPERSEDED by [G-01](#g-01--v1-target-wedge-is-provisional-not-decided)** |
| **R1-12** | Event plane present but not architecturally foregrounded | **PARTIALLY_VALID** | Four-layer model was implicit | Make explicit: Knowledge → (Graph Intelligence ∥ Event Journal) → Memory → Context Compiler | [A §4](../00-PRODUCT-THESIS.md#5-the-four-layer-architecture), [D §5](../03-CANONICAL-DATA-MODEL.md#5-the-event-plane) | Presentation; no decision change | ✅ Applied |
| **R1-13** | [I-14](../01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) required reconstructable/auditable agent-visible state | **VALID (strengthen)** | Needed scope-authorization + explicit trust stratification | I-14 strengthened to require reconstructable **+ provenance-linked + scope-authorized + auditable**, with a **7-level trust stratification** that must never be collapsed | [I-14](../01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable), [G §4](../06-AGENT-MODEL.md#4-context-delivery-and-the-trust-stratification) | Strengthens GLM-5.3 posture | ✅ Applied |
| **R1-14** | "Content is evidence, never authority" canonical | **VALID** | — | Retain; three-plane separation retained; prompt-only enforcement still rejected | none (confirmed) | None | ✅ Confirmed |
| **R1-15** | Identity survives rename/move | **PARTIALLY_VALID** | Copy / duplicate / merge-conflict / restored-backup / import cases under-specified | Full identity-event matrix across 11 filesystem operations, distinguishing moved / copied / duplicated / conflicting / imported | [D §3.2](../03-CANONICAL-DATA-MODEL.md#32-identity-across-filesystem-operations), [N](../13-RECOVERY-MODEL.md) | Closes an identity gap before storage prototypes | ✅ Applied |
| **R1-16** | Derived state rebuildable; `.fehrest/derived` deletable | **VALID (clarify)** | Risk of reading "`.fehrest/` is disposable" | Explicit two-class split. **Canonical event and memory state inside `.fehrest/` is NOT disposable** | [E §1](../04-DERIVED-DATA-MODEL.md#1-two-classes-of-state-inside-fehrest), [D §2](../03-CANONICAL-DATA-MODEL.md#2-storage-categories-provisional-layout) | Prevents a catastrophic misreading | ✅ Applied |
| **R1-17** | `.fehrest/` hierarchy presented as settled | **PARTIALLY_VALID** | No ADR justified physical layout | Layout marked **PROVISIONAL**; semantic storage categories defined first; physical layout deferred to post-prototype ADR | [D §2](../03-CANONICAL-DATA-MODEL.md#2-storage-categories-provisional-layout) | Layout ADR added to Phase 1 | ✅ Applied |
| **R1-18** | [B-7](../10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment) benchmarks against plain competent agent | **VALID (strengthen)** | Needed explicit falsification threshold and stated Agent B inputs | Agent B receives **no private chain-of-thought, no Agent A hidden state, no raw conversation dump** — only normal project files/tools + Fehrest context. Explicit falsification threshold added | [B-7](../10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment) | Sharper falsification | ✅ Applied |
| **R1-19** | Scope reductions listed | **VALID** | — | Preserve all exclusions from slice 1 | none (confirmed) | None | ✅ Confirmed |
| **R1-20** | Registry risks did not separate current from historical | **VALID (gap)** | Enabled the R1-05 error | Registry risk fields restructured: current verified state / historical issue / fixed issue / unresolved issue / architectural lesson / Fehrest mitigation | [SRC-001](../research/FEHREST_SOURCE_REGISTRY.md#21-graphify), [registry §1](../research/FEHREST_SOURCE_REGISTRY.md#1-dispositions-changed-in-f1-r1) | Prevents recurrence | ✅ Applied |

---

## 3. Corrected evidence, in full

Three F1 evidence items were wrong. Their corrections are the substance of this reconciliation.

### 3.1 Repository (R1-01)

```
gh api repos/TheHalfMoon/Fehrest   → HTTP 404
gh api user --jq .login            → wepld
```

The 404 is **reproducible and uninformative**. The authenticated principal is `wepld`; `TheHalfMoon` is a different account, and its private repositories are invisible to an unaffiliated token. `users/TheHalfMoon/repos?type=all` returns public entries only — absence there is not evidence of non-existence.

F1 committed a category error: it treated *"not visible to this token"* as *"does not exist."* Corrected. `TheHalfMoon/Fehrest` is canonical. `wepld/Fehrest` is not canonical, is not a fallback, and receives nothing.

### 3.2 Editor (R1-02)

Both facts are true and F1 reported only one:

| Fact | F1 | R1 |
|---|---|---|
| `toeverything/blocksuite` standalone mirror last synced 2025-07-07 | ✅ reported | ✅ retained |
| `@blocksuite/store` unpublished since 2025-07-01 at `0.22.4` | ✅ reported | ✅ retained |
| **AFFiNE `blocksuite/` subtree actively developed through 2026-08-10** | ❌ **missed** | ✅ **added** |

Observed commits touching `blocksuite/` in AFFiNE:

```
2026-08-10  6375f5ab  chore: bump typescript 7 (#15465)
2026-08-10  0c7b20dc  chore: migrate oxlint & oxfmt (#15464)
2026-08-10  ee899a26  feat(server): improve context management (#15448)
2026-07-31  6170a907  feat(editor): permanent global toggle for code block line numbers (#15376)
2026-07-31  fb647b60  chore: bump up js-yaml version to v5 [SECURITY] (#15385)
2026-07-28  e7ec8a10  feat(editor): improve select perf (#15353)
```

Feature work, performance work and security bumps — not a dormant tree. **The correct statement is that the standalone distribution path is stale, not that the editor is unmaintained.** Consequences: the "unpatched transitive vulnerabilities" argument weakens sharply (security bumps land in the maintained tree), and Candidate B must be evaluated as *vendoring from a maintained monorepo*, which is a packaging and coupling problem — real, but a different and more tractable problem than adopting abandoned code.

### 3.3 Graphify identity (R1-05)

All cited issues are **fixed at the pinned commit**:

| Issue | F1 implied | Actual |
|---|---|---|
| #2614 Turkish `İ` idempotency | current defect | **Fixed in 0.9.40 (2026-08-11)** |
| #811 Unicode collapse | current defect | **Fixed** — NFKC + casefold + `re.UNICODE` |
| #1033 AST-vs-LLM mismatch | current defect | **Fixed** at the relative-path remap chokepoint |
| #550 same-filename collisions | current defect | **Root cause fixed** — four hand-synced copies unified into `graphify.ids`, guarded by contract + hypothesis property tests |

`_disambiguate_colliding_node_ids` is present in current code and actively salts colliding IDs apart. Citing these as live defects was wrong and is retracted.

**The invariant survives on stronger, structural grounds.** Two facts at the pinned commit:

1. File-level node IDs are spec'd `{parent_dir}_{stem}` — **path-derived by construction**. Rename or move changes the ID. Not a bug; the design.
2. Upstream explicitly rejected extension-aware IDs because they "would rewrite every file and symbol id and force a full-rebuild migration."

Fact 2 is the decisive one: **upstream itself states that changing the ID scheme rewrites every ID.** An identifier whose scheme is expected to change across versions cannot be a durable identity. That argument does not depend on any bug, present or past, and cannot be invalidated by upstream fixing things — which is exactly the property F1's bug-based argument lacked.

---

## 4. Decision status after R1

| Decision | F1 | R1 |
|---|---|---|
| Repository identity | OPEN | ✅ **CLOSED** — `TheHalfMoon/Fehrest` |
| v1 user wedge | OPEN | ⚠️ **SUPERSEDED by [G-01](#g-01--v1-target-wedge-is-provisional-not-decided)** — provisional planning assumption; founder ratification required |
| Editor architecture | ❌ DECIDED (CodeMirror 6) | 🔄 **REOPENED** — prototype-gated |
| CRDT / Yjs | DEFER | 🔄 **CONDITIONAL** — editor-dependent |
| Graph Intelligence capability | implicit, at risk | ⚠️ **SUPERSEDED by [G-02](#g-02--graph-intelligence-is-explicitly-falsifiable)** — core current product hypothesis, explicitly falsifiable |
| Graph Intelligence runtime | ADR-0003 decided (sidecar) | 🔄 **PROVISIONAL** — pending GI-BENCH |
| Extractor IDs ≠ canonical identity | decided (weak evidence) | ✅ **DECIDED** — G-ID-1..4, structural evidence |
| Derived state rebuildable | decided | ✅ **RETAINED** + canonical/derived split clarified |
| Storage layout | presented as settled | 🔄 **PROVISIONAL** — semantic categories first |
| Lexical-first retrieval | decided | ✅ RETAINED |
| Bitemporal memory | decided | ✅ RETAINED |
| Content is evidence, never authority | decided | ✅ RETAINED + strengthened |
| Core language / desktop shell | OPEN | OPEN — unchanged, deliberately |
| Data Intelligence deferrals | deferred | ✅ RETAINED |

**Net:** two decisions closed, three reopened, one downgraded to provisional, one capability promoted to core.

---

## 5. Downstream impact

**New gated work:**
- **Phase 3E — Editor Bake-Off Gate** ([18-EDITOR-GATE](../18-EDITOR-GATE.md)), blocking Phase 7.
- **GI-BENCH** ([B-11](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix)), blocking any Graph Intelligence runtime/packaging decision.
- **Storage layout ADR**, Phase 1.

**Removed:** repository-identity blocker; v1-persona blocker.

**Unchanged:** the vertical-slice sequence, all constitutional invariants except the strengthened I-14 and added G-ID-1..4, the threat model, the security verification plan, and [B-7](../10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment) as the falsification experiment.

---

## 6. Unresolved after R1

| # | Item | Why it stays open | Resolved by |
|---|---|---|---|
| U-1 | Editor architecture | Requires executable prototype evidence | Phase 3E |
| U-2 | Graph Intelligence runtime shape | Requires GI-BENCH across corpus types | B-11 |
| U-3 | Round-trip fidelity ceiling per candidate | Requires the gate's acceptance suite | Phase 3E |
| U-4 | Core implementation language ([ADR-0010](../09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language)) | Founder priority, not deduction. **Not to be closed merely to close it** | Founder |
| U-5 | Desktop shell ([ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell)) | Same; partly editor-dependent | Founder / Phase 3E |
| U-6 | License and publication timing | Commercial decision | Founder |
| U-7 | `AI OFF` positioning ([H-3](../research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)) | Needs B-5 | Phase 4 |
| U-8 | Whether structured `payload` extraction is common enough | Needs B-4 | Phase 4 |

U-4 and U-5 are called out because the review explicitly forbids closing them for tidiness. They remain open.

---

## 7. Findings NOT accepted

None. All 20 findings were accepted in full or in the corrected form recorded above.

Two are worth flagging for GPT-5.6 Sol as places where I applied judgement beyond the literal instruction:

1. **R1-04.** The review asked me to stop asserting the impossibility argument. I did — but I did not swing to asserting round-trip *is* achievable. Both would be unevidenced. The gate now carries an explicit **proof obligation** ([18-EDITOR-GATE §4](../18-EDITOR-GATE.md#4-the-round-trip-proof-obligation)) that either candidate must discharge with a running prototype.

2. **R1-06.** Promoting Graph Intelligence to CORE required rewriting failure condition F-3, which previously permitted "drop the graph entirely." It now permits only *replacing the implementation*. This is a real tightening of the plan's falsifiability and is deliberate: a capability that is thesis-critical must not be droppable on implementation-cost grounds.

---

## 8. Validation performed

| # | Check | Result |
|---|---|---|
| 1 | All internal Markdown links valid | ✅ 0 broken of 800+ |
| 2 | No document claims `TheHalfMoon/Fehrest` does not exist | ✅ |
| 3 | No document treats `wepld/Fehrest` as canonical | ✅ (referenced only as explicitly non-canonical) |
| 4 | Editor choice is OPEN / prototype-gated | ✅ |
| 5 | Graph Intelligence capability vs Graphify runtime separated | ✅ |
| 6 | Fixed Graphify bugs no longer described as current | ✅ |
| 7 | Extractor IDs still forbidden as canonical identity | ✅ G-ID-1..4 |
| 8 | Yjs editor-dependent | ✅ |
| 9 | DuckDB / TimesFM / Data Formulator deferred | ✅ |
| 10 | Derived state rebuildable | ✅ |
| 11 | Canonical event/memory state not marked disposable | ✅ two-class split |
| 12 | Agent Event Plane represented | ✅ four-layer model |
| 13 | v1 target user resolved | ⚠️ **SUPERSEDED by [G-01](#g-01--v1-target-wedge-is-provisional-not-decided)** — provisional only; remains an open founder decision |
| 14 | No product implementation exists | ✅ docs only |
| 15 | No push or merge occurred | ✅ local commits only |

---

## 9. Verdict

# `F1_R1_RECONCILED_READY_FOR_GPT_REVIEW`

All 20 findings reconciled. Three factually incorrect claims retracted at source. Three decisions reopened with executable gates rather than argument. No implementation performed, nothing pushed, nothing merged.

---

## 10. Post-R1 governance corrections (pre-G2)

Applied **after** the R1 delta above and **before** GPT-5.6 Sol review. Recorded as an amendment rather than by rewriting §2, so the R1 audit trail stays intact — consistent with Fehrest's own append-only correction principle ([R-5](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).

Two corrections. **No other architecture changes were made.**

### G-01 — V1 target wedge is provisional, not decided

**Supersedes:** the R1-11 row in §2, the "v1 user wedge — RESOLVED (candidate)" row in §4, and validation item 13 in §8.

**Status now:**

```
V1 TARGET WEDGE:
PROVISIONALLY_ACCEPTED_FOR_PLANNING
FOUNDER_RATIFICATION_REQUIRED
```

**Current planning candidate, NOT founder-approved:**

> "Power users, developers, researchers, and AI-native knowledge workers who regularly use multiple agents and need durable local project memory across tools, sessions, and model providers."

**Why corrected.** R1 recorded this as "RESOLVED (candidate)," which reads as closer to settled than it is. The wedge drives four architecture consequences (MCP gateway in v1, CLI-first ordering, Graph Intelligence in v1, local-first as a feature), so recording it as resolved would let those consequences inherit an authority the decision does not have. **Q-8 remains OPEN.**

**Constraint.** No document may describe this wedge as approved, decided, or resolved unless the founder explicitly authorizes the wording.

**Files:** [A §4](../00-PRODUCT-THESIS.md#4-the-v1-user-wedge), [Q-8](../16-OPEN-QUESTIONS.md#q-8--v1-target-wedge-provisionally-accepted-for-planning), [VERDICT](../VERDICT.md), [README](../../README.md).

### G-02 — Graph Intelligence is explicitly falsifiable

**Supersedes:** the R1-06 row in §2 ("F-3 no longer permits dropping the capability — only replacing the implementation") and the "Graph Intelligence capability — CORE" row in §4.

**Status now:**

```
GRAPH INTELLIGENCE:
CORE CURRENT PRODUCT HYPOTHESIS
EXPLICITLY FALSIFIABLE
```

**Failure condition added to [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost):**

> If controlled continuation/retrieval benchmarks show that graph-assisted understanding does not provide a material benefit over simpler local retrieval approaches at acceptable cost, Fehrest MUST permit redesign or removal of Graph Intelligence from the core product hypothesis.

**Why corrected.** R1 fixed a real problem — F1 let implementation cost threaten a core capability — but overcorrected into "may be REPLACED, never DROPPED." That made a product claim **unfalsifiable**, which is precisely what [17-FAILURE-CONDITIONS](../17-FAILURE-CONDITIONS.md) exists to prevent. A core capability may be load-bearing *and* testable; those are not in tension.

**What is preserved from R1-06.** The capability/implementation distinction still holds, and still matters: a weak result from one implementation or one retrieval configuration is evidence about *that pairing*. F-3 is graduated accordingly, and removal requires evidence "across configurations and corpus types" — which guards equally against premature deletion and against indefinite deflection of a genuinely negative result.

**Files:** [A §5](../00-PRODUCT-THESIS.md#5-the-four-layer-architecture), [E §5](../04-DERIVED-DATA-MODEL.md#5-graph-intelligence-capability-vs-implementation), [I §1](../08-DONOR-MATRIX.md#1-dispositions-as-reconciled-in-f1-r1), [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape), [B-3](../10-BENCHMARK-PLAN.md#b-3--retrieval-quality-by-stage), [B-11](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix), [O](../14-PERFORMANCE-BUDGETS.md), [P Phase 3](../15-IMPLEMENTATION-PHASES.md#phase-3--graph-sidecar), [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost), [registry §1.3](../research/FEHREST_SOURCE_REGISTRY.md#13-confirmed-from-f1), [README](../../README.md).

### Scope confirmation

These two corrections are **governance only**. No architecture decision, invariant, threat-model control, benchmark design, phase structure or donor disposition was altered beyond what G-01 and G-02 require. No product code exists. Nothing pushed, nothing merged.
