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
| An AFFiNE fork | Explicitly rejected. See [SRC-006](research/FEHREST_SOURCE_REGISTRY.md#33-affine--study-reclassified-from-adapt) |
| A RAG pipeline | RAG retrieves passages. Fehrest resolves *current state* deterministically, and can say "this decision was superseded on 3 June" |
| An agent framework | Fehrest is what agents connect *to*. It does not own the agent loop |
| A BI or analytics product | Deferred entirely ([SRC-018](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval)) |
| A Linear or Airtable clone | Structured views are a later projection over the object model, not the product |
| A vector database | Vectors are an optional, rebuildable accelerator. sqlite-vec's current release line is **alpha** ([E-12](research/EVIDENCE_LOG.md#e-12--vector-store-maturity)) |

## 4. The three-plane thesis

Evaluated in detail in [D](03-CANONICAL-DATA-MODEL.md) and [E](04-DERIVED-DATA-MODEL.md). Summarised:

| Plane | Status | Contents | Rebuildable? |
|---|---|---|---|
| **Knowledge** | Canonical | Markdown + YAML frontmatter, attachments, structured open metadata | No — this *is* the user's data |
| **Activity/Event** | Canonical | Append-only typed event records: what happened, who did it, what was shown to whom | No — history cannot be recomputed |
| **Derived** | Disposable | Graph, FTS index, embeddings, communities, extracted text, summaries, thumbnails | Yes — always, by definition |

The decomposition survives scrutiny, with one correction: **the Event Plane must be selective.** Storing every model chunk forever is what the founder's brief warns against, and the harness's own event vocabulary includes `assistant/chunk` for "token-level replay fidelity" ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)) — appropriate for a debugging runtime, wrong for a decade-long personal memory store. Fehrest splits durability tiers within the Event Plane; see [D §5](03-CANONICAL-DATA-MODEL.md#5-the-event-plane).

## 5. The defining capability: context compilation

If Fehrest has one feature that justifies it, it is this:

> Given a project, a question, and a token budget, produce a **bounded, provenance-linked, deterministic** evidence package sufficient for a fresh agent to continue the work correctly.

Not "retrieve the top 20 chunks." A compiled package: current project state, active constraints, live decisions and the superseded ones that explain them, procedures, known gotchas, open work, contradictions surfaced rather than silently resolved, and a citation for every claim.

Deterministic and reproducible is the load-bearing property. The same inputs must produce the same package, because a memory substrate that cannot be re-derived cannot be audited, and one that cannot be audited cannot be trusted with a decade of a person's thinking. LLM summarisation is an optional final stage, never the mechanism. Full specification in [H](07-CONTEXT-COMPILER-SPEC.md).

## 6. The falsification test

Fehrest's thesis is falsifiable by a single experiment, specified as [B-7](10-BENCHMARK-PLAN.md):

> Agent A works a project over a long period. Agent A is destroyed. Agent B receives **no chat history** — only a Fehrest-compiled context package — and must continue the project correctly.

Fehrest must beat: raw chat-history stuffing, BM25, dense RAG, hybrid RAG, graph-only retrieval, existing memory systems, and — the bar that actually matters — **a competent agent with ordinary file tools and no memory system at all.**

If Fehrest cannot beat the last baseline, it does not deserve to exist. That is stated here deliberately, before any code is written.

## 7. Scope commitments

**In scope for v1** (challenged item-by-item in [P](15-IMPLEMENTATION-PHASES.md)): local vault of open files, stable identity, deterministic ingestion, append-only event journal, Markdown-native editing, deterministic structural graph, lexical search, bitemporal memory with supersession, context compiler, scoped MCP gateway, provenance and audit.

**Explicitly deferred:** rich block editing, CRDT collaboration, canvas, sync, vectors, graph explorer UI, plugins, mobile, analytics, forecasting, OCR, transcription, multi-user, marketplace.

**Explicitly forbidden in v1:** mandatory cloud, hosted auth, opaque telemetry, mandatory LLM, mandatory vector DB, mandatory graph DB, unrestricted agent filesystem or network access.

## 8. Why this is buildable by a small team

The architecture deliberately buys rather than builds where the evidence supports it: deterministic code understanding comes from Graphify (60,202 lines, 28 grammars, Apache-2.0, ~18 files/s measured, zero LLM cost — [E-5](research/EVIDENCE_LOG.md#e-5--graphify-measured-extraction-throughput-and-confidence-distribution)); the event-plane design comes from a donor whose subsystem documentation is specification-grade ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)); storage is SQLite.

And it deliberately refuses to build the most expensive thing — a rich collaborative block editor — because the one candidate substrate is a 13-month-stale unreleased mirror ([E-10](research/EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate)), and because Markdown-native editing makes canonical round-trip an identity function instead of a lossy mapping ([ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--v1-editing-is-markdown-native-blocksuite-is-deferred)).

The remaining novel work — bitemporal memory, promotion, context compilation, the agent boundary — is where Fehrest's actual contribution lies, and is small enough to build correctly.

## 9. What would change this thesis

| Finding | Consequence |
|---|---|
| Context compilation cannot beat a competent agent with plain file tools ([B-7](10-BENCHMARK-PLAN.md)) | **Thesis falsified.** The product has no reason to exist |
| Deterministic promotion captures little durable value ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)) | Memory requires a model; the `AI OFF` mode degrades from "full function" to "read-only knowledge base" — a materially weaker product |
| Markdown plus sidecars proves insufficient for real knowledge work ([H-4](research/EVIDENCE_LOG.md#h-4--a-markdown-native-canonical-format-is-sufficient-for-v1-knowledge-work)) | Editor decision reopens; either a maintained rich substrate must be found or Fehrest owns one permanently |
| Users do not value local ownership enough to accept the feature cost | Thesis is technically sound but commercially wrong. Not resolvable by architecture |
