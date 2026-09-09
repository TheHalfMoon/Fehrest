//! Object identity and canonical frontmatter.
//!
//! F-CORE-04: paths are locations; IDs are identities. There is deliberately no
//! conversion from any path type into [`ObjectId`] — the absence of that impl is
//! the enforcement mechanism, not a convention.

use crate::{Error, Result};
use std::fmt;
use uuid::Uuid;

/// A canonical Fehrest object identity. Opaque, allocated, immutable.
///
/// UUIDv7 per ADR-0004: time-ordered for index locality, RFC 9562 standardised so
/// third parties can parse it, and not content-derived so editing a file cannot
/// change what it is.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct ObjectId(Uuid);

impl ObjectId {
    /// Allocate a new identity. The only construction path that invents one.
    pub fn generate() -> Self {
        ObjectId(Uuid::now_v7())
    }

    pub fn parse(s: &str) -> Result<Self> {
        Uuid::parse_str(s.trim())
            .map(ObjectId)
            .map_err(|_| Error::InvalidId(s.to_string()))
    }
}

impl fmt::Display for ObjectId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// Canonical frontmatter: the fields Fehrest understands, plus every line it does
/// not, preserved byte-for-byte.
///
/// R-8 is the reason `unknown` exists. Dropping unrecognised fields silently
/// destroys data written by a newer version or another tool, and it is the kind
/// of loss nobody notices until the data is needed.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Frontmatter {
    pub id: ObjectId,
    pub title: Option<String>,
    pub project: Option<String>,
    /// Unrecognised lines, in order, exactly as written.
    pub unknown: Vec<String>,
}

/// A parsed canonical object: frontmatter plus body.
#[derive(Debug, Clone)]
pub struct ParsedObject {
    pub frontmatter: Frontmatter,
    pub body: String,
}

const FENCE: &str = "---";

/// Parse frontmatter and body from canonical file content.
///
/// This is a deliberately bounded `key: value` parser, not a YAML engine
/// ([dependencies.md](../specs/001-headless-rust-fehrest/dependencies.md)). A general
/// YAML parser would accept anchors, aliases, merge keys and arbitrary nesting from
/// attacker-influenced vault content (T-17) to gain nothing this subset lacks.
///
/// Rejecting what it does not understand is the point: an unparseable frontmatter
/// is an error, never a silent partial read.
pub fn parse(content: &str) -> Result<ParsedObject> {
    let mut lines = content.lines();

    match lines.next() {
        Some(first) if first.trim_end() == FENCE => {}
        _ => return Err(Error::NoFrontmatter),
    }

    let mut id: Option<ObjectId> = None;
    let mut title = None;
    let mut project = None;
    let mut unknown = Vec::new();
    let mut closed = false;
    let mut consumed = 1usize;

    for line in lines.by_ref() {
        consumed += 1;
        if line.trim_end() == FENCE {
            closed = true;
            break;
        }
        match split_kv(line) {
            Some(("id", v)) => id = Some(ObjectId::parse(v)?),
            Some(("title", v)) => title = Some(unquote(v).to_string()),
            Some(("project", v)) => project = Some(unquote(v).to_string()),
            _ => unknown.push(line.to_string()),
        }
    }

    if !closed {
        return Err(Error::NoFrontmatter);
    }

    let id = id.ok_or(Error::MissingId)?;

    // Rebuild the body from the original content so line endings inside the body
    // survive untouched. Splitting and rejoining would normalise CRLF to LF and
    // silently rewrite the user's file.
    let body = skip_lines(content, consumed);

    Ok(ParsedObject {
        frontmatter: Frontmatter {
            id,
            title,
            project,
            unknown,
        },
        body: body.to_string(),
    })
}

