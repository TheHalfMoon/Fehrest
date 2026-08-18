# S. Engineering Method — Spec Kit and Ponytail

**Status:** ACCEPTED — founder decisions D-2 and D-3
**Date:** 2026-08-17 (F1-R2)
**ADR:** [ADR-0014](09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail)

How implementation proceeds **after** founder authorization. Nothing in this document is executed during F1-R2; neither tool has been installed into the project.

> ```
> SPEC KIT AND PONYTAIL ARE DEVELOPMENT AND GOVERNANCE TOOLING.
> NEITHER IS A FEHREST RUNTIME DEPENDENCY.
> ```
>
> Enforced by [R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules): neither may appear in a shipped dependency graph. A build that ships either fails.

---

## 1. Why two disciplines

Fehrest is built largely by AI coding agents against a specification-heavy planning package. That produces two characteristic failures, and they pull in opposite directions:

| Failure | Cause | Discipline that addresses it |
|---|---|---|
| Work drifts from the specification | Nothing binds code to the plan | **Spec Kit** |
| Code accretes | Generating a new implementation is cheaper for an agent than finding the existing one | **Ponytail** |

Either alone makes the other worse. Spec Kit without Ponytail produces well-specified bloat — every specification honoured, the codebase doubled. Ponytail without Spec Kit produces minimal code that solves the wrong problem elegantly.

---

## 2. The Ponytail necessity gate

Before implementing anything new, in order:

| # | Question | If yes |
|---|---|---|
| 1 | **Does this capability need to exist?** | If no — stop. This is the question that saves the most work and is asked the least |
| 2 | **Does Fehrest already implement it?** | Use it. Applies to Fehrest's own code first, including [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice)'s |
| 3 | **Can Rust `std`/`core` or a platform primitive solve it?** | Use that |
| 4 | **Can an already-approved dependency solve it?** | Use that. "Already approved" means present in the [Source Registry](research/FEHREST_SOURCE_REGISTRY.md) with a disposition |
| 5 | **Can the requirement be satisfied with a smaller implementation?** | Build the smaller one |
| 6 | Only then | Implement the minimum correct solution |

### 2.1 What Ponytail may never minimise

```
authorization boundaries       canonical-data integrity
security controls              recovery correctness
provenance                     privacy
data-loss prevention           required accessibility
invariant tests
```

**This list is the decision, not a caveat.** A minimisation discipline applied by an agent optimising for less code will, given the chance, argue that an authorization chokepoint "does not need to exist," that a recovery path is "unreachable in practice," or that an invariant test is "covered by another test." Each argument is locally plausible and globally catastrophic — and each one succeeds by answering Ponytail's own question 1 in the affirmative.

On these paths, **the answer to question 1 is fixed at "yes" by the constitution**, and questions 2–6 apply only to *how*, never to *whether*.

**Fewer tests is never a Ponytail outcome.** Invariant tests are on the exclusion list precisely because they are the cheapest thing to delete and the most expensive thing to lose: they are what makes every invariant in [B](01-ARCHITECTURE-CONSTITUTION.md) a property rather than a slogan.

---

## 3. The Spec Kit lifecycle

```
constitution → specify → clarify → plan → checklist → tasks
             → analyze → implement → converge
```

| Stage | Produces | Fehrest note |
|---|---|---|
| `constitution` | The binding rules for the work | Derived from [B](01-ARCHITECTURE-CONSTITUTION.md); never a second source of invariants |
| `specify` | What is being built and why | Traces to a document in this package |
| `clarify` | Resolved ambiguities | Unresolved ambiguity is recorded, not guessed |
| `plan` | How it will be built | Includes the Ponytail gate result (§2) |
| `checklist` | Verifiable completion criteria | Includes the invariant tests the change must keep green |
| `tasks` | Decomposed work | — |
| `analyze` | Consistency check against the specification | This is where drift is caught |
| `implement` | The code | Rust, per [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language) |
| `converge` | Reconciliation of what was built against what was specified | Divergence is documented, not silently accepted |

**Reduced workflow.** For small bounded work, a shortened lifecycle may be used — at minimum `specify` → `implement` → `analyze`. **The reduction must be justified in writing on the change itself.** An unjustified reduction is how a process becomes a formality, and the justification is what makes the shortcut auditable rather than habitual.

---

## 4. The full loop for a production feature

```
  SPEC KIT
    constitution → specify → clarify → plan → checklist → tasks → analyze
         │
         ▼
  PONYTAIL NECESSITY / REUSE GATE            (section 2)
    need? → already in Fehrest? → std/core? → platform?
          → approved dependency? → smaller? → then implement
         │
         ▼
  IMPLEMENT                                   Rust core (ADR-0010)
         │
         ▼
  TESTS · BENCHMARKS · SECURITY GATES         (K, L)
    invariant tests green · phase benchmarks met
    boundary-control tests CI-blocking
         │
         ▼
  SPECKIT CONVERGE                            built vs specified
         │
         ▼
  INDEPENDENT REVIEW
```

**Two rules govern the loop, and they are the reason it is written down:**

1. **Ponytail never overrides a security or correctness requirement.** Where §2.1 applies, the gate answers *how small*, never *whether*.
2. **Spec Kit never becomes runtime architecture.** It governs how Fehrest is built. It ships in no binary, appears in no dependency graph, and is present in no user's installation ([R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)).

---

## 5. Relationship to the phase plan

Every phase in [P](15-IMPLEMENTATION-PHASES.md) runs its production work through this loop. The loop does **not** replace the phase gates — a phase still exits on executable tests and reported benchmarks, not on process compliance.

**Nothing here is executed during F1-R2.** Spec Kit and Ponytail are stood up as CI/governance tooling at [Phase 0](15-IMPLEMENTATION-PHASES.md#phase-0--foundation-validation), after review gates and explicit founder implementation authorization.

---

## 6. Failure conditions for the method itself

| Finding | Consequence |
|---|---|
| Spec Kit's artifact overhead exceeds its drift-prevention benefit across several features | Default to the reduced workflow, retaining `specify` and `analyze` |
| Ponytail's gate is observed producing under-built code on a security-relevant path despite §2.1 | The exclusion list is insufficiently specific. **Remove the gate from those paths entirely** rather than rewording it |
| Either tool appears in a shipped dependency graph | [R-11](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) violation. Build failure, not a warning |
| Process compliance is used to justify a phase exit that benchmarks do not support | The method has become the goal. Phase gates are executable tests, always |
