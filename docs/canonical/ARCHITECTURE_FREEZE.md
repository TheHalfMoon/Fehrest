# Fehrest — Architecture Freeze

```
ARCHITECTURE:                FROZEN
SECURITY_ARCHITECTURE:       FROZEN_FOR_IMPLEMENTATION_PROOF
PRODUCT_IMPLEMENTATION:      NOT AUTHORIZED
HEADLESS_THESIS_PROOF:       READY_FOR_FOUNDER_AUTHORIZATION — NOT STARTED
```

**Freeze date:** 2026-08-18
**Canonical repository:** `TheHalfMoon/Fehrest` (private, `main`, size 0, no implementation)

**This document is the authoritative entry point to the frozen architecture.** It does not restate the package; it states what is fixed, what is conditional, what is open, and what must happen before any code is written. Every clause links to the document that owns it.

---

## 1. What freeze means — and does not

**Freeze means:** the architecture is sufficiently specified and reviewed to authorize a **bounded** implementation *after explicit founder approval*.

**Freeze does not mean:**

| Not implied | |
|---|---|
| Every future feature is decided | Many are deliberately open (§10) |
| Every dependency is selected | None is adopted (§12) |
| Every benchmark has passed | **None has been run** (§11) |
| Every hypothesis is proven | Several are explicitly falsifiable (§9) |
| Every deferred subsystem is authorized | None is (§9, §10) |
| Architecture can never change | It changes under §13 change control |

**Most importantly: freeze is not implementation authorization.** See §14.

---

## 2. Freeze provenance

```
GATE HISTORY
  F0     discovery
  F1     initial architecture and planning
  G1     GPT adversarial architecture review
  F1-R1  reconciliation                        -> G1-R  GPT delta review
  G2     Codex independent adversarial review  -> GPT G2 validation
  F1-R2  final architectural reconciliation    -> GPT F1-R2 delta review
         pre-G3 audit and source corrections
  G3     GLM-5.3 dedicated security review     -> GPT G3 validation
         G3 security reconciliation            -> GPT final security delta

SECURITY LINEAGE
  GLM_REVIEWED_CANDIDATE     bdda3d297282098282cdd67b65472c4e48cb7407
  GLM_VERDICT                G3_SECURITY_PASS_WITH_REQUIRED_RECONCILIATION
  GLM_COUNTS                 CRITICAL=0  HIGH=2  MEDIUM=7  LOW=5  INFO=4
  SECURITY_RECONCILIATION    efeb19d9bb9be600a8956901b4754462dee4c46a
  GPT_FINAL_SECURITY_DELTA   G3_SECURITY_FINAL_ACCEPTED
                             SECURITY_RECONCILIATION_CLEAN

FREEZE_BASE                  efeb19d9bb9be600a8956901b4754462dee4c46a
FINAL_FREEZE_COMMIT          REPORTED_EXTERNALLY_AFTER_COMMIT
```

