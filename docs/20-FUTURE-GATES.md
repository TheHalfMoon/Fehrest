# T. Future Capability Gates

**Status:** DEFINED, NOT SCHEDULED
**Date:** 2026-08-17 (F1-R2)

Gates for capabilities that are **not in v1** and must not be assumed. Each exists so that a future decision is made on measured evidence rather than by accumulation — the same discipline as the [Editor Gate](18-EDITOR-GATE.md), applied to questions that are further out.

> **None of these is authorized, scheduled, or on the critical path.** The first authorized implementation remains [Phase T — Headless Rust Thesis-Proof](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice), and every gate below is downstream of the product thesis surviving [B-7a](10-BENCHMARK-PLAN.md#b-7a--early-headless-thesis-pilot) and [B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark).

**Why write them now.** F1-R2's donor addendum admitted a number of sources — Penpot, AFFiNE Edgeless, Loro, Automerge, y-octo, AppFlowy-Collab, Superset — that are only meaningful against a question. **A donor without a gate becomes an assumption**: it sits in the registry acquiring plausibility until someone treats its presence as a decision. Each gate below names the question its candidates answer, and the conditions under which the answer is *no capability at all*.

---

## 1. Gate discipline — common to all four

Every gate here inherits the rules the Editor Gate established, because they are what made that gate honest:

1. **The question comes before the candidates.** A gate that starts from a candidate list is a procurement exercise.
2. **Weights and criteria are fixed before evaluation**, and may never be adjusted after results arrive.
3. **"No candidate clears the floor" is a legitimate outcome**, and so is "the capability is not worth its cost." A gate that can only select is not a gate.
4. **Elimination conditions are independent of score** — silent data loss, canonical-format compromise, or a mandatory service each eliminate regardless of how well a candidate scores elsewhere.
5. **Constitutional constraints bind every candidate.** Canonical artifacts stay open, specified and losslessly exportable ([I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended)); derived state stays rebuildable ([I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)); the Core stays operable without the surface ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface)) and without Python ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)). A candidate that cannot satisfy these is eliminated however capable.
6. **Ponytail question 1 is asked first and asked seriously:** *does this capability need to exist?*

---

## 2. Visual/Canvas Engine Gate

