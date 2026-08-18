//! Benchmark harness — context adequacy across five arms.
//!
//! **This does NOT measure the product thesis.** It measures whether the context an
//! arm hands to an agent contains what is needed to answer correctly, and whether it
//! contains stale or out-of-scope material presented as current. Running an actual
//! language model on each arm's context is `PENDING_MODEL_EXECUTION` and did not
//! happen. See `bench/PRE-REGISTRATION.md`, which fixed every metric below before
//! any result was observed.
//!
//! Adequacy is **necessary but not sufficient**: a context lacking the answer means
//! no agent can reliably produce it, but a context containing the answer does not
//! mean an agent will use it.

use fehrest::context::{self, CompileRequest, SourceItem};
use fehrest::derived::Derived;
use fehrest::envelope::TrustLevel;
use fehrest::events::hash_bytes;
use fehrest::memory::{Basis, Lifecycle, Memory, MemoryType, Scope};
use fehrest::vault::Vault;
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

/// Identical for every arm. No arm gets more room than another.
const BUDGET_BYTES: usize = 4_000;

// ---------------------------------------------------------------------------
// Ground truth, loaded from the pre-registered fixture
// ---------------------------------------------------------------------------

#[derive(Debug)]
struct Query {
    id: String,
    class: String,
    project: String,
    as_of_day: Option<i64>,
    question: String,
    must_contain: Vec<String>,
    stale_tokens: Vec<String>,
}

/// Minimal field extraction from the fixture JSON. `serde_json` is already an
/// admitted dependency, so this is deserialization, not a parser.
fn load_queries(path: &Path) -> Vec<Query> {
    let text = fs::read_to_string(path).expect("queries fixture must exist");
    let v: serde_json::Value = serde_json::from_str(&text).expect("queries fixture must parse");
    v.as_array()
        .expect("queries fixture is an array")
        .iter()
        .map(|q| Query {
            id: q["id"].as_str().unwrap().to_string(),
            class: q["class"].as_str().unwrap().to_string(),
            project: q["project"].as_str().unwrap().to_string(),
            as_of_day: q["as_of_day"].as_i64(),
            question: q["question"].as_str().unwrap().to_string(),
            must_contain: str_list(&q["must_contain"]),
            stale_tokens: str_list(&q["stale_tokens"]),
        })
        .collect()
}

fn str_list(v: &serde_json::Value) -> Vec<String> {
    v.as_array()
        .map(|a| a.iter().map(|s| s.as_str().unwrap().to_string()).collect())
        .unwrap_or_default()
}

// ---------------------------------------------------------------------------
// The Fehrest-side memory record of the same corpus.
//
// These are hand-written, exactly as `fixtures/wiki.md` is hand-written. Both arms
// therefore assume the same thing: a diligent maintainer. Giving Fehrest curated
// memory while giving B4 a stale wiki would be rigging the comparison, so B4's page
// is fully current and this is its structural equivalent.
// ---------------------------------------------------------------------------

