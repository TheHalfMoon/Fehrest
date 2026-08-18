# Fehrest

**An open-source, local-first knowledge and long-memory operating system for humans and AI agents.**

> Agents are disposable. Memory is not.
>
> The user's knowledge must survive Fehrest itself.

---

## Status

```
ARCHITECTURE:            FROZEN
PRODUCT_IMPLEMENTATION:  NOT AUTHORIZED
HEADLESS_THESIS_PROOF:   READY_FOR_FOUNDER_AUTHORIZATION — NOT STARTED
```

**➤ [ARCHITECTURE FREEZE](docs/canonical/ARCHITECTURE_FREEZE.md) — the authoritative entry point.**

**PLANNING ONLY. NO IMPLEMENTATION EXISTS AND NONE IS AUTHORIZED.** Freeze is not authorization: the founder must explicitly authorize the Headless Rust Thesis-Proof before any code is written.

| Phase | State |
|---|---|
| F0 Discovery | ✅ Complete |
| F1 Architecture + Plan | ✅ Complete |
| F1-R1 Reconciliation | ✅ Complete — [delta](docs/reviews/F1-R1-RECONCILIATION.md) |
| G2 independent review + GPT-5.6 Sol validation | ✅ Complete — 13 VALID · 5 PARTIAL · 1 NEEDS_EVIDENCE · 0 REJECTED |
| F1-R2 Reconciliation | ✅ Complete — [delta](docs/reviews/F1-R2-RECONCILIATION.md) |
| GPT-5.6 Sol R2 delta review | ✅ Accepted with two pre-GLM corrections |
| GLM-5.3 adversarial security review | ✅ `G3_SECURITY_PASS_WITH_REQUIRED_RECONCILIATION` — CRITICAL=0, HIGH=2, MED=7, LOW=5, INFO=4 |
| G3 Security Reconciliation | ✅ Complete — [delta](docs/reviews/G3-SECURITY-RECONCILIATION.md) |
| GPT-5.6 Sol final security delta review | ✅ `G3_SECURITY_FINAL_ACCEPTED` · `SECURITY_RECONCILIATION_CLEAN` |
| **G4 Architecture Freeze** | ✅ **Complete** — [frozen architecture](docs/canonical/ARCHITECTURE_FREEZE.md) |
| Founder authorization of the Headless Rust Thesis-Proof | ⏳ **Next gate — blocking all implementation** |

**Verdict:** `G4_ARCHITECTURE_FROZEN_READY_FOR_FOUNDER_AUTHORIZATION` — see [the freeze](docs/canonical/ARCHITECTURE_FREEZE.md) and [the verdict](docs/VERDICT.md).

**No foundational trust assumption was found invalid.** What G3 corrected were **claims stronger than their mechanisms** — see [what Fehrest v1 does not claim](docs/02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make).

**Founder decisions recorded in F1-R2:**

```
D-1  Rust is the canonical Fehrest Core language              ACCEPTED
D-2  GitHub Spec Kit is the specification-driven workflow     ACCEPTED  (development only)
D-3  Ponytail is the implementation-minimisation discipline   ACCEPTED  (development only)
```

The desktop shell ([ADR-0011](docs/09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell)) is **deliberately not resolved by D-1** — Tauri 2 remains the leading candidate, and "the core is Rust, therefore the shell is Tauri" is an association, not an argument.

**Canonical repository:** `TheHalfMoon/Fehrest` (private, `main`, size 0). `wepld/Fehrest` is **not** canonical and receives nothing.

---

## Read in this order

**Start here if you are reviewing:**

0. [**Architecture Freeze**](docs/canonical/ARCHITECTURE_FREEZE.md) — the authoritative statement of what is frozen, what is hypothesis-gated, what is open, and why implementation is not authorized.
1. [Evidence Log](docs/research/EVIDENCE_LOG.md) — every measurement this plan rests on, with the exact commands. **Attack this first.** If a measurement is wrong, the decisions it supports are void. Its [unmeasured-quantities table](docs/research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2) lists the numbers that are *not* measurements and says so.
2. [Product Thesis](docs/00-PRODUCT-THESIS.md) — what Fehrest is, is not, and the experiment that would falsify it.
3. [Architecture Constitution](docs/01-ARCHITECTURE-CONSTITUTION.md) — 15 invariants, each with an enforcing mechanism and a detecting test. Two are amended from the founder's draft, with arguments.
4. [Failure Conditions](docs/17-FAILURE-CONDITIONS.md) — what findings would force redesign. The plan's falsifiability lives here.
5. [Open Questions](docs/16-OPEN-QUESTIONS.md) — unresolved decisions and known weaknesses, including where I most want to be attacked.

