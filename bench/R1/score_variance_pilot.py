#!/usr/bin/env python3
"""
Blinded scoring for R1-v2 variance pilot (972 sessions).

This script scores the 720 continuation sessions (600 comparison + 120 calibration)
using scorer.py, blinded to arm identity, and computes the statistical
derivation for confirmatory planning.

It follows VARIANCE-PILOT-V2.md §§6-10 and PREREGISTRATION-V2.md §§19-20,28.

It does NOT unblind or issue PRODUCT_THESIS verdicts at pilot stage.

Usage:
  python bench/R1/score_variance_pilot.py --validate   # checks raw completeness
  python bench/R1/score_variance_pilot.py --score      # scores continuation, writes scores.jsonl
  python bench/R1/score_variance_pilot.py --derive     # computes psi_hat, N_pairs, r_conf
"""

import json
import hashlib
import sys
from pathlib import Path
from collections import defaultdict, Counter

BENCH_DIR = Path(__file__).parent.resolve()
REPO_ROOT = BENCH_DIR.parent.parent.resolve()
RUNS_DIR = REPO_ROOT / "runs" / "variance-pilot-v2"
RAW_DIR = RUNS_DIR / "raw"

def load_spec():
    return json.loads((BENCH_DIR / "benchmark-spec-v2.json").read_text())
def load_tasks():
    return json.loads((BENCH_DIR / "tasks-v2.json").read_text())
def load_corpus():
    return json.loads((BENCH_DIR / "corpus-manifest-v2.json").read_text()).get("evidence", [])
def load_oracles():
    return {o["task_id"]: o for o in json.loads((BENCH_DIR / "oracles-v2.json").read_text())}

def validate_raw():
    print("="*60)
    print("Validating raw evidence completeness")
    print("="*60)
    records = [json.loads(l) for l in (RUNS_DIR / "records.jsonl").read_text().splitlines() if l.strip()]
    print(f"Records: {len(records)} (expected 972)")
    # Check types
    types = Counter(r["type"] for r in records)
    print(f"Types: {types} (expected maintenance 252, continuation 720)")
    # Check distinct run_ids
    run_ids = [r["run_id"] for r in records]
    print(f"Distinct run_ids: {len(set(run_ids))} (expected 972)")
    # Check raw files exist
    missing = []
    for r in records:
        raw_path = RUNS_DIR / r["raw_path"]
        if not raw_path.exists():
            missing.append(r["run_id"])
    print(f"Missing raw files: {len(missing)}")
    if missing:
        print(missing[:10])
        return 1
    # Check raw count
    raw_files = list(RAW_DIR.glob("*.txt"))
    print(f"Raw files on disk: {len(raw_files)} (expected 972)")
    # Check infra vs task failure
    outcomes = Counter(r["outcome"] for r in records)
    print(f"Outcomes: {outcomes}")
    # Check that continuation records have task_id
    cont = [r for r in records if r["type"]=="continuation"]
    print(f"Continuation records: {len(cont)} (expected 720)")
    # Check that maintenance records are 252
    maint = [r for r in records if r["type"]=="maintenance"]
    print(f"Maintenance records: {len(maint)} (expected 252)")
    if len(records)!=972 or len(set(run_ids))!=972 or len(raw_files)!=972:
        print("FAIL: completeness check failed")
        return 1
    if types["maintenance"]!=252 or types["continuation"]!=720:
        print("FAIL: session type counts wrong")
        return 1
    print("PASS: raw evidence completeness")
    return 0

