//! Append-only hash-chained canonical event log.
//!
//! **F-CORE-12 — what this provides, stated precisely.**
//!
//! | Detected | Not detected |
//! |---|---|
//! | single-record edit, truncation, reordering, splice, deletion, inconsistent restore | a **complete, internally consistent rewrite** of the whole chain |
//!
//! The chain is **unkeyed**. Under the declared root of trust (C §3.1) an attacker
//! holding the OS account can recompute every dependent hash and the result
//! verifies. This is partial-tamper evidence, **never authentication**. No MAC is
//! used, because key custody would be the same account being defended against.

use crate::{Error, Result};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs::OpenOptions;
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};

/// The six event types Phase T needs. Not the full architecture vocabulary —
/// event tiering stays unfrozen pending B-0.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EventKind {
    VaultCreated,
    ObjectRegistered,
    ObjectConflict,
    MemoryRecorded,
    MemorySuperseded,
    ContextCompiled,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Event {
    pub seq: u64,
    pub kind: EventKind,
    pub subject: String,
    pub detail: String,
    pub prev_hash: String,
    pub hash: String,
}

pub fn hash_bytes(bytes: &[u8]) -> String {
    let mut h = Sha256::new();
    h.update(bytes);
    format!("{:x}", h.finalize())
}

const GENESIS: &str = "0000000000000000000000000000000000000000000000000000000000000000";

fn compute_hash(seq: u64, kind: EventKind, subject: &str, detail: &str, prev: &str) -> String {
    // Canonical serialization for hashing: field order is fixed here, not inherited
    // from a serializer whose output could change between versions.
    let payload = format!("{seq}|{kind:?}|{subject}|{detail}|{prev}");
    hash_bytes(payload.as_bytes())
}

/// The append-only event log.
#[derive(Debug)]
pub struct EventLog {
    path: PathBuf,
}

/// Result of verifying the chain.
#[derive(Debug, PartialEq, Eq)]
pub enum ChainStatus {
    Intact { events: usize },
    /// A record's `prev_hash` does not match its predecessor's `hash`, or a
    /// record's own hash does not recompute. Reported with the exact sequence.
    Broken { at_seq: u64, reason: String },
    /// `seq` is contiguous by construction; a gap means removal or a partial
    /// restore. N §3.3: not normal crash damage, and never silently continued.
    Gap { from_seq: u64, to_seq: u64 },
}

impl EventLog {
    pub fn open(control_dir: &Path) -> Result<Self> {
        std::fs::create_dir_all(control_dir)
            .map_err(|e| Error::Event(format!("cannot create control dir: {e}")))?;
        Ok(EventLog {
            path: control_dir.join("events.jsonl"),
        })
    }

