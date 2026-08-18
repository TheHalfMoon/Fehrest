# Dependency Admission Records — Phase T

Every runtime dependency carries a record. **Founder donor-use authorization does not substitute for this gate** ([PHASE_T_AUTHORIZATION §3](../../docs/canonical/PHASE_T_AUTHORIZATION.md)).

**Advisory status note.** `RUSTSEC_STATUS` and `OSV_STATUS` are recorded as `NOT_SCANNED_IN_THIS_ENVIRONMENT` where no scanner was run. That is a statement about what was checked, not a clean bill of health — the same discipline the source registry applies to unverified pins.

---

## ADMITTED

### rusqlite

```
CAPABILITY_REQUIRED=            embedded SQL storage with FTS5 for the derived index
WHY_STDLIB_INSUFFICIENT=        std has no database, no FTS. ADR-0006 selects SQLite
WHY_NATIVE_PLATFORM_INSUFFICIENT= no OS provides FTS5-equivalent full-text search
CANDIDATES_CONSIDERED=          rusqlite (bundled), rusqlite (system libsqlite3), sqlx, libsqlite3-sys direct
SELECTED_DEPENDENCY=            rusqlite
EXACT_VERSION=                  0.37 (features: bundled)
LICENSE=                        MIT
RUSTSEC_STATUS=                 NOT_SCANNED_IN_THIS_ENVIRONMENT
OSV_STATUS=                     NOT_SCANNED_IN_THIS_ENVIRONMENT
UNSAFE_OR_FFI=                  YES - FFI to SQLite C. Unavoidable for any SQLite binding
BUILD_RS=                       YES - compiles bundled SQLite
PROC_MACRO=                     NO
DEFAULT_FEATURES=               disabled
SELECTED_FEATURES=              bundled
WHY_MINIMUM=                    'bundled' pins the engine version and removes a system-library
                                dependency, which matters because E section 13 requires a specific
                                hardening posture (extension loading disabled, trusted_schema).
                                A system SQLite could be built with different defaults.
                                sqlx rejected: async runtime for a single-threaded local CLI.
REMOVAL_PATH=                   derived state is rebuildable by construction (I-6). Replacing the
                                index engine costs a rebuild, not data.
```

### uuid

```
CAPABILITY_REQUIRED=            UUIDv7 generation and parsing for canonical object identity
WHY_STDLIB_INSUFFICIENT=        std has no UUID type and no time-ordered generator
WHY_NATIVE_PLATFORM_INSUFFICIENT= platform GUID APIs give v4, not the time-ordered v7 ADR-0004 requires
CANDIDATES_CONSIDERED=          uuid crate, hand-rolled v7
SELECTED_DEPENDENCY=            uuid
EXACT_VERSION=                  1
LICENSE=                        Apache-2.0 OR MIT
RUSTSEC_STATUS=                 NOT_SCANNED_IN_THIS_ENVIRONMENT
OSV_STATUS=                     NOT_SCANNED_IN_THIS_ENVIRONMENT
UNSAFE_OR_FFI=                  NO (with selected features)
BUILD_RS=                       NO
PROC_MACRO=                     NO
DEFAULT_FEATURES=               disabled
SELECTED_FEATURES=              v7, std
WHY_MINIMUM=                    Hand-rolling identity generation is on Ponytail's exclusion list --
                                identity is a durable-correctness concern (F-CORE-04). A v7
                                implementation must get monotonicity and counter-rollover right,
                                and getting it subtly wrong produces colliding identities that
                                surface as data corruption years later.
REMOVAL_PATH=                   ObjectId is a newtype; the generator is one function.
```

### sha2

```
CAPABILITY_REQUIRED=            SHA-256 for event hash chaining, content hashes, manifest digests
WHY_STDLIB_INSUFFICIENT=        std has no cryptographic hash
WHY_NATIVE_PLATFORM_INSUFFICIENT= platform crypto APIs differ per OS and would need three code paths
CANDIDATES_CONSIDERED=          sha2, ring, blake3, hand-rolled
SELECTED_DEPENDENCY=            sha2
EXACT_VERSION=                  0.10
LICENSE=                        Apache-2.0 OR MIT
RUSTSEC_STATUS=                 NOT_SCANNED_IN_THIS_ENVIRONMENT
OSV_STATUS=                     NOT_SCANNED_IN_THIS_ENVIRONMENT
UNSAFE_OR_FFI=                  minimal, in the RustCrypto backend
BUILD_RS=                       NO
PROC_MACRO=                     NO
DEFAULT_FEATURES=               disabled
SELECTED_FEATURES=              (none beyond default-off std)
WHY_MINIMUM=                    Hand-rolling a hash is explicitly forbidden -- audit integrity is on
                                Ponytail's exclusion list. ring rejected: larger surface, build
                                complexity, and Phase T needs one primitive. blake3 rejected: the
                                architecture documents specify sha256 throughout.
REMOVAL_PATH=                   one hashing function behind one internal helper.
```

