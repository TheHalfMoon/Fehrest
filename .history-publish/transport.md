# Historical bundle transport boundary

Only raw bundle chunks whose base64 text Git blob SHA is precomputed locally and exactly reproduced by GitHub are eligible for the staging tree.

Empirical transport checks in this connector established:

```text
RAW_CHUNK_2048_BYTES=BYTE_EXACT_SUPPORTED
RAW_CHUNK_2560_BYTES=REJECTED_MISMATCH
RAW_CHUNK_3072_BYTES=REJECTED_MISMATCH
RAW_CHUNK_4096_BYTES=REJECTED_MISMATCH
RAW_CHUNK_8192_BYTES=REJECTED_MISMATCH
RAW_CHUNK_14000_BYTES=REJECTED_MISMATCH
```

The final publication workflow must independently reconstruct the complete bundle and verify its SHA-256 before any push.
