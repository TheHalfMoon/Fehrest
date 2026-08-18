# A. Product Thesis

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

---

## 1. What Fehrest is

Fehrest is an open-source, local-first knowledge and long-memory operating system for humans and AI agents.

The compressed formulation:

> Obsidian-style local ownership + deterministic structural understanding + temporal/event memory + agent context compilation.

The two governing principles:

> **Agents are disposable. Memory is not.**
>
> **The user's knowledge must survive Fehrest itself.**

## 2. The problem Fehrest exists to solve

An agent that works on a project for three months accumulates understanding: which approaches failed, which constraints are non-negotiable, which framework the project migrated *away* from, which environment quirk breaks the build. When that agent's session ends, all of it is destroyed. The next agent starts from zero, re-derives what is already known, and repeats resolved mistakes.

The industry's answer has been to make context windows larger and to bolt retrieval onto chat logs. Both treat the symptom. The disease is that **the durable artifact is the conversation rather than the knowledge**, and conversations are owned by vendors, are not inspectable, are not temporally resolved, and cannot distinguish "this was true in March" from "this is true now."

Fehrest inverts the ownership: the knowledge is a set of files on the user's disk, plus an append-only record of what happened, plus a memory layer with explicit time semantics. Agents connect to it, are granted bounded access, contribute provenance-tagged memories, and are discarded.

This is a stronger claim than "better RAG." It is that **the memory substrate should outlive every agent, every model, every vendor, and Fehrest itself.**

### 2.1 Evidence that the problem is real and measurable

This is not a speculative problem. LongMemEval-V2 (arXiv `2605.12493`) measures exactly it — 451 curated questions over 1,870 task trajectories with histories reaching 115M tokens — and defines five abilities a memory system must exhibit: static state recall, dynamic state tracking, workflow knowledge, environment gotchas, and premise awareness ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)).

Those five are the specification. Fehrest's memory model is designed against them rather than against an invented taxonomy.

The honest bar is also published there: the best reported memory system scores 72.5% against **69.3% for an off-the-shelf coding agent with ordinary tools**. The margin that justifies a memory OS is 3.2 points, not the 24 points over a RAG baseline. Fehrest must be measured against the competent-agent baseline. See [K](10-BENCHMARK-PLAN.md).

## 3. What Fehrest is not

