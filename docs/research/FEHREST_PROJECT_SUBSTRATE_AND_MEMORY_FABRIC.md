# Fehrest Project Substrate and Memory Fabric

**Status:** NON-AUTHORIZING PRODUCT / ARCHITECTURE DIRECTION  
**Date:** 2026-09-02  
**Authority:** founder strategic direction captured for planning only. Implementation remains gated by `specs/CURRENT.md`, canonical execution order, active specifications, evidence gates, security review, and required exact-head review.

> This document does not authorize any current product implementation while R1 remains open.

```text
ACTIVE_EXECUTION_FRONTIER=R1
R1_SEMANTICS_CHANGED=NO
PRODUCT_BEHAVIOR_CHANGED=NO
GIT_IMPORT_IMPLEMENTATION_AUTHORIZED=NO
GIT_EXPORT_IMPLEMENTATION_AUTHORIZED=NO
GITHUB_SYNC_IMPLEMENTATION_AUTHORIZED=NO
HOSTED_STORAGE_IMPLEMENTATION_AUTHORIZED=NO
UI_IMPLEMENTATION_AUTHORIZED=NO
```

---

## 1. Strategic expansion

Fehrest should become two things at once, through one coherent core:

1. **The best durable brain a human or AI agent can use.**
2. **A portable project substrate that can ingest a project from GitHub, preserve and enrich it inside Fehrest without requiring a GitHub fork, and later publish selected changes back to GitHub or another Git remote.**

The target experience is:

```text
GitHub repository / URL / project source
        ↓
Import into Fehrest
        ↓
Project becomes a durable Fehrest Project Capsule
        ↓
Humans + agents work with complete project continuity
        ↓
Knowledge / decisions / work / memory / evidence accumulate
        ↓
Selected code/history can be exported or published to GitHub
```

Fehrest is therefore not merely a Git client, Git host, note system, memory service, or workspace.

The long-term category claim is:

> **Fehrest is the durable project brain and portable work substrate between repositories, humans, agents, IDEs, CLIs, and model providers.**

---

## 2. GitHub is a publication and collaboration surface, not the only home of a project

A GitHub repository is excellent at storing Git objects and coordinating software development, but a long-lived project contains materially more state than Git alone normally captures:

```text
code
history
issues
pull requests
reviews
decisions
research
constraints
procedures
known failures
agent trajectories
context packages
execution receipts
artifacts
project memory
work state
conversations
external evidence
```

Fehrest should be able to preserve these layers together without requiring the user to create a GitHub fork merely to explore, modify, learn from, or extend another public project.

### 2.1 The no-fork workflow

Target workflow:

```text
fehrest import https://github.com/owner/project
```

Conceptually, this creates a local Fehrest Project Capsule containing an exact imported Git object boundary plus Fehrest-owned semantic state.

The user can then:

```text
study
branch locally
run agents
record decisions
create work items
attach evidence
build memory
create patches
compare against upstream
track upstream movement
```

without creating a GitHub fork.

When the user decides to publish:

```text
Fehrest Project Capsule
        ↓ explicit export/publish intent
Git repository / bundle / patch / new GitHub repository / branch / PR
```

A remote fork may still be created later when GitHub collaboration semantics require it, but it is not the prerequisite for local project ownership inside Fehrest.

---

## 3. Project Capsule: the core portability primitive

The mature system should define an open, versioned `ProjectCapsule` format or equivalent specification.

A capsule is not one giant archive that hides semantics. It is a portable project root with independently inspectable layers.

Conceptual structure:

```text
ProjectCapsule
├── identity/
├── repository/
├── knowledge/
├── work/
├── decisions/
├── memory/
├── evidence/
├── trajectories/
├── receipts/
├── artifacts/
├── provenance/
├── policies/
└── derived/
```

The exact physical layout is future specification work.

### 3.1 Required capsule properties

```text
OPEN_SPECIFICATION=YES
LOCAL_FIRST=YES
OFFLINE_READABLE=YES
PORTABLE=YES
EXPORTABLE_WITHOUT_FEHREST_SERVICE=YES
CANONICAL_AND_DERIVED_SEPARATED=YES
SOURCE_PROVENANCE_PRESERVED=YES
GIT_OBJECT_IDENTITY_PRESERVED_WHERE_IMPORTED=YES
DERIVED_STATE_REBUILDABLE=YES
```

