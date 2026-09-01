# G3 Security Reconciliation

**Phase:** `G3` security reconciliation — documentation only
**Date:** 2026-08-18
**Canonical repository:** `TheHalfMoon/Fehrest` (private, `main`, size 0, no implementation)
**Next gate:** GPT-5.6 Sol final security delta review → *then* architecture freeze may be considered → founder implementation authorization

**Implementation is NOT authorized. No product code exists.**

### Reviewed state

```
GLM_REVIEWED_HEAD          bdda3d297282098282cdd67b65472c4e48cb7407
GLM_FINAL_VERDICT          G3_SECURITY_PASS_WITH_REQUIRED_RECONCILIATION
GLM_COUNTS                 CRITICAL=0  HIGH=2  MEDIUM=7  LOW=5  INFO=4
                           FREEZE_BLOCKERS=9  IMPL_BLOCKERS=8  DEFERRABLE=9
PRE_RECONCILIATION_HEAD    bdda3d297282098282cdd67b65472c4e48cb7407
FINAL_CANDIDATE_HEAD       REPORTED_EXTERNALLY_AFTER_COMMIT
```

**GLM-5.3 did not mutate this repository.** It reported `PRODUCT_CODE_WRITTEN=NO`, `FILES_MODIFIED=NO`, `COMMITS_CREATED=NO`, `PUSHED=NO`, `MERGED=NO`, `IMPLEMENTATION_AUTHORIZED=NO`. Every change in this reconciliation was made here, against the tree it reviewed.

*(`FINAL_CANDIDATE_HEAD` is reported out-of-band for the reason established pre-GLM: a commit SHA hashes the tree containing the field, so an embedded "current HEAD" can never be both present and correct.)*

---

## 1. What survived

**No foundational trust assumption was found invalid.** The load-bearing architecture stands unchanged and is **not reopened** here:

```
instruction / evidence / control plane separation   pre-retrieval frozen grants
deny-by-default authorization chokepoint            Fehrest-owned identity, not path identity
permanent served-item manifest                      one agent read envelope
four-axis memory semantics                          PENDING non-authoritative state
canonical / derived separation                      conditional historical reconstructability
```

**What G3 found instead were claims stronger than their mechanisms**, and terms used without being defined. Two of the three highest-value findings have the same shape as F1-R2's: a security property asserted in prose with nothing behind it. That is now the package's characteristic failure mode, and §5 names it again.

---

## 2. Validation summary

| GPT verdict | Findings | Handling |
|---|---|---|
| **VALID** | G3-H1, G3-H2, G3-M1–M6, G3-L1–L5, G3-I2, G3-I3, G3-I4 | Applied |
| **PARTIAL** | G3-M7, G3-I1 | Valid risk applied; proposed remedy replaced |
| **REJECT** | none | — |
| **NEEDS_EVIDENCE** | none | — |

**Four GLM remedies were modified rather than adopted** (§4). In each case the *finding* was right and the *fix* would have introduced a worse defect than the one it closed.

---

## 3. Finding-by-finding delta

### 3.1 HIGH

