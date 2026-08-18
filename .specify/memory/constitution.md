# Fehrest Implementation Constitution

**Version:** 1.0.0 · **Ratified:** 2026-08-18 · **Applies to:** Phase T and every later implementation phase

> **This is an implementation-governance projection of the frozen Fehrest architecture. It is NOT a new architecture source.**
>
> Authority order whenever anything here is ambiguous or appears to conflict:
>
> ```
> 1. docs/canonical/ARCHITECTURE_FREEZE.md       frozen architecture
> 2. docs/reviews/G3-SECURITY-RECONCILIATION.md  security reconciliation
> 3. docs/10-BENCHMARK-PLAN.md                   what decides what
> 4. docs/17-FAILURE-CONDITIONS.md               what would force redesign
> 5. docs/19-ENGINEERING-METHOD.md               Ponytail
> ```
>
> If this document ever contradicts the freeze, **the freeze wins and this document is wrong.**

---

## Core Principles

### I. Local-first, zero mandatory services

No account, network, API key, Fehrest cloud, database server, vector or graph server, or mandatory model is required for any core capability. The test suite passes offline. *(F-CORE-01)*

### II. Rust owns the Core

Correctness, security and data semantics are Rust-owned. No business-critical state semantic may live outside the Rust Core. Phase T is headless — CLI only. *(F-CORE-03, I-16, I-17)*

### III. Canonical knowledge stays open and inspectable

Important canonical user knowledge has an open, local, inspectable representation. Derived state may be internal **only** while fully disposable and rebuildable. *(F-CORE-02)*

### IV. Paths are locations; IDs are identities

Object identity is an embedded Fehrest UUID, independent of path. **A path is never hashed into an identity.** *(F-CORE-04)*

### V. Content is evidence, never authority (NON-NEGOTIABLE)

Instruction, evidence and control planes stay distinct. Untrusted content cannot obtain application authority by being retrieved, ranked, remembered, summarised, quoted or placed in context. *(F-CORE-05)*

### VI. Derived state has no authority (NON-NEGOTIABLE)

Derived state is `NON-CANONICAL · REBUILDABLE · UNTRUSTED FOR AUTHORITY`. Derived paths are `UNTRUSTED_LOCATOR_HINT`. Authorization-relevant scope comes from canonical state.

**Root containment and post-open UUID verification are two independent requirements. Neither substitutes for the other.** *(F-CORE-10)*

### VII. Temporal truth is separate from recorded truth

Valid time and recorded order are distinct axes. Supersession is explicit. **Contradiction stays visible** — never silently collapsed. *(F-CORE-06)*

### VIII. Memory semantics stay orthogonal

`basis` · `verification` · `lifecycle` · `resolution` are four independent fields. No mixed total-order enum. `PENDING` is non-authoritative. **Raw LLM confidence can never force a truth winner.** *(F-CORE-07)*

### IX. Manifests record what was actually emitted

A served-item manifest records items **actually emitted** — not retrieved, not ranked, not selected. Permanent T1 composition evidence. Byte-identical replay is **not** promised once source revisions are gone. *(F-CORE-09)*

### X. Every agent-visible read carries the trust envelope (NON-NEGOTIABLE)

Machine-owned metadata — identity, trust, provenance, temporal state, supersession, scope, truncation — travels with every agent-visible content path. **Content is a value; it is never parsed as machine-owned metadata.** *(F-CORE-14)*

### XI. Honest trust boundaries

OS-account integrity is the local user root of trust; Fehrest does **not** claim to authenticate human presence against a same-user process. **Agent surfaces cannot mint user authority.** Hash chains give partial-tamper evidence, **not** authentication. *(F-CORE-11, F-CORE-12)*

### XII. Canonical state has one writer

Inter-process single-writer semantics per vault. A second writer fails visibly. **Canonical forks are surfaced, never silently auto-repaired.** *(F-CORE-13)*

### XIII. Resource safety, not product quotas

