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

> **RESHAPED IN F1-R2 ([R2-04](reviews/F1-R2-RECONCILIATION.md), [R2-05](reviews/F1-R2-RECONCILIATION.md)).** The single `epistemic_status` enum and the single `status` field are replaced by four orthogonal fields (§3.3). `scope` becomes a multi-dimensional selector with valid time removed from it (§3.4). `confidence` is demoted to diagnostic metadata and is no longer a resolution input (§3.1).

```json
{
  "id": "0198f2b7-...",                    // UUIDv7, immutable
  "statement": "The project migrated from React to SolidJS.",
  "payload": { "subject": "0198...", "predicate": "uses_framework", "object": "SolidJS" },
  "memory_type": "fact",

  // --- four orthogonal semantic axes (F1-R2, I-12) ---
  "basis":        "AGENT_ASSERTED",        // core-assigned, never actor-supplied
  "verification": "UNVERIFIED",
  "lifecycle":    "ACTIVE",
  "resolution":   "CLEAR",

  "actor": { "kind": "agent", "id": "agent:claude", "session": "0198..." },
  "evidence": [
    { "kind": "object", "id": "0198...", "locator": "L42-48", "content_hash": "sha256:...",
      "served_in": "0198f4..." },          // context package that served it (R2-02)
    { "kind": "event",  "id": "0198..." }
  ],
  "recorded_at": "2026-08-17T14:22:03Z",   // system-assigned, NEVER actor-supplied
  "valid_from":  "2026-06-03T00:00:00Z",   // actor-supplied, validated
  "valid_until": null,                      // null = still valid
  "scope": {                                // orthogonal dimensions; NO time dimension
    "vault":        "0198...",
    "project":      "0198...",              // omitted = not project-restricted
    "objects":      null,                   // omitted = not object-restricted
    "object_types": null                    // omitted = not type-restricted
  },
  "supersedes": ["0198f2b0-..."],
  "confidence_diagnostic": 0.85,            // metadata only; NEVER a resolution input
  "provenance": { "mechanism": "rule:decision-extractor", "mechanism_version": "1.2.0" }
}
```

### 3.1 Field semantics that carry weight

**`statement` and `payload` both exist.** `statement` is the human- and model-readable form; `payload` is the machine-resolvable triple. Structured resolution needs the triple (to know that two memories are about the same subject/predicate and therefore conflict); humans and models need the sentence. Storing only one forces either lossy parsing or unresolvable conflicts. `payload` is optional — not every useful memory is a clean triple, and refusing those would discard most gotchas.

**`recorded_at` is system-assigned.** This is a security property, not a convenience: it is what makes backdating impossible ([T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse)).

**`valid_from` is actor-supplied but validated.** A `valid_from` earlier than the earliest evidence timestamp is flagged. It cannot be forbidden — a user legitimately records in August that a decision was made in June — so the control is visibility, not prohibition.

**`confidence_diagnostic` has no truth authority ([R2-04](reviews/F1-R2-RECONCILIATION.md)).** F1 kept numeric confidence as the sixth and final tie-break in §4.2, which meant that when every principled rule was exhausted, **an uncalibrated floating-point number produced by a language model decided what Fehrest reported as true.** That is the exact failure the deterministic-resolution thesis exists to prevent, arrived at by the back door.

It is now **removed from the resolution path entirely**. The field is retained, renamed, and reclassified as diagnostic metadata: useful for tuning promotion rules and for showing a user how a mechanism rated its own output, and admissible in no comparison that decides an answer. When the deterministic ladder cannot separate two candidates, the result is `CONTRADICTION`, not a coin-flip weighted by a model's self-report. See [Q-6](16-OPEN-QUESTIONS.md).

**`lifecycle`** replaces the former `status` field, and `rejected` leaves it: a rejected *candidate* never becomes a memory, so it is a `memory/rejected` event, not a memory state. Superseded, retracted and expired memories are **retained, never deleted** — this is what makes memory substitution visible ([T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse)) and what lets the compiler explain *why* the current answer is current.

**`evidence[].served_in`** names the context package whose manifest contains the item. It is what makes [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) checkable rather than aspirational ([R2-02](reviews/F1-R2-RECONCILIATION.md)).

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
| `unclassified` | Type could not be determined deterministically | — | **never auto-promoted** — queued as `PENDING` (§5.1, [R2-16](reviews/F1-R2-RECONCILIATION.md)) |

