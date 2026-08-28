# Ponytail Gate — Spec 002

## Necessity verdict

**KEEP** the Phase 1 convergence work.

It protects canonical, unrecomputable state. It is not optional polish.

## Reuse before invention

### Single-writer

Existing `Vault` / `WriteLock` is present.

```text
DECISION=REUSE
NEW_LOCK_FRAMEWORK=NO
```

### Canonical write

Prefer Rust std/filesystem primitives and one small shared helper.

Do not add a storage engine to solve atomic Markdown/object replacement.

### Event schema

Use the existing serde stack.

Do not add protobuf/Cap'n Proto/FlatBuffers merely to obtain versioning.

### Recovery

Implement only the failure classes already required by the Recovery Model and Phase 1 acceptance criteria.

Do not build a generic transaction manager.

## Explicit deferrals

```text
memory curator            DEFER Phase 4+
graph                     DEFER Phase 3 gate
vectors                   DEFER benchmark gate
MCP                       DEFER Phase 5
agent runtime             REJECT as a core concern
sandbox platform          REJECT as a core concern
web acquisition           DEFER until a measured need
UI                        DEFER Phase 7
plugin architecture       REJECT for this feature
```

## Security non-minimization

Ponytail may not remove or weaken:

```text
root confinement
post-open identity verification
writer ownership
canonical durability/recovery evidence
event integrity checks
provenance
resource bounds
negative security claims
```

## Dependency target

```text
NEW_RUNTIME_DEPENDENCIES=0
```

Any deviation requires a written dependency decision with requirement, alternatives, rights/security review, pin and exit strategy.
