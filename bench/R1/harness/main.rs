//! R1 — longitudinal continuation benchmark harness.
//!
//! **This harness cannot produce a thesis result on its own.** It builds arm
//! packages, enforces the temporal evidence boundary, emits a sealed run bundle and
//! scores model responses. The scoring input must come from an actual model. There
//! is no code path here that invents a model response, and `selftest` refuses to
//! print an arm score.
//!
//! What it does establish, without a model:
//!
//! - that no arm package at `Ti` contains vocabulary that first appears after `Ti`;
//! - that every task's answer is derivable from evidence available at its checkpoint;
//! - that every distractor a task punishes actually exists in the corpus;
//! - that baseline arms never receive Fehrest metadata;
//! - that the scorer rewards a correct answer, rejects a stale one, and gives an
//!   empty output no credit on any task type, including abstention.
//!
//! Those are instrument properties. None of them is evidence about Fehrest.

use fehrest::context::{self, CompileRequest, SourceItem};
use fehrest::derived::Derived;
use fehrest::envelope::TrustLevel;
use fehrest::events::hash_bytes;
use fehrest::memory::{Basis, Lifecycle, Memory, MemoryType, Resolution, Scope};
use fehrest::vault::Vault;
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

/// Identical for every arm. Preregistered; see `PREREGISTRATION.md` §4.
const BUDGET_BYTES: usize = 6_000;
const VAULT_NAME: &str = "r1";

// ---------------------------------------------------------------------------
// Scenario model
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
struct Evidence {
    path: String,
    kind: String,
    title: String,
    body: String,
}

#[derive(Debug, Clone)]
struct Checkpoint {
    t: usize,
    day: i64,
    evidence: Vec<Evidence>,
}

#[derive(Debug, Clone)]
struct Scenario {
    id: String,
    name: String,
    project: String,
    checkpoints: Vec<Checkpoint>,
}

impl Scenario {
    /// Evidence visible at `t`, newest checkpoint last.
    fn upto(&self, t: usize) -> Vec<(&Checkpoint, &Evidence)> {
        let mut out = Vec::new();
        for cp in self.checkpoints.iter().filter(|c| c.t <= t) {
            for e in &cp.evidence {
                out.push((cp, e));
            }
        }
        out
    }

    /// Evidence introduced strictly after `t`. Used only by the leakage assertion.
    fn after(&self, t: usize) -> Vec<&Evidence> {
        self.checkpoints
            .iter()
            .filter(|c| c.t > t)
            .flat_map(|c| c.evidence.iter())
            .collect()
    }

    fn day_at(&self, t: usize) -> i64 {
        self.checkpoints
            .iter()
            .filter(|c| c.t <= t)
            .map(|c| c.day)
            .max()
            .unwrap_or(0)
    }
}

fn kv(seg: &str) -> (String, String) {
    match seg.split_once('=') {
        Some((k, v)) => (k.trim().to_string(), v.trim().to_string()),
        None => (seg.trim().to_string(), String::new()),
    }
}

fn parse_scenario(text: &str) -> Scenario {
    let mut id = String::new();
    let mut name = String::new();
    let mut project = String::new();
    let mut checkpoints: Vec<Checkpoint> = Vec::new();
    let mut pending: Option<Evidence> = None;
    let mut body = String::new();

    for line in text.lines() {
        if let Some(rest) = line.strip_prefix("SCENARIO ") {
            let mut parts = rest.split('|');
            id = parts.next().unwrap_or("").trim().to_string();
            for p in parts {
                let (k, v) = kv(p);
                match k.as_str() {
                    "name" => name = v,
                    "project" => project = v,
                    _ => {}
                }
            }
        } else if let Some(rest) = line.strip_prefix("CHECKPOINT ") {
            let mut t = 0usize;
            let mut day = 0i64;
            for p in rest.split('|') {
                let (k, v) = kv(p);
                match k.as_str() {
                    "t" => t = v.parse().unwrap_or(0),
                    "day" => day = v.parse().unwrap_or(0),
                    _ => {}
                }
            }
            checkpoints.push(Checkpoint {
                t,
                day,
                evidence: Vec::new(),
            });
        } else if let Some(rest) = line.strip_prefix("EVIDENCE ") {
            let mut parts = rest.split('|');
            let path = parts.next().unwrap_or("").trim().to_string();
            let mut kind = "doc".to_string();
            let mut title = String::new();
            for p in parts {
                let (k, v) = kv(p);
                match k.as_str() {
                    "kind" => kind = v,
                    "title" => title = v,
                    _ => {}
                }
            }
            pending = Some(Evidence {
                path,
                kind,
                title,
                body: String::new(),
            });
            body.clear();
        } else if line.trim() == "ENDEVIDENCE" {
            if let Some(mut e) = pending.take() {
                e.body = body.trim_end().to_string();
                if let Some(cp) = checkpoints.last_mut() {
                    cp.evidence.push(e);
                }
            }
            body.clear();
        } else if pending.is_some() {
            body.push_str(line);
            body.push('\n');
        }
    }

    Scenario {
        id,
        name,
        project,
        checkpoints,
    }
}

fn load_scenarios(dir: &Path) -> Vec<Scenario> {
    let mut files: Vec<PathBuf> = fs::read_dir(dir)
        .expect("scenarios dir must exist")
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|p| p.extension().and_then(|s| s.to_str()) == Some("scn"))
        .collect();
    files.sort();
    files
        .iter()
        .map(|p| parse_scenario(&fs::read_to_string(p).expect("scenario readable")))
        .collect()
}

// ---------------------------------------------------------------------------
// Tasks and oracles
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
struct Task {
    task_id: String,
    scenario: String,
    checkpoint: usize,
    class: String,
    kind: String,
    prompt: String,
}

#[derive(Debug, Clone)]
struct Check {
    field: String,
    any: Vec<String>,
}

#[derive(Debug, Clone)]
struct Oracle {
    task_id: String,
    abstain_required: bool,
    require_all: Vec<Check>,
    forbid: Vec<Check>,
    min_action_chars: usize,
    derivable_from: Vec<String>,
    trap_present: Vec<String>,
}

fn str_list(v: &serde_json::Value) -> Vec<String> {
    v.as_array()
        .map(|a| {
            a.iter()
                .filter_map(|s| s.as_str().map(str::to_string))
                .collect()
        })
        .unwrap_or_default()
}

fn checks(v: &serde_json::Value) -> Vec<Check> {
    v.as_array()
        .map(|a| {
            a.iter()
                .map(|c| Check {
                    field: c["field"].as_str().unwrap_or("").to_uppercase(),
                    any: str_list(&c["any"]),
                })
                .collect()
        })
        .unwrap_or_default()
}

fn load_tasks(path: &Path) -> (String, Vec<Task>) {
    let v: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(path).expect("tasks readable"))
            .expect("tasks parse");
    let contract = v["output_contract"].as_str().unwrap_or("").to_string();
    let tasks = v["tasks"]
        .as_array()
        .expect("tasks array")
        .iter()
        .map(|t| Task {
            task_id: t["task_id"].as_str().unwrap_or("").to_string(),
            scenario: t["scenario"].as_str().unwrap_or("").to_string(),
            checkpoint: t["checkpoint"].as_u64().unwrap_or(0) as usize,
            class: t["class"].as_str().unwrap_or("").to_string(),
            kind: t["kind"].as_str().unwrap_or("continuation").to_string(),
            prompt: t["prompt"].as_str().unwrap_or("").to_string(),
        })
        .collect();
    (contract, tasks)
}

fn load_oracles(path: &Path) -> BTreeMap<String, Oracle> {
    let v: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(path).expect("oracles readable"))
            .expect("oracles parse");
    v["oracles"]
        .as_array()
        .expect("oracles array")
        .iter()
        .map(|o| {
            let id = o["task_id"].as_str().unwrap_or("").to_string();
            (
                id.clone(),
                Oracle {
                    task_id: id,
                    abstain_required: o["abstain_required"].as_bool().unwrap_or(false),
                    require_all: checks(&o["require_all"]),
                    forbid: checks(&o["forbid"]),
                    min_action_chars: o["min_action_chars"].as_u64().unwrap_or(20) as usize,
                    derivable_from: str_list(&o["derivable_from"]),
                    trap_present: str_list(&o["trap_present"]),
                },
            )
        })
        .collect()
}