### serde + serde_json

```
CAPABILITY_REQUIRED=            manifest and envelope serialization
WHY_STDLIB_INSUFFICIENT=        std has no serialization framework and no JSON
WHY_NATIVE_PLATFORM_INSUFFICIENT= not a platform capability
CANDIDATES_CONSIDERED=          serde+serde_json, hand-rolled JSON writer, no JSON at all
SELECTED_DEPENDENCY=            serde, serde_json
EXACT_VERSION=                  serde 1 (derive), serde_json 1
LICENSE=                        Apache-2.0 OR MIT
RUSTSEC_STATUS=                 NOT_SCANNED_IN_THIS_ENVIRONMENT
OSV_STATUS=                     NOT_SCANNED_IN_THIS_ENVIRONMENT
UNSAFE_OR_FFI=                  minimal
BUILD_RS=                       NO
PROC_MACRO=                     YES - serde_derive
DEFAULT_FEATURES=               serde: disabled + derive, std
SELECTED_FEATURES=              derive, std
WHY_MINIMUM=                    Hand-rolling JSON escaping is precisely the bug class the trust
                                envelope exists to prevent (G section 4.3). Writing our own escaper for
                                a security-relevant serialization boundary would be Ponytail
                                minimising a security control, which the exclusion list forbids.
REMOVAL_PATH=                   serialization is confined to envelope.rs and context.rs.
```

---

## REJECTED

### serde_yaml — rejected

```
CAPABILITY_CONSIDERED=  parse YAML frontmatter
REJECTED_BECAUSE=       Fehrest's frontmatter contract is a bounded key-value subset: id, title,
                        project, plus verbatim passthrough of unknown lines (R-8). A general YAML
                        parser accepts anchors, aliases, merge keys, multi-document streams and
                        arbitrary nesting -- a large parsing surface applied to attacker-influenced
                        vault content (T-17), to gain nothing the subset parser does not provide.
                        serde_yaml is additionally unmaintained upstream.
PONYTAIL_QUESTION=      5 - can a smaller implementation satisfy the requirement? Yes: ~40 lines
                        parsing 'key: value' between --- fences, preserving unknown lines byte-for-byte.
NOTE=                   This is NOT Ponytail minimising a security control. It is choosing the
                        SMALLER attack surface. A subset parser that rejects what it does not
                        understand is safer here than a general parser that accepts everything.
```

### cap-std — not adopted

```
STATUS=                 STRONG CANDIDATE, NOT ADOPTED (SEC-R14 / G3-I1)
EVALUATED_BECAUSE=      root containment is a frozen requirement (F-CORE-10)
NOT_ADOPTED_BECAUSE=    std reached the Phase T contract: component rejection before open,
                        symlink_metadata check on the final component, canonical parent-chain
                        verification, and post-open UUID verification. The containment tests
                        (K-12, K-22) pass without it.
REEVALUATE_IF=          a platform case is found where std cannot express the containment contract
                        with acceptable complexity, or GLM-5.3 finds a gap in the std approach.
NOT_CLAIMED=            cap-std is not an authorization engine, not a process sandbox, and not a
                        substitute for identity verification.
```

### Cedar — not adopted

```
STATUS=     DEFERRED to a later multi-actor / MCP authorization gate (SEC-R15)
REASON=     Phase T has one principal and a two-dimension scope selector. A policy engine for
            that is not minimum-correct. Equally, NO custom policy language was written --
            authorization is a direct deny-by-default scope check in Rust.
```

### tokio / async — not adopted

```
REASON=     No concurrency exists in Phase T. Constitution: no async unless actual concurrency
            requires it. The single-writer lock makes concurrent canonical writes an error, not
            a workload.
```

---

## Summary

```
ADMITTED  = 5 crates (rusqlite, uuid, sha2, serde, serde_json)
REJECTED  = 4 (serde_yaml, cap-std, Cedar, async runtime)
UNSAFE in Fehrest code = 0
FFI = only inside rusqlite -> bundled SQLite
```