*(The freeze commit's own SHA is reported out-of-band. A commit SHA hashes the tree containing the field, so an embedded "final commit" can never be simultaneously present and correct.)*

**"Security accepted" means the specification is accepted.** It does **not** mean implementation security is proven — the kill tests in §11 remain unrun.

---

## 3. Product thesis — frozen

> **Fehrest — The Context OS for Humans and Agents.**
>
> Humans write. Agents work. Fehrest remembers.
>
> **Agents are disposable. Memory is not.**

Fehrest is a **local-first, human-owned shared long-term memory and context layer** between humans and replaceable AI agents.

**The thesis is not notes, not RAG, not vector search, not chat history, not a knowledge graph.** It is the *combination*:

```
open canonical knowledge
+ durable work/experience history
+ temporal, supersession-aware memory
+ provenance
+ bounded deterministic context compilation
+ agent-access boundaries
```

**The thesis remains empirically falsifiable** through the [Headless Rust Thesis-Proof](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) and [B-7a/B-7b](../10-BENCHMARK-PLAN.md#b-7--agent-continuation-the-defining-experiment). Freezing the architecture does **not** freeze the thesis as true. Full statement: [A — Product Thesis](../00-PRODUCT-THESIS.md).

---

## 4. Frozen foundational decisions

**Seventeen decisions are FROZEN.** Each names the document that owns it. Changing any is a Class C, D or E change (§13).

| # | Decision | Owner |
|---|---|---|
| **F-CORE-01** | **Local-first, zero mandatory services.** Usable with no account, no network, no API key, no Fehrest cloud, no database server, no vector or graph database server, no mandatory model | [I-1](../01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default)–[I-4](../01-ARCHITECTURE-CONSTITUTION.md#i-4--core-functionality-requires-no-paid-api) |
| **F-CORE-02** | **Open, human-owned canonical data.** Important knowledge has an open, local, inspectable representation. Derived state may be internal **only** while fully disposable and rebuildable | [I-5](../01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended), [I-6](../01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) |
| **F-CORE-03** | **Rust Core.** Correctness, security and data semantics are Rust-owned. TypeScript/React is presentation only. Python only behind optional bounded process boundaries | [ADR-0010](../09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language), [I-16](../01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface), [I-17](../01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python) |
| **F-CORE-04** | **Path is not identity.** Paths are locations; embedded Fehrest UUIDs are identities, independent of path | [I-15](../01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities), [D §3.3](../03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics) |
| **F-CORE-05** | **Content is evidence, never authority.** Untrusted content cannot obtain application authority by being retrieved, ranked, remembered, summarised, graphed, quoted or placed in context | [I-13](../01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority), [C §1](../02-THREAT-MODEL.md#1-governing-principle) |
| **F-CORE-06** | **Temporal memory.** What *was* true, what *is* true, when Fehrest learned it, what is superseded, what is unresolved. **Contradiction is never silently collapsed** | [F §4](../05-MEMORY-MODEL.md#4-bitemporality), [ADR-0008](../09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) |
| **F-CORE-07** | **Orthogonal memory semantics.** `basis`, `verification`, `lifecycle`, `resolution` stay separate. **No mixed total-order enum. Raw LLM confidence is not truth authority** | [I-12](../01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended), [F §3.3](../05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model) |
| **F-CORE-08** | **Context Compiler** — the defining capability under test. Bounded, permission-aware, temporal- and supersession-aware, provenance-backed, trust-labelled, deterministic where specified, manifested, honest about omission and truncation | [H](../07-CONTEXT-COMPILER-SPEC.md) |
| **F-CORE-09** | **Served-item manifest.** Permanent T1 composition evidence of what was served. Exact historical *content* reconstruction remains conditional on retained source revisions | [H §3.2](../07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1), [I-14](../01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) |
| **F-CORE-10** | **Derived state has no authority.** Rebuildable, non-canonical, **untrusted for authority**. Derived paths are locator hints. Authorization scope comes from canonical state. **Root confinement and post-open identity verification are distinct requirements** | [E §12](../04-DERIVED-DATA-MODEL.md#12-derived-state-is-untrusted-for-authority) |
| **F-CORE-11** | **Single-user root of trust.** OS account integrity is the user root of trust. Fehrest does **not** claim to authenticate human presence against a malicious same-user process. **Agent, MCP and untrusted-content surfaces still cannot mint user authority** | [C §3.1](../02-THREAT-MODEL.md#31-the-local-root-of-trust-g3-h1), [G §2.4](../06-AGENT-MODEL.md#24-the-user-authority-surface-is-separate-from-the-agent-surface) |
| **F-CORE-12** | **Honest audit integrity.** Unkeyed chains give partial-tamper, corruption, reorder and truncation evidence. They give **no** cryptographic authentication against a complete consistent same-user rewrite | [C §6.1](../02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides), [T-4](../02-THREAT-MODEL.md#t-4--event-log-tampering) |
| **F-CORE-13** | **Canonical single writer.** Inter-process single-writer semantics. Forks are surfaced and **never silently auto-repaired** | [D §9](../03-CANONICAL-DATA-MODEL.md#9-inter-process-single-writer-discipline) |
| **F-CORE-14** | **Safe context serialization.** Typed machine-owned envelope metadata is structurally distinct from untrusted content; content cannot forge trust, provenance or section metadata. **No claim of LLM behavioural injection immunity** | [G §4.3](../06-AGENT-MODEL.md#43-two-layers-typed-internal-envelope-canonical-serialization) |
| **F-CORE-15** | **Resource safety, not product quotas.** Local safety bounds only — **not** commercial quotas, daily limits, trial exhaustion or vendor-controlled availability. Prefer coalescing, dedup, idempotency and bounded concurrency before rejection | [O §13](../14-PERFORMANCE-BUDGETS.md#13-local-resource-safety-bounds) |
| **F-CORE-16** | **Ingestion fails toward exclusion.** Supported-content allowlist. `.fehrest/` and `.git/` are not ordinary user knowledge. Unsupported classes require future ingestion gates | [D §10](../03-CANONICAL-DATA-MODEL.md#10-ingestion-boundary--supported-content-allowlist) |
| **F-CORE-17** | **Security claim boundaries** — the frozen negative claims in §5 | [C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make) |

---

## 5. Security boundaries — frozen negative claims

**Fehrest v1 explicitly does NOT claim:**

```
 1  protection against OS or root compromise
 2  confidentiality against arbitrary same-user processes
 3  cryptographic proof of physical-human authentication in the headless model
 4  full-history tamper resistance against a complete consistent same-user rewrite
 5  immunity from prompt injection at the level of model persuasion
 6  any automatic secret-detection or DLP guarantee
 7  multi-user security
 8  sync-channel security, before sync exists
 9  a process sandbox from Cedar
10  a process sandbox from MCP
11  an arbitrary-code sandbox from cap-std
12  that derived-state corruption is only an availability issue
```

**Each is a limit of the declared model, not a defect awaiting a fix.** Changing any requires deliberately re-scoping the threat model with its own adversarial review (Class D, §13). Full text: [C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make).

**What is positively guaranteed** is separated by class in [C §6.1](../02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides): **correctness** · **integrity and partial-tamper evidence** · **authentication — currently empty**.

---

## 6. Canonical versus derived — frozen

| | **Canonical** | **Derived** |
|---|---|---|
| Recomputable | **No** — losing it loses knowledge | **Yes, always** |
| Contents | Vault files, attachments, event journal, memory assertions, sidecars, **served-item manifests**, vault identity, schema version | Indexes, FTS, graph, vectors, caches, projections, checkpoints |
| Authority | **The only source of authorization-relevant scope** | **None.** Untrusted for authority |
| On deletion | Irreplaceable loss | Inconvenience — rebuild |
| Backup | Required | Never needed |

**Two consequences are frozen because each was corrected during review:** `.fehrest/` is **not** disposable — only its derived subtree is ([E §1](../04-DERIVED-DATA-MODEL.md#1-two-classes-of-state-inside-fehrest)); and **rebuildability does not make derived corruption a mere availability problem** ([E §12](../04-DERIVED-DATA-MODEL.md#12-derived-state-is-untrusted-for-authority)).

---

## 7. Engineering method — frozen

| Discipline | Role |
|---|---|
| **GitHub Spec Kit** | Canonical specification-driven development workflow |
| **Ponytail** | Canonical necessity / reuse / minimum-implementation discipline |

```
SPEC -> CLARIFY -> PLAN -> CHECKLIST -> TASKS -> ANALYZE
     -> PONYTAIL GATE
          does it need to exist?
          already implemented in Fehrest?
          Rust std/core?
          platform primitive?
          approved existing dependency?
          smaller correct solution?
     -> IMPLEMENT -> TEST -> BENCHMARK (where required)
     -> SECURITY -> REVIEW -> CONVERGE
```

**Ponytail may never minimise** authorization boundaries, canonical-data integrity, security controls, recovery correctness, provenance, privacy, data-loss prevention, required accessibility, or invariant tests.

**Neither is a product runtime dependency** ([R-11](../01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)). Full method: [S](../19-ENGINEERING-METHOD.md), [ADR-0014](../09-TECHNOLOGY-DECISIONS.md#adr-0014--engineering-method-spec-kit--ponytail).

---

## 8. First implementation slice — frozen boundary

**Target: HEADLESS RUST FEHREST THESIS-PROOF** ([Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice)).

**Included — the minimum needed to test the thesis safely:**

```
Rust process
+ explicit single-user OS-account trust model
+ no agent path capable of minting user authority
+ ordinary supported open canonical files
+ stable embedded Fehrest UUID identity
+ root-confined filesystem access
+ post-open UUID verification
+ canonical scope authority
+ derived locator hints only
+ SQLite / FTS5 with hardening baseline
+ explicit durable memory writes only
+ temporal / supersession resolver
+ supersession graph validity
+ canonical single-writer semantics
+ minimum T1 event / audit records
+ honest hash / tamper-evidence semantics
+ served-item manifests
+ typed trust / provenance envelope
+ unambiguous model-visible serialization
+ context item / package budget atomicity
+ local resource-safety bounds
+ supported-content ingestion allowlist
+ deterministic bounded Context Compiler
+ benchmark hooks required by Phase T
```

**Excluded, unless an implementation requirement proves otherwise:**

```
desktop UI · editor · CRDT · sync · cloud · MCP · Cedar engine
Graphify production sidecar · graph runtime · vectors
automatic memory promotion · automatic confirmation queue
plugin system · analytics studio · dashboard engine · mobile
distributed processing · mandatory model or provider
```

**And no security subsystem beyond the declared threat model:** no MAC, keychain or TPM; no authentication subsystem; **no TTY/PTY detection as authentication**; no external notarization. Each would *exceed* the declared model rather than satisfy it ([C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make)).

---

## 9. Hypothesis-gated — NOT frozen as inevitable architecture

**These are recorded as conditional. None is production-authorized by this freeze.**

| Component | Status | Gate |
|---|---|---|
| **Graph Intelligence** | `CURRENT CORE PRODUCT HYPOTHESIS` · `FALSIFIABLE` · **`NOT PRODUCTION-AUTHORIZED`** | Must **first** materially improve controlled outcomes over the simpler Fehrest Core at acceptable cost — [GI-CAP (B-13)](../10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) before any integration, then [GI-BENCH](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix). [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) permits **removal** |
| ↳ **Graphify** | Implementation *candidate* — optional, replaceable, Python sidecar only, **not a canonical dependency** | [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) |
| **Automatic memory promotion** | `DEFERRED / BENCHMARK-GATED` | [B-5](../10-BENCHMARK-PLAN.md#b-5--memory-promotion-quality). Phase T uses **explicit writes only** |
| **CRDT / collaboration** | `DEFERRED / REQUIREMENT-GATED` | [Collaboration/CRDT Gate](../20-FUTURE-GATES.md#4-collaborationcrdt-gate). Candidates are research inputs only |
| **Vectors** | `DERIVED / OPTIONAL / BENCHMARK-GATED` — **not canonical** | [ADR-0007](../09-TECHNOLOGY-DECISIONS.md#adr-0007--retrieval-is-lexical-first-vectors-are-optional), [B-3](../10-BENCHMARK-PLAN.md#b-3--retrieval-quality-by-stage) |
| **Editor / UI / canvas** | `OPEN / FUTURE-GATED` — **no editor or canvas architecture is authorized by this freeze** | [Editor Gate](../18-EDITOR-GATE.md), [Visual/Canvas Gate](../20-FUTURE-GATES.md#2-visualcanvas-engine-gate) |

**Recording a component here is not a plan to build it.** Each may be removed on evidence, and [F-3](../17-FAILURE-CONDITIONS.md#f-3--graph-intelligence-does-not-deliver-material-benefit-at-acceptable-cost) exists precisely so the largest of them can be.

---

## 10. Deferred and open founder decisions

**Deliberately NOT resolved by this freeze.** Converting an open decision into an accepted one to make a freeze document look complete is the specific failure this section prevents.

| # | Open decision | Why it does not block Phase T | Resolved at |
|---|---|---|---|
| 1 | **Desktop shell** ([ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell)) | Phase T is headless. [I-16](../01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) guarantees the Core never depends on a shell | Phase 3 / before Phase 7 |
| 2 | **v1 target wedge ratification** ([Q-8](../16-OPEN-QUESTIONS.md#q-8--v1-target-wedge-provisionally-accepted-for-planning)) | Phase T tests the thesis mechanism, which is wedge-independent. The wedge shapes *product* consequences, not the proof | Before Phase 3E; before any v1 scope commitment |
| 3 | **Editor-gate weights** ([Q-16](../16-OPEN-QUESTIONS.md#q-16--editor-gate-weights-and-agent-editability)) | No editor in Phase T. Weights are contingent on decision 2 | Before Phase 3E |
| 4 | **Licence and publication timing** ([Q-1a](../16-OPEN-QUESTIONS.md#q-1--repository-identity-closed)) | Nothing is published, pushed or distributed | Before first distribution; before any copyleft code reuse |
| 5 | **`AI OFF` product positioning** ([Q-4](../16-OPEN-QUESTIONS.md#q-4--is-ai-off-a-first-class-product-or-a-compliance-mode)) | Phase T is `AI OFF` by construction — explicit writes only, no model required | After [B-5](../10-BENCHMARK-PLAN.md#b-5--memory-promotion-quality) at Phase 4 |
| 6 | **Frontmatter intrusion ergonomics** ([Q-5](../16-OPEN-QUESTIONS.md#q-5--how-intrusive-may-fehrest-be-with-user-files)) | The mechanism is decided ([ADR-0004](../09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque)); only UX intrusiveness is open, and Phase T has one user | Dogfooding, Phase 7 |

**Also still open and scheduled:** long-term schema compatibility ([ADR-0015](../09-TECHNOLOGY-DECISIONS.md#adr-0015--long-term-canonical-schema-compatibility)), context-package bodies vs manifests ([Q-15](../16-OPEN-QUESTIONS.md#q-15--should-context-packages-store-bodies-not-just-manifests)), storage layout ([ADR-0013](../09-TECHNOLOGY-DECISIONS.md#adr-0013--storage-layout-provisional)).

---

## 11. Required gates — REQUIREMENT frozen, RESULT not

> **Nothing below has been run. No gate is marked passed.** The freeze fixes what must be satisfied; it asserts nothing about whether it will be.

| Gate | Status |
|---|---|
| **Kill tests K-01 … K-24b** ([L §13](../11-SECURITY-VERIFICATION-PLAN.md#13-kill-test-canon)) | **REQUIRED — NOT PASSED.** Future implementation gates |
| **B-0** event-volume measurement | REQUIRED — not run. Gates all event-tiering and retention parameters |
| **B-7a / B-7b** thesis proof | REQUIRED — not run. **Only B-7b may falsify the thesis** |
| **B-9** rebuild equivalence | REQUIRED — not run |
| **B-12** FTS5 ranking/rebuild determinism | REQUIRED — not run |
| **B-13 GI-CAP** graph capability | REQUIRED before any graph integration — not run |
| Filesystem identity matrix ([D §3.3](../03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics)) | REQUIRED — not run |
| Confirmation-load tests | REQUIRED at the automatic-memory gate — not run |
| Adversarial corpora C-INJECT / C-PATH / C-MALFORMED / C-POISON / C-TAMPER | REQUIRED — not run |

**"Security accepted" means the specification passed review.** The implementation properties still have to pass these tests, and until they do, no security property is demonstrated.

---

## 12. Research and donor freeze

```
FEHREST BROAD DONOR DISCOVERY:  FROZEN
```

**The donor registry is evidence. It is not architecture.** Future donor research must be **gap-driven**.

| Valid trigger | Invalid trigger |
|---|---|
| Measured FTS failure · security finding · failed graph experiment · ratified collaboration requirement · editor gate · new platform correctness requirement | *"Collect more projects because they look interesting"* |

**Donor adoption rule.** An observed or pinned source revision is **not** an adoption pin. Future dependency or code reuse must pass: requirement → Ponytail necessity gate → rights/licence/provenance → deliberately reviewed revision → security and advisory review → benchmark where applicable → implementation authorization. **No donor is grandfathered into production by appearing in research** ([registry §14.12](../research/FEHREST_SOURCE_REGISTRY.md#1412-an-observed-revision-is-not-an-adoption-pin)).

---

## 13. Change control after freeze

| Class | Change | Requires |
|---|---|---|
| **A** | Editorial, non-semantic — wording, formatting, links, typos | Nothing. Update freely |
| **B** | Implementation detail **within** frozen invariants — mechanism selection, schema field naming, parameter values | Spec Kit, and an ADR where the choice is durable |
| **C** | **Architecture-semantic** change — a component's contract, a phase boundary, a benchmark's decision authority | **Explicit ADR + review** |
| **D** | **Security-boundary or foundational-invariant** change — any `F-CORE-*`, any constitutional invariant, any §5 negative claim | **Dedicated adversarial / security review** |
| **E** | **Product-thesis or founder-direction** change — the thesis in §3, the first slice in §8, the v1 scope | **Founder authorization + architecture reconsideration** |

**Legitimate reasons to reopen frozen architecture after freeze:**

```
measured implementation evidence
a new security or correctness requirement
a failed hypothesis or benchmark
a founder product decision
```

**Every one must be captured through an explicit ADR or spec update.** Architecture that changes without a recorded reason is architecture that was never frozen.

**Weakening an invariant without following its amendment procedure** ([B §5](../01-ARCHITECTURE-CONSTITUTION.md#5-amendment-procedure)) remains the specific failure mode the constitution exists to prevent — and freeze does not relax it.

---

## 14. Implementation authorization — NOT GRANTED

```
ARCHITECTURE_FROZEN
IMPLEMENTATION_BLOCKED_PENDING_FOUNDER_AUTHORIZATION
```

**This freeze does not authorize implementation.** Before any production or scaffold code begins, the founder must **explicitly authorize**:

> **HEADLESS RUST THESIS-PROOF IMPLEMENTATION**

**None of the following is implementation authorization:**

```
"freeze"      "ready"      "accepted"      "security pass"
"reconciled"  "complete"   "G3_SECURITY_FINAL_ACCEPTED"
```

Each describes the state of the **planning package**. None describes permission to write code.

### Current state

```
ARCHITECTURE:                 FROZEN
SECURITY_ARCHITECTURE:        FROZEN_FOR_IMPLEMENTATION_PROOF
PRODUCT_IMPLEMENTATION:       NOT AUTHORIZED
HEADLESS_THESIS_PROOF:        READY_FOR_FOUNDER_AUTHORIZATION — NOT STARTED
UI:                           NOT STARTED
GRAPH PRODUCTION INTEGRATION: NOT AUTHORIZED
MCP:                          NOT STARTED
AUTOMATIC MEMORY:             NOT AUTHORIZED
REMOTE PUSH:                  NOT PERFORMED
```

### What the founder is being asked to authorize

**Not the product. One bounded experiment**, whose purpose is to find out — cheaply, and before the expensive architecture exists — whether the thesis in §3 survives contact with measurement. The slice in §8 is scoped so that a negative result costs a slice rather than a product.

**The honest expectation, stated before authorization rather than after:** [F-1](../17-FAILURE-CONDITIONS.md#f-1--compiled-context-does-not-beat-a-competent-agent-with-plain-file-tools) is the condition most likely to fire. LongMemEval-V2's own reporting shows the best memory system beating an off-the-shelf coding agent by **3.2 points**, and [B-7a](../10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) now also has to beat a maintained LLM Wiki. Authorizing Phase T is authorizing the attempt to falsify Fehrest, not the assumption that it works.

---

## Reading order

| Order | Document |
|---|---|
| 1 | **This document** — what is frozen |
| 2 | [Evidence Log](../research/EVIDENCE_LOG.md) — every measurement, and the [unmeasured quantities](../research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2) recorded as such |
| 3 | [A — Product Thesis](../00-PRODUCT-THESIS.md) · [B — Constitution](../01-ARCHITECTURE-CONSTITUTION.md) · [C — Threat Model](../02-THREAT-MODEL.md) |
| 4 | [Failure Conditions](../17-FAILURE-CONDITIONS.md) — what would force redesign |
| 5 | [Open Questions](../16-OPEN-QUESTIONS.md) — including where the plan most wants to be attacked |
| 6 | Review deltas: [F1-R1](../reviews/F1-R1-RECONCILIATION.md) · [F1-R2](../reviews/F1-R2-RECONCILIATION.md) · [G3 Security](../reviews/G3-SECURITY-RECONCILIATION.md) |

---

**`G4_ARCHITECTURE_FROZEN_READY_FOR_FOUNDER_AUTHORIZATION`**
