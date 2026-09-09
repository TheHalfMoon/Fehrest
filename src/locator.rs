//! Root-confined location resolution and post-open identity verification.
//!
//! **E §12.1 — two independent guarantees, and neither substitutes for the other.**
//!
//! ```text
//! Without containment          Without identity verification
//! -------------------          -----------------------------
//! a read reaches OUTSIDE the   a poisoned locator swaps WHICH
//! vault before any UUID is     in-vault object is served.
//! examined                     Entirely inside the root, so
//!                              containment never fires.
//! ```
//!
//! Both are implemented here, separately, and tested separately.

use crate::identity::{self, ObjectId};
use crate::{Error, Result};
use std::fs::File;
use std::io::Read;
use std::path::{Component, Path, PathBuf};

/// An untrusted locator hint, typically read from the derived store.
///
/// F-CORE-10: derived paths answer *where the object probably was*, never *what
/// may be opened*. The newtype exists so a raw string from SQLite cannot be
/// mistaken for an authorized path anywhere in the codebase.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Locator(String);

impl Locator {
    pub fn new(rel: impl Into<String>) -> Self {
        Locator(rel.into())
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// Reject a locator before touching the filesystem.
///
/// This is the cheap first gate: absolute paths, parent traversal, and Windows
/// prefixes (drive letters, UNC, `\\?\`) never reach an `open` call.
fn reject_unsafe_components(rel: &str) -> Result<PathBuf> {
    if rel.is_empty() {
        return Err(Error::Containment("empty locator".into()));
    }
    let p = Path::new(rel);
    let mut out = PathBuf::new();
    for c in p.components() {
        match c {
            Component::Normal(seg) => out.push(seg),
            Component::CurDir => {}
            Component::ParentDir => {
                return Err(Error::Containment(format!("parent traversal in {rel:?}")))
            }
            Component::RootDir => return Err(Error::Containment(format!("absolute path {rel:?}"))),
            Component::Prefix(_) => {
                return Err(Error::Containment(format!("path prefix in {rel:?}")))
            }
        }
    }
    if out.as_os_str().is_empty() {
        return Err(Error::Containment("locator resolves to nothing".into()));
    }
    Ok(out)
}

/// Open a file strictly inside `root`, following the containment contract.
///
/// Order matters and is deliberate:
/// 1. reject dangerous components before any syscall;
/// 2. reject a symlink/reparse point on the final component **before** opening it;
/// 3. open;
/// 4. verify the canonical parent chain still resolves inside the root.
///
/// Step 4 runs after the open so that a directory swapped between check and open
/// cannot leave us holding a handle outside the root — the handle is discarded if
/// verification fails.
pub fn open_confined(root: &Path, rel: &str) -> Result<File> {
    let safe = reject_unsafe_components(rel)?;
    let candidate = root.join(&safe);

    // A symlink on the final component is refused outright. T-8: symlinks are not
    // followed during ingestion by default, and "the target happens to be inside
    // the vault" is not a reason to relax it — the target can change.
    let meta = std::fs::symlink_metadata(&candidate)
        .map_err(|e| Error::Containment(format!("cannot stat {rel:?}: {e}")))?;
    if meta.file_type().is_symlink() {
        return Err(Error::Containment(format!("symlink not followed: {rel:?}")));
    }
    if !meta.file_type().is_file() {
        return Err(Error::Containment(format!("not a regular file: {rel:?}")));
    }

    let file = File::open(&candidate)
        .map_err(|e| Error::Containment(format!("cannot open {rel:?}: {e}")))?;

    // The parent chain must canonicalise inside the root. This catches a symlinked
    // *directory* component, which the final-component check above does not see.
    let root_canon = root
        .canonicalize()
        .map_err(|e| Error::Containment(format!("vault root unresolvable: {e}")))?;
    let parent = candidate
        .parent()
        .ok_or_else(|| Error::Containment("locator has no parent".into()))?;
    let parent_canon = parent
        .canonicalize()
        .map_err(|e| Error::Containment(format!("parent unresolvable for {rel:?}: {e}")))?;
    if !parent_canon.starts_with(&root_canon) {
        return Err(Error::Containment(format!(
            "escapes vault root: {rel:?} -> {}",
            parent_canon.display()
        )));
    }

    Ok(file)
}

/// Read an object through the confined path and verify its identity **after** opening.
///
/// The content is read from the already-open handle. The path is never re-resolved,
/// which is what makes the check meaningful under a concurrent swap: whatever the
/// handle refers to is what gets verified and what gets returned.
///
/// A mismatch fails closed. Serving the bytes anyway is how a poisoned locator
/// becomes a content substitution that every downstream provenance record then
/// attests to.
pub fn read_verified(root: &Path, rel: &str, expected: ObjectId) -> Result<String> {
    let mut file = open_confined(root, rel)?;
    let mut content = String::new();
    file.read_to_string(&mut content)
        .map_err(|e| Error::Containment(format!("cannot read {rel:?}: {e}")))?;

    let actual = identity::read_id(&content).map_err(|e| match e {
        Error::NoFrontmatter | Error::MissingId => Error::IdentityMismatch {
            expected: expected.to_string(),
            actual: "<no embedded identity>".into(),
        },
        other => other,
    })?;

    if actual != expected {
        return Err(Error::IdentityMismatch {
            expected: expected.to_string(),
            actual: actual.to_string(),
        });
    }
    Ok(content)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    fn tmp() -> PathBuf {
        let d = std::env::temp_dir().join(format!("fehrest-loc-{}", uuid::Uuid::now_v7()));
        fs::create_dir_all(&d).unwrap();
        d
    }

    #[test]
    fn rejects_absolute_and_traversal_and_prefix() {
        for bad in ["../escape.md", "a/../../escape.md", "/etc/passwd", "", "./"] {
            assert!(
                reject_unsafe_components(bad).is_err(),
                "should reject {bad:?}"
            );
        }
        #[cfg(windows)]
        for bad in ["C:\\Windows\\win.ini", "\\\\?\\C:\\x", "\\\\server\\share"] {
            assert!(
                reject_unsafe_components(bad).is_err(),
                "should reject {bad:?}"
            );
        }
    }

    #[test]
    fn accepts_ordinary_relative_paths() {
        assert!(reject_unsafe_components("notes/a.md").is_ok());
        assert!(reject_unsafe_components("./notes/a.md").is_ok());
    }

    #[test]
    fn open_confined_rejects_traversal_even_when_target_exists() {
        let root = tmp();
        let outside = root.parent().unwrap().join("outside-secret.md");
        fs::write(&outside, "secret").unwrap();
        let inner = root.join("vault");
        fs::create_dir_all(&inner).unwrap();

        let err = open_confined(&inner, "../outside-secret.md").unwrap_err();
        assert!(matches!(err, Error::Containment(_)));

        let _ = fs::remove_file(&outside);
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn post_open_identity_mismatch_fails_closed() {
        let root = tmp();
        let wanted = ObjectId::generate();
        let other = ObjectId::generate();
        // The file exists, is inside the root, and opens fine — containment passes.
        // Only the identity check catches the substitution.
        fs::write(root.join("a.md"), format!("---\nid: {other}\n---\nbody\n")).unwrap();

        let err = read_verified(&root, "a.md", wanted).unwrap_err();
        match err {
            Error::IdentityMismatch { expected, actual } => {
                assert_eq!(expected, wanted.to_string());
                assert_eq!(actual, other.to_string());
            }
            e => panic!("expected IdentityMismatch, got {e:?}"),
        }
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn post_open_verification_accepts_matching_identity() {
        let root = tmp();
        let id = ObjectId::generate();
        fs::write(root.join("a.md"), format!("---\nid: {id}\n---\nhello\n")).unwrap();
        let content = read_verified(&root, "a.md", id).unwrap();
        assert!(content.contains("hello"));
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn file_without_identity_is_a_mismatch_not_a_pass() {
        let root = tmp();
        let id = ObjectId::generate();
        fs::write(root.join("plain.md"), "no frontmatter at all\n").unwrap();
        assert!(matches!(
            read_verified(&root, "plain.md", id),
            Err(Error::IdentityMismatch { .. })
        ));
        let _ = fs::remove_dir_all(&root);
    }
}
