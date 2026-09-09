# Tasks — Spec 002 Post-R1 Canonical Core Convergence

**Status:** GATE_A_CLOSED → SLICE_A_ACTIVE (T041–T045) → SLICE_B_READY (T046 onward)
**Frontier:** `specs/CURRENT.md` ACTIVE_SPEC=002-post-r1-canonical-core-convergence SPEC_002_STATUS=ACTIVE_SLICE_A
**Policy:** `OPENAI_API_KEY_USAGE=PROHIBITED` — zero paid model calls; this file ticked only after evidence exists.

Tick tasks only after evidence exists.

## Gate A — Activation

- [x] **T037** Record live GitHub/local implementation state used for work and reconcile it against the historical R1 v1.1 anchor.
- [x] **T038** Record the R1 terminal verdict and the route it authorizes. (R1-v3 terminal THESIS_SUPPORTED_ON_COST_CAVEAT, docs/canonical/R1_V3_TERMINAL_VERDICT_2026-09-09.md, pilot 556b32..., confirmatory 05443fe6..., B5 vs B4 p=1.2e-32)
- [x] **T039** Record explicit founder authorization for Spec 002. (docs/canonical/FOUNDER_AUTHORIZATION_SPEC_002_2026-09-09.md)
- [x] **T040** Update `specs/CURRENT.md` from `BLOCKED` to `ACTIVE` in the activation commit. (this commit)

## Slice A — Activation (Gate A) — CLOSED

