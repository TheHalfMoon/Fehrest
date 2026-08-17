# Fehrest Evidence Log

**Status:** CANONICAL MEASUREMENT RECORD
**Date of measurements:** 2026-08-17
**Purpose:** Every load-bearing claim in the Fehrest planning package cites an entry here. If an entry is wrong, the decision it supports is void.

This document exists so that adversarial reviewers can attack *measurements* rather than *opinions*. Each entry states the exact command, the exact output, and what may and may not be concluded from it.

Labels used throughout the planning package:

| Label | Meaning |
|---|---|
| `FACT` | Directly observed in this session, reproducible by the command shown. |
| `INFERENCE` | A conclusion drawn from one or more FACTs. Defeasible. |
| `RECOMMENDATION` | A decision proposal. Depends on stated FACTs/INFERENCEs. |
| `HYPOTHESIS` | Unproven. Requires an experiment before it may drive implementation. |
| `VENDOR-REPORTED` | Claimed by an upstream project, not independently reproduced here. |

---

## E-0 — Canonical repository state

> **CORRECTED IN F1-R1 ([R1-01](../reviews/F1-R1-RECONCILIATION.md)).** The F1 version of this entry concluded that `TheHalfMoon/Fehrest` did not exist. That conclusion was a **category error** — it treated "not visible to this token" as "does not exist" — and is retracted.

**Command:**
```bash
gh api repos/TheHalfMoon/Fehrest
gh api user --jq .login
gh api "users/TheHalfMoon/repos?type=all&per_page=100"
```

**Output:**
```
repos/TheHalfMoon/Fehrest  → HTTP 404 Not Found
authenticated principal    → wepld
users/TheHalfMoon/repos    → public entries only; no Fehrest listed
```

**FACT:** The 404 is reproducible.

**FACT:** The authenticated principal in this environment is **`wepld`**, a different account from **`TheHalfMoon`**.

**FACT:** `users/<user>/repos` returns only repositories visible to the caller. For an unaffiliated token this is the public set. **Absence from that listing is not evidence of non-existence.**

**INFERENCE — the correction:** A 404 from an unaffiliated token against a private repository is **indistinguishable** from a 404 against a nonexistent one. GitHub returns 404 rather than 403 for private repositories precisely to avoid disclosing their existence. The F1 entry read an authorization signal as an existence signal.

**CANONICAL TRUTH (founder-asserted, authoritative over this environment):**

| Property | Value |
|---|---|
| Canonical repository | **`TheHalfMoon/Fehrest`** |
| Visibility | private |
| Default branch | `main` |
| Size | 0 |
| Implementation | none |

**ENVIRONMENT ACCESS LIMITATION:** This session cannot read `TheHalfMoon/Fehrest`. That is a limitation of the credential available here, recorded as such. It is not evidence about the repository.

**FACT:** `wepld/Fehrest` exists (public, created 2026-08-02, empty — `HTTP 409 "Git Repository is empty"`, zero branches). It is **NOT canonical for this project**, is not a fallback, and receives no planning work.

**FACT:** The local working directory `C:\Users\Shehr\OneDrive\Desktop\Fehrest` was empty and not a git repository at F1 session start. A local repository was initialised there to hold the planning package. As of F1-R1 its `origin` is set to `https://github.com/TheHalfMoon/Fehrest.git`. **Nothing has been pushed to any remote.**

**FACT:** There is no pre-existing Fehrest source code, schema, or planning artifact other than this package.

**INFERENCE:** Fehrest is greenfield — no migration path, backward-compatibility constraint, or legacy invariant exists. There is **no upstream repository HEAD to report**, because the canonical repository is empty (size 0).

