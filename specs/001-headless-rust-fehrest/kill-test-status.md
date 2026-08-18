# G3 Kill-Test Status — Phase T

`STATUS_HONESTY: EXECUTION_EVIDENCE_ONLY`

This file records what was **actually executed on this host**, not what the suite
appears to report. It exists because `cargo test` has no "skipped" state: a test
that returns early because a platform capability is unavailable prints `ok` and is
otherwise indistinguishable from a test that ran its assertion. One kill test in
this suite is in exactly that position, and it is recorded below as
`PENDING_NATIVE_EXECUTION`, **not** as a pass.

## Execution environment

| Field | Value |
|---|---|
| `HOST_OS` | Microsoft Windows 11, build 10.0.26200.9168 |
| `HOST_TARGET` | `x86_64-pc-windows-msvc` |
| `RUSTC` | 1.97.1 (`8bab26f4f`, 2026-07-14) |
| `SUITE` | `tests/kill_tests.rs` |
| `RESULT` | 23 passed · 0 failed · 0 ignored |
| `SYMLINK_CAPABILITY` | **UNAVAILABLE** (no Developer Mode, non-elevated) |
| `JUNCTION_CAPABILITY` | AVAILABLE (`mklink /J` succeeded) |

## Status vocabulary

| Token | Meaning |
|---|---|
| `PASS` | The attack was constructed and executed on this host, and the assertion ran and held |
| `PENDING_NATIVE_EXECUTION` | The test exists and compiles, but a host capability was missing, so **the assertion did not run**. Not evidence of anything |
| `PENDING_MACOS_EXECUTION` | Never executed on macOS |
| `PENDING_LINUX_EXECUTION` | Never executed on Linux |
| `DEFERRED_SURFACE_NOT_PRESENT` | The attacked surface does not exist in Phase T. Nothing was tested and nothing is claimed |

**`PASS` means the specified attack was tried and did not work.** It does not mean
the surface is secure, and it converts none of the twelve negative claims in
`C §7.1` into a positive claim.

## Proving which tests really ran

A skip is silent by default. Set `FEHREST_REQUIRE_NATIVE_FS=1` to turn any missing
capability into a hard failure, which is the only way to prove from the outside that
the filesystem kill tests executed:

```bash
FEHREST_REQUIRE_NATIVE_FS=1 cargo test --test kill_tests
```

On this host that run reports **`21 passed; 1 failed`** — `k12_symlink_escape_fails`
fails with `PENDING_NATIVE_EXECUTION`, which is the honest result. On a host with
symlink capability the same command must report all tests passing; until that run
happens, K-12 has no execution evidence on any platform.

## Per-test status

