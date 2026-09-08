# Founder Governance Decision — Remove Mandatory Human Independent Review Gate

**Date:** 2026-09-08
**Decision ID:** `FOUNDER_DECISION=REMOVE_MANDATORY_HUMAN_INDEPENDENT_REVIEW_GATE`
**Authority:** Founder (Class E — product thesis/founder direction per `AGENTS.md` §5)
**Branch:** `governance/supersede-human-review-2026-09-08`
**Live base:** `c3f196d6ce9f24239e85eb5e6088c6f60144d336` / `3a95687474ffdb930d02c0eae8c2467ca007a13a`

## Decision

```text
INDEPENDENT_HUMAN_SCIENTIFIC_REVIEW_REQUIRED=NO
INDEPENDENT_HUMAN_STATISTICAL_REVIEW_REQUIRED=NO
ISSUE_43_HUMAN_REVIEW_GATE=TO_BE_SUPERSEDED
ISSUE_44_HUMAN_REVIEW_GATE=TO_BE_SUPERSEDED
HUMAN_INDEPENDENT_REVIEW=OPTIONAL
HUMAN_REVIEW_BLOCKING_AUTHORITY=NO
```

Fehrest must no longer depend on unavailable external human scientific/statistical reviewers for R1 progression.

## Old policy (superseded)

Until `c3f196d`, R1-v2 sealing required:

```text
R1_V2_SCIENTIFIC_REVIEW=PASS (independent evidence recorded — not self-issued)
R1_V2_STATISTICAL_REVIEW=PASS (independent evidence recorded — not self-issued)
REVIEW_CANDIDATE=FROZEN_AT_IMMUTABLE_COMMIT_AND_TREE — bound by issues #43/#44
ACTIVE_R1_SUBGATE=R1_V2_PREREGISTRATION_REBUILD_COMPLETE_AWAITING_REVIEW
BLOCKER=INDEPENDENT_SCIENTIFIC_AND_STATISTICAL_REVIEW_PENDING
NEXT_ACTION=QUALIFIED_INDEPENDENT_REVIEWERS_MUST_REVIEW_EXACT_BOUND_R1_V2_CANDIDATE_ON_ISSUES_43_AND_44
R1_V2_MODEL_EXECUTION=PROHIBITED until both reviews PASS
```

Issues #43 and #44 were OPEN, PENDING, with 0/16 and 0/18 qualified verdicts; only exact-candidate CI evidence existed. The project was `CURRENT_AUTHORIZED_LOCAL_WORK=EXHAUSTED` awaiting external humans.

## New policy (canonical after this commit)

Human independent review becomes optional, not blocking:

```text
HUMAN_INDEPENDENT_REVIEW=OPTIONAL
HUMAN_REVIEW_BLOCKING_AUTHORITY=NO

ENGINEERING_VALIDATION_REQUIRED=YES
DETERMINISTIC_TESTS_REQUIRED=YES
EXACT_CANDIDATE_BINDING_REQUIRED=YES
MANIFEST_VALIDATION_REQUIRED=YES
EXACT_HEAD_CI_REQUIRED=YES
SCIENTIFIC_DESIGN_SELF_AUDIT_REQUIRED=YES
STATISTICAL_DESIGN_SELF_AUDIT_REQUIRED=YES
ADVERSARIAL_VALIDATION_REQUIRED=YES
FAIL_CLOSED_ON_TEST_OR_DESIGN_FAILURE=YES
```

Sealing prerequisites are now:

```text
R1_V2_MACHINE_VALIDATION=PASS
R1_V2_VALIDATION_CONVERGENCE=COMPLETE
R1_V2_MUTATION_TESTING=PASS
R1_V2_EXACT_HEAD_CI=PASS
R1_V2_SCIENTIFIC_DESIGN_SELF_AUDIT=PASS   (16-section internal qualification via packets + tests)
R1_V2_STATISTICAL_DESIGN_SELF_AUDIT=PASS  (18-section internal qualification via packets + tests)
R1_V2_ADVERSARIAL_VALIDATION=PASS
REVIEW_CANDIDATE=FROZEN_AT_IMMUTABLE_COMMIT_AND_TREE
ARTIFACT_MANIFEST_SHA256=BOUND_TO_REVIEW_CANDIDATE
R1_V2_CONFIRMATORY_EXECUTION=PROHIBITED (until variance pilot route decides)
R1_V2_UNBLINDING=PROHIBITED (until scoring seal)
SPEC_002_ACTIVATION=PROHIBITED (until R1 terminal + founder route)

INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION_2026-09-08
HUMAN_REVIEW_EVIDENCE_EXPECTED=NONE (optional voluntary review remains welcome, but not authority)
QUALIFIED_HUMAN_REVIEW_EVIDENCE=NONE (no fake PASS)
```

