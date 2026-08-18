//! Deterministic temporal resolution and supersession-graph validation.
//!
//! **The normative resolver (F §4.2).** Five rungs, each comparing exactly one
//! well-founded axis. Where a rung carries no information it is *skipped*, not
//! guessed. The ladder terminates in `Contradiction` — **never in a number**.
//!
//! F1's sixth rung was "higher confidence", which meant an uncalibrated float
//! produced by a language model decided what Fehrest reported as true whenever the
//! principled rules ran out. That rung does not exist here, and
//! `test_confidence_cannot_change_outcome` asserts its absence behaviourally.

use crate::memory::{Basis, Lifecycle, Memory, Resolution, Scope, Verification};
use crate::{Error, Result};
use std::collections::{HashMap, HashSet};

/// The result of resolving current (or historical) state.
#[derive(Debug, Clone, PartialEq)]
pub enum ResolveOutcome {
    /// Exactly one candidate, or one that strictly dominates.
    ///
    /// Boxed to keep the enum small: `Memory` is ~240 bytes and `NoAnswer` is the
    /// common result, so an unboxed variant would make every abstention pay for a
    /// payload it does not carry.
    Answer(Box<Memory>),
    /// Candidates exist but none dominates. Surfaced, never silently resolved.
    Contradiction(Vec<Memory>),
    /// No candidate. Abstention is a correct answer, not a failure.
    NoAnswer,
}

fn verification_rank(v: Verification) -> u8 {
    match v {
        Verification::UserConfirmed => 3,
        Verification::Corroborated => 2,
        Verification::Unverified => 1,
    }
}

/// Rung 2 ordering, with the reasoning that fixes it.
///
/// `UserAsserted` outranks `Extracted` because authority originates with the user
/// and only the user — a user correcting Fehrest's parse must win. `Extracted`
/// outranks `AgentAsserted` because Fehrest parsing a primary source is
/// mechanically checkable while an agent's claim to have done so is not; that is
/// the T-2 boundary expressed as an ordering.
fn basis_rank(b: Basis) -> u8 {
    match b {
        Basis::UserAsserted => 4,
        Basis::Extracted => 3,
        Basis::AgentAsserted => 2,
        Basis::Inferred => 1,
    }
}

/// Is this memory admissible as an answer **at `as_of_valid`**?
///
/// Deliberately NOT `Memory::is_authoritative`, which answers a different
/// question: *is this in force now*. Historical resolution needs *was this in
/// force then*, and collapsing the two makes AS-2 structurally unanswerable --
/// every superseded record would be invisible at every point in time, including
/// the interval it actually governed.
///
/// The rule that keeps K-10 intact while making history reachable:
///
/// | lifecycle | admissible |
/// |---|---|
/// | `Active` | yes, subject to the valid-time window |
/// | `Pending` | never -- not authoritative at any point in valid time |
/// | `Retracted` | never -- a retraction says the claim was never true, which is exactly what separates it from `Superseded` |
/// | `Superseded` / `Expired` | **only if `valid_until` is recorded.** That field says *when* it stopped being in force, and the window below then admits it for the interval it governed. Without it we do not know when it stopped, and inventing an interval would be a fabrication -- so it is excluded everywhere |
fn admissible_at(m: &Memory, as_of_valid: i64) -> bool {
    if m.resolution == Resolution::Unresolved {
        return false;
    }
    let lifecycle_permits = match m.lifecycle {
        Lifecycle::Active => true,
        Lifecycle::Pending | Lifecycle::Retracted => false,
        Lifecycle::Superseded | Lifecycle::Expired => m.valid_until.is_some(),
    };
    // Valid-time window, half-open: `[valid_from, valid_until)`. Keeping it here
    // rather than at the call site means there is exactly one place where a record
    // can be admitted, so a future rung cannot quietly bypass it.
    lifecycle_permits
        && m.valid_from <= as_of_valid
        && m.valid_until.is_none_or(|u| u > as_of_valid)
}

