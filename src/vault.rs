//! Vault root, content admission, and the single-writer lock.

use crate::identity::{self, ObjectId};
use crate::limits;
use crate::{Error, Result};
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

/// Control directory. Never indexed as user knowledge (F-CORE-16).
pub const CONTROL_DIR: &str = ".fehrest";

/// Directory names excluded from ordinary knowledge indexing.
///
/// `.fehrest` holds Fehrest's own canonical machine state — indexing it would feed
/// audit records back as knowledge. `.git` holds object data, hooks, and remote
/// URLs that can carry credentials.
const RESERVED_DIRS: &[&str] = &[CONTROL_DIR, ".git"];

/// Supported canonical content. **Allowlist, not deny-list** (F-CORE-16).
///
/// A deny-list of secret filenames is a permanent race against names nobody has
/// thought of, and it fails toward indexing. This fails toward exclusion.
const SUPPORTED_EXTENSIONS: &[&str] = &["md", "markdown"];

pub fn is_supported(path: &Path) -> bool {
    path.extension()
        .and_then(|e| e.to_str())
        .map(|e| SUPPORTED_EXTENSIONS.contains(&e.to_ascii_lowercase().as_str()))
        .unwrap_or(false)
}

fn is_reserved_component(name: &str) -> bool {
    RESERVED_DIRS.contains(&name)
}

/// One admitted canonical object.
#[derive(Debug, Clone)]
pub struct ObjectRecord {
    pub id: ObjectId,
    /// Vault-relative locator, forward-slash normalised for stable storage.
    pub rel_path: String,
    pub title: Option<String>,
    pub project: Option<String>,
    pub content_hash: String,
    pub body: String,
}

/// The result of scanning a vault.
#[derive(Debug, Default)]
pub struct ScanResult {
    pub objects: Vec<ObjectRecord>,
    /// Files skipped because they are not supported content or sit under a
    /// reserved directory. Recorded so exclusion is visible, not silent.
    pub skipped: Vec<String>,
    /// Files that look canonical but could not be parsed. Surfaced, never ignored.
    pub malformed: Vec<(String, String)>,
    /// Duplicate identities: one id observed at two or more locations.
    ///
    /// D §3.2: both are retained and neither is silently discarded. Guessing which
    /// is "real" merges two objects' histories, which is unrecoverable.
    pub conflicts: Vec<(ObjectId, Vec<String>)>,
}

/// An open vault. Holding this value holds the write lock.
#[derive(Debug)]
pub struct Vault {
    root: PathBuf,
    lock: Option<WriteLock>,
}

impl Vault {
    /// Create a new vault, taking the write lock.
    pub fn create(root: impl AsRef<Path>) -> Result<Self> {
        let root = root.as_ref().to_path_buf();
        fs::create_dir_all(root.join(CONTROL_DIR))
            .map_err(|e| Error::Vault(format!("cannot create control dir: {e}")))?;
        Self::open_write(root)
    }

    /// Open an existing vault for writing, taking the single-writer lock.
    pub fn open_write(root: impl AsRef<Path>) -> Result<Self> {
        let root = root.as_ref().to_path_buf();
        Self::require_vault(&root)?;
        let lock = WriteLock::acquire(&root)?;
        Ok(Vault {
            root,
            lock: Some(lock),
        })
    }

    /// Open read-only. Takes no lock, so concurrent readers are fine.
    pub fn open_read(root: impl AsRef<Path>) -> Result<Self> {
        let root = root.as_ref().to_path_buf();
        Self::require_vault(&root)?;
        Ok(Vault { root, lock: None })
    }

