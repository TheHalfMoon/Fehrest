#!/usr/bin/env python3
"""R1-v2 deterministic scorer.

Arm-blind, field-scored, deterministic adjudication.
Supports v1 field types plus v2 additions:
- require_synthesis: verifies facts from multiple checkpoints
- require_epoch: verifies epoch boundary identification
"""

import json
import re
from pathlib import Path


class ScorerError(Exception):
    pass


def normalize(text):
    """Normalize text for comparison: lowercase, collapse whitespace, strip punctuation."""
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


def field_value(response, field):
    """Get a field value from a response, handling nested paths."""
    if '.' in field:
        parts = field.split('.')
        current = response
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current
    return response.get(field)


def check_require_all(response, require_all):
    """Check that all required field conditions are met."""
    failures = []
    for req in require_all:
        field = req["field"]
        value = field_value(response, field)
        if value is None:
            failures.append(f"Field '{field}' is missing")
            continue

        if "contains" in req:
            normalized_value = normalize(str(value))
            normalized_contains = normalize(req["contains"])
            if normalized_contains not in normalized_value:
                failures.append(f"Field '{field}' does not contain '{req['contains']}'")

        if "equals" in req:
            if value != req["equals"]:
                failures.append(f"Field '{field}' value '{value}' != expected '{req['equals']}'")

    return len(failures) == 0, failures


def check_forbid(response, forbid):
    """Check that no forbidden field conditions are met."""
    failures = []
    for f in forbid:
        field = f["field"]
        value = field_value(response, field)
        if value is None:
            continue

        if "contains" in f:
            normalized_value = normalize(str(value))
            normalized_contains = normalize(f["contains"])
            if normalized_contains in normalized_value:
                failures.append(f"Field '{field}' contains forbidden term '{f['contains']}'")

        if "equals" in f:
            if value == f["equals"]:
                failures.append(f"Field '{field}' has forbidden value '{value}'")

    return len(failures) == 0, failures


def check_abstention(response, abstention_ok, abstention_required):
    """Check abstention rules."""
    failures = []
    ab_value = field_value(response, "abstain")

    if abstention_required:
        if not ab_value or str(ab_value).upper() not in ("YES", "TRUE", "1"):
            failures.append("Abstention required but ABSTAIN is not YES")
    else:
        if ab_value and str(ab_value).upper() in ("YES", "TRUE", "1"):
            failures.append("Abstention not allowed but ABSTAIN is YES")

    return len(failures) == 0, failures


def check_substantive(response, min_action_chars=10):
    """Check that response has substantive content."""
    failures = []

    # Check for non-empty action field first
    action = field_value(response, "action")
    if action and len(str(action).strip()) >= min_action_chars:
        return True, []

    # If action is missing/short, check other fields
    has_substantive = False
    for key, value in response.items():
        if value and isinstance(value, str) and len(value.strip()) >= min_action_chars:
            has_substantive = True
            break
        if value and isinstance(value, list) and len(value) > 0:
            has_substantive = True
            break

    if not has_substantive:
        failures.append(f"Response too short or empty (min {min_action_chars} chars)")

    return len(failures) == 0, failures


def check_require_synthesis(response, require_synthesis, corpus):
    """Check that response synthesizes facts from multiple checkpoints."""
    failures = []

    if not require_synthesis:
        return True, []

    min_checkpoints = require_synthesis.get("min_checkpoints", 2)
    required_checkpoints = require_synthesis.get("required_checkpoints", [])

    # Extract checkpoint references from response
    response_text = json.dumps(response).lower()
    checkpoint_refs = set()

    for match in re.findall(r't(\d+)', response_text):
        checkpoint_refs.add(int(match))
    for match in re.findall(r'checkpoint\s+(\d+)', response_text):
        checkpoint_refs.add(int(match))

    if len(checkpoint_refs) < min_checkpoints:
        failures.append(
            f"Require synthesis: references {len(checkpoint_refs)} checkpoints, "
            f"need at least {min_checkpoints}"
        )

    for cp in required_checkpoints:
        if cp not in checkpoint_refs:
            failures.append(f"Require synthesis: checkpoint {cp} not referenced")

    return len(failures) == 0, failures


