# Editor Architecture Gate

**Status:** OPEN / PROTOTYPE-GATED
**Created:** 2026-08-17 (F1-R1, finding [R1-02](reviews/F1-R1-RECONCILIATION.md) / [R1-03](reviews/F1-R1-RECONCILIATION.md) / [R1-04](reviews/F1-R1-RECONCILIATION.md))
**Resolves:** [ADR-0002](09-TECHNOLOGY-DECISIONS.md#adr-0002--editor-architecture-open--prototype-gated)
**Executed at:** [Phase 3E](15-IMPLEMENTATION-PHASES.md#phase-3e--editor-bake-off-gate)

The editor is chosen by **executable prototype evidence**, not architectural preference. F1 closed this decision on an argument; R1 reopens it and specifies the experiment.

**No prototype is to be built yet.** This document defines the gate. Building it is Phase 3E work, after implementation authorization.

---

## 1. Why this gate exists

F1 concluded: *BlockSuite is stale, therefore CodeMirror 6.* That reasoning had two defects.

**Defect 1 — incomplete evidence.** The standalone `toeverything/blocksuite` mirror is genuinely stale (last sync 2025-07-07; `@blocksuite/store` unpublished since 2025-07-01 at `0.22.4`). But the implementation is actively developed inside `toeverything/AFFiNE` under `blocksuite/`, with feature, performance and security commits through 2026-08-10 ([E-10](research/EVIDENCE_LOG.md#e-10--blocksuite-distribution-is-stale-the-implementation-is-not-editor-gate)). The correct statement is that **the distribution path is stale, not the editor**.

**Defect 2 — an unproven impossibility claim.** F1 argued that lossless rich-editor↔Markdown round-trip requires preserving CRDT operation history, so any sidecar becomes the real canonical document. That conflates separable concerns and was never demonstrated (§4).

Neither defect proves the F1 *conclusion* wrong. Candidate A may still win. But it must win on measurement.

---

## 2. Candidates

### Candidate A — CodeMirror 6

Markdown-native text editing; the canonical bytes are the document model.

| Strengths to test | Risks to expose |
|---|---|
| Markdown-native editing; canonical file *is* the document | Rich blocks must be built or integrated separately |
| Trivial external-file compatibility | Page ↔ canvas experience not inherited |
| Mature, maintained, MIT (`@codemirror/state` 6.7.1, 2026-07-05) | Tables, databases, rich embeds may require substantial custom work |
| Low dependency weight, small install | Block-level identity has no native home |
| Round-trip fidelity likely near-perfect for plain Markdown | May under-serve non-developer knowledge work |

### Candidate B — maintained AFFiNE BlockSuite subtree

**Evaluate `toeverything/AFFiNE` → `blocksuite/…` at a pinned commit. Do not evaluate the stale standalone package.**

| Strengths to test | Risks to expose |
|---|---|
| Mature block architecture | Extraction from a 446 MB application monorepo |
| Page + Edgeless primitives (canvas for free) | Coupling to AFFiNE-specific infrastructure |
| Rich blocks, databases, data views | Dependency surface and packaging weight |
| Proven editing interaction model | Maintenance burden if we diverge from upstream |
| Potentially large implementation reuse | Canonical-file round-trip complexity (§4) |
| Security fixes land in the maintained tree | Split license — MIT outside `packages/backend` and `packages/common/native`; per-file provenance required |

### Candidate C — alternate maintained substrate

Include **only if** Candidates A and B both leave a demonstrated gap. Permitted: ProseMirror, Tiptap, Milkdown.

**No open-ended editor shopping.** A third candidate requires a written statement of the specific gap it closes, recorded before evaluation begins.

---

## 3. Common corpus

One fixture corpus, committed under `bench/editor/corpus/`, used identically by every candidate. Each file exercises named features and ships with an expected-output fixture.

**Content features:** CommonMark + GFM · YAML frontmatter · wikilinks · headings · lists · task lists · code blocks (incl. fenced with language + line numbers) · tables · callouts/admonitions · embedded local files (image, PDF, arbitrary attachment) · internal links · external links · footnotes · block quotes · horizontal rules · HTML inline and block.

**Identity features:** stable note IDs · stable block IDs where the candidate supports them.

**Internationalisation:** non-Latin text · Arabic (RTL, bidirectional runs, shaping) · CJK (no word boundaries, full-width punctuation) · **Turkish Unicode edge cases (dotted/dotless İ/ı, casefold asymmetry)** · combining marks and NFC/NFD pairs · emoji and ZWJ sequences · mixed-direction lines.

The Turkish and combining-mark cases are called out because the same normalisation hazard that produced a real upstream defect in Graphify's ID layer ([E-4](research/EVIDENCE_LOG.md#e-4--extractor-ids-are-name-derived-by-design-not-by-defect)) applies to any editor computing block identity from content.

**Scale:** a 1 MB single document · a 10,000-line document · a document with 5,000 blocks · a document with 1,000 inline links.

---

## 4. The round-trip proof obligation

F1's impossibility argument is **retracted**. It is replaced by a proof obligation neither candidate is presumed to pass or fail.

### 4.1 Six separable concerns

The F1 argument collapsed these. They must be evaluated independently:

| # | Concern | Must it be canonical? |
|---|---|---|
| 1 | **Semantic document content** | **Yes** — this is the user's knowledge |
| 2 | **Structured metadata** (properties, types) | **Yes** |
| 3 | **Stable block identity** | **Yes, where block-level references exist** |
| 4 | **Provenance and comments** | **Yes** |
| 5 | **Collaboration history (CRDT ops)** | **Not established.** Likely collaboration machinery, not document meaning |
| 6 | **Transient editor runtime state** (selection, presence, undo stack) | **No** |

F1 treated (5) as canonical and derived an impossibility from it. That premise was never demonstrated. A CRDT's operation log is how concurrent edits converge; it is not obviously part of what a document *means*, any more than a git object database is part of what a source file means.

### 4.2 Candidate architecture to test — NOT adopted

```
note.md
    canonical human-readable content            (concerns 1, 2)

note.fehrest.json
    canonical structured metadata, only when needed:
      - stable block IDs                        (concern 3)
      - provenance, comments                    (concern 4)
      - metadata for rich objects Markdown cannot express

Y.Doc / CRDT state
    transient or collaboration-specific
    unless independently proven canonical       (concern 5)
```

**This design is a hypothesis to test, not a decision.** It is recorded so the gate has something concrete to falsify.

### 4.3 What must be proven

Each candidate must demonstrate, with a running prototype:

- **P-1 Fidelity.** Corpus → editor → edit → serialise → reload produces content equal to expectation, with every deviation enumerated. No silent loss.
- **P-2 Loss disclosure.** Anything the candidate cannot represent in canonical form is *reported*, not dropped. A candidate that loses data silently fails outright regardless of score.
- **P-3 Identity stability.** Note and block IDs survive edit, reload, rename, move, and external modification.
- **P-4 External-edit tolerance.** A file edited by another tool (or `git checkout`) reloads correctly; unresolvable anchors are surfaced as orphaned, never discarded.
- **P-5 Canonical sufficiency.** With derived state deleted, the canonical files alone reconstruct the document — consistent with [I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable).
- **P-6 Sidecar boundedness.** If a sidecar is used, it contains **no content** — only references into content plus metadata. Deleting it must lose annotations, never the document.

P-6 is the discriminator that decides whether F1's fear was justified. If a candidate's sidecar must carry content or operation history to round-trip, then that sidecar is the real document and the concern was real. If it need not, F1 was wrong and Candidate B's path is open.

---

## 5. Acceptance suite

Executed identically against every candidate. Each is pass/fail with recorded detail.

| # | Test | Applies to |
|---|---|---|
| 1 | CommonMark/GFM fidelity across the corpus | All |
| 2 | YAML frontmatter preserved verbatim, **including unknown fields** ([R-8](01-ARCHITECTURE-CONSTITUTION.md#2-derived-rules)) | All |
| 3 | Wikilinks preserved and resolvable | All |
| 4 | Stable note IDs survive edit/reload | All |
| 5 | Stable block IDs survive edit/reload | Where supported |
| 6 | Headings, lists, task lists, code blocks, tables round-trip | All |
| 7 | Callouts/admonitions round-trip | All |
| 8 | Embedded local files survive | All |
| 9 | Internal + external links survive | All |
| 10 | Non-Latin, Arabic (RTL/bidi), CJK render and round-trip | All |
| 11 | **Turkish Unicode + combining marks are idempotent** under any ID/normalisation the candidate performs | All |
| 12 | Large-document load, edit and save within budget | All |
| 13 | External file edit detected and reloaded | All |
| 14 | Rename / move preserves identity and links | All |
| 15 | **Crash during save loses no committed content** (fault injection) | All |
| 16 | Reload fidelity: byte-equality where expected, enumerated deviation otherwise | All |
| 17 | Agent-generated edits (programmatic write) round-trip | All |
| 18 | **Git diff readability** — a one-word change produces a minimal, reviewable diff | All |
| 19 | Comments anchored and re-anchored after edit | Rich candidates |
| 20 | Block references resolve after edit | Rich candidates |
| 21 | Database / data-view blocks round-trip | Rich candidates |
| 22 | Page ↔ canvas transition preserves content | Rich candidates |
| 23 | Embedded structured objects round-trip | Rich candidates |
| 24 | Sidecar deletion loses annotations only, never document content (P-6) | Rich candidates |

**Test 18 deserves emphasis.** A canonical format whose every edit produces an unreadable diff is not meaningfully open, whatever its specification says. This is a direct test of [I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended) in practice.

**Test 15 is a hard gate.** Any candidate that loses committed content on crash is eliminated, whatever it scores.

---

## 6. Scoring

| Criterion | Weight | Measured by |
|---|---|---|
| Canonical / open-file fidelity | **30%** | Tests 1–11, 16, 18; P-1, P-2, P-5, P-6 |
| Maintenance burden | **20%** | Upstream release cadence, extraction/vendoring cost, divergence risk, per-file license provenance, update path |
| Rich editing capability | **15%** | Tests 19–23; capability inventory vs [v1 wedge](00-PRODUCT-THESIS.md#4-the-v1-user-wedge) needs |
| Performance | **10%** | Test 12; load/edit/save latency at corpus scale |
| Binary / install size | **10%** | Measured bundle delta |
| Security surface | **5%** | Dependency count, advisory exposure, sandbox implications |
| Agent editability | **5%** | Test 17; ease of correct programmatic edit |
| Future canvas integration | **5%** | Test 22; cost to reach [Phase 8](15-IMPLEMENTATION-PHASES.md#phase-8--deferred) canvas |

**Weights are fixed before evaluation and may be changed only with written reasoning recorded in this document — never after seeing results.**

Fidelity dominates at 30% because it is the criterion the constitution makes non-negotiable. Maintenance is second at 20% because it is where F1's analysis was strongest and remains a genuine differentiator: vendoring from an active monorepo and depending on an unreleased package are different risks, and the gate must price both.

**Elimination conditions**, independent of score: silent data loss (P-2), content loss on crash (test 15), or a sidecar that must carry document content (P-6).

---

## 7. Output

The gate produces an **ADR**, not a preference. It must record: per-candidate scores with raw measurements; every enumerated fidelity deviation; the P-1…P-6 verdicts; elimination conditions triggered; the decision with reversal conditions; and the consequent status of [ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent) (CRDT/Yjs), which is editor-dependent ([R1-09](reviews/F1-R1-RECONCILIATION.md)).

An inconclusive result is a legitimate outcome. If no candidate clears the fidelity floor, the correct action is to report that and reconsider scope — not to pick a winner on aggregate score.

---

## 8. What this gate does not decide

- **Whether Fehrest has a canvas.** Canvas remains [Phase 8](15-IMPLEMENTATION-PHASES.md#phase-8--deferred). Candidate B inheriting Edgeless primitives is scored as future value, not a v1 feature.
- **Whether collaboration is in scope.** It is not. Collaboration must never be added to justify a CRDT ([R1-09](reviews/F1-R1-RECONCILIATION.md)).
- **The desktop shell.** [ADR-0011](09-TECHNOLOGY-DECISIONS.md#adr-0011--desktop-shell) is separate, though partly editor-dependent.
- **Whether Fehrest is a Markdown editor.** It is not, under any outcome. The editor is one surface over the [four-layer architecture](00-PRODUCT-THESIS.md#5-the-four-layer-architecture); the memory, graph, event and context layers are the product.
