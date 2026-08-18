//! Explicit durable memory with four orthogonal semantic axes.
//!
//! **F-CORE-07.** The four axes are separate fields with separate types. There is
//! deliberately no combined status type and no `Ord` on any of them that could be
//! used to build a total order across axes — the R1 eight-state enum failed
//! precisely because ordering an *origin* against a *verification level* is a
//! category error.
//!
//! **Automatic extraction and promotion do not exist here.** Phase T writes memory
//! only when explicitly told to.

use crate::identity::ObjectId;
use crate::{limits, Error, Result};
use serde::{Deserialize, Serialize};

/// Axis 1 — where the claim came from. **Core-assigned; never actor-supplied.**
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Basis {
    UserAsserted,
    Extracted,
    AgentAsserted,
    Inferred,
}

/// Axis 2 — whether it has been checked, and by whom.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Verification {
    Unverified,
    Corroborated,
    UserConfirmed,
}

/// Axis 3 — whether it is in force.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Lifecycle {
    /// Recorded and visible, but **not authoritative** (F §5.5).
    Pending,
    Active,
    Superseded,
    Retracted,
    Expired,
}

/// Axis 4 — whether it currently resolves cleanly.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Resolution {
    Clear,
    Conflicted,
    /// Its own evidence does not resolve; cannot participate in resolution.
    Unresolved,
}

/// The Phase T memory types — five, not eleven (Ponytail SHRINK).
///
/// These five carry every dimension the benchmark measures. The rest would add
/// vocabulary without adding a tested property.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MemoryType {
    Fact,
    Decision,
    Constraint,
    Gotcha,
    State,
}

/// Scope as **orthogonal dimensions**, not an ordered lattice (F §3.4).
///
/// Valid time is deliberately absent: it is temporal validity, not containment,
/// and it has its own fields on the record.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Scope {
    /// Always required. There is no cross-vault memory in Phase T.
    pub vault: String,
    /// `None` = not project-restricted (vault-global).
    pub project: Option<String>,
}

impl Scope {
    pub fn vault_global(vault: impl Into<String>) -> Self {
        Scope {
            vault: vault.into(),
            project: None,
        }
    }
    pub fn project(vault: impl Into<String>, project: impl Into<String>) -> Self {
        Scope {
            vault: vault.into(),
            project: Some(project.into()),
        }
    }

    /// Does this memory's scope admit a request at `req`?
    ///
    /// Dimension-wise: for each dimension, either this scope is unconstrained, or
    /// the request's value is admitted.
    pub fn matches(&self, req: &Scope) -> bool {
        if self.vault != req.vault {
            return false;
        }
        match (&self.project, &req.project) {
            (None, _) => true,        // unconstrained: applies anywhere in the vault
            (Some(_), None) => false, // constrained memory, unconstrained request
            (Some(a), Some(b)) => a == b,
        }
    }

    /// Specificity as a **partial** order (F §3.4).
    ///
    /// Returns `Some(Ordering)` only when the two are genuinely comparable.
    /// `None` means incomparable — and incomparable scopes must not be used to
    /// pick a winner, which is why the resolver skips the rung rather than
    /// inventing a tie-break.
    pub fn specificity_cmp(&self, other: &Scope) -> Option<std::cmp::Ordering> {
        use std::cmp::Ordering;
        if self.vault != other.vault {
            return None;
        }
        match (&self.project, &other.project) {
            (Some(a), Some(b)) if a == b => Some(Ordering::Equal),
            (Some(_), Some(_)) => None, // different projects: incomparable
            // A project-restricted scope is strictly MORE specific than
            // vault-global. This is what makes it structurally impossible for a
            // vault-global memory to outrank a conflicting project-local one.
            (Some(_), None) => Some(Ordering::Greater),
            (None, Some(_)) => Some(Ordering::Less),
            (None, None) => Some(Ordering::Equal),
        }
    }
}

/// Evidence supporting a memory.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Evidence {
    pub object_id: String,
    /// The context package whose manifest served this item, if any.
    /// K-04: an evidence claim without a matching manifest entry is not
    /// "observed by this session".
    pub served_in: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MemoryId(pub String);

/// One explicit durable memory.
///
/// `PartialEq` (not `Eq`) because `confidence_diagnostic` is an `f32`. That is
/// deliberate and harmless: the field is diagnostic metadata and never
/// participates in ordering or resolution.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Memory {
    pub id: MemoryId,
    pub statement: String,
    /// Subject/predicate for structured resolution. Optional: not every useful
    /// memory is a clean triple, and refusing those would discard most gotchas.
    pub subject: Option<String>,
    pub predicate: Option<String>,
    pub memory_type: MemoryType,

    pub basis: Basis,
    pub verification: Verification,
    pub lifecycle: Lifecycle,
    pub resolution: Resolution,

    pub scope: Scope,
    /// System-assigned monotonic order. Actors cannot supply it — this is what
    /// defeats backdating (T-5).
    pub recorded_seq: u64,
    /// Actor-supplied valid time, as a simple ordinal day for Phase T fixtures.
    pub valid_from: i64,
    pub valid_until: Option<i64>,

    pub supersedes: Vec<String>,
    pub evidence: Vec<Evidence>,
    /// Diagnostic only. **Never an input to resolution** (F-CORE-07).
    /// The resolver does not read this field; `test_confidence_cannot_change_outcome`
    /// asserts that by mutating it across the full range.
    pub confidence_diagnostic: Option<f32>,
}