/// Resolve state for a subject/predicate within a scope, at a point in valid time.
///
/// `as_of_valid` selects historical vs current truth. `as_of_recorded` bounds what
/// the system had learned by then — the two axes answer genuinely different
/// questions and are never collapsed.
pub fn resolve(
    memories: &[Memory],
    subject: &str,
    predicate: &str,
    request_scope: &Scope,
    as_of_valid: i64,
    as_of_recorded: u64,
) -> ResolveOutcome {
    // ---- ADMISSION -------------------------------------------------------
    let mut candidates: Vec<&Memory> = memories
        .iter()
        .filter(|m| m.subject.as_deref() == Some(subject))
        .filter(|m| m.predicate.as_deref() == Some(predicate))
        .filter(|m| m.scope.matches(request_scope))
        // PENDING, RETRACTED and UNRESOLVED are excluded here, and SUPERSEDED /
        // EXPIRED are admitted only for the interval they actually governed. This
        // is the single enforcement point for R-12 on the resolver path.
        .filter(|m| admissible_at(m, as_of_valid))
        .filter(|m| m.recorded_seq <= as_of_recorded)
        .collect();

    if candidates.is_empty() {
        return ResolveOutcome::NoAnswer;
    }
    if candidates.len() == 1 {
        return ResolveOutcome::Answer(Box::new(candidates[0].clone()));
    }

    // ---- DETERMINISTIC EVIDENCE LADDER -----------------------------------
    // Rung 1: verification.
    if let Some(w) = dominant(&candidates, |m| verification_rank(m.verification)) {
        return ResolveOutcome::Answer(Box::new(w.clone()));
    }
    // Rung 2: basis.
    if let Some(w) = dominant(&candidates, |m| basis_rank(m.basis)) {
        return ResolveOutcome::Answer(Box::new(w.clone()));
    }
    // Rung 3: scope specificity — SKIPPED where scopes are incomparable.
    if let Some(w) = dominant_by_specificity(&candidates) {
        return ResolveOutcome::Answer(Box::new(w.clone()));
    }
    // Rung 4: later valid_from.
    if let Some(w) = dominant(&candidates, |m| m.valid_from) {
        return ResolveOutcome::Answer(Box::new(w.clone()));
    }
    // Rung 5: later recorded_seq.
    if let Some(w) = dominant(&candidates, |m| m.recorded_seq) {
        return ResolveOutcome::Answer(Box::new(w.clone()));
    }

    // Nothing separated them. There is no rung 6.
    candidates.sort_by_key(|m| m.recorded_seq);
    ResolveOutcome::Contradiction(candidates.into_iter().cloned().collect())
}

/// Return the unique maximum by `key`, or `None` if the top is tied.
fn dominant<'a, K: Ord, F: Fn(&Memory) -> K>(
    candidates: &[&'a Memory],
    key: F,
) -> Option<&'a Memory> {
    let mut best: Option<(&Memory, K)> = None;
    let mut tied = false;
    for m in candidates {
        let k = key(m);
        match &best {
            None => best = Some((m, k)),
            Some((_, bk)) => match k.cmp(bk) {
                std::cmp::Ordering::Greater => {
                    best = Some((m, k));
                    tied = false;
                }
                std::cmp::Ordering::Equal => tied = true,
                std::cmp::Ordering::Less => {}
            },
        }
    }
    if tied {
        None
    } else {
        best.map(|(m, _)| m)
    }
}

/// Specificity domination over a **partial** order.
///
/// A winner requires being strictly more specific than *every* other candidate.
/// If any pair is incomparable, there is no winner and the rung yields nothing —
/// which is the honest outcome, not a defect.
fn dominant_by_specificity<'a>(candidates: &[&'a Memory]) -> Option<&'a Memory> {
    for &m in candidates {
        let dominates_all = candidates.iter().all(|&o| {
            std::ptr::eq(m, o)
                || matches!(
                    m.scope.specificity_cmp(&o.scope),
                    Some(std::cmp::Ordering::Greater)
                )
        });
        if dominates_all {
            return Some(m);
        }
    }
    None
}

