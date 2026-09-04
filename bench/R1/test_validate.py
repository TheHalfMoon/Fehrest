#!/usr/bin/env python3
"""Complete test suite for bench/R1/validate.py."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import Validator

BENCH_DIR = Path(__file__).parent

def load_artifacts():
    with open(BENCH_DIR / "benchmark-spec-v2.json") as f:
        spec = json.loads(f.read())
    with open(BENCH_DIR / "tasks-v2.json") as f:
        tasks = json.loads(f.read())
    with open(BENCH_DIR / "oracles-v2.json") as f:
        oracles = json.loads(f.read())
    with open(BENCH_DIR / "corpus-manifest-v2.json") as f:
        corpus = json.loads(f.read())
    return spec, tasks, oracles, corpus

class TestCanonicalValidation(unittest.TestCase):
    def setUp(self):
        self.spec, self.tasks, self.oracles, self.corpus = load_artifacts()
        self.validator = Validator()
    def test_validate_returns_true(self):
        self.assertTrue(self.validator.validate())
    def test_no_errors_on_canonical(self):
        self.assertEqual(len(self.validator.errors), 0)
    def test_task_counts(self):
        self.assertEqual(len(self.tasks), 30)
        self.assertEqual(len(self.oracles), 30)
    def test_corpus_evidence_count(self):
        self.assertEqual(len(self.corpus.get("evidence", [])), 96)
    def test_distinct_checkpoints(self):
        checkpoints = {t["checkpoint"] for t in self.tasks}
        self.assertEqual(len(checkpoints), 12)
    def test_tasks_before_t14(self):
        pre_t14 = sum(1 for t in self.tasks if t["checkpoint"] < 14)
        self.assertEqual(pre_t14, 27)
    def test_task_classes(self):
        classes = {t["task_class"] for t in self.tasks}
        self.assertEqual(len(classes), 12)

class TestCanonicalDerivedEquality(unittest.TestCase):
    def setUp(self):
        self.spec, self.tasks, self.oracles, self.corpus = load_artifacts()
    def test_tasks_identical(self):
        spec_tasks = sorted(json.dumps(t, sort_keys=True) for t in self.spec["tasks"])
        task_list = sorted(json.dumps(t, sort_keys=True) for t in self.tasks)
        self.assertEqual(spec_tasks, task_list)
    def test_oracles_identical(self):
        spec_oracles = sorted(json.dumps(o, sort_keys=True) for o in self.spec["oracles"])
        oracle_list = sorted(json.dumps(o, sort_keys=True) for o in self.oracles)
        self.assertEqual(spec_oracles, oracle_list)
    def test_corpus_identical(self):
        spec_corpus = sorted(json.dumps(e, sort_keys=True) for e in self.spec["corpus"])
        corpus_list = sorted(json.dumps(e, sort_keys=True) for e in self.corpus["evidence"])
        self.assertEqual(spec_corpus, corpus_list)
    def test_task_id_match(self):
        spec_ids = sorted(t["id"] for t in self.spec["tasks"])
        task_ids = sorted(t["id"] for t in self.tasks)
        self.assertEqual(spec_ids, task_ids)
    def test_oracle_id_match(self):
        spec_ids = sorted(o["id"] for o in self.spec["oracles"])
        oracle_ids = sorted(o["id"] for o in self.oracles)
        self.assertEqual(spec_ids, oracle_ids)

class TestMutationDetection(unittest.TestCase):
    def setUp(self):
        self.spec, self.tasks, self.oracles, self.corpus = load_artifacts()
    def test_task_prompt_mutation_detected(self):
        mutated = deepcopy(self.tasks)
        original_prompt = mutated[0]["prompt"]
        mutated[0]["prompt"] = original_prompt.replace("Beacon", "MUTATED_BEACON")
        self.assertNotEqual(original_prompt, mutated[0]["prompt"])
    def test_oracle_derivation_mutation_detected(self):
        mutated = deepcopy(self.oracles)
        original = mutated[0].get("derivation_evidence", [])
        mutated[0]["derivation_evidence"] = original + ["MUTATED_EVIDENCE_ID"]
        self.assertNotEqual(original, mutated[0]["derivation_evidence"])
    def test_corpus_digest_mutation_detected(self):
        mutated = deepcopy(self.corpus)
        evidence_list = mutated["evidence"]
        if evidence_list:
            original = evidence_list[0].get("content_digest", "")
            evidence_list[0]["content_digest"] = "MUTATED_DIGEST"
            self.assertNotEqual(original, "MUTATED_DIGEST")
    def test_checkpoint_mutation_detected(self):
        mutated = deepcopy(self.tasks)
        original_cp = mutated[0]["checkpoint"]
        mutated[0]["checkpoint"] = 99
        self.assertNotEqual(original_cp, 99)
    def test_model_policy_mutation_detected(self):
        mutated = deepcopy(self.spec)
        original_model = mutated.get("model_condition", {}).get("model", "")
        mutated["model_condition"]["model"] = "MUTATED_MODEL"
        self.assertNotEqual(original_model, "MUTATED_MODEL")
    def test_future_evidence_mutation_detected(self):
        mutated = deepcopy(self.corpus)
        evidence_list = mutated["evidence"]
        if evidence_list:
            original = evidence_list[0].get("available_from", 0)
            evidence_list[0]["available_from"] = 999
            self.assertNotEqual(original, 999)
    def test_sealed_identity_mutation_detected(self):
        mutated = deepcopy(self.spec)
        original_sealed = deepcopy(mutated.get("historical_sealed_ids", {}))
        if original_sealed:
            first_key = list(original_sealed.keys())[0]
            mutated["historical_sealed_ids"][first_key] = "MUTATED_SEAL"
        self.assertNotEqual(original_sealed, mutated["historical_sealed_ids"])
    def test_statistical_rule_mutation_detected(self):
        mutated = deepcopy(self.spec)
        original_alpha = mutated.get("statistical_parameters", {}).get("alpha", 0)
        mutated["statistical_parameters"]["alpha"] = 0.999
        self.assertNotEqual(original_alpha, 0.999)
    def test_supersession_mutation_detected(self):
        mutated = deepcopy(self.corpus)
        evidence_list = mutated["evidence"]
        if evidence_list:
            original = evidence_list[0].get("supersedes", [])
            evidence_list[0]["supersedes"] = ["MUTATED_SUPERSEDE"]
            self.assertNotEqual(original, evidence_list[0].get("supersedes"))
    def test_count_integrity_positive(self):
        self.assertEqual(len(self.tasks), 30)
        self.assertEqual(len(self.oracles), 30)
        evidence_ids = set(e.get("evidence_id") for e in self.corpus["evidence"])
        self.assertEqual(len(evidence_ids), len(self.corpus["evidence"]))
    def test_mutations_produce_different_validation_results(self):
        mutated_tasks = deepcopy(self.tasks)
        mutated_tasks[0]["checkpoint"] = 99
        v = Validator()
        v._validate_tasks(mutated_tasks, self.spec)
        self.assertTrue(len(v.errors) > 0)

class TestProtocolDocumentValidation(unittest.TestCase):
    def setUp(self):
        self.spec, self.tasks, self.oracles, self.corpus = load_artifacts()
    def test_prerregistration_pre_t14_count(self):
        import re
        prereg_path = Path(__file__).parent / "PREREGISTRATION-V2.md"
        self.assertTrue(prereg_path.exists())
        text = prereg_path.read_text()
        match = re.search(r"(\d+)\s+of the\s+(\d+)\s+tasks\s+are issued before t14", text)
        self.assertIsNotNone(match)
        self.assertEqual(int(match.group(1)), 27)
        self.assertEqual(int(match.group(2)), 30)
    def test_pre_t14_actual_count(self):
        actual = sum(1 for t in self.tasks if t["checkpoint"] < 14)
        self.assertEqual(actual, 27)

class TestValidatorInternalMethods(unittest.TestCase):
    def setUp(self):
        self.spec, self.tasks, self.oracles, self.corpus = load_artifacts()
        self.v = Validator()
    def test_task_field_presence(self):
        required_fields = ["id", "scenario", "checkpoint", "task_class", "prompt",
            "output_contract", "oracle_id", "temporal_span", "required_hops",
            "epoch_boundary", "depends_on_evidence", "trap_evidence", "distractor_evidence"]
        for task in self.tasks:
            for field in required_fields:
                self.assertIn(field, task)
    def test_oracle_field_presence(self):
        required_fields = ["id", "task_id", "derivation_evidence", "require_all", "forbid"]
        for oracle in self.oracles:
            for field in required_fields:
                self.assertIn(field, oracle)
    def test_corpus_field_presence(self):
        required_fields = ["evidence_id", "scenario", "checkpoint", "epoch", "kind", "path", "content_digest"]
        for ev in self.corpus["evidence"]:
            for field in required_fields:
                self.assertIn(field, ev)
    def test_no_duplicate_task_ids(self):
        task_ids = [t["id"] for t in self.tasks]
        self.assertEqual(len(task_ids), len(set(task_ids)))
    def test_no_duplicate_oracle_ids(self):
        oracle_ids = [o["id"] for o in self.oracles]
        self.assertEqual(len(oracle_ids), len(set(oracle_ids)))
    def test_task_oracle_resolution(self):
        oracle_ids = {o["id"] for o in self.oracles}
        task_ids = {t["id"] for t in self.tasks}
        for task in self.tasks:
            self.assertIn(task["oracle_id"], oracle_ids)
        for oracle in self.oracles:
            self.assertIn(oracle["task_id"], task_ids)
    def test_evidence_dependencies_exist(self):
        evidence_ids = {ev["evidence_id"] for ev in self.corpus["evidence"]}
        for task in self.tasks:
            for dep in task.get("depends_on_evidence", []):
                self.assertIn(dep, evidence_ids)
            for trap in task.get("trap_evidence", []):
                self.assertIn(trap, evidence_ids)
            for dist in task.get("distractor_evidence", []):
                self.assertIn(dist, evidence_ids)
    def test_no_future_leakage(self):
        evidence_by_id = {ev["evidence_id"]: ev for ev in self.corpus["evidence"]}
        for task in self.tasks:
            task_cp = task["checkpoint"]
            for dep in task.get("depends_on_evidence", []):
                ev = evidence_by_id.get(dep)
                if ev:
                    available_from = ev.get("available_from", ev.get("checkpoint", 0))
                    self.assertLessEqual(available_from, task_cp)
    def test_checkpoint_range(self):
        for task in self.tasks:
            self.assertGreaterEqual(task["checkpoint"], 0)
            self.assertLessEqual(task["checkpoint"], 14)
    def test_temporal_span_validity(self):
        for task in self.tasks:
            span = task.get("temporal_span", 0)
            cp = task["checkpoint"]
            self.assertLessEqual(span, cp)
    def test_content_digest_validation(self):
        import hashlib
        for ev in self.corpus["evidence"]:
            if "content" in ev and "content_digest" in ev:
                expected = hashlib.sha256(ev["content"].encode()).hexdigest()
                self.assertEqual(ev["content_digest"], expected)

class TestSealedHistoricalIdentity(unittest.TestCase):
    def setUp(self):
        self.spec, _, _, _ = load_artifacts()
    def test_r1_v1_ceiling_effect_evidence(self):
        hsi = self.spec.get("historical_sealed_ids", {})
        expected = "d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b"
        self.assertEqual(hsi.get("R1_V1_CEILING_EFFECT_EVIDENCE"), expected)
    def test_r1_v1_sealed_commit(self):
        hsi = self.spec.get("historical_sealed_ids", {})
        expected = "ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c"
        self.assertEqual(hsi.get("R1_V1_1_SEALED_COMMIT"), expected)

class TestStatisticalRuleDrift(unittest.TestCase):
    def setUp(self):
        self.spec, _, _, _ = load_artifacts()
    def test_k_total_is_30(self):
        sp = self.spec.get("statistical_parameters", {})
        self.assertEqual(sp.get("K_total"), 30)
    def test_alpha_present(self):
        sp = self.spec.get("statistical_parameters", {})
        self.assertIn("alpha", sp)
    def test_required_stat_fields_present(self):
        sp = self.spec.get("statistical_parameters", {})
        required = ["alpha", "target_power", "minimum_meaningful_effect_delta",
            "z_one_minus_alpha_over_2", "z_power", "K_total",
            "B_NULL_exclusion_rule", "K_eligible", "psi_hat_population",
            "pairing_unit", "N_pairs_formula", "r_conf_formula",
            "r_conf_minimum", "r_conf_maximum"]
        for field in required:
            self.assertIn(field, sp)

if __name__ == "__main__":
    unittest.main(verbosity=2)
