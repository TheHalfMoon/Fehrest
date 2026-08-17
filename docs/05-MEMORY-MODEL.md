# F. Memory Model

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

---

## 1. What the memory model must represent

The specification is taken from LongMemEval-V2 rather than invented, because it is externally defined and measurable ([E-14](research/EVIDENCE_LOG.md#e-14--longmemeval-v2-exists-and-defines-the-right-target)). Its five measured abilities map directly onto structural requirements:

| Measured ability | What it requires structurally |
|---|---|
| **Static state recall** | Durable facts with stable identity |
| **Dynamic state tracking** | **Bitemporality** — the same subject holding different values over time, resolvable to "now" |
| **Workflow knowledge** | A first-class **procedure** type with ordered steps |
| **Environment gotchas** | A first-class **negative-knowledge** type — failed approaches and traps |
| **Premise awareness** | **Scope-bounded validity** — a fact true in project A, wrong in project B |

The last two are the ones memory systems usually omit, and they are where a memory OS earns its margin. "Approach X fails for reason Y" and "this constraint applies only here" are exactly the knowledge that dies with an agent session and cannot be re-derived from source files.

The honest bar from the same source: the best reported system scores 72.5% against **69.3% for an off-the-shelf coding agent with ordinary tools**. Fehrest is measured against that 69.3%, not against the 48.5% RAG baseline ([K](10-BENCHMARK-PLAN.md)).

---

## 2. Why memory is a separate primitive

Memory is not `type: memory` on an Object ([D §1](03-CANONICAL-DATA-MODEL.md#1-the-object-model-decision)) because it has lifecycle semantics documents do not:

- **Bitemporal validity.** Every memory has *when it was true* and *when Fehrest learned it*. Notes have neither.
- **Supersession.** A memory can be replaced while remaining retained and queryable. Notes are edited in place.
- **Assertion, not authorship.** A memory is a claim by an identified actor from identified evidence. A note is content.
- **Deterministic current-state resolution.** Given contradictory memories, exactly one must win by rule. Notes have no such requirement.

Forcing these onto Objects would put `valid_from`/`valid_until`/`supersedes`/`confidence` in every note's frontmatter — wrong for notes and expensive for everything.

---

## 3. The memory record

```json
{
  "id": "0198f2b7-...",                    // UUIDv7, immutable
  "statement": "The project migrated from React to SolidJS.",
  "payload": { "subject": "0198...", "predicate": "uses_framework", "object": "SolidJS" },
  "memory_type": "fact",
  "epistemic_status": "asserted",
  "actor": { "kind": "agent", "id": "agent:claude", "session": "0198..." },
  "evidence": [
    { "kind": "object", "id": "0198...", "locator": "L42-48", "content_hash": "sha256:..." },
    { "kind": "event",  "id": "0198..." }
  ],
  "recorded_at": "2026-08-17T14:22:03Z",   // system-assigned, NEVER actor-supplied
  "valid_from":  "2026-06-03T00:00:00Z",   // actor-supplied, validated
  "valid_until": null,                      // null = still valid
  "confidence": 0.85,
  "status": "active",
  "scope": { "kind": "project", "id": "0198..." },
  "supersedes": ["0198f2b0-..."],
  "provenance": { "mechanism": "rule:decision-extractor", "mechanism_version": "1.2.0" }
}
```

### 3.1 Field semantics that carry weight

**`statement` and `payload` both exist.** `statement` is the human- and model-readable form; `payload` is the machine-resolvable triple. Structured resolution needs the triple (to know that two memories are about the same subject/predicate and therefore conflict); humans and models need the sentence. Storing only one forces either lossy parsing or unresolvable conflicts. `payload` is optional — not every useful memory is a clean triple, and refusing those would discard most gotchas.

**`recorded_at` is system-assigned.** This is a security property, not a convenience: it is what makes backdating impossible ([T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse)).

**`valid_from` is actor-supplied but validated.** A `valid_from` earlier than the earliest evidence timestamp is flagged. It cannot be forbidden — a user legitimately records in August that a decision was made in June — so the control is visibility, not prohibition.

**`confidence` is a number, and this is a known weakness.** Numeric confidence from an LLM is not calibrated, and reviewers should treat it as an ordering hint only. Fehrest therefore **never uses `confidence` alone to resolve a conflict** — resolution is by the deterministic rules in §4, with confidence only as a final tiebreak. See [Q-6](16-OPEN-QUESTIONS.md).

**`status`** ∈ `active | superseded | rejected | retracted | expired`. Superseded and rejected memories are **retained, never deleted** — this is what makes memory substitution visible ([T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse)) and what lets the compiler explain *why* the current answer is current.

### 3.2 Memory types

| Type | Holds | LME-V2 ability | Promotion |
|---|---|---|---|
| `fact` | Objective state | static recall, dynamic tracking | rule or model |
| `preference` | User preference | — | **human-confirmed** |
| `decision` | A choice and its rationale | dynamic tracking | **human-confirmed** |
| `constraint` | A non-negotiable rule | premise awareness | **human-confirmed** |
| `procedure` | Ordered steps for a recurring task | **workflow knowledge** | rule or model |
| `gotcha` | Failed approach, trap, recurring failure mode | **environment gotchas** | rule or model |
| `relationship` | Typed link between entities | static recall | rule |
| `episodic` | "On 3 June, X happened" | dynamic tracking | rule |
| `semantic` | Generalised knowledge | static recall | model-assisted |
| `state` | Current project/task state | dynamic tracking | rule |

`gotcha` and `procedure` are first-class rather than tags because they answer two of the five measured abilities and because they are the memory kinds with the highest value-per-byte: they encode work that cannot be recovered by re-reading the repository.

The three types that most strongly steer future agent behaviour — `preference`, `decision`, `constraint` — require human confirmation, because those are exactly the targets of memory poisoning ([T-2](02-THREAT-MODEL.md#t-2--memory-poisoning)).

### 3.3 The Fehrest evidence and trust model

> **DEFINED NATIVELY IN F1-R1 ([R1-08](reviews/F1-R1-RECONCILIATION.md)).** F1's four-value `epistemic_status` was serviceable but partly shaped by an extractor's vocabulary. **Extractor confidence labels must map into Fehrest's model, never define it** — a label distribution observed on one corpus (`AMBIGUOUS` at 0.0%) says nothing about ambiguity in general.

**Eight states**, event-sourced per [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended):

| State | Meaning | Reachable by |
|---|---|---|
| `EXTRACTED` | Deterministically derived from a primary source Fehrest itself parsed | Deterministic extraction only |
| `ASSERTED` | An identified actor claims it | Any actor, including agents |
| `INFERRED` | Derived by a mechanism from other memories | Rules or models |
| `USER_CONFIRMED` | A human explicitly affirmed it | The user only |
| `AGENT_CONFIRMED` | An agent affirmed it from independent evidence | Agents, with a second evidence link |
| `CONFLICTED` | Contradicts another active memory; resolution failed | Contradiction detection |
| `SUPERSEDED` | Replaced by a later memory; retained | Supersession |
| `UNRESOLVED` | Recorded but its evidence does not currently resolve | Imports, broken anchors, degraded cases |

**Permitted transitions** — anything not listed is forbidden, and every transition emits an event:

```
ASSERTED   → USER_CONFIRMED     (human affirmation)
ASSERTED   → AGENT_CONFIRMED    (independent corroborating evidence)
ASSERTED   → CONFLICTED         (contradiction detected)
INFERRED   → ASSERTED           (an actor adopts the inference as a claim)
INFERRED   → CONFLICTED
EXTRACTED  → CONFLICTED         (source changed or contradicts)
EXTRACTED  → UNRESOLVED         (source deleted or anchor broken)
CONFLICTED → USER_CONFIRMED     (human resolves in this memory's favour)
CONFLICTED → SUPERSEDED         (resolved against it)
any        → SUPERSEDED         (a later memory replaces it)
any        → UNRESOLVED         (evidence stops resolving)
```

**Three rules that make this a boundary rather than a label:**

1. **No upward transition without new evidence or a human.** `ASSERTED → USER_CONFIRMED` requires a human event; `→ AGENT_CONFIRMED` requires a *second, independent* evidence link. An agent cannot confirm its own assertion.
2. **`EXTRACTED` is not reachable by any agent.** Only Fehrest's own deterministic parsing produces it. An agent asserting "I read this in the file" produces `ASSERTED`, not `EXTRACTED` — the distinction between *Fehrest parsed it* and *something told us it parsed it* is exactly the boundary [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) attacks.
3. **`CONFLICTED` is a first-class resting state, not an error.** A memory may sit conflicted indefinitely. Forcing resolution is how a memory system starts inventing answers.

**Mapping extractor labels in** — one-way, at ingestion:

| Extractor label | Fehrest state |
|---|---|
| `EXTRACTED` | `EXTRACTED` |
| `INFERRED` | `INFERRED` |
| `AMBIGUOUS` | `UNRESOLVED` |
| *(unrecognised label)* | `UNRESOLVED` |

The last row matters: an unknown label from a future or different extractor degrades to `UNRESOLVED` rather than being trusted or dropped. This is what lets the extractor be replaced ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)) without touching the trust model.

---

## 4. Bitemporality

**Recommendation: adopt bitemporal semantics. This is the single most defensible technical decision in the plan.**

Two independent axes:

- **Valid time** (`valid_from`, `valid_until`) — when the fact was true in the world.
- **Recorded time** (`recorded_at`) — when Fehrest learned it.

### 4.1 The motivating case, worked

The brief's example: a project used React, then moved to SolidJS. A retrieval system without valid time surfaces both and asks the model to guess.

```
M1: uses_framework = React     valid [2025-01-01, 2026-06-03)  recorded 2025-01-04
M2: uses_framework = SolidJS   valid [2026-06-03, ∞)           recorded 2026-06-05
```

Now three genuinely different questions have three deterministic answers:

| Question | Resolution | Answer |
|---|---|---|
| "What framework does this use?" | valid at now | **SolidJS** — one answer, no LLM guessing |
| "What did it use in March 2026?" | valid at 2026-03-01 | **React** |
| "What did we believe in May 2026?" | recorded ≤ 2026-05-01, valid at then | **React** — correctly reports the past belief |

The third row is why *both* axes are needed. Valid time alone cannot answer "what did the system think last month," which is exactly the question asked when auditing why an agent made a wrong decision. That audit capability is a core Fehrest promise ([I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable)), so single-axis temporality is insufficient.

### 4.2 Deterministic resolution

```
resolve(subject, predicate, scope, as_of_valid=now, as_of_recorded=now):
  candidates = memories where
      payload.subject   == subject
      payload.predicate == predicate
      scope             ⊇ requested scope
      status            == 'active'
      recorded_at       <= as_of_recorded
      valid_from        <= as_of_valid
      (valid_until is null or valid_until > as_of_valid)

  if empty:      return NO_ANSWER          # abstain; never fabricate
  if one:        return it
  otherwise, order by:
      1. epistemic_status:  observed > asserted > inferred > unverified
      2. human-confirmed before machine-asserted
      3. narrower scope before broader scope
      4. later valid_from
      5. later recorded_at
      6. higher confidence                 # last resort only
  if the top two are indistinguishable after all six:
      return CONTRADICTION(top candidates)  # surface, never silently pick
```

Four properties this ordering guarantees, and all four are testable:

1. **Total and deterministic** given the same inputs — required by [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable).
2. **No LLM in the resolution path** — required by [I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) and [R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules).
3. **Explicit abstention.** `NO_ANSWER` is a first-class result. Abstention is a measured axis in LongMemEval and a system that guesses instead of abstaining is worse than useless for a memory OS.
4. **Contradiction is surfaced, not resolved.** Silently choosing between two equally-supported conflicting memories is how a memory system becomes untrustworthy. The compiler passes contradictions through to the agent explicitly ([H](07-CONTEXT-COMPILER-SPEC.md)).

Property tests: resolution is monotone in `recorded_at`; resolution is stable under reordering of the input set; resolution over a random history equals a naive reference implementation.

### 4.3 Cost

Bitemporality costs a wider index and more complex queries. It does **not** require an LLM, a graph database, or vectors. Given that dynamic state tracking is one of the five measured abilities, and given that the failure it prevents (retrieving two conflicting values and asking a model to guess) is the failure the product exists to fix, the cost is justified.

---

## 5. Promotion

Not every message becomes memory. The pipeline:

```
event / conversation turn
  → [1] candidate extraction
  → [2] triage: is this durable at all?
  → [3] classification: type + scope
  → [4] deduplication
  → [5] contradiction detection
  → [6] temporal resolution
  → [7] value scoring
  → [8] provenance attachment
  → [9] promote | reject | queue for confirmation
  → later: supersession
```

### 5.1 Which stages are deterministic

This is the question the brief asks, and the answer determines whether `AI OFF` is a real mode or a marketing claim.

| Stage | Mechanism | Rationale |
|---|---|---|
| 1 — extraction | **Rule-driven** + optional model | Explicit markers (`decision:`, "remember that", "note that X fails") and structured events are rule-extractable. A model finds more. |
| 2 — triage | **Deterministic** | Hard filters below. |
| 3 — classification | Rule for marked, **model-assisted** otherwise | Type inference from free prose is genuinely hard without a model; unclassified candidates default to `fact`/`unverified` rather than being dropped. |
| 4 — dedup | **Deterministic** | Exact payload match, then normalised-statement match, then MinHash/trigram near-duplicate. No model needed. |
| 5 — contradiction | **Deterministic** for same subject+predicate; model-assisted for semantic conflict | Structural conflicts are computable; paraphrased conflicts are not. |
| 6 — temporal | **Deterministic** | §4.2. |
| 7 — value scoring | **Rule-driven** with optional model | §5.3. |
| 8 — provenance | **Deterministic and mandatory** | [I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance). |
| 9 — decision | **Rule** for auto-promote/auto-reject; **human** for high-influence types | §5.4. |

**With AI OFF, stages 1–2 and 4–9 run.** Fehrest still captures explicitly marked memories, all structured event-derived state, decisions, and everything an agent writes through the memory API. What is lost is *implicit* extraction from unmarked prose. That is a real degradation and it is stated plainly: `AI OFF` gives a fully functional memory system that captures less automatically. This is [H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value) and it is unproven.

**AgeMem's vocabulary is adopted; its mechanism is rejected.** The six operations — `add`, `update`, `delete`, `retrieve`, `summary`, `filter` — become Fehrest's memory API. Its actual results depend on a three-stage RL-trained policy (SFT → outcome RL → step-level GRPO), which cannot be the promotion decider in a system that must work with no model at all ([E-15](research/EVIDENCE_LOG.md#e-15--agemem-is-a-learned-policy-not-a-transplantable-algorithm)).

### 5.2 Triage — deterministic rejection

Rejected without a model:

- Pure intent about the immediate turn: *"I will inspect Cargo.toml."*
- Tool-call narration: *"Reading file X."*
- Restatements of retrievable content — if the statement is a near-duplicate of an indexed object body, it adds nothing.
- Statements with no resolvable subject.
- Content below a length/information floor.
- Statements whose evidence set is empty ([I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance)).

Rejections are recorded as `memory/candidate` + `memory/rejected` (T2, compactable per [D §5.2](03-CANONICAL-DATA-MODEL.md#52-durability-tiers--the-correction-to-the-brief)), so promotion behaviour is tunable against real data rather than guessed at.

### 5.3 Value scoring

The brief's three examples, scored:

| Statement | Score | Outcome |
|---|---|---|
| "I will inspect Cargo.toml." | Rejected at triage | Never a memory |
| "Dependency X is incompatible with environment Y because Z." | High | Auto-promote as `gotcha` |
| "Fehrest must never require cloud infrastructure." | Highest | Queue as `constraint` for confirmation |

Signals: generality (applies beyond this turn), durability (unlikely to change soon), non-recoverability (**cannot be re-derived from files — the strongest signal, because it is exactly what is otherwise lost**), causal content (explains *why*), negative knowledge (records a failure), and explicit user marking (overrides everything).

Non-recoverability is weighted highest deliberately. A memory duplicating what a file already says is nearly worthless; a memory recording an experiment that failed is irreplaceable.

### 5.4 Who decides

| Path | Applies to | Why |
|---|---|---|
| **Auto-promote** | `fact`, `episodic`, `relationship`, `state`, `procedure`, `gotcha` with resolvable evidence and no contradiction | High volume, moderate influence, fully reversible |
| **Auto-reject** | Triage failures | Cheap and safe |
| **Human confirmation required** | `decision`, `constraint`, `preference`; anything superseding a human-confirmed memory; anything contradicting an active memory | These steer all future agent behaviour and are the poisoning targets ([T-2](02-THREAT-MODEL.md#t-2--memory-poisoning)) |
| **Queued** | Everything else | Batched review, not a modal interruption |

The confirmation queue is the main UX risk in this design: if it produces dozens of prompts a day, users will approve blindly and the control becomes theatre. Mitigations: batch review, group by session, sensible defaults, and a measured target of **fewer than 5 confirmations per active day** ([O](14-PERFORMANCE-BUDGETS.md)). If dogfooding exceeds that, the promotion rules are wrong — not the user.

---

## 6. Supersession

Supersession is an event, not a mutation:

```
memory/superseded { superseded_id, superseding_id, reason, actor, ts }
```

Rules: the superseding memory must satisfy full provenance; the superseded memory becomes `status: superseded` and is retained; its `valid_until` is set to the superseding memory's `valid_from` unless explicitly given; superseding a human-confirmed memory with a machine-asserted one requires confirmation; chains are traversable in both directions.

Retention matters more than it appears. It is what allows the compiler to include *"previously SolidJS was rejected in favour of React on 4 January; reversed 3 June because of X"* — the superseded decision is often what explains the current one, and deleting it destroys the reasoning while keeping the conclusion.

---

## 7. Retrieval

Memory retrieval is a stage of the compiler ([H](07-CONTEXT-COMPILER-SPEC.md)), not a separate system:

1. Structured resolution for known subject/predicate — deterministic, no scoring.
2. Scope filter applied **first**, at every stage including graph expansion ([T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval)).
3. Temporal filter — `active` at the requested valid time, unless superseded memories are explicitly requested.
4. Lexical retrieval over statements via FTS5.
5. Graph expansion from memory subjects to related entities.
6. Optional vector similarity if D3 is enabled.
7. Type-aware assembly: constraints and gotchas are included preferentially because they are the highest-consequence omissions.
8. Contradictions attached explicitly.

---

## 8. Growth and forgetting

At 50 memories/day: ~18K/year, ~180K/decade. At ~1 KB each that is ~180 MB of JSONL per decade — a non-problem for storage, a real problem for retrieval precision.

**Fehrest does not delete memories by default.** Instead: `expired` status when `valid_until` passes; decay applied to *ranking*, not existence; consolidation of many episodic memories into one semantic memory that `supersedes` them (retaining originals); and archival segments for old memory files, still queryable.

Deletion is user-initiated only. A memory system that silently forgets is a memory system that cannot be trusted — and the one thing worse than a missing memory is a memory whose absence is undetectable.

---

## 9. Falsification criteria

| Finding | Consequence |
|---|---|
| Deterministic promotion recall < 60% of model-assisted ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)) | `AI OFF` degrades to read-only knowledge base; a thesis-level weakening requiring founder sign-off |
| Bitemporal resolution cannot be made deterministic in real conflicts | Core value proposition fails; redesign |
| Confirmation queue exceeds 5/day sustained | Promotion rules wrong; retune before shipping |
| Users never consult superseded memories | Retention is over-engineered; simplify (cheap to reverse) |
| Contradiction detection produces mostly false positives | Detection is noise; move behind a flag |
| Structured `payload` extractable for < 30% of memories | Deterministic resolution covers too little to matter; the model becomes prose-first and much weaker |