| Fehrest is not | Because |
|---|---|
| A cloud knowledge service | Core function must work with no network, no account, no server ([B](01-ARCHITECTURE-CONSTITUTION.md)) |
| An Obsidian clone | Obsidian stores human notes. Fehrest stores human knowledge *and* machine memory in one temporally-resolved substrate, with an audited agent boundary |
| An AFFiNE fork | Explicitly rejected. See [SRC-006](research/FEHREST_SOURCE_REGISTRY.md#33-affine--study--source-of-candidate-b) |
| A RAG pipeline | RAG retrieves passages. Fehrest resolves *current state* deterministically, and can say "this decision was superseded on 3 June" |
| An agent framework | Fehrest is what agents connect *to*. It does not own the agent loop |
| A BI or analytics product | Deferred entirely ([SRC-018](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval)) |
| A Linear or Airtable clone | Structured views are a later projection over the object model, not the product |
| A vector database | Vectors are an optional, rebuildable accelerator. sqlite-vec's current release line is **alpha** ([E-12](research/EVIDENCE_LOG.md#e-12--vector-store-maturity)) |

## 4. The v1 user wedge

```
V1 TARGET WEDGE:
PROVISIONALLY_ACCEPTED_FOR_PLANNING
FOUNDER_RATIFICATION_REQUIRED
```

**Status.** This is a **planning assumption**, not a founder decision. It is adopted so that architecture work has a coherent target, and it is **not approved**. The wording below has **not** been ratified by the founder and must not be described as founder-approved anywhere in this package.

**Current planning candidate:**

> **Fehrest v1 targets power users, developers, researchers and AI-native knowledge workers who regularly use multiple agents and need durable local project memory across tools, sessions and model providers.**

This wedge is not the ceiling. It is the population for whom the unique thesis would be *provable* — people who already feel the pain of memory dying with every session, and who already run several of: Claude, Codex, Gemini, GLM, Cursor, local models, MCP tools.

**Fehrest makes memory portable across all of them.** That is the wedge's defining requirement, and no incumbent serves it: Obsidian has no agent boundary, each vendor's memory is locked to that vendor, and RAG tools have no temporal or provenance model.

**Architecture consequences — this is why the wedge matters, and why it needs ratifying:**

| Decision | Because of the wedge |
|---|---|
| MCP gateway is v1, not deferred | Multi-provider portability *is* the value proposition |
| CLI-first through Phase 6 | This user is comfortable in a terminal; UI can follow proof |
| Graph Intelligence stays in v1 | Code and structured corpora are central to this user's work |
| Local-first is a feature, not a constraint | This user has strong opinions about data ownership |
| Rich block editing is not the wedge's core need | Supports — but does not decide — the [Editor Gate](18-EDITOR-GATE.md) |

**Strongest alternative considered:** *general knowledge workers (an Obsidian-adjacent audience)*. Rejected for v1 because it would make the editor the product, demote the agent gateway, and put Fehrest in direct feature competition with mature incumbents on their strongest axis — while leaving the actual thesis (portable agent memory) untested. It remains the natural **second** market once the thesis is proven.

If this wedge is wrong — or is not ratified — the decisions that change are the four in the table above. **Founder ratification is required before any of them may be treated as settled.** Recorded in [Q-8](16-OPEN-QUESTIONS.md#q-8--v1-target-wedge-provisionally-accepted-for-planning).

## 5. The four-layer architecture

**Made explicit in F1-R1 ([R1-12](reviews/F1-R1-RECONCILIATION.md)).** Fehrest answers four different questions, and each has its own layer:

```
                    Canonical Knowledge
                    "what exists?"
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
     Graph Intelligence            Event Journal
     "what is connected?"          "what happened?"
              │                           │
              └─────────────┬─────────────┘
                            │
                  temporal interpretation
                            │
                            ▼
                         Memory
                "what remains true now?"
                            │
                            ▼
                   Context Compiler
             "what should this agent see?"
```

| Layer | Question | Donor influence |
|---|---|---|
| **Canonical Knowledge** | What exists? | Obsidian-style local ownership |
| **Graph Intelligence** | What is connected? | Graphify-style deterministic relationship extraction |
| **Event Journal** | What happened? | DeepSeek-Harness-style append-only typed events |
| **Memory** | What remains relevant and currently true? | Bitemporal + supersession |
| **Context Compiler** | What should this agent see now? | Fehrest-native |

```
GRAPH INTELLIGENCE:
CORE CURRENT PRODUCT HYPOTHESIS
EXPLICITLY FALSIFIABLE
```

**Graph Intelligence is a core *current product hypothesis*, and Graphify is a replaceable implementation of it** ([R1-06](reviews/F1-R1-RECONCILIATION.md)). The hypothesis is that lexical search alone cannot answer "what is connected," and that answering it materially improves agent continuation.

**That hypothesis is testable and may fail.** If controlled continuation and retrieval benchmarks show graph-assisted understanding does not deliver a material benefit over simpler local retrieval at acceptable cost, Fehrest **must permit redesign or removal of Graph Intelligence from the core product hypothesis** ([F-3](17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost)).

Two failure modes are distinguished, because they have different consequences:
- **The implementation underperforms** → replace Graphify ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)).
- **The capability itself does not earn its cost** → redesign or remove it from the core hypothesis, and revise this thesis accordingly.