    fn require_vault(root: &Path) -> Result<()> {
        if !root.join(CONTROL_DIR).is_dir() {
            return Err(Error::Vault(format!(
                "not a Fehrest vault (no {CONTROL_DIR}/): {}",
                root.display()
            )));
        }
        Ok(())
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    pub fn control_dir(&self) -> PathBuf {
        self.root.join(CONTROL_DIR)
    }

    pub fn has_write_lock(&self) -> bool {
        self.lock.is_some()
    }

    /// Scan the vault for admitted canonical objects.
    ///
    /// Reads go through the confined path even here: the scan discovers relative
    /// locators, and every subsequent read of one is contained and identity-checked
    /// like any other.
    pub fn scan(&self) -> Result<ScanResult> {
        let mut result = ScanResult::default();
        let mut seen: HashMap<ObjectId, Vec<String>> = HashMap::new();
        self.scan_dir(&self.root, &mut result, &mut seen)?;

        for (id, paths) in seen {
            if paths.len() > 1 {
                let mut paths = paths;
                paths.sort();
                result.conflicts.push((id, paths));
            }
        }
        result.conflicts.sort_by_key(|(id, _)| *id);
        result.objects.sort_by(|a, b| a.rel_path.cmp(&b.rel_path));
        result.skipped.sort();
        Ok(result)
    }

    fn scan_dir(
        &self,
        dir: &Path,
        out: &mut ScanResult,
        seen: &mut HashMap<ObjectId, Vec<String>>,
    ) -> Result<()> {
        let entries =
            fs::read_dir(dir).map_err(|e| Error::Vault(format!("cannot read {dir:?}: {e}")))?;

        for entry in entries {
            let entry = entry.map_err(|e| Error::Vault(format!("bad dir entry: {e}")))?;
            let path = entry.path();
            let name = entry.file_name().to_string_lossy().to_string();

            // symlink_metadata, not metadata: a symlinked directory must not be
            // descended into, and a symlinked file must not be admitted.
            let meta = fs::symlink_metadata(&path)
                .map_err(|e| Error::Vault(format!("cannot stat {path:?}: {e}")))?;

            if meta.file_type().is_symlink() {
                out.skipped.push(self.rel(&path));
                continue;
            }

            if meta.is_dir() {
                if is_reserved_component(&name) {
                    continue; // reserved: not knowledge, not reported as skipped noise
                }
                self.scan_dir(&path, out, seen)?;
                continue;
            }

            if !is_supported(&path) {
                out.skipped.push(self.rel(&path));
                continue;
            }

            if meta.len() > limits::MAX_OBJECT_BYTES as u64 {
                out.malformed.push((
                    self.rel(&path),
                    format!("exceeds MAX_OBJECT_BYTES ({})", limits::MAX_OBJECT_BYTES),
                ));
                continue;
            }

            let rel = self.rel(&path);
            let content = match fs::read_to_string(&path) {
                Ok(c) => c,
                Err(e) => {
                    out.malformed.push((rel, format!("unreadable: {e}")));
                    continue;
                }
            };

            match identity::parse(&content) {
                Ok(parsed) => {
                    let id = parsed.frontmatter.id;
                    seen.entry(id).or_default().push(rel.clone());
                    out.objects.push(ObjectRecord {
                        id,
                        rel_path: rel,
                        title: parsed.frontmatter.title,
                        project: parsed.frontmatter.project,
                        content_hash: crate::events::hash_bytes(content.as_bytes()),
                        body: parsed.body,
                    });
                }
                Err(e) => out.malformed.push((rel, e.to_string())),
            }
        }
        Ok(())
    }

    fn rel(&self, path: &Path) -> String {
        path.strip_prefix(&self.root)
            .unwrap_or(path)
            .to_string_lossy()
            .replace('\\', "/")
    }

    /// Write a new canonical object, allocating an identity.
    pub fn add_object(
        &self,
        rel_path: &str,
        title: Option<&str>,
        project: Option<&str>,
        body: &str,
    ) -> Result<ObjectId> {
        if !self.has_write_lock() {
            return Err(Error::Vault("write requires the vault write lock".into()));
        }
        if body.len() > limits::MAX_OBJECT_BYTES {
            return Err(Error::LimitExceeded {
                what: "object body",
                limit: limits::MAX_OBJECT_BYTES,
                actual: body.len(),
            });
        }
        let safe = crate::locator::Locator::new(rel_path);
        let id = ObjectId::generate();
        let fm = identity::Frontmatter {
            id,
            title: title.map(str::to_string),
            project: project.map(str::to_string),
            unknown: Vec::new(),
        };
        let content = identity::serialize(&fm, body);

        // Reuse the containment check for the write path by resolving through the
        // same rejection rules, then writing under the root.
        let target = self.resolve_for_write(safe.as_str())?;
        if let Some(parent) = target.parent() {
            fs::create_dir_all(parent)
                .map_err(|e| Error::Vault(format!("cannot create parent: {e}")))?;
        }
        fs::write(&target, content).map_err(|e| Error::Vault(format!("cannot write: {e}")))?;
        Ok(id)
    }

    fn resolve_for_write(&self, rel: &str) -> Result<PathBuf> {
        if !is_supported(Path::new(rel)) {
            return Err(Error::Vault(format!(
                "unsupported content type for {rel:?}; supported: {SUPPORTED_EXTENSIONS:?}"
            )));
        }
        for comp in Path::new(rel).components() {
            match comp {
                std::path::Component::Normal(seg) => {
                    let s = seg.to_string_lossy();
                    if is_reserved_component(&s) {
                        return Err(Error::Vault(format!("reserved directory in {rel:?}")));
                    }
                }
                std::path::Component::CurDir => {}
                _ => return Err(Error::Containment(format!("unsafe write locator {rel:?}"))),
            }
        }
        Ok(self.root.join(rel))
    }
}

/// The inter-process single-writer lock (F-CORE-13).
///
/// `create_new` maps to `O_EXCL` / `CREATE_NEW`, so acquisition is atomic and a
/// second writer cannot win a race. A stale lock is **reported, never stolen**:
/// N §1 principle 5 forbids destroying state to restore consistency, and silently
/// taking a lock reintroduces exactly the concurrent-writer risk it prevents.
#[derive(Debug)]
pub struct WriteLock {
    path: PathBuf,
}

impl WriteLock {
    fn acquire(root: &Path) -> Result<Self> {
        let path = root.join(CONTROL_DIR).join("writer.lock");
        match fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&path)
        {
            Ok(mut f) => {
                use std::io::Write;
                let _ = writeln!(f, "pid={}", std::process::id());
                Ok(WriteLock { path })
            }
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {
                let holder = fs::read_to_string(&path).unwrap_or_default();
                Err(Error::WriterLocked {
                    holder: holder.trim().to_string(),
                    path: path.display().to_string(),
                })
            }
            Err(e) => Err(Error::Vault(format!("cannot acquire write lock: {e}"))),
        }
    }
}