/// Validate a proposed supersession edge.
///
/// Five invalid classes, each rejected as `InvalidSupersession` and **never
/// silently normalised** (F §6.1). Dropping a cycle edge to make the graph
/// traversable produces a plausible current state derived from an invalid history
/// — worse than an error, because nothing downstream can tell.
pub fn validate_supersession(
    memories: &HashMap<String, Memory>,
    superseding_id: &str,
    superseded_id: &str,
) -> Result<()> {
    if superseding_id == superseded_id {
        return Err(Error::InvalidSupersession(format!(
            "self-supersession: {superseding_id}"
        )));
    }
    let sup = memories.get(superseding_id).ok_or_else(|| {
        Error::InvalidSupersession(format!("superseding memory not found: {superseding_id}"))
    })?;
    let old = memories.get(superseded_id).ok_or_else(|| {
        Error::InvalidSupersession(format!("superseded memory not found: {superseded_id}"))
    })?;

    // A PENDING memory may never supersede authoritative state (R-12).
    if sup.lifecycle == Lifecycle::Pending {
        return Err(Error::InvalidSupersession(format!(
            "PENDING memory {superseding_id} cannot supersede {superseded_id}"
        )));
    }
    // Cross-vault supersession is meaningless: vault is a required dimension.
    if sup.scope.vault != old.scope.vault {
        return Err(Error::InvalidSupersession(format!(
            "cross-vault supersession {} -> {}",
            sup.scope.vault, old.scope.vault
        )));
    }
    // Cross-project supersession would be a cross-project write primitive,
    // bypassing scope isolation entirely.
    match (&sup.scope.project, &old.scope.project) {
        (Some(a), Some(b)) if a != b => {
            return Err(Error::InvalidSupersession(format!(
                "cross-project supersession {a} -> {b}"
            )))
        }
        _ => {}
    }
    // A USER_CONFIRMED memory may only be superseded by another confirmed one.
    if old.verification == Verification::UserConfirmed
        && sup.verification != Verification::UserConfirmed
    {
        return Err(Error::InvalidSupersession(format!(
            "{superseding_id} ({:?}) cannot supersede USER_CONFIRMED {superseded_id}",
            sup.verification
        )));
    }
    // Cycle detection: walking from the proposed target must not reach the source.
    if reaches(memories, superseded_id, superseding_id) {
        return Err(Error::InvalidSupersession(format!(
            "cycle: {superseded_id} already reaches {superseding_id}"
        )));
    }
    Ok(())
}