fn fehrest_memories() -> Vec<Memory> {
    let mut out = Vec::new();

    // The reversed datastore decision. Valid-time intervals are half-open.
    let mut old = Memory::new(
        "m-datastore-old",
        "Canonical state lives in Postgres. All services connect through the shared pool.",
        MemoryType::Decision,
        Basis::UserAsserted,
        Scope::project("bench", "core"),
        1,
        3,
    )
    .unwrap()
    .with_triple("core", "datastore");
    old.valid_until = Some(40);
    old.lifecycle = Lifecycle::Superseded;
    out.push(old);

    let mut new = Memory::new(
        "m-datastore-new",
        "Canonical state moves to SQLite, one file per vault. The local-first requirement landed after ADR-0001 and changed the problem.",
        MemoryType::Decision,
        Basis::UserAsserted,
        Scope::project("bench", "core"),
        2,
        40,
    )
    .unwrap()
    .with_triple("core", "datastore");
    new.supersedes = vec!["m-datastore-old".into()];
    out.push(new);

    out.push(
        Memory::new(
            "m-core-uuid",
            "Every read of a canonical object verifies its UUID after opening the handle.",
            MemoryType::Constraint,
            Basis::UserAsserted,
            Scope::project("bench", "core"),
            3,
            1,
        )
        .unwrap()
        .with_triple("core", "read_constraint"),
    );

    out.push(
        Memory::new(
            "m-core-network",
            "No network I/O in the core.",
            MemoryType::Constraint,
            Basis::UserAsserted,
            Scope::project("bench", "core"),
            4,
            1,
        )
        .unwrap()
        .with_triple("core", "network_constraint"),
    );

    out.push(
        Memory::new(
            "m-edge-retention",
            "The edge service must retain request logs for ninety days.",
            MemoryType::Constraint,
            Basis::UserAsserted,
            Scope::project("bench", "edge"),
            5,
            1,
        )
        .unwrap()
        .with_triple("edge", "retention_constraint"),
    );

    out.push(
        Memory::new(
            "m-edge-gateway",
            "The edge service runs behind the shared gateway and inherits its TLS termination.",
            MemoryType::Fact,
            Basis::UserAsserted,
            Scope::project("bench", "edge"),
            6,
            1,
        )
        .unwrap()
        .with_triple("edge", "gateway"),
    );

    out.push(
        Memory::new(
            "m-gotcha-rebuild",
            "A vault root with a trailing separator produced doubled separators during index rebuild; the FTS insert accepted them silently and queries returned nothing. Normalize the root before walking.",
            MemoryType::Gotcha,
            Basis::UserAsserted,
            Scope::project("bench", "core"),
            7,
            1,
        )
        .unwrap()
        .with_triple("core", "rebuild_gotcha"),
    );

    // Two active, inseparable positions -- identical on every rung of the ladder.
    for (id, claim) in [
        ("m-deploy-a", "The deploy target is staging. Production deploys go through the release train, and anything else breaks the rollback guarantee."),
        ("m-deploy-b", "The deploy target is production. The release train adds a day of latency for no benefit now that the canary covers the same risk."),
    ] {
        out.push(
            Memory::new(id, claim, MemoryType::Decision, Basis::UserAsserted, Scope::project("bench", "core"), 8, 7)
                .unwrap()
                .with_triple("core", "deploy_target"),
        );
    }

    out
}

// ---------------------------------------------------------------------------
// Arms
// ---------------------------------------------------------------------------

fn corpus_docs(dir: &Path) -> Vec<(String, String)> {
    let mut docs: Vec<(String, String)> = fs::read_dir(dir)
        .expect("corpus must exist")
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| p.extension().is_some_and(|x| x == "md"))
        .map(|p| {
            (
                p.file_name().unwrap().to_string_lossy().to_string(),
                fs::read_to_string(&p).unwrap(),
            )
        })
        .collect();
    docs.sort_by(|a, b| a.0.cmp(&b.0)); // path order, deterministic
    docs
}

fn cut(s: String, budget: usize) -> String {
    if s.len() <= budget {
        return s;
    }
    // Cut on a char boundary, never mid-UTF-8.
    let mut end = budget;
    while end > 0 && !s.is_char_boundary(end) {
        end -= 1;
    }
    s[..end].to_string()
}

/// B0 — plain agent. The floor.
fn arm_b0(_q: &Query) -> String {
    String::new()
}

/// B1 — every corpus document concatenated in path order, cut at budget.
fn arm_b1(docs: &[(String, String)]) -> String {
    let joined: String = docs
        .iter()
        .map(|(n, c)| format!("--- {n} ---\n{c}\n"))
        .collect();
    cut(joined, BUDGET_BYTES)
}

/// B3 — FTS5 top-k over the same corpus. Raw document text only.
/// Stopwords dropped before term search. Without this the arm searches for "What"
/// and "does" and ranks the whole corpus equally.
const STOPWORDS: &[&str] = &[
    "what", "which", "does", "did", "do", "is", "are", "the", "a", "an", "for", "of", "on", "in",
    "to", "use", "apply", "governs", "that", "and", "or",
];

fn arm_b3(derived: &Derived, vault: &Vault, q: &Query) -> String {
    // Fehrest's FTS expression builder joins quoted tokens with implicit AND, so
    // handing it a whole question retrieves nothing at all. A real lexical baseline
    // ORs its content terms; searching per term and merging by first-appearance rank
    // is the fair equivalent, and keeps this arm on raw document text only.
    let terms: Vec<String> = q
        .question
        .split_whitespace()
        .map(|t| {
            t.trim_matches(|c: char| !c.is_alphanumeric())
                .to_lowercase()
        })
        .filter(|t| t.len() > 2 && !STOPWORDS.contains(&t.as_str()))
        .collect();

    let mut seen = std::collections::BTreeSet::new();
    let mut hits = Vec::new();
    for term in &terms {
        for c in derived.search(term, 20).unwrap_or_default() {
            if seen.insert(c.id.to_string()) {
                hits.push(c);
            }
        }
    }

    let mut out = String::new();
    for c in hits {
        // Read through the verified path, exactly as the product would; the arm
        // still only ever SEES the document text.
        let Ok(content) = fehrest::locator::read_verified(vault.root(), &c.rel_path, c.id) else {
            continue;
        };
        let body = content
            .split("---\n")
            .nth(2)
            .unwrap_or(&content)
            .to_string();
        let next = format!("--- {} ---\n{}\n", c.rel_path, body);
        if out.len() + next.len() > BUDGET_BYTES {
            break;
        }
        out.push_str(&next);
    }
    out
}