A user must be able to leave Fehrest while retaining the canonical project data and sufficient metadata to interpret it.

---

## 4. Three separate concepts must never be collapsed

The architecture must distinguish:

### 4.1 Git object storage

Exact repository objects and history:

```text
commits
trees
blobs
tags
refs
```

Git semantics remain Git semantics.

### 4.2 Repository working state

Mutable work derived from Git:

```text
branches
worktrees
patches
staged changes
uncommitted files
upstream tracking
```

### 4.3 Fehrest semantic project state

Project meaning that Git cannot represent adequately on its own:

```text
active decisions
supersession
constraints
project memory
agent context
work graph
execution evidence
review evidence
agent identities
capability history
research evidence
conversations
```

Hard rule:

```text
GIT_HISTORY != FEHREST_PROJECT_MEMORY
```

and:

```text
FEHREST_SEMANTIC_STATE_MUST_NOT_CORRUPT_GIT_OBJECT_IDENTITY
```

---

## 5. Source identity and upstream provenance

Every imported project must retain immutable source provenance.

Conceptual `RepositorySource` fields:

```text
source_id
source_kind
original_url
host
owner
repository_name
imported_ref
imported_commit
object_identity_root
imported_at
license_snapshot_ref
notice_snapshot_ref
upstream_tracking_policy
```

For GitHub imports, Fehrest should know the difference between:

```text
origin source
current upstream state
local Fehrest work
published derivative
```

The user must always be able to answer:

```text
Where did this project come from?
Which exact upstream revision did I start from?
What changed locally?
What changes came from upstream later?
What did my agents change?
What have I published back?
```

---

## 6. Storage without becoming a GitHub clone

Fehrest may eventually store Git objects locally and optionally replicate them, but its product goal is not to recreate every GitHub hosting feature.

The core value is:

```text
Git object portability
+ project continuity
+ semantic memory
+ agent context
+ governed action
+ evidence
```

A future hosted Fehrest service may accelerate backup, collaboration, remote agents, or cross-device access, but:

```text
HOSTED_FEHREST != CANONICAL_REQUIREMENT
```

The local capsule remains complete enough to preserve the project brain.

---

## 7. Import modes

Future import architecture should support explicit modes rather than one ambiguous copy operation.

Conceptual modes:

```text
SNAPSHOT_IMPORT
MIRROR_IMPORT
TRACKED_UPSTREAM_IMPORT
SELECTIVE_SUBTREE_IMPORT
PATCH_IMPORT
BUNDLE_IMPORT
LOCAL_DIRECTORY_IMPORT
```

### Snapshot import

Preserve one exact source revision and stop.

### Mirror import

Preserve repository object history locally.

### Tracked upstream import

Keep a declared upstream relationship and periodically allow explicit reconciliation.

No upstream change silently mutates canonical Fehrest semantic state.

---

## 8. Publish and export modes

Publishing must also be explicit.

Conceptual outputs:

```text
Git repository
Git bundle
patch series
commit series
branch
new GitHub repository
GitHub pull request
archive
Fehrest capsule
semantic export
```

Hard rule:

```text
IMPORT_DOES_NOT_IMPLY_PUBLISH_AUTHORITY
```

and:

```text
PUBLISH_TARGET != CANONICAL_PROJECT_OWNER
```

A GitHub remote is a destination and collaboration surface, not the sole owner of project truth.

---

## 9. The Brain: no practical forgetting without false promises

The founder target is that Fehrest becomes the best brain available to humans and agents and that agents can recover complete relevant project context in seconds.

An absolute promise that a system will "never forget" is not technically honest. Hardware can fail, users can delete data, retention policy can remove detail, encryption keys can be lost, and source evidence can disappear.

Fehrest should instead make stronger, testable guarantees:

```text
NO_SILENT_FORGETTING_OF_CANONICAL_STATE=YES
EXPLICIT_RETENTION_POLICY=YES
PROVENANCE_PRESERVED=YES
SUPERSESSION_PRESERVED=YES
LOSS_IS_DETECTABLE=YES
UNRECONSTRUCTABLE_IS_REPORTED_HONESTLY=YES
BACKUP_AND_EXPORT_ARE_FIRST_CLASS=YES
```