- [x] **T037** Record live GitHub/local implementation state used for work and reconcile it against the historical R1 v1.1 anchor. (`docs/canonical/T037_IMPLEMENTATION_BASELINE.md`, bundle `a36639da` verify PASS, HEAD `ed79d8e`/`f7ea7e0f`)
- [x] **T038** Record the R1 terminal verdict and the route it authorizes. (R1-v3 `THESIS_SUPPORTED_ON_COST_CAVEAT`, `docs/canonical/R1_V3_TERMINAL_VERDICT_2026-09-09.md`, pilot `556b32` 972, confirmatory `05443fe6` 1404, B5 vs B4 p=1.2e-32, cost caveat)
- [x] **T039** Record explicit founder authorization for Spec 002. (`docs/canonical/FOUNDER_AUTHORIZATION_SPEC_002_2026-09-09.md` 2026-09-09T04:00:00Z, route permits Phase 1 with cost as primary constraint)
- [x] **T040** Update `specs/CURRENT.md` from `BLOCKED` to `ACTIVE` in the activation commit. (`a8d3052` Merge #57 `feat/spec-002-activation` c54734d)

## Slice B — Phase T truth reconciliation — COMPLETE (T041–T045)

- [x] **T041** Create `docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md`. (`docs/reviews/PHASE_T_IMPLEMENTATION_CONFORMANCE.md` 2026-09-09, §1–§8 covers source baseline `ed79`, fully vs minimized, R1-exercised vs deferred, 6 spec §4 distinctions, bootstrap constraint preserved)
- [x] **T042** Reconcile Phase T memory requirements against the absence of a durable product memory journal/CLI write surface; preserve historical truth and defer product memory to its planned phase. (conformance §4.2: four-axis semantics + temporal resolver implemented in `src/memory.rs`/`temporal.rs`, durable CLI/journal absent and correctly deferred to Spec 006 `phase4-memory-productization`, not silently pulled into Phase 1)
- [x] **T043** Reconcile the Phase T bounded compiler against the full Context Compiler specification; preserve production convergence for Phase 5. (conformance §4.3: Phase T bounded deterministic assembly (`src/context.rs`) vs full H receipted pipeline (`SelectionTrace`, grant/digest/high-water, tokenizer, gateway) preserved for Spec 007 `phase5-context-compiler-agent-gateway`)
- [x] **T044** Reconcile Phase T byte budgeting and the historically unavailable incremental-vs-clean B-12 arm. (conformance §4.4: `limits::*` byte safety ceilings not tokenizer pins, B-12 `UNAVAILABLE` because `INCREMENTAL_REINDEX=YAGNI_DEFERRED` in `src/derived.rs`, honestly reported `UNTESTED` never `PASS` per `analyze.md` A-01)
- [x] **T045** Run Spec Kit analyze + Ponytail necessity gate for the Phase 1 implementation. (`specs/002-post-r1-canonical-core-convergence/analyze.md` post-Slice-A 2026-09-09 + `ponytail-gate.md` T045 PASS KEEP/REUSE/0 new deps, cost ZERO)

## Slice C — Vault format and crash-safe canonical writes

- [ ] **T046** Specify the minimal vault identity/version metadata schema.
- [ ] **T047** Implement vault metadata create/open validation.
- [ ] **T048** Add fixtures for current, older/upcastable and unsupported/newer vault formats as required.
- [ ] **T049** Measure native replacement semantics on Windows and Linux before finalizing the canonical write helper.
- [ ] **T050** Implement crash-aware canonical object replacement.
- [ ] **T051** Add fault injection across temp create/write/flush/sync/replace/cleanup.
- [ ] **T052** Prove zero silent partial canonical success across the required fault matrix.
- [ ] **T053** Verify unknown frontmatter preservation after the new write path.

## Slice D — Writer-owned mutation

- [ ] **T054** Inventory every canonical mutation entry point.
- [ ] **T055** Select the smallest writer-capability/chokepoint design using Ponytail.
- [ ] **T056** Refactor canonical mutation to require/prove writer ownership.
- [ ] **T057** Add direct-bypass negative tests.
- [ ] **T058** Preserve visible second-writer failure and no-auto-steal behavior.
- [ ] **T059** Add stale-lock diagnostics only if they do not widen authority or misrepresent PID state as authentication.

## Slice E — Versioned event journal

- [ ] **T060** Define compatibility for the historical event schema and the next versioned envelope.
- [ ] **T061** Replace production free-form event-detail usage with the typed payload variants required by Phase 1.
- [ ] **T062** Freeze canonical hash serialization for each versioned event schema participating in the chain.
- [ ] **T063** Define and implement the event append flush/sync durability boundary.
- [ ] **T064** Commit a historical event-log golden fixture.
- [ ] **T065** Implement read-time upcasting without rewriting historical bytes.

## Slice F — Startup integrity and recovery

- [ ] **T066** Implement startup integrity gating before writable open.
- [ ] **T067** Detect and preserve torn final records.
- [ ] **T068** Implement authorized torn-tail quarantine/recovery.
- [ ] **T069** Fail closed on mid-log sequence gaps.
- [ ] **T070** Fail closed on hash-chain breaks.
- [ ] **T071** Record recovery/synthetic events according to the Recovery Model.
- [ ] **T072** Add kill-and-restart fault matrices spanning canonical write + event append.
- [ ] **T073** Run the exact Phase 1 randomized kill/restart criterion owned by the canonical implementation plan and preserve raw evidence.

## Slice G — Verification and closeout

- [ ] **T074** Run fmt/check/clippy/test and dependency/security gates.
- [ ] **T075** Run native filesystem gates on genuinely available platforms; report missing platform evidence explicitly.
- [ ] **T076** Re-run all applicable Phase T kill/security tests.
- [ ] **T077** Reconcile and verify historical R1 v1.1 semantic evidence remains unchanged by Spec 002.
- [ ] **T078** Conduct dedicated crash/recovery/writer-boundary adversarial review.
- [ ] **T079** Resolve every blocker without weakening frozen invariants.
- [ ] **T080** Produce `verification.md` with exact evidence.
- [ ] **T081** Produce final `analyze.md` cross-artifact consistency review.
- [ ] **T082** Close Spec 002 only if every Phase 1 exit criterion is genuinely met.
- [ ] **T083** Update `specs/CURRENT.md` to the next authorized frontier. Do not activate Spec 003 without its entry authorization.

## Closeout commands

At minimum:

```text
cargo fmt --check
cargo check --all-targets
cargo clippy --all-targets --all-features -- -D warnings
cargo test
```

Plus the active native-filesystem, crash/recovery, security and historical-evidence preservation commands defined during the Spec Kit.

## Explicitly unauthorized

No task above authorizes:

```text
graph
vectors
automatic memory
MCP / agent gateway
Firecrawl
LlamaIndex
LangGraph
LangChain
Mem0 integration
Letta integration
Graphiti integration
OpenSandbox product integration
UI
```

Those systems remain donors/benchmarks for later gates.