/// B4 — maintained LLM wiki. The bar that matters most.
fn arm_b4(wiki: &str) -> String {
    cut(wiki.to_string(), BUDGET_BYTES)
}

/// B5 — Fehrest Core compiled context package.
fn arm_b5(memories: &[Memory], q: &Query) -> String {
    let as_of = q.as_of_day.unwrap_or(i64::MAX);
    let scope = Scope::project("bench", &q.project);

    let mut items: Vec<SourceItem> = Vec::new();
    for m in memories {
        if !m.scope.matches(&scope) {
            continue;
        }
        // Temporal admissibility, using the same rule the resolver uses.
        if m.valid_from > as_of {
            continue;
        }
        if m.valid_until.is_some_and(|u| u <= as_of) && m.lifecycle != Lifecycle::Superseded {
            continue;
        }

        // A record whose interval has closed relative to `as_of` is history, and is
        // placed in the superseded section so the label travels with the content.
        let closed = m.valid_until.is_some_and(|u| u <= as_of);
        let section = match (m.memory_type, closed) {
            (_, true) => "superseded_decisions",
            (MemoryType::Constraint, _) => "active_constraints",
            (MemoryType::Gotcha, _) => "gotchas",
            (MemoryType::Decision, _) => "current_decisions",
            _ => "project_state",
        };

        items.push(SourceItem {
            section,
            item_id: m.id.0.clone(),
            content: m.statement.clone(),
            source_content_hash: hash_bytes(m.statement.as_bytes()),
            trust_level: TrustLevel::VaultKnowledge,
            memory: Some(m.clone()),
            superseded_by: None,
        });
    }

    // Contention detection: two admissible decisions on the same subject/predicate
    // that nothing separates. Surfaced, never silently resolved.
    let mut by_triple: BTreeMap<(String, String), Vec<usize>> = BTreeMap::new();
    for (i, it) in items.iter().enumerate() {
        if let Some(m) = &it.memory {
            if it.section == "superseded_decisions" {
                continue;
            }
            if let (Some(s), Some(p)) = (&m.subject, &m.predicate) {
                by_triple.entry((s.clone(), p.clone())).or_default().push(i);
            }
        }
    }
    let contended: Vec<usize> = by_triple
        .values()
        .filter(|v| v.len() > 1)
        .flat_map(|v| v.iter().copied())
        .collect();
    for i in contended {
        items[i].section = "contradictions";
    }

    let req = CompileRequest {
        principal: "agent:bench".into(),
        scope,
        as_of_valid: as_of,
        as_of_recorded: u64::MAX,
        budget_bytes: BUDGET_BYTES,
    };
    context::compile(&req, &items).wire
}

// ---------------------------------------------------------------------------
// Leak guard — a baseline that sees Fehrest metadata invalidates the comparison
// ---------------------------------------------------------------------------

const FEHREST_MARKERS: &[&str] = &[
    "<fehrest:item",
    "trust_level=",
    "authority=",
    "lifecycle=",
    "temporal=",
    "provenance=",
    "content_len=",
    "verification=",
];

fn assert_no_fehrest_metadata(arm: &str, ctx: &str) {
    for m in FEHREST_MARKERS {
        assert!(
            !ctx.contains(m),
            "LEAK: arm {arm} received Fehrest metadata `{m}`. The comparison is invalid."
        );
    }
}

// ---------------------------------------------------------------------------
// Scoring — fixed by the pre-registration, before any result was seen
// ---------------------------------------------------------------------------

/// Markers that identify nearby text as not-current. Used to decide whether a stale
/// token is *labelled* rather than merely present.
const LABEL_MARKERS: &[&str] = &[
    "Superseded",
    "superseded",
    "Historical",
    "historical",
    "replaced",
    "Supersedes",
    "no longer",
    "Unresolved",
    "unresolved",
    "earlier",
];