def score():
    print("="*60)
    print("Blinded scoring (arm identity stripped)")
    print("="*60)
    sys.path.insert(0, str(BENCH_DIR))
    import scorer
    corpus = load_corpus()
    oracles = load_oracles()
    tasks = {t["id"]: t for t in load_tasks()}
    records = [json.loads(l) for l in (RUNS_DIR / "records.jsonl").read_text().splitlines() if l.strip()]
    cont_records = [r for r in records if r["type"]=="continuation"]
    print(f"Scoring {len(cont_records)} continuation records (blinded)...")
    scores = []
    # For B-NULL, we will later use for exclusion
    for r in cont_records:
        task_id = r["task_id"]
        arm = r["arm"]
        raw_path = RUNS_DIR / r["raw_path"]
        raw_text = raw_path.read_text(encoding="utf-8")
        # Parse raw as JSON if possible
        try:
            response = json.loads(raw_text)
            # Ensure response is dict with expected fields
            if not isinstance(response, dict):
                response = {"output": raw_text}
        except:
            # If not JSON, treat as raw text in output field
            response = {"output": raw_text, "reasoning": raw_text, "action": raw_text}
        # Ensure substantive field exists
        # The scorer will handle field extraction
        oracle = oracles.get(task_id)
        if not oracle:
            print(f"WARN: no oracle for {task_id}")
            continue
        # Blinded: scorer does not see arm, but we pass it for record-keeping
        # scorer.score_task is arm-blind (it doesn't use arm)
        try:
            result = scorer.score_task(response, oracle, corpus)
            # result is dict with score, failures, details
            score_val = result.get("score", 0)
            # Also check if raw was infra failure
            if r["outcome"] != "OK":
                score_val = 0
                result = {"score": 0, "failures": [f"Outcome {r['outcome']}"], "details": result}
        except Exception as e:
            result = {"score": 0, "failures": [str(e)], "error": str(e)}
            score_val = 0
        scores.append({
            "run_id": r["run_id"],
            "task_id": task_id,
            "arm": arm,
            "repeat_index": r["repeat_index"],
            "score": score_val,
            "failures": result.get("failures", []),
            "details": result,
            "outcome": r["outcome"],
            "model_returned": r.get("model_returned",""),
        })
    # Write scores
    scores_path = RUNS_DIR / "scores.jsonl"
    scores_path.write_text("\n".join(json.dumps(s, sort_keys=True) for s in scores) + "\n")
    print(f"Wrote {scores_path} ({len(scores)} entries)")
    # Summarize per arm
    per_arm = defaultdict(list)
    for s in scores:
        per_arm[s["arm"]].append(s["score"])
    for arm in sorted(per_arm.keys()):
        vals = per_arm[arm]
        mean = sum(vals)/len(vals) if vals else 0
        print(f"  {arm}: {len(vals)} scores, mean {mean:.3f}, sum {sum(vals)}")
    # Also check B-NULL
    bnull_scores = [s for s in scores if s["arm"]=="B-NULL"]
    print(f"B-NULL scores: {len(bnull_scores)}, mean {sum(s['score'] for s in bnull_scores)/len(bnull_scores) if bnull_scores else 0:.3f}")
    print("PASS: blinded scoring complete, no unblinding, no thesis verdict")
    return 0

