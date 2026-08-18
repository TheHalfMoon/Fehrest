//! Minimal headless CLI. Hand dispatch — ten subcommands do not justify a
//! command-line framework and its proc-macro tree (Ponytail DELETE: `clap`).

use crate::context::{self, CompileRequest, SourceItem};
use crate::derived::Derived;
use crate::envelope::TrustLevel;
use crate::events::{ChainStatus, EventKind, EventLog};
use crate::memory::Scope;
use crate::vault::Vault;
use crate::{limits, Result};
use std::path::PathBuf;

pub const USAGE: &str = "\
fehrest — Phase T headless thesis-proof (EXPERIMENTAL, not a product)

USAGE:
  fehrest <command> --vault <path> [options]

COMMANDS:
  init              Create a vault
  add               Add a canonical object      --path <rel> --body <text> [--title T] [--project P]
  scan              List admitted objects, conflicts and exclusions
  rebuild           Rebuild derived state from canonical state
  search            Lexical candidate search     --query <text> [--limit N]
  read              Read an object by id         --id <uuid>
  compile           Compile a context package    [--project P] [--budget BYTES] [--as-of DAY]
  manifest          Show the last package manifest
  events            Show the event log
  verify            Verify the event chain
";

struct Args {
    vault: Option<PathBuf>,
    flags: std::collections::HashMap<String, String>,
}

fn parse_args(argv: &[String]) -> Args {
    let mut flags = std::collections::HashMap::new();
    let mut i = 0;
    while i < argv.len() {
        if let Some(name) = argv[i].strip_prefix("--") {
            let value = argv.get(i + 1).cloned().unwrap_or_default();
            if value.starts_with("--") {
                flags.insert(name.to_string(), String::new());
                i += 1;
            } else {
                flags.insert(name.to_string(), value);
                i += 2;
            }
        } else {
            i += 1;
        }
    }
    Args {
        vault: flags.get("vault").map(PathBuf::from),
        flags,
    }
}

impl Args {
    fn get(&self, k: &str) -> Option<&str> {
        self.flags
            .get(k)
            .map(String::as_str)
            .filter(|s| !s.is_empty())
    }
    fn require(&self, k: &str) -> Result<&str> {
        self.get(k)
            .ok_or_else(|| crate::Error::Vault(format!("missing required --{k}")))
    }
    fn vault_root(&self) -> Result<&PathBuf> {
        self.vault
            .as_ref()
            .ok_or_else(|| crate::Error::Vault("missing required --vault".into()))
    }
}