// ---------------------------------------------------------------------------
// Maintained state — produced by a maintainer model, folded from per-checkpoint ops
// ---------------------------------------------------------------------------

/// One arm's maintained artefact at a checkpoint, plus what it cost to get there.
#[derive(Debug, Default, Clone)]
struct Maintained {
    /// B1 repository-native documents, path -> body.
    files: BTreeMap<String, String>,
    /// B4 single wiki page.
    wiki: String,
    /// B5 memory set, folded from ops.
    memories: Vec<Memory>,
    /// Cumulative maintenance cost through this checkpoint.
    cost: Cost,
    /// True when no maintainer output exists for this arm/scenario.
    absent: bool,
}

#[derive(Debug, Default, Clone, Copy)]
struct Cost {
    actions: usize,
    objects_touched: usize,
    input_bytes: usize,
    output_bytes: usize,
}

fn mtype(s: &str) -> MemoryType {
    match s.to_ascii_lowercase().as_str() {
        "decision" => MemoryType::Decision,
        "constraint" => MemoryType::Constraint,
        "gotcha" => MemoryType::Gotcha,
        "state" => MemoryType::State,
        _ => MemoryType::Fact,
    }
}

/// Fold maintenance ops for checkpoints `0..=t` into arm state.
///
/// `Basis` is **always** `AgentAsserted`. A maintainer cannot mint user authority;
/// that is core-assigned and K-21 asserts it. The maintenance schema deliberately
/// has no field for it.
fn fold_maintenance(state_dir: &Path, arm: Arm, scn: &Scenario, t: usize) -> Maintained {
    let mut m = Maintained::default();
    let mut seen_any = false;
    let mut by_id: BTreeMap<String, Memory> = BTreeMap::new();
    let mut seq: u64 = 0;

    for cp in scn.checkpoints.iter().filter(|c| c.t <= t) {
        let p = state_dir
            .join(arm.dir())
            .join(&scn.id)
            .join(format!("t{:02}.json", cp.t));
        let Ok(text) = fs::read_to_string(&p) else {
            continue;
        };
        seen_any = true;
        let Ok(v) = serde_json::from_str::<serde_json::Value>(&text) else {
            continue;
        };

        m.cost.input_bytes += v["evidence_bytes_seen"].as_u64().unwrap_or(0) as usize;
        m.cost.output_bytes += text.len();

        match arm {
            Arm::B1 => {
                for f in v["files"].as_array().unwrap_or(&Vec::new()) {
                    let path = f["path"].as_str().unwrap_or("").to_string();
                    let body = f["body"].as_str().unwrap_or("").to_string();
                    if path.is_empty() {
                        continue;
                    }
                    m.files.insert(path, body);
                    m.cost.actions += 1;
                    m.cost.objects_touched += 1;
                }
            }
            Arm::B4 => {
                if let Some(w) = v["wiki"].as_str() {
                    m.wiki = w.to_string();
                    m.cost.actions += 1;
                    m.cost.objects_touched += 1;
                }
            }
            Arm::B5 => {
                for op in v["memories"].as_array().unwrap_or(&Vec::new()) {
                    let kind = op["op"].as_str().unwrap_or("add");
                    let id = op["id"].as_str().unwrap_or("").to_string();
                    if id.is_empty() {
                        continue;
                    }
                    m.cost.actions += 1;
                    match kind {
                        "add" => {
                            seq += 1;
                            let project = op["project"].as_str().unwrap_or(&scn.project);
                            let Ok(mut rec) = Memory::new(
                                id.clone(),
                                op["statement"].as_str().unwrap_or(""),
                                mtype(op["mtype"].as_str().unwrap_or("fact")),
                                Basis::AgentAsserted,
                                Scope::project(VAULT_NAME, project),
                                seq,
                                op["valid_from"].as_i64().unwrap_or(cp.day),
                            ) else {
                                continue;
                            };
                            if let Some(sup) = op["supersedes"].as_array() {
                                rec.supersedes = sup
                                    .iter()
                                    .filter_map(|s| s.as_str().map(str::to_string))
                                    .collect();
                            }
                            by_id.insert(id, rec);
                            m.cost.objects_touched += 1;
                        }
                        "supersede" => {
                            if let Some(rec) = by_id.get_mut(&id) {
                                rec.lifecycle = Lifecycle::Superseded;
                                rec.valid_until =
                                    Some(op["valid_until"].as_i64().unwrap_or(cp.day));
                                m.cost.objects_touched += 1;
                            }
                        }
                        "retract" => {
                            if let Some(rec) = by_id.get_mut(&id) {
                                rec.lifecycle = Lifecycle::Retracted;
                                m.cost.objects_touched += 1;
                            }
                        }
                        "conflict" => {
                            if let Some(rec) = by_id.get_mut(&id) {
                                rec.resolution = Resolution::Conflicted;
                                m.cost.objects_touched += 1;
                            }
                        }
                        _ => {}
                    }
                }
            }
            _ => {}
        }
    }

    m.memories = by_id.into_values().collect();
    m.absent = !seen_any;
    m
}

// ---------------------------------------------------------------------------
// Arms
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Arm {
    /// Calibration only. Task prompt with no project context. Never a comparison arm.
    BNull,
    B0,
    B1,
    B3,
    B4,
    B5,
}

impl Arm {
    fn id(self) -> &'static str {
        match self {
            Arm::BNull => "B-NULL",
            Arm::B0 => "B0",
            Arm::B1 => "B1",
            Arm::B3 => "B3",
            Arm::B4 => "B4",
            Arm::B5 => "B5",
        }
    }
    fn dir(self) -> &'static str {
        match self {
            Arm::BNull => "BNULL",
            Arm::B0 => "B0",
            Arm::B1 => "B1",
            Arm::B3 => "B3",
            Arm::B4 => "B4",
            Arm::B5 => "B5",
        }
    }
    fn maintained(self) -> bool {
        matches!(self, Arm::B1 | Arm::B4 | Arm::B5)
    }
}

const COMPARISON_ARMS: &[Arm] = &[Arm::B0, Arm::B1, Arm::B3, Arm::B4, Arm::B5];

/// Envelope markers that must never appear in a baseline arm's package.
const FEHREST_MARKERS: &[&str] = &[
    "<fehrest:item",
    "authority=",
    "trust_level=",
    "lifecycle=",
    "content_len=",
];

fn cut(mut s: String, budget: usize) -> String {
    if s.len() > budget {
        s.truncate(budget);
        while !s.is_char_boundary(s.len()) {
            s.pop();
        }
    }
    s
}

fn render(e: &Evidence) -> String {
    format!("--- {} [{}] ---\n{}\n\n", e.path, e.kind, e.body)
}

/// B0 — the plain project. Raw files, **newest checkpoint first**.
///
/// Recency ordering is deliberate and is the strongest simple heuristic available
/// without maintenance: an engineer dropped into an unfamiliar repository reads the
/// most recently changed material first. Path-order concatenation would have made
/// this arm needlessly weak, and a weakened baseline is not a baseline.
fn arm_b0(scn: &Scenario, t: usize) -> String {
    let mut items = scn.upto(t);
    items.reverse();
    let mut out = String::new();
    for (_, e) in items {
        let next = render(e);
        if out.len() + next.len() > BUDGET_BYTES {
            continue;
        }
        out.push_str(&next);
    }
    out
}

/// B1 — repository-native state documentation, then the raw project underneath it.
fn arm_b1(scn: &Scenario, t: usize, m: &Maintained) -> String {
    let mut out = String::new();
    for (path, body) in &m.files {
        let next = format!("--- {path} ---\n{body}\n\n");
        if out.len() + next.len() > BUDGET_BYTES {
            continue;
        }
        out.push_str(&next);
    }
    let mut items = scn.upto(t);
    items.reverse();
    for (_, e) in items {
        let next = render(e);
        if out.len() + next.len() > BUDGET_BYTES {
            continue;
        }
        out.push_str(&next);
    }
    out
}