**Full package:**

| Doc | Contents |
|---|---|
| [A — Product Thesis](docs/00-PRODUCT-THESIS.md) | What Fehrest is and is not |
| [B — Architecture Constitution](docs/01-ARCHITECTURE-CONSTITUTION.md) | Non-negotiable invariants |
| [C — Threat Model](docs/02-THREAT-MODEL.md) | Assets, actors, boundaries, 21 attack paths, controls |
| [D — Canonical Data Model](docs/03-CANONICAL-DATA-MODEL.md) | Objects, identity, files, events, the editor round-trip gate |
| [E — Derived Data Model](docs/04-DERIVED-DATA-MODEL.md) | Indexes, graph boundary, rebuild semantics |
| [F — Memory Model](docs/05-MEMORY-MODEL.md) | Bitemporal semantics, promotion, supersession |
| [G — Agent Model](docs/06-AGENT-MODEL.md) | Identity, capabilities, tools, audit |
| [H — Context Compiler](docs/07-CONTEXT-COMPILER-SPEC.md) | The defining feature |
| [I — Donor Matrix](docs/08-DONOR-MATRIX.md) | USE / ADAPT / STUDY / BENCHMARK / DEFER / REJECT |
| [J — Technology Decisions](docs/09-TECHNOLOGY-DECISIONS.md) | 12 ADRs, each with a reversal condition |
| [K — Benchmark Plan](docs/10-BENCHMARK-PLAN.md) | 10 benchmarks, each deciding something |
| [L — Security Verification](docs/11-SECURITY-VERIFICATION-PLAN.md) | Static analysis, fuzzing, adversarial corpora |
| [M — Migration Model](docs/12-MIGRATION-SCHEMA-EVOLUTION.md) | Schema evolution |
| [N — Recovery Model](docs/13-RECOVERY-MODEL.md) | 17 failure scenarios |
| [O — Performance Budgets](docs/14-PERFORMANCE-BUDGETS.md) | Measurable envelopes |
| [P — Implementation Phases](docs/15-IMPLEMENTATION-PHASES.md) | 8 gated phases, CLI-first vertical slice |
| [Q — Open Questions](docs/16-OPEN-QUESTIONS.md) | Founder decisions and known weaknesses |
| [S — Engineering Method](docs/19-ENGINEERING-METHOD.md) | Spec Kit + Ponytail — how implementation proceeds after authorization |
| [T — Future Capability Gates](docs/20-FUTURE-GATES.md) | Visual/Canvas Engine · Unified Surface Test · Collaboration/CRDT · View Engine — **none authorized** |
| [**ARCHITECTURE FREEZE**](docs/canonical/ARCHITECTURE_FREEZE.md) | **What is frozen, conditional, open — and what is not authorized. Start here** |
| [G3 Security Reconciliation](docs/reviews/G3-SECURITY-RECONCILIATION.md) | The security delta |
| [Editor Gate](docs/18-EDITOR-GATE.md) | Prototype bake-off deciding the editor |
| [Failure Conditions](docs/17-FAILURE-CONDITIONS.md) | What would force redesign |
| [F1-R2 Reconciliation](docs/reviews/F1-R2-RECONCILIATION.md) | **The R2 delta — read this first** |
| [F1-R1 Reconciliation](docs/reviews/F1-R1-RECONCILIATION.md) | The R1 delta — preserved as the earlier audit trail |
| [Source Registry](docs/research/FEHREST_SOURCE_REGISTRY.md) | Every external source, pinned |
| [Evidence Log](docs/research/EVIDENCE_LOG.md) | Every measurement |
| [Verdict](docs/VERDICT.md) | Final assessment |

---

## The four layers

