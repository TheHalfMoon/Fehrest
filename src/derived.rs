//! Derived SQLite + FTS5 index.
//!
//! **F-CORE-10 — `NON-CANONICAL · REBUILDABLE · UNTRUSTED FOR AUTHORITY`.**
//!
//! Rows here are *hints*. A `rel_path` read from this store is an
//! [`Locator`](crate::locator::Locator), never an authorized path, and a `project`
//! column read from here is a **search accelerator**, never an authorization input
//! — [`authoritative_project`] exists precisely so the difference is visible in the
//! type system and in the call sites.

use crate::identity::ObjectId;
use crate::vault::{ObjectRecord, Vault};
use crate::{limits, Error, Result};
use rusqlite::{Connection, OpenFlags};
use std::path::Path;

/// A lexical search hit. **Untrusted for authority.**
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Candidate {
    pub id: ObjectId,
    /// Untrusted locator hint. Must be opened through `locator::read_verified`.
    pub rel_path: String,
    pub title: Option<String>,
    /// **Accelerator only.** Never read as an authorization input.
    pub project_hint: Option<String>,
}

pub struct Derived {
    conn: Connection,
}

impl Derived {
    /// Open the derived database with the E §13.1 hardening posture.
    pub fn open(control_dir: &Path) -> Result<Self> {
        std::fs::create_dir_all(control_dir)
            .map_err(|e| Error::Derived(format!("cannot create control dir: {e}")))?;
        // Path derives from the vault root. There is no configuration input here,
        // and nothing a document can influence reaches it.
        let db_path = control_dir.join("derived.sqlite");

        let conn = Connection::open_with_flags(
            &db_path,
            OpenFlags::SQLITE_OPEN_READ_WRITE
                | OpenFlags::SQLITE_OPEN_CREATE
                // No URI parsing: blocks `file:...?mode=` style path tricks from
                // ever being interpreted, even if a path reached here.
                | OpenFlags::SQLITE_OPEN_NO_MUTEX,
        )
        .map_err(|e| Error::Derived(format!("cannot open derived db: {e}")))?;

        // Extension loading is disabled by construction. rusqlite does not enable
        // it unless the `load_extension` feature is compiled in — which it is not
        // (see Cargo.toml: default-features = false, features = ["bundled"]).
        // This pragma makes the posture explicit and testable rather than implicit.
        conn.pragma_update(None, "trusted_schema", false)
            .map_err(|e| Error::Derived(format!("cannot set trusted_schema: {e}")))?;
        conn.pragma_update(None, "foreign_keys", true)
            .map_err(|e| Error::Derived(format!("cannot set foreign_keys: {e}")))?;

        let d = Derived { conn };
        d.init_schema()?;
        Ok(d)
    }