The Event Journal is equally first-class. Knowledge without activity history cannot answer "why is this the current decision," and memory without events has no provenance to resolve conflicts against ([D §5](03-CANONICAL-DATA-MODEL.md#5-the-event-plane)).

## 6. The three-plane storage thesis

Evaluated in detail in [D](03-CANONICAL-DATA-MODEL.md) and [E](04-DERIVED-DATA-MODEL.md). Summarised:

| Plane | Status | Contents | Rebuildable? |
|---|---|---|---|
| **Knowledge** | Canonical | Markdown + YAML frontmatter, attachments, structured open metadata | No — this *is* the user's data |
| **Activity/Event** | Canonical | Append-only typed event records: what happened, who did it, what was shown to whom | No — history cannot be recomputed |
| **Derived** | Disposable | Graph, FTS index, embeddings, communities, extracted text, summaries, thumbnails | Yes — always, by definition |

The decomposition survives scrutiny, with one correction: **the Event Plane must be selective.** Storing every model chunk forever is what the founder's brief warns against, and the harness's own event vocabulary includes `assistant/chunk` for "token-level replay fidelity" ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)) — appropriate for a debugging runtime, wrong for a decade-long personal memory store. Fehrest splits durability tiers within the Event Plane; see [D §5](03-CANONICAL-DATA-MODEL.md#5-the-event-plane).

## 7. The defining capability: context compilation

If Fehrest has one feature that justifies it, it is this:

> Given a project, a question, and a token budget, produce a **bounded, provenance-linked, deterministic** evidence package sufficient for a fresh agent to continue the work correctly.

Not "retrieve the top 20 chunks." A compiled package: current project state, active constraints, live decisions and the superseded ones that explain them, procedures, known gotchas, open work, contradictions surfaced rather than silently resolved, and a citation for every claim.

Deterministic and reproducible is the load-bearing property. The same inputs must produce the same package, because a memory substrate that cannot be re-derived cannot be audited, and one that cannot be audited cannot be trusted with a decade of a person's thinking. LLM summarisation is an optional final stage, never the mechanism. Full specification in [H](07-CONTEXT-COMPILER-SPEC.md).

## 8. The falsification test

Fehrest's thesis is falsifiable by a single experiment, specified as [B-7](10-BENCHMARK-PLAN.md):

> Agent A works a project over a long period. Agent A is destroyed. Agent B receives **no chat history** — only a Fehrest-compiled context package — and must continue the project correctly.

Fehrest must beat: raw chat-history stuffing, BM25, dense RAG, hybrid RAG, graph-only retrieval, existing memory systems, **a maintained Karpathy-style LLM Wiki**, and — the bar that actually matters — **a competent agent with ordinary file tools and no memory system at all.**

If Fehrest cannot beat the last baseline, it does not deserve to exist. That is stated here deliberately, before any code is written.

### 8.1 The maintained-wiki baseline, and what it demands *(added in F1-R2)*

> **RAG repeatedly reconstructs understanding from raw sources on every query. A maintained LLM Wiki instead creates a persistent, interlinked knowledge artifact that compounds over time** ([SRC-101](research/FEHREST_SOURCE_REGISTRY.md#82-andrej-karpathy--llm-wiki)).

That second pattern is a far closer relative of Fehrest's thesis than any RAG variant — and it needs **no system at all**: raw sources, a maintained Markdown wiki, explicit links, and an ordinary agent that can search and read.

Adding it to the baseline ladder ([K §3.1](10-BENCHMARK-PLAN.md#31-the-baseline-ladder)) sharpens the claim this document is making. Fehrest is not claiming that *having durable, linked, maintained knowledge* helps an agent — a directory of Markdown files already delivers that. **Fehrest is claiming that the following add measurable value on top of it:**

| Claim | Why a maintained wiki cannot supply it |
|---|---|
| **Temporal state** | A wiki says what is written now. It cannot answer "what was true in March" |
| **Supersession** | A wiki edit destroys the reasoning and keeps the conclusion |
| **Provenance** | A wiki page is authored, not sourced; nothing links a claim to the evidence that produced it |
| **Deterministic context compilation** | A wiki is read by search and judgement, not compiled to a bounded, reproducible, budgeted package |
| **The agent experience** | A wiki has no capability boundary, no audit, and no record of what any agent was shown |
| **Graph intelligence** *(optional, falsifiable)* | A wiki's links are the ones a human remembered to write |

**Beating a plain agent while merely tying a maintained wiki would be a real result with an uncomfortable reading**: that the value is in *having a maintained artifact*, not in Fehrest's architecture — a materially smaller product than the one this document describes. That is why the baseline is in the ladder rather than left out of it.

**No endorsement is claimed or implied.** Karpathy has not endorsed Fehrest, Graphify, or Graph Intelligence, and no such endorsement is established. The pattern is used as a baseline and a framing — as something to beat and to think with — never as an authority.

## 9. Scope commitments

**In scope for v1** (challenged item-by-item in [P](15-IMPLEMENTATION-PHASES.md)): local vault of open files, stable identity, deterministic ingestion, append-only event journal, Markdown-native editing, deterministic structural graph, lexical search, bitemporal memory with supersession, context compiler, scoped MCP gateway, provenance and audit.

**Explicitly deferred:** rich block editing, CRDT collaboration, canvas, sync, vectors, graph explorer UI, plugins, mobile, analytics, forecasting, OCR, transcription, multi-user, marketplace.

**Explicitly forbidden in v1:** mandatory cloud, hosted auth, opaque telemetry, mandatory LLM, mandatory vector DB, mandatory graph DB, unrestricted agent filesystem or network access, **a mandatory Python runtime** ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)), **and a mandatory graphical interface** ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)).

**Implementation language: Rust** ([ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language), founder decision D-1). The Core owns every correctness- and security-sensitive semantic; TypeScript/React is presentation only; Python sits behind an optional process boundary.

## 10. Why this is buildable by a small team

The architecture deliberately buys rather than builds where the evidence supports it: deterministic code understanding comes from Graphify (60,202 lines, 28 grammars, Apache-2.0, ~18 files/s measured, zero LLM cost — [E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-preliminary)); the event-plane design comes from a donor whose subsystem documentation is specification-grade ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)); storage is SQLite.