| ID | GPT | Accepted risk | Modified / rejected remedy | Canonical correction | Documents | Freeze | Impl | Tests |
|---|---|---|---|---|---|---|---|---|
| **G3-H1** | VALID | `USER_ASSERTED` / `USER_CONFIRMED` / "explicit user authority" were used without defining **what authenticates the user** on a headless CLI | **TTY/PTY detection as authentication REJECTED.** A same-user process can allocate and drive a PTY, so the check distinguishes nothing while appearing to — converting an honest limit into a false guarantee | **OS account is the local root of trust**, stated explicitly. v1 does not claim to distinguish a human from a same-user process. **Agent and MCP surfaces cannot mint user authority** — a separate control surface holds those transitions | [C §3.1](../02-THREAT-MODEL.md#31-the-local-root-of-trust-g3-h1) · [C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make) · [G §2.4](../06-AGENT-MODEL.md#24-the-user-authority-surface-is-separate-from-the-agent-surface) | ✅ | ✅ | `test_agent_surface_cannot_mint_user_authority`, K-21 |
| **G3-H2** | VALID | "Derived corruption is an availability problem" is **too strong** — semantic poisoning affects scope attribution, ID→location, candidate selection and ranking **before** rebuild | **Post-open UUID verification is necessary but NOT sufficient.** Root containment is independently required; the two failures are disjoint | Derived state = `NON-CANONICAL · REBUILDABLE · UNTRUSTED FOR AUTHORITY`. Two independent guarantees: containment **and** identity. **Canonical scope is the authorization authority** | [E §12](../04-DERIVED-DATA-MODEL.md#12-derived-state-is-untrusted-for-authority) · [T-16](../02-THREAT-MODEL.md#t-16--corrupted-derived-indexes) · [ADR-0006](../09-TECHNOLOGY-DECISIONS.md#adr-0006--sqlite-is-the-derived-store-and-only-the-derived-store) | ✅ | ✅ | K-14, K-16, K-17, K-22 |

### 3.2 MEDIUM

| ID | GPT | Accepted risk | Modified / rejected remedy | Canonical correction | Documents | Freeze | Impl | Tests |
|---|---|---|---|---|---|---|---|---|
| **G3-M1** + **G3-L4** | VALID | Nothing stopped untrusted content from **writing envelope syntax** | **Serialization integrity does NOT imply LLM persuasion immunity**, and **no encoding family is selected here** | Two layers — **typed internal envelope** (content is a value, never metadata) plus **canonical serialization** with six normative properties. Canonical content preserved, never rewritten for display safety | [G §4.3](../06-AGENT-MODEL.md#43-two-layers-typed-internal-envelope-canonical-serialization) | ✅ | ✅ | K-23, serializer fuzz |
| **G3-M2** | VALID | An **unkeyed** hash chain does not authenticate history against a full consistent rewrite | **MAC / keychain NOT required in Phase T.** Key custody would be the same account being defended against | Normative table separating **correctness / integrity-and-partial-tamper-evidence / authentication**. The authentication row is **empty**. "Unforgeable" withdrawn | [C §6.1](../02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides) · [T-4](../02-THREAT-MODEL.md#t-4--event-log-tampering) | ✅ | — | K-05, K-18 |
| **G3-M3** | VALID | No inter-process single-writer discipline for canonical state | Mechanism deliberately not frozen | One canonical writer per vault; a second fails visibly; duplicate sequence, chain forks and journal forks detected; **forks NEVER auto-merged or auto-repaired** | [D §9](../03-CANONICAL-DATA-MODEL.md#9-inter-process-single-writer-discipline) | ✅ | ✅ | K-24 |
| **G3-M4** | VALID | Budget truncation could strip an item's trust and provenance metadata | — | Content + trust + provenance + temporal + supersession + truncation status is **one emission unit**. `FULL` / `TRUNCATED` / `OMITTED`. **Omit rather than emit stripped** | [H §4](../07-CONTEXT-COMPILER-SPEC.md#4-pipeline) | ✅ | ✅ | K-20 |
| **G3-M5** | VALID | Authorized agents can permanently amplify canonical state | **Resource-safety bounds are NOT commercial quotas.** No daily, tier, trial or lifetime limits — those would violate a founder principle | Local resource-safety bounds; prefer coalescing, idempotency and dedup **before** rejection; rejections explicit, audited, local; **never silently discard canonical state** | [O §13](../14-PERFORMANCE-BUDGETS.md#13-local-resource-safety-bounds) | ✅ | ✅ | K-24b |
| **G3-M6** | VALID | No SQLite security posture; FTS5 `MATCH` treated as a string | **Not "SQL parameterization"** — the right-hand side of `MATCH` is its own query language, and a bound parameter is still interpreted as syntax | Extension loading disabled by construction; no untrusted `ATTACH`; `trusted_schema=OFF` or documented equivalent; vault-rooted DB path; bounded resources; **literal FTS expression construction** with length and complexity bounds | [E §13](../04-DERIVED-DATA-MODEL.md#13-sqlite-and-fts5-hardening-baseline) | ✅ | ✅ | K-16, K-17 |
| **G3-M7** | **PARTIAL** | Everything under the vault root was implicitly indexable — `.env`, `.git/`, key material | **Deny-list of secret filenames REJECTED as the primary boundary.** It is a permanent race against unknown filenames and fails toward indexing | **Supported-content allowlist + reserved-path exclusion + explicit opt-in.** `.fehrest/` and `.git/` reserved. Secret patterns remain `DEFENSE_IN_DEPTH` only. Audit metadata kept separate from model-visible metadata | [D §10](../03-CANONICAL-DATA-MODEL.md#10-ingestion-boundary--supported-content-allowlist) | ✅ | ✅ | — |

### 3.3 LOW and INFO

| ID | GPT | Accepted risk | Modified / rejected remedy | Canonical correction | Documents |
|---|---|---|---|---|---|
| **G3-L1** | VALID | Supersession graph had no invalid-edge rules | — | Self-supersession, cycles, cross-vault, prohibited cross-project, PENDING-supersedes-authoritative and incomparable authority transitions rejected as `INVALID_SUPERSESSION`. **Never silently normalised** | [F §6.1](../05-MEMORY-MODEL.md#61-supersession-graph-integrity) |
| **G3-L2** | VALID | Paraphrase flooding of the confirmation queue | **No semantic-duplicate classifier pulled into Phase T** | Phase T has explicit writes only, no auto-promotion and no confirmation queue — the surface is intentionally absent. Requirements retained for the future automatic-memory gate | [F §5.5](../05-MEMORY-MODEL.md#55-pending-confirmation-semantics) |
| **G3-L3** | VALID | A perfectly consistent full rollback is indistinguishable from a legitimate restore without an external anchor | **No remote notarization or cloud authority added to v1** | Documented as an accepted limitation | [C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make) |
| **G3-L5** | VALID | Observed revisions could be read as adoption approvals | — | **`EXTERNALLY_OBSERVED_SOURCE_REVISION` is not an `ADOPTION_PIN`.** Adoption requires a deliberately reviewed revision with recorded rationale, licence, advisory state, source paths and delta since the prior pin | [registry §14.12](../research/FEHREST_SOURCE_REGISTRY.md#1412-an-observed-revision-is-not-an-adoption-pin) |
| **G3-I1** | **PARTIAL** | cap-std is a genuine containment candidate | **Not a sandbox, not an authorization engine, not injection defence, not a substitute for identity verification** | Recorded as a future candidate whose adoption must evaluate whether the no-ambient-`std::fs` discipline is maintainable | [SRC-112](../research/FEHREST_SOURCE_REGISTRY.md#src-112--cap-std) |
| **G3-I2** | VALID | — | — | **Cedar remains deferred.** Phase T uses the minimum explicit deny-by-default Rust model. **Do not build a mini policy language to avoid Cedar** | [SRC-113](../research/FEHREST_SOURCE_REGISTRY.md#src-113--cedar-for-agents-extends-src-042) |
| **G3-I3** | VALID | — | — | **ADR-0011 stays open.** A future Tauri gate must cover IPC, capabilities, CSP, deep links, protocol handlers, drag/drop, clipboard, file URLs, updater trust and shell/process plugins | [ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) |
| **G3-I4** | VALID | — | — | **Protocol discovery is not an authorization grant.** Permitted actions originate from Fehrest authorization state, never from `tools/list`, capabilities or tool descriptions. MCP elicitation may not become a second hidden approval path without an ADR and security review | [G §5](../06-AGENT-MODEL.md#5-transports) |

**Freeze-blocking status:** all 9 freeze blockers closed. **Implementation-blocking:** all 8 closed as *specifications*; they become closed as *code* only when Phase T implements them. **Deferrable:** 9 items remain deferred with their gates named (G3-L2, G3-L3, G3-I1 through G3-I4, and the MCP, desktop and automatic-memory gates).

---

## 4. Remedies modified rather than adopted

Recorded separately because the difference between *"the finding was wrong"* and *"the fix was wrong"* is the most useful thing a reviewer can carry forward. **All four findings below were accepted in full.**

### 4.1 G3-H1 — TTY detection is not authentication

GLM offered interactive-TTY detection as one candidate mechanism for recognising the user.

**Rejected.** A malicious same-user process can allocate and drive a PTY. The check therefore distinguishes **nothing**, while producing an artifact that looks like an authentication boundary in code review, in documentation and in a future security claim. **A control that appears to work is worse than a stated limitation**, because the limitation invites compensating design and the false control forecloses it.

**Adopted instead:** state the root of trust honestly — the OS account — and keep the *enforceable* boundary, which is that agent and MCP paths have no user-authority transition on their surface at all.

### 4.2 G3-H2 — post-open UUID verification does not replace containment

The remedy risked being read as *"verify the UUID after opening, and path traversal stops mattering."*

**It does not.** The two defend disjoint failures:

| Without containment | Without identity verification |
|---|---|
| A read reaches **outside the vault** before any UUID is examined. A file with no Fehrest UUID errors *after* it has been opened and read | A poisoned locator swaps **which in-vault object** is served. Entirely inside the root, so containment never fires |

**Both are required, independently**, and [E §12.1](../04-DERIVED-DATA-MODEL.md#121-two-independent-guarantees--neither-substitutes-for-the-other) says so explicitly.

### 4.3 G3-M2 — no MAC, keychain or notarization in Phase T

GLM proposed an optional OS-keychain MAC path over the event chain.

**Recorded as possible future hardening only.** Under the root of trust now stated, the attacker in scope holds the OS account — and therefore holds the keychain. **A MAC whose key custody is the same account it defends against is ceremony**: it changes the effort required from "rewrite the chain" to "rewrite the chain and re-MAC it," while creating a *stronger-sounding* claim than the mechanism supports.

**Adopted instead:** an honest three-class property table with an **empty authentication row** ([C §6.1](../02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides)). An accurate statement of a weaker property is worth more than a mechanism that overstates a stronger one.

### 4.4 G3-M5 — resource safety is not a product quota

The finding is real: authorized agents can permanently amplify canonical state.

**Rejected as remedies:** daily compile limits, paid-tier limits, trial-style limits, arbitrary lifetime quotas, vendor-controlled waiting queues. Fehrest imposes **no artificial product limits** — that is a founder principle, and a security review is exactly the moment such limits arrive disguised as prudence.

**Adopted instead:** **local resource-safety bounds** — request and event size caps, bounded concurrency, disk-reserve thresholds, bounded pending-approval amplification — with **coalescing, idempotency and deduplication preferred before rejection**, and every rejection explicit, audited, local and non-commercial ([O §13](../14-PERFORMANCE-BUDGETS.md#13-local-resource-safety-bounds)).

### 4.5 G3-M7 — allowlist, not deny-list

GLM proposed detecting secret filenames.

**Rejected as the primary boundary.** A deny-list is a permanent race against filenames nobody has thought of, and it fails in the dangerous direction: **anything unlisted is indexed by default.**

**Adopted instead:** supported-content **allowlist** plus reserved-path exclusion plus explicit opt-in, which fails toward *not* indexing. Secret-pattern detection is retained as `DEFENSE_IN_DEPTH` and is explicitly **not** presented as a DLP guarantee ([C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make)).

### 4.6 K-21 — corrected test semantics

GLM's K-21 tested whether a **script** could reach a user-authority transition. Under the declared threat model that test **cannot pass and should not be written** — a process with the user's OS authority is not claimed to be distinguishable from the user.

**The invariant actually tested** is that an agent, MCP or untrusted-content path *without user-authority interface access* cannot mint user authority. Narrower, enforceable, and structural ([L §13](../11-SECURITY-VERIFICATION-PLAN.md#13-kill-test-canon)).

---

## 5. The pattern across three reviews

Worth naming, because it is now three for three and it predicts where the next finding will come from.

| Round | Characteristic error |
|---|---|
| **F1 → R1** | **Absence of signal read as evidence of absence.** A 404 read as non-existence; a stale mirror read as a dead project |
| **F1-R2** | **An unmeasured number, or an untested engine property, treated as a finding.** 500 events/day; "< 5 confirmations"; FTS5 ranking stability |
| **G3** | **A security claim stronger than its mechanism.** "Unforgeable provenance" over an unkeyed chain; "availability problem" over a poisonable index; "explicit user authority" with no defined authenticator |

All three share one root: **a sentence that reads as established, with nothing underneath it that a test could reach.** The package's defences against this are now structural — the [Evidence Log's unmeasured-quantities table](../research/EVIDENCE_LOG.md#unmeasured-quantities-recorded-as-such-f1-r2), the [security-property table](../02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides), the [explicit non-claims](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make), and the [kill-test canon](../11-SECURITY-VERIFICATION-PLAN.md#13-kill-test-canon).

**For the next reviewer:** the highest-value target is a fourth instance of the same shape — a claim that sounds settled and has no reachable test. [T-3](../02-THREAT-MODEL.md#t-3--forged-provenance) was one, found in F1-R2. G3 found three more. There is no reason to assume the supply is exhausted.

---

## 6. Freeze conditions

All 37 conditions required before the GPT final security delta review are satisfied. Summarised:

| Group | Status |
|---|---|
| Root of trust explicit; same-user limits honest; agent paths cannot mint user authority (1–3) | ✅ [C §3.1](../02-THREAT-MODEL.md#31-the-local-root-of-trust-g3-h1), [G §2.4](../06-AGENT-MODEL.md#24-the-user-authority-surface-is-separate-from-the-agent-surface) |
| Derived paths untrusted; containment independent of UUID; post-open verification; canonical scope authority (4–8) | ✅ [E §12](../04-DERIVED-DATA-MODEL.md#12-derived-state-is-untrusted-for-authority) |
| Typed envelope; serialization unforgeable; **injection immunity NOT claimed** (9–11) | ✅ [G §4.3](../06-AGENT-MODEL.md#43-two-layers-typed-internal-envelope-canonical-serialization) |
| Hash-chain claims calibrated; no MAC subsystem in Phase T (12–13) | ✅ [C §6.1](../02-THREAT-MODEL.md#61-what-each-mechanism-actually-provides) |
| Single-writer semantics; forks surfaced (14–15) | ✅ [D §9](../03-CANONICAL-DATA-MODEL.md#9-inter-process-single-writer-discipline) |
| Budget atomicity; FULL/TRUNCATED/OMITTED (16–17) | ✅ [H §4](../07-CONTEXT-COMPILER-SPEC.md#4-pipeline) |
| Resource-safety bounds, explicitly **not** product quotas (18–19) | ✅ [O §13](../14-PERFORMANCE-BUDGETS.md#13-local-resource-safety-bounds) |
| SQLite extensions; `trusted_schema`; literal FTS `MATCH` (20–22) | ✅ [E §13](../04-DERIVED-DATA-MODEL.md#13-sqlite-and-fts5-hardening-baseline) |
| Ingestion allowlist; `.git/` and `.fehrest/` reserved (23–24) | ✅ [D §10](../03-CANONICAL-DATA-MODEL.md#10-ingestion-boundary--supported-content-allowlist) |
| Supersession cycles rejected (25) | ✅ [F §6.1](../05-MEMORY-MODEL.md#61-supersession-graph-integrity) |
| Rollback limitation documented (26) | ✅ [C §7.1](../02-THREAT-MODEL.md#71-security-claims-fehrest-v1-explicitly-does-not-make) |
| Adoption pins distinguished from observed revisions (27) | ✅ [registry §14.12](../research/FEHREST_SOURCE_REGISTRY.md#1412-an-observed-revision-is-not-an-adoption-pin) |
| Cedar deferred; cap-std unadopted; MCP deferred; desktop ADR open (28–31) | ✅ unchanged |
| Headless Rust Thesis-Proof remains first future build (32) | ✅ [Phase T](../15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice) |
| No product code · no dependency installed · nothing pushed · nothing merged · links resolve (33–37) | ✅ verified at commit |

---

## 7. Remaining deferred security work

| Item | Gate |
|---|---|
| Confirmation-fatigue controls — grouping, amplification bounds, ASK-storm prevention | Future automatic-memory gate |
| cap-std or another Rust-native containment mechanism | Implementation evaluation |
| Cedar policy engine | When MCP, multiple actors or complex policy arrive |
| MCP authorization surface | MCP gate |
| Desktop shell security surface — IPC, CSP, deep links, updater trust | [ADR-0011](../09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) gate |
| Graph sidecar isolation ([H-5](../research/EVIDENCE_LOG.md#h-5--a-single-sidecar-process-is-sufficient-isolation-for-the-extraction-path)) | Phase 3B, **if** [GI-CAP](../10-BENCHMARK-PLAN.md#b-13--gi-cap--graph-intelligence-capability-experiment) retains the capability |
| Stronger-than-OS-account authentication | Only with a deliberately re-scoped threat model |
| At-rest encryption; sync-channel security; multi-user | Unchanged, out of v1 |

**Open founder decisions are unchanged by G3:** desktop shell, v1 wedge ratification, editor-gate weights, licence and publication timing, `AI OFF` positioning, frontmatter intrusion.

---

## 8. Confirmation

- **No product code was written.** No Rust, no `cargo new`, no Spec Kit initialization, no Ponytail installation, no SQLite implementation, no MCP, no Cedar, no cap-std, no UI, no Graphify, no kill tests, no benchmark harness, no Headless Proof execution.
- **No dependency was installed.**
- **No architecture was reopened** beyond the corrections above; the load-bearing model in §1 is unchanged.
- **Nothing was pushed. Nothing was merged.** Local commit only.
- **Implementation remains unauthorized.**

---

## 9. Verdict

# `G3_SECURITY_RECONCILED_READY_FOR_GPT_DELTA_REVIEW`

All 16 VALID findings applied. Both PARTIAL findings applied in their valid portion, with the replaced remedies argued in §4. No finding was rejected, and none required evidence Fehrest does not have.

**The verdict is not `G3_SECURITY_RECONCILIATION_BLOCKED`:** every freeze condition is satisfied, and every deferred item has a named gate. **It is not `G3_SECURITY_MAJOR_REDESIGN_REQUIRED`:** no foundational trust assumption was invalidated, and the corrections narrowed claims and specified mechanisms rather than replacing the model.

**What changed is the honesty of the security claims, and the specificity of the mechanisms behind them.** Three claims were withdrawn as overstated; six mechanisms that existed only as prose now have normative specifications; and the package now records, in one place, **what Fehrest v1 does not claim** — which is the part a reader would otherwise have to infer.

**Next gate: GPT-5.6 Sol final security delta review. Architecture freeze may be considered only after it. Implementation remains blocked pending explicit founder authorization.**
