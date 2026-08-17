# Fehrest

**An open-source, local-first knowledge and long-memory operating system for humans and AI agents.**

> Agents are disposable. Memory is not.
>
> The user's knowledge must survive Fehrest itself.

---

## Status

**PLANNING ONLY. NO IMPLEMENTATION EXISTS AND NONE IS AUTHORIZED.**

This repository currently contains an architecture and implementation plan awaiting independent adversarial review. No product code has been written. The next gate is external review, not coding.

**Verdict:** `READY_FOR_ADVERSARIAL_REVIEW` — see [the final verdict](docs/VERDICT.md).

---

## Read in this order

**Start here if you are reviewing:**

1. [Evidence Log](docs/research/EVIDENCE_LOG.md) — every measurement this plan rests on, with the exact commands. **Attack this first.** If a measurement is wrong, the decisions it supports are void.
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
| [Failure Conditions](docs/17-FAILURE-CONDITIONS.md) | What would force redesign |
| [Source Registry](docs/research/FEHREST_SOURCE_REGISTRY.md) | Every external source, pinned |
| [Evidence Log](docs/research/EVIDENCE_LOG.md) | Every measurement |
| [Verdict](docs/VERDICT.md) | Final assessment |

---

## The four decisions most likely to be contested

Each is argued from measurement, not preference. Full reasoning at the links.

1. **BlockSuite is deferred, not adopted.** Its repository is a downstream mirror whose sync stopped 2025-07-07; `@blocksuite/store` has not been published in 13.5 months and sits at pre-1.0 `0.22.4`; six dependency-vulnerability branches are unmerged. Separately, the Markdown round-trip gate is *structurally* unpassable — a lossless mapping requires a sidecar that then becomes the real canonical document. v1 editing is Markdown-native on CodeMirror 6, which makes round-trip the identity function. [E-10](docs/research/EVIDENCE_LOG.md#e-10--blocksuite-is-a-stale-downstream-mirror-editor-gate) · [ADR-0002](docs/09-TECHNOLOGY-DECISIONS.md#adr-0002--v1-editing-is-markdown-native-blocksuite-is-deferred)

2. **Graphify runs as a long-lived sidecar, and its IDs are never identities.** Cold import measured at 4,451 ms, warm 276 ms — so per-call invocation is impossible and a sidecar is forced. Its node IDs are name-derived slugs with documented same-filename collisions, so Fehrest allocates its own UUIDv7 identities. [E-4](docs/research/EVIDENCE_LOG.md#e-4--graphify-node-ids-are-name-derived-not-stable-identities) · [E-6](docs/research/EVIDENCE_LOG.md#e-6--graphify-startup-cost-cold-vs-warm) · [ADR-0003](docs/09-TECHNOLOGY-DECISIONS.md#adr-0003--graphify-runs-as-a-managed-long-lived-sidecar)

3. **Retrieval is lexical-first; vectors are optional.** sqlite-vec's current release line is alpha, and the one prose-memory benchmark reported for graph retrieval shows it *tying* dense RAG. Neither approach dominates, so vectors must earn inclusion by measurement. [E-8](docs/research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks) · [E-12](docs/research/EVIDENCE_LOG.md#e-12--vector-store-maturity) · [ADR-0007](docs/09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional)

4. **Memory is bitemporal with deterministic resolution.** Valid time answers "what is true now"; recorded time answers "what did we believe last month." Both are needed, and neither requires an LLM. [ADR-0008](docs/09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution)

---

## The experiment that decides everything

> A project is worked for months by Agent A. Agent A is destroyed. Agent B receives **no chat history** — only a Fehrest-compiled context package — and must continue correctly.

Fehrest must beat raw history stuffing, BM25, dense RAG, hybrid RAG, graph-only retrieval, existing memory systems, and — the bar that actually matters — **a competent agent with ordinary file tools and no memory system at all.**

If it cannot beat that last baseline, Fehrest does not deserve to exist. Stated before any code is written. [B-7](docs/10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment)

---

## Repository note

The brief named `TheHalfMoon/Fehrest`, which **does not exist** (HTTP 404). The only reachable Fehrest repository, `wepld/Fehrest`, is **empty** — zero commits. This planning package is committed locally and pushed nowhere pending a founder decision on which remote is canonical. [E-0](docs/research/EVIDENCE_LOG.md#e-0--canonical-repository-state) · [Q-1](docs/16-OPEN-QUESTIONS.md#q-1--which-repository-is-canonical)

---

## License

Undecided — see [Q-1](docs/16-OPEN-QUESTIONS.md#q-1--which-repository-is-canonical). Donor obligations (Apache-2.0 from Graphify, MIT from others) are compatible with either MIT or Apache-2.0 for Fehrest.