The user experience target remains:

> **If Fehrest was entrusted with durable project state and that state remains within declared retention/recovery guarantees, any authorized human or agent should be able to recover the right project context quickly without depending on the original conversation or agent.**

---

## 10. Seconds-to-context is a product SLO, not a slogan

"An agent gets the whole context in seconds" must be specified carefully.

The system should not dump the entire historical corpus into every model. It should compile the complete **relevant working context** required for the current task, with drill-down access to the full authorized project history.

Define future measurable SLO classes such as:

```text
PROJECT_ORIENTATION_P50
PROJECT_ORIENTATION_P95
TASK_CONTEXT_COMPILE_P50
TASK_CONTEXT_COMPILE_P95
FIRST_USEFUL_CONTEXT_LATENCY
CONTEXT_TOKEN_BUDGET
CONTEXT_RECALL_AT_BUDGET
CONSTRAINT_MISS_RATE
STALE_STATE_RATE
PROVENANCE_COMPLETENESS
```

Candidate experience objective for future benchmark design:

```text
OPEN_PROJECT
→ useful orientation in <= 1 second on warm local state
→ bounded task context in <= 2 seconds on warm local state
→ deeper evidence drill-down available immediately after
```

These are planning targets, not current claims, and must be qualified on realistic project sizes and hardware before becoming commitments.

---

## 11. Two-level memory access

To achieve fast orientation without losing depth, Fehrest should separate:

### Working Continuity Layer

Small, current, high-value state:

```text
project identity
current goals
active constraints
active decisions
open blockers
active work
known gotchas
recent meaningful changes
critical procedures
```

### Deep Project Memory

The full authorized durable history:

```text
superseded decisions
past failures
old trajectories
archived work
historical conversations
prior experiments
source revisions
execution evidence
long-tail knowledge
```

The working continuity layer is derived from canonical state and reproducible. It is not a second authority.

```text
FAST_CONTEXT != LOSSY_CANONICAL_REWRITE
```

---

## 12. IDE and CLI independence

Fehrest must remain useful when the user changes tools.

The same project brain should be consumable from:

```text
Codex CLI
Claude Code
Hermes
OpenCode
VS Code-compatible environments
JetBrains
Zed
terminal tools
custom agents
future IDEs
future model providers
```

The integration contract should be protocol-first and provider-neutral where possible.

Potential surfaces:

```text
Fehrest CLI
MCP
ACP adapters
local HTTP/IPC API
SDKs
filesystem projections
context capsule export
```

No IDE gets exclusive semantics.

```text
IDE != MEMORY OWNER
MODEL_PROVIDER != MEMORY OWNER
AGENT_RUNTIME != MEMORY OWNER
```

---

## 13. Universal project addressability

A mature Fehrest should let users refer to project entities across tools by stable identity, not path alone.

Examples:

```text
fehrest://project/<id>
fehrest://object/<id>
fehrest://decision/<id>
fehrest://work/<id>
fehrest://execution/<id>
```

The URI shape is illustrative, not authorized.

The strategic requirement is stable cross-tool identity.

A file may move. A repository may be renamed. A GitHub organization may change. The Fehrest project identity must survive those location changes.

---

## 14. Upstream reconciliation without fork dependence

Tracked projects need a first-class upstream reconciliation model.

Future operation concept:

```text
fehrest upstream fetch
fehrest upstream compare
fehrest upstream reconcile
```

The reconciliation view should distinguish:

```text
upstream Git changes
local Git changes
Fehrest semantic changes affected by upstream
stale decisions
invalidated procedures
changed dependencies
new security/release information
```

This is more powerful than `git pull` because code movement may invalidate project memory.

Example:

```text
upstream removes framework X
        ↓
Fehrest detects references to X in active procedures/decisions
        ↓
marks them for review
        ↓
does not silently rewrite canonical memory
```

This is a major Fehrest-native advantage.

---

## 15. Memory invalidation is as important as memory retrieval

A brain that remembers stale facts perfectly is dangerous.

Fehrest must optimize not just for remembering but for knowing when a memory may no longer be valid.

