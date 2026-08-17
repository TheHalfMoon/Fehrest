# H. Context Compiler Specification

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

The context compiler is Fehrest's defining feature. If it works, Fehrest is justified; if it does not beat a competent agent with plain file tools, nothing else in this plan matters ([B-7](10-BENCHMARK-PLAN.md)).

---

## 1. Contract

> Given a scope, an optional question, and a token budget, produce a **bounded, provenance-linked, deterministic, reproducible** evidence package sufficient for a fresh agent with no prior history to continue the work correctly.

Four properties are non-negotiable:

| Property | Meaning | Why |
|---|---|---|
| **Bounded** | Never exceeds the budget | An unbounded compiler is just history-stuffing with extra steps |
| **Provenance-linked** | Every item cites its source | [I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance), [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable) |
| **Deterministic** | Same inputs → same output | Auditability; without it replay is impossible |
| **Reproducible** | Recomputable later from canonical state | [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable) |

**The compiler is a deterministic retrieval-and-assembly pipeline, not an LLM summarisation call.** LLM summarisation is an optional final compression stage (§6) that can be omitted entirely without changing what the package *contains*. This is the difference between a system whose output can be audited and one whose output must be trusted.

---

## 2. Interface

```
fehrest context <scope> [--question Q] [--budget N] [--as-of T] [--format json|md]
```

```json
{
  "scope":    { "kind": "project", "id": "0198..." },
  "question": "Why did we move off React?",
  "budget":   { "max_tokens": 32000, "tokenizer": "cl100k_base" },
  "as_of":    { "valid": "now", "recorded": "now" },
  "include":  ["state","constraints","decisions","procedures","gotchas",
               "entities","open_work","evidence","contradictions"],
  "session":  "0198f3a0-..."
}
```

`session` is required: the grant attached to it determines what is visible, and it is checked before any retrieval begins ([G §2](06-AGENT-MODEL.md#2-capabilities)).

`budget.tokenizer` is explicit because token counts are tokenizer-specific. A budget without a named tokenizer is not a budget.

---

## 3. Output

```json
{
  "package_id": "0198f4...",
  "compiled_at": "2026-08-17T14:05:00Z",
  "canonical_high_water_mark": 14827,
  "compiler_version": "1.0.0",
  "input_digest": "sha256:...",
  "output_digest": "sha256:...",
  "budget": { "max_tokens": 32000, "used_tokens": 28411 },
  "sections": {
    "project_state":    [ ... ],
    "active_constraints":[ ... ],
    "current_decisions":[ ... ],
    "superseded_decisions":[ ... ],
    "procedures":       [ ... ],
    "gotchas":          [ ... ],
    "key_entities":     [ ... ],
    "recent_events":    [ ... ],
    "open_work":        [ ... ],
    "evidence":         [ ... ],
    "contradictions":   [ ... ],
    "permitted_actions":[ ... ]
  },
  "omitted": {
    "reason": "budget",
    "counts": { "evidence": 42, "recent_events": 118 },
    "next_cursor": "0198..."
  },
  "provenance": { "every_item_cites": true, "unsourced_items": 0 }
}
```

### 3.1 Design choices that matter

**`canonical_high_water_mark`** records the event sequence number the package was compiled against. It is what makes a failed reproduction *explainable* — "canonical state advanced from 14827 to 15022" — rather than mysterious. Without it, [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable) verification produces unattributable mismatches.

**`omitted` is mandatory and never empty when truncation occurred.** A compiler that silently drops content produces confidently wrong agents. The agent must be able to know that 118 recent events existed and 12 were shown. Hiding truncation is the single most dangerous thing a context compiler can do, because the agent cannot detect the absence.

**`superseded_decisions` is a first-class section, not an afterthought.** The superseded decision is frequently what explains the current one — "React was chosen in January, reversed in June because of X." Omitting it keeps the conclusion and destroys the reasoning.

**`contradictions` is a section rather than an error.** When [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution) cannot deterministically resolve a conflict, the conflict is passed through explicitly. The agent is told "these two memories conflict and Fehrest cannot decide," which is strictly more useful than a silent coin-flip.

**`permitted_actions`** tells the agent what it may do, sourced from its grant. This prevents the failure where an agent plans work it is not authorised to perform.

---

## 4. Pipeline

Ten deterministic stages. Every stage is individually testable and none requires a model.

```
[0] AUTHORIZE            resolve grant; freeze permitted scopes      (fail closed)
[1] SEED                 identity + structured lookup
[2] STATE RESOLUTION     bitemporal resolve for scope subjects
[3] LEXICAL RETRIEVAL    FTS5/BM25 over objects + memory statements
[4] GRAPH EXPANSION      bounded traversal from seeds
[5] VECTOR CANDIDATES    optional, only if D3 enabled
[6] FUSION               deterministic RRF over ranked lists
[7] TEMPORAL FILTER      drop invalid-at-as_of; classify superseded
[8] SCOPE ASSERTION      re-verify every candidate in scope
[9] BUDGET ALLOCATION    priority-ordered fill; record omissions
[10] ASSEMBLE            envelope, provenance, digests, events
```

### 4.1 Stage notes

**[0] Authorize before anything.** No retrieval occurs before the grant is frozen. This ordering *is* the injection boundary ([T-1](02-THREAT-MODEL.md#t-1--indirect-prompt-injection-via-imported-document)).

**[1] Seed** — exact identity lookups and structured property queries first. These are free, exact, and high-precision. Starting with search when you have an ID is a waste.

**[2] State resolution** — deterministic bitemporal resolution ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)). No scoring, no ranking, no model.

**[3] Lexical** — FTS5/BM25 is the baseline, not a fallback. It requires no model, no embedding, and is the floor everything else must beat ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)).