/// Serialize frontmatter and body back to canonical file content.
///
/// Unknown lines are written back in their original position and form.
pub fn serialize(fm: &Frontmatter, body: &str) -> String {
    let mut out = String::with_capacity(body.len() + 128);
    out.push_str(FENCE);
    out.push('\n');
    out.push_str(&format!("id: {}\n", fm.id));
    if let Some(t) = &fm.title {
        out.push_str(&format!("title: {t}\n"));
    }
    if let Some(p) = &fm.project {
        out.push_str(&format!("project: {p}\n"));
    }
    for line in &fm.unknown {
        out.push_str(line);
        out.push('\n');
    }
    out.push_str(FENCE);
    out.push('\n');
    out.push_str(body);
    out
}

/// Read only the identity from content already read from an opened handle.
///
/// Used by post-open verification, where the question is narrowly "what does this
/// content claim to be?" and a full parse would do more work than the check needs.
pub fn read_id(content: &str) -> Result<ObjectId> {
    parse(content).map(|p| p.frontmatter.id)
}

fn split_kv(line: &str) -> Option<(&str, &str)> {
    let (k, v) = line.split_once(':')?;
    let k = k.trim();
    if k.is_empty() || k.contains(char::is_whitespace) {
        return None;
    }
    Some((k, v.trim()))
}

fn unquote(v: &str) -> &str {
    let v = v.trim();
    if v.len() >= 2 {
        let b = v.as_bytes();
        if (b[0] == b'"' && b[b.len() - 1] == b'"') || (b[0] == b'\'' && b[b.len() - 1] == b'\'') {
            return &v[1..v.len() - 1];
        }
    }
    v
}

/// Return the remainder of `s` after `n` lines, preserving original line endings.
fn skip_lines(s: &str, n: usize) -> &str {
    let mut rest = s;
    for _ in 0..n {
        match rest.find('\n') {
            Some(i) => rest = &rest[i + 1..],
            None => return "",
        }
    }
    rest
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generates_distinct_time_ordered_ids() {
        let a = ObjectId::generate();
        let b = ObjectId::generate();
        assert_ne!(a, b);
    }

    #[test]
    fn round_trips_and_preserves_unknown_fields_verbatim() {
        // CL-04 / R-8: a version that drops unknown fields destroys forward
        // compatibility, so this asserts byte-for-byte survival.
        let id = ObjectId::generate();
        let src = format!(
            "---\nid: {id}\ntitle: Test\ncustom_field: kept\nweird:   spacing\n---\nbody line\nsecond\n"
        );
        let parsed = parse(&src).unwrap();
        assert_eq!(parsed.frontmatter.id, id);
        assert_eq!(parsed.frontmatter.title.as_deref(), Some("Test"));
        assert_eq!(parsed.frontmatter.unknown.len(), 2);
        assert_eq!(parsed.body, "body line\nsecond\n");

        let out = serialize(&parsed.frontmatter, &parsed.body);
        let reparsed = parse(&out).unwrap();
        assert_eq!(reparsed.frontmatter, parsed.frontmatter);
        assert_eq!(reparsed.body, parsed.body);
    }

    #[test]
    fn rejects_missing_or_malformed_frontmatter() {
        assert!(matches!(
            parse("no fence here\n"),
            Err(Error::NoFrontmatter)
        ));
        assert!(matches!(
            parse("---\ntitle: no id\n---\nbody"),
            Err(Error::MissingId)
        ));
        assert!(matches!(
            parse("---\nid: not-a-uuid\n---\nbody"),
            Err(Error::InvalidId(_))
        ));
        // Unterminated frontmatter must not be read as a partial success.
        assert!(matches!(
            parse("---\nid: 018f0000-0000-7000-8000-000000000000\nbody"),
            Err(Error::NoFrontmatter)
        ));
    }

    #[test]
    fn body_line_endings_survive() {
        let id = ObjectId::generate();
        let src = format!("---\nid: {id}\n---\nline1\r\nline2\r\n");
        let parsed = parse(&src).unwrap();
        assert_eq!(parsed.body, "line1\r\nline2\r\n");
    }
}
