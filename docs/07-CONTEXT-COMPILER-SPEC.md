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
| **Provenance-linked** | Every item cites its source | [I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance), [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) |
| **Deterministic** | Same inputs → same output | Auditability; without it replay is impossible |
| **Composition-auditable** | What was served is recorded **permanently**, unconditionally | [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) property 1; §3.2 |
| **Content-reconstructable — while sources survive** | Item content is recomputable **only while its cited source revisions exist**; otherwise replay reports why not | [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) property 2; §3.3 |

> **The F1 "Reproducible" property is split and narrowed in F1-R2 ([R2-01](reviews/F1-R2-RECONCILIATION.md)).** "Recomputable later from canonical state" was unsatisfiable as an unconditional claim: a user editing a source, T2 compaction, or a compiler-version change each break it, and all three are normal permitted operations. The permanent guarantee is now *what was served*; the conditional guarantee is *what it said*.

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
    "permitted_actions":[ ... ],
    "pending_advisory": [ ... ]
  },
  "manifest_ref": "0198f5...",
  "omitted": {
    "reason": "budget",
    "counts": { "evidence": 42, "recent_events": 118 },
    "next_cursor": "0198..."
  },
  "provenance": { "every_item_cites": true, "unsourced_items": 0 }
}
```

### 3.1 Design choices that matter

**`canonical_high_water_mark`** records the event sequence number the package was compiled against. It is what makes a failed reproduction *explainable* — "canonical state advanced from 14827 to 15022" — rather than mysterious. Without it, [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) verification produces unattributable mismatches.

**`omitted` is mandatory and never empty when truncation occurred.** A compiler that silently drops content produces confidently wrong agents. The agent must be able to know that 118 recent events existed and 12 were shown. Hiding truncation is the single most dangerous thing a context compiler can do, because the agent cannot detect the absence.

**`superseded_decisions` is a first-class section, not an afterthought.** The superseded decision is frequently what explains the current one — "React was chosen in January, reversed in June because of X." Omitting it keeps the conclusion and destroys the reasoning.

**`contradictions` is a section rather than an error.** When [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution) cannot deterministically resolve a conflict, the conflict is passed through explicitly. The agent is told "these two memories conflict and Fehrest cannot decide," which is strictly more useful than a silent coin-flip.

**`permitted_actions`** tells the agent what it may do, sourced from its grant. This prevents the failure where an agent plans work it is not authorised to perform. **`PENDING` memories never appear here** ([F §5.5](05-MEMORY-MODEL.md#55-pending-confirmation-semantics)).

**`pending_advisory` is a non-authoritative section, added in F1-R2 ([R2-06](reviews/F1-R2-RECONCILIATION.md)).** It carries memory candidates awaiting confirmation, each labelled with its proposed type and scope and with `authority="none"` reinforced at the item level. Its contract:

- It is **never** merged into `active_constraints`, `current_decisions`, `project_state` or `permitted_actions`.
- Its items may cause an agent to **ask, abstain, or request human confirmation**. They may never cause an agent to proceed differently on its own authority.
- It is budgeted **after** every authoritative section and is the first to be truncated, with the omission recorded as usual.

The section exists because both alternatives are worse: promoting unconfirmed candidates into authoritative sections is memory poisoning by default, and hiding them entirely means an agent can violate a constraint the user has already stated but not yet confirmed.

### 3.2 The served-item manifest — permanent, T1

> **ADDED IN F1-R2 ([R2-01](reviews/F1-R2-RECONCILIATION.md)).** F1 recorded `context/compiled` with *inputs plus a digest* and claimed the package was recoverable by recomputation. A digest proves a later recomputation matched; **it cannot say what was in the package when the match fails** — and once a source has changed or T2 detail has been compacted, the match is expected to fail. The audit question "what did this session actually see?" therefore had no durable answer, which also left [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) unimplementable ([R2-02](reviews/F1-R2-RECONCILIATION.md)).

Every compiled package writes a **canonical T1 manifest** enumerating the logical items it served. It is written at emission, is never compacted, and is never derived — it is the audit record.

**Package-level fields:**

```
context_id · compiler_version · manifest_schema_version
principal (session id) · agent id · grant_snapshot_digest
request_digest (scope, question, budget, include set, as_of)
compiled_at · canonical_high_water_mark
source_high_water_marks (per plane: object index, event seq, memory seq)
package_digest
```

**Per served item:**

```
item_ordinal          # position within its section; part of what was served
section
kind                  # object | memory | event | excerpt | contradiction | advisory
subject_id            # object / memory / event identity
source_revision       # where the source carries one
source_content_hash   # hash of the source bytes the item was drawn from
rendered_hash         # hash of the exact fragment emitted
trust_level           # G section 4, never absent
basis / verification / lifecycle / resolution   # F section 3.3, all four axes
scope_snapshot        # the selector under which it qualified
```

**Field names are not frozen here.** They are stated to fix the *required information*; exact naming reconciles against the event and memory schema conventions in [D §5.3](03-CANONICAL-DATA-MODEL.md#53-event-record) when those are implemented.

**What the manifest deliberately does not contain: the item bodies.** Storing every package body means storing the vault repeatedly, and F1's objection to that stands. The manifest records *identity, position, and two hashes* per item — enough to prove exactly what was served and to detect any later divergence, at a small constant cost per item. **Storing complete package bodies is not adopted, and may only be adopted if a storage-and-forensics analysis shows it to be the smallest correct design** ([Q-15](16-OPEN-QUESTIONS.md)).

### 3.3 Replay outcomes are explicit — three results, never two

A historical package is replayed by recompiling from the manifest's recorded inputs. The result is **always one of three named outcomes**, and a mismatch is never reported as a success:

| Outcome | Meaning | Reported detail |
|---|---|---|
| `IDENTICAL` | Recompilation reproduced every item and the package digest | — |
| `DIVERGED` | Recompilation succeeded but produced a different result | **Reason** — e.g. `canonical_state_advanced` (with the high-water marks then and now), `compiler_version_changed`, `grant_changed`, `ranking_changed` — plus the per-item diff against the manifest |
| `UNRECONSTRUCTABLE` | Recompilation could not be attempted or completed | **Reason** — e.g. `source_revision_no_longer_retained`, `t2_detail_compacted`, `source_object_deleted`, `upcaster_absent` |

**In all three cases the manifest still answers the audit question**, because the manifest is not the thing being recomputed. `UNRECONSTRUCTABLE` means "we can no longer show you the exact text"; it never means "we no longer know what was served."

**Test.** `test_context_package_replay` asserts the reported outcome and reason are correct, including deliberately induced `DIVERGED` and `UNRECONSTRUCTABLE` cases. A build in which a divergent replay reports `IDENTICAL` fails.

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
[10] ASSEMBLE            envelope, provenance, digests, MANIFEST, events
```

