Fehrest R1 replacement evidence collector V3

Use only AFTER FEHREST-R1-X1-REPLACEMENT-V8 has completed successfully.

Run:
  COLLECT_EVIDENCE_NOW.cmd

V3 is a non-semantic evidence-packaging helper. It does not run a model, score, unblind, perform power analysis, start confirmatory execution, or mutate source evidence.

V3 supersedes evidence collectors V1 and V2:
- V1 used a wildcard with Compress-Archive -LiteralPath and may fail to create the ZIP.
- V2 fixed archive creation but packaged only the result and raw archive.
- V3 also packages and verifies the sealed execution bindings needed for Issue #11 execution review: source/replacement arming manifests, source/replacement preflight records, incident record, replacement control record, and supervisor logs.

V8 itself is unchanged and remains identified only by SHA-256:
  9c53e45e41a0be5766779129a45e55aef4399d02395a1b4309e9d97114bef969

Output on Desktop:
  FEHREST-R1-X1-REPLACEMENT-EVIDENCE-V3-<timestamp>.zip

The collector never overwrites a prior evidence ZIP.
Upload the generated V3 ZIP to ChatGPT for exact Issue #11 execution review.