const STOPWORDS: &[&str] = &[
    "what", "which", "does", "did", "the", "and", "for", "you", "your", "would", "state", "with",
    "that", "this", "from", "have", "has", "are", "was", "were", "will", "into", "them", "they",
    "their", "then", "than", "just", "picking", "asks", "ask", "take", "first", "next", "one",
    "line", "using", "answer", "identify", "concrete", "step", "item", "work", "project",
];

/// B3 — lexical retrieval over the same raw evidence, through the real index.
///
/// Ranked by distinct query-term hits, ties broken by recency. Raw document text
/// only: no envelope, no label, no memory record.
fn arm_b3(derived: &Derived, scn: &Scenario, t: usize, q: &str) -> String {
    let terms: Vec<String> = q
        .split_whitespace()
        .map(|w| {
            w.trim_matches(|c: char| !c.is_alphanumeric())
                .to_lowercase()
        })
        .filter(|w| w.len() > 2 && !STOPWORDS.contains(&w.as_str()))
        .collect();

    let mut hits: BTreeMap<String, usize> = BTreeMap::new();
    for term in &terms {
        for c in derived.search(term, 30).unwrap_or_default() {
            *hits.entry(c.rel_path.clone()).or_insert(0) += 1;
        }
    }

    // Recency rank for tie-breaking, from the scenario's own ordering.
    let order: BTreeMap<String, usize> = scn
        .upto(t)
        .iter()
        .enumerate()
        .map(|(i, (_, e))| (e.path.clone(), i))
        .collect();

    let mut ranked: Vec<(&String, usize)> = hits.iter().map(|(p, n)| (p, *n)).collect();
    ranked.sort_by(|a, b| {
        b.1.cmp(&a.1)
            .then(order.get(b.0).cmp(&order.get(a.0)))
            .then(a.0.cmp(b.0))
    });

    let by_path: BTreeMap<&str, &Evidence> = scn
        .upto(t)
        .iter()
        .map(|(_, e)| (e.path.as_str(), *e))
        .collect();

    let mut out = String::new();
    for (path, _) in ranked {
        let Some(e) = by_path.get(path.as_str()) else {
            continue;
        };
        let next = render(e);
        if out.len() + next.len() > BUDGET_BYTES {
            continue;
        }
        out.push_str(&next);
    }
    out
}

/// B4 — the maintained wiki page, and nothing else.
fn arm_b4(m: &Maintained) -> String {
    cut(m.wiki.clone(), BUDGET_BYTES)
}

/// B5 — Fehrest Core compiled package at the checkpoint's valid time.
fn arm_b5(scn: &Scenario, t: usize, m: &Maintained) -> String {
    let as_of = scn.day_at(t);
    let scope = Scope::project(VAULT_NAME, &scn.project);

    let mut items: Vec<SourceItem> = Vec::new();
    for rec in &m.memories {
        if !rec.scope.matches(&scope) {
            continue;
        }
        if rec.valid_from > as_of {
            continue;
        }
        if rec.valid_until.is_some_and(|u| u <= as_of) && rec.lifecycle != Lifecycle::Superseded {
            continue;
        }
        let closed = rec.valid_until.is_some_and(|u| u <= as_of);
        let section = match (rec.memory_type, closed, rec.resolution) {
            (_, _, Resolution::Conflicted) => "contradictions",
            (_, true, _) => "superseded_decisions",
            (MemoryType::Constraint, _, _) => "active_constraints",
            (MemoryType::Gotcha, _, _) => "gotchas",
            (MemoryType::Decision, _, _) => "current_decisions",
            _ => "project_state",
        };
        items.push(SourceItem {
            section,
            item_id: rec.id.0.clone(),
            content: rec.statement.clone(),
            source_content_hash: hash_bytes(rec.statement.as_bytes()),
            trust_level: TrustLevel::VaultKnowledge,
            memory: Some(rec.clone()),
            superseded_by: None,
        });
    }

    let req = CompileRequest {
        principal: "r1-bench".into(),
        scope,
        as_of_valid: as_of,
        as_of_recorded: u64::MAX,
        budget_bytes: BUDGET_BYTES,
    };
    context::compile(&req, &items).wire
}

// ---------------------------------------------------------------------------
// Response parsing and scoring
// ---------------------------------------------------------------------------

const FIELDS: &[&str] = &[
    "DECISION",
    "ACTION",
    "CONSTRAINTS_APPLIED",
    "EVIDENCE",
    "UNRESOLVED",
    "ABSTAIN",
];

fn parse_response(text: &str) -> BTreeMap<String, String> {
    let mut out: BTreeMap<String, String> = FIELDS
        .iter()
        .map(|f| ((*f).to_string(), String::new()))
        .collect();
    let mut current: Option<String> = None;
    for line in text.lines() {
        let mut matched = false;
        for f in FIELDS {
            let prefix = format!("{f}:");
            if line.trim_start().to_uppercase().starts_with(&prefix) {
                let value = line.trim_start()[prefix.len()..].trim().to_string();
                out.insert((*f).to_string(), value);
                current = Some((*f).to_string());
                matched = true;
                break;
            }
        }
        if !matched {
            // Continuation of a wrapped field value.
            if let Some(f) = &current {
                if !line.trim().is_empty() {
                    let e = out.get_mut(f).expect("field present");
                    e.push(' ');
                    e.push_str(line.trim());
                }
            }
        }
    }
    out
}

#[derive(Debug, Clone)]
struct TaskScore {
    task_id: String,
    class: String,
    kind: String,
    primary: bool,
    forbid_hit: bool,
    require_missing: usize,
    substantive: bool,
    abstained: bool,
    false_abstention: bool,
    conflict_flagged: bool,
    provenance_given: bool,
}

fn field_matches(fields: &BTreeMap<String, String>, c: &Check) -> bool {
    let hay = fields
        .get(&c.field)
        .cloned()
        .unwrap_or_default()
        .to_lowercase();
    c.any.iter().any(|n| hay.contains(&n.to_lowercase()))
}

/// The preregistered primary rule. See `PREREGISTRATION.md` §6.
///
/// An empty or unparseable response scores zero on **every** task type. Abstention
/// credit requires an explicit `ABSTAIN: YES` **and** a substantive `ACTION`, so
/// silence is never rewarded.
fn score_one(task: &Task, oracle: &Oracle, response: &str) -> TaskScore {
    let f = parse_response(response);
    let action = f.get("ACTION").cloned().unwrap_or_default();
    let action_chars = action.chars().filter(|c| !c.is_whitespace()).count();
    let substantive = action_chars >= oracle.min_action_chars;

    let abstained = f
        .get("ABSTAIN")
        .map(|v| v.to_uppercase().contains("YES"))
        .unwrap_or(false);

    let require_missing = oracle
        .require_all
        .iter()
        .filter(|c| !field_matches(&f, c))
        .count();
    let forbid_hit = oracle.forbid.iter().any(|c| field_matches(&f, c));

    let abstain_ok = if oracle.abstain_required {
        abstained
    } else {
        !abstained
    };

    let primary = substantive && require_missing == 0 && !forbid_hit && abstain_ok;

    let unresolved = f.get("UNRESOLVED").cloned().unwrap_or_default();
    let evidence = f.get("EVIDENCE").cloned().unwrap_or_default();

    TaskScore {
        task_id: task.task_id.clone(),
        class: task.class.clone(),
        kind: task.kind.clone(),
        primary,
        forbid_hit,
        require_missing,
        substantive,
        abstained,
        false_abstention: abstained && !oracle.abstain_required,
        conflict_flagged: !unresolved.trim().is_empty()
            && !unresolved.trim().eq_ignore_ascii_case("none"),
        provenance_given: !evidence.trim().is_empty()
            && !evidence.trim().eq_ignore_ascii_case("none"),
    }
}

// ---------------------------------------------------------------------------
// Instrument pilot
// ---------------------------------------------------------------------------

fn words(s: &str) -> BTreeSet<String> {
    s.split(|c: char| !c.is_alphanumeric() && c != '-' && c != '_')
        .map(|w| w.to_lowercase())
        .filter(|w| w.len() >= 6)
        .collect()
}

struct Checker {
    pass: usize,
    fail: usize,
    lines: Vec<String>,
    family: String,
    /// Per-family (passed, failed), in declaration order.
    families: Vec<(String, usize, usize)>,
}

