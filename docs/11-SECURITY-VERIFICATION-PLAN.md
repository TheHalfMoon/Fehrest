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