**[4] Graph expansion** — bounded by hop count (default 2), fan-out per node, and total node budget. Unbounded expansion on a hub node ("god node") pulls in the whole vault; the caps are mandatory, not tuning. Scope is enforced *during* traversal ([T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval)). Degrades to a no-op if the graph is absent ([E §8](04-DERIVED-DATA-MODEL.md#8-failure-and-degradation)).

**[5] Vectors** — optional; skipped entirely when D3 is off, with no behavioural change other than recall.

**[6] Fusion** — **Reciprocal Rank Fusion**, chosen because it is deterministic, score-scale-free, and requires no training. Score-based fusion would require normalising BM25 against cosine similarity, which is not principled. RRF's rank-only property also means adding or removing the vector list cannot destabilise the ordering of the others.

**[9] Budget allocation** is where the compiler earns or loses. Priority order:

| Priority | Section | Rationale |
|---|---|---|
| 1 | `active_constraints` | Violating a constraint is the worst failure mode |
| 2 | `project_state` | Without current state the agent works on the wrong thing |
| 3 | `current_decisions` | Prevents re-litigating settled questions |
| 4 | `gotchas` | Prevents repeating known failures — **irrecoverable knowledge** |
| 5 | `open_work` | What to do next |
| 6 | `procedures` | How to do recurring things |
| 7 | `contradictions` | Must be known if present |
| 8 | `key_entities` | Orientation |
| 9 | `superseded_decisions` | Explains the present |
| 10 | `recent_events` | Lowest density per token |
| 11 | `evidence` | Excerpts; most compressible |

Constraints and gotchas outrank raw evidence deliberately: one line of "never require cloud infrastructure" or "approach X fails because Y" is worth more than a page of source excerpt, and these are precisely the two categories a chat-history-stuffing baseline loses.

Each section has a floor (never fully starved) and a cap (cannot crowd out others). Within a section, truncation is by rank, and the count omitted is always recorded.

---

## 5. Determinism

Guaranteed by: fixed stage order; deterministic tie-breaking on every ranked list (score, then `recorded_at`, then id — never insertion order); no wall-clock reads inside the pipeline (`compiled_at` is captured once at entry); no set/hashmap iteration order dependencies; no parallel non-determinism in ranking; explicit `compiler_version` in the digest.

`input_digest` covers the request plus the canonical high-water mark. `output_digest` covers the assembled package. Together they make `test_context_package_replay` meaningful: identical inputs and unchanged canonical state must yield an identical output digest.

**Known determinism hazards, named because reviewers will look for them:** FTS5 ranking ties, floating-point score summation order in RRF, and tokenizer version drift. All three are addressed by explicit tie-breaking on stable keys, fixed-order accumulation, and pinning the tokenizer in the budget spec.

---

## 6. Optional AI stages

Strictly optional, strictly after the deterministic pipeline, and individually disableable:

| Stage | Effect | If disabled |
|---|---|---|
| Query expansion | More recall in [3] | Fewer paraphrase matches |
| Semantic reranking | Better precision after [6] | RRF order stands |
| Excerpt compression | More content per token | Excerpts truncate instead |
| Section summarisation | Denser sections | Items listed verbatim |

Rules: an AI stage may **reorder or compress** but never **introduce** content; anything an AI stage produces is marked `epistemic_status: inferred` and carries the model id; the deterministic package is always recoverable by disabling the stages; and with all stages off the compiler must still pass every acceptance test — only quality metrics move.

This is what keeps `AI OFF` a real mode rather than a degraded curiosity ([I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api)).

---

## 7. Failure behaviour

| Failure | Behaviour |
|---|---|
| Grant missing/insufficient | Fail closed. No partial package |
| Scope resolves to nothing | Empty package with explicit `reason: empty_scope` — **not** a silent fallback to vault-wide |
| Graph unavailable | Skip [4], flag `degraded: ["graph"]` in the package |
| FTS index corrupt | Fail loudly, trigger rebuild, do **not** silently return fewer results |
| Budget too small for floors | Return the highest-priority floors, set `omitted.reason: budget_insufficient` |
| Contradiction unresolvable | Include in `contradictions`; never guess |
| No memories exist | Valid package with empty memory sections; **abstention is a correct answer** |
| Tokenizer unavailable | Fail — an unbounded package is worse than no package |

The pattern: **degrade visibly or fail closed; never degrade silently.** The dangerous failure for a context compiler is not returning nothing — it is returning a plausible-looking package that quietly omits the constraint the agent was about to violate.

---

## 8. Performance budgets

Full envelopes in [O](14-PERFORMANCE-BUDGETS.md).

| Vault | p50 | p95 | Notes |
|---|---|---|---|
| 1K files | < 150 ms | < 400 ms | |
| 10K files | < 400 ms | < 1.2 s | |
| 100K files | < 1.5 s | < 4 s | Graph expansion capped |

Latency is a first-class metric because LongMemEval-V2 treats it as co-equal with accuracy ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). A compiler that needs 30 seconds will not be used, regardless of quality.

**Compression target:** ≥ 20× reduction versus raw history stuffing at equal or better task correctness ([B-7](10-BENCHMARK-PLAN.md)).

---

## 9. Worked example

**Request:** scope = project Fehrest, question = *"Should I add a vector database?"*, budget = 8000 tokens.

**Compiler output, abridged:**

```
active_constraints (2)
  · Core functionality must not require a vector database.
    [memory 0198…, constraint, user-confirmed, valid from 2026-08-17,
     source: docs/01-ARCHITECTURE-CONSTITUTION.md#I-6]
  · No LLM call on any indexing path.
    [memory 0198…, constraint, user-confirmed, source: …#R-1]

current_decisions (1)
  · Vectors are D3-optional; FTS5 is the retrieval baseline.
    [memory 0198…, decision, user-confirmed, valid from 2026-08-17,
     source: docs/04-DERIVED-DATA-MODEL.md#6]

gotchas (1)
  · sqlite-vec's current release line is v0.1.10-alpha.*; alpha status
    disqualifies it as a required component.
    [memory 0198…, gotcha, observed, evidence: E-12]

superseded_decisions (0)
contradictions (0)

evidence (3 of 27 shown; omitted for budget)
  · docs/04-DERIVED-DATA-MODEL.md §6 — "FTS5 first, measured; graph second; vectors third"
  · docs/research/EVIDENCE_LOG.md E-8 — graph ties dense RAG at 76% on LongMemEval-S (n=50)
  · docs/10-BENCHMARK-PLAN.md B-3 — vectors adopted only on measured gain

permitted_actions: context.compile, search.query, object.read, memory.add, graph.query
omitted: { reason: "budget", counts: { evidence: 24, recent_events: 61 } }
used_tokens: 6218 / 8000
```

The agent now knows the constraint, the decision, the evidence that produced it, the disqualifying fact about the candidate library, that 24 further pieces of evidence exist, and what it is allowed to do. **It did not receive a single line of chat history.** That is the product.

---

## 10. Falsification criteria

| Finding | Consequence |
|---|---|
| Compiled context does not beat a competent agent with plain file tools ([B-7](10-BENCHMARK-PLAN.md)) | **The product thesis fails.** Not a tuning problem |
| Determinism cannot be achieved (unstable digests on unchanged input) | Replay and audit are impossible; [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--agent-visible-state-is-reconstructable-and-auditable) fails |
| p95 latency exceeds budget by > 2× at 10K files | Compiler unusable interactively; pre-computation or caching becomes mandatory |
| Graph expansion contributes no measurable gain over FTS + memory | Drop stage [4]; the Graphify dependency loses most of its justification |
| Agents systematically ignore the `authority="none"` envelope | Envelope was never a boundary (already stated); confirms structural controls must carry the full load |
| Budget allocation priorities are wrong — agents fail from omitted sections | Re-derive priorities empirically from failure analysis |
