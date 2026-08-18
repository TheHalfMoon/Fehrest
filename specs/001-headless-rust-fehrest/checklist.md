# Phase T Quality Checklist

**Status:** defined pre-implementation · verified at [analyze.md](./analyze.md) and at technical closeout.

Each item states the frozen requirement it protects and how it is verified. `[ ]` = defined, not yet verified.

---

## Frozen invariants

- [ ] **CL-01** No network code path exists in the product crate *(F-CORE-01)* — grep for network APIs; tests run offline
- [ ] **CL-02** No model or provider is required to build, test or run *(F-CORE-01)* — full suite passes with no credentials
- [ ] **CL-03** Canonical content is readable without Fehrest *(F-CORE-02)* — vault files are plain Markdown
- [ ] **CL-04** `ObjectId` cannot be constructed from a path *(F-CORE-04)* — type-level; no `From<Path>` impl exists
- [ ] **CL-05** Deleting derived state loses nothing canonical *(F-CORE-02, I-6)* — `test_rebuild_preserves_canonical`
- [ ] **CL-06** Two independent rebuilds produce identical results *(I-6)* — `test_rebuild_deterministic`

## Authorization

- [ ] **CL-07** Scope check runs before emission, deny-by-default *(F-CORE-10)* — cross-project test
- [ ] **CL-08** Authorization reads canonical scope, never derived *(F-CORE-10)* — poisoned-index test
- [ ] **CL-09** No agent-facing path mints user authority *(F-CORE-11)* — K-21
- [ ] **CL-10** Vault-global authority is unreachable from a project-scoped path *(F-CORE-11)* — K-08

## Filesystem containment

- [ ] **CL-11** Absolute-path locator fails *(F-CORE-10)* — K-22
- [ ] **CL-12** Parent-traversal locator fails *(F-CORE-10)* — K-22
- [ ] **CL-13** Symlink escape fails *(T-8)* — K-12
- [ ] **CL-14** Windows junction/reparse escape test exists *(T-18)* — K-13; **native execution status recorded honestly**
- [ ] **CL-15** A derived locator cannot expand filesystem authority *(F-CORE-10)* — K-22

## Post-open identity

- [ ] **CL-16** UUID is read from the **opened handle**, not re-resolved *(F-CORE-10)* — code inspection + K-14
- [ ] **CL-17** Mismatch fails closed, never serves the bytes *(F-CORE-10)* — K-14
- [ ] **CL-18** Duplicate UUID is an explicit conflict, both retained *(D §3.2)* — K-11
- [ ] **CL-19** Containment and identity are **independently** tested *(E §12.1)* — separate tests, neither passing by the other's mechanism

## SQLite hardening

- [ ] **CL-20** Extension loading disabled *(E §13.1)* — open flags asserted in test
- [ ] **CL-21** `trusted_schema=OFF` or documented incompatibility *(E §13.1)* — pragma asserted
- [ ] **CL-22** Database path derives from the vault root *(E §13.1)* — construction is the only path
- [ ] **CL-23** Corrupt database is discarded and rebuilt, not repaired into trust *(E §13.1)* — corruption test
- [ ] **CL-24** Poisoned index rows cannot grant access *(E §12)* — K-16

## FTS5

- [ ] **CL-25** Literal text cannot activate FTS5 syntax *(E §13.2)* — K-17 with `OR`, `NEAR`, `title:`, `*`
- [ ] **CL-26** Query input length is bounded *(E §13.2)* — oversize test
- [ ] **CL-27** Result count is bounded *(F-CORE-15)* — cap asserted
- [ ] **CL-28** Ranking never grants authority *(E §12)* — scope filter applied after candidate generation

## Temporal and supersession

- [ ] **CL-29** Current-state resolution is correct on the ground-truth fixture *(FR-019)*
- [ ] **CL-30** `as-of` historical resolution differs correctly from current *(FR-020)*
- [ ] **CL-31** `CONTRADICTION` is returned, not a guessed winner *(F §4.2)*
- [ ] **CL-32** `NO_ANSWER` is returned rather than a fabrication *(F §4.2)*
- [ ] **CL-33** Confidence cannot change a resolution outcome *(F-CORE-07)* — mutate across full range, assert invariance
- [ ] **CL-34** Self-supersession, cycles, cross-vault, prohibited cross-scope and `PENDING`-supersedes-authoritative are all rejected *(F §6.1)*
- [ ] **CL-35** Superseded state cannot silently reactivate *(K-10)*
- [ ] **CL-36** `PENDING` never reaches an authoritative result *(F-CORE-07)*

