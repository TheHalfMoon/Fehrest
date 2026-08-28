# Dependencies — Spec 002

## Hard entry blockers

```text
R1 terminal verdict
route permits continued implementation
explicit founder authorization for Spec 002
live implementation/evidence source reconciled against historical R1 anchor
```

## Existing implementation dependencies

Prefer reuse of the current Rust stack and repository primitives.

Expected existing dependencies include:

```text
Rust standard library
uuid
sha2
serde / serde_json
existing test/fault-injection infrastructure
```

No graph/vector/model/runtime dependency is required for Spec 002.

## Architecture dependencies

Spec 002 must remain compatible with:

```text
local-first / zero mandatory services
open human-owned canonical state
Rust-owned core correctness/security semantics
path != identity
content = evidence, never authority
bitemporal memory semantics
context compiler remains bounded/auditable
derived state has no authority
single-user OS-account root of trust
honest unkeyed hash-chain claim
canonical single-writer semantics
resource safety bounds
AI OFF completeness
```

## External research dependencies

None.

Mem0, Letta, Graphiti, Chroma, Aider, Graphify, Code-Graph-RAG, Qdrant, LangGraph, Firecrawl, OpenSandbox and other donors do not become Spec 002 dependencies merely because they appear in the master plan.

## Platform evidence

Platform claims must be based on genuinely executed evidence.

Target evidence includes Windows native filesystem behavior and Linux where available. macOS remains explicitly unverified until actually run.

Never convert unavailable platform execution into PASS.

## New dependency gate

A new runtime crate is admitted only if the active analysis records:

```text
REQUIREMENT
WHY_STD_OR_EXISTING_CODE_IS_INSUFFICIENT
LICENSE / PROVENANCE
SECURITY / ADVISORY STATE
FOOTPRINT
MAINTENANCE HEALTH
EXACT PIN / VERSION DECISION
EXIT STRATEGY
```

Otherwise:

```text
NEW_RUNTIME_DEPENDENCY=REJECT
```