impl Memory {
    /// Construct a memory. `basis` is a parameter here because the *core* supplies
    /// it at the call site; no deserialized or user-supplied value reaches it.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        id: impl Into<String>,
        statement: impl Into<String>,
        memory_type: MemoryType,
        basis: Basis,
        scope: Scope,
        recorded_seq: u64,
        valid_from: i64,
    ) -> Result<Self> {
        let statement = statement.into();
        if statement.len() > limits::MAX_STATEMENT_BYTES {
            return Err(Error::LimitExceeded {
                what: "memory statement",
                limit: limits::MAX_STATEMENT_BYTES,
                actual: statement.len(),
            });
        }
        Ok(Memory {
            id: MemoryId(id.into()),
            statement,
            subject: None,
            predicate: None,
            memory_type,
            basis,
            verification: Verification::Unverified,
            lifecycle: Lifecycle::Active,
            resolution: Resolution::Clear,
            scope,
            recorded_seq,
            valid_from,
            valid_until: None,
            supersedes: Vec::new(),
            evidence: Vec::new(),
            confidence_diagnostic: None,
        })
    }

    pub fn with_triple(mut self, subject: &str, predicate: &str) -> Self {
        self.subject = Some(subject.to_string());
        self.predicate = Some(predicate.to_string());
        self
    }

    pub fn with_evidence(mut self, object_id: ObjectId, served_in: Option<String>) -> Self {
        self.evidence.push(Evidence {
            object_id: object_id.to_string(),
            served_in,
        });
        self
    }

    /// Is this memory authoritative — eligible to be reported as current state?
    ///
    /// `PENDING` is excluded here, which is the single place that enforces R-12
    /// for the resolver path.
    pub fn is_authoritative(&self) -> bool {
        self.lifecycle == Lifecycle::Active && self.resolution != Resolution::Unresolved
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn mem(scope: Scope) -> Memory {
        Memory::new(
            "m1",
            "s",
            MemoryType::Fact,
            Basis::UserAsserted,
            scope,
            1,
            0,
        )
        .unwrap()
    }

    #[test]
    fn vault_global_applies_everywhere_project_local_does_not() {
        let global = Scope::vault_global("v");
        let proj_a = Scope::project("v", "a");
        assert!(global.matches(&Scope::project("v", "a")));
        assert!(global.matches(&Scope::vault_global("v")));
        assert!(proj_a.matches(&Scope::project("v", "a")));
        assert!(!proj_a.matches(&Scope::project("v", "b")));
        // A project-restricted memory must not answer an unrestricted request.
        assert!(!proj_a.matches(&Scope::vault_global("v")));
        // Different vault never matches.
        assert!(!global.matches(&Scope::vault_global("other")));
    }

    #[test]
    fn project_local_is_strictly_more_specific_than_vault_global() {
        use std::cmp::Ordering;
        let global = Scope::vault_global("v");
        let local = Scope::project("v", "a");
        assert_eq!(local.specificity_cmp(&global), Some(Ordering::Greater));
        assert_eq!(global.specificity_cmp(&local), Some(Ordering::Less));
    }

    #[test]
    fn different_projects_are_incomparable_not_ordered() {
        // The dangerous alternative would be inventing an order here, which would
        // let one project's memory outrank another's for no principled reason.
        let a = Scope::project("v", "a");
        let b = Scope::project("v", "b");
        assert_eq!(a.specificity_cmp(&b), None);
    }

    #[test]
    fn pending_is_not_authoritative() {
        let mut m = mem(Scope::vault_global("v"));
        assert!(m.is_authoritative());
        m.lifecycle = Lifecycle::Pending;
        assert!(!m.is_authoritative());
    }

    #[test]
    fn unresolved_evidence_cannot_participate() {
        let mut m = mem(Scope::vault_global("v"));
        m.resolution = Resolution::Unresolved;
        assert!(!m.is_authoritative());
    }

    #[test]
    fn oversized_statement_is_rejected() {
        let big = "x".repeat(limits::MAX_STATEMENT_BYTES + 1);
        assert!(matches!(
            Memory::new(
                "m",
                big,
                MemoryType::Fact,
                Basis::UserAsserted,
                Scope::vault_global("v"),
                1,
                0
            ),
            Err(Error::LimitExceeded { .. })
        ));
    }
}