impl Checker {
    fn new() -> Self {
        Checker {
            pass: 0,
            fail: 0,
            lines: Vec::new(),
            family: String::new(),
            families: Vec::new(),
        }
    }
    /// Open a check family. Printed as the section header, and counted, so the
    /// per-family totals in PILOT.md are measured rather than asserted.
    fn family(&mut self, name: &str) {
        println!("\n{name}");
        self.family = name.to_string();
        self.families.push((name.to_string(), 0, 0));
    }
    fn check(&mut self, name: &str, ok: bool, detail: &str) {
        if ok {
            self.pass += 1;
            if let Some(f) = self.families.last_mut() {
                f.1 += 1;
            }
            self.lines.push(format!("  PASS  {name}"));
        } else {
            self.fail += 1;
            if let Some(f) = self.families.last_mut() {
                f.2 += 1;
            }
            self.lines.push(format!("  FAIL  {name} -- {detail}"));
        }
    }
}

/// Deterministic placeholder maintenance so the package pipeline can be exercised.
///
/// **This is plumbing, not an arm.** It is task-blind and mechanical, it is not a
/// maintenance strategy any real maintainer would use, and no score computed over it
/// is reported as an arm result. Its only job is to make B1/B4/B5 produce a
/// well-formed package so the leakage, budget and metadata assertions have something
/// to run against.
fn plumbing_state(arm: Arm, scn: &Scenario, t: usize) -> Maintained {
    let mut m = Maintained::default();
    let visible = scn.upto(t);
    match arm {
        Arm::B1 => {
            let mut body = format!("# {} — state\n\n", scn.name);
            for (cp, e) in &visible {
                body.push_str(&format!("- day {}: {} ({})\n", cp.day, e.title, e.path));
            }
            m.files.insert("CURRENT_STATE.md".into(), body);
        }
        Arm::B4 => {
            let mut w = format!("# {} — wiki\n\n", scn.name);
            for (cp, e) in &visible {
                let first = e.body.lines().find(|l| !l.trim().is_empty()).unwrap_or("");
                w.push_str(&format!("## {} (day {})\n{}\n\n", e.title, cp.day, first));
            }
            m.wiki = w;
        }
        Arm::B5 => {
            let mut seq = 0u64;
            for (cp, e) in &visible {
                seq += 1;
                let statement = format!("{}: {}", e.title, first_sentence(&e.body));
                if let Ok(rec) = Memory::new(
                    format!("{}-{}", scn.id, seq),
                    statement,
                    MemoryType::Fact,
                    Basis::AgentAsserted,
                    Scope::project(VAULT_NAME, &scn.project),
                    seq,
                    cp.day,
                ) {
                    m.memories.push(rec);
                }
            }
        }
        _ => {}
    }
    m
}

fn first_sentence(body: &str) -> String {
    let text: String = body
        .lines()
        .filter(|l| !l.trim().is_empty() && !l.trim_start().starts_with('#'))
        .collect::<Vec<_>>()
        .join(" ");
    let cut_at = text
        .find(". ")
        .map(|i| i + 1)
        .unwrap_or(text.len().min(240));
    text[..cut_at.min(text.len())].trim().to_string()
}

/// A synthetic response built from an oracle. Used **only** to test the scorer.
fn synth(oracle: &Oracle, variant: &str) -> String {
    let mut f: BTreeMap<&str, String> = FIELDS.iter().map(|k| (*k, String::new())).collect();
    f.insert(
        "ACTION",
        "Take the concrete documented next step and record the outcome.".into(),
    );
    f.insert("EVIDENCE", "docs/status-current.md".into());
    f.insert("UNRESOLVED", "none".into());
    f.insert("CONSTRAINTS_APPLIED", "none".into());
    f.insert("DECISION", "Proceeding as recorded.".into());
    f.insert(
        "ABSTAIN",
        if oracle.abstain_required { "YES" } else { "NO" }.into(),
    );

    for c in &oracle.require_all {
        let token = c.any.first().cloned().unwrap_or_default();
        let slot = f.entry(field_key(&c.field)).or_default();
        slot.push(' ');
        slot.push_str(&token);
    }

    match variant {
        "gold" => {}
        "stale" => {
            if let Some(c) = oracle.forbid.first() {
                if let Some(tok) = c.any.first() {
                    let slot = f.entry(field_key(&c.field)).or_default();
                    slot.push(' ');
                    slot.push_str(tok);
                }
            }
        }
        "empty" => return String::new(),
        "abstain_only" => return "ABSTAIN: YES".to_string(),
        "hedge" => {
            return "It depends on a number of factors and the situation is nuanced. \
                    There are several considerations worth weighing carefully here."
                .to_string()
        }
        "wrong_abstain" => {
            f.insert(
                "ABSTAIN",
                if oracle.abstain_required { "NO" } else { "YES" }.into(),
            );
        }
        _ => {}
    }

    FIELDS
        .iter()
        .map(|k| format!("{}: {}", k, f.get(k).cloned().unwrap_or_default().trim()))
        .collect::<Vec<_>>()
        .join("\n")
}

fn field_key(field: &str) -> &'static str {
    FIELDS
        .iter()
        .find(|f| **f == field)
        .copied()
        .unwrap_or("DECISION")
}

// ---------------------------------------------------------------------------