impl Drop for WriteLock {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.path);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tmp() -> PathBuf {
        let d = std::env::temp_dir().join(format!("fehrest-vault-{}", uuid::Uuid::now_v7()));
        fs::create_dir_all(&d).unwrap();
        d
    }

    #[test]
    fn allowlist_admits_only_supported_extensions() {
        assert!(is_supported(Path::new("a.md")));
        assert!(is_supported(Path::new("a.MD")));
        assert!(is_supported(Path::new("a.markdown")));
        for bad in ["a.pdf", "a.docx", "a.png", "a.exe", ".env", "a", "a.md.exe"] {
            assert!(!is_supported(Path::new(bad)), "must not admit {bad}");
        }
    }

    #[test]
    fn reserved_dirs_are_excluded_from_knowledge() {
        let root = tmp();
        let v = Vault::create(&root).unwrap();
        fs::create_dir_all(root.join(".git")).unwrap();
        let id = ObjectId::generate();
        fs::write(root.join(".git/config.md"), format!("---\nid: {id}\n---\nsecret\n")).unwrap();
        fs::write(
            root.join(CONTROL_DIR).join("internal.md"),
            format!("---\nid: {}\n---\naudit\n", ObjectId::generate()),
        )
        .unwrap();

        let scan = v.scan().unwrap();
        assert!(scan.objects.is_empty(), "reserved dirs must not be indexed");
        drop(v);
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn duplicate_uuid_is_surfaced_as_conflict_and_both_retained() {
        let root = tmp();
        let v = Vault::create(&root).unwrap();
        let id = ObjectId::generate();
        fs::write(root.join("a.md"), format!("---\nid: {id}\n---\nA\n")).unwrap();
        fs::write(root.join("b.md"), format!("---\nid: {id}\n---\nB\n")).unwrap();

        let scan = v.scan().unwrap();
        assert_eq!(scan.conflicts.len(), 1);
        let (cid, paths) = &scan.conflicts[0];
        assert_eq!(*cid, id);
        assert_eq!(paths.len(), 2);
        // Both retained: neither silently discarded.
        assert_eq!(scan.objects.len(), 2);
        drop(v);
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn second_writer_fails_visibly() {
        let root = tmp();
        let v1 = Vault::create(&root).unwrap();
        let err = Vault::open_write(&root).unwrap_err();
        assert!(matches!(err, Error::WriterLocked { .. }));
        drop(v1);
        // Lock released on drop: a fresh writer may now proceed.
        let v2 = Vault::open_write(&root).unwrap();
        drop(v2);
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn readers_do_not_need_the_lock() {
        let root = tmp();
        let w = Vault::create(&root).unwrap();
        let r = Vault::open_read(&root).unwrap();
        assert!(!r.has_write_lock());
        drop(r);
        drop(w);
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn write_rejects_reserved_and_unsupported_and_traversal() {
        let root = tmp();
        let v = Vault::create(&root).unwrap();
        assert!(v.add_object(".git/x.md", None, None, "b").is_err());
        assert!(v.add_object(".fehrest/x.md", None, None, "b").is_err());
        assert!(v.add_object("x.pdf", None, None, "b").is_err());
        assert!(v.add_object("../x.md", None, None, "b").is_err());
        assert!(v.add_object("ok.md", None, None, "b").is_ok());
        drop(v);
        let _ = fs::remove_dir_all(&root);
    }
}