fn reaches(memories: &HashMap<String, Memory>, from: &str, target: &str) -> bool {
    let mut seen = HashSet::new();
    let mut stack = vec![from.to_string()];
    while let Some(cur) = stack.pop() {
        if cur == target {
            return true;
        }
        if !seen.insert(cur.clone()) {
            continue;
        }
        if let Some(m) = memories.get(&cur) {
            for next in &m.supersedes {
                stack.push(next.clone());
            }
        }
    }
    false
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::memory::{MemoryType, Scope};

    fn m(id: &str, seq: u64, valid_from: i64, basis: Basis, scope: Scope) -> Memory {
        Memory::new(id, format!("stmt-{id}"), MemoryType::Decision, basis, scope, seq, valid_from)
            .unwrap()
            .with_triple("project", "framework")
    }

    #[test]
    fn no_answer_when_nothing_matches() {
        let out = resolve(&[], "project", "framework", &Scope::vault_global("v"), 100, 100);
        assert_eq!(out, ResolveOutcome::NoAnswer);
    }

    #[test]
    fn current_and_historical_truth_differ() {
        let s = Scope::vault_global("v");
        let mut old = m("react", 1, 10, Basis::UserAsserted, s.clone());
        old.valid_until = Some(50);
        let new = m("solid", 2, 50, Basis::UserAsserted, s.clone());
        let all = vec![old, new];

        // Current: the later value.
        match resolve(&all, "project", "framework", &s, 100, 100) {
            ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "solid"),
            o => panic!("expected solid, got {o:?}"),
        }
        // Historical: what was true at day 20.
        match resolve(&all, "project", "framework", &s, 20, 100) {
            ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "react"),
            o => panic!("expected react, got {o:?}"),
        }
    }

    #[test]
    fn recorded_time_bounds_what_was_known() {
        let s = Scope::vault_global("v");
        let a = m("a", 1, 10, Basis::UserAsserted, s.clone());
        let b = m("b", 9, 20, Basis::UserAsserted, s.clone());
        let all = vec![a, b];
        // As of recorded_seq 5, 'b' had not been learned yet.
        match resolve(&all, "project", "framework", &s, 100, 5) {
            ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "a"),
            o => panic!("expected a, got {o:?}"),
        }
    }

    #[test]
    fn verification_outranks_basis() {
        let s = Scope::vault_global("v");
        let mut confirmed_agent = m("agent", 1, 10, Basis::AgentAsserted, s.clone());
        confirmed_agent.verification = Verification::UserConfirmed;
        let unverified_user = m("user", 2, 10, Basis::UserAsserted, s.clone());
        let all = vec![confirmed_agent, unverified_user];
        match resolve(&all, "project", "framework", &s, 100, 100) {
            ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "agent"),
            o => panic!("verification must outrank basis, got {o:?}"),
        }
    }

    #[test]
    fn vault_global_never_outranks_conflicting_project_local() {
        // The dangerous direction is structurally unavailable: project-local is
        // strictly more specific, so it wins rung 3 and global cannot.
        let global = m("global", 5, 10, Basis::UserAsserted, Scope::vault_global("v"));
        let local = m("local", 1, 10, Basis::UserAsserted, Scope::project("v", "p"));
        let all = vec![global, local];
        match resolve(&all, "project", "framework", &Scope::project("v", "p"), 100, 100) {
            ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "local"),
            o => panic!("project-local must win, got {o:?}"),
        }
    }

    #[test]
    fn incomparable_scopes_yield_contradiction_not_a_winner() {
        // Two vault-global memories, identical on every rung. Nothing separates
        // them, so the honest answer is CONTRADICTION.
        let s = Scope::vault_global("v");
        let a = m("a", 7, 10, Basis::UserAsserted, s.clone());
        let b = m("b", 7, 10, Basis::UserAsserted, s.clone());
        let all = vec![a, b];
        match resolve(&all, "project", "framework", &s, 100, 100) {
            ResolveOutcome::Contradiction(c) => assert_eq!(c.len(), 2),
            o => panic!("expected contradiction, got {o:?}"),
        }
    }

    /// The decision an outcome represents: which variant, and which memories in
    /// which order. Deliberately excludes the memories' own field values, because
    /// the confidence test mutates one of those fields on purpose — comparing whole
    /// records would assert that the echoed input is unchanged, which is trivially
    /// false and not the property under test.
    fn outcome_shape(o: &ResolveOutcome) -> (u8, Vec<String>) {
        match o {
            ResolveOutcome::NoAnswer => (0, vec![]),
            ResolveOutcome::Answer(m) => (1, vec![m.id.0.clone()]),
            ResolveOutcome::Contradiction(ms) => {
                (2, ms.iter().map(|m| m.id.0.clone()).collect())
            }
        }
    }

    #[test]
    fn confidence_cannot_change_outcome() {
        // F-CORE-07 asserted behaviourally rather than by inspection: mutate
        // confidence across its full range, including the case where it would
        // reverse a winner if it were consulted, and require the DECISION to be
        // identical every time.
        let s = Scope::vault_global("v");
        let base_a = m("a", 7, 10, Basis::UserAsserted, s.clone());
        let base_b = m("b", 7, 10, Basis::UserAsserted, s.clone());

        let mut previous: Option<(u8, Vec<String>)> = None;
        for conf in [0.0f32, 0.01, 0.5, 0.99, 1.0] {
            let mut a = base_a.clone();
            let mut b = base_b.clone();
            a.confidence_diagnostic = Some(conf);
            b.confidence_diagnostic = Some(1.0 - conf);
            let shape = outcome_shape(&resolve(&[a, b], "project", "framework", &s, 100, 100));
            if let Some(prev) = &previous {
                assert_eq!(&shape, prev, "confidence must not affect resolution");
            }
            previous = Some(shape);
        }
        // And the invariant outcome is CONTRADICTION -- not a confidence-picked
        // winner, which is exactly what F1's sixth rung would have produced.
        let (variant, ids) = previous.unwrap();
        assert_eq!(variant, 2, "expected CONTRADICTION");
        assert_eq!(ids, vec!["a".to_string(), "b".to_string()]);
    }

    #[test]
    fn confidence_cannot_break_a_tie_that_evidence_cannot() {
        // The specific F1 defect: when the principled ladder is exhausted, an
        // uncalibrated model-produced float decided the answer. Give one candidate
        // maximum confidence and the other minimum, and require CONTRADICTION.
        let s = Scope::vault_global("v");
        let mut a = m("a", 7, 10, Basis::UserAsserted, s.clone());
        let mut b = m("b", 7, 10, Basis::UserAsserted, s.clone());
        a.confidence_diagnostic = Some(1.0);
        b.confidence_diagnostic = Some(0.0);
        match resolve(&[a, b], "project", "framework", &s, 100, 100) {
            ResolveOutcome::Contradiction(c) => assert_eq!(c.len(), 2),
            o => panic!("confidence must not pick a winner, got {o:?}"),
        }
    }

    #[test]
    fn pending_is_excluded_from_resolution() {
        let s = Scope::vault_global("v");
        let mut pending = m("pending", 9, 90, Basis::UserAsserted, s.clone());
        pending.lifecycle = Lifecycle::Pending;
        let active = m("active", 1, 10, Basis::UserAsserted, s.clone());
        match resolve(&[pending, active], "project", "framework", &s, 100, 100) {
            ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "active"),
            o => panic!("PENDING must not win, got {o:?}"),
        }
    }

    #[test]
    fn superseded_cannot_reactivate() {
        let s = Scope::vault_global("v");
        let mut old = m("old", 1, 10, Basis::UserAsserted, s.clone());
        old.lifecycle = Lifecycle::Superseded;
        assert_eq!(
            resolve(&[old], "project", "framework", &s, 100, 100),
            ResolveOutcome::NoAnswer
        );
    }

    fn map(ms: Vec<Memory>) -> HashMap<String, Memory> {
        ms.into_iter().map(|m| (m.id.0.clone(), m)).collect()
    }

    #[test]
    fn rejects_all_five_invalid_supersession_classes() {
        let s = Scope::vault_global("v");

        // 1. self-supersession
        let ms = map(vec![m("a", 1, 0, Basis::UserAsserted, s.clone())]);
        assert!(validate_supersession(&ms, "a", "a").is_err());

        // 2. cycle
        let mut a = m("a", 1, 0, Basis::UserAsserted, s.clone());
        a.supersedes.push("b".into());
        let b = m("b", 2, 0, Basis::UserAsserted, s.clone());
        let ms = map(vec![a, b]);
        assert!(validate_supersession(&ms, "b", "a").is_err());

        // 3. cross-vault
        let x = m("x", 1, 0, Basis::UserAsserted, Scope::vault_global("v1"));
        let y = m("y", 2, 0, Basis::UserAsserted, Scope::vault_global("v2"));
        let ms = map(vec![x, y]);
        assert!(validate_supersession(&ms, "x", "y").is_err());

        // 4. cross-project
        let p = m("p", 1, 0, Basis::UserAsserted, Scope::project("v", "a"));
        let q = m("q", 2, 0, Basis::UserAsserted, Scope::project("v", "b"));
        let ms = map(vec![p, q]);
        assert!(validate_supersession(&ms, "p", "q").is_err());

        // 5. PENDING supersedes authoritative
        let mut pend = m("pend", 1, 0, Basis::UserAsserted, s.clone());
        pend.lifecycle = Lifecycle::Pending;
        let act = m("act", 2, 0, Basis::UserAsserted, s.clone());
        let ms = map(vec![pend, act]);
        assert!(validate_supersession(&ms, "pend", "act").is_err());
    }

    #[test]
    fn unverified_cannot_supersede_user_confirmed() {
        let s = Scope::vault_global("v");
        let mut confirmed = m("c", 1, 0, Basis::UserAsserted, s.clone());
        confirmed.verification = Verification::UserConfirmed;
        let plain = m("p", 2, 0, Basis::AgentAsserted, s.clone());
        let ms = map(vec![confirmed, plain]);
        assert!(validate_supersession(&ms, "p", "c").is_err());
    }

    #[test]
    fn valid_supersession_is_accepted() {
        let s = Scope::vault_global("v");
        let old = m("old", 1, 0, Basis::UserAsserted, s.clone());
        let new = m("new", 2, 0, Basis::UserAsserted, s.clone());
        let ms = map(vec![old, new]);
        assert!(validate_supersession(&ms, "new", "old").is_ok());
    }

    #[test]
    fn superseded_without_valid_until_is_excluded_at_every_point_in_time() {
        // The conservative half of `admissible_at`. We know it stopped being in
        // force; we do NOT know when. Placing it anywhere on the timeline would be
        // inventing an interval, so it is admissible nowhere -- which is also what
        // keeps K-10 true.
        let mut mm = m("m", 1, 1, Basis::UserAsserted, Scope::vault_global("v"));
        mm.lifecycle = Lifecycle::Superseded;
        assert!(mm.valid_until.is_none());
        for as_of in [0i64, 1, 5, 100, i64::MAX] {
            assert!(
                matches!(
                    resolve(std::slice::from_ref(&mm), "project", "framework", &Scope::vault_global("v"), as_of, u64::MAX),
                    ResolveOutcome::NoAnswer
                ),
                "superseded-without-valid_until must not answer at {as_of}"
            );
        }
    }

    #[test]
    fn superseded_with_valid_until_answers_for_the_interval_it_governed() {
        // The other half. `valid_until` records when it stopped, so history is
        // reachable -- and the present is still correctly refused.
        let mut mm = m("m", 1, 10, Basis::UserAsserted, Scope::vault_global("v"));
        mm.lifecycle = Lifecycle::Superseded;
        mm.valid_until = Some(20);

        for inside in [10i64, 15, 19] {
            match resolve(std::slice::from_ref(&mm), "project", "framework", &Scope::vault_global("v"), inside, u64::MAX) {
                ResolveOutcome::Answer(w) => assert_eq!(w.id.0, "m"),
                o => panic!("day {inside} is inside [10, 20), got {o:?}"),
            }
        }
        // Half-open: the closing bound is NOT included.
        for outside in [9i64, 20, 21, i64::MAX] {
            assert!(
                matches!(
                    resolve(std::slice::from_ref(&mm), "project", "framework", &Scope::vault_global("v"), outside, u64::MAX),
                    ResolveOutcome::NoAnswer
                ),
                "day {outside} is outside [10, 20)"
            );
        }
    }

    #[test]
    fn retracted_is_never_admissible_even_with_a_valid_interval() {
        // This is what separates RETRACTED from SUPERSEDED. A supersession says
        // "true then, not now". A retraction says "never true" -- so no valid-time
        // window can resurrect it, and giving it one must change nothing.
        let mut mm = m("m", 1, 10, Basis::UserAsserted, Scope::vault_global("v"));
        mm.lifecycle = Lifecycle::Retracted;
        mm.valid_until = Some(20);
        for as_of in [9i64, 10, 15, 19, 20, i64::MAX] {
            assert!(
                matches!(
                    resolve(std::slice::from_ref(&mm), "project", "framework", &Scope::vault_global("v"), as_of, u64::MAX),
                    ResolveOutcome::NoAnswer
                ),
                "retracted must not answer at {as_of}"
            );
        }
    }
}