struct Built {
    packages: BTreeMap<(String, usize, &'static str), String>,
}

/// Write already-constructed arm packages without changing their bytes.
///
/// This is execution plumbing only: package construction remains exclusively in
/// `build_all` and `arm_b0`..`arm_b5`. The exporter never parses, normalizes,
/// truncates, ranks, or otherwise transforms a package after construction.
fn write_built_packages<F>(
    built: &Built,
    out: &Path,
    trajectory: &str,
    include: F,
) -> Vec<(String, String)>
where
    F: Fn(&str) -> bool,
{
    let mut manifest = Vec::new();
    for ((sid, t, arm), ctx) in &built.packages {
        if !include(arm) {
            continue;
        }
        let dir = out.join(trajectory).join(arm).join(sid);
        fs::create_dir_all(&dir).expect("package export dir");
        let path = dir.join(format!("t{t:02}.txt"));
        fs::write(&path, ctx.as_bytes()).expect("write exported package");
        let rel = path
            .strip_prefix(out)
            .expect("export path under root")
            .to_string_lossy()
            .replace('\\', "/");
        manifest.push((rel, hash_bytes(ctx.as_bytes())));
    }
    manifest
}

/// Export the exact package bytes constructed by the native R1 harness.
///
/// Layout matches the external runner contract:
/// `<out>/<TRAJECTORY>/<ARM>/<SCENARIO>/t<NN>.txt`. Unmaintained arms are
/// exported once under T0. Maintained arms are exported separately from the T1
/// and T2 maintenance-state roots. Missing maintenance files mean "state left
/// unchanged", exactly as MAINTENANCE.md §7 specifies.
fn emit_packages(root: &Path, state_root: &Path, out: &Path) -> i32 {
    let scenarios = load_scenarios(&root.join("scenarios"));
    let (_contract, tasks) = load_tasks(&root.join("tasks").join("tasks.json"));

    let _ = fs::remove_dir_all(out);
    fs::create_dir_all(out).expect("package export root");

    let mut manifest: Vec<(String, String)> = Vec::new();

    // B0 and B3 are maintenance-independent. Build once and expose under T0.
    let unmaintained = build_all(&scenarios, &tasks, false, &state_root.join("T0"));
    manifest.extend(write_built_packages(&unmaintained, out, "T0", |arm| {
        matches!(arm, "B0" | "B3")
    }));

    // Maintained arms are trajectory-specific. The same native fold + arm builder
    // is invoked for both trajectories; no construction logic exists in the runner.
    for trajectory in ["T1", "T2"] {
        let built = build_all(&scenarios, &tasks, false, &state_root.join(trajectory));
        manifest.extend(write_built_packages(&built, out, trajectory, |arm| {
            matches!(arm, "B1" | "B4" | "B5")
        }));
    }

    manifest.sort_by(|a, b| a.0.cmp(&b.0));
    let mut text = String::from("# R1 native package export manifest v1\n");
    text.push_str("# sha256  relative_path\n");
    for (rel, digest) in &manifest {
        text.push_str(&format!("{digest}  {rel}\n"));
    }
    fs::write(out.join("PACKAGE-MANIFEST.txt"), text.as_bytes()).expect("write package manifest");

    println!("NATIVE_PACKAGE_EXPORT_STATUS=PASS");
    println!("PACKAGE_COUNT={}", manifest.len());
    println!("PACKAGE_MANIFEST_SHA256={}", hash_bytes(text.as_bytes()));
    0
}

fn parse_arm(id: &str) -> Option<Arm> {
    match id {
        "B0" => Some(Arm::B0),
        "B1" => Some(Arm::B1),
        "B3" => Some(Arm::B3),
        "B4" => Some(Arm::B4),
        "B5" => Some(Arm::B5),
        _ => None,
    }
}

/// Render the current maintained artefact using the same native fold consumed by
/// package construction. This keeps the external runner from reimplementing B5
/// memory lifecycle/supersession semantics merely to prepare the next maintainer
/// prompt.
fn maintained_view(
    root: &Path,
    state_dir: &Path,
    arm_id: &str,
    scenario_id: &str,
    t: usize,
) -> i32 {
    let Some(arm) = parse_arm(arm_id) else {
        eprintln!("maintenance-view requires one of B1, B4, B5");
        return 2;
    };
    if !arm.maintained() {
        eprintln!("maintenance-view requires a maintained arm");
        return 2;
    }
    let scenarios = load_scenarios(&root.join("scenarios"));
    let Some(scn) = scenarios.iter().find(|s| s.id == scenario_id) else {
        eprintln!("unknown scenario: {scenario_id}");
        return 2;
    };
    let m = fold_maintenance(state_dir, arm, scn, t);
    match arm {
        Arm::B1 => {
            for (path, body) in &m.files {
                println!("--- {path} ---");
                println!("{body}");
            }
        }
        Arm::B4 => print!("{}", m.wiki),
        Arm::B5 => {
            for rec in &m.memories {
                println!(
                    concat!(
                        "id={} | type={:?} | lifecycle={:?} | resolution={:?} | ",
                        "valid_from={} | valid_until={:?} | supersedes={:?}\n{}\n"
                    ),
                    rec.id.0,
                    rec.memory_type,
                    rec.lifecycle,
                    rec.resolution,
                    rec.valid_from,
                    rec.valid_until,
                    rec.supersedes,
                    rec.statement
                );
            }
        }
        _ => unreachable!(),
    }
    0
}

fn build_all(scenarios: &[Scenario], tasks: &[Task], plumbing: bool, state_dir: &Path) -> Built {
    let mut packages = BTreeMap::new();
    let work = std::env::temp_dir().join(format!(
        "fehrest-r1-{}",
        fehrest::identity::ObjectId::generate()
    ));

    for scn in scenarios {
        // t=0 is always built. It is the baseline the leakage detector subtracts as
        // an arm's structural vocabulary: anything an arm emits at the very first
        // checkpoint is part of its output format, not knowledge of the future.
        let mut checkpoints: BTreeSet<usize> = tasks
            .iter()
            .filter(|t| t.scenario == scn.id)
            .map(|t| t.checkpoint)
            .collect();
        checkpoints.insert(0);

        for &t in &checkpoints {
            // A vault holding exactly the evidence visible at this checkpoint. The
            // temporal boundary is enforced by construction, not by filtering later.
            let vroot = work.join(format!("{}-t{}", scn.id, t));
            let vault = Vault::create(&vroot).expect("vault");
            for (_, e) in scn.upto(t) {
                vault
                    .add_object(&e.path, Some(&e.title), Some(&scn.project), &e.body)
                    .expect("add object");
            }
            let scan = vault.scan().expect("scan");
            let derived = Derived::open(&vault.control_dir()).expect("derived");
            derived.rebuild(&scan.objects).expect("rebuild");

            for arm in COMPARISON_ARMS {
                let m = if arm.maintained() {
                    if plumbing {
                        plumbing_state(*arm, scn, t)
                    } else {
                        fold_maintenance(state_dir, *arm, scn, t)
                    }
                } else {
                    Maintained::default()
                };

                let ctx = match arm {
                    Arm::B0 => arm_b0(scn, t),
                    Arm::B1 => arm_b1(scn, t, &m),
                    Arm::B3 => {
                        // One package per task, since retrieval is query-dependent.
                        let mut merged = String::new();
                        for task in tasks
                            .iter()
                            .filter(|x| x.scenario == scn.id && x.checkpoint == t)
                        {
                            merged.push_str(&arm_b3(&derived, scn, t, &task.prompt));
                        }
                        cut(merged, BUDGET_BYTES)
                    }
                    Arm::B4 => arm_b4(&m),
                    Arm::B5 => arm_b5(scn, t, &m),
                    Arm::BNull => String::new(),
                };
                packages.insert((scn.id.clone(), t, arm.id()), ctx);
            }
        }
    }
    let _ = fs::remove_dir_all(&work);
    Built { packages }
}

fn selftest(root: &Path) -> i32 {
    let scenarios = load_scenarios(&root.join("scenarios"));
    let (_contract, tasks) = load_tasks(&root.join("tasks").join("tasks.json"));
    let oracles = load_oracles(&root.join("oracles").join("oracles.json"));
    let mut c = Checker::new();

    println!("R1 INSTRUMENT PILOT — measurement-instrument validation only");
    println!("NO MODEL EXECUTED. NO ARM SCORE IS PRODUCED OR IMPLIED.\n");

    println!(
        "corpus: {} scenarios, {} checkpoints, {} evidence items, {} tasks, {} oracles",
        scenarios.len(),
        scenarios.iter().map(|s| s.checkpoints.len()).sum::<usize>(),
        scenarios
            .iter()
            .flat_map(|s| s.checkpoints.iter())
            .map(|c| c.evidence.len())
            .sum::<usize>(),
        tasks.len(),
        oracles.len()
    );

    // --- 1. Task/oracle correspondence ------------------------------------
    c.family("[1] TASK / ORACLE CORRESPONDENCE");
    for t in &tasks {
        c.check(
            &format!("oracle exists for {}", t.task_id),
            oracles.contains_key(&t.task_id),
            "no oracle",
        );
    }
    for id in oracles.keys() {
        c.check(
            &format!("task exists for oracle {id}"),
            tasks.iter().any(|t| &t.task_id == id),
            "orphan oracle",
        );
    }
    for t in &tasks {
        if let Some(o) = oracles.get(&t.task_id) {
            let want_abstain = t.kind == "abstention";
            c.check(
                &format!("kind/abstain agree for {}", t.task_id),
                o.abstain_required == want_abstain,
                "task kind and oracle abstain_required disagree",
            );
        }
    }

    // --- 2. Answerability and trap reality --------------------------------
    c.family("[2] ANSWERABILITY AND TRAP REALITY");
    for t in &tasks {
        let Some(scn) = scenarios.iter().find(|s| s.id == t.scenario) else {
            c.check(&format!("scenario for {}", t.task_id), false, "missing");
            continue;
        };
        let Some(o) = oracles.get(&t.task_id) else {
            continue;
        };
        let visible: Vec<_> = scn.upto(t.checkpoint);
        let paths: BTreeSet<&str> = visible.iter().map(|(_, e)| e.path.as_str()).collect();
        let corpus: String = visible
            .iter()
            .map(|(_, e)| e.body.to_lowercase())
            .collect::<Vec<_>>()
            .join("\n");

        for d in &o.derivable_from {
            c.check(
                &format!("{} derivable from {d}", t.task_id),
                paths.contains(d.as_str()),
                "evidence path not visible at this checkpoint",
            );
        }
        for trap in &o.trap_present {
            c.check(
                &format!("{} trap '{trap}' is real", t.task_id),
                corpus.contains(&trap.to_lowercase()),
                "distractor token never appears in the corpus, so the trap is fake",
            );
        }
        // A require and a forbid on the same field must not name the same string.
        let mut clash = None;
        for r in &o.require_all {
            for fb in &o.forbid {
                if r.field == fb.field {
                    for a in &r.any {
                        if fb.any.iter().any(|b| b.eq_ignore_ascii_case(a)) {
                            clash = Some(a.clone());
                        }
                    }
                }
            }
        }
        c.check(
            &format!("{} require/forbid disjoint", t.task_id),
            clash.is_none(),
            &format!("token {clash:?} both required and forbidden"),
        );
    }

    // --- 3. Scorer validation --------------------------------------------
    c.family("[3] SCORER VALIDATION (synthetic responses, not model output)");
    for t in &tasks {
        let Some(o) = oracles.get(&t.task_id) else {
            continue;
        };
        c.check(
            &format!("{} oracle id matches task", t.task_id),
            o.task_id == t.task_id,
            "oracle task_id does not match the task it is keyed under",
        );
        let gold = score_one(t, o, &synth(o, "gold"));
        c.check(
            &format!("{} gold scores 1", t.task_id),
            gold.primary,
            &format!(
                "missing={} forbid={} substantive={}",
                gold.require_missing, gold.forbid_hit, gold.substantive
            ),
        );
        if !o.forbid.is_empty() {
            let stale = score_one(t, o, &synth(o, "stale"));
            c.check(
                &format!("{} stale scores 0", t.task_id),
                !stale.primary,
                "a response using a forbidden distractor received credit",
            );
        }
        let empty = score_one(t, o, &synth(o, "empty"));
        c.check(
            &format!("{} empty scores 0", t.task_id),
            !empty.primary,
            "EMPTY OUTPUT RECEIVED CREDIT -- primary metric is unsafe",
        );
        let ao = score_one(t, o, &synth(o, "abstain_only"));
        c.check(
            &format!("{} bare-abstain scores 0", t.task_id),
            !ao.primary,
            "a bare ABSTAIN with no substantive action received credit",
        );
        let hedge = score_one(t, o, &synth(o, "hedge"));
        c.check(
            &format!("{} contract-less hedge scores 0", t.task_id),
            !hedge.primary,
            "prose with no output contract received credit",
        );
        let wa = score_one(t, o, &synth(o, "wrong_abstain"));
        c.check(
            &format!("{} inverted abstain scores 0", t.task_id),
            !wa.primary,
            "abstention polarity is not enforced",
        );
    }

    // --- 4. Package construction, budget, leakage -------------------------
    c.family("[4] PACKAGE CONSTRUCTION (plumbing maintenance -- NOT an arm result)");
    let built = build_all(&scenarios, &tasks, true, &root.join("state"));
    // t=0 is built only as the structural-vocabulary baseline for the leakage test.
    // It carries no tasks, so a query-driven arm legitimately has nothing to build.
    let task_cps: BTreeSet<(String, usize)> = tasks
        .iter()
        .map(|t| (t.scenario.clone(), t.checkpoint))
        .collect();
    for ((sid, t, arm), ctx) in &built.packages {
        if !task_cps.contains(&(sid.clone(), *t)) {
            continue;
        }
        c.check(
            &format!("{sid} t{t} {arm} within budget"),
            ctx.len() <= BUDGET_BYTES,
            &format!("{} bytes > {BUDGET_BYTES}", ctx.len()),
        );
        c.check(
            &format!("{sid} t{t} {arm} non-empty"),
            !ctx.is_empty(),
            "arm produced no context at all",
        );
    }

    c.family("[4A] NATIVE PACKAGE EXPORT BYTE IDENTITY");
    let export_a = std::env::temp_dir().join(format!(
        "fehrest-r1-export-a-{}",
        fehrest::identity::ObjectId::generate()
    ));
    let export_b = std::env::temp_dir().join(format!(
        "fehrest-r1-export-b-{}",
        fehrest::identity::ObjectId::generate()
    ));
    let ma = write_built_packages(&built, &export_a, "T0", |_| true);
    let mb = write_built_packages(&built, &export_b, "T0", |_| true);
    c.check(
        "native export manifest is deterministic",
        ma == mb,
        "two exports of the same Built package map differed",
    );
    for ((sid, t, arm), ctx) in &built.packages {
        let pa = export_a
            .join("T0")
            .join(arm)
            .join(sid)
            .join(format!("t{t:02}.txt"));
        let pb = export_b
            .join("T0")
            .join(arm)
            .join(sid)
            .join(format!("t{t:02}.txt"));
        let a = fs::read(&pa).unwrap_or_default();
        let b = fs::read(&pb).unwrap_or_default();
        c.check(
            &format!("{sid} t{t} {arm} export bytes equal canonical in-memory package"),
            a == ctx.as_bytes() && b == ctx.as_bytes(),
            "export changed package bytes",
        );
    }
    let _ = fs::remove_dir_all(&export_a);
    let _ = fs::remove_dir_all(&export_b);

    c.family("[5] BASELINE METADATA ISOLATION");
    for ((sid, t, arm), ctx) in &built.packages {
        if *arm == "B5" {
            continue;
        }
        let leaked: Vec<&str> = FEHREST_MARKERS
            .iter()
            .filter(|m| ctx.contains(**m))
            .copied()
            .collect();
        c.check(
            &format!("{sid} t{t} {arm} has no Fehrest metadata"),
            leaked.is_empty(),
            &format!("leaked {leaked:?}"),
        );
    }

    c.family("[6] TEMPORAL BOUNDARY -- no arm may see the future");
    for scn in &scenarios {
        let cps: BTreeSet<usize> = tasks
            .iter()
            .filter(|t| t.scenario == scn.id)
            .map(|t| t.checkpoint)
            .collect();
        for &t in &cps {
            let mut past = BTreeSet::new();
            for (_, e) in scn.upto(t) {
                past.extend(words(&e.body));
                past.extend(words(&e.path));
                past.extend(words(&e.title));
            }
            let mut future_only = BTreeSet::new();
            for e in scn.after(t) {
                for w in words(&e.body).union(&words(&e.path)).cloned() {
                    if !past.contains(&w) {
                        future_only.insert(w);
                    }
                }
            }
            for arm in COMPARISON_ARMS {
                let Some(ctx) = built.packages.get(&(scn.id.clone(), t, arm.id())) else {
                    continue;
                };
                // An arm's own output format is not knowledge. Section labels,
                // envelope attributes and headings the compiler emits unconditionally
                // are present at t=0, before any later evidence exists, so they are
                // subtracted before the intersection is taken.
                let structural = built
                    .packages
                    .get(&(scn.id.clone(), 0, arm.id()))
                    .map(|p| words(p))
                    .unwrap_or_default();
                let got: BTreeSet<String> = words(ctx).difference(&structural).cloned().collect();
                let leaked: Vec<&String> = future_only.intersection(&got).take(5).collect();
                c.check(
                    &format!("{} t{t} {} no future vocabulary", scn.id, arm.id()),
                    leaked.is_empty(),
                    &format!("future-only tokens present: {leaked:?}"),
                );
            }
        }
    }

    // A detector that never fires proves nothing. Each assertion above is re-run
    // against a deliberately corrupted input, and must fail.
    c.family("[7] NEGATIVE CONTROLS -- every detector must fire when fed a defect");
    {
        // 7a. Temporal-boundary detector, exercised at a checkpoint that actually has
        // a future. A task issued at a scenario's last checkpoint cannot test the
        // boundary, cannot test maintenance lag, and cannot test knowledge decay --
        // so the benchmark is required to issue at least one task before the end.
        let mid = tasks.iter().find_map(|x| {
            let scn = scenarios.iter().find(|s| s.id == x.scenario)?;
            (!scn.after(x.checkpoint).is_empty()).then_some((scn, x.checkpoint))
        });
        c.check(
            "design: at least one task is issued before its scenario ends",
            mid.is_some(),
            "every task sits at its scenario's final checkpoint, so no arm is ever \
             asked to answer while the project still evolves -- maintenance lag, \
             staleness and knowledge decay are all untestable",
        );
        let Some((scn, t)) = mid else {
            return finish(&c);
        };

        let mut past = BTreeSet::new();
        for (_, e) in scn.upto(t) {
            past.extend(words(&e.body));
        }
        let future_only: BTreeSet<String> = scn
            .after(t)
            .iter()
            .flat_map(|e| words(&e.body))
            .filter(|w| !past.contains(w))
            .collect();
        let poisoned = format!(
            "{}\n{}",
            built
                .packages
                .get(&(scn.id.clone(), t, "B0"))
                .cloned()
                .unwrap_or_default(),
            future_only
                .iter()
                .take(3)
                .cloned()
                .collect::<Vec<_>>()
                .join(" ")
        );
        let detected = !future_only
            .intersection(&words(&poisoned))
            .collect::<Vec<_>>()
            .is_empty();
        c.check(
            "negative control: temporal-boundary detector fires on injected future text",
            detected || future_only.is_empty(),
            "a package carrying future vocabulary was not detected",
        );
        c.check(
            "negative control: future vocabulary set is non-empty",
            !future_only.is_empty(),
            "no future-only vocabulary exists, so the boundary check is vacuous",
        );

        // 7b. Metadata-leak detector.
        let fake_baseline = "--- doc ---\n<fehrest:item authority=\"full\">\n";
        c.check(
            "negative control: metadata detector fires on an injected envelope",
            FEHREST_MARKERS.iter().any(|m| fake_baseline.contains(m)),
            "an envelope marker in a baseline package was not detected",
        );

        // 7c. Scorer must reject a response that satisfies everything but the action.
        if let Some((task, oracle)) = tasks
            .iter()
            .find_map(|x| oracles.get(&x.task_id).map(|o| (x, o)))
        {
            let mut gold = synth(oracle, "gold");
            gold = gold
                .lines()
                .map(|l| {
                    if l.starts_with("ACTION:") {
                        "ACTION:"
                    } else {
                        l
                    }
                })
                .collect::<Vec<_>>()
                .join("\n");
            c.check(
                "negative control: scorer rejects a correct answer with an empty ACTION",
                !score_one(task, oracle, &gold).primary,
                "an answer with no action received continuation credit",
            );
        }
    }

    println!("\n[8] MAINTENANCE STATE PRESENCE");
    let state_dir = root.join("state");
    for scn in &scenarios {
        for arm in COMPARISON_ARMS.iter().filter(|a| a.maintained()) {
            let m = fold_maintenance(&state_dir, *arm, scn, usize::MAX);
            println!(
                "  {:<6} {:<3} maintainer output: {}",
                arm.id(),
                scn.id,
                if m.absent {
                    "ABSENT -- arm cannot be scored until a maintainer runs".to_string()
                } else {
                    format!(
                        "{} actions, {} objects, {} output bytes",
                        m.cost.actions, m.cost.objects_touched, m.cost.output_bytes
                    )
                }
            );
        }
    }

    finish(&c)
}

fn finish(c: &Checker) -> i32 {
    for l in &c.lines {
        if l.starts_with("  FAIL") {
            println!("{l}");
        }
    }

    println!("\nCHECKS BY FAMILY");
    for (name, pass, fail) in &c.families {
        println!("  {pass:>4} passed {fail:>3} failed   {name}");
    }

    println!("\n=====================================================");
    println!("INSTRUMENT CHECKS: {} passed, {} failed", c.pass, c.fail);
    println!("=====================================================");
    println!(
        "R1_INSTRUMENT_PILOT: {}",
        if c.fail == 0 { "PASS" } else { "FAIL" }
    );
    println!("MODEL_EXECUTED: NO");
    println!("ARM_SCORES_PRODUCED: NONE");
    println!("VARIANCE_ESTIMATE: UNAVAILABLE_WITHOUT_MODEL_EXECUTION");
    println!("PRODUCT_THESIS_STATUS: NOT_EVALUATED");
    i32::from(c.fail != 0)
}

// ---------------------------------------------------------------------------

fn emit_bundle(root: &Path, out: &Path) -> i32 {
    let scenarios = load_scenarios(&root.join("scenarios"));
    let (contract, tasks) = load_tasks(&root.join("tasks").join("tasks.json"));

    let _ = fs::remove_dir_all(out);
    fs::create_dir_all(out).expect("bundle dir");

    let mut manifest = String::new();
    manifest.push_str("# R1 run bundle manifest\n\n");
    manifest.push_str(&format!("budget_bytes: {BUDGET_BYTES}\n"));
    manifest.push_str("model_executed: NO\n");
    manifest.push_str("oracles_included: NO\n\n");

    // Evidence bundles per checkpoint, for the maintainer sessions.
    for scn in &scenarios {
        for cp in &scn.checkpoints {
            let dir = out
                .join("evidence")
                .join(&scn.id)
                .join(format!("t{:02}", cp.t));
            fs::create_dir_all(&dir).expect("evidence dir");
            for e in &cp.evidence {
                let name = e.path.replace('/', "__");
                fs::write(dir.join(&name), &e.body).expect("write evidence");
            }
            manifest.push_str(&format!(
                "evidence {} t{:02} day={} items={}\n",
                scn.id,
                cp.t,
                cp.day,
                cp.evidence.len()
            ));
        }
    }

    // Continuation task prompts, arm-blinded at execution time by the runner.
    let tdir = out.join("tasks");
    fs::create_dir_all(&tdir).expect("tasks dir");
    for t in &tasks {
        let body = format!(
            "TASK_ID: {}\nSCENARIO: {}\nCHECKPOINT: t{:02}\n\n\
             You are continuing work on an ongoing project. You have been given the \
             project context separately. Do not assume anything not supported by it.\n\n\
             {}\n\n{}\n",
            t.task_id, t.scenario, t.checkpoint, t.prompt, contract
        );
        fs::write(tdir.join(format!("{}.txt", t.task_id)), body).expect("write task");
        manifest.push_str(&format!(
            "task {} scenario={} t={:02} class={} kind={}\n",
            t.task_id, t.scenario, t.checkpoint, t.class, t.kind
        ));
    }

    // Arm roster. B-NULL is listed because the runner must execute it: it is the
    // calibration arm that detects tasks answerable from the prompt alone. It is not
    // a comparison arm and its score is never reported alongside the others.
    let mut arms = String::from("# R1 arms\n\nid\tmaintained\trole\n");
    for a in [Arm::BNull, Arm::B0, Arm::B1, Arm::B3, Arm::B4, Arm::B5] {
        let role = match a {
            Arm::BNull => "calibration -- prompt only, no project context",
            Arm::B0 => "baseline -- plain project files, recency ordered, zero maintenance",
            Arm::B1 => "baseline -- repository-native state docs plus the project",
            Arm::B3 => "baseline -- lexical retrieval over the project",
            Arm::B4 => "baseline -- maintained wiki page",
            Arm::B5 => "treatment -- Fehrest compiled context package",
        };
        arms.push_str(&format!("{}\t{}\t{}\n", a.id(), a.maintained(), role));
    }
    fs::write(out.join("ARMS.txt"), &arms).expect("write arms");
    fs::write(out.join("MANIFEST.txt"), &manifest).expect("write manifest");

    // The bundle must not carry the oracles.
    let leaked = walk(out)
        .into_iter()
        .filter(|p| {
            fs::read_to_string(p)
                .map(|s| s.contains("abstain_required") || s.contains("trap_present"))
                .unwrap_or(false)
        })
        .count();
    println!("bundle written to {}", out.display());
    println!("files: {}", walk(out).len());
    println!(
        "ORACLE_LEAK_CHECK: {}",
        if leaked == 0 { "CLEAN" } else { "LEAKED" }
    );
    i32::from(leaked != 0)
}

fn walk(dir: &Path) -> Vec<PathBuf> {
    let mut out = Vec::new();
    if let Ok(rd) = fs::read_dir(dir) {
        for e in rd.flatten() {
            let p = e.path();
            if p.is_dir() {
                out.extend(walk(&p));
            } else {
                out.push(p);
            }
        }
    }
    out
}

fn response_identity(path: &Path) -> Option<(String, String, Option<usize>)> {
    let stem = path.file_stem()?.to_str()?;
    if let Some(repeat) = stem.strip_prefix('r').and_then(|n| n.parse::<usize>().ok()) {
        let task_id = path.parent()?.file_name()?.to_str()?.to_string();
        let arm = path.parent()?.parent()?.file_name()?.to_str()?.to_string();
        Some((arm, task_id, Some(repeat)))
    } else {
        let arm = path.parent()?.file_name()?.to_str()?.to_string();
        Some((arm, stem.to_string(), None))
    }
}

fn score_jsonl(root: &Path, responses: &Path, out: &Path) -> i32 {
    let (_c, tasks) = load_tasks(&root.join("tasks").join("tasks.json"));
    let oracles = load_oracles(&root.join("oracles").join("oracles.json"));
    let mut paths = walk(responses);
    paths.sort();
    let mut lines = String::new();
    for p in paths {
        let Some((arm, task_id, repeat_index)) = response_identity(&p) else {
            continue;
        };
        let Some(task) = tasks.iter().find(|t| t.task_id == task_id) else {
            continue;
        };
        let Some(oracle) = oracles.get(&task_id) else {
            continue;
        };
        let text = fs::read_to_string(&p).unwrap_or_default();
        let score = score_one(task, oracle, &text);
        let record = serde_json::json!({
            "arm_id": arm,
            "task_id": task_id,
            "repeat_index": repeat_index,
            "class": score.class,
            "kind": score.kind,
            "primary": score.primary,
            "forbid_hit": score.forbid_hit,
            "require_missing": score.require_missing,
            "substantive": score.substantive,
            "abstained": score.abstained,
            "false_abstention": score.false_abstention,
            "conflict_flagged": score.conflict_flagged,
            "provenance_given": score.provenance_given,
            "response_sha256": hash_bytes(text.as_bytes()),
        });
        lines.push_str(&serde_json::to_string(&record).expect("score record serializes"));
        lines.push('\n');
    }
    if lines.is_empty() {
        eprintln!("no scorable responses found under {}", responses.display());
        return 1;
    }
    fs::write(out, lines.as_bytes()).expect("write score jsonl");
    println!("R1_SCORE_JSONL={}", out.display());
    println!("R1_SCORE_JSONL_SHA256={}", hash_bytes(lines.as_bytes()));
    0
}

fn score_dir(root: &Path, responses: &Path) -> i32 {
    let (_c, tasks) = load_tasks(&root.join("tasks").join("tasks.json"));
    let oracles = load_oracles(&root.join("oracles").join("oracles.json"));

    let mut per_arm: BTreeMap<String, Vec<TaskScore>> = BTreeMap::new();
    let mut response_paths = walk(responses);
    response_paths.sort();
    for p in response_paths {
        let Some((arm, task_id, _repeat_index)) = response_identity(&p) else {
            continue;
        };
        let Some(task) = tasks.iter().find(|t| t.task_id == task_id) else {
            continue;
        };
        let Some(oracle) = oracles.get(&task_id) else {
            continue;
        };
        let text = fs::read_to_string(&p).unwrap_or_default();
        per_arm
            .entry(arm)
            .or_default()
            .push(score_one(task, oracle, &text));
    }

    if per_arm.is_empty() {
        println!("no responses found under {}", responses.display());
        println!("R1_SCORING: NO_INPUT -- a model must run first");
        return 1;
    }

    println!("PER-TASK DETAIL");
    println!(
        "{:<10} {:<20} {:<24} {:<12} {:>7} {:>6} {:>6} {:>6} {:>6}",
        "ARM", "TASK", "CLASS", "KIND", "PRIMARY", "STALE", "ABST", "CONFL", "PROV"
    );
    for (arm, ss) in &per_arm {
        for s in ss {
            println!(
                "{:<10} {:<20} {:<24} {:<12} {:>7} {:>6} {:>6} {:>6} {:>6}",
                arm,
                s.task_id,
                s.class,
                s.kind,
                yn(s.primary),
                yn(s.forbid_hit),
                yn(s.abstained),
                yn(s.conflict_flagged),
                yn(s.provenance_given),
            );
        }
    }

    println!("\nPRIMARY OUTCOME (continuation correctness)");
    println!("{:<10} {:>6} {:>9} {:>10}", "ARM", "N", "PRIMARY", "RATE");
    for (arm, ss) in &per_arm {
        let n = ss.len();
        let p = ss.iter().filter(|s| s.primary).count();
        println!(
            "{arm:<10} {n:>6} {p:>9} {:>9.1}%",
            100.0 * p as f64 / n.max(1) as f64
        );
    }

    println!("\nSECONDARY DIMENSIONS -- reported separately, never folded into PRIMARY");
    println!(
        "{:<10} {:>11} {:>12} {:>12} {:>12} {:>12}",
        "ARM", "STALE_USE", "FALSE_ABST", "MISSED_ABST", "CONFLICT_FL", "PROVENANCE"
    );
    for (arm, ss) in &per_arm {
        let stale = ss.iter().filter(|s| s.forbid_hit).count();
        let fa = ss.iter().filter(|s| s.false_abstention).count();
        let missed = ss
            .iter()
            .filter(|s| s.kind == "abstention" && !s.abstained)
            .count();
        let conf = ss
            .iter()
            .filter(|s| s.class == "CONTRADICTION_HANDLING" && s.conflict_flagged)
            .count();
        let prov = ss.iter().filter(|s| s.provenance_given).count();
        println!("{arm:<10} {stale:>11} {fa:>12} {missed:>12} {conf:>12} {prov:>12}");
    }

    println!("\nNo composite score is computed. Weighting one was not preregistered,");
    println!("and inventing one after seeing results is exactly what the protocol forbids.");
    0
}

fn yn(b: bool) -> &'static str {
    if b {
        "yes"
    } else {
        "no"
    }
}

