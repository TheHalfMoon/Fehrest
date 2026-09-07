# Fehrest V2 Tencent-Driven Gap Review — 2026-09-08

**Status:** REVIEW / NON-AUTHORIZING  
**Inputs:** current Fehrest V2 proposal set + qualified source review for Tencent/RoMem, Tencent/WeKnora and Tencent/SkillHone  
**Execution effect:** NONE  
**Canonical frontier:** unchanged; live `specs/CURRENT.md` wins

> The purpose of this review is to find structural gaps exposed by the three new sources without converting donor capabilities into requirements. It preserves the current one-frontier, canonical-vs-derived, local-first and evidence-first model.

## 1. Review verdict

The current V2 proposal already has strong phase decomposition, but the new sources expose a set of contracts that were either implicit or split across several future specs.

This review does **not** recommend new top-level Spec IDs. It assigns each gap to an existing owner so the program does not grow merely because new donors were discovered.

```text
NEW_GAPS_IDENTIFIED=14
NEW_GAPS_WITH_OWNER_OR_EXPLICIT_GATE=14/14
NEW_TOP_LEVEL_SPECS_REQUIRED=0
KNOWN_NEW_DEPENDENCY_CYCLES=0
R1_SEMANTICS_CHANGED=NO
R1_REVIEW_CANDIDATE_CHANGED=NO
IMPLEMENTATION_AUTHORIZED=NO
```

## 2. TG-01 — Temporal ranking can be mistaken for temporal truth

**Source trigger:** RoMem.

### Gap

The proposal states that temporal state is explicit and search rank is derived, but it does not explicitly prohibit a temporal reranker from deciding which fact is canonically current.

### Risk

A graph/vector/model-derived score could silently replace deterministic provenance-backed temporal resolution.

### Owner

```text
006 owns canonical temporal truth/resolution
004 owns temporal/graph capability experiment
005 may own a retained derived provider
007 may consume derived rank only after canonical scope/time filtering
```

### Required invariant

```text
TEMPORAL_RANK != TEMPORAL_TRUTH
DERIVED_VOLATILITY != CANONICAL_VALIDITY_INTERVAL
MODEL_TEMPORAL_SCORE != SUPERSESSION_EVENT
```

### Gate

Any temporal-ranking provider must be benchmarked against a simpler canonical-time filter + lexical/structured baseline before retention.

---

## 3. TG-02 — Relation volatility has no explicit persistence/authority class

**Source trigger:** RoMem semantic speed gate.

### Gap

A future relation-level volatility estimate could be useful, but the program does not say where such a value lives or whether it may influence lifecycle.

### Owner

004 experimental research; 005 derived provider if retained.

### Resolution

```text
RELATION_VOLATILITY_CLASS=DERIVED_REBUILDABLE
RELATION_VOLATILITY_CAN_AUTHOR_MEMORY=NO
RELATION_VOLATILITY_CAN_OVERRIDE_AS_OF=NO
```

If the signal adds no material outcome value, reject it and retain explicit temporal semantics only.

---

## 4. TG-03 — Memory promotion policy is too generic across memory types

**Source trigger:** WeKnora categories + confirmation stage.

### Gap

The proposed 006 Memory Proposal lifecycle is intentionally generic. It does not yet require different promotion rules for low-risk convenience memory versus high-influence decisions, constraints, preferences, identities or procedures.

### Risk

A single auto-promotion policy could turn a model extraction into durable authority.

### Owner

006.

### Required design rule

The authorized 006 spec must define a promotion matrix over at least:

```text
MEMORY_KIND
INFLUENCE_LEVEL
EVIDENCE_REQUIREMENT
CORROBORATION_REQUIREMENT
HUMAN_CONFIRMATION_REQUIREMENT
EXPIRY_OR_REVALIDATION_RULE
SUPERSESSION_RULE
RETRACTION_RULE
```

High-influence objects require explicit human confirmation unless a later founder/security decision authorizes a narrower deterministic rule.

---

## 5. TG-04 — Resident memory versus on-demand memory is not an explicit context policy

**Source trigger:** WeKnora persistent profile context + `search_memory` recall.

### Gap

006 owns memory and 007 owns context compilation, but the proposal does not require a policy for which durable memories are resident in every request versus recalled only when relevant.

### Risks

```text
unnecessary token cost
privacy overexposure
stale-context persistence
cross-task contamination
hidden priority bias
```

### Owner

006 defines memory metadata needed for residency/relevance; 007 owns the compiler/residency policy and receipts.

### Required benchmark

Compare at minimum:

```text
minimal resident profile + on-demand recall
vs
all eligible memory injected
vs
strong no-memory / repository-native baseline
```

Measure quality, privacy exposure, token cost and stale-use rate.

---

## 6. TG-05 — Editable derived chunks/wiki pages can become shadow canonical state