#[derive(Debug, Clone, Copy)]
struct Score {
    contains_correct: bool,
    contains_stale: bool,
    stale_is_labelled: bool,
    misleading: bool,
    adequate: bool,
    bytes: usize,
}

/// Is every occurrence of a stale token accompanied by a label identifying it as
/// not-current? Checked within a window around each occurrence, so a label attached
/// to a different item does not launder an unlabelled one.
fn stale_labelled(ctx: &str, token: &str) -> bool {
    let mut from = 0;
    while let Some(rel) = ctx[from..].find(token) {
        let at = from + rel;
        let lo = at.saturating_sub(400);
        let hi = (at + token.len() + 400).min(ctx.len());
        let (lo, hi) = (floor_boundary(ctx, lo), floor_boundary(ctx, hi));
        let window = &ctx[lo..hi];
        if !LABEL_MARKERS.iter().any(|m| window.contains(m)) {
            return false;
        }
        from = at + token.len();
    }
    true
}

fn floor_boundary(s: &str, mut i: usize) -> usize {
    while i > 0 && i < s.len() && !s.is_char_boundary(i) {
        i -= 1;
    }
    i.min(s.len())
}

/// Every project named anywhere in the fixture. Used so that "this belongs to a
/// DIFFERENT project" counts as a scope label.
const PROJECTS: &[&str] = &["core", "edge"];

/// Is the stale token scoped away by a nearby mention of a different project?
///
/// A wiki that files a constraint under an `## edge — constraints` heading HAS
/// labelled it, and a human reader would not misapply it to core. Scoring only
/// Fehrest-shaped markers (`Superseded`, `Historical`) would penalise the baseline
/// for using a plain heading -- which would be measuring formatting, not adequacy.
fn scope_labelled(ctx: &str, token: &str, own_project: &str) -> bool {
    let others: Vec<&&str> = PROJECTS.iter().filter(|p| **p != own_project).collect();
    if others.is_empty() {
        return false;
    }
    let mut from = 0;
    let mut found_any = false;
    while let Some(rel) = ctx[from..].find(token) {
        let at = from + rel;
        let lo = floor_boundary(ctx, at.saturating_sub(400));
        let hi = floor_boundary(ctx, (at + token.len() + 400).min(ctx.len()));
        let window = &ctx[lo..hi];
        if !others.iter().any(|p| window.contains(**p)) {
            return false;
        }
        found_any = true;
        from = at + token.len();
    }
    found_any
}

fn score(q: &Query, ctx: &str) -> Score {
    let contains_correct = q.must_contain.iter().all(|t| ctx.contains(t.as_str()));
    let contains_stale = q.stale_tokens.iter().any(|t| ctx.contains(t.as_str()));
    let stale_is_labelled = q
        .stale_tokens
        .iter()
        .filter(|t| ctx.contains(t.as_str()))
        .all(|t| stale_labelled(ctx, t) || scope_labelled(ctx, t, &q.project));
    let misleading = contains_stale && !stale_is_labelled;

    let adequate = match q.class.as_str() {
        // Both contenders present AND the conflict marked. Presence alone is not
        // enough: an agent handed two flat contradictory claims will pick one.
        "CONTRADICTION" => {
            contains_correct
                && (ctx.contains("contradictions")
                    || ctx.contains("Unresolved")
                    || ctx.contains("unresolved"))
        }
        // Scored on what the context LACKS. An arm cannot win by retrieving
        // something plausible, only by retrieving nothing misleading.
        "ABSENT" => !contains_stale,
        _ => contains_correct && !misleading,
    };

    Score {
        contains_correct,
        contains_stale,
        stale_is_labelled,
        misleading,
        adequate,
        bytes: ctx.len(),
    }
}

// ---------------------------------------------------------------------------