def check_require_epoch(response, require_epoch, corpus):
    """Check that response correctly identifies epoch boundary."""
    failures = []

    if not require_epoch:
        return True, []

    epochs = require_epoch.get("epochs", [])
    must_identify = require_epoch.get("must_identify")

    response_text = json.dumps(response).lower()

    for epoch in epochs:
        if epoch.lower() not in response_text:
            failures.append(f"Require epoch: epoch '{epoch}' not identified")

    if must_identify:
        if must_identify.lower() not in response_text:
            failures.append(f"Require epoch: required identification '{must_identify}' missing")

    return len(failures) == 0, failures


def score_task(response, oracle, corpus=None):
    """Score a single task response against its oracle."""
    if corpus is None:
        corpus = {}

    all_failures = []
    details = {}

    # 1. Check substantive
    sub_ok, sub_failures = check_substantive(response)
    details["substantive"] = {"passed": sub_ok, "failures": sub_failures}
    all_failures.extend(sub_failures)

    # 2. Check require_all
    req_ok, req_failures = check_require_all(response, oracle.get("require_all", []))
    details["require_all"] = {"passed": req_ok, "failures": req_failures}
    all_failures.extend(req_failures)

    # 3. Check forbid
    forbid_ok, forbid_failures = check_forbid(response, oracle.get("forbid", []))
    details["forbid"] = {"passed": forbid_ok, "failures": forbid_failures}
    all_failures.extend(forbid_failures)

    # 4. Check abstention
    abstention_required = oracle.get("abstention_ok", False)
    abst_ok, abst_failures = check_abstention(
        response,
        abstention_ok=oracle.get("abstention_ok", False),
        abstention_required=abstention_required
    )
    details["abstention"] = {"passed": abst_ok, "failures": abst_failures}
    all_failures.extend(abst_failures)

    # 5. Check require_synthesis (v2)
    synth_ok, synth_failures = check_require_synthesis(
        response, oracle.get("require_synthesis"), corpus
    )
    details["require_synthesis"] = {"passed": synth_ok, "failures": synth_failures}
    all_failures.extend(synth_failures)

    # 6. Check require_epoch (v2)
    epoch_ok, epoch_failures = check_require_epoch(
        response, oracle.get("require_epoch"), corpus
    )
    details["require_epoch"] = {"passed": epoch_ok, "failures": epoch_failures}
    all_failures.extend(epoch_failures)

    score = 1 if len(all_failures) == 0 else 0

    return {
        "score": score,
        "failures": all_failures,
        "details": details,
    }


def load_oracles(path):
    """Load oracles from JSON file, indexed by oracle ID."""
    with open(path) as f:
        oracles = json.load(f)
    return {o["id"]: o for o in oracles}


def load_corpus(path):
    """Load corpus manifest."""
    with open(path) as f:
        return json.load(f)


def main():
    """CLI entry point for the scorer."""
    import argparse

    parser = argparse.ArgumentParser(description="R1-v2 deterministic scorer")
    parser.add_argument("--oracles", type=Path, required=True, help="Path to oracles-v2.json")
    parser.add_argument("--corpus", type=Path, default=None, help="Path to corpus-manifest-v2.json")
    parser.add_argument("--response", type=str, required=True, help="JSON response string or @file.json")
    parser.add_argument("--oracle-id", type=str, required=True, help="Oracle ID to score against")

    args = parser.parse_args()

    oracles = load_oracles(args.oracles)
    corpus = load_corpus(args.corpus) if args.corpus else {}

    if args.oracle_id not in oracles:
        print(f"Error: Oracle '{args.oracle_id}' not found", file=sys.stderr)
        sys.exit(1)

    oracle = oracles[args.oracle_id]

    response_str = args.response
    if response_str.startswith("@"):
        response_path = Path(response_str[1:])
        with open(response_path) as f:
            response = json.load(f)
    else:
        response = json.loads(response_str)

    result = score_task(response, oracle, corpus)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["score"] == 1 else 1)


if __name__ == "__main__":
    import sys
    main()