**Status:** OPEN — Phase 8+. Canvas is deferred ([A §9](00-PRODUCT-THESIS.md#9-scope-commitments)) and this gate does not un-defer it.

**The question.** *If Fehrest ships a visual/canvas surface, which engine renders and edits it — and what remains canonical on disk when that engine is gone?*

The second half is the part that matters. Fehrest's position is that the **format outlives the engine** ([I-5](01-ARCHITECTURE-CONSTITUTION.md#i-5--canonical-artifacts-are-open-local-and-inspectable-amended)), so this gate scores portability of the artifact at least as heavily as capability of the tool.

**Candidates** — all `STUDY` in the registry, none adopted:

| Candidate | Registry | Brings | Principal risk to expose |
|---|---|---|---|
| **JSON Canvas** as the interchange baseline | [SRC-171](research/FEHREST_SOURCE_REGISTRY.md#148-json-canvas--visual-interchange-promotes-src-071) | An open, specified, already-adopted format | May not express richer semantics without loss |
| **Penpot** | [SRC-120](research/FEHREST_SOURCE_REGISTRY.md#src-120--penpot) | Open-standard visual document architecture; SVG/CSS/HTML/JSON interoperability; design tokens; components and variants; layout/grid/flex; plugin and API architecture; large-canvas mutation handling | A hosted collaborative application's server and runtime assumptions, which Fehrest does not share |
| **AFFiNE BlockSuite Edgeless** | [SRC-121](research/FEHREST_SOURCE_REGISTRY.md#src-121--affine--blocksuite-extended-scope-extends-src-004-src-006) | Page and canvas transitions in one substrate; proven interaction model | Monorepo extraction cost; split license; coupling depth |
| **tldraw** and **Excalidraw** | [SRC-084](research/FEHREST_SOURCE_REGISTRY.md#9-product-references) | Canvas interaction, gestures, export, shape libraries | A second canvas runtime — explicitly constrained against |
| **OpenPencil** | [SRC-180](research/FEHREST_SOURCE_REGISTRY.md#src-180--openpencil) | Identified `open-pencil/open-pencil` at `15bd0ba…` *(externally observed 2026-08-18, not verified here)* | Licence not observed — must be established before any code import. Identification is not adoption |

**What must be proven** — the visual analogue of the Editor Gate's P-1…P-6:

- **V-1 Canonical sufficiency.** Canonical files alone reconstruct the visual document with derived state deleted.
- **V-2 Open interchange.** The artifact is readable by a third party from a published specification, with no Fehrest software.
- **V-3 No silent loss.** Anything the format cannot express is **reported**, never dropped. If richer semantics need a sidecar, that sidecar carries references and metadata, never content ([D §4.4](03-CANONICAL-DATA-MODEL.md#44-the-sidecar-format)).
- **V-4 Identity stability.** Visual object identity survives edit, reload, rename and external modification, under [I-15](01-ARCHITECTURE-CONSTITUTION.md#i-15--paths-are-locations-stable-ids-are-identities).
- **V-5 No mandatory service.** The engine runs with all network interfaces down ([I-2](01-ARCHITECTURE-CONSTITUTION.md#i-2--core-functionality-requires-no-network), [I-3](01-ARCHITECTURE-CONSTITUTION.md#i-3--core-functionality-requires-no-fehrest-hosted-service)).

**Elimination, independent of score:** any candidate requiring a server, requiring an account, or producing a canonical artifact that only it can read.

**Explicitly not decided by this gate:** whether Fehrest has a canvas at all. That is a product decision, and the honest default is **no**.

---

## 3. Unified Surface Test

**Status:** OPEN HYPOTHESIS — no scheduled phase.

> **This gate exists because Fehrest already holds a position, and positions held without a test become assumptions.** [D §1](03-CANONICAL-DATA-MODEL.md#1-the-object-model-decision) adopts *"Everything is an Object; views are projections"* — and AFFiNE, AppFlowy and Anytype each pursue a related idea at much larger scope. **Do not assume the unified approach wins.**

**The question, stated so it can fail either way:**

> Does Fehrest benefit **materially** from **one shared object/block substrate** across documents, canvas and structured views — or is a **smaller composition of independent engines** easier to maintain while preserving canonical open data?

**Evidence for a shared substrate:**

| Source | What it demonstrates |
|---|---|
| **AFFiNE / BlockSuite** ([SRC-121](research/FEHREST_SOURCE_REGISTRY.md#src-121--affine--blocksuite-extended-scope-extends-src-004-src-006)) | Docs and edgeless canvas over one block model; page and canvas transitions; database and multi-view blocks; linked pages; journals |
| **AppFlowy-Collab** ([SRC-133](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates)) | A Rust collaborative substrate shared across document, database and folder/workspace types — the closest existing analogue to the Fehrest hypothesis |
| **Anytype** ([SRC-134](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates)) | Object-oriented knowledge UX at product scale |

**Evidence for independent engines:**

| Argument | Weight |
|---|---|
| Fehrest's canonical model is **files**, not blocks ([D §1](03-CANONICAL-DATA-MODEL.md#1-the-object-model-decision)) — a shared block substrate pulls toward a database-canonical design, the exact inversion [I-1](01-ARCHITECTURE-CONSTITUTION.md#i-1--user-knowledge-exists-locally-by-default) forbids | **High** |
| A shared substrate is a shared **failure mode**: one model's defect reaches every surface | High |
| The three unified products above are built by substantially larger teams than Fehrest's | High |
| Independent engines can each be replaced behind their own boundary — the pattern that already governs [every heavy donor](08-DONOR-MATRIX.md#8-aggregate-dependency-risk) | Moderate |

**What would settle it.** Not a bake-off — a **maintenance-cost observation**. The test is whether a second surface (structured views over the object model) can be built on independent engines without duplicating state semantics, and what that costs. Until Fehrest has two real surfaces the question has no data, and any answer is preference.

**The constraint that holds either way:** whatever substrate is chosen, **canonical data stays open files**, and no surface owns a state semantic ([I-16](01-ARCHITECTURE-CONSTITUTION.md#i-16--fehrest-remains-operable-without-its-user-interface), [ADR-0010](09-TECHNOLOGY-DECISIONS.md#adr-0010--core-implementation-language)).

---

## 4. Collaboration/CRDT Gate

**Status:** CONDITIONAL — fires only if collaboration or the Editor Gate independently creates the requirement ([ADR-0012](09-TECHNOLOGY-DECISIONS.md#adr-0012--crdt-adoption-is-editor-dependent)).

**The question.** *If a CRDT becomes necessary, which one — and which parts of its state are canonical?*

**The precondition, restated because it is the whole discipline:**

```
NO CRDT IS AUTHORIZED FOR THE HEADLESS THESIS-PROOF.
COLLABORATION MUST NEVER BE ADDED TO THE MVP IN ORDER TO JUSTIFY A CRDT.
```

Two ways this gate can be opened illegitimately, both now named: acquiring a collaboration requirement Fehrest does not have ([R1-09](reviews/F1-R1-RECONCILIATION.md)), and adopting a Rust-native CRDT **because it is Rust-native** rather than because it is needed ([SRC-122](research/FEHREST_SOURCE_REGISTRY.md#src-122--octobase-and-y-octo)).

**Candidate set — no automatic preference is granted to any member:**

| Candidate | Registry | Note |
|---|---|---|
| **Loro** | [SRC-130](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates) | Rust-native; text, rich text, map/list/tree; version and history inspection |
| **Automerge** | [SRC-131](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates) | F1 listed it alone; R2 makes it one of four |
| **y-octo / OctoBase** | [SRC-122](research/FEHREST_SOURCE_REGISTRY.md#src-122--octobase-and-y-octo) | Rust, thread-safe, Yjs-compatible semantics |
| **Yrs / Yjs** | [SRC-005](research/FEHREST_SOURCE_REGISTRY.md#32-yjs--conditional--editor-dependent) | Arrives with Candidate B if it wins the Editor Gate; reference otherwise |
| **AppFlowy-Collab** | [SRC-133](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates) | Substrate evidence rather than a CRDT choice |

**What must be proven:**

- **C-1** Which CRDT state is **canonical**, which is collaboration-specific, and which is transient — the question [D §7.3](03-CANONICAL-DATA-MODEL.md#73-six-separable-concerns) concern 5 leaves open and F1 wrongly assumed settled.
- **C-2** Canonical files remain sufficient with CRDT state deleted ([I-6](01-ARCHITECTURE-CONSTITUTION.md#i-6--derived-state-is-disposable-and-rebuildable)).
- **C-3** One CRDT runtime only. Two simultaneously requires a dedicated ADR proving a need neither satisfies alone.
- **C-4** No mandatory service, no account, no network requirement ([I-2](01-ARCHITECTURE-CONSTITUTION.md#i-2--core-functionality-requires-no-network), [I-7](01-ARCHITECTURE-CONSTITUTION.md#i-7--sync-is-optional)).

**Related but separate: device sync.** [iroh](research/FEHREST_SOURCE_REGISTRY.md#143-local-first-and-crdt-candidates) is `STUDY / DEFER` for a future device-to-device case. **Sync is not collaboration**, and neither implies the other. Fehrest v1 remains local and single-device capable.

---

## 5. View Engine Gate — data, analytics and structured views

**Status:** DEFERRED — no phase, no schedule. Analytics is outside v1 ([SRC-018](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval)).

**The question.** *If Fehrest gains structured views — tables, timelines, charts, dashboards — what is the boundary between canonical knowledge and its projections?*

**The principle this gate must preserve, and the reason deferral is safe:**

```
CANONICAL OBJECTS  !=  VIEWS
```

A dashboard, chart, table or timeline is a **projection over canonical or derived data** — never the canonical knowledge itself. Because a projection touches no canonical record, an analytics layer can arrive years later without a migration. That is what makes deferral cheap, and it is why the boundary matters more than the feature.

**Study sources — all deferred:**

| Source | Registry | Contributes |
|---|---|---|
| **Apache Superset** | [SRC-170](research/FEHREST_SOURCE_REGISTRY.md#src-170--apache-superset) | Separation of semantic data definitions from visual presentation; reusable metrics and dimensions; dataset abstraction; chart/view plugin organisation; dashboard composition; permission-aware analytics |
| **Microsoft Data Formulator** | [SRC-079](research/FEHREST_SOURCE_REGISTRY.md#9-product-references) | A *different* problem: agentic exploratory analysis, branching investigations, Data Threads |
| **Airtable / Teable / Baserow / NocoDB** | [SRC-076](research/FEHREST_SOURCE_REGISTRY.md#9-product-references) | One dataset, many views |
| **DuckDB** | [SRC-018](research/FEHREST_SOURCE_REGISTRY.md#4-storage-and-retrieval) | Deferred. **Not admitted to the MVP because analytics products use it** |
| **Microsoft Flint** | [SRC-181](research/FEHREST_SOURCE_REGISTRY.md#src-181--microsoft-flint) | Declarative chart specification with agent-oriented usage — a *projection description*, which is this gate's principle in miniature. `microsoft/flint-chart` at `34ef451…`, MIT *(externally observed 2026-08-18)*. **Still deferred**: identification does not open this gate |

**Hard constraints on any future analytics layer:**

```
ZERO MANDATORY SERVICES · LOCAL-FIRST · RUST-OWNED CORE
OPEN DATA · REBUILDABLE DERIVED VIEWS
```

**Explicitly forbidden as consequences of studying Superset:** a Superset runtime dependency; Python introduced because of it ([I-17](01-ARCHITECTURE-CONSTITUTION.md#i-17--fehrest-remains-usable-without-python)); Redis, Celery or server infrastructure; a mandatory database server; DuckDB in the MVP; dashboards before the thesis-proof passes; a plugin marketplace in v1.

**Opens only on** a measured user or product requirement — not a founder intuition, and not because the architecture would accommodate it.

---

## 6. What none of these gates may do

| Prohibited | Because |
|---|---|
| Change the first future build | It remains [Phase T](15-IMPLEMENTATION-PHASES.md#phase-t--headless-rust-thesis-proof-slice), headless and Rust |
| Introduce a runtime dependency by being written down | The registry is evidence, not an implementation plan ([§14](research/FEHREST_SOURCE_REGISTRY.md#14-f1-r2-final-donor-discovery-addendum)) |
| Bypass Spec Kit, Ponytail, rights review or security gates | [S](19-ENGINEERING-METHOD.md) applies to every future adoption without exception |
| Reopen broad donor discovery | `FROZEN`. New sources enter only through a documented gap trigger |
| Proceed before the product thesis has evidence | Every capability here is worthless if [B-7b](10-BENCHMARK-PLAN.md#b-7b--confirmatory-powered-benchmark) fails |