### 4.1 Stage notes

**[0] Authorize before anything.** No retrieval occurs before the grant is frozen. This ordering *is* the injection boundary ([T-1](02-THREAT-MODEL.md#t-1--indirect-prompt-injection-via-imported-document)).

**[1] Seed** — exact identity lookups and structured property queries first. These are free, exact, and high-precision. Starting with search when you have an ID is a waste.

**[2] State resolution** — deterministic bitemporal resolution ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)). No scoring, no ranking, no model.

**[3] Lexical** — FTS5/BM25 is the baseline, not a fallback. It requires no model, no embedding, and is the floor everything else must beat ([E-8](research/EVIDENCE_LOG.md#e-8--graphifys-self-reported-retrieval-benchmarks)).

**[4] Graph expansion** — bounded by hop count (default 2), fan-out per node, and total node budget. Unbounded expansion on a hub node ("god node") pulls in the whole vault; the caps are mandatory, not tuning. Scope is enforced *during* traversal ([T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval)). Degrades to a no-op if the graph is absent ([E §8](04-DERIVED-DATA-MODEL.md#9-failure-and-degradation)).

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
| 12 | `pending_advisory` | **Non-authoritative** — must never displace anything that is |

Constraints and gotchas outrank raw evidence deliberately: one line of "never require cloud infrastructure" or "approach X fails because Y" is worth more than a page of source excerpt, and these are precisely the two categories a chat-history-stuffing baseline loses.

`pending_advisory` sits last on purpose: unconfirmed material is worth showing when there is room and must never crowd out confirmed state. It has no floor — it is the one section permitted to be starved entirely.

Each other section has a floor (never fully starved) and a cap (cannot crowd out others). Within a section, truncation is by rank, and the count omitted is always recorded. **Stage [10] then writes the served-item manifest (§3.2) from exactly what survived budgeting** — the manifest records what was *emitted*, never what was *selected*.

---

## 5. Determinism

Guaranteed by: fixed stage order; deterministic tie-breaking on every ranked list (score, then `recorded_at`, then id — never insertion order); no wall-clock reads inside the pipeline (`compiled_at` is captured once at entry); no set/hashmap iteration order dependencies; no parallel non-determinism in ranking; explicit `compiler_version` in the digest.

`input_digest` covers the request plus the canonical high-water mark. `output_digest` covers the assembled package. Together they make `test_context_package_replay` meaningful: identical inputs and unchanged canonical state must yield an identical output digest.

**Known determinism hazards, named because reviewers will look for them:** FTS5 ranking ties, floating-point score summation order in RRF, and tokenizer version drift. The latter two are addressed by fixed-order accumulation and by pinning the tokenizer in the budget spec.

> **The FTS5 hazard is not addressed by tie-breaking, and F1-R2 stops claiming that it is ([R2-14](reviews/F1-R2-RECONCILIATION.md)).** Explicit tie-breaking makes the compiler's *use* of a candidate list deterministic. It does nothing about the prior question: **whether FTS5 produces the same candidate set and the same relative ranking for a logically identical corpus reached by different write histories.** An index built by heavy incremental `insert`/`update`/`delete`/`replace` and an index built fresh from the same final corpus are not guaranteed by SQLite to rank identically, and `output_digest` — which is load-bearing for replay and audit — sits directly downstream of that ranking.
>
> This is now an **empirical gate, not an assumption**: [B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability) measures it early, before the digest is depended upon. Candidate remedies (a different FTS5 table configuration, using FTS purely for candidate generation with a Fehrest-owned deterministic rerank, or another minimal measured approach) are **not chosen here** — the benchmark chooses.

---

## 6. Optional AI stages

Strictly optional, strictly after the deterministic pipeline, and individually disableable:

| Stage | Effect | If disabled |
|---|---|---|
| Query expansion | More recall in [3] | Fewer paraphrase matches |
| Semantic reranking | Better precision after [6] | RRF order stands |
| Excerpt compression | More content per token | Excerpts truncate instead |
| Section summarisation | Denser sections | Items listed verbatim |

Rules: an AI stage may **reorder or compress** but never **introduce** content; anything an AI stage produces carries `basis: INFERRED` ([F §3.3](05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model)) and the model id, and is recorded as such in the manifest; the deterministic package is always recoverable by disabling the stages; and with all stages off the compiler must still pass every acceptance test — only quality metrics move.

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

pending_advisory (1)  — NOT AUTHORITATIVE, awaiting confirmation
  · [proposed constraint, unconfirmed] "Vector search must stay opt-in per vault."
    [memory 0198…, PENDING, AGENT_ASSERTED, UNVERIFIED, scope: project]
    → may justify asking the user; may not be treated as a constraint

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
| Determinism cannot be achieved (unstable digests on unchanged input) | Replay and audit are impossible; [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) fails |
| **FTS5 ranking is not stable across rebuild histories** ([B-12](10-BENCHMARK-PLAN.md#b-12--fts5-rebuild-and-ranking-stability)) | The digest cannot rest on engine-internal ranking. Remedy chosen by measurement, not now |
| **The manifest's per-item cost is unaffordable at realistic volume** ([R2-12](reviews/F1-R2-RECONCILIATION.md)) | Reduce what is recorded per item — never what is recorded per *package*. Dropping the manifest re-breaks [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) |
| p95 latency exceeds budget by > 2× at 10K files | Compiler unusable interactively; pre-computation or caching becomes mandatory |
| Graph expansion contributes no measurable gain over FTS + memory | Drop stage [4]; the Graphify dependency loses most of its justification |
| Agents systematically ignore the `authority="none"` envelope | Envelope was never a boundary (already stated); confirms structural controls must carry the full load |
| Budget allocation priorities are wrong — agents fail from omitted sections | Re-derive priorities empirically from failure analysis |
