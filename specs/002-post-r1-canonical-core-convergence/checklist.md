# Checklist — Spec 002 Post-R1 Canonical Core Convergence

## Entry gate

- [ ] R1 terminal verdict exists.
- [ ] R1 route permits Phase 1.
- [ ] Founder explicitly authorized Spec 002.
- [ ] Historical R1 v1.1 anchor is reconciled against the implementation/evidence source used for work.
- [ ] Live HEAD/worktree/source provenance is recorded before mutation.

## Reconciliation

- [ ] Phase T implementation vs specification delta is recorded without rewriting history.
- [ ] Existing Vault/WriteLock single-writer mechanism is credited accurately.
- [ ] Missing durable product memory surface remains deferred to its proper phase.
- [ ] Phase T compiler subset vs full production compiler is recorded.
- [ ] Historically unavailable B-12 incremental arm remains recorded honestly.

## Vault / canonical writes

- [ ] Vault identity is explicit.
- [ ] Vault format/schema version is explicit.
- [ ] Unsupported/newer format fails visibly.
- [ ] Canonical replacement is crash-aware under the documented platform contract.
- [ ] Fault injection before/after replacement never produces silent partial canonical success.
- [ ] Unknown frontmatter preservation remains green.

## Writer ownership

- [ ] Second writer fails visibly.
- [ ] Stale lock is never auto-stolen.
- [ ] Canonical mutation requires/proves writer ownership or an equivalent exhaustive chokepoint proof exists.
- [ ] Read-only concurrent access remains supported.

## Event journal

- [ ] Event schema version exists.
- [ ] Production payloads are typed/versioned.
- [ ] Canonical hash serialization is fixed per version.
- [ ] Unkeyed chain is never described as authentication.
- [ ] Append durability boundary is documented.
- [ ] Torn tail is detected and preserved before repair.
- [ ] Mid-log gap fails closed.
- [ ] Chain break fails closed.
- [ ] Recovery is auditable.
- [ ] Historical event fixture upcasts without rewriting original bytes.

## Scope discipline

- [ ] No graph production module.
- [ ] No vector/embedding default.
- [ ] No automatic memory.
- [ ] No MCP/agent gateway.
- [ ] No UI.
- [ ] No new network/process/plugin capability.
- [ ] No unnecessary runtime dependency.

## Verification

- [ ] `cargo fmt --check`.
- [ ] `cargo check --all-targets`.
- [ ] `cargo clippy --all-targets --all-features -- -D warnings`.
- [ ] `cargo test`.
- [ ] Required native filesystem/crash gates pass on genuinely executed platforms.
- [ ] Historical R1 semantics are verified unchanged by Spec 002.
- [ ] Dedicated adversarial review has zero unresolved blocker.