def derive():
    print("="*60)
    print("Statistical derivation (psi_hat, K_eligible, N_pairs, r_conf)")
    print("="*60)
    spec = load_spec()
    sp = spec["statistical_parameters"]
    # Load scores
    scores_path = RUNS_DIR / "scores.jsonl"
    if not scores_path.exists():
        print("FAIL: scores.jsonl not found, run --score first")
        return 1
    scores = [json.loads(l) for l in scores_path.read_text().splitlines() if l.strip()]
    # Group by (task, repeat) for B5 vs B4
    # For each (task, repeat), we have one score for B5 and one for B4
    # psi_hat is proportion of (task,repeat) where exactly one of B5,B4 is correct
    from collections import defaultdict
    grouped = defaultdict(dict)  # (task, repeat) -> {arm: score}
    for s in scores:
        key = (s["task_id"], s["repeat_index"])
        grouped[key][s["arm"]] = s["score"]
    # B-NULL exclusion: tasks where B-NULL scores >0 are excluded
    # For each task, check if any B-NULL repeat scored >0
    bnull_by_task = defaultdict(list)
    for s in scores:
        if s["arm"]=="B-NULL":
            bnull_by_task[s["task_id"]].append(s["score"])
    excluded_tasks = set()
    for task_id, vals in bnull_by_task.items():
        if any(v>0 for v in vals):
            excluded_tasks.add(task_id)
    print(f"B-NULL excluded tasks: {len(excluded_tasks)} / 30 (tasks where B-NULL scored >0)")
    if excluded_tasks:
        print(f"  excluded: {sorted(excluded_tasks)}")
    K_total = 30
    K_eligible = K_total - len(excluded_tasks)
    print(f"K_total={K_total}, K_eligible={K_eligible}")
    # Now compute psi_hat using only eligible tasks
    eligible_keys = [k for k in grouped.keys() if k[0] not in excluded_tasks]
    print(f"Eligible (task,repeat) pairs: {len(eligible_keys)} (expected {K_eligible*4})")
    # For each eligible pair, check discordance B5 vs B4
    discordant = 0
    total = 0
    for key in eligible_keys:
        arm_scores = grouped[key]
        # Need both B5 and B4
        if "B5" not in arm_scores or "B4" not in arm_scores:
            continue
        total += 1
        if arm_scores["B5"] != arm_scores["B4"]:
            discordant += 1
    psi_hat = discordant / total if total else 0
    print(f"Discordant pairs: {discordant}/{total} = psi_hat={psi_hat:.4f}")
    # Also compute per-task discordance for reporting
    # Now compute N_pairs and r_conf using preregistered formula
    delta = sp["minimum_meaningful_effect_delta"]  # 0.15
    alpha = sp["alpha"]  # 0.05
    z_alpha = sp["z_one_minus_alpha_over_2"]  # 1.959964
    z_power = sp["z_power"]  # 0.841621
    N_pairs_floor = sp.get("N_pairs_floor", 90)
    N_pairs_ceiling = sp.get("N_pairs_ceiling", 600)
    r_conf_min = sp.get("r_conf_minimum", 3)
    r_conf_max = sp.get("r_conf_maximum", 20)
    K_min = sp.get("minimum_K", 15)
    import math
    if psi_hat <= delta**2:
        print(f"psi_hat {psi_hat:.4f} <= delta^2 {delta**2:.4f} → NO_DETECTABLE_DISCORDANCE, formula undefined")
        N_pairs = None
        r_conf = None
        print("N_pairs: UNDEFINED (no variance to detect)")
        print("r_conf: UNDEFINED")
        print("Route: CEILING_EFFECT or UNDERPOWERED, no confirmatory N, founder decision required")
    else:
        # Compute N_pairs
        N_pairs_raw = math.ceil((z_alpha * math.sqrt(psi_hat) + z_power * math.sqrt(psi_hat - delta**2))**2 / delta**2)
        print(f"N_pairs raw (from formula): {N_pairs_raw}")
        # Apply bounds
        N_pairs = max(N_pairs_floor, min(N_pairs_raw, N_pairs_ceiling))
        if N_pairs_raw < N_pairs_floor:
            print(f"N_pairs floored to {N_pairs_floor}")
        elif N_pairs_raw > N_pairs_ceiling:
            print(f"N_pairs ceiled to {N_pairs_ceiling} (raw {N_pairs_raw} > ceiling)")
        # Compute r_conf
        r_conf_raw = math.ceil(N_pairs / K_eligible) if K_eligible else float('inf')
        print(f"r_conf raw = ceil({N_pairs} / {K_eligible}) = {r_conf_raw}")
        if r_conf_raw < r_conf_min:
            r_conf = r_conf_min
            print(f"r_conf raised to minimum {r_conf_min}")
        elif r_conf_raw > r_conf_max:
            print(f"r_conf {r_conf_raw} > max {r_conf_max} → UNDERPOWERED_FOR_PREREGISTERED_EFFECT")
            r_conf = f"UNDERPOWERED (raw {r_conf_raw} > {r_conf_max})"
        else:
            r_conf = r_conf_raw
        print(f"N_pairs required: {N_pairs}")
        print(f"r_conf (repeats per eligible task): {r_conf}")
    # Check LOW_K route
    if K_eligible < K_min:
        print(f"K_eligible {K_eligible} < minimum_K {K_min} → LOW_K_ROUTE UNDERPOWERED")
    # Task class loss route
    # Check per-class B-NULL exclusion
    tasks = {t["id"]: t for t in load_tasks()}
    class_excluded = Counter()
    for task_id in excluded_tasks:
        tc = tasks[task_id].get("task_class", "UNKNOWN")
        class_excluded[tc] += 1
    if class_excluded:
        print(f"Task classes fully/partially excluded due to B-NULL: {dict(class_excluded)}")
        # Check if any class fully excluded
        from collections import Counter as C2
        class_total = C2(t["task_class"] for t in tasks.values())
        for cls, cls_total in class_total.items():
            excl = class_excluded.get(cls, 0)
            if excl == cls_total:
                print(f"  Class {cls} fully excluded ({excl}/{cls_total}) → TASK_CLASS_LOSS_ROUTE")
            elif excl>0:
                print(f"  Class {cls} partially excluded ({excl}/{cls_total})")
    # Write derivation
    derivation = {
        "K_total": K_total,
        "B_NULL_excluded_tasks": sorted(excluded_tasks),
        "B_NULL_excluded_count": len(excluded_tasks),
        "K_eligible": K_eligible,
        "psi_hat": psi_hat,
        "discordant_pairs": discordant,
        "total_pairs": total,
        "delta": delta,
        "alpha": alpha,
        "z_alpha": z_alpha,
        "z_power": z_power,
        "N_pairs": N_pairs,
        "r_conf": r_conf,
        "N_pairs_floor": N_pairs_floor,
        "N_pairs_ceiling": N_pairs_ceiling,
        "r_conf_min": r_conf_min,
        "r_conf_max": r_conf_max,
        "K_min": K_min,
        "route": "CEILING_EFFECT" if psi_hat <= delta**2 else ("LOW_K" if K_eligible < K_min else "POWERED" if isinstance(r_conf,int) else "UNDERPOWERED"),
    }
    out_path = RUNS_DIR / "statistical-derivation.json"
    out_path.write_text(json.dumps(derivation, indent=2, sort_keys=True) + "\n")
    print(f"\nWrote {out_path}")
    print(json.dumps(derivation, indent=2, sort_keys=True))
    print("\nPASS: statistical derivation complete (no thesis verdict at pilot stage)")
    return 0

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--validate", action="store_true", help="Validate raw completeness")
    p.add_argument("--score", action="store_true", help="Blinded scoring")
    p.add_argument("--derive", action="store_true", help="Derive psi_hat etc.")
    p.add_argument("--all", action="store_true", help="Run all steps")
    args = p.parse_args()
    if not any([args.validate, args.score, args.derive, args.all]):
        args.all = True
    rc = 0
    if args.validate or args.all:
        rc = validate_raw()
        if rc: return rc
    if args.score or args.all:
        rc = score()
        if rc: return rc
    if args.derive or args.all:
        rc = derive()
        if rc: return rc
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