Triggers may include:

```text
source file changed
upstream commit moved
package version changed
issue closed/reopened
new contradictory evidence
decision superseded
test failed
review rejected assumption
environment changed
```

The system should connect durable memory to the evidence that supports it so changes can create explicit revalidation work.

Target principle:

```text
MEMORY_WITHOUT_INVALIDATION_PATH_IS_INCOMPLETE
```

---

## 16. Human memory and AI memory share a substrate, not an interface

Fehrest should be useful as a human brain even when no agent is active.

For humans:

```text
remember decisions
find why something happened
recover abandoned work
see relationships
resume after months
understand external projects
preserve research
```

For agents:

```text
compile bounded context
retrieve deep evidence
receive active constraints
understand work state
operate under grants
record evidence
propose durable learning
```

The canonical substrate can be shared while the presentation and context compilation are role-specific.

---

## 17. Knowledge ingestion beyond GitHub

GitHub is strategically important but not sufficient.

A project brain may need:

```text
Git repositories
local folders
PDFs
papers
web sources
documentation
Slack exports
Notion exports
issue trackers
email evidence
meeting notes
datasets
artifacts
terminal logs
benchmark outputs
```

Every importer must preserve source provenance and treat imported content as evidence, not authority.

This creates a broader long-term concept:

> **Anything relevant to a project can enter Fehrest, become addressable evidence, and contribute to context without silently becoming truth.**

---

## 18. Distribution strategy: Fehrest follows the project

If Fehrest aims to become one of the most-used developer/knowledge tools, adoption cannot require replacing GitHub, the IDE, or the CLI on day one.

The distribution model should be additive:

```text
keep GitHub
keep your IDE
keep your CLI agent
add Fehrest
```

Immediate value should come from continuity and context portability.

The user should not have to migrate their entire workflow to receive benefit.

Long-term, Fehrest may become the primary workspace because it earns that role, not because it demands it.

---

## 19. The Fehrest adoption flywheel

Target flywheel:

```text
Import any project
        ↓
Instant orientation
        ↓
Agent/human does useful work
        ↓
Fehrest preserves durable learning + evidence
        ↓
Next session starts smarter
        ↓
Switch IDE/model without losing project brain
        ↓
Project becomes more valuable inside Fehrest over time
        ↓
Publish to GitHub when needed
```

This creates compounding value that ordinary repository storage does not provide.

The moat is not lock-in. The moat is accumulated, portable, provenance-linked project understanding.

---

## 20. Anti-lock-in requirement

The better Fehrest becomes as a brain, the more dangerous proprietary lock-in would become.

Therefore:

```text
THE_MORE_IMPORTANT_THE_STATE, THE_STRONGER_THE_EXPORT_GUARANTEE
```

Critical semantic state must have documented export forms.

At minimum, future export must preserve meanings for:

```text
identity
decisions
supersession
memory status
work state
provenance
evidence links
agent/session identity
execution receipts
source relationships
```

A plain Markdown dump that destroys those relationships is not sufficient semantic export.

---

## 21. Integrity and disaster recovery

If Fehrest becomes a project brain, recovery is product functionality.

Future requirements should include:

```text
content-addressed integrity checks
canonical inventory
backup verification
restore drills
corruption detection
partial-loss reporting
export verification
optional redundant storage
portable recovery bundle
```

The system must distinguish:

```text
NOT_FOUND
DELETED_BY_POLICY
CORRUPTED
SOURCE_UNAVAILABLE
UNRECONSTRUCTABLE
```

It must never report remembered state as intact when underlying evidence is missing.

---

## 22. Performance architecture for very large project brains

"Whole project context in seconds" requires deliberate indexing and tiering.

Future architecture should assume projects with:

```text
millions of files/objects
multi-year history
large issue/review archives
many agent trajectories
large evidence stores
multiple repositories
```

The fast path must not scan all history.

Expected design pattern:

```text
canonical durable state
        ↓
deterministic incremental projections
        ↓
working continuity index
        ↓
query/context compiler
        ↓
provenance-linked deep retrieval on demand
```

Derived indexes may use FTS, graph, vectors, summaries, caches, or other accelerators only when rebuildable and benchmark-retained.

---

## 23. Project federation