**Source trigger:** WeKnora chunk editing, wiki editing and rollback.

### Gap

The V2 plan has canonical notes/documents and derived retrieval, but does not explicitly state what happens when a user edits a derived chunk, generated wiki page or graph-derived summary.

### Risk

The visible product can diverge from canonical source while the derived representation becomes de facto truth.

### Owner

```text
003 owns derived projection rebuild/equality
010 owns canonical object/open-format semantics
011 owns editing/history UX
012 owns graph/search presentation
```

### Required invariant

```text
EDIT_DERIVED_STATE_DIRECTLY=NO
```

A user edit must either:

1. mutate an explicitly canonical object through the canonical writer; or
2. create a canonical annotation/proposal/reference with provenance; or
3. be rejected as editing a disposable projection.

Rebuild from canonical state must never silently erase a user-authored durable edit.

---

## 7. TG-06 — Execution admission/receipt ownership is under-specified in the V2 spec map

**Source trigger:** WeKnora session-persistent sandboxes and SkillHone executable helpers.

### Gap

007 owns grants/context and later specs own models/web/extensions, but the proposal does not clearly assign one owner for durable external-execution admission, attempt identity, fencing and terminal receipts.

### Risk

013, 014 and 021 could independently implement incompatible retry and authority semantics.

### Owner

007 must own a general execution-admission/receipt foundation. 013, 014 and 021 consume it and may add provider-specific metadata, never alternate authority.

### Required contract family

```text
ExecutionAdmission
ExecutionAttemptId
FencingGeneration
ExecutorAudience
EffectiveScope
ReservedBudget
DispatchIntent
StartedEvidence
TerminalReceipt
IndeterminateState
ReconciliationEvidence
```

### Required invariant

```text
FAILED_PROCESS_STATUS != RETRY_SAFE
NO_DURABLE_DISPATCH_INTENT -> NO_DISPATCH
INDETERMINATE -> NO_BLIND_RETRY
```

---

## 8. TG-07 — External/scoped API key identity can be confused with canonical principal identity

**Source trigger:** WeKnora scoped API keys/principal model.

### Gap

007 defines principal/session/grant concepts but the proposal does not explicitly require external credential identities to map into, rather than define, Fehrest principals.

### Owner

007 baseline; 018 organization extension; 021 connector/extension credentials consume the same rule.

### Required invariant

```text
API_KEY_ID != CANONICAL_PRINCIPAL_ID
EXTERNAL_IDENTITY != GRANT
CREDENTIAL_POSSESSION != SCOPE_WIDENING
```

Every external identity mapping must be auditable, revocable and fail closed on ambiguity.

---

## 9. TG-08 — Queue/worker concurrency lacks canonical idempotency and fencing semantics

**Source trigger:** WeKnora task queue and worker-pool governance.

### Gap

Operational queues are likely for model/tool/automation work, but queue retry semantics are not currently separated from safe execution semantics.

### Owner

007 owns attempt/fencing/idempotent admission. Provider/runtime specs may own scheduling and concurrency tuning only.

### Required rules

```text
QUEUE_JOB_ID != EXECUTION_ATTEMPT_ID
WORKER_RETRY != AUTHORIZED_RETRY
CONCURRENCY_LIMIT != AUTHORIZATION
PROVIDER_ACK != DURABLE_COMPLETION_RECEIPT
```

Recovery tests must cover crash after durable dispatch intent but before provider acknowledgement.

---

## 10. TG-09 — Skill artifacts have no explicit lifecycle/ownership model

**Source trigger:** SkillHone whole-skill optimization.

### Gap

021 covers extension manifests and automation but not a first-class lifecycle for skills containing instructions, executable helpers, references and assets.

### Owner

021.

### Required future model

```text
SkillPackage
SkillRevision
SkillSourceProvenance
SkillCapabilityRequirements
SkillRuntimeCompatibility
SkillEvalBinding
SkillReleaseState
SkillRollbackTarget
```

Skill executable helpers must pass the same capability/execution boundary as any other external tool.

---

## 11. TG-10 — Held-out evaluation isolation is not mandatory for skill evolution

**Source trigger:** SkillHone eval/skill split.

### Gap

The program requires benchmarks but does not require optimization/evolution systems to be structurally unable to read held-out probes/gold labels.

### Owner

021 for skill evolution; reusable benchmark-security pattern may be consumed by later optimization systems.

### Required invariant

```text
HELD_OUT_EVAL_DATA=EVIDENCE_ARTIFACT
OPTIMIZER_READ_ACCESS_TO_HELD_OUT_GOLD=NO
PROMPT_CONVENTION_IS_NOT_ISOLATION
```

The isolation mechanism must be enforced by process/filesystem/capability boundaries and tested adversarially.

---

## 12. TG-11 — Persistent decision history is not clearly separated from memory

**Source trigger:** SkillHone persistent decision history.