fn main() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("bench")
        .join("R1");
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let cmd = argv.first().map(String::as_str).unwrap_or("selftest");

    let code = match cmd {
        "selftest" => selftest(&root),
        "bundle" => {
            let out = argv
                .get(1)
                .map(PathBuf::from)
                .unwrap_or_else(|| root.join("bundle"));
            emit_bundle(&root, &out)
        }
        "export-packages" => {
            let Some(state_root) = argv.get(1).map(PathBuf::from) else {
                eprintln!("USAGE: fehrest-r1 export-packages <state-root> <out-dir>");
                std::process::exit(2);
            };
            let Some(out) = argv.get(2).map(PathBuf::from) else {
                eprintln!("USAGE: fehrest-r1 export-packages <state-root> <out-dir>");
                std::process::exit(2);
            };
            emit_packages(&root, &state_root, &out)
        }
        "maintenance-view" => {
            let Some(state_dir) = argv.get(1).map(PathBuf::from) else {
                eprintln!(
                    "USAGE: fehrest-r1 maintenance-view <state-dir> <arm> <scenario> <checkpoint>"
                );
                std::process::exit(2);
            };
            let Some(arm) = argv.get(2) else {
                eprintln!(
                    "USAGE: fehrest-r1 maintenance-view <state-dir> <arm> <scenario> <checkpoint>"
                );
                std::process::exit(2);
            };
            let Some(scenario) = argv.get(3) else {
                eprintln!(
                    "USAGE: fehrest-r1 maintenance-view <state-dir> <arm> <scenario> <checkpoint>"
                );
                std::process::exit(2);
            };
            let Some(checkpoint) = argv.get(4).and_then(|s| s.parse::<usize>().ok()) else {
                eprintln!("checkpoint must be an integer");
                std::process::exit(2);
            };
            maintained_view(&root, &state_dir, arm, scenario, checkpoint)
        }
        "score-jsonl" => {
            let dir = argv
                .get(1)
                .map(PathBuf::from)
                .unwrap_or_else(|| root.join("responses"));
            let out = argv
                .get(2)
                .map(PathBuf::from)
                .unwrap_or_else(|| root.join("score-records.jsonl"));
            score_jsonl(&root, &dir, &out)
        }
        "score" => {
            let dir = argv
                .get(1)
                .map(PathBuf::from)
                .unwrap_or_else(|| root.join("responses"));
            score_dir(&root, &dir)
        }
        other => {
            eprintln!("unknown command: {other}\n");
            eprintln!("USAGE:");
            eprintln!("  fehrest-r1 selftest");
            eprintln!("  fehrest-r1 bundle [dir]");
            eprintln!("  fehrest-r1 export-packages <state-root> <out-dir>");
            eprintln!("  fehrest-r1 maintenance-view <state-dir> <arm> <scenario> <checkpoint>");
            eprintln!("  fehrest-r1 score-jsonl <responses-dir> <out-file>");
            eprintln!("  fehrest-r1 score <responses-dir>");
            2
        }
    };
    std::process::exit(code);
}