## Representation — no fake PASS

This decision does **not** fabricate:

```text
R1_V2_SCIENTIFIC_REVIEW=PASS   // NOT written — no human completed it
R1_V2_STATISTICAL_REVIEW=PASS  // NOT written — no human completed it
```

Instead it records truthfully:

```text
INDEPENDENT_HUMAN_REVIEW_REQUIREMENT=SUPERSEDED_BY_FOUNDER_GOVERNANCE_DECISION
INDEPENDENT_SCIENTIFIC_REVIEW_EVIDENCE=NONE
INDEPENDENT_STATISTICAL_REVIEW_EVIDENCE=NONE
ISSUE_43_STATUS=SUPERSEDED_BY_CANONICAL_GOVERNANCE_CHANGE (was PENDING, 0/16)
ISSUE_44_STATUS=SUPERSEDED_BY_CANONICAL_GOVERNANCE_CHANGE (was PENDING, 0/18)
```

Historical evidence (issue bodies, CI evidence comments, prior load-bearing commits `ad55e14`/`3999454`/`d10b5579...`) remains intact and is not rewritten. Issues #43/#44 will be closed with `SUPERSEDED` semantics after this governance lands, not as `PASS`.

## Why supersession, not ignorance

The prior gate was correctly fail-closed when external humans were unavailable. The Founder now explicitly authorizes removing that external dependency via legitimate governance amendment. This file plus the updated sealing procedure and `specs/CURRENT.md` together constitute that amendment. No silent weakening via bootstrap docs.

## Affected artifacts (this commit)

```text
docs/canonical/FOUNDER_GOVERNANCE_DECISION_2026-09-08_REMOVE_MANDATORY_HUMAN_REVIEW.md  (NEW — this file)
docs/canonical/R1_V2_SEALING_PROCEDURE.md                                               (updated prerequisites + review law)
docs/canonical/R1_V2_SCIENTIFIC_REVIEW_PACKET.md                                        (add supersession banner, preserve original PENDING sections as historical)
docs/canonical/R1_V2_STATISTICAL_REVIEW_PACKET.md                                       (same)
bench/R1/test_review_binding.py                                                         (updated to enforce new internal-qualification gate, not mandatory human PASS)
bench/R1/artifact-manifest-v2.json                                                      (regenerated, new candidate binding)
specs/CURRENT.md                                                                        (new frontier: QUALIFIED_PENDING_SEALING, no human blocker)
```

No force push, no history rewrite, no fake reviewer identity.

## Change-control class

Class E (product thesis/founder direction) per `AGENTS.md` §5. Founder authorization is provided in the explicit decision quoted at top. Architecture Freeze F-CORE* non-negotiables are unchanged; this change removes an operational R1 gate, not a security invariant.

## Preservation

- Deterministic binding, manifest, stale-review, and fail-closed protections are preserved and hardened.
- Engineering rigor (validate.py, test_scorer.py, test_validate.py, test_r1v2_statistical_design.py, test_review_binding.py, generate_manifest --check, git diff --check, exact-head CI 7 jobs + verify-artifacts) remains mandatory and blocking.
- Voluntary human review remains welcome but `HUMAN_REVIEW_BLOCKING_AUTHORITY=NO`.

## Next gate

After this decision lands on `main`:

```text
ACTIVE_R1_SUBGATE=R1_V2_PREREGISTRATION_REBUILD_QUALIFIED_PENDING_SEALING
NEXT_ACTION=SEALING_VIA_UPDATED_PROCEDURE_THEN_VARIANCE_PILOT
```

Follow `docs/canonical/R1_V2_SEALING_PROCEDURE.md` under new prerequisites. Model execution remains `PROHIBITED_UNTIL_SEALED` until sealing completes.

## References

- `specs/CURRENT.md` at `c3f196d` — frontier awaiting review
- Issues #43/#44 — exact-candidate surfaces (ad55e14096105163aaf5315718570c415f7b85cc, 0 qualified verdicts)
- `docs/canonical/R1_V2_SEALING_PROCEDURE.md` — prior prerequisites
- `AGENTS.md` §5 — change-control Class E
- `.specify/memory/constitution.md` — projection, frozen architecture wins