| Kill test | Attack | Status | Test function | Note |
|---|---|---|---|---|
| **K-01** | Imported-content injection → capability change / tool execution | `DEFERRED_SURFACE_NOT_PRESENT` | — | Phase T has **no capability grant and no tool-execution surface**, so the asserted outcome has nothing to bind to. The evidence-only half of the property is covered by K-02, which is not the same test |
| **K-02** | Malicious `AGENTS.md`-style in-vault instruction file | `PASS` | `k02_instruction_shaped_vault_content_remains_evidence` | Header stays `authority="none"`, `trust_level="4"`; exactly one machine-owned item emitted |
| **K-03** | MCP capability / `tools/list` manipulation | `DEFERRED_SURFACE_NOT_PRESENT` | — | No MCP surface exists in Phase T (hard non-goal) |
| **K-04** | In-grant-but-not-served provenance claim | `PASS` | `k04_in_scope_but_not_served_is_not_observed_evidence` | Manifest is the sole arbiter; omissions recorded |
| **K-05** | Manifest / chain partial tamper | `PASS` | `k05_partial_tamper_is_detected` | Detected at exact `seq`. **No authentication claimed** against a full consistent rewrite — that limit is itself asserted by `events::tests::consistent_full_rewrite_is_not_detected_and_we_say_so` |
| **K-06** | Package/manifest mismatch | `PASS` | `k06_package_manifest_mismatch_fails` | Forged manifest entry naming an unemitted item fails verification |
| **K-07** | Cross-project memory poisoning | `PASS` | `k07_cross_project_contamination_blocked` | Project A memory is never a candidate for project B |
| **K-08** | Vault-global poisoning | `PASS` (ordering half) | `k08_vault_global_cannot_outrank_project_local` | The ordering invariant is executed. The roster's other half — "vault-global creation is unreachable from any agent path" — is vacuous in Phase T because **no agent path exists**; it is not claimed as tested |
| **K-09** | `PENDING` influence and advisory flooding | `PASS` | `k09_pending_never_becomes_authoritative_and_flooding_does_not_help` | 500 `PENDING` assertions resolve to exactly what one does: `NoAnswer`. Flooding also cannot force a `CONTRADICTION`, which would be a denial-of-answer win |
| **K-10** | Temporal resurrection | `PASS` | `k10_superseded_cannot_reactivate` | Superseded/expired never returned as current state |
| **K-11** | Duplicate UUID | `PASS` | `k11_duplicate_uuid_is_a_conflict` | Surfaced as conflict; **both** files retained |
| **K-12** | **Symlink escape** | **`PENDING_NATIVE_EXECUTION`** | `k12_symlink_escape_fails` | **The assertion did not run.** Symlink creation is unavailable to a non-elevated process on this host without Developer Mode, so the test returned early. It reports `ok` under a plain `cargo test` — that green is meaningless and must not be read as evidence. Requires a POSIX host or an elevated / Developer-Mode Windows host |
| **K-13** | Windows reparse point / junction escape | `PASS` | `k13_windows_directory_reparse_escape_fails` | **Executed natively on Windows 11.** Junction created via `mklink /J`; the read failed at the containment boundary |
| **K-14** | Authorize/open swap (TOCTOU) | `PASS` | `k14_authorize_then_swap_fails_closed` | Post-open UUID verification rejects the swapped bytes. This is the *identity* guarantee and is **independent of** containment (K-12/K-13/K-22); neither substitutes for the other |
| **K-15** | Git rename / case storm | `PASS` | `k15_identity_survives_rename_and_case_rename` | Identity survives; no duplicate object allocated |
| **K-16** | Poisoned derived SQLite | `PASS` | `k16_poisoned_derived_index_cannot_grant_authority` | Poisoned rows grant nothing; canonical scope remains the authorization authority |
| **K-17** | Hostile FTS5 `MATCH` syntax | `PASS` | `k17_fts_syntax_in_user_text_is_literal`, `k17_oversized_query_is_bounded` | Operators, `NEAR`, column filters and quotes are treated as literal tokens; oversized queries bounded |
| **K-18** | Event replay / reorder | `PASS` | `k18_reorder_and_replay_are_surfaced` | Reorder and rollback surfaced. **No authentication claimed** |
| **K-19** | Graph identity injection | `DEFERRED_SURFACE_NOT_PRESENT` | — | No graph and no extractor exist in Phase T (hard non-goal) |
| **K-20** | Provenance / trust truncation under budget | `PASS` | `k20_budget_pressure_never_strips_security_metadata` | `FULL` / `TRUNCATED` / `OMITTED`; never emitted stripped |
| **K-21** | Scripted user-authority path | `PASS` (corrected semantics) | `k21_agent_path_cannot_mint_user_authority` | Tests the enforceable invariant — an agent-facing path cannot produce `USER_ASSERTED` / `USER_CONFIRMED` and cannot supersede one. It deliberately does **not** test whether a script can reach a user-authority transition: under the declared OS-account root of trust that test cannot pass and should not be written |
| **K-22** | Derived path vault escape | `PASS` | `k22_derived_locator_cannot_escape_the_vault` | No injected locator value opens a resource outside the root |
| **K-23** | Envelope serialization forgery | `PASS` | `k23_content_cannot_forge_envelope_fields` | Content cannot create a second machine-owned item or forge trust, provenance or section identity |
| **K-24** | Concurrent canonical writers | `PASS` | `k24_concurrent_writer_is_rejected_visibly` | Second writer fails visibly; the lock is **never stolen**; forks never auto-merged |
| **K-24b** | Permanent-state amplification | `PASS` | `k24b_permanent_state_amplification_is_bounded` | Local **resource-safety** bounds hold, rejections explicit and audited, no canonical state silently discarded. These are safety limits and **are not** commercial, tier, trial or lifetime quotas |

## Roll-up

| Metric | Value |
|---|---|
| `KILL_TESTS_IN_ROSTER` | 25 |
| `EXECUTED_AND_PASSED` | 21 |
| `PENDING_NATIVE_EXECUTION` | 1 (K-12) |
| `DEFERRED_SURFACE_NOT_PRESENT` | 3 (K-01, K-03, K-19) |
| `FAILED` | 0 |
| `TEST_FUNCTIONS` | 23 |

## Platform coverage

| Platform | Status | Basis |
|---|---|---|
| Windows 11 (`x86_64-pc-windows-msvc`) | **EXECUTED** | Full suite run natively; the K-13 junction attack was really constructed |
| Windows with symlink capability | `PENDING_NATIVE_EXECUTION` | K-12 requires Developer Mode or elevation |
| macOS | `PENDING_MACOS_EXECUTION` | Never run. No macOS claim is made |
| Linux | `PENDING_LINUX_EXECUTION` | Never run. No Linux claim is made |

`T-18` holds that Windows confinement is the **weakest** platform. This suite ran on
that weakest platform, which is the useful direction — but a Windows result does not
transfer to POSIX, and K-12 is precisely the POSIX-shaped attack that remains
unexecuted everywhere.

## What this file does not establish

1. That Fehrest is secure. It establishes that 21 named attacks were built and failed.
2. That K-12's containment path works. It has **never been executed**.
3. Anything about MCP, graph or policy-engine surfaces. They do not exist to attack.
4. Authentication of the event chain. The chain is unkeyed by design (`C §6.1`), and
   K-05 / K-18 are scoped to partial-tamper evidence only.