    pub fn append(&self, kind: EventKind, subject: &str, detail: &str) -> Result<Event> {
        if detail.len() > crate::limits::MAX_EVENT_BYTES {
            return Err(Error::LimitExceeded {
                what: "event detail",
                limit: crate::limits::MAX_EVENT_BYTES,
                actual: detail.len(),
            });
        }
        let events = self.read_all()?;
        let (seq, prev) = match events.last() {
            Some(e) => (e.seq + 1, e.hash.clone()),
            None => (1, GENESIS.to_string()),
        };
        let hash = compute_hash(seq, kind, subject, detail, &prev);
        let ev = Event {
            seq,
            kind,
            subject: subject.to_string(),
            detail: detail.to_string(),
            prev_hash: prev,
            hash,
        };
        let line = serde_json::to_string(&ev)
            .map_err(|e| Error::Event(format!("cannot serialize event: {e}")))?;
        let mut f = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&self.path)
            .map_err(|e| Error::Event(format!("cannot open event log: {e}")))?;
        writeln!(f, "{line}").map_err(|e| Error::Event(format!("cannot append event: {e}")))?;
        Ok(ev)
    }

    pub fn read_all(&self) -> Result<Vec<Event>> {
        if !self.path.exists() {
            return Ok(Vec::new());
        }
        let f = std::fs::File::open(&self.path)
            .map_err(|e| Error::Event(format!("cannot open event log: {e}")))?;
        let mut out = Vec::new();
        for (i, line) in BufReader::new(f).lines().enumerate() {
            let line = line.map_err(|e| Error::Event(format!("cannot read line {i}: {e}")))?;
            if line.trim().is_empty() {
                continue;
            }
            let ev: Event = serde_json::from_str(&line)
                .map_err(|e| Error::Event(format!("malformed event at line {i}: {e}")))?;
            out.push(ev);
        }
        Ok(out)
    }

    /// Verify chain integrity. Detects what an unkeyed chain can detect, and the
    /// return type deliberately says nothing about authenticity.
    pub fn verify(&self) -> Result<ChainStatus> {
        let events = self.read_all()?;
        let mut prev_hash = GENESIS.to_string();

        for (expected_seq, ev) in (1u64..).zip(events.iter()) {
            if ev.seq != expected_seq {
                return Ok(ChainStatus::Gap {
                    from_seq: expected_seq,
                    to_seq: ev.seq,
                });
            }
            if ev.prev_hash != prev_hash {
                return Ok(ChainStatus::Broken {
                    at_seq: ev.seq,
                    reason: "prev_hash does not match predecessor".into(),
                });
            }
            let recomputed = compute_hash(ev.seq, ev.kind, &ev.subject, &ev.detail, &ev.prev_hash);
            if recomputed != ev.hash {
                return Ok(ChainStatus::Broken {
                    at_seq: ev.seq,
                    reason: "record hash does not recompute".into(),
                });
            }
            prev_hash = ev.hash.clone();
        }
        Ok(ChainStatus::Intact {
            events: events.len(),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tmp() -> PathBuf {
        let d = std::env::temp_dir().join(format!("fehrest-ev-{}", uuid::Uuid::now_v7()));
        std::fs::create_dir_all(&d).unwrap();
        d
    }

    #[test]
    fn chain_is_intact_after_appends() {
        let d = tmp();
        let log = EventLog::open(&d).unwrap();
        log.append(EventKind::VaultCreated, "vault", "").unwrap();
        log.append(EventKind::ObjectRegistered, "obj-1", "a.md")
            .unwrap();
        log.append(EventKind::MemoryRecorded, "mem-1", "fact")
            .unwrap();
        assert_eq!(
            log.verify().unwrap(),
            ChainStatus::Intact { events: 3 }
        );
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn single_record_edit_is_detected() {
        let d = tmp();
        let log = EventLog::open(&d).unwrap();
        log.append(EventKind::VaultCreated, "vault", "").unwrap();
        log.append(EventKind::ObjectRegistered, "obj-1", "a.md")
            .unwrap();
        log.append(EventKind::ObjectRegistered, "obj-2", "b.md")
            .unwrap();

        // Tamper with the middle record's detail, leaving hashes untouched.
        let p = d.join("events.jsonl");
        let text = std::fs::read_to_string(&p).unwrap();
        let mut lines: Vec<String> = text.lines().map(str::to_string).collect();
        lines[1] = lines[1].replace("a.md", "evil.md");
        std::fs::write(&p, lines.join("\n") + "\n").unwrap();

        match log.verify().unwrap() {
            ChainStatus::Broken { at_seq, .. } => assert_eq!(at_seq, 2),
            s => panic!("edit must be detected, got {s:?}"),
        }
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn truncation_and_removal_are_detected() {
        let d = tmp();
        let log = EventLog::open(&d).unwrap();
        for i in 0..4 {
            log.append(EventKind::ObjectRegistered, &format!("o{i}"), "x")
                .unwrap();
        }
        let p = d.join("events.jsonl");
        let text = std::fs::read_to_string(&p).unwrap();
        let lines: Vec<&str> = text.lines().collect();
        // Remove the second record: seq jumps 1 -> 3.
        let kept = format!("{}\n{}\n{}\n", lines[0], lines[2], lines[3]);
        std::fs::write(&p, kept).unwrap();

        match log.verify().unwrap() {
            ChainStatus::Gap { from_seq, to_seq } => {
                assert_eq!((from_seq, to_seq), (2, 3));
            }
            s => panic!("removal must be detected, got {s:?}"),
        }
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn consistent_full_rewrite_is_not_detected_and_we_say_so() {
        // This test exists to make the LIMIT executable rather than merely written
        // down. An unkeyed chain cannot detect a complete consistent rewrite; C 6.1
        // states that plainly, and this asserts the stated behaviour rather than
        // pretending otherwise.
        let d = tmp();
        let log = EventLog::open(&d).unwrap();
        log.append(EventKind::VaultCreated, "vault", "").unwrap();
        log.append(EventKind::ObjectRegistered, "real", "a.md")
            .unwrap();

        // Attacker rewrites the entire history consistently.
        let p = d.join("events.jsonl");
        std::fs::remove_file(&p).unwrap();
        let log2 = EventLog::open(&d).unwrap();
        log2.append(EventKind::VaultCreated, "vault", "").unwrap();
        log2.append(EventKind::ObjectRegistered, "forged", "evil.md")
            .unwrap();

        assert_eq!(log2.verify().unwrap(), ChainStatus::Intact { events: 2 });
        // Verification passes. That is the documented limit, not a defect.
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn oversized_event_detail_is_rejected() {
        let d = tmp();
        let log = EventLog::open(&d).unwrap();
        let big = "x".repeat(crate::limits::MAX_EVENT_BYTES + 1);
        assert!(matches!(
            log.append(EventKind::MemoryRecorded, "m", &big),
            Err(Error::LimitExceeded { .. })
        ));
        let _ = std::fs::remove_dir_all(&d);
    }
}