And it deliberately refuses to build the most expensive thing — a rich collaborative block editor — because the one candidate substrate is a 13-month-stale unreleased mirror ([E-10](research/EVIDENCE_LOG.md#e-10--blocksuite-distribution-is-stale-the-implementation-is-not-editor-gate)), and because Markdown-native editing makes canonical round-trip an identity function instead of a lossy mapping ([ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated)).

The remaining novel work — bitemporal memory, promotion, context compilation, the agent boundary — is where Fehrest's actual contribution lies, and is small enough to build correctly.

## 11. What would change this thesis

| Finding | Consequence |
|---|---|
| Context compilation cannot beat a competent agent with plain file tools ([B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark)) | **Thesis falsified.** The product has no reason to exist. Indicated early by [B-7a](10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) at [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice); **only the powered study may fire it** |
| Fehrest beats a plain agent but only ties a maintained LLM Wiki ([§8.1](#81-the-maintained-wiki-baseline-and-what-it-demands-added-in-f1-r2)) | The value is in *having a maintained artifact*, not in temporal state, supersession, provenance or compilation. A **materially smaller product**; this thesis is restated, not defended |
| Deterministic promotion captures little durable value ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)) | Memory requires a model; the `AI OFF` mode degrades from "full function" to "read-only knowledge base" — a materially weaker product |
| Markdown plus sidecars proves insufficient for real knowledge work ([H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work)) | Editor decision reopens; either a maintained rich substrate must be found or Fehrest owns one permanently |
| Users do not value local ownership enough to accept the feature cost | Thesis is technically sound but commercially wrong. Not resolvable by architecture |
