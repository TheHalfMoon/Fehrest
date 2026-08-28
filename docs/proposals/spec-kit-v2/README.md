# Fehrest V2 Spec Kit Planning Control Index

**Status:** PROPOSAL CONTROL INDEX / NON-AUTHORIZING  
**Created:** 2026-08-28  
**Canonical authority:** unchanged; see `AGENTS.md`, `specs/CURRENT.md`, and `docs/canonical/EXECUTION_MASTER_PLAN.md`.

> The files in this directory refine the earlier V2 planning proposal into a Spec Kit-compatible program decomposition. Within the non-canonical V2 proposal branch only, if these files conflict with older V2 proposal sequencing or ownership language, this directory is the newer planning refinement. It does not supersede canonical repository governance.

---

## Read order

```text
1. PROGRAM_BLUEPRINT.md
2. RUST_PLATFORM_ARCHITECTURE.md
3. CROSS_SPEC_INVARIANTS_AND_OWNERSHIP.md
4. SPEC_SEQUENCE_AND_DEPENDENCIES.md
5. TRACEABILITY_AND_COVERAGE_MATRIX.md
6. CONFLICT_AND_GAP_REVIEW.md
7. SPEC_AUTHORING_CHECKLIST.md
```

Then read the broader V2 product documents:

```text
docs/product/FOUNDER_PRODUCT_VISION_V2.md
docs/product/UX_BLUEPRINT_V2.md
docs/product/HUMAN_AGENT_FEATURE_CATALOG_V2.md
docs/research/COMPETITIVE_CAPABILITY_MATRIX_2026-08-28.md
docs/reviews/PRODUCT_GAP_REVIEW_V2_2026-08-28.md
docs/proposals/AI_SEARCH_WEBMCP_PROVIDER_ARCHITECTURE.md
docs/proposals/EXECUTION_MASTER_PLAN_V2_PROPOSAL.md
```

---

## What this refinement changes versus the older V2 proposal

### 1. Formal Spec Kit program layer

V2 is treated as a program/assessment, not one giant feature spec.

### 2. Rust-first platform direction

Founder technical direction is now explicit:

```text
RUST_PRIMARY_PRODUCT_LANGUAGE=YES
RUST_OWNS_CANONICAL_SEMANTICS=YES
RUST_OWNS_SECURITY_AND_AUTHORIZATION=YES
RUST_OWNS_MEMORY_SEARCH_SYNC_GATEWAYS=YES
NON_RUST_INTEROP=THIN_ONLY_WHEN_JUSTIFIED
```

UI, sync, search and provider libraries remain subject to their own future Spec Kit research/benchmark gates. Rust-first does not pre-authorize a framework or dependency.

### 3. Constitution reconciliation gate

Missing historical Constitution/Architecture Freeze sources are treated as a hard reconciliation gate, not reconstructed from memory.

### 4. Single semantic ownership

Every durable entity/lifecycle/contract/authorization responsibility gets one owning future spec.

### 5. Graph separation

```text
Graph Intelligence experiment/provider != Graph visualization UX
```

A useful Obsidian-style graph interface may exist over explicit canonical links even when derived graph intelligence is rejected/deferred.

### 6. Gateway/AI separation

```text
007 Universal Context/Memory Gateway
!=
013 AI Provider Runtime/Ask Fehrest
```

Core context/authorization remains model-independent.

### 7. Organization before team communication

The refined order is:

```text
collaboration experiment
-> production sync/multi-writer substrate
-> organization identity/policy/admin
-> channels/topics/DMs/shared team workspace
```

This removes a security dependency inversion in the earlier proposal.

### 8. Workspace object foundation before UI

Canonical Note/Task/Project/Space/open-format semantics are specified before desktop presentation owns them accidentally.

### 9. WebMCP separated into an external-evidence/tool spec

WebMCP remains a provider candidate under Fehrest-owned authorization/origin/prompt-injection controls.

### 10. Traceability and converge requirements

Every MUST requirement must trace through acceptance/test/tasks/evidence and close with no orphan requirements or tasks.

---

## Current state

```text
V2_PROGRAM_REFINEMENT=PREPARED
FOUNDER_LANGUAGE_DIRECTION=RUST
V2_PROGRAM_CANONICAL=NO
R1_CHANGED=NO
CURRENT_CHANGED=NO
SPEC_002_CHANGED=NO
IMPLEMENTATION_AUTHORIZED=NO
```