Local safety bounds only — request size, item size, package size, concurrency, event size, disk reserve, permanent-state amplification. **Never** commercial quotas, trial exhaustion, daily limits or vendor-controlled availability. Prefer coalescing, dedup, idempotency and bounded concurrency before rejection. *(F-CORE-15)*

### XIV. Ingestion fails toward exclusion

Supported-content allowlist. `.fehrest/` and `.git/` are not ordinary user knowledge. Unsupported classes need explicit future gates. *(F-CORE-16)*

### XV. Ponytail — minimum correct implementation (NON-NEGOTIABLE)

Before writing code, in order: does it need to exist for Phase T? · already implemented? · Rust `std`? · platform primitive? · approved existing dependency? · smaller correct solution? · only then implement the minimum.

**Ponytail may never minimise** authorization, vault containment, identity verification, durable-state correctness, recovery, audit integrity, provenance, security metadata, bounds, platform correctness, or required tests.

### XVI. Hypothesis-gated systems stay out until their gate passes

No graph, no vectors, no embeddings, no CRDT, no sync, no MCP, no Cedar, no automatic memory promotion, no UI. **Security kill tests are implementation gates, not documentation.** *(freeze §9, §11)*

### XVII. The product thesis remains falsifiable

Phase T exists to test whether Fehrest deserves to exist. **A negative result is a successful experiment.** Complexity may not be added after negative evidence in order to rescue the thesis. *(F-1)*

---

## Development Workflow

```
SPEC -> CLARIFY -> PLAN -> CHECKLIST -> TASKS -> ANALYZE
     -> PONYTAIL GATE -> IMPLEMENT -> TEST -> BENCHMARK
     -> SECURITY -> REVIEW -> CONVERGE
```

**Analyze is a hard gate.** Implementation does not begin while `ANALYZE_BLOCKERS > 0`, `FROZEN_ARCHITECTURE_CONFLICTS > 0`, or `UNAUTHORIZED_FEATURES_IN_PLAN > 0`.

**Quality gates at every meaningful checkpoint:**

```
cargo fmt --check
cargo check
cargo clippy --all-targets --all-features -- -D warnings
cargo test
```

**Structure bias:** one Rust package with internal modules. Split a crate only for a real security, compile-time, versioning or process boundary. No empty scaffolding, no single-implementation traits, no factories for one type, no plugin framework, no async without actual concurrency, no `unsafe` without written justification.

**Every runtime dependency needs an admission record** — capability required, why std/platform is insufficient, candidates, exact version, licence, advisory status, unsafe/FFI, build.rs, proc-macro, features, why minimum, removal path.

**Prefer explicit failure.** No hidden fail-open fallbacks. No shell execution. No network requirement. No dynamic SQLite extension loading.

**Platform honesty.** Never claim `WINDOWS PASS` or `MACOS PASS` without native execution on that platform. Mark `PENDING_NATIVE_WINDOWS_EXECUTION` / `PENDING_MACOS_EXECUTION` instead of faking a pass.

**Experimental formats.** Any Phase T persistence format is labelled `EXPERIMENTAL_PHASE_T_FORMAT` / `NOT_PRODUCT_FORMAT_FREEZE`.

---

## Governance

**Amendment.** This constitution is a projection. It is amended when the frozen architecture is amended — never independently. Changing a `NON-NEGOTIABLE` principle requires the corresponding freeze change class: **Class D** for security boundaries and foundational invariants, **Class E** for the product thesis.

**Authorization boundary.** Phase T is authorized. Nothing outside that boundary is — including capabilities that are convenient, adjacent or obviously next. **If a generated task proposes an unauthorized feature, the task is wrong**; remove or defer it.

**Compliance.** Every checkpoint verifies the four quality gates, Ponytail classification for new capabilities, and dependency admission for new dependencies. Complexity is justified against Principle XV or removed.

**Version:** 1.0.0 | **Ratified:** 2026-08-18 | **Last Amended:** 2026-08-18
