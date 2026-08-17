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
| `no-mutable-epistemic-status` | Direct assignment to `epistemic_status` outside the event projection | [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended) |

The last two are the ones most likely to be violated by a well-meaning refactor, because both look like ordinary field assignment.

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
| Identity survives arbitrary rename/move/case sequences | [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities) |
| Bitemporal resolution equals a naive reference implementation over random histories | [ADR-0008](09-TECHNOLOGY-DECISIONS.md#adr-0008--memory-is-bitemporal-with-deterministic-resolution) |
| Resolution is monotone in `recorded_at` and stable under input reordering | [T-5](02-THREAT-MODEL.md#t-5--memory-supersession-abuse) |
| Projected epistemic status always equals event-derived status | [I-12](01-ARCHITECTURE-CONSTITUTION.md#i-12--inference-is-never-silently-promoted-to-fact-amended) |
| Subagent capability sets are subsets of parents, over random delegation trees | [T-14](02-THREAT-MODEL.md#t-14--agent-privilege-confusion-subagent--delegation) |
| Scope filtering admits no out-of-scope object, over random scope assignments | [T-6](02-THREAT-MODEL.md#t-6--unauthorized-cross-project-retrieval) |
| Compiler output is byte-identical for identical inputs | [I-14](01-ARCHITECTURE-CONSTITUTION.md#i-14--model-visible-state-is-reconstructable-provenance-linked-scope-authorized-and-auditable) |
| Rebuild produces equal query results | [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable) |
| Hash chain verification detects every single-record mutation | [T-4](02-THREAT-MODEL.md#t-4--event-log-tampering) |

---

## 6. Adversarial corpora

Versioned artifacts under `bench/adversarial/`.

### 6.1 C-INJECT — prompt injection
AgentDojo-derived plus Fehrest-specific payloads: instructions in note bodies, frontmatter, PDF text, PDF metadata, image EXIF, filenames, tool results, memory statements, code comments; authority claims ("system override," "the user pre-approved this"); urgency and emotional pressure; encoded/obfuscated instructions; instructions embedded in *superseded* memories.

**Gate: zero capability changes, zero unapproved tool executions.** Model *output* influence is measured and reported but is not a gate — that boundary was never claimed ([threat model §1](02-THREAT-MODEL.md#1-governing-principle)).

### 6.2 C-PATH — traversal and symlinks
`../` sequences, absolute paths, UNC paths, `\\?\` prefixes, NTFS alternate data streams, reserved device names (`CON`, `NUL`, `AUX`), trailing dots/spaces, Unicode normalisation tricks, overlong encodings, symlinks and junctions pointing outside the vault, symlink loops, TOCTOU swaps.
**Gate: zero escapes, on all three platforms.** Windows is tested first, since it is both the founder's environment and the weakest confinement platform ([T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix)).

### 6.3 C-MALFORMED — hostile vault files
10 MB frontmatter, invalid YAML, invalid UTF-8, BOM variants, 10^6 links, cyclic links, duplicate IDs, malformed IDs, zip bombs, polyglots, deeply nested structures, files that change during read.
**Gate:** no crash, no corruption, no unbounded resource use, no silent data alteration.

### 6.4 C-POISON — memory poisoning
Agent-asserted false constraints; forged provenance attempts; supersession of human-confirmed decisions; backdated `valid_from`; contradictory floods; cross-scope writes.
**Gate:** all poisoned memories traceable to actor and session, and bulk-revocable by provenance.

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

The last test is the one that keeps [T-18](02-THREAT-MODEL.md#t-18--windows-confinement-is-weaker-than-posix) honest: a platform that overstates its confinement fails CI. This is adopted from the donor's practice of reporting partial enforcement rather than claiming uniform safety ([E-9](research/EVIDENCE_LOG.md#e-9--deepseek-harness-pinned-version-and-adoptable-patterns)).

---

## 8. Recovery tests

Every scenario in [N](13-RECOVERY-MODEL.md) has an automated test that kills or corrupts the system at a specific point and asserts: no canonical data loss, automatic detection, automatic or clearly-guided recovery, and a recorded event describing what happened.

Fault injection points: mid-file-write, mid-event-append, mid-index-transaction, mid-rebuild, sidecar SIGKILL, disk-full, read-only filesystem, clock jump backwards.

The clock-jump case matters more than it appears: `recorded_at` is system-assigned and monotonicity is assumed by resolution ordering ([F §4.2](05-MEMORY-MODEL.md#42-deterministic-resolution)). A backward clock jump must be detected and recorded rather than silently producing out-of-order history.

---

## 9. Review gates

| Gate | When | Blocking |
|---|---|---|
| Threat-model review of each new subsystem | Design time | Yes |
| Security review of every PR touching auth, paths, events, memory writes, IPC | Per PR | Yes |
| Full internal adversarial review | Before each phase exit | Yes |
| **GLM-5.3 external adversarial review** | Before implementation authorization | Yes |
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
