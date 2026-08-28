# Historical Object Publication Attempt — Fail-Closed Record

Status: `BLOCKED_EXTERNAL_TRANSPORT`

This temporary branch records bounded publication-route experiments only. It is not historical publication evidence.

Verified facts:

```text
CANONICAL_MAIN=d3ba3bd505c2df00389c6a7014cd130972160491
TARGET_REF=refs/heads/historical/r1-v1.1
TARGET_COMMIT=ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c
TARGET_TREE=f7ea7e0f57019c8061a4019ac614730f68750f19
ORIGINAL_GIT_OBJECT_GRAPH_PUBLISHED=NO
FORCE_PUSH_USED=NO
REBASE_USED=NO
MAIN_CHANGED=NO
```

Repository-text transport experiments were rejected whenever byte identity did not match. A 2048-byte raw chunk could be represented exactly through the connector, but larger model-mediated payloads were not consistently byte-exact. No reconstructed bundle was accepted and no archival ref was pushed.

A GitHub Actions write-token preflight and an independent read-only hosted-runner preflight both failed before runner allocation. The read-only job contained only an `echo` step, yet completed with `steps=[]` and `runner_id=0`. Therefore this branch must not stage the full historical bundle until hosted execution or another exact object transport becomes available.

The durable Windows publication package retained in Fehrest recovery artifacts remains the valid prepared route:

```text
PACKAGE=FEHREST-HISTORICAL-OBJECT-PUBLISH-V1.zip
ENTRYPOINT=PUBLISH_THIS_NOW.cmd
```

Issue #1 remains authoritative for closure criteria.