`gotcha` and `procedure` are first-class rather than tags because they answer two of the five measured abilities and because they are the memory kinds with the highest value-per-byte: they encode work that cannot be recovered by re-reading the repository.

The three types that most strongly steer future agent behaviour — `preference`, `decision`, `constraint` — require human confirmation, because those are exactly the targets of memory poisoning ([T-2](02-THREAT-MODEL.md#t-2--memory-poisoning)).

### 3.3 The Fehrest evidence and trust model

> **DEFINED NATIVELY IN F1-R1 ([R1-08](reviews/F1-R1-RECONCILIATION.md)).** F1's four-value `epistemic_status` was serviceable but partly shaped by an extractor's vocabulary. **Extractor confidence labels must map into Fehrest's model, never define it** — a label distribution observed on one corpus (`AMBIGUOUS` at 0.0%) says nothing about ambiguity in general.
>
> **DECOMPOSED IN F1-R2 ([R2-04](reviews/F1-R2-RECONCILIATION.md)).** R1's **eight-state single enum is withdrawn.** It mixed four independent semantic axes into one vocabulary. The eight states are not replaced by a total ordering over the same list — they are **redistributed onto the four axes they actually belonged to**.

### The four axes

Each memory carries **one value from each axis**, independently. Every axis is event-sourced per [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended).

**Axis 1 — `basis`: where the claim came from.** Core-assigned; **no actor may supply it**.

| Value | Meaning | Reachable by |
|---|---|---|
| `USER_ASSERTED` | A human stated it | The user only |
| `EXTRACTED` | Fehrest's own deterministic parsing derived it from a primary source | Fehrest core only |
| `AGENT_ASSERTED` | An identified agent stated it | Any authenticated agent session |
| `INFERRED` | A mechanism (rule or model) derived it from other Fehrest state | Rules or models |

**Axis 2 — `verification`: whether it has been checked, and by whom.**

| Value | Meaning | Reached by |
|---|---|---|
| `UNVERIFIED` | Default for everything | — |
| `CORROBORATED` | A **second, independent** evidence link resolves and supports it | Any actor **other than** the asserting session |
| `USER_CONFIRMED` | A human explicitly affirmed it | The user only |

**Axis 3 — `lifecycle`: whether it is in force.**

| Value | Meaning |
|---|---|
| `PENDING` | Recorded and visible, but **not authoritative** — awaiting confirmation (§5.5) |
| `ACTIVE` | In force |
| `SUPERSEDED` | Replaced by a later memory; retained and queryable |
| `RETRACTED` | Withdrawn by its asserter or revoked by provenance; retained |
| `EXPIRED` | `valid_until` has passed; retained |

**Axis 4 — `resolution`: whether it currently resolves cleanly.**

| Value | Meaning |
|---|---|
| `CLEAR` | Its evidence resolves and it does not contend with another candidate |
| `CONFLICTED` | It contends with another candidate and the deterministic resolver produced no justified winner |
| `UNRESOLVED` | Its **own** evidence does not currently resolve — broken anchor, deleted source, unrecognised extractor label. It cannot participate in resolution at all |

### Why four axes rather than one enum

The eight R1 states map onto the axes cleanly, which is the demonstration that they were never one vocabulary:

| R1 state | Axis it actually described |
|---|---|
| `EXTRACTED`, `INFERRED`, `ASSERTED` | `basis` |
| `USER_CONFIRMED`, `AGENT_CONFIRMED` | `verification` |
| `SUPERSEDED` | `lifecycle` |
| `CONFLICTED`, `UNRESOLVED` | `resolution` |

Two concrete defects follow from the collapse, and both are removed by the split:

1. **Real states were inexpressible.** A memory asserted by an agent, later confirmed by the user, currently active, and now contending with a newer memory occupies one value on each of four axes. The single enum forced a choice among `ASSERTED`, `USER_CONFIRMED` and `CONFLICTED`, destroying two of the three facts.
2. **It invited an unjustified total ordering.** Ranking `observed > asserted > inferred > unverified` compares an origin against a verification level — a category error that then decided which memory Fehrest reported as true. §4.2 is rewritten accordingly.

**Per-axis transition rules** — anything not listed is forbidden, and every transition emits an event:

```
basis         immutable after allocation.  No transition exists.  (core-assigned)

verification  UNVERIFIED    → CORROBORATED    (second independent resolving evidence link,
                                               contributed by a session other than the asserter)
              UNVERIFIED    → USER_CONFIRMED  (explicit human confirmation event)
              CORROBORATED  → USER_CONFIRMED  (explicit human confirmation event)
              no downward transition; a withdrawn confirmation is a RETRACTED lifecycle,
              not a lowered verification

lifecycle     PENDING → ACTIVE       (confirmation, or an auto-promote rule that applies)
              PENDING → RETRACTED    (rejected at review)
              ACTIVE  → SUPERSEDED   (a later memory replaces it)
              ACTIVE  → RETRACTED    (withdrawal or provenance revocation)
              ACTIVE  → EXPIRED      (valid_until passes)
              SUPERSEDED/RETRACTED/EXPIRED are terminal; correction is a new memory

resolution    CLEAR      ↔ CONFLICTED   (contention appears or is removed)
              any        → UNRESOLVED   (its own evidence stops resolving)
              UNRESOLVED → CLEAR        (evidence resolves again)
```

**Three rules that make this a boundary rather than a label:**

1. **No upward `verification` transition without new evidence or a human.** `→ USER_CONFIRMED` requires a human event; `→ CORROBORATED` requires a *second, independent* evidence link contributed by a different session. **An actor cannot corroborate its own assertion.**
2. **`basis = EXTRACTED` is unreachable by any agent.** Only Fehrest's own deterministic parsing produces it. An agent asserting "I read this in the file" produces `AGENT_ASSERTED`, not `EXTRACTED` — the distinction between *Fehrest parsed it* and *something told us it parsed it* is exactly the boundary [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) attacks.
3. **`CONFLICTED` is a first-class resting state, not an error.** A memory may sit conflicted indefinitely. Forcing resolution is how a memory system starts inventing answers.

**Mapping extractor labels in** — one-way, at ingestion, and now onto **two** axes rather than one:

| Extractor label | `basis` | `resolution` |
|---|---|---|
| `EXTRACTED` | `EXTRACTED` | `CLEAR` |
| `INFERRED` | `INFERRED` | `CLEAR` |
| `AMBIGUOUS` | `INFERRED` | `UNRESOLVED` |
| *(unrecognised label)* | `INFERRED` | `UNRESOLVED` |

The last row matters: an unknown label from a future or different extractor degrades to `UNRESOLVED` rather than being trusted or dropped. This is what lets the extractor be replaced ([ADR-0003](09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape)) without touching the trust model.

### 3.4 Scope is orthogonal dimensions, not an ordered lattice

> **REDESIGNED IN F1-R2 ([R2-05](reviews/F1-R2-RECONCILIATION.md)).** F1 listed scope kinds as `vault · project · object · type · time` and treated them as a single ordered lattice from broad to narrow. That is wrong twice over: **`time` is not a containment scope at all** — it is temporal validity, and it already has two dedicated axes (§4) — and **`type` is a selector, not a container**: `type: decision` does not sit inside or outside `project: Fehrest`.

**A scope is a selector over independent dimensions.** Each dimension is either *unconstrained* or restricted to a set:

| Dimension | Meaning | Unconstrained means |
|---|---|---|
| `vault` | The vault this memory belongs to | — **always required**; there is no cross-vault memory in v1 ([Q-11](16-OPEN-QUESTIONS.md)) |
| `project` | Restricted to specific projects | Applies across all projects in the vault |
| `objects` | Restricted to specific object IDs | Not object-restricted |
| `object_types` | Restricted to specific object types | Not type-restricted |
| `principal` | *(grants only)* restricted to specific sessions or agents | Not principal-restricted |

**Valid time is not here.** `valid_from` / `valid_until` and the request's `as_of` answer *when* a memory is true. Encoding that as a scope kind conflated "where does this apply" with "when was this true", and would have made a time window compete with a project ID in the same ordering.

**Match.** A memory `M` is a candidate for a request `R` **iff for every dimension, either `M` is unconstrained on it, or `R`'s value for that dimension is in `M`'s admitted set.** A dimension `R` does not specify cannot be matched by an `M` that constrains it.

**Intersection.** Dimension-wise. If any dimension intersects to the empty set, the two scopes are **incompatible** and share no candidate. Grants intersect the same way, so a session's effective scope is the intersection of its grant with the request.

**Specificity is a partial order, deliberately.** `S₁ ≻ S₂` (strictly more specific) iff on every dimension `S₁`'s admitted set is a subset of `S₂`'s, and on at least one it is a proper subset. Otherwise the two are **incomparable**.

Two consequences, and both are the point:

- **A vault-global memory can never silently override a conflicting project-local one.** Vault-global leaves `project` unconstrained; project-local restricts it. Project-local is therefore *strictly more specific*, and §4.2 ranks specificity above nothing else that could invert it. The dangerous direction is structurally unavailable.
- **Incomparable scopes do not resolve.** `{type: decision}` and `{project: Fehrest}` are incomparable. Two conflicting memories at incomparable scopes produce `CONTRADICTION`, not an invented winner. Silently preferring one would be the same failure as the confidence tie-break, wearing a different name.

**Creation of a vault-global durable memory requires explicit user authority.** It is never a default promotion scope and never an automatic widening. **Default promotion scope is the narrowest selector that covers all of the memory's evidence**: if every evidence item resolves inside one project, the memory is project-scoped; if the evidence spans projects, the candidate is queued for confirmation with the proposed scope shown, never silently promoted to vault-global.

**Enforced at every retrieval stage, never as a post-filter** ([T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval)) — including graph expansion, which crosses project boundaries by nature.

**Property tests.**
- `test_scope_cross_project_poisoning` — a memory written under project A, at any scope its author can construct, never becomes a resolution candidate for project B unless the user explicitly authored it vault-global.
- `test_scope_incomparable_yields_contradiction` — over randomly generated incomparable selector pairs with contradictory payloads, resolution returns `CONTRADICTION` and never a winner.
- `test_scope_intersection_is_dimensionwise` — property test against a naive reference implementation.
- `test_vault_global_requires_user_authority` — no agent-reachable path creates a vault-unconstrained durable memory.

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

> **NORMATIVE RESOLVER SPECIFICATION — rewritten in F1-R2 ([R2-04](reviews/F1-R2-RECONCILIATION.md), [R2-05](reviews/F1-R2-RECONCILIATION.md)).** This is the single authoritative statement of how Fehrest decides what is currently true. Any other document describing resolution defers to this one.

```
resolve(subject, predicate, request_scope, as_of_valid=now, as_of_recorded=now):

  # ---- ADMISSION -------------------------------------------------------
  candidates = memories where
      payload.subject   == subject
      payload.predicate == predicate
      scope_matches(m.scope, request_scope)      # §3.4 match, dimension-wise
      m.lifecycle       == ACTIVE                # PENDING is NOT authoritative (§5.5)
      m.resolution      != UNRESOLVED            # own evidence must resolve
      m.recorded_at     <= as_of_recorded
      m.valid_from      <= as_of_valid
      (m.valid_until is null or m.valid_until > as_of_valid)

  if empty:      return NO_ANSWER                # abstain; never fabricate
  if one:        return it

  # ---- DETERMINISTIC EVIDENCE LADDER -----------------------------------
  # Each rung compares ONE axis. A rung applies only where the comparison
  # is well-founded; where it is not, the rung is skipped, not guessed.

  1. verification     USER_CONFIRMED > CORROBORATED > UNVERIFIED
  2. basis            USER_ASSERTED > EXTRACTED > AGENT_ASSERTED > INFERRED
  3. scope specificity  strictly-more-specific wins
                        INCOMPARABLE scopes -> rung skipped (§3.4)
  4. valid_from       later wins
  5. recorded_at      later wins

  if one candidate strictly dominates after the ladder:
      return it
  else:
      return CONTRADICTION(remaining candidates, reason)
```

**What changed, and why it matters.**

- **`confidence` is gone from the ladder.** F1's rung 6 let an uncalibrated model-produced float pick the winner whenever principled rules ran out. Removed ([§3.1](#31-field-semantics-that-carry-weight)). The ladder now **terminates in `CONTRADICTION` rather than in a number**.
- **Rungs 1 and 2 were one rung.** F1 ranked `observed > asserted > inferred > unverified` and then, separately, "human-confirmed before machine-asserted" — comparing origin against verification inside a single order. They are now two rungs on two axes, in the order that reflects which question dominates: *has a human checked this* outranks *where did it come from*.
- **Rung 2's internal order.** `USER_ASSERTED` outranks `EXTRACTED` because authority originates with the user and only the user ([C §3](02-THREAT-MODEL.md#3-actors)); a user correcting Fehrest's parse must win. `EXTRACTED` outranks `AGENT_ASSERTED` because Fehrest parsing a primary source is mechanically checkable while an agent's claim to have done so is not — this is the [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning) boundary expressed as an ordering.
- **Rung 3 can be skipped.** Incomparable scopes are common and legitimate (§3.4). A skipped rung is not a tie broken silently; it simply carries no information, and if nothing below it separates the candidates, the answer is `CONTRADICTION`.

**Five properties this guarantees, all testable:**

1. **Deterministic** given the same inputs — required by [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable). Note it is deliberately **not total**: incomparable inputs have no winner, and the resolver says so.
2. **No LLM in the resolution path** — required by [I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) and [R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules). No model output influences any rung.
3. **Explicit abstention.** `NO_ANSWER` is a first-class result. Abstention is a measured axis in LongMemEval, and a system that guesses instead of abstaining is worse than useless for a memory OS.
4. **Contradiction is surfaced, not resolved.** Silently choosing between two equally-supported conflicting memories is how a memory system becomes untrustworthy. The compiler passes contradictions through to the agent explicitly ([H](07-CONTEXT-COMPILER-SPEC.md)).
5. **Unconfirmed candidates cannot win.** `PENDING` memories are excluded at admission, so nothing awaiting confirmation can be reported as current state (§5.5, [R-12](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).

**Property tests.** Resolution is monotone in `recorded_at`; stable under reordering of the input set; equal to a naive reference implementation over random histories; **never returns a winner selected by `confidence_diagnostic`** (mutate the field across the full range and assert the result is unchanged); and returns `CONTRADICTION` — not a winner — for every randomly generated incomparable-scope conflict.

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
| 3 — classification | Rule for marked, **model-assisted** otherwise. **With AI off, unclassified prose is queued, never auto-typed** ([R2-16](reviews/F1-R2-RECONCILIATION.md)) | Type inference from free prose is genuinely hard without a model. |
| 4 — dedup | **Deterministic** | Exact payload match, then normalised-statement match, then MinHash/trigram near-duplicate. No model needed. |
| 5 — contradiction | **Deterministic** for same subject+predicate; model-assisted for semantic conflict | Structural conflicts are computable; paraphrased conflicts are not. |
| 6 — temporal | **Deterministic** | §4.2. |
| 7 — value scoring | **Rule-driven** with optional model | §5.3. |
| 8 — provenance | **Deterministic and mandatory** | [I-11](01-ARCHITECTURE-CONSTITUTION.md#i-11--agent-generated-memories-preserve-provenance). |
| 9 — decision | **Rule** for auto-promote/auto-reject; **human** for high-influence types | §5.4. |

**With AI OFF, stages 1–2 and 4–9 run.** Fehrest still captures explicitly marked memories, all structured event-derived state, decisions, and everything an agent writes through the memory API. What is lost is *implicit* extraction from unmarked prose. That is a real degradation and it is stated plainly: `AI OFF` gives a fully functional memory system that captures less automatically. This is [H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value) and it is unproven.

#### The AI-OFF classification default — corrected in F1-R2 ([R2-16](reviews/F1-R2-RECONCILIATION.md))

F1 specified that unclassified candidates *"default to `fact`/`unverified` rather than being dropped."* Combined with §5.4, where `fact` is an **auto-promote** type, that default silently converted arbitrary unclassified prose into authoritative memory whenever no model was available — in the exact configuration the constitution designates as fully supported ([I-4](01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api)).

**The corrected rule: uncertainty about type is uncertainty about influence.**

If Fehrest cannot determine with a deterministic rule whether an item is a `fact`, `decision`, `constraint`, `preference`, `procedure`, `gotcha` or anything else, it does **not** pick the type that happens to auto-promote. The candidate is recorded with `memory_type: unclassified` and `lifecycle: PENDING`, and it waits for an explicit classification action (§5.5).

| Situation | AI ON | AI OFF |
|---|---|---|
| Explicit marker present (`decision:`, "remember that…") | Rule-classified | Rule-classified — identical |
| Structured event-derived state | Rule-classified | Rule-classified — identical |
| Type inferable by a model | Model-classified, then §5.4 applies | **Queued as `unclassified` / `PENDING`** |
| No marker, no rule, no model | **Queued as `unclassified` / `PENDING`** | **Queued as `unclassified` / `PENDING`** |

Nothing is dropped — F1's concern was right. It is *held*, visibly, without authority.

**Measured by [B-5](10-BENCHMARK-PLAN.md#b-5--memory-promotion-quality), with a metric added in R2:** **type-assignment precision**, and specifically the rate at which memories that *should* have required confirmation (`decision`, `constraint`, `preference`) were classified into an auto-promote type. That number is a safety metric, not a quality metric: each such misclassification is a memory that acquired steering authority without a human ever seeing it.

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

| Path | Applies to | Resulting lifecycle | Why |
|---|---|---|---|
| **Auto-promote** | `fact`, `episodic`, `relationship`, `state`, `procedure`, `gotcha` with resolvable evidence, a determinate type, and no contradiction | `ACTIVE` | High volume, moderate influence, fully reversible |
| **Auto-reject** | Triage failures | *(never a memory; `memory/rejected` event)* | Cheap and safe |
| **Human confirmation required** | `decision`, `constraint`, `preference`; anything superseding a human-confirmed memory; anything contradicting an active memory; anything proposing a vault-global scope (§3.4) | `PENDING` | These steer all future agent behaviour and are the poisoning targets ([T-2](02-THREAT-MODEL.md#t-2--memory-poisoning)) |
| **Queued** | Everything else, including every `unclassified` candidate | `PENDING` | Batched review, not a modal interruption |

The confirmation queue is the main UX risk in this design: if it produces dozens of prompts a day, users will approve blindly and the control becomes theatre. Mitigations: batch review, group by session, sensible defaults, and the confirmation-burden budget in [O §10](14-PERFORMANCE-BUDGETS.md) — which F1-R2 reclassifies as an **unvalidated planning assumption to be measured, not a canonised threshold** ([R2-06](reviews/F1-R2-RECONCILIATION.md)). If dogfooding exceeds the measured tolerable rate, the promotion rules are wrong — not the user.

### 5.5 Pending-confirmation semantics

> **ADDED IN F1-R2 ([R2-06](reviews/F1-R2-RECONCILIATION.md)).** F1 named a confirmation queue but never specified what a queued item *is* while it waits. Two opposite failures were both reachable from that silence: an unconfirmed candidate leaking into authoritative state, or an unconfirmed candidate being invisible until someone happened to open a review screen — so an agent could act in ignorance of a constraint the user had already stated.

`lifecycle: PENDING` is a real, specified state, and it is **non-authoritative but not hidden**.

**What a PENDING memory may do:**

- Appear in a **clearly separated, explicitly non-authoritative** advisory section of a compiled context package — `pending_advisory` ([H §3](07-CONTEXT-COMPILER-SPEC.md#3-output)) — labelled as unconfirmed, with its proposed type and scope shown.
- Justify **asking**, **abstaining**, or **requesting human confirmation**. "There is an unconfirmed candidate constraint that may forbid this; confirm before proceeding" is exactly the behaviour wanted.
- Be listed, searched, reviewed, promoted or rejected by the user.

**What a PENDING memory may never do — [R-12](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules):**

- Enter `active_constraints`, `current_decisions`, `project_state`, or any other authoritative section.
- Be returned by `resolve()` as current state. It is excluded at admission (§4.2).
- Grant a capability, revoke a capability, or appear in `permitted_actions`.
- Supersede any `ACTIVE` memory, and specifically never a `USER_CONFIRMED` one.
- Become executable policy of any kind.

**The distinction in one line:** a `PENDING` memory can cause an agent to *stop and ask*; it can never cause an agent to *proceed differently and silently*. Advisory content can only ever narrow what an agent does on its own authority.

**Tests.** `test_pending_never_authoritative` — for every authoritative surface (resolver output, each authoritative package section, `permitted_actions`, capability evaluation), assert no `PENDING` memory can reach it by any path. `test_pending_is_visible` — a `PENDING` candidate appears in `pending_advisory` with its non-authoritative labelling intact. `test_pending_cannot_supersede` — a supersession event naming a `PENDING` memory as the superseding record is rejected at the storage layer.

**Confirmation burden is measured before automation is enabled.** Any expansion of auto-promotion beyond §5.4 requires measured confirmation-volume data from real multi-agent traces, not the assumed rate.

---

## 6. Supersession

Supersession is an event, not a mutation:

```
memory/superseded { superseded_id, superseding_id, reason, actor, ts }
```

Rules: the superseding memory must satisfy full provenance; the superseded memory moves to `lifecycle: SUPERSEDED` and is retained; its `valid_until` is set to the superseding memory's `valid_from` unless explicitly given; **a memory with `verification: USER_CONFIRMED` may be superseded only by another `USER_CONFIRMED` memory or after explicit confirmation**; **a `PENDING` memory may never supersede anything** (§5.5); chains are traversable in both directions.

Retention matters more than it appears. It is what allows the compiler to include *"previously SolidJS was rejected in favour of React on 4 January; reversed 3 June because of X"* — the superseded decision is often what explains the current one, and deleting it destroys the reasoning while keeping the conclusion.

---

## 7. Retrieval

Memory retrieval is a stage of the compiler ([H](07-CONTEXT-COMPILER-SPEC.md)), not a separate system:

1. Structured resolution for known subject/predicate — deterministic, no scoring.
2. Scope filter applied **first**, at every stage including graph expansion, using the dimension-wise match of §3.4 ([T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval)).
3. Temporal filter — `lifecycle: ACTIVE` at the requested valid time, unless superseded memories are explicitly requested. `PENDING` items are retrieved only into the advisory channel (§5.5).
4. Lexical retrieval over statements via FTS5.
5. Graph expansion from memory subjects to related entities.
6. Optional vector similarity if D3 is enabled.
7. Type-aware assembly: constraints and gotchas are included preferentially because they are the highest-consequence omissions.
8. Contradictions attached explicitly.

---

## 8. Growth and forgetting

At 50 memories/day: ~18K/year, ~180K/decade. At ~1 KB each that is ~180 MB of JSONL per decade — a non-problem for storage, a real problem for retrieval precision.

> **The 50 memories/day and 500 events/day figures are UNVALIDATED PLANNING ASSUMPTIONS** ([R2-12](reviews/F1-R2-RECONCILIATION.md)). They are not measured, and no counter-estimate has been accepted in their place. Phase 0 measures real multi-agent event and memory volume by class before any retention, tiering or compaction parameter is frozen ([O §9](14-PERFORMANCE-BUDGETS.md#9-growth-over-time)).

**Fehrest does not delete memories by default.** Instead: `lifecycle: EXPIRED` when `valid_until` passes; decay applied to *ranking*, not existence; consolidation of many episodic memories into one semantic memory that `supersedes` them (retaining originals); and archival segments for old memory files, still queryable.

Deletion is user-initiated only. A memory system that silently forgets is a memory system that cannot be trusted — and the one thing worse than a missing memory is a memory whose absence is undetectable.

---

## 9. Falsification criteria

| Finding | Consequence |
|---|---|
| Deterministic promotion recall < 60% of model-assisted ([H-3](research/EVIDENCE_LOG.md#h-3--deterministic-promotion-rules-capture-most-durable-memory-value)) | `AI OFF` degrades to read-only knowledge base; a thesis-level weakening requiring founder sign-off |
| Bitemporal resolution cannot be made deterministic in real conflicts | Core value proposition fails; redesign |
| Confirmation burden exceeds what dogfooding shows users will actually service | Promotion rules wrong; retune before shipping. **The tolerable rate is measured, not assumed** ([R2-06](reviews/F1-R2-RECONCILIATION.md)) |
| Users never consult superseded memories | Retention is over-engineered; simplify (cheap to reverse) |
| Contradiction detection produces mostly false positives | Detection is noise; move behind a flag |
| Structured `payload` extractable for < 30% of memories | Deterministic resolution covers too little to matter; the model becomes prose-first and much weaker |
| **The four-axis model produces `CONTRADICTION` so often that agents cannot act** ([R2-04](reviews/F1-R2-RECONCILIATION.md)) | The ladder is under-powered, **not** an argument to restore a confidence tie-break. Add *evidence-based* rungs, or accept a higher abstention rate as honest. Restoring uncalibrated confidence as truth authority is forbidden |
| **`PENDING` items accumulate faster than they are reviewed** | The auto-promote boundary in §5.4 is drawn too conservatively for real use; widen it on measured type-assignment precision, never by lowering the confirmation requirement for `decision`/`constraint`/`preference` |