pub fn run(argv: &[String]) -> Result<i32> {
    if argv.is_empty() || argv[0] == "--help" || argv[0] == "-h" {
        println!("{USAGE}");
        return Ok(0);
    }
    let cmd = argv[0].as_str();
    let args = parse_args(&argv[1..]);

    match cmd {
        "init" => {
            let root = args.vault_root()?;
            let v = Vault::create(root)?;
            let log = EventLog::open(&v.control_dir())?;
            log.append(EventKind::VaultCreated, &root.display().to_string(), "")?;
            Derived::open(&v.control_dir())?;
            println!("vault created: {}", root.display());
            Ok(0)
        }

        "add" => {
            let v = Vault::open_write(args.vault_root()?)?;
            let id = v.add_object(
                args.require("path")?,
                args.get("title"),
                args.get("project"),
                args.require("body")?,
            )?;
            let log = EventLog::open(&v.control_dir())?;
            log.append(
                EventKind::ObjectRegistered,
                &id.to_string(),
                args.require("path")?,
            )?;
            println!("{id}");
            Ok(0)
        }

        "scan" => {
            let v = Vault::open_read(args.vault_root()?)?;
            let scan = v.scan()?;
            println!("objects: {}", scan.objects.len());
            for o in &scan.objects {
                println!("  {} {}", o.id, o.rel_path);
            }
            if !scan.conflicts.is_empty() {
                println!("CONFLICTS (both retained, neither discarded):");
                for (id, paths) in &scan.conflicts {
                    println!("  {id} at {paths:?}");
                }
            }
            if !scan.malformed.is_empty() {
                println!("malformed:");
                for (p, why) in &scan.malformed {
                    println!("  {p}: {why}");
                }
            }
            println!("excluded (unsupported or reserved): {}", scan.skipped.len());
            Ok(if scan.conflicts.is_empty() { 0 } else { 2 })
        }

        "rebuild" => {
            let v = Vault::open_write(args.vault_root()?)?;
            let scan = v.scan()?;
            let d = Derived::open(&v.control_dir())?;
            let n = d.rebuild(&scan.objects)?;
            println!("rebuilt derived index: {n} objects");
            Ok(0)
        }

        "search" => {
            let v = Vault::open_read(args.vault_root()?)?;
            let d = Derived::open(&v.control_dir())?;
            let limit = args
                .get("limit")
                .and_then(|s| s.parse().ok())
                .unwrap_or(20usize);
            for c in d.search(args.require("query")?, limit)? {
                println!("{} {}", c.id, c.rel_path);
            }
            Ok(0)
        }

        "read" => {
            let v = Vault::open_read(args.vault_root()?)?;
            let id = crate::identity::ObjectId::parse(args.require("id")?)?;
            let d = Derived::open(&v.control_dir())?;
            // The index supplies an untrusted locator hint; the read is confined
            // and identity-verified before anything is returned.
            let hits = d.search(args.get("query").unwrap_or(""), limits::MAX_SEARCH_RESULTS)?;
            let hint = hits
                .iter()
                .find(|c| c.id == id)
                .map(|c| c.rel_path.clone())
                .or_else(|| {
                    v.scan().ok().and_then(|s| {
                        s.objects
                            .iter()
                            .find(|o| o.id == id)
                            .map(|o| o.rel_path.clone())
                    })
                })
                .ok_or_else(|| crate::Error::Vault(format!("object not found: {id}")))?;
            let content = crate::locator::read_verified(v.root(), &hint, id)?;
            print!("{content}");
            Ok(0)
        }

        "compile" => {
            let v = Vault::open_write(args.vault_root()?)?;
            let scan = v.scan()?;
            let scope = match args.get("project") {
                Some(p) => Scope::project("vault", p),
                None => Scope::vault_global("vault"),
            };
            let budget = args
                .get("budget")
                .and_then(|s| s.parse().ok())
                .unwrap_or(limits::MAX_PACKAGE_BYTES);
            let as_of = args
                .get("as-of")
                .and_then(|s| s.parse().ok())
                .unwrap_or(i64::MAX);

            let items: Vec<SourceItem> = scan
                .objects
                .iter()
                .map(|o| SourceItem {
                    section: "project_state",
                    item_id: o.id.to_string(),
                    content: o.body.clone(),
                    source_content_hash: o.content_hash.clone(),
                    trust_level: TrustLevel::VaultKnowledge,
                    memory: None,
                    superseded_by: None,
                })
                .collect();

            let req = CompileRequest {
                principal: "agent:cli".into(),
                scope,
                as_of_valid: as_of,
                as_of_recorded: u64::MAX,
                budget_bytes: budget,
            };
            let pkg = context::compile(&req, &items);
            let manifest_path = v.control_dir().join("last-manifest.json");
            std::fs::write(
                &manifest_path,
                serde_json::to_string_pretty(&pkg.manifest)
                    .map_err(|e| crate::Error::Derived(e.to_string()))?,
            )
            .map_err(|e| crate::Error::Vault(format!("cannot write manifest: {e}")))?;

            let log = EventLog::open(&v.control_dir())?;
            log.append(
                EventKind::ContextCompiled,
                &pkg.manifest.context_id,
                &format!(
                    "items={} omitted={} digest={}",
                    pkg.manifest.entries.len(),
                    pkg.manifest.omissions.len(),
                    pkg.manifest.package_digest
                ),
            )?;
            print!("{}", pkg.wire);
            Ok(0)
        }

        "manifest" => {
            let v = Vault::open_read(args.vault_root()?)?;
            let p = v.control_dir().join("last-manifest.json");
            let text = std::fs::read_to_string(&p)
                .map_err(|e| crate::Error::Vault(format!("no manifest yet: {e}")))?;
            println!("{text}");
            Ok(0)
        }

        "events" => {
            let v = Vault::open_read(args.vault_root()?)?;
            let log = EventLog::open(&v.control_dir())?;
            for e in log.read_all()? {
                println!("{:>4} {:?} {} {}", e.seq, e.kind, e.subject, e.detail);
            }
            Ok(0)
        }

        "verify" => {
            let v = Vault::open_read(args.vault_root()?)?;
            let log = EventLog::open(&v.control_dir())?;
            match log.verify()? {
                ChainStatus::Intact { events } => {
                    println!("chain intact: {events} events");
                    // Stated at the point of use, not only in documentation.
                    println!(
                        "note: unkeyed chain — partial-tamper evidence only, NOT authentication"
                    );
                    Ok(0)
                }
                ChainStatus::Broken { at_seq, reason } => {
                    eprintln!("CHAIN BROKEN at seq {at_seq}: {reason}");
                    Ok(3)
                }
                ChainStatus::Gap { from_seq, to_seq } => {
                    eprintln!("CHAIN GAP: expected {from_seq}, found {to_seq}");
                    Ok(3)
                }
            }
        }

        other => {
            eprintln!("unknown command: {other}\n\n{USAGE}");
            Ok(64)
        }
    }
}
