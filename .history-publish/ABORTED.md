# Historical Object Publication Attempt — Aborted

Status: `ABORTED_BEFORE_PUBLICATION`

This branch records a rejected transfer experiment only.

The first staged base64 chunk did not reproduce the expected beginning of the verified historical Git bundle. The chunk was removed before any workflow, archival-ref push, tree construction, or mutation of `main`.

Do not use this branch as historical publication evidence.

Required live truth remains owned by Issue #1:

```text
ARCHIVAL_REF=refs/heads/historical/r1-v1.1
SEALED_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
SEALED_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
ORIGINAL_GIT_OBJECT_GRAPH_PUBLISHED=NO
```

Any future publication attempt must transport the verified existing Git objects byte-for-byte and must fail closed on any digest or object-identity mismatch.
