# Implementation Plan — Spec 002 Post-R1 Canonical Core Convergence

**Status:** PLANNED / BLOCKED  
**Depends on:** `spec.md`, frozen architecture, Phase 1 implementation plan, Recovery Model, Migration Model, Threat Model.

## 1. Strategy

Implement in six evidence-gated slices:

```text
A. Phase T truth reconciliation
B. Vault metadata + crash-safe canonical writes
C. Writer-owned mutation API
D. Versioned typed event journal
E. Startup integrity + recovery + upcasting
F. Verification + closeout
```

No later slice begins while a blocker remains in the current slice.

## 2. Slice A — Reconciliation

Create a Phase T implementation-conformance review that records:

```text
what Phase T implemented fully
what it deliberately minimized
what old wording overstated
what R1 actually exercised
what remains Phase 1 / 2 / 4 / 5 work
```

Do not edit old verification records to make the story cleaner.

Required corrections include:

- credit the existing Vault/WriteLock single-writer mechanism;
- record that durable product memory persistence/CLI write is later work;
- record that the Phase T compiler is a bounded subset of the full compiler;
- preserve B-12 as historically unavailable because incremental indexing did not exist.

## 3. Slice B — Vault metadata and canonical writes

### Vault metadata

Add only currently required machine-owned metadata, such as:

```text
vault_id
format_version
created_by_version
```

Do not pre-design cloud/collaboration fields.

### Canonical write mechanism

Ponytail order:

1. Rust `std` and existing repository primitives.
2. Existing admitted helper/dependency.
3. New small dependency only if measurement proves the first two cannot meet platform correctness.

Required properties:

```text
same-filesystem temp
complete write
explicit flush/sync according to the documented durability contract
replace target
parent-directory sync where relevant/supported by the contract
cleanup only after outcome is known
```

Windows behavior must be tested natively; do not assume Unix rename semantics.

## 4. Slice C — Writer-owned mutation

Reuse current write-lock behavior.

Evaluate the smallest API that makes canonical mutation ownership explicit, for example:

```text
VaultWriter<'a>
WriterLease
Vault::append_event(...)
EventLog::for_writer(...)
```

Do not preselect the abstraction before analysis.

Selection criteria:

```text
cannot be forged from arbitrary path input
preserves read-only concurrency
keeps tests simple
adds no lock framework
keeps stale-lock policy visible/no-auto-steal
```

## 5. Slice D — Event journal

### Schema

Move from indefinitely free-form event payloads toward a versioned envelope + typed payloads for Phase 1 needs only.

Do not implement the entire future event vocabulary before event-volume evidence exists.

### Hashing

Freeze canonical field order/serialization for each schema version that participates in the hash.

Keep the security claim honest: an unkeyed chain detects accidental/partial mutation, not a fully capable malicious rewrite that recomputes the chain.

### Durability

Define precisely what append success means on each supported platform/filesystem class. Do not promise physical durability beyond what the OS/filesystem can establish.

## 6. Slice E — Startup integrity and recovery

Before writable open:

```text
identify vault format
inspect writer state
verify event framing
separate torn final record from mid-log damage
verify seq/hash chain
preserve forensic bytes before repair
execute only authorized recovery
record recovery/synthetic state when required
allow mutation only after integrity gate
```

### Upcasting

Commit a historical event fixture. Upcast in memory. Do not rewrite canonical historical bytes merely to read them.

## 7. Slice F — Verification

At minimum:

```text
cargo fmt --check
cargo check --all-targets
cargo clippy --all-targets --all-features -- -D warnings
cargo test
release/native filesystem gates where meaningful
historical R1 semantic-preservation verification
```

Then conduct a dedicated adversarial review of:

```text
crash windows
Windows replacement behavior
writer ownership
malformed event framing
recovery misclassification
schema upcast ambiguity
```

## 8. Expected source scope

Primary source files are expected to remain near:

```text
src/vault.rs
src/events.rs
src/identity.rs only if required
src/cli.rs only for Phase 1 behavior
src/lib.rs only for required types/errors/limits
tests/integration.rs
tests/kill_tests.rs
```

Do not touch sealed R1 semantics, graph/vector/agent/UI modules, or add runtime dependencies without a reviewed dependency decision.

## 9. Dependency policy

Default:

```text
NEW_RUNTIME_DEPENDENCIES=0
```

Any proposed dependency requires:

```text
requirement
proof existing/std path is insufficient
license/provenance
security/advisory review
footprint
maintenance health
pin/version decision
exit strategy
```

## 10. Commit discipline

Prefer local atomic commits per verified slice. Suggested messages are guidance, not mandatory history shape:

```text
docs(spec): reconcile phase T implementation truth
feat(core): add versioned vault metadata
fix(core): make canonical object replacement crash-safe
refactor(core): require writer ownership for canonical mutation
feat(events): add versioned typed event envelopes
fix(events): add durable append and startup recovery
test(core): complete phase 1 crash and recovery gates
docs(review): close canonical core convergence
```

No force push, destructive rewrite, PR, merge or release without the relevant authorization.