## Provenance and audit

- [ ] **CL-37** Event log is hash-chained; single-record edit is detected *(F-CORE-12)* — K-05/K-18
- [ ] **CL-38** Hash-chain claims are **not** stated as authentication *(F-CORE-12)* — docs + test names
- [ ] **CL-39** Manifest lists exactly what was emitted *(F-CORE-09)* — emit-loop construction + test
- [ ] **CL-40** In-scope-but-not-served evidence claim is rejected *(K-04)*
- [ ] **CL-41** Package/manifest mismatch fails *(K-06)*

## Trust serialization

- [ ] **CL-42** Every agent-visible read returns an envelope *(F-CORE-14)* — exhaustive surface test
- [ ] **CL-43** Content cannot create a second machine-owned item *(K-23)*
- [ ] **CL-44** Content cannot forge trust or provenance fields *(K-23)*
- [ ] **CL-45** Instruction-shaped content remains evidence *(K-02)*
- [ ] **CL-46** No claim of prompt-injection immunity appears anywhere *(C §7.1)*

## Context budget atomicity

- [ ] **CL-47** An item is `FULL`, `TRUNCATED` or `OMITTED` — never emitted stripped *(F-CORE-14)* — K-20
- [ ] **CL-48** Envelope survives truncation; only content shortens *(H §4)* — K-20
- [ ] **CL-49** Package stays within budget *(FR-027)*
- [ ] **CL-50** Omissions are recorded and countable *(H §3.1)*

## Canonical single writer

- [ ] **CL-51** Second concurrent writer fails visibly *(F-CORE-13)* — K-24
- [ ] **CL-52** Stale lock is surfaced, never silently stolen *(N §1 principle 5)*
- [ ] **CL-53** No silent concurrent append to the event log *(F-CORE-13)*

## Resource safety

- [ ] **CL-54** Request, item, package and event size bounds exist *(F-CORE-15)* — K-24b
- [ ] **CL-55** Bounds are technical safety limits — no quota, tier, trial or daily concept exists in the code *(F-CORE-15)* — grep audit
- [ ] **CL-56** A safety rejection never silently discards canonical state *(F-CORE-15)*

## Ingestion allowlist

- [ ] **CL-57** Only supported extensions are admitted *(F-CORE-16)*
- [ ] **CL-58** `.fehrest/` is excluded from knowledge indexing *(F-CORE-16)*
- [ ] **CL-59** `.git/` is excluded from knowledge indexing *(F-CORE-16)*
- [ ] **CL-60** Unsupported content is excluded by default, not by pattern-matching secrets *(F-CORE-16)*

## Benchmark fairness

- [ ] **CL-61** Baselines and Fehrest share one task definition and one grading path *(K §5)*
- [ ] **CL-62** No Fehrest-only metadata leaks into baseline arms *(prompt requirement)*
- [ ] **CL-63** Context cost is measured for every arm, not only the Fehrest arm *(K §5)*
- [ ] **CL-64** Fixtures are not tuned after seeing results *(K §7)*
- [ ] **CL-65** Negative results are reported as measured *(Constitution XVII)*

## Scope discipline

- [ ] **CL-66** No graph, vector, embedding, CRDT, sync, MCP, Cedar or UI module exists *(freeze §9)* — file listing
- [ ] **CL-67** No automatic memory extraction or promotion exists *(Phase T scope D)*
- [ ] **CL-68** Kill tests for absent surfaces are marked `DEFERRED_SURFACE_NOT_PRESENT`, never `PASS`
- [ ] **CL-69** Platform claims match executed platforms *(prompt requirement)*
- [ ] **CL-70** `unsafe` count in Fehrest code is zero *(Constitution workflow)*