    fn init_schema(&self) -> Result<()> {
        self.conn
            .execute_batch(
                "CREATE TABLE IF NOT EXISTS object (
                   id           TEXT PRIMARY KEY,
                   rel_path     TEXT NOT NULL,
                   title        TEXT,
                   project      TEXT,
                   content_hash TEXT NOT NULL
                 );
                 CREATE VIRTUAL TABLE IF NOT EXISTS object_fts USING fts5(
                   id UNINDEXED, title, body,
                   tokenize = 'unicode61 remove_diacritics 2'
                 );",
            )
            .map_err(|e| Error::Derived(format!("cannot init schema: {e}")))
    }

    /// Rebuild the entire index from canonical state.
    ///
    /// Full rebuild only — `INCREMENTAL_REINDEX = YAGNI_DEFERRED`. The consequence
    /// is recorded honestly in `analyze.md` finding A-01: B-12's incremental-vs-fresh
    /// comparison **cannot run**, and is reported as untested rather than passed.
    pub fn rebuild(&self, objects: &[ObjectRecord]) -> Result<usize> {
        self.conn
            .execute_batch("DELETE FROM object; DELETE FROM object_fts;")
            .map_err(|e| Error::Derived(format!("cannot clear index: {e}")))?;

        for o in objects {
            self.conn
                .execute(
                    "INSERT INTO object (id, rel_path, title, project, content_hash)
                     VALUES (?1, ?2, ?3, ?4, ?5)",
                    rusqlite::params![
                        o.id.to_string(),
                        o.rel_path,
                        o.title,
                        o.project,
                        o.content_hash
                    ],
                )
                .map_err(|e| Error::Derived(format!("cannot insert object: {e}")))?;
            self.conn
                .execute(
                    "INSERT INTO object_fts (id, title, body) VALUES (?1, ?2, ?3)",
                    rusqlite::params![o.id.to_string(), o.title.clone().unwrap_or_default(), o.body],
                )
                .map_err(|e| Error::Derived(format!("cannot insert fts row: {e}")))?;
        }
        Ok(objects.len())
    }

    /// Lexical candidate generation. **Candidates only** — never authority.
    ///
    /// Results are ordered by `(rank, id)`. The `id` tiebreak makes ordering
    /// deterministic even when FTS5 assigns equal ranks, which is what lets two
    /// independent rebuilds be compared for equality at all.
    pub fn search(&self, query: &str, limit: usize) -> Result<Vec<Candidate>> {
        if query.len() > limits::MAX_QUERY_BYTES {
            return Err(Error::LimitExceeded {
                what: "search query",
                limit: limits::MAX_QUERY_BYTES,
                actual: query.len(),
            });
        }
        let limit = limit.min(limits::MAX_SEARCH_RESULTS);
        let match_expr = literal_match_expression(query);
        if match_expr.is_empty() {
            return Ok(Vec::new());
        }

        let mut stmt = self
            .conn
            .prepare(
                "SELECT o.id, o.rel_path, o.title, o.project
                 FROM object_fts f
                 JOIN object o ON o.id = f.id
                 WHERE object_fts MATCH ?1
                 ORDER BY rank, o.id
                 LIMIT ?2",
            )
            .map_err(|e| Error::Derived(format!("cannot prepare search: {e}")))?;

        let rows = stmt
            .query_map(rusqlite::params![match_expr, limit as i64], |r| {
                Ok((
                    r.get::<_, String>(0)?,
                    r.get::<_, String>(1)?,
                    r.get::<_, Option<String>>(2)?,
                    r.get::<_, Option<String>>(3)?,
                ))
            })
            .map_err(|e| Error::Derived(format!("cannot run search: {e}")))?;

        let mut out = Vec::new();
        for row in rows {
            let (id, rel_path, title, project) =
                row.map_err(|e| Error::Derived(format!("bad search row: {e}")))?;
            out.push(Candidate {
                id: ObjectId::parse(&id)?,
                rel_path,
                title,
                project_hint: project,
            });
        }
        Ok(out)
    }

    /// Read the **authoritative** project for an object — from canonical state.
    ///
    /// This deliberately does not consult the index. E §12.2: derived scope columns
    /// may accelerate matching, never be the sole authority. K-16 poisons the index
    /// and asserts this path is unaffected.
    pub fn authoritative_project(
        &self,
        vault: &Vault,
        id: ObjectId,
        rel_path_hint: &str,
    ) -> Result<Option<String>> {
        let content = crate::locator::read_verified(vault.root(), rel_path_hint, id)?;
        let parsed = crate::identity::parse(&content)?;
        Ok(parsed.frontmatter.project)
    }

    pub fn object_count(&self) -> Result<usize> {
        self.conn
            .query_row("SELECT COUNT(*) FROM object", [], |r| r.get::<_, i64>(0))
            .map(|n| n as usize)
            .map_err(|e| Error::Derived(format!("cannot count: {e}")))
    }
}