Many real projects span multiple repositories.

Fehrest should eventually support a higher-level project identity containing:

```text
multiple Git repositories
services
packages
docs
infrastructure
research
work items
shared decisions
```

A Fehrest `Project` must therefore not be equivalent to one Git repository.

```text
PROJECT != REPOSITORY
```

A repository is one source/container associated with a project.

This is essential for becoming more important than a Git forge boundary.

---

## 24. GitHub interoperability principles

Future GitHub integration should obey:

```text
GITHUB_IS_FIRST_CLASS=YES
GITHUB_IS_EXCLUSIVE=NO
FORK_REQUIRED_FOR_IMPORT=NO
SOURCE_PROVENANCE_REQUIRED=YES
UPSTREAM_RELATIONSHIP_PRESERVED=YES
PUBLISH_IS_EXPLICIT=YES
PUSH_REQUIRES_AUTHORITY=YES
PR_CREATION_REQUIRES_AUTHORITY=YES
REMOTE_FAILURE_DOES_NOT_CORRUPT_LOCAL_CANONICAL_STATE=YES
```

Fehrest should support GitHub extremely well while remaining compatible with GitLab, Forgejo, Gitea, local remotes, and future hosts.

---

## 25. Product metrics for the brain/substrate vision

Usage count alone cannot prove product quality.

The product should track or benchmark metrics such as:

```text
Time to first useful orientation
Fresh-agent continuation success
Constraint miss rate
Stale-memory error rate
Context compile latency
Context token efficiency
Provenance completeness
Task closeout evidence completeness
Human interruption rate per successful agent task
Cross-runtime continuation success
Upstream reconciliation correctness
Export fidelity
Recovery success
Import-to-first-value time
```

North-star outcome metric candidate:

> **How often can a fresh authorized human or agent continue a real long-lived project correctly, quickly, and with less reconstruction work because Fehrest exists?**

---

## 26. Strategic product laws added by this direction

```text
PROJECT != REPOSITORY
REPOSITORY != PROJECT_BRAIN
GIT_HISTORY != PROJECT_MEMORY
IMPORT != FORK
IMPORT != PUBLISH_AUTHORITY
REMOTE != CANONICAL_OWNER
FAST_CONTEXT != FULL_HISTORY_DUMP
MEMORY != UNCHECKED_SUMMARY
REMEMBERING != VALIDITY
IDE != MEMORY_OWNER
AGENT_RUNTIME != MEMORY_OWNER
MODEL_PROVIDER != MEMORY_OWNER
HOSTED_SERVICE != REQUIRED_CANONICAL_AUTHORITY
```

---

## 27. Future architecture gates created by this direction

Before implementation, future specifications should explicitly gate:

```text
P-01 Project Capsule open format
P-02 Git object import integrity
P-03 source/upstream provenance model
P-04 no-fork tracked import semantics
P-05 explicit publish/export authority
P-06 semantic export fidelity
P-07 project federation across repositories
P-08 upstream reconciliation + memory invalidation
P-09 working continuity layer correctness
P-10 seconds-to-context benchmark/SLO qualification
P-11 disaster recovery and corruption tests
P-12 cross-IDE/CLI context portability
P-13 cross-agent continuation benchmark
P-14 massive-project performance benchmark
P-15 GitHub adapter qualification
P-16 non-GitHub Git remote qualification
```

These are planning gates, not current tasks and not current implementation authority.

---

## 28. Final target

Fehrest should make this workflow ordinary:

```text
I find any useful project on GitHub.
I import it into Fehrest without forking.
Fehrest understands exactly where it came from.
I ask an agent to work on it from any IDE or CLI.
The agent receives the right current context in seconds.
Every important action is bounded and auditable.
Every durable lesson survives the agent session.
Upstream changes can be reconciled without erasing what my project learned.
Months later, a completely different agent can continue correctly.
When I want to publish, I can ship code back to GitHub explicitly.
If I leave Fehrest, my project and its semantic history remain mine.
```

The long-term ambition is not merely to be used beside GitHub.

It is to become the place where a project's durable understanding lives while GitHub, IDEs, CLIs, agents, and model providers remain replaceable interfaces around that understanding.

> **GitHub can host the repository. Fehrest should remember the project.**
