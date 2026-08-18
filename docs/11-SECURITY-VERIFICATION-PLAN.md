# L. Security Verification Plan

**Status:** PROPOSED — awaiting adversarial review
**Date:** 2026-08-17

Security verification is designed before implementation so that controls are testable by construction. GLM-5.3's later adversarial review is a gate, **not the only gate** — a program that depends on one external review has no internal safety property.

---

## 1. Principles

1. **Every control in [C](02-THREAT-MODEL.md) has a test.** An untested control is a claim.
2. **Boundary controls are CI-blocking. Defence-in-depth controls are reported, not blocking.** The [threat model's controls table](02-THREAT-MODEL.md#6-controls-summary-by-mechanism) marks which is which; conflating them means a soft failure can block a release while a hard failure passes.
3. **Fail closed in tests too.** A security test that cannot run counts as failed, never skipped.
4. **Adversarial corpora are versioned artifacts**, grown on every finding and never shrunk.
5. **Findings become regression tests permanently.**

---

## 2. Static analysis

| Tool | Scope | Gate |
|---|---|---|
| **CodeQL** | Core language(s) | Blocking on high/critical |
| **Semgrep** | All source, incl. custom Fehrest rules (§2.1) | Blocking on custom-rule violations |
| **Type checking** | Strict mode everywhere | Blocking |
| **Lint (security rules)** | All source | Blocking |

### 2.1 Custom Semgrep rules — the invariants that decay silently

These encode architectural invariants that ordinary review misses because each individual violation looks reasonable:

| Rule | Detects | Protects |
|---|---|---|
| `no-path-from-agent` | A path-typed value reaching a filesystem call from an agent-facing handler | [ADR-0009](09-TECHNOLOGY-DECISIONS.md#adr-0009--agents-address-objects-by-id-never-by-path), [T-7](02-THREAT-MODEL.md#t-7--path-traversal) |
| `no-authz-bypass` | A tool handler reachable without the authorization chokepoint | [I-10](01-ARCHITECTURE-CONSTITUTION.md#i-10--agents-receive-explicitly-bounded-access), [T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin) |
| `no-llm-on-index-path` | A provider call inside ingestion, indexing or startup | [R-1](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) |
| `no-network-in-core` | Non-loopback I/O in a core module | [I-2](01-ARCHITECTURE-CONSTITUTION.md#i-2--core-functionality-requires-no-network) |
| `no-derived-to-canonical` | A canonical write whose input is a derived read | [R-2](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules) |
| `no-secret-in-event` | Credential-shaped values reaching event serialisation | [T-21](02-THREAT-MODEL.md#t-21--credential-exfiltration) |
| `no-actor-supplied-timestamp` | `recorded_at` assigned from request data | [T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse) |
| `no-mutable-memory-axis` | Direct assignment to `basis`, `verification`, `lifecycle` or `resolution` outside the event projection | [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended) |
| `no-collapsed-memory-status` | Any type, API or serialisation that merges the four axes into one status value | [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended), [R2-04](reviews/F1-R2-RECONCILIATION.md) |
| `no-confidence-in-resolution` | `confidence_diagnostic` reaching any comparison inside the resolver | [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution), [R2-04](reviews/F1-R2-RECONCILIATION.md) |
| `no-actor-supplied-basis` | `basis` assigned from request data | [F §3.3](05-MEMORY-MODEL.md#33-the-fehrest-evidence-and-trust-model) |
| `no-unenveloped-agent-response` | An agent-facing handler serialising content by any path other than the core response envelope | [R-9](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules), [R2-03](reviews/F1-R2-RECONCILIATION.md) |
| `no-canonical-ref-to-disposable` | A T1/T2 event referencing a `DERIVED_DISPOSABLE` locator | [D §5.5](03-CANONICAL-DATA-MODEL.md#55-spilled-locators-have-a-declared-durability-class), [R2-11](reviews/F1-R2-RECONCILIATION.md) |
| `no-pending-in-authoritative-path` | A `PENDING` memory reaching a resolver result, authoritative section, or capability evaluation | [R-12](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules), [R2-06](reviews/F1-R2-RECONCILIATION.md) |
| `no-authority-in-ui` | Memory resolution, supersession, authorization, canonical write or identity allocation implemented in the UI package | [I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface) |

**One rule was renamed and seven added in F1-R2** (`no-mutable-epistemic-status` became `no-mutable-memory-axis` when the single enum was decomposed). `no-mutable-memory-axis`, `no-actor-supplied-timestamp` and `no-actor-supplied-basis` are the ones most likely to be violated by a well-meaning refactor, because all three look like ordinary field assignment. `no-collapsed-memory-status` and `no-unenveloped-agent-response` exist because both defects are *additive*: nothing breaks when someone adds a convenient flattened status or a bespoke response shape, which is exactly why a human reviewer will not catch it.

---

## 3. Dependency and supply chain

| Tool | Ecosystem | Cadence | Gate |
|---|---|---|---|
| **OSV-Scanner** | All | Every PR + daily | Blocking on high/critical |
| **cargo-audit / cargo-deny** | Rust | Every PR | Blocking; also license and duplicate policy |
| **npm/pnpm audit** | JS | Every PR | Blocking on high/critical |
| **pip-audit** | **Python sidecar** | Every PR + daily | Blocking |

`pip-audit` is called out because the sidecar is 32 packages / 130 MB ([E-3](research/EVIDENCE_LOG.md#e-3--graphify-dependency-weight-and-installed-footprint)) and its upstream already tracks CVEs in its optional HTTP stack with pinned floors. This is the largest untracked surface in the plan if left unscanned.

**Supply-chain controls.** Lockfiles required in every ecosystem; a build that cannot resolve a lockfile fails rather than floating. Donor commits pinned ([registry pinning rule](research/FEHREST_SOURCE_REGISTRY.md)). **No auto-update of the sidecar with the app.** Provenance-ledger CI rules ([registry §11](research/FEHREST_SOURCE_REGISTRY.md#11-code-provenance-ledger)) including the check that fails when a ledger entry points at a path that no longer exists — the rule that stops the ledger decaying into fiction. Release signing and SLSA provenance deferred but scheduled before public distribution.

---

## 4. Fuzzing

| Target | Harness | Trigger |
|---|---|---|
| Frontmatter parser | `cargo-fuzz`/libFuzzer | Continuous |
| Markdown link extractor | " | Continuous |
| Event-log record parser | " | Continuous |
| Sidecar JSON parser | " | Continuous |
| Extraction-schema validator | " | Continuous |
| Context-package serialiser | " | Nightly |
| **Sidecar extraction path** | File-mutation fuzzing over C-ADVERSARIAL | Nightly |

**Priority order:** the event-log parser first — it is the only component whose corruption is unrecoverable, since canonical history cannot be rebuilt. Frontmatter second, as it carries identity.

ClusterFuzzLite from Phase 4, when parsers land ([SRC-097](research/FEHREST_SOURCE_REGISTRY.md#10-security-verification-toolchain)).

The sidecar target is where [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is decided. Fehrest does not control 28 upstream grammars ([T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities)); the question is whether the sidecar boundary contains what they do. Crashes in upstream grammars are reported upstream and mitigated locally by resource caps and per-file non-fatal failure — a crash is acceptable, an escape is not.

---

## 5. Property testing

| Property | Protects |
|---|---|
| Identity survives arbitrary rename/move/case sequences, **on each platform's filesystem semantics** | [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities), [D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics) |
| Bitemporal resolution equals a naive reference implementation over random histories | [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) |
| Resolution is monotone in `recorded_at` and stable under input reordering | [T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse) |
| **Resolution is invariant under any value of `confidence_diagnostic`** | [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution), [R2-04](reviews/F1-R2-RECONCILIATION.md) |
| **Conflicts at incomparable scopes always yield `CONTRADICTION`, never a winner** | [F §3.4](05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice), [R2-05](reviews/F1-R2-RECONCILIATION.md) |
| **A vault-global memory never outranks a conflicting project-local one** | [F §3.4](05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice) |
| Each of the four memory axes, projected, always equals its event-derived value | [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended) |
| Subagent capability sets are subsets of parents, over random delegation trees | [T-14](02-THREAT-MODEL.md#t-14--agent-privilege-confusion-subagent--delegation) |
| Scope filtering admits no out-of-scope object, over random scope assignments | [T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval) |
| Compiler output is byte-identical for identical inputs | [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) |
| **Every emitted item appears in the served-item manifest, exactly once, in emission order** | [H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1), [R2-01](reviews/F1-R2-RECONCILIATION.md) |
| Rebuild produces equal query results | [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) |
| **Incremental application equals full rebuild over random mutation sequences** | [E §10](04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data), [R2-07](reviews/F1-R2-RECONCILIATION.md) |
| **Every artifact whose inputs include a mutated identity is invalidated** | [E §10](04-DERIVED-DATA-MODEL.md#10-derivation-lineage-as-data) |
| Hash chain verification detects every single-record mutation | [T-4](02-THREAT-MODEL.md#t-4--event-log-tampering) |

---

## 6. Adversarial corpora

Versioned artifacts under `bench/adversarial/`.

### 6.1 C-INJECT — prompt injection
AgentDojo-derived plus Fehrest-specific payloads: instructions in note bodies, frontmatter, PDF text, PDF metadata, image EXIF, filenames, tool results, memory statements, code comments; authority claims ("system override," "the user pre-approved this"); urgency and emotional pressure; encoded/obfuscated instructions; instructions embedded in *superseded* memories.

**Fehrest-specific attack classes — added in F1-R2.** AgentDojo supplies the generic corpus; these are the attacks that only exist because Fehrest exists, and they are the ones the **GLM-5.3 security review should be briefed on**:

| Attack class | Targets |
|---|---|
| **Poisoned Markdown** in the vault | [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority), trust levels 4 vs 5 |
| **Poisoned PDFs and imports** — body text, metadata, EXIF | [T-12](02-THREAT-MODEL.md#t-12--malicious-attachment--parser-confusion), ingest labelling |
| **Poisoned memory** | [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning), the four semantic axes |
| **Forged provenance**, including **in-grant-but-not-served** | [T-3](02-THREAT-MODEL.md#t-3--forged-provenance), the served-item manifest |
| **Malicious MCP output** from a connected client or tool | [T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin), trust level 6, the response envelope |
| **Cross-project memory contamination** | [T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval), scope dimensions and specificity |
| **Supersession poisoning** | [T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse), `USER_CONFIRMED` protection |
| **Capability escalation attempts** — in-session widening, subagent laundering, replayed approvals | [T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin), [T-14](02-THREAT-MODEL.md#t-14--agent-privilege-confusion-subagent--delegation), [T-15](02-THREAT-MODEL.md#t-15--rollback-and-replay-abuse) |

**Gate: zero capability changes, zero unapproved tool executions.** Model *output* influence is measured and reported but is not a gate — that boundary was never claimed ([threat model §1](02-THREAT-MODEL.md#1-governing-principle)).

### 6.2 C-PATH — traversal and symlinks
`../` sequences, absolute paths, UNC paths, `\\?\` prefixes, NTFS alternate data streams, reserved device names (`CON`, `NUL`, `AUX`), trailing dots/spaces, Unicode normalisation tricks, overlong encodings, symlinks and junctions pointing outside the vault, symlink loops, TOCTOU swaps.
**Gate: zero escapes, on all three platforms.** Windows is tested first, since it is both the founder's environment and the weakest confinement platform ([T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix)).

### 6.3 C-MALFORMED — hostile vault files
10 MB frontmatter, invalid YAML, invalid UTF-8, BOM variants, 10^6 links, cyclic links, duplicate IDs, malformed IDs, zip bombs, polyglots, deeply nested structures, files that change during read.
**Gate:** no crash, no corruption, no unbounded resource use, no silent data alteration.

### 6.4 C-POISON — memory poisoning
Agent-asserted false constraints; forged provenance attempts; supersession of human-confirmed decisions; backdated `valid_from`; contradictory floods; cross-scope writes.

**Added in F1-R2:** **in-grant-but-not-served evidence claims** ([R2-02](reviews/F1-R2-RECONCILIATION.md)) — the memory cites a real object inside the session's grant that was never in any manifest served to it; **high-confidence conflict flooding** ([R2-04](reviews/F1-R2-RECONCILIATION.md)) — the attacker asserts contradicting memories at maximum `confidence_diagnostic` to win resolution, which must have **no effect whatsoever**; **vault-global contamination** ([R2-05](reviews/F1-R2-RECONCILIATION.md)) — an agent attempts to write or widen a memory to vault scope in order to reach another project; **pending escalation** ([R2-06](reviews/F1-R2-RECONCILIATION.md)) — an unconfirmed candidate is manoeuvred into an authoritative section, a capability grant, or a supersession.

**Gate:** all poisoned memories traceable to actor and session, and bulk-revocable by provenance. **Plus: zero successful in-grant-but-not-served evidence claims, zero confidence-driven resolution wins, zero cross-project contamination, zero pending escalations.**

### 6.5 C-TAMPER — log integrity
Single-byte edits, record deletion, reordering, splicing, truncation, rollback to an earlier log, replay of a valid log.
**Gate:** 100% detection. **Note the honest scope:** this verifies *tamper-evidence*, not tamper-resistance — a local-first single-user system cannot prevent the file's owner from editing it ([T-4](02-THREAT-MODEL.md#t-4--event-log-tampering)).

---

## 7. Capability and isolation tests

| Test | Asserts |
|---|---|
| `test_deny_by_default` | Empty grant permits nothing, including read |
| `test_grant_immutable_in_session` | No path widens a grant mid-session |
| `test_chokepoint_coverage` | Every tool handler is reachable only via authorization — a coverage assertion, not a convention |
| `test_sidecar_readonly` | Sidecar cannot write anywhere in the vault |
| `test_sidecar_no_egress` | Zero outbound connections during a full extraction, loopback-only namespace |
| `test_no_credentials_in_sidecar` | Sidecar environment contains no secrets |
| `test_platform_enforcement_matrix` | **Reported** enforcement equals **measured** enforcement per platform |
| `test_no_unlabelled_content_path` | **Every** agent-facing read path returns the core envelope with trust level, provenance, the four axes and supersession intact ([R2-03](reviews/F1-R2-RECONCILIATION.md)) |
| `test_no_python_required` | Full core suite passes with no Python interpreter present ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)) |
| `test_core_suite_headless` | Full core suite passes with no UI built or running ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)) |

The last test is the one that keeps [T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix) honest: a platform that overstates its confinement fails CI. This is adopted from the donor's practice of reporting partial enforcement rather than claiming uniform safety ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)).

---

## 8. Recovery tests

Every scenario in [N](13-RECOVERY-MODEL.md) has an automated test that kills or corrupts the system at a specific point and asserts: no canonical data loss, automatic detection, automatic or clearly-guided recovery, and a recorded event describing what happened.

Fault injection points: mid-file-write, mid-event-append, mid-index-transaction, mid-rebuild, sidecar SIGKILL, disk-full, read-only filesystem, clock jump backwards.

**Added in F1-R2 ([R2-13](reviews/F1-R2-RECONCILIATION.md)) — hostile environment injection:** sharing violation / file lock during read and during atomic rename; watcher-event flood above the escalation threshold; cloud placeholder file presented in place of content; sync-driven content revert to a prior known revision; conflict-copy file carrying a duplicate embedded UUID; checkpoint invalidated or deleted between runs.

**And environment testing on real clients, not simulations:** the [N §3A](13-RECOVERY-MODEL.md#3a-hostile-filesystem-and-sync-environments) suite runs against **real OneDrive on Windows** and **real iCloud Drive on macOS** before support for either is claimed. Simulating a sync client tests the simulation.

The clock-jump case matters more than it appears: `recorded_at` is system-assigned and monotonicity is assumed by resolution ordering ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)). A backward clock jump must be detected and recorded rather than silently producing out-of-order history.

---

## 9. Review gates

| Gate | When | Blocking |
|---|---|---|
| Threat-model review of each new subsystem | Design time | Yes |
| Security review of every PR touching auth, paths, events, memory writes, IPC | Per PR | Yes |
| Full internal adversarial review | Before each phase exit | Yes |
| **GLM-5.3 external adversarial review** | Before implementation authorization | Yes |
| ↳ *briefed on* | The Fehrest-specific attack classes in [§6.1](#61-c-inject--prompt-injection), and on whether [cap-std](research/FEHREST_SOURCE_REGISTRY.md#src-112--cap-std) or another Rust-native capability strategy materially improves the filesystem boundary | — |
| Independent penetration test | Before public release | Yes |

---

## 10. Release criteria

No release without: all boundary-control tests passing; zero unresolved high/critical advisories; all adversarial corpora passing their gates; fuzzers run ≥ 24 h with no new reachable crashes; the platform enforcement matrix accurate; the provenance ledger complete and CI-verified; and **a written statement of known residual risks** shipped with the release.

That last item is a hard requirement. [T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities) (28 upstream grammars), [T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix) (Windows confinement) and [T-19](02-THREAT-MODEL.md#t-19--local-process-reads-the-vault) (co-resident processes) are accepted risks, not solved problems. Shipping without saying so would be the dishonest kind of security.

---

## 11. What this plan does not cover

| Gap | Why | When |
|---|---|---|
| Formal verification of the policy engine | Disproportionate for v1's small policy space | If policy grows complex |
| Side-channel and timing attacks | Single-user local threat model | Multi-user |
| Hardware and OS compromise | Out of scope; nothing above the OS can defend it | Never |
| At-rest encryption | Key custody unsolved for local-first | Separate ADR |
| Sync-channel security | Sync deferred | With sync |
| Untrusted plugin sandboxing | No plugin system in v1; WASI seam preserved | With plugins |
| Model-output safety | Fehrest bounds privilege, not persuasion | Not Fehrest's boundary |

---

## 12. Handoff note — GLM-5.3 security/cyber review

> **ADDED PRE-GLM.** A reviewer handoff, not a review. **No security review has been performed here**, and nothing in this section is a finding.

**Attack these, particularly:**

| # | Surface | Why it is on this list |
|---|---|---|
| 1 | **Uniform trust-envelope completeness** | [R2-03](reviews/F1-R2-RECONCILIATION.md) found the envelope covered **one of seven** agent-facing read paths. The fix is structural ([G §4.1](06-AGENT-MODEL.md#41-one-envelope-every-read-path)) and `test_no_unlabelled_content_path` is a *claim about coverage* — verify the surface is genuinely enumerable |
| 2 | **Context manifest forgery and tampering** | The served-item manifest ([H §3.2](07-CONTEXT-COMPILER-SPEC.md#32-the-served-item-manifest--permanent-t1)) is new, T1, and now load-bearing for [T-3](02-THREAT-MODEL.md#t-3--forged-provenance). It inherits only the hash chain's tamper-**evidence**, never resistance |
| 3 | **Evidence provenance spoofing** | Specifically the **in-grant-but-not-served** case, which F1's design silently failed |
| 4 | **Pending-memory influence** | [F §5.5](05-MEMORY-MODEL.md#55-pending-confirmation-semantics) claims a `PENDING` item can only make an agent *stop and ask*. Attack that bound — advisory-channel flooding, and any path from advisory to authoritative |
| 5 | **Cross-project and vault-global contamination** | The scope redesign ([F §3.4](05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice)) argues specificity makes the dangerous direction structurally unavailable. Test that, including incomparable selectors |
| 6 | **MCP authorization assumptions** | **MCP is transport, not authorization** ([T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin)). The official Rust SDK is a preferred *implementation* candidate ([SRC-114](research/FEHREST_SOURCE_REGISTRY.md#src-114--official-mcp-rust-sdk)) and changes nothing about the boundary — verify the adapter sits below the chokepoint |
| 7 | **Cedar policy bypass and misconfiguration** | [SRC-113](research/FEHREST_SOURCE_REGISTRY.md#src-113--cedar-for-agents-extends-src-042) is externally verified to **exist**, which is not evidence its authorization model is correct for Fehrest, correctly configured, or bypass-free. **Review it independently** |
| 8 | **cap-std, path, symlink and confinement limits** | [SRC-112](research/FEHREST_SOURCE_REGISTRY.md#src-112--cap-std) is an adoption *candidate*, not a decision. Assess whether it or another Rust-native capability strategy materially improves the boundary, and whether [ADR-0009](09-TECHNOLOGY-DECISIONS.md#adr-0009--agents-address-objects-by-id-never-by-path) already carries the load |
| 9 | **Windows filesystem semantics** | The weakest confinement platform ([T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix)) **and** the founder's own environment. The new identity design ([D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics)) is untested code |
| 10 | **Imported-content prompt injection** | [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority) bounds privilege, not persuasion — a limit stated deliberately. Attack the privilege bound, and the Fehrest-specific corpus in [§6.1](#61-c-inject--prompt-injection) |
| 11 | **Memory poisoning and supersession attacks** | [T-2](02-THREAT-MODEL.md#t-2--memory-poisoning), [T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse), against the **four-axis** model and the confidence-free resolver, both new |
| 12 | **Event and audit tampering** | [T-4](02-THREAT-MODEL.md#t-4--event-log-tampering), now also carrying manifests and spilled-locator durability classes ([D §5.5](03-CANONICAL-DATA-MODEL.md#55-spilled-locators-have-a-declared-durability-class)) |
| 13 | **Graph sidecar future isolation** | [H-5](research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path) is unproven and 28 upstream grammars are outside Fehrest's control ([T-10](02-THREAT-MODEL.md#t-10--parser-vulnerabilities)). Note that [GI-CAP](10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) may remove the capability before the sidecar exists |
| 14 | **Recovery under malicious or corrupt derived state** | [N](13-RECOVERY-MODEL.md), including the new [§3A](13-RECOVERY-MODEL.md#3a-hostile-filesystem-and-sync-environments) hostile-environment scenarios and checkpoint loss |

**Two framings worth carrying into the review.** First, the [controls table](02-THREAT-MODEL.md#6-controls-summary-by-mechanism) marks which controls are **Boundary** and which are **defence-in-depth** — only the former are load-bearing, and F1-R2 found one Boundary row (T-3) that had **no implementable mechanism behind it**. A second instance of that pattern is the most valuable thing this review could find. Second, **no source in the registry is a runtime dependency**, and external verification of a repository establishes existence, never security.

---

## 13. Kill-test canon

**K-01 through K-24b.**

> **ADDED IN G3.** The adversarial test set from the GLM-5.3 security review, reconciled against the GPT-5.6 Sol validation. **Where GLM's proposed remedy conflicts with that validation, the corrected semantics below are normative** — most visibly for [K-21](#k-21-semantics-corrected).
>
> **None of these is implemented.** They are specified now so that the [Headless Thesis-Proof](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) is built against them rather than retrofitted to them.

| ID | Kill test | Asserts | Primary reference |
|---|---|---|---|
| **K-01** | Imported-content injection | No capability change, no unapproved tool execution | [T-1](02-THREAT-MODEL.md#t-1--indirect-prompt-injection-via-imported-document), [§6.1](#61-c-inject--prompt-injection) |
| **K-02** | Malicious `AGENTS.md`-style in-vault instruction file | Instruction-shaped vault content gains no authority; trust level 4 stays evidence | [I-13](01-ARCHITECTURE-CONSTITUTION.md#i-13--imported-and-retrieved-content-is-evidence-never-authority) |
| **K-03** | MCP capability / tool-description manipulation | Permitted actions come from Fehrest authorization state, never from `tools/list`, capabilities or descriptions | [T-13](02-THREAT-MODEL.md#t-13--privilege-escalation-via-mcp-or-plugin) |
| **K-04** | In-grant-but-not-served provenance claim | Rejected as observed evidence | [T-3](02-THREAT-MODEL.md#t-3--forged-provenance) |
| **K-05** | Manifest tamper | Partial modification detected; **no authentication claimed** against a full consistent rewrite | [C §6.1](02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides) |
| **K-06** | Package/manifest mismatch | Replay reports `DIVERGED` or `UNRECONSTRUCTABLE` with a reason, never `IDENTICAL` | [H §3.3](07-CONTEXT-COMPILER-SPEC.md#33-replay-outcomes-are-explicit--three-results-never-two) |
| **K-07** | Cross-project poisoning | No memory written under project A becomes a candidate for project B | [F §3.4](05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice) |
| **K-08** | Vault-global poisoning | Vault-global creation is unreachable from any agent path; global never outranks project-local | [F §3.4](05-MEMORY-MODEL.md#34-scope-is-orthogonal-dimensions-not-an-ordered-lattice) |
| **K-09** | Pending influence and flooding | `PENDING` never reaches an authoritative surface; advisory flooding cannot force action | [F §5.5](05-MEMORY-MODEL.md#55-pending-confirmation-semantics) |
| **K-10** | Temporal resurrection | A superseded or expired memory cannot be returned as current state | [F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution) |
| **K-11** | Duplicate UUID | Surfaced as an identity conflict; neither file silently discarded | [D §3.2](03-CANONICAL-DATA-MODEL.md#32-identity-across-filesystem-operations) |
| **K-12** | Symlink escape | Read fails at the containment boundary | [T-8](02-THREAT-MODEL.md#t-8--symlink-and-junction-attacks) |
| **K-13** | Windows reparse point / junction escape | Same, on the weakest confinement platform | [T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix) |
| **K-14** | Authorize/open swap (TOCTOU) | The bytes served are the object authorized — post-open verification, not pre-open checking | [T-9](02-THREAT-MODEL.md#t-9--filesystem-race-conditions) |
| **K-15** | Git rename / case storm | Identity survives; no duplicate objects allocated; bulk change escalates to reconciliation | [D §3.3](03-CANONICAL-DATA-MODEL.md#33-filesystem-identity-and-path-semantics) |
| **K-16** | Poisoned derived SQLite | Poisoned rows cannot grant access, redirect a read outside the root, or substitute an object | [E §12](04-DERIVED-DATA-MODEL.md#12-derived-state-is-untrusted-for-authority) |
| **K-17** | Poisoned FTS / hostile `MATCH` syntax | Literal input never activates FTS5 query syntax; pathological queries bounded | [E §13.2](04-DERIVED-DATA-MODEL.md#132-fts5-match-is-a-query-language-not-a-string) |
| **K-18** | Event replay / reorder | Partial tamper detected; rollback surfaced; **no authentication claimed** | [T-4](02-THREAT-MODEL.md#t-4--event-log-tampering) |
| **K-19** | Graph identity injection | Extractor IDs never become canonical identity; collisions surfaced | [G-ID-1…4](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) |
| **K-20** | Provenance / trust truncation | An item is `FULL`, `TRUNCATED` (envelope intact) or `OMITTED` — never emitted stripped | [H §4](07-CONTEXT-COMPILER-SPEC.md#4-pipeline) |
| **K-21** | Scripted user-authority path | **See corrected semantics below** | [C §3.1](02-THREAT-MODEL.md#31-the-local-root-of-trust-g3-h1) |
| **K-22** | Derived path vault escape | No derived path value opens a resource outside the authorized root | [E §12.3](04-DERIVED-DATA-MODEL.md#123-required-properties) |
| **K-23** | Envelope serialization forgery | Content cannot create a second machine-owned item or forge trust, provenance or section identity | [G §4.3](06-AGENT-MODEL.md#43-two-layers-typed-internal-envelope-canonical-serialization) |
| **K-24** | Concurrent canonical writers | One writer per vault; forks detected and surfaced, **never auto-merged** | [D §9](03-CANONICAL-DATA-MODEL.md#9-inter-process-single-writer-discipline) |
| **K-24b** | Permanent-state amplification | Local resource-safety bounds hold; rejections explicit and audited; **no canonical state silently discarded** | [O §13](14-PERFORMANCE-BUDGETS.md#13-local-resource-safety-bounds) |

### K-21 semantics, corrected

> **This is the one place where GLM's proposed remedy is not adopted, and the reason matters.**

GLM's K-21 tested whether a **script** could reach a user-authority transition. Under the root of trust now stated in [C §3.1](02-THREAT-MODEL.md#31-the-local-root-of-trust-g3-h1), **that test cannot pass and should not be written**: a process holding the user's OS authority is not claimed to be distinguishable from the user, and any mechanism that appeared to distinguish it — TTY presence being the obvious candidate — is defeated by a process that allocates a PTY.

**The invariant actually tested is narrower and genuinely enforceable:**

> An **agent, MCP, or untrusted-content path** — one **without user-authority interface access** — cannot mint user authority.

That covers the actor class the product actually exposes, and it is structural rather than behavioural: the transition does not exist on the agent surface at all ([G §2.4](06-AGENT-MODEL.md#24-the-user-authority-surface-is-separate-from-the-agent-surface)).

**If the threat model is ever widened to include hostile same-user processes, K-21 must become stricter — but only after a real authentication mechanism exists.** Writing the stricter test first produces a test that fails for correct code, and the usual response to that is to weaken the test rather than build the mechanism.

### What the kill-test canon does not do

It does not establish security. **Passing every test above means the specified attacks were tried and did not work** — not that the model is sound, and not that the [§7.1 non-claims](02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make) have quietly become claims. The corpora rule in [§1 principle 4](#1-principles) applies: this set grows on every finding and is never shrunk.