/// Build an FTS5 `MATCH` expression that treats input as **literal text**.
///
/// This is not SQL parameterisation. Parameter binding protects the *statement*;
/// the right-hand side of `MATCH` is then interpreted by FTS5's own query language,
/// so a bound parameter carrying `foo OR bar`, `title:secret` or `NEAR(a b)` is
/// passed through as **syntax**.
///
/// Each token is wrapped in double quotes and internal quotes are doubled, which is
/// FTS5's own escape for a literal string. Operators, column filters and prefix
/// syntax therefore cannot activate.
fn literal_match_expression(query: &str) -> String {
    query
        .split_whitespace()
        .filter(|t| !t.is_empty())
        .map(|t| {
            let escaped = t.replace('"', "\"\"");
            format!("\"{escaped}\"")
        })
        .collect::<Vec<_>>()
        .join(" ")
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    fn tmp() -> PathBuf {
        let d = std::env::temp_dir().join(format!("fehrest-drv-{}", uuid::Uuid::now_v7()));
        std::fs::create_dir_all(&d).unwrap();
        d
    }

    fn rec(id: ObjectId, path: &str, project: Option<&str>, body: &str) -> ObjectRecord {
        ObjectRecord {
            id,
            rel_path: path.into(),
            title: Some(path.into()),
            project: project.map(str::to_string),
            content_hash: "h".into(),
            body: body.into(),
        }
    }

    #[test]
    fn hardening_pragmas_are_applied() {
        let d = tmp();
        let der = Derived::open(&d).unwrap();
        let trusted: i64 = der
            .conn
            .query_row("PRAGMA trusted_schema", [], |r| r.get(0))
            .unwrap();
        assert_eq!(trusted, 0, "trusted_schema must be OFF");
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn extension_loading_is_unavailable() {
        // The load_extension SQL function must not exist. With the feature not
        // compiled in, SQLite rejects the call rather than loading anything.
        let d = tmp();
        let der = Derived::open(&d).unwrap();
        let r = der
            .conn
            .execute("SELECT load_extension('evil')", []);
        assert!(r.is_err(), "load_extension must not be callable");
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn rebuild_is_deterministic_across_independent_builds() {
        // Not B-12: this compares rebuild-vs-rebuild, not incremental-vs-fresh.
        // The incremental arm does not exist (YAGNI_DEFERRED), and analyze.md A-01
        // records that B-12 therefore cannot run.
        let objs = vec![
            rec(ObjectId::generate(), "a.md", Some("p"), "alpha beta"),
            rec(ObjectId::generate(), "b.md", Some("p"), "beta gamma"),
        ];
        let d1 = tmp();
        let d2 = tmp();
        let x = Derived::open(&d1).unwrap();
        let y = Derived::open(&d2).unwrap();
        x.rebuild(&objs).unwrap();
        y.rebuild(&objs).unwrap();
        assert_eq!(x.search("beta", 10).unwrap(), y.search("beta", 10).unwrap());
        let _ = std::fs::remove_dir_all(&d1);
        let _ = std::fs::remove_dir_all(&d2);
    }

    #[test]
    fn literal_query_cannot_activate_fts_syntax() {
        // Each of these is FTS5 syntax. As literal text they must match nothing
        // special, and must not error or broaden the result set.
        for hostile in [
            "alpha OR beta",
            "title:secret",
            "NEAR(alpha beta)",
            "alph*",
            "alpha AND NOT beta",
            "\"unbalanced",
            "^alpha",
        ] {
            let expr = literal_match_expression(hostile);
            assert!(
                !expr.contains(" OR ") || expr.contains("\"OR\""),
                "operator must be quoted in {expr}"
            );
            assert!(
                !expr.contains("title:") || expr.contains("\"title:secret\""),
                "column filter must be quoted in {expr}"
            );
        }
    }

    #[test]
    fn hostile_query_returns_no_results_rather_than_erroring() {
        let d = tmp();
        let der = Derived::open(&d).unwrap();
        let id = ObjectId::generate();
        der.rebuild(&[rec(id, "a.md", None, "alpha beta")]).unwrap();

        // "alpha OR beta" as literal text matches nothing, because no document
        // contains the literal token "OR" adjacent to those words.
        let hits = der.search("alpha OR beta", 10).unwrap();
        assert!(hits.is_empty(), "literal operator must not broaden results");

        // The plain term still works.
        assert_eq!(der.search("alpha", 10).unwrap().len(), 1);
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn query_and_result_bounds_are_enforced() {
        let d = tmp();
        let der = Derived::open(&d).unwrap();
        let big = "x".repeat(limits::MAX_QUERY_BYTES + 1);
        assert!(matches!(
            der.search(&big, 10),
            Err(Error::LimitExceeded { .. })
        ));

        let objs: Vec<_> = (0..50)
            .map(|i| rec(ObjectId::generate(), &format!("f{i}.md"), None, "common"))
            .collect();
        der.rebuild(&objs).unwrap();
        assert_eq!(der.search("common", 5).unwrap().len(), 5);
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn empty_query_returns_nothing() {
        let d = tmp();
        let der = Derived::open(&d).unwrap();
        der.rebuild(&[rec(ObjectId::generate(), "a.md", None, "x")])
            .unwrap();
        assert!(der.search("   ", 10).unwrap().is_empty());
        let _ = std::fs::remove_dir_all(&d);
    }
}