### Gap

A development decision history is valuable, but the current product vision could tempt a later implementation to ingest every optimization trajectory directly into durable memory.

### Owner

021 owns skill-evolution decision evidence. 006 may accept explicit Memory Proposals derived from that evidence, never raw automatic promotion.

### Required invariant

```text
DECISION_HISTORY=EVIDENCE
TRAJECTORY=EVIDENCE
MERGED_SKILL_DIFF=SOURCE_EVIDENCE
NONE_OF_THE_ABOVE=AUTO_ACTIVE_MEMORY
```

---

## 13. TG-12 — Generated wiki/knowledge crystallization lacks an explicit authority transition

**Source trigger:** WeKnora auto-wiki.

### Gap

Fehrest has notes, memory proposals and team crystallization UX, but the transition from generated summary/wiki output to durable canonical content is not explicit.

### Owner

010 owns canonical document/object representation; 006 owns memory promotion; 011/019 own personal/team review UX; 013 may generate drafts.

### Required states

```text
GENERATED_DRAFT
USER_SAVED_CANONICAL_DOCUMENT
MEMORY_PROPOSAL
APPROVED_MEMORY
```

These states must not collapse into one another.

---

## 14. TG-13 — Session-persistent sandbox state can outlive its grant or secret policy

**Source trigger:** WeKnora persistent Docker/E2B/Cube sandboxes.

### Gap

A session-persistent sandbox improves workflows but creates stale credential, stale grant and leftover-artifact risk.

### Owner

007 owns grant/execution admission; 018 may extend org policy; 021 owns extension/skill sandbox product integration.

### Required tests

```text
grant revoked while sandbox alive
credential reference rotated
network scope narrowed
session expires
snapshot restored under different principal
artifact from prior attempt reused
sandbox provider unavailable
```

A live sandbox does not imply a live authority chain.

---

## 15. TG-14 — Source-license admission is documented but lacks a standard reusable evidence record

**Source trigger:** RoMem's missing root license and WeKnora's mixed third-party license surface.

### Gap

Program invariant I-17 requires provenance/rights, but future specs could each record source admission differently.

### Owner/gate

Program engineering method + each adopting spec research/Ponytail gate.

### Required evidence schema

```text
SOURCE_REPOSITORY
SOURCE_COMMIT
SOURCE_PATH
SOURCE_BLOB_OR_DIGEST
COPYRIGHT_ORIGIN
LICENSE_OR_PERMISSION_BASIS
THIRD_PARTY_STATUS
ATTRIBUTION_REQUIREMENTS
SECURITY_REVIEW
ADOPTION_CLASS=USE|ADAPT|STUDY|BENCHMARK|DEFER|REJECT
AUTHORIZED_BY
```

Absence of a provable rights basis forces `STUDY/BENCHMARK` or `DEFER`, not code reuse.

## 16. Cross-gap dependency check

No new top-level spec is necessary if ownership is enforced as follows:

```text
004/005 = optional derived temporal/graph intelligence
006     = canonical temporal memory and promotion semantics
007     = context + principal/grant + execution-admission foundation
009     = trusted vertical proof including temporal/promotion safety
010/011 = canonical document state + edit/history UX
013/014 = model/web consumers of 007 execution authority
018     = organization policy extension
021     = extension/skill lifecycle and held-out evolution gates
```

This preserves the existing dependency spine rather than adding donor-shaped phases.

## 17. New strategic kill criteria

Future specs must be willing to reject donor-inspired complexity when any of these are true:

```text
TEMPORAL_RERANK_GAIN_NOT_MATERIAL -> reject/defer RoMem-like derived temporal layer
MEMORY_RESIDENCY_GAIN_NOT_MATERIAL -> use simpler context policy
CONFIRMATION_FRICTION_EXCEEDS_SAFETY_GAIN -> redesign, do not silently auto-promote
DERIVED_EDIT_CANNOT_ROUNDTRIP -> do not expose editable derived surface
SANDBOX_POLICY_NOT_ENFORCEABLE -> deny requested execution mode
SKILL_OPTIMIZATION_FAILS_HELD_OUT_GENERALIZATION -> reject auto-evolution path
SKILL_EVAL_LEAKAGE_DETECTED -> invalidate optimization evidence
SOURCE_RIGHTS_UNPROVEN -> no code reuse
```

## 18. Final gap disposition

```text
TENCENT_SOURCE_GAP_REVIEW=COMPLETE
GAPS_IDENTIFIED=14
GAPS_OWNED_OR_GATED=14
NEW_SPEC_IDS=0
KNOWN_NEW_SEMANTIC_OVERLAP_WITHOUT_OWNER=0
KNOWN_NEW_AUTHORIZATION_BYPASS=0
R1_CHANGED=NO
PRODUCT_IMPLEMENTATION_AUTHORIZED=NO
```
