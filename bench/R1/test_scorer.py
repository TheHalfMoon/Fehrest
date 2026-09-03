#!/usr/bin/env python3
"""Focused tests for the R1-v2 scorer."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scorer import score_task, normalize, check_require_synthesis, check_require_epoch


def test_positive_case():
    oracle = {
        "id": "test-pos", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "action", "contains": "schema registry"}],
        "forbid": [{"field": "action", "contains": "ignore"}], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "Add schema registry to the pipeline", "reasoning": "Required for type safety"}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected score 1, got {result['score']}: {result['failures']}"
    print("PASS: test_positive_case")


def test_negative_case():
    oracle = {
        "id": "test-neg", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "action", "contains": "schema registry"}],
        "forbid": [], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "Ignore the requirement", "reasoning": "Not needed"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected score 0, got {result['score']}"
    print("PASS: test_negative_case")


def test_field_scoping():
    oracle = {
        "id": "test-scope", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "action", "contains": "correct"}],
        "forbid": [{"field": "action", "contains": "wrong"}], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "Take correct action", "reasoning": "Not wrong to do this"}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1 (field scoping), got {result['score']}: {result['failures']}"
    response = {"action": "This is wrong", "reasoning": "None"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (wrong in action), got {result['score']}"
    print("PASS: test_field_scoping")


def test_wrong_field_content():
    oracle = {
        "id": "test-wrong", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "action", "contains": "hash"}, {"field": "reasoning", "contains": "PII"}],
        "forbid": [], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "Hash the data", "reasoning": "For security"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (missing PII in reasoning), got {result['score']}"
    response = {"action": "Hash the data", "reasoning": "PII must be protected"}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1, got {result['score']}: {result['failures']}"
    print("PASS: test_wrong_field_content")


def test_determinism():
    oracle = {
        "id": "test-det", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "action", "contains": "correct"}],
        "forbid": [], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "This is correct"}
    results = [score_task(response, oracle) for _ in range(10)]
    scores = [r["score"] for r in results]
    assert all(s == scores[0] for s in scores), f"Non-deterministic: {scores}"
    print("PASS: test_determinism")


def test_malformed_response():
    oracle = {
        "id": "test-mal", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "action", "contains": "required"}],
        "forbid": [], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 for empty response, got {result['score']}"
    response = {"reasoning": "I don't know"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 for missing field, got {result['score']}"
    print("PASS: test_malformed_response")


def test_empty_response():
    oracle = {
        "id": "test-empty", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [], "forbid": [], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 for empty response, got {result['score']}"
    print("PASS: test_empty_response")


def test_abstention_interaction():
    oracle_non_abstain = {
        "id": "test-abst-1", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [], "forbid": [], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "Some action that is long enough", "abstain": "YES"}
    result = score_task(response, oracle_non_abstain)
    assert result["score"] == 0, f"Expected 0 (abstain not allowed), got {result['score']}"

    oracle_abstain = {
        "id": "test-abst-2", "task_id": "test-task", "derivation_evidence": [],
        "require_all": [{"field": "abstain", "equals": True}],
        "forbid": [], "abstention_ok": True,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": [], "stale_facts": [], "correct_facts": [],
    }
    response = {"action": "I cannot answer this question", "abstain": True}
    result = score_task(response, oracle_abstain)
    assert result["score"] == 1, f"Expected 1 (abstain allowed), got {result['score']}: {result['failures']}"

    response = {"abstain": "YES"}
    result = score_task(response, oracle_abstain)
    assert result["score"] == 0, f"Expected 0 (bare abstain), got {result['score']}"
    print("PASS: test_abstention_interaction")


def test_provenance_interaction():
    oracle = {
        "id": "test-prov", "task_id": "test-task", "derivation_evidence": ["S1-T4-ADR-020"],
        "require_all": [{"field": "evidence_id", "equals": "S1-T4-ADR-020"}],
        "forbid": [{"field": "evidence_id", "contains": "S2-"}, {"field": "evidence_id", "contains": "S3-"}],
        "abstention_ok": False, "require_synthesis": None, "require_epoch": None,
        "provenance_required": True, "trap_present": ["S2-T4-ADR-010", "S3-T4-ADR-005"],
        "stale_facts": [], "correct_facts": ["S1-T4-ADR-020"],
    }
    response = {"action": "Apply 30-day retention", "evidence_id": "S1-T4-ADR-020"}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1, got {result['score']}: {result['failures']}"
    response = {"action": "Apply 90-day retention", "evidence_id": "S2-T4-ADR-010"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (trap), got {result['score']}"
    print("PASS: test_provenance_interaction")


def test_stale_answer_rejection():
    oracle = {
        "id": "test-stale", "task_id": "test-task", "derivation_evidence": ["S1-T1-DEC-002"],
        "require_all": [{"field": "answer", "contains": "Protobuf"}],
        "forbid": [{"field": "answer", "contains": "JSON"}], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": ["S1-T0-DEC-002"], "stale_facts": ["S1-T0-DEC-002"],
        "correct_facts": ["S1-T1-DEC-002"],
    }
    response = {"answer": "Protobuf", "reasoning": "Current format"}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1, got {result['score']}: {result['failures']}"
    response = {"answer": "JSON", "reasoning": "Original format"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (stale), got {result['score']}"
    print("PASS: test_stale_answer_rejection")


def test_cross_file_synthesis_false_positive():
    oracle = {
        "id": "test-synth-fp", "task_id": "test-task", "derivation_evidence": ["S1-T0-CON-001", "S1-T11-DEC-001", "S1-T12-DEC-001"],
        "require_all": [{"field": "action", "contains": "hash"}, {"field": "action", "contains": "encrypt"}],
        "forbid": [], "abstention_ok": False,
        "require_synthesis": {"min_checkpoints": 3, "required_checkpoints": [0, 11, 12]},
        "require_epoch": None, "provenance_required": False, "trap_present": [],
        "stale_facts": [], "correct_facts": ["S1-T0-CON-001", "S1-T11-DEC-001"],
    }
    response = {"action": "Hash and encrypt", "reasoning": "From t0 and t11"}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (missing t12), got {result['score']}"
    print("PASS: test_cross_file_synthesis_false_positive")


def test_cross_file_synthesis_true_positive():
    oracle = {
        "id": "test-synth-tp", "task_id": "test-task", "derivation_evidence": ["S1-T0-CON-001", "S1-T11-DEC-001", "S1-T12-DEC-001"],
        "require_all": [{"field": "action", "contains": "hash"}, {"field": "action", "contains": "encrypt"}],
        "forbid": [], "abstention_ok": False,
        "require_synthesis": {"min_checkpoints": 3, "required_checkpoints": [0, 11, 12]},
        "require_epoch": None, "provenance_required": False, "trap_present": [],
        "stale_facts": [], "correct_facts": ["S1-T0-CON-001", "S1-T11-DEC-001"],
    }
    response = {"action": "Hash PII and encrypt at rest", "reasoning": "t0 PII constraint, t11 encryption, t12 config"}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1, got {result['score']}: {result['failures']}"
    print("PASS: test_cross_file_synthesis_true_positive")


def test_epoch_false_positive():
    oracle = {
        "id": "test-epoch-fp", "task_id": "test-task", "derivation_evidence": ["S1-T0-DEC-001", "S1-T0-DEC-002", "S1-T5-DEP-001", "S1-T10-DEP-001"],
        "require_all": [
            {"field": "valid_decisions", "contains": "S1-T0-DEC-001"},
            {"field": "deprecated_decisions", "contains": "S1-T0-DEC-002"},
        ],
        "forbid": [], "abstention_ok": False, "require_synthesis": None,
        "require_epoch": {"epochs": ["foundation", "maturity"], "must_identify": "S1-T5-DEP-001"},
        "provenance_required": False, "trap_present": ["S1-T5-DEP-001"],
        "stale_facts": ["S1-T0-DEC-002"], "correct_facts": ["S1-T0-DEC-001", "S1-T10-DEP-001"],
    }
    response = {
        "valid_decisions": ["S1-T0-DEC-001"],
        "deprecated_decisions": ["S1-T0-DEC-002"],
        "reasoning": "Foundation to maturity transition",
    }
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (missing deprecation ID), got {result['score']}"
    print("PASS: test_epoch_false_positive")


def test_epoch_true_positive():
    oracle = {
        "id": "test-epoch-tp", "task_id": "test-task", "derivation_evidence": ["S1-T0-DEC-001", "S1-T0-DEC-002", "S1-T5-DEP-001", "S1-T10-DEP-001"],
        "require_all": [
            {"field": "valid_decisions", "contains": "S1-T0-DEC-001"},
            {"field": "deprecated_decisions", "contains": "S1-T0-DEC-002"},
        ],
        "forbid": [], "abstention_ok": False, "require_synthesis": None,
        "require_epoch": {"epochs": ["foundation", "maturity"], "must_identify": "S1-T5-DEP-001"},
        "provenance_required": False, "trap_present": ["S1-T5-DEP-001"],
        "stale_facts": ["S1-T0-DEC-002"], "correct_facts": ["S1-T0-DEC-001", "S1-T10-DEP-001"],
    }
    response = {
        "valid_decisions": ["S1-T0-DEC-001"],
        "deprecated_decisions": ["S1-T0-DEC-002"],
        "reasoning": "Foundation to maturity: S1-T5-DEP-001 deprecated JSON",
    }
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1, got {result['score']}: {result['failures']}"
    print("PASS: test_epoch_true_positive")


def test_historical_cutoff_behavior():
    oracle = {
        "id": "test-hist", "task_id": "test-task", "derivation_evidence": ["S1-T1-DEC-002"],
        "require_all": [{"field": "answer", "contains": "Protobuf"}, {"field": "as_of_checkpoint", "equals": 1}],
        "forbid": [{"field": "answer", "contains": "JSON"}], "abstention_ok": False,
        "require_synthesis": None, "require_epoch": None, "provenance_required": False,
        "trap_present": ["S1-T7-DEC-001"], "stale_facts": [], "correct_facts": ["S1-T1-DEC-002"],
    }
    response = {"answer": "Protocol Buffers (Protobuf)", "as_of_checkpoint": 1}
    result = score_task(response, oracle)
    assert result["score"] == 1, f"Expected 1, got {result['score']}: {result['failures']}"
    response = {"answer": "Protocol Buffers (Protobuf)", "as_of_checkpoint": 7}
    result = score_task(response, oracle)
    assert result["score"] == 0, f"Expected 0 (wrong checkpoint), got {result['score']}"
    print("PASS: test_historical_cutoff_behavior")


def test_normalize():
    assert normalize("Hello World!") == "hello world"
    assert normalize("  Multiple   Spaces  ") == "multiple spaces"
    assert normalize("") == ""
    assert normalize("UPPERCASE") == "uppercase"
    print("PASS: test_normalize")


def test_check_require_synthesis():
    oracle = {"require_synthesis": {"min_checkpoints": 3, "required_checkpoints": [0, 11, 12]}}
    response = {"reasoning": "From t0 and t11 and t12"}
    ok, failures = check_require_synthesis(response, oracle["require_synthesis"], {})
    assert ok, f"Expected pass, got failures: {failures}"
    response = {"reasoning": "From t0 and t11"}
    ok, failures = check_require_synthesis(response, oracle["require_synthesis"], {})
    assert not ok, "Expected failure for missing t12"
    print("PASS: test_check_require_synthesis")


def test_check_require_epoch():
    oracle = {"require_epoch": {"epochs": ["foundation", "maturity"], "must_identify": "S1-T5-DEP-001"}}
    response = {"reasoning": "Foundation to maturity: S1-T5-DEP-001 deprecated"}
    ok, failures = check_require_epoch(response, oracle["require_epoch"], {})
    assert ok, f"Expected pass, got failures: {failures}"
    response = {"reasoning": "Foundation to maturity transition"}
    ok, failures = check_require_epoch(response, oracle["require_epoch"], {})
    assert not ok, "Expected failure for missing deprecation ID"
    print("PASS: test_check_require_epoch")


def run_all_tests():
    tests = [
        test_positive_case, test_negative_case, test_field_scoping,
        test_wrong_field_content, test_determinism, test_malformed_response,
        test_empty_response, test_abstention_interaction, test_provenance_interaction,
        test_stale_answer_rejection, test_cross_file_synthesis_false_positive,
        test_cross_file_synthesis_true_positive, test_epoch_false_positive,
        test_epoch_true_positive, test_historical_cutoff_behavior, test_normalize,
        test_check_require_synthesis, test_check_require_epoch,
    ]

    passed = 0
    failed = 0
    errors = []

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            errors.append(f"FAIL: {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            errors.append(f"ERROR: {test.__name__}: {e}")

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    if errors:
        for e in errors:
            print(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
