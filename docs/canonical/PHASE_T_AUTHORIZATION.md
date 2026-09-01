# Phase T — Founder Authorization and Governance Addendum

**Date:** 2026-08-18
**Applies to:** [Architecture Freeze](ARCHITECTURE_FREEZE.md) · [Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice)
**Freeze base:** `0e0d78711194a8b69d95d13d998e9b407ba351bd` (G4)

This document records what the founder has authorized, what remains unauthorized, and three governance facts that arrived with the authorization. **It grants no authority beyond what is written here.**

---

## 1. Implementation authorization — ACTIVE

```
FEHREST_HEADLESS_RUST_THESIS_PROOF_IMPLEMENTATION:  AUTHORIZED
```

The [§14 gate](ARCHITECTURE_FREEZE.md#14-implementation-authorization--not-granted) of the architecture freeze is satisfied. Implementation of the Phase T slice may proceed.

### Authorized

```
Phase T governance updates          Ponytail minimization review
Spec Kit bootstrap                  Rust scaffolding
Spec Kit constitution alignment     bounded Phase T Rust implementation
specify / clarify / plan            tests
checklist / tasks / analyze         applicable G3 kill tests
                                    local benchmark harness + execution
                                    local commits
```

### NOT authorized

```
full Fehrest product implementation   graph runtime / vectors / embeddings
frontend / UI / Tauri desktop app     CRDT / collaboration / sync / cloud
editor / canvas                       plugin system
MCP                                   automatic memory promotion
Cedar                                 automatic confirmation queue
Graphify production integration       analytics studio / dashboard engine
mobile / distributed runtime          mandatory model or provider
remote push / PR creation / merge / release / publication
```

**Authority is not inferable outside this boundary.** A capability absent from the authorized list is unauthorized, including capabilities that would be convenient, adjacent, or obviously next.

### Status preserved

```
ARCHITECTURE:                 FROZEN
SECURITY_ARCHITECTURE:        FROZEN_FOR_IMPLEMENTATION_PROOF
HEADLESS_RUST_THESIS_PROOF:   AUTHORIZED
PRODUCT_IMPLEMENTATION:       BOUNDED_TO_PHASE_T
UI:                           FUTURE_WORKFLOW_SELECTED - IMPLEMENTATION_NOT_AUTHORIZED
MCP:                          NOT_AUTHORIZED
GRAPH_PRODUCTION_INTEGRATION: NOT_AUTHORIZED
AUTOMATIC_MEMORY:             NOT_AUTHORIZED
REMOTE_PUSH:                  NOT_AUTHORIZED
MERGE:                        NOT_AUTHORIZED
```

---

## 2. `FOUNDER_SELECTED_FUTURE_UI_WORKFLOW` — v0

The founder has selected **v0** as the **future** Fehrest UI design and generation workflow.

**v0 may later be used for:** visual exploration, frontend generation and iteration, product UI prototyping, component iteration.

**v0 is NOT:**

| Not | Because |
|---|---|
| A Fehrest runtime dependency | The Core never calls it |
| A Fehrest cloud dependency | [F-CORE-01](ARCHITECTURE_FREEZE.md#4-frozen-foundational-decisions) — zero mandatory services |
| A canonical-data dependency | Nothing canonical is produced by it |
| A security authority | It decides no boundary |
| Part of Phase T | Not used, not invoked, not present |
| Authorization to implement UI now | UI remains unauthorized |

**Expected future flow:**

```
frozen product requirements -> durable product/design context -> v0
   -> generated frontend source -> ordinary local Fehrest repository
   -> quality / design / a11y review -> normal source control and code review
```

**The invariant that bounds it:** *if the UI disappears, Fehrest Core remains operable* ([I-16](../01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)). Generated frontend source enters the repository as ordinary reviewed code, never as a live dependency on a generator.

**[ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) (desktop shell) remains OPEN.** Selecting a UI *generation workflow* decides nothing about the *shell that hosts it* — the same association-is-not-an-argument reasoning that kept ADR-0011 open when the Core language was decided.

**Phase T spends no effort on frontend aesthetics, canvas technology, editor architecture or desktop shell.**

---

## 3. `FOUNDER_REPRESENTED_DONOR_USE_AUTHORIZATION`

**The founder represents that Fehrest is authorized to use all donor and source materials the founder has supplied to the project** — study, copy, modify, adapt, integrate, where useful.

This removes one question from the critical path: *"do we have founder permission to use this supplied source?"*

### What it does not remove

```
AUTHORIZATION  !=  PROVENANCE
```

**Every actual code or content reuse still records:**

```
upstream owner              imported/copied/adapted portion
exact repository            Fehrest destination
exact commit or tag         modification notes
exact source path           observed upstream license
source/test paths           founder authorization status
                            import date
                            update strategy
                            replacement/exit strategy where relevant
```

**Three limits, stated because a broad authorization invites all three mistakes:**

1. **No fabricated permission documents.** Only the founder's *representation* is recorded. Where documentary permission genuinely exists it is cited; where it does not, nothing is claimed.
2. **Upstream licence obligations survive.** If an actual upstream licence carries obligations — attribution, NOTICE propagation, copyleft — those obligations are preserved regardless of founder authorization. The founder can authorize Fehrest's *use*; they cannot waive a third party's licence terms.
3. **Founder permission does not override the gates.** [Ponytail necessity](../19-ENGINEERING-METHOD.md#2-the-ponytail-necessity-gate), security review, dependency admission and provenance recording all still apply. *"We are allowed to"* is not *"we should."*

---

## 4. New donor — Impeccable

```yaml
source: pbakaus/impeccable
repository: https://github.com/pbakaus/impeccable
observed_revision: f88b2837a7d7c3182e46307bbbb091a1ed547571
observed_date: 2026-08-18
observed_license: Apache-2.0
class: [CODE_DONOR, DEVELOPMENT_TOOL, DESIGN_SYSTEM_DONOR,
        UI_QUALITY_REFERENCE, AGENT_WORKFLOW_REFERENCE]
decision: STUDY / ADAPT / FUTURE_UI_USE
runtime: NO
phase_t: NO PRODUCT INTEGRATION
future_gate: UI / FRONTEND QUALITY GATE
founder_use_authorization: YES (founder representation, section 3)
```

Full record: [registry §14.13](../research/FEHREST_SOURCE_REGISTRY.md#1413-impeccable--future-uiquality-donor).

**Admitted under the research-freeze gap rule** ([registry §14.9](../research/FEHREST_SOURCE_REGISTRY.md#149-research-freeze--now-binding)): founder-supplied, and it closes a documented future UI/design-quality gap. **`FEHREST BROAD DONOR DISCOVERY` remains `FROZEN`** — this is not a reopening.

### Phase T hard boundary

```
DO NOT install Impeccable        DO NOT install React
DO NOT run Impeccable            DO NOT use v0
DO NOT run npx impeccable        DO NOT generate frontend files
DO NOT create Tauri files        DO NOT create PRODUCT.md / DESIGN.md for future UI
```

Record the donor; continue the headless Rust proof.

---

## 5. What this addendum did not change

| Unchanged | |
|---|---|
| **Frozen architecture** | All 17 `F-CORE-*` decisions stand |
| **Security boundaries** | All 12 negative claims stand |
| **Hypothesis gates** | Graph, automatic memory, CRDT, vectors, editor/UI all still gated |
| **Open decisions** | All 9 remain open, including ADR-0011 |
| **Research freeze** | Active |
| **First implementation slice** | Unchanged — [Phase T](ARCHITECTURE_FREEZE.md#8-first-implementation-slice--frozen-boundary) |

**The scope of Phase T was not widened by this authorization.** It was authorized as written.