Fehrest answers four different questions, and each has its own layer ([A §5](docs/00-PRODUCT-THESIS.md#5-the-four-layer-architecture)):

```
Canonical Knowledge  "what exists?"
      ├─► Graph Intelligence  "what is connected?"
      └─► Event Journal       "what happened?"
                └─► Memory            "what remains true now?"
                      └─► Context Compiler  "what should this agent see?"
```

```
GRAPH INTELLIGENCE:  CORE CURRENT PRODUCT HYPOTHESIS — EXPLICITLY FALSIFIABLE
GRAPHIFY RUNTIME:    REPLACEABLE IMPLEMENTATION CANDIDATE
```

Graph Intelligence is a **core current product hypothesis**, not an axiom. If controlled continuation/retrieval benchmarks show graph-assisted understanding gives no material benefit over simpler local retrieval at acceptable cost, Fehrest **must permit redesign or removal** of it from the core hypothesis ([F-3](docs/17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)).

```
V1 TARGET WEDGE:  PROVISIONALLY_ACCEPTED_FOR_PLANNING — FOUNDER_RATIFICATION_REQUIRED
```

The v1 wedge ([A §4](docs/00-PRODUCT-THESIS.md#4-the-v1-user-wedge)) is a **planning assumption, not an approved decision**.

## The decisions most likely to be contested

1. **The editor is OPEN, decided by a prototype bake-off.** F1 concluded "BlockSuite is stale ⇒ CodeMirror 6." **R1 corrected that:** the standalone mirror is stale, but the editor is actively developed inside AFFiNE (`feat(editor)` and security commits through 2026-08-10). Candidate A = CodeMirror 6; Candidate B = the maintained `AFFiNE/blocksuite/…` subtree. [E-10.1](docs/research/EVIDENCE_LOG.md#e-101--the-evidence-f1-missed-the-affine-subtree-is-active) · [Editor Gate](docs/18-EDITOR-GATE.md) · [ADR-0002](docs/09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated)

2. **Extractor IDs are never canonical identities — on structural grounds.** F1 justified this with upstream bugs; **those bugs are fixed** and the citation is retracted. The durable argument: extractor IDs are path-derived by design (`{parent_dir}_{stem}`) and their *schemes* change across versions — upstream itself rejected an alternative because it "would rewrite every file and symbol id." Formalised as G-ID-1…G-ID-4. [E-4](docs/research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect) · [ADR-0004](docs/09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque)

3. **Retrieval is lexical-first; vectors are optional.** sqlite-vec's current release line is alpha, and the one prose-memory benchmark reported for graph retrieval shows it *tying* dense RAG. Vectors must earn inclusion by measurement. [E-12](docs/research/EVIDENCE_LOG.md#e-12--vector-store-maturity) · [ADR-0007](docs/09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional)

4. **Memory is bitemporal with deterministic resolution.** Valid time answers "what is true now"; recorded time answers "what did we believe last month." Both are needed, and neither requires an LLM. [ADR-0008](docs/09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution)

5. **Graph Intelligence runtime shape is PROVISIONAL.** F1's "100K files ≈ 90 min" was a linear extrapolation from one corpus on one machine. Withdrawn; [GI-BENCH](docs/10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) decides. [ADR-0003](docs/09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)

---

## The experiment that decides everything

> A project is worked for months by Agent A. Agent A is destroyed. Agent B receives **no chat history** — only a Fehrest-compiled context package — and must continue correctly.

Fehrest must beat raw history stuffing, BM25, dense RAG, hybrid RAG, graph-only retrieval, existing memory systems, and — the bar that actually matters — **a competent agent with ordinary file tools and no memory system at all.**

If it cannot beat that last baseline, Fehrest does not deserve to exist. Stated before any code is written. [B-7](docs/10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment)

---

## Repository note

The canonical repository is **`TheHalfMoon/Fehrest`** — private, default branch `main`, size 0, no implementation. Repository identity is **CLOSED**.

This session authenticates as a different account (`wepld`) and therefore cannot read it. The resulting 404 is an **environment access limitation**, not evidence about the repository. F1 misread that 404 as non-existence — a category error, since GitHub returns 404 rather than 403 for private repositories precisely to avoid disclosing them. Corrected in [R1-01](docs/reviews/F1-R1-RECONCILIATION.md).

`wepld/Fehrest` is **not canonical**, is not a fallback, and receives no planning work.

The planning package lives in a local git repository whose `origin` points at `TheHalfMoon/Fehrest`. **Nothing has been pushed**, pending explicit authorization. [E-0](docs/research/EVIDENCE_LOG.md#e-0--canonical-repository-state) · [Q-1](docs/16-OPEN-QUESTIONS.md#q-1--repository-identity-closed)

---

## License

Undecided — see [Q-1a](docs/16-OPEN-QUESTIONS.md#q-1--repository-identity-closed). Donor obligations (Apache-2.0 from Graphify, MIT from others) are compatible with either MIT or Apache-2.0 for Fehrest. This is a **separate question from repository identity** and must not be conflated with it.
