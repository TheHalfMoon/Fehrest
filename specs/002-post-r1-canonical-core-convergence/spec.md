# Feature Specification: Post-R1 Canonical Core Convergence

**Feature ID:** `002-post-r1-canonical-core-convergence`  
**Status:** SPECIFIED / BLOCKED  
**Activation:** requires an R1 terminal route that permits continuation **and explicit founder authorization**.

## 1. Purpose

If R1 permits continued investment, the next work must make the irreplaceable canonical layer production-grade before expanding graph, vectors, UI, agent gateway or automatic memory.

The feature covers:

```text
stable vault identity / format version
crash-aware canonical writes
writer-owned mutation boundary
versioned typed event journal
explicit append durability boundary
startup integrity
recovery and torn-tail handling
schema upcasting + golden fixtures
native fault/kill matrices
```

## 2. Entry criteria

All must be true:

```text
R1_TERMINAL_VERDICT_RECORDED=YES
R1_ROUTE_PERMITS_PHASE_1=YES
FOUNDER_AUTHORIZATION_SPEC_002=YES
LIVE_WORKTREE_RECONCILED=YES
HISTORICAL_R1_V1_1_EVIDENCE_VERIFIED=YES
R1_SEMANTICS_UNCHANGED_BY_SPEC_002=YES
```

The GitHub bootstrap SHA is not a replacement for historical sealed R1 identifiers. See `docs/canonical/GITHUB_BOOTSTRAP_PROVENANCE.md`.

## 3. Non-goals

This feature does not implement:

```text
incremental derived indexing
graph
vectors / embeddings
automatic memory
memory curator
full durable memory product subsystem
MCP / agent gateway
external web acquisition
sandbox provider
UI/editor/canvas
sync/CRDT/cloud
plugin framework
```

It does not change R1 or reinterpret its result.

## 4. Phase T reconciliation requirement

Before implementation, create a closeout record comparing Phase T requirements with actual delivered behavior.

Preserve these distinctions:

1. Vault-level single-writer locking already exists.
2. Canonical mutator ownership is enforced mainly through the Vault/write path; stronger type/chokepoint enforcement remains useful.
3. Memory value semantics exist; a product durable memory journal/CLI write surface remains a later memory-phase concern.
4. Phase T context compilation is a minimal deterministic bounded subset, not the full production compiler.
5. Phase T byte budgeting is not the final tokenizer/model-token budget.
6. Incremental-vs-clean B-12 could not be completed because incremental indexing did not exist.

Do not rewrite historical records to pretend these distinctions never existed.

## 5. Functional requirements

### Vault identity and format

- **FR2-001** A vault MUST have explicit Fehrest vault identity and format/schema version metadata.
- **FR2-002** Unsupported/newer format MUST fail visibly or enter a specified migration path; it MUST NOT be guessed.

### Canonical writes

- **FR2-003** Canonical object replacement MUST use a crash-aware atomic-write strategy appropriate to the supported platform.
- **FR2-004** A successful write MUST have a documented persistence boundary.
- **FR2-005** Injected failure MUST preserve the old complete object, the new complete object, or a detectable recovery artifact; never silent partial canonical success.
- **FR2-006** Existing unknown-frontmatter preservation guarantees MUST remain green.

### Writer ownership

- **FR2-007** Existing one-writer-per-vault semantics MUST remain.
- **FR2-008** Canonical mutator APIs SHOULD structurally require/prove writer ownership where practical rather than relying only on convention.
- **FR2-009** Stale locks MUST remain visible and MUST NOT be automatically stolen.
- **FR2-010** PID/process diagnostics MUST NOT become authentication or permission.

### Event journal

- **FR2-011** Event records MUST carry an explicit schema version.
- **FR2-012** Production event payloads MUST be typed/versioned rather than an indefinitely expanding free-form detail string.
- **FR2-013** Event append MUST retain contiguous sequence and honest unkeyed hash-chain semantics.
- **FR2-014** Append success MUST define its flush/sync durability boundary.
- **FR2-015** A torn final record MUST be detected and preserved/quarantined before repair.
- **FR2-016** A mid-log gap or chain break MUST fail closed and MUST NOT be normalized as crash damage.
- **FR2-017** Event schema evolution MUST have read-time upcasting and a committed historical golden fixture.
- **FR2-018** A complete internally consistent malicious rewrite remains outside the guarantee of an unkeyed hash chain.

### Startup integrity and recovery

- **FR2-019** Writable vault open MUST execute the Phase 1 startup integrity sequence before mutation is allowed.
- **FR2-020** Recovery actions MUST be auditable and distinguish recovered/synthetic state from clean history.
- **FR2-021** Forensic evidence MUST be preserved before destructive cleanup.

### Event tiering

- **FR2-022** T1/T2/T3 retention parameters MUST NOT be invented without B-0 event-volume evidence.
- **FR2-023** If B-0 is unavailable, choose the minimum non-compacting correct behavior.

### Security continuity

- **FR2-024** Phase T path confinement, post-open identity, allowlist, resource bounds and writer kill tests MUST remain green.
- **FR2-025** `unsafe` remains forbidden in Fehrest Core.
- **FR2-026** No new network/process/plugin capability is introduced.

## 6. Acceptance scenarios

### AS2-1 — Kill during canonical replacement

At every injected point around temp creation, write, flush/sync and replacement, startup sees either the old complete object, the new complete object, or a detectable recovery artifact. Never silently truncated success.

### AS2-2 — Second writer

Two processes attempt mutation. Exactly one obtains writer ownership; the other fails visibly without canonical append.

### AS2-3 — Direct mutation bypass

Production APIs make unowned canonical append unavailable or explicitly rejected, or exhaustive chokepoint evidence proves equivalent enforcement.

### AS2-4 — Torn event tail

A partial final record is classified as tail crash damage, preserved, and handled under the Recovery Model.

### AS2-5 — Mid-log deletion

A missing middle event causes visible gap/chain failure and writable continuation is refused.

### AS2-6 — Historical schema

A committed historical event fixture opens through read-time upcasting without rewriting original fixture bytes merely to read them.

### AS2-7 — Honest hash-chain limitation

The negative test showing a fully recomputed unkeyed chain can verify remains preserved; no report calls this authentication.

### AS2-8 — R1 preservation

Spec 002 work never edits or regenerates sealed R1 semantic evidence.

## 7. Success criteria

```text
cargo fmt --check PASS
cargo check --all-targets PASS
cargo clippy --all-targets --all-features -- -D warnings PASS
cargo test PASS
Phase T kill/security tests remain green
new atomic-write fault matrix PASS
writer-ownership tests PASS
event recovery matrix PASS
historical event upcast fixture PASS
canonical loss in required crash matrix = 0
historical R1 semantics verified unchanged
unauthorized feature paths added = 0
```

Phase 1 exits only with evidence, not because the code appears robust.

## 8. Failure routing

- Canonical loss: stop; do not proceed to Phase 2.
- Unsupported atomic replacement semantics: record platform limitation and reopen the mechanism through the proper change class.
- Writer boundary too complex to strengthen safely: preserve current lock, add exhaustive chokepoint tests, record residual risk.
- Event JSONL fails measured durability/size needs: invoke the existing failure condition; do not silently change formats.