fn main() {
    let bench_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("bench");
    let fixtures = bench_dir.join("fixtures");
    let queries = load_queries(&fixtures.join("queries.json"));
    let docs = corpus_docs(&fixtures.join("corpus"));
    let wiki = fs::read_to_string(fixtures.join("wiki.md")).expect("wiki fixture must exist");
    let memories = fehrest_memories();

    // A throwaway vault holding the same corpus, so B3 searches real indexed text.
    let work = std::env::temp_dir().join(format!(
        "fehrest-bench-{}",
        fehrest::identity::ObjectId::generate()
    ));
    let vault = Vault::create(&work).expect("bench vault");
    for (name, body) in &docs {
        vault
            .add_object(name, Some(name), Some("core"), body)
            .unwrap();
    }
    let scan = vault.scan().unwrap();
    let derived = Derived::open(&vault.control_dir()).unwrap();
    derived.rebuild(&scan.objects).unwrap();

    println!("FEHREST PHASE T — CONTEXT ADEQUACY PILOT");
    println!("PRE_REGISTERED: bench/PRE-REGISTRATION.md");
    println!("MEASURES: context adequacy. NOT the product thesis.");
    println!("THESIS_STATUS: NOT_EVALUATED (PENDING_MODEL_EXECUTION)");
    println!("BUDGET_BYTES: {BUDGET_BYTES} (identical for every arm)");
    println!("QUERIES: {} | CORPUS_DOCS: {}", queries.len(), docs.len());
    println!("SAMPLE_SIZE_STATUS: PILOT_ONLY_NOT_POWERED — no significance is claimed\n");

    let arms = ["B0", "B1", "B3", "B4", "B5"];
    let mut results: BTreeMap<(&str, String), Score> = BTreeMap::new();

    for q in &queries {
        for arm in arms {
            let ctx = match arm {
                "B0" => arm_b0(q),
                "B1" => arm_b1(&docs),
                "B3" => arm_b3(&derived, &vault, q),
                "B4" => arm_b4(&wiki),
                "B5" => arm_b5(&memories, q),
                _ => unreachable!(),
            };
            // Every baseline is checked for metadata leakage. B5 is exempt because
            // the metadata IS its arm.
            if arm != "B5" {
                assert_no_fehrest_metadata(arm, &ctx);
            }
            results.insert((arm, q.id.clone()), score(q, &ctx));
        }
    }

    // Per-query detail.
    println!("PER-QUERY ADEQUACY");
    println!(
        "{:<5} {:<14} {:>4} {:>4} {:>4} {:>4} {:>4}",
        "QRY", "CLASS", "B0", "B1", "B3", "B4", "B5"
    );
    for q in &queries {
        print!("{:<5} {:<14}", q.id, q.class);
        for arm in arms {
            let s = results[&(arm, q.id.clone())];
            print!(" {:>4}", if s.adequate { "OK" } else { "--" });
        }
        println!();
    }

    // Roll-up.
    println!("\nARM TOTALS");
    println!(
        "{:<5} {:>9} {:>12} {:>12}",
        "ARM", "ADEQUATE", "MISLEADING", "MEAN_BYTES"
    );
    for arm in arms {
        let ss: Vec<Score> = queries
            .iter()
            .map(|q| results[&(arm, q.id.clone())])
            .collect();
        let adequate = ss.iter().filter(|s| s.adequate).count();
        let misleading = ss.iter().filter(|s| s.misleading).count();
        let mean_bytes = ss.iter().map(|s| s.bytes).sum::<usize>() / ss.len();
        println!(
            "{:<5} {:>6}/{:<2} {:>9}/{:<2} {:>12}",
            arm,
            adequate,
            queries.len(),
            misleading,
            queries.len(),
            mean_bytes
        );
    }

    // Where each arm failed, and why. A total without the failures is not a result.
    println!("\nFAILURES BY ARM");
    for arm in arms {
        let fails: Vec<&Query> = queries
            .iter()
            .filter(|q| !results[&(arm, q.id.clone())].adequate)
            .collect();
        if fails.is_empty() {
            println!("  {arm}: none");
            continue;
        }
        println!("  {arm}:");
        for q in fails {
            let s = results[&(arm, q.id.clone())];
            let why = if !s.contains_correct && !q.must_contain.is_empty() {
                "missing the correct answer".to_string()
            } else if s.misleading {
                "stale material present with no label".to_string()
            } else if q.class == "ABSENT" && s.contains_stale {
                "offered plausible-looking material for a question nothing answers".to_string()
            } else if q.class == "CONTRADICTION" {
                "both claims present but the conflict is not marked".to_string()
            } else {
                format!(
                    "correct={} stale={} stale_labelled={}",
                    s.contains_correct, s.contains_stale, s.stale_is_labelled
                )
            };
            println!("    {} ({}) — {}", q.id, q.class, why);
        }
    }

    println!("\nREMINDER: adequacy is necessary, not sufficient. No thesis claim follows from these numbers.");

    drop(derived);
    drop(vault);
    let _ = fs::remove_dir_all(&work);
}