**Consequence for review:** Any reviewer statement of the form "the current implementation does X" is unsupportable. There is no implementation. Repository *identity* is CLOSED; only license, publication strategy and release timing remain open ([Q-1](../16-OPEN-QUESTIONS.md#q-1--repository-identity-closed)).

---

## E-1 — Graphify: pinned version and license

**Command:**
```bash
git clone --depth 1 --branch v8 https://github.com/Graphify-Labs/graphify.git
git rev-parse HEAD
```

**Output:**
```
PINNED_COMMIT: 0738af373af9cf5c95f862cc5f3327fd96b4ea23
DATE: 2026-08-16T21:12:56+01:00
```

**FACT:** Default branch is `v8` (not `main`/`master`). Language Python. Stars 107,385. `archived: false`.

**FACT (licensing):** `LICENSE` is Apache License 2.0. `NOTICE` states: *"This product is licensed under the Apache License, Version 2.0... Portions of this software were contributed under the MIT License prior to the relicensing and remain available under those terms."* `LICENSE-MIT` retains the original MIT text (Copyright 2026 Safi Shamsi). `pyproject.toml` declares `license = "Apache-2.0"` and `license-files = ["LICENSE", "LICENSE-MIT", "NOTICE"]`.

**INFERENCE:** Apache-2.0 is compatible with a permissively licensed Fehrest and imposes attribution + NOTICE propagation + patent-grant terms. Copying code requires preserving `NOTICE`. This is a tractable obligation, not a blocker.

**FACT:** PyPI distribution name is `graphifyy` (not `graphify`), version `0.9.45`. `requires-python = ">=3.10"`.

---

## E-2 — Graphify: module inventory and size

**Command:**
```bash
find graphify -name '*.py' | wc -l
find graphify -name '*.py' -exec wc -l {} + | tail -1
```

**Output:**
```
81
60202 total
```

**FACT:** 81 Python modules, 60,202 lines, in the `graphify/` package.

**FACT (pipeline, from `ARCHITECTURE.md` at the pinned commit):**
```
detect() → extract() → build() → cluster() → analyze helpers → report.generate() → export.to_*()
```
Stages communicate through "plain Python dicts and NetworkX graphs — no shared state, no side effects outside `graphify-out/`."

**FACT (extraction schema, from `ARCHITECTURE.md`):**
```json
{
  "nodes": [{"id": "...", "label": "...", "source_file": "path", "source_location": "L42"}],
  "edges": [{"source": "id_a", "target": "id_b", "relation": "calls|imports|uses|...",
             "confidence": "EXTRACTED|INFERRED|AMBIGUOUS"}]
}
```

**FACT (upstream security posture, `ARCHITECTURE.md` + `SECURITY.md`):** external input passes `graphify/security.py`: `validate_url()` (http/https only, blocks `file://` redirects), `safe_fetch()` (size cap, timeout), `validate_graph_path()` (must resolve inside `graphify-out/`), `sanitize_label()` (strips control chars, caps 256 chars, HTML-escapes).

**INFERENCE:** Graphify already implements path-confinement and label sanitisation of the same class Fehrest requires. This is reusable prior art, not a gap to invent. It is **not** sufficient on its own — see [E-4](#e-4--extractor-ids-are-name-derived-by-design-not-by-defect).

---

## E-3 — Graphify: dependency weight and installed footprint

**Command:**
```bash
uv venv gfenv
uv pip install --python gfenv/Scripts/python.exe "graphifyy==0.9.45"
uv pip list --python gfenv/Scripts/python.exe | wc -l
du -sh gfenv/Lib/site-packages
```

**Output:**
```
32
130M	gfenv/Lib/site-packages
131M	gfenv
```

**FACT:** A base install of `graphifyy==0.9.45` resolves to **32 packages** occupying **130 MB** of `site-packages` on Windows, excluding the CPython runtime itself.

**FACT (from `pyproject.toml`):** base `dependencies` include `networkx>=3.4`, `numpy>=1.21`, `rapidfuzz>=3.0`, and **28 separate `tree-sitter-*` grammar packages** (python, javascript, typescript, go, rust, java, groovy, c, cpp, ruby, c-sharp, kotlin, scala, php, swift, lua, zig, powershell, elixir, objc, julia, verilog, fortran, bash, json, plus `tree-sitter` core). Optional extras add ~25 more feature groups (`mcp`, `pdf`, `watch`, `svg`, `leiden`, `office`, `postgres`, `video`, `neo4j`, `falkordb`, and per-provider LLM extras).

**FACT (upstream-documented packaging hazards, comments in `pyproject.toml`):**
- `tree-sitter-dm` "ships only a Windows wheel, so on Linux/Mac it must compile from source (needs a C toolchain + python3-dev)" — kept optional to avoid breaking default install (#1104).
- The `mcp` extra floors `starlette>=1.3.1` explicitly "above the CVE-2026-48818 / CVE-2026-54283 fixes".

**INFERENCE:** Embedding Graphify means shipping a CPython runtime plus ~130 MB of native wheels, ~30 of which are compiled grammars. Adding a bundled interpreter puts the realistic desktop-installer delta in the **200–300 MB** range for the graph capability alone.

**INFERENCE:** The upstream project's own dependency comments show active CVE tracking in its transitive HTTP stack. Any Fehrest bundling strategy must therefore include an **independent update path for the sidecar**, not a frozen snapshot.

---

## E-4 — Extractor IDs are name-derived **by design**, not by defect

> **CORRECTED IN F1-R1 ([R1-05](../reviews/F1-R1-RECONCILIATION.md)).** The F1 version cited upstream issues #550, #811, #1033 and #2614 as if they were live defects. **They are fixed.** Those citations are retracted. The architectural conclusion is unchanged and now rests on structural evidence that no upstream fix can invalidate.

**Source:** `graphify/ids.py`, `graphify/extract.py`, `graphify/build.py` and `CHANGELOG.md` at pinned commit `0738af37`.

### The retracted claims

| Issue | F1 implied | Verified status at pinned commit |
|---|---|---|
| #2614 Turkish `İ` idempotency | current defect | **FIXED in 0.9.40 (2026-08-11)** — "`normalize_id()` is now idempotent for Turkish `İ` and similar codepoints by casefolding before the non-word filter" |
| #811 Unicode collapse | current defect | **FIXED** — NFKC applied before ID generation; `.casefold()` replaced `.lower()`; `[^\w]+` with `re.UNICODE` preserves CJK/Cyrillic/Arabic/accented Latin |
| #1033 AST-vs-semantic mismatch | current defect | **FIXED** at the relative-path remap chokepoint |
| #550 same-filename collisions | current defect | **ROOT CAUSE FIXED** — four hand-synced copies of the recipe unified into one `graphify.ids` module, "guarded by contract + hypothesis property tests" |

**FACT:** `_disambiguate_colliding_node_ids` exists in current code (`graphify/extract.py`, `graphify/build.py`) and actively salts colliding IDs apart.

**Assessment:** Graphify's identity layer is **actively maintained and hardened**, with property-based tests specifically guarding the normalisation contract. Describing it as bug-ridden was wrong.

### The structural facts that survive

**FACT:** `ids.py` normalises: NFKC → casefold → NFKC → replace non-word runs with `_` → collapse `_` → strip. IDs are **derived from names**, not allocated.

**FACT:** File-level node IDs follow the documented spec **`{parent_dir}_{stem}`** (`graphify/extract.py:182`). The identifier is therefore a **function of the file's path**.

**FACT — the decisive one:** The CHANGELOG records that an extension-aware ID scheme was considered and rejected because it *"would rewrite every file and symbol id and force a full-rebuild migration in lockstep with the skill/validation id spec."*

**FACT:** Incremental updates can carry stale derived edges across an upstream fix: after the #1814 fix, "because `graphify update` only re-extracts changed files, an unchanged wrapper keeps that edge until it is next edited or a `--force` full rebuild runs."

### Conclusion

**INFERENCE — load-bearing, and now defect-independent:** Extractor IDs cannot be Fehrest identities, for three structural reasons:

1. **Path-derived.** `{parent_dir}_{stem}` changes when a file is renamed or moved. Identity that changes on `mv` is not identity.
2. **Scheme-versioned.** Upstream states plainly that changing the scheme rewrites every ID. An identifier whose scheme is expected to change across versions cannot anchor durable references.
3. **Rebuild-sensitive.** Incremental derived state can hold stale IDs until a forced rebuild.

None of these is a bug. All three follow from what an extractor ID is *for* — addressing nodes within one build of one graph. That is a legitimate design, and it is simply not the same thing as durable object identity.

**This argument is strictly stronger than F1's**, because upstream fixing every open issue would leave it untouched.

**RECOMMENDATION:** Fehrest allocates its own opaque identities; `extractor_id` is a derived, non-authoritative, rebuildable mapping column. Formalised as invariants **G-ID-1…G-ID-4** ([B §1](../01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities)) and [ADR-0004](../09-TECHNOLOGY-DECISIONS.md#adr-0004--object-identity-is-fehrest-allocated-and-opaque).

**Generalisation:** this applies to **any** extractor, not to Graphify specifically — which is what makes it an invariant rather than a donor caveat ([R1-06](../reviews/F1-R1-RECONCILIATION.md)).

---

## E-5 — Graphify: measured extraction throughput (PRELIMINARY)

> **RECLASSIFIED IN F1-R1 ([R1-07](../reviews/F1-R1-RECONCILIATION.md)):** `PRELIMINARY / SINGLE-ENVIRONMENT / SINGLE-CORPUS`. One machine, one corpus (Graphify's own Python source), Windows, cold cache. The linear extrapolation below is **not a verified system property** and must not drive runtime or packaging decisions. [GI-BENCH](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) supersedes it.

**Command:** (run against Graphify's own source tree as the corpus)
```python
from graphify.extract import extract, collect_files
files = collect_files(Path('graphify').resolve())
res = extract(files, root=root)
```

**Output:**
```
AST extraction: 776/776 uncached files (100%) [12 workers]
extract: 42.22s  nodes=13770 edges=26894
confidence: Counter({'EXTRACTED': 26147, 'INFERRED': 747})
relations: [('calls', 9383), ('contains', 8965), ('rationale_for', 3288),
            ('imports', 1914), ('references', 1776), ('imports_from', 808),
            ('method', 325), ('indirect_call', 166)]
```

**FACT:** 776 files → 42.22 s wall clock with 12 worker processes → **≈18.4 files/second** on the measurement machine (Windows 11, cold cache).

**FACT:** 13,770 nodes and 26,894 edges from 776 files → ≈17.7 nodes and ≈34.7 edges per file.

**FACT — measured confidence distribution:** `EXTRACTED` 26,147 (97.2%), `INFERRED` 747 (2.8%), **`AMBIGUOUS` 0 (0.0%)**.

**INFERENCE:** The advertised three-level confidence model is, on this corpus, a **two-level model**. Fehrest must not build UI or trust logic that depends on `AMBIGUOUS` being populated. Treat the vocabulary as open but expect binary behaviour.

**HYPOTHESIS — naive linear extrapolation. NOT A BUDGET. NOT A SYSTEM PROPERTY.**

| Vault size | Naive linear projection |
|---|---|
| 1,000 files | ≈55 s |
| 10,000 files | ≈9 min |
| 100,000 files | ≈90 min |

**These numbers must not be cited as Fehrest performance characteristics** ([R1-07](../reviews/F1-R1-RECONCILIATION.md)). They assume linearity in file count on one corpus of one type on one machine. Cross-file symbol resolution is plausibly superlinear, and corpus composition (code-heavy vs Markdown-heavy, many-small vs few-large) is entirely unmodelled. Tracked as [HYPOTHESIS H-2](#h-2--extraction-scales-linearly-in-file-count); measured by [GI-BENCH](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix).

**INFERENCE — load-bearing:** A full graph rebuild of a large vault is a **tens-of-minutes background job**, not an interactive operation. Therefore: incremental extraction is mandatory, not an optimisation; graph availability must never gate application startup; and rebuild must be resumable and cancellable.

**FACT (graceful degradation observed):** missing optional grammars produced warnings and partial graphs rather than failure — e.g. *"6 `.sql` file(s) contributed nothing... tree_sitter_sql not installed"*, *"1 file(s) had syntax errors and may be partially extracted"*. A caching layer exists (`N/M uncached files`), and empty extractions are deliberately not cached so they retry (#1666).

---

## E-6 — Graphify: startup cost (PRELIMINARY)

> **RECLASSIFIED IN F1-R1 ([R1-07](../reviews/F1-R1-RECONCILIATION.md)):** `PRELIMINARY / SINGLE-ENVIRONMENT`. Windows 11, one machine, cold filesystem cache. Directionally strong (a ~16× cold/warm gap is unlikely to be measurement noise) but not cross-platform verified. [GI-BENCH](../10-BENCHMARK-PLAN.md#b-11--gi-bench--graph-intelligence-benchmark-matrix) must confirm before [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape) is finalised.

**Command:**
```bash
for i in 1 2 3; do <time> python -c "pass"; done
for i in 1 2 3; do <time> python -c "import graphify.extract"; done
```

**Output:**
```
bare interpreter:        119 ms, 101 ms, 98 ms
import graphify.extract: 4451 ms, 276 ms, 276 ms
```

**FACT:** Bare CPython start ≈98–119 ms. First `import graphify.extract` **4,451 ms**; subsequent imports **276 ms** (warm filesystem/bytecode cache).

**INFERENCE — load-bearing, decides the Graphify integration shape:**
- **Per-operation subprocess invocation is not viable.** Even warm, ≈376 ms of pure process+import overhead per call makes per-file or per-keystroke invocation impossible; the 4.45 s cold path would make first use appear broken.
- **A long-lived sidecar process amortises this to once per application session.**
- No evidence yet justifies a Rust port. The cost being amortised is *startup*, which a sidecar removes entirely; porting 60,202 lines would address throughput, which has not yet been shown to be the binding constraint.

**RECOMMENDATION:** Managed long-lived sidecar. See [ADR-0003](../09-TECHNOLOGY-DECISIONS.md#adr-0003--graph-intelligence-runtime-integration-shape).

---

## E-7 — Graphify: agent-facing surface

**Source:** `graphify/serve.py` at pinned commit.

**FACT — MCP tools exposed:** `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

**FACT — MCP resources exposed:** `graphify://report`, `graphify://stats`, `graphify://god-nodes`, `graphify://surprises`, `graphify://audit`, `graphify://questions`.

**FACT:** `serve.py` supports both stdio and HTTP transports, and contains bearer-token/authorization handling for the HTTP path. It is dual-compatible with the `mcp` 1.x decorator API and 2.x constructor-callback API, selected at runtime in `_build_server`.

**INFERENCE:** Graphify's MCP surface is designed for *codebase* interrogation and includes repository/PR-specific tools irrelevant to a personal knowledge vault. Fehrest must **not** re-expose this surface to agents directly: it would (a) leak a tool vocabulary Fehrest cannot authorise, and (b) hand agents a second, unaudited retrieval path that bypasses Fehrest's context compiler and scope checks. Fehrest calls the sidecar as a *library over a private channel* and publishes its own MCP surface.

---

## E-8 — Graphify's self-reported retrieval benchmarks

**Source:** `BENCHMARKS.md` at pinned commit; "Last updated: 2026-07-05."

**VENDOR-REPORTED:**

| Suite | Dataset (n) | Metric | graphify | Field |
|---|---|---|---|---|
| Memory | LOCOMO (300) | QA accuracy | 45.3% | supermemory 49.7%, bm25 31.3%, mem0 27.3% |
| Memory | LOCOMO (300) | recall@10 | 0.497 | bm25 0.362, mem0 0.048 |
| Memory | LongMemEval-S (50) | QA accuracy | 76% | dense RAG 76%, hybrid 74%, mem0 70% |
| Cost | LOCOMO ingest | USD | ≈$1.40 | supermemory $15.67, mem0 $3.48 |
| Cost | graph build | LLM credits | $0 | n/a |

Harness detail: graphify's own harness, one shared model (Kimi K2.6), competing systems run as in-harness adapters, judge blind-validated against a second judge (90.6% agreement, Cohen's κ 0.81).

**INFERENCE — three material caveats that a hostile reviewer will raise, so we raise them first:**

1. **Self-authored harness.** The benchmark is run by the project being measured, with competitors wired in as adapters. This is disclosed and methodologically reasonable, but it is not third-party replication. Treat as VENDOR-REPORTED.
2. **LongMemEval-S at n=50 cannot distinguish the top systems.** 76% vs 76% vs 74% on 50 items: the 95% Wilson interval for 38/50 is roughly ±12 percentage points. graphify **ties** dense RAG here. This *falsifies* any claim that graph retrieval beats dense retrieval on long-horizon conversational QA — on the one prose-memory benchmark reported, it does not.
3. **The demonstrated wins are recall and cost, on code-shaped and conversational corpora — not prose QA accuracy.** recall@10 0.497 vs BM25 0.362 is a real margin; $0 index build vs $15.67 is a large margin.

**RECOMMENDATION:** Adopt Graphify for **code and structured-file understanding**, where its deterministic AST extraction is its measured strength and requires no LLM credits. Do **not** assume it outperforms lexical or dense retrieval over note prose. Fehrest's retrieval baseline must therefore be lexical-first (FTS5), with the graph as an *expansion* stage rather than the primary recall mechanism. This position is falsifiable by [Benchmark B-3](../10-BENCHMARK-PLAN.md).

---

## E-9 — DeepSeek Harness: pinned version and adoptable patterns

**Command:**
```bash
git clone --depth 1 https://github.com/deepseek-ai/deepseek-harness.git
git rev-parse HEAD
```

**Output:**
```
PINNED_COMMIT: 99f6f02fecdb7dff40c3fbc9470f5907c29f74ca
DATE: 2026-08-17T19:03:17+08:00
```

**FACT:** TypeScript, MIT licensed, default branch `master`, 147,412 stars, ~50 workspace packages under `packages/`, plus `native/landlock-run`, `apps/cli`, `apps/web`. Repository carries `THIRD_PARTY_NOTICES.md` and 45 English subsystem documents under `docs/subsystems/`.

**FACT — event log design (`docs/subsystems/session.md`):** A `Session` is an **append-only log of typed `SessionEvent`s** and is "the single source of truth for an agent's whole interaction history. The LLM message history is *derived* from the log, never stored separately; replay is re-derivation from the same events." Events are "lossless JSON and sequence numbers stay contiguous, including raw chunks, so persistence can store the canonical log verbatim." The event map is **merge-extensible** via TypeScript declaration merging; plugins add event types (e.g. `compaction/start|summary|end`, `hook/invoked|result`).

**FACT — observed core event vocabulary:** `turn/start`, `turn/end{reason}`, `step/start`, `step/end`, `user/message`, `assistant/chunk{chunk}`, assembled assistant message per step carrying `usage`. A `user/message` may be a human prompt, a synthetic `agent.inject()` context, or a goal continuation — "All three project their `content` verbatim; `source` tells them apart."

**FACT — persistence seam (`docs/subsystems/persistence.md`):** one abstract service (`ctx.sessionPersistence`) with **two interchangeable backends: JSONL and SQLite**, over the *same* `SessionEvent` type — "**no parallel persisted event type**." Writes batch within a bounded window; `session/flush` is the ordering and error-observation checkpoint.

**FACT — crash recovery:** a log crashed mid-turn has an open `turn/start` with no `turn/end`. The backend "does **not** truncate — a single turn can be huge in a long-horizon task... Instead it closes the orphaned turn with a synthetic `turn/end { reason: { kind: 'interrupted' } }`." `interrupted` is the one reason no loop ever emits. Repair applies only to cold sessions; live sessions reject rather than receive synthetic boundaries.

**FACT — metadata separation:** `SessionHeader` (format version, cwd, lineage, seed boundary) travels **separately** from the event log because these are "storage concerns, not conversation events, so they stay out of `SessionEventMap` and never reach `deriveMessages()`."

**FACT — approval seam (`docs/subsystems/approval.md`):** every request gets a fresh branded `ApprovalRequestId` pairing a log-only `approval/asked` with `approval/decided`. The brand deliberately prevents approval ids from being "interchangeable with tool-call or agent/session ids." Callers "fail closed unless it is `allowed-once`."

**FACT — spill seam (`docs/subsystems/spill.md`):** oversized tool text is persisted and replaced with an opaque locator. The request's `source` field is "used for naming and inspection — **not access control**"; `suggestedName` "may be used as a naming hint (**it is not a path**)."

**FACT — sandbox seam (`docs/subsystems/sandbox.md`):** `SandboxMode` is `'read-only' | 'workspace-write' | 'danger-full-access'`, governing **filesystem effects only**. Backends: Linux bwrap/Landlock, macOS Seatbelt, Windows ACL restricted-token. Two explicit limitations are documented upstream: *"Network and process visibility are outside this vocabulary,"* and the Windows ACL runner "grants no explicit writable root and **reports partial enforcement for its ambient ACL gaps**."

**FACT — invariants service (`docs/subsystems/invariants.md`):** a package-owned runtime invariant registry where each package registers checks under its exact npm name; `fail(message)` throws `InvariantError` with stable `code: 'INVARIANT'` and the owning `packageName`. A CI script mechanically rejects unexplained empty checks. What a check may assert is constrained to "authoritative event streams or mutable data, never service or method presence."

**FACT — session location (`docs/subsystems/persistence.md`):** `SessionLocation.path` is documented as "a location hint, **not authorization** or a freshness guarantee. Consumers must treat it as a location hint, never as an authorization token."

**INFERENCE:** Four of these are directly transplantable to Fehrest and materially de-risk its event plane: (1) derived-not-stored message history, (2) non-truncating crash repair via a synthetic terminator no producer emits, (3) one event type with two backends (JSONL canonical, SQLite derived), (4) header metadata outside the event vocabulary. Three are directly transplantable to Fehrest's security model: branded non-interchangeable ids, "source/name is not authorization," and honest partial-enforcement reporting.

**INFERENCE — a gap Fehrest must close itself:** the harness sandbox vocabulary explicitly excludes network egress, and its Windows backend self-reports incomplete enforcement. Fehrest cannot inherit a network boundary from this donor and must specify one independently. See [Threat Model T-11](../02-THREAT-MODEL.md).

**RECOMMENDATION:** ADAPT the patterns; do **not** take a runtime dependency on the harness or on Cordis. Rationale in [ADR-0005](../09-TECHNOLOGY-DECISIONS.md#adr-0005--fehrest-adapts-harness-event-patterns-without-depending-on-the-harness-runtime).

---

## E-10 — BlockSuite *distribution* is stale; the *implementation* is not (editor gate)

> **CORRECTED IN F1-R1 ([R1-02](../reviews/F1-R1-RECONCILIATION.md)).** F1 reported the staleness of the standalone mirror and **missed** that the editor is actively developed inside the AFFiNE monorepo. The conclusion drawn from the partial evidence — "therefore CodeMirror 6" — is retracted, and the editor decision is reopened as a prototype gate ([18-EDITOR-GATE](../18-EDITOR-GATE.md)). See §E-10.1 for the added evidence.

**Commands:**
```bash
gh api repos/toeverything/blocksuite/commits/main
gh api repos/toeverything/blocksuite/commits?per_page=5
gh api repos/toeverything/blocksuite/branches
gh api repos/toeverything/blocksuite/tags
curl -s https://registry.npmjs.org/@blocksuite/store
gh api repos/toeverything/AFFiNE
gh api repos/toeverything/AFFiNE/contents/blocksuite
```

**Output:**
```
blocksuite main HEAD: 5cb5cb68471ca692f3c162258f0087cb22fcb82d  2025-07-07T08:16:28Z

recent commits (all branches):
  2025-07-07  5cb5cb68  chore: sync affine blocksuite to packages (#9149)
  2025-07-01  a5091e72  chore: sync affine blocksuite to packages (#9147)
  2025-06-24  358ed364  chore: sync affine blocksuite to packages (#9146)
  2025-06-16  ee807e43  chore: sync affine blocksuite to packages (#9144)
  2025-06-09  cf6d8a4f  chore: Lock file maintenance (#9141)

branches: main, master, renovate/lock-file-maintenance,
  renovate/npm-dompurify-vulnerability, renovate/npm-file-type-vulnerability,
  renovate/npm-lodash-es-vulnerability, renovate/npm-minimatch-vulnerability,
  renovate/npm-simple-git-vulnerability, renovate/npm-vite-vulnerability,
  renovate/npm-vitest-vulnerability

tags (latest): v0.22.4

npm @blocksuite/store: latest 0.22.4, registry modified 2025-07-01
  publish history tail: 0.20.0 (2025-03-16), 0.21.0 (2025-04-07), 0.22.4 (2025-07-01)

toeverything/AFFiNE: default branch canary, HEAD b4c8548c 2026-08-17T04:01:30Z
AFFiNE/blocksuite/ contains: affine, docs, docs-site, framework,
  integration-test, playground, tsconfig.json
```

**FACT:** `toeverything/blocksuite` `main` last received a commit on **2025-07-07** — 13.4 months before the date of this measurement (2026-08-17).

**FACT:** The commit messages are `chore: sync affine blocksuite to packages`. The repository is a **downstream mirror** of packages developed inside AFFiNE, and that sync stopped.

**FACT:** `@blocksuite/store` on npm was last published **2025-07-01** at version **0.22.4**. There have been no releases in 13.5 months. The version is pre-1.0.

**FACT:** Six open `renovate/npm-*-vulnerability` branches (dompurify, file-type, lodash-es, minimatch, simple-git, vite, vitest) remain **unmerged**.

**FACT:** `toeverything/AFFiNE` is actively developed (HEAD 2026-08-17) and contains `blocksuite/` as an in-repo directory tree.

**FACT (AFFiNE licensing):** AFFiNE's `LICENSE` is a split license. Content under `packages/backend` and `packages/common/native` is governed by a separate license file; "Content outside of the above mentioned directories... is available under the 'MIT' license as defined in `LICENSE-MIT`." The `toeverything/blocksuite` mirror itself reports **MPL-2.0**.

**INFERENCE:** The standalone **distribution path** is not viable. Depending on `@blocksuite/*` from npm would mean depending on packages unpublished for 13.5 months at pre-1.0.

---

### E-10.1 — The evidence F1 missed: the AFFiNE subtree is active

**Command:**
```bash
gh api "repos/toeverything/AFFiNE/commits?path=blocksuite&per_page=10"
```

**Output:**
```
2026-08-10  6375f5ab  chore: bump typescript 7 (#15465)
2026-08-10  0c7b20dc  chore: migrate oxlint & oxfmt (#15464)
2026-08-10  ee899a26  feat(server): improve context management (#15448)
2026-08-05  921e83bb  chore: bump @atlaskit/pragmatic-drag-and-drop-auto-scroll (#15412)
2026-07-31  6170a907  feat(editor): add permanent global toggle for code block line numbers (#15376)
2026-07-31  fb647b60  chore: bump up js-yaml version to v5 [SECURITY] (#15385)
2026-07-28  b6fc0a21  fix(mobile): mobile keyboard padding (#15365)
2026-07-28  e7ec8a10  feat(editor): improve select perf (#15353)
```

**FACT:** The `blocksuite/` subtree inside `toeverything/AFFiNE` received commits through **2026-08-10** — one week before this measurement — including editor feature work (#15376, #15353), a mobile fix (#15365), toolchain upgrades (#15465, #15464) and a **security** dependency bump (#15385).

**INFERENCE — the correction:** The editor implementation is **actively maintained**. F1's characterisation of BlockSuite as an unmaintained component was wrong; what is unmaintained is the standalone *mirror and npm distribution*. These are different claims with different consequences.

**INFERENCE:** Two F1 sub-arguments weaken materially:
- *"Unpatched transitive vulnerabilities"* — security bumps land in the maintained tree (#15385). The unmerged renovate branches sit on the abandoned mirror, not on the code that would be vendored.
- *"The gate cannot be cleared against a maintained upstream"* — **false.** It can be cleared against `AFFiNE/blocksuite/…` at a pinned commit.

**FACT (unchanged, and still a real cost):** AFFiNE's license is split — MIT applies outside `packages/backend` and `packages/common/native`. Vendoring requires per-file license provenance. The monorepo is 446 MB, so extraction and coupling are genuine engineering problems.

**RECOMMENDATION — REPLACES the F1 recommendation:** Reclassify the editor decision from *decided* to **OPEN / PROTOTYPE-GATED**. Evaluate Candidate A (CodeMirror 6) against Candidate B (**maintained AFFiNE `blocksuite/` subtree at a pinned commit — never the stale standalone package**) via an executable bake-off. See [18-EDITOR-GATE](../18-EDITOR-GATE.md) and [ADR-0002](../09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated).

**Method note for reviewers:** the F1 error was querying repository health at the *repository* level when development had moved to a *subtree of a different repository*. Repository-level staleness signals are unreliable whenever a project vendors its own packages. Generalised into the registry's current-vs-historical risk fields ([R1-20](../reviews/F1-R1-RECONCILIATION.md)).

---

## E-11 — Yjs and CodeMirror are healthy; the CRDT is not the stale part

**Commands:**
```bash
gh api repos/yjs/yjs/contents/LICENSE
curl -s https://registry.npmjs.org/yjs
curl -s https://registry.npmjs.org/@codemirror/state
gh api repos/codemirror/dev
```

**Output:**
```
yjs LICENSE: The MIT License (MIT), Copyright (c) 2023 Kevin Jahns; RWTH Aachen
yjs npm: latest 13.6.32, modified 2026-08-04
@codemirror/state npm: latest 6.7.1, modified 2026-07-05, license MIT
codemirror/dev: archived: true  (meta-repo only; @codemirror/* packages ship independently)
```

**FACT:** Yjs is MIT licensed and actively released — 13.6.32 published within 2 weeks of this measurement.

**FACT:** CodeMirror 6 is MIT and current (`@codemirror/state` 6.7.1, 2026-07-05). The archived `codemirror/dev` repository is the historical meta-repo; the runtime packages are published separately and remain maintained.

**INFERENCE:** The staleness identified in [E-10](#e-10--blocksuite-distribution-is-stale-the-implementation-is-not-editor-gate) is specific to the **block-editor layer**, not to the CRDT layer or to text-editor substrates generally. Deferring BlockSuite therefore does not require deferring Yjs on maintenance grounds — it is deferred on *necessity* grounds (single-user MVP needs no CRDT), which is a weaker and more reversible reason.

---

## E-12 — Vector-store maturity

**Commands:**
```bash
gh api repos/asg017/sqlite-vec ; gh api repos/asg017/sqlite-vec/tags
gh api repos/unum-cloud/usearch
gh api repos/quickwit-oss/tantivy
```

**Output:**
```
sqlite-vec: Apache-2.0, pushed 2026-05-18, 8023 stars
sqlite-vec tags: v0.1.10-alpha.4, v0.1.10-alpha.3, v0.1.10-alpha.2,
                 v0.1.10-alpha.1, v0.1.9
USearch: Apache-2.0, pushed 2026-07-10, 4268 stars
tantivy: MIT, pushed 2026-08-17, 15716 stars
```

**FACT:** sqlite-vec's newest tags are **`v0.1.10-alpha.*`**; the newest non-alpha is `v0.1.9`. It is pre-1.0 and its current release line is explicitly alpha. Last push 2026-05-18 (3 months before measurement).

**FACT:** USearch (Apache-2.0) and Tantivy (MIT) are both actively maintained; Tantivy was pushed the day of measurement.

**INFERENCE:** sqlite-vec's alpha status is by itself sufficient reason to forbid it from being a *required* component. This independently confirms the constitution's "vectors are optional and rebuildable" clause on engineering grounds rather than philosophical ones.

---

## E-13 — Supporting donors and standards verified live

**Command:** `gh api repos/<each>`

| Source | License | Last push | Note |
|---|---|---|---|
| `obsidianmd/jsoncanvas` | MIT | 2026-07-24 | JSON Canvas spec, active |
| `google/magika` | Apache-2.0 | 2026-08-15 | content-type detection |
| `docling-project/docling` | MIT | 2026-08-17 | 64,911 stars, very active |
| `microsoft/markitdown` | MIT | 2026-07-29 | 174,202 stars |
| `ggml-org/llama.cpp` | MIT | 2026-08-17 | optional local inference |
| `tauri-apps/tauri` | Apache-2.0 | 2026-08-17 | desktop shell + capabilities |
| `cedar-policy/cedar` | Apache-2.0 | 2026-08-14 | authorization model |
| `bytecodealliance/wasmtime` | Apache-2.0 | 2026-08-14 | future plugin isolation |
| `ethz-spylab/agentdojo` | MIT | 2026-06-02 | prompt-injection benchmark |
| `cordiverse/cordis` | MIT | 2026-08-13 | harness's own framework |

**FACT:** All ten exist, are unarchived, and carry permissive licenses compatible with a permissive Fehrest.

---

## E-14 — LongMemEval-V2 exists and defines the right target

**Source:** web search; arXiv `2605.12493`; HF dataset `xiaowu0162/longmemeval-v2`; project page `xiaowu0162.github.io/longmemeval-v2/`.

**FACT (as reported by the paper/dataset pages):** LongMemEval-V2 contains **451 manually curated questions** and **1,870 task trajectories** in WebArena-style and ServiceNow-style environments. Histories reach **up to 500 trajectories and 115M tokens**. Memory systems "consume the trajectory history and return compact evidence for downstream question answering," with **accuracy and query latency** both targeted as metrics.

**FACT — the five measured memory abilities:**
1. **static state recall** — remembers important landmarks and page layouts
2. **dynamic state tracking** — understands how states change over time
3. **workflow knowledge** — knows the steps for recurring tasks
4. **environment gotchas** — recognises recurring local failure modes
5. **premise awareness** — detects assumptions valid elsewhere but wrong here

**FACT — reported results:** AgentRunbook-C 72.5% average accuracy; strongest RAG baseline 48.5%; off-the-shelf coding-agent baseline 69.3%.

**INFERENCE — load-bearing for the memory model:** These five abilities are an externally defined, measurable target that maps almost exactly onto Fehrest's memory taxonomy. Fehrest should adopt them as the **primary specification** of what its memory must represent, rather than inventing a taxonomy. Specifically: (2) requires bitemporality, (3) requires procedural memory, (4) requires a first-class negative/gotcha memory type, (5) requires scope-bound validity.

**INFERENCE — the honest bar:** the margin that matters is **72.5% vs 69.3% = 3.2 points** over an off-the-shelf coding agent, not 72.5% vs 48.5% over RAG. A memory system that beats RAG but not a competent agent with plain tools has not justified its existence. This is the number Fehrest must be evaluated against. See [Benchmark B-7](../10-BENCHMARK-PLAN.md).

**Reproducibility caveat:** these figures are read from the paper's own abstract/pages and are VENDOR-REPORTED for our purposes. The dataset must be obtained and the baselines re-run locally before they are used as acceptance thresholds.

---

## E-15 — AgeMem is a learned policy, not a transplantable algorithm

**Source:** web search; arXiv `2601.01885` ("Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for LLM Agents"), ACL 2026 (`2026.acl-long.981`).

**FACT (as reported):** AgeMem exposes **six memory operations as tool-based actions** — `add`, `update`, `delete` for long-term; `retrieve`, `summary`, `filter` for short-term — and lets the agent decide what to store, retrieve, update, summarise or discard. Training is three-stage: supervised warm-up on memory demonstrations, task-level RL with outcome rewards, then step-level GRPO for per-action credit assignment.

**INFERENCE — load-bearing:** AgeMem's *results* depend on a **trained policy**. Its operation vocabulary is free to adopt; its mechanism is not, because it requires RL training and a capable model at inference time. Under Fehrest's `AI OFF` mode requirement, an RL-trained memory manager cannot be the promotion mechanism.

**RECOMMENDATION:** Adopt the six-operation vocabulary as Fehrest's memory-mutation API. Reject the learned policy as the promotion decider; use deterministic rules as the floor, with model assistance as an optional accelerator. See [Memory Model §5](../05-MEMORY-MODEL.md).

---

## Open hypotheses requiring experiment before they may drive implementation

### H-1 — FTS5 + graph expansion beats dense retrieval on personal vaults
Motivated by [E-8](#e-8--graphifys-self-reported-retrieval-benchmarks) caveat 2 (graph tied dense RAG on the only prose benchmark reported). **Status:** unproven. **Falsified if** Benchmark B-3 shows dense or hybrid retrieval beating lexical+graph by more than the measurement interval on Fehrest's own corpus.

### H-2 — Extraction scales linearly in file count
Extrapolated in [E-5](#e-5--graphify-measured-extraction-throughput-preliminary). Cross-file symbol resolution may be superlinear. **Status:** unproven beyond 776 files. **Falsified if** 10K-file extraction exceeds 2× the linear projection.

### H-3 — Deterministic promotion rules capture most durable memory value
**Status:** unproven. **Falsified if** rule-only promotion recall on a labelled corpus falls below 60% of model-assisted promotion.

### H-4 — A Markdown-native canonical format is sufficient for v1 knowledge work
**Status:** unproven, and deliberately the cheapest hypothesis to test. **Falsified if** first-week dogfooding shows users routinely needing block-level transclusion or inline comments that Markdown plus a documented sidecar cannot express.

### H-5 — A single sidecar process is sufficient isolation for the extraction path
The sidecar spawns 12 worker processes ([E-5](#e-5--graphify-measured-extraction-throughput-preliminary)) and parses untrusted files. **Status:** unproven. **Falsified if** parser fuzzing yields memory-unsafe crashes reachable from vault content.

---

## Measurement environment

| Property | Value |
|---|---|
| OS | Windows 11 Home 10.0.26200 |
| Python | 3.11.15 (`uv`-managed venv) |
| Node | v22.23.1 |
| Cargo | 1.97.1 |
| Worker count reported by Graphify | 12 |
| Date | 2026-08-17 |

All timings are single-machine, cold-cache, Windows. They are **order-of-magnitude evidence for architectural shape**, not portable performance guarantees. Cross-platform re-measurement is required in [Phase 0](../15-IMPLEMENTATION-PHASES.md).
