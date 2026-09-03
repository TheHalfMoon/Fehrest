#!/usr/bin/env python3
"""R1-v2 benchmark machine validator."""
import json
import hashlib
import re
import sys
from pathlib import Path

BENCH_DIR = Path("bench/R1")

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

class ValidationError(Exception):
    pass

class Validator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def check(self, condition, msg):
        if not condition:
            self.error(msg)

    def validate(self):
        spec = self._load_spec()
        tasks = self._load_tasks()
        oracles = self._load_oracles()
        corpus = self._load_corpus()

        if spec is None or tasks is None or oracles is None or corpus is None:
            return False

        self._validate_spec_structure(spec)
        self._validate_tasks(tasks, spec)
        self._validate_oracles(oracles, tasks, spec)
        self._validate_corpus(corpus, tasks, oracles, spec)
        self._validate_task_oracle_resolution(tasks, oracles)
        self._validate_evidence_dependencies(tasks, corpus)
        self._validate_no_future_leakage(tasks, corpus)
        self._validate_task_counts(tasks, spec)
        self._validate_task_class_counts(tasks, spec)
        self._validate_task_distribution(tasks, spec)
        self._validate_temporal_spans(tasks)
        self._validate_epoch_boundaries(tasks, spec)
        self._validate_maintenance_arithmetic(spec)
        self._validate_session_arithmetic(spec)
        self._validate_model_condition(spec)
        self._validate_statistical_parameters(spec)
        self._validate_model_identity_policy(spec)
        self._validate_context_budget(spec)
        self._validate_arms(spec)
        self._validate_historical_sealed_ids(spec)
        self._validate_scorer_support(oracles)
        self._validate_no_duplicate_ids(tasks, oracles)
        self._validate_trap_metadata(tasks, oracles, corpus)
        self._validate_cross_scenario_dependencies(tasks)
        self._validate_protocol_documents(spec, tasks)

        return len(self.errors) == 0

    def _load_spec(self):
        path = BENCH_DIR / "benchmark-spec-v2.json"
        if not path.exists():
            self.error(f"Missing benchmark spec: {path}")
            return None
        try:
            spec = json.loads(path.read_text())
            self.check(isinstance(spec, dict), "Benchmark spec must be a JSON object")
            return spec
        except json.JSONDecodeError as e:
            self.error(f"Invalid JSON in benchmark spec: {e}")
            return None

    def _load_tasks(self):
        path = BENCH_DIR / "tasks-v2.json"
        if not path.exists():
            self.error(f"Missing tasks artifact: {path}")
            return None
        try:
            tasks = json.loads(path.read_text())
            self.check(isinstance(tasks, list), "Tasks must be a JSON array")
            return tasks
        except json.JSONDecodeError as e:
            self.error(f"Invalid JSON in tasks: {e}")
            return None

    def _load_oracles(self):
        path = BENCH_DIR / "oracles-v2.json"
        if not path.exists():
            self.error(f"Missing oracles artifact: {path}")
            return None
        try:
            oracles = json.loads(path.read_text())
            self.check(isinstance(oracles, list), "Oracles must be a JSON array")
            return oracles
        except json.JSONDecodeError as e:
            self.error(f"Invalid JSON in oracles: {e}")
            return None

    def _load_corpus(self):
        path = BENCH_DIR / "corpus-manifest-v2.json"
        if not path.exists():
            self.error(f"Missing corpus manifest: {path}")
            return None
        try:
            corpus = json.loads(path.read_text())
            self.check(isinstance(corpus, dict), "Corpus manifest must be a JSON object")
            return corpus
        except json.JSONDecodeError as e:
            self.error(f"Invalid JSON in corpus manifest: {e}")
            return None

    def _validate_spec_structure(self, spec):
        required_keys = [
            "preregistration_version", "model_condition", "scenarios",
            "task_classes", "tasks", "oracles", "corpus", "arms",
            "maintenance_protocol", "session_arithmetic", "statistical_parameters",
            "model_identity_admissibility", "execution_prohibitions", "context_budget",
            "randomization"
        ]
        for key in required_keys:
            self.check(key in spec, f"Missing required spec key: {key}")

    def _validate_tasks(self, tasks, spec):
        self.check(len(tasks) == 30, f"Expected 30 tasks, got {len(tasks)}")
        required_fields = [
            "id", "scenario", "checkpoint", "task_class", "prompt",
            "output_contract", "oracle_id", "temporal_span", "required_hops",
            "epoch_boundary", "depends_on_evidence", "trap_evidence",
            "distractor_evidence"
        ]
        for task in tasks:
            for field in required_fields:
                self.check(field in task, f"Task {task.get('id', '?')} missing field: {field}")
            if "checkpoint" in task:
                self.check(0 <= task["checkpoint"] <= 14, f"Task {task['id']} checkpoint out of range: {task['checkpoint']}")
            if "temporal_span" in task and "checkpoint" in task:
                self.check(task["temporal_span"] <= task["checkpoint"],
                           f"Task {task['id']} temporal_span ({task['temporal_span']}) > checkpoint ({task['checkpoint']})")

    def _validate_oracles(self, oracles, tasks, spec):
        self.check(len(oracles) == 30, f"Expected 30 oracles, got {len(oracles)}")
        required_fields = ["id", "task_id", "derivation_evidence", "require_all", "forbid"]
        for oracle in oracles:
            for field in required_fields:
                self.check(field in oracle, f"Oracle {oracle.get('id', '?')} missing field: {field}")

    def _validate_corpus(self, corpus, tasks, oracles, spec):
        evidence_list = corpus.get("evidence", [])
        self.check(len(evidence_list) > 0, "Corpus must contain evidence items")
        required_fields = [
            "evidence_id", "scenario", "checkpoint", "epoch", "kind",
            "path", "content_digest"
        ]
        for ev in evidence_list:
            for field in required_fields:
                self.check(field in ev, f"Evidence {ev.get('evidence_id', '?')} missing field: {field}")
            if "content" in ev and "content_digest" in ev:
                expected_digest = sha256(ev["content"])
                self.check(ev["content_digest"] == expected_digest,
                           f"Evidence {ev['evidence_id']} content digest mismatch")

    def _validate_task_oracle_resolution(self, tasks, oracles):
        oracle_ids = {o["id"] for o in oracles}
        task_ids = {t["id"] for t in tasks}
        for task in tasks:
            oracle_id = task.get("oracle_id")
            self.check(oracle_id in oracle_ids,
                       f"Task {task['id']} oracle_id '{oracle_id}' not found in oracles")
        for oracle in oracles:
            task_id = oracle.get("task_id")
            self.check(task_id in task_ids,
                       f"Oracle {oracle['id']} task_id '{task_id}' not found in tasks")

    def _validate_evidence_dependencies(self, tasks, corpus):
        evidence_ids = {ev["evidence_id"] for ev in corpus.get("evidence", [])}
        for task in tasks:
            for dep in task.get("depends_on_evidence", []):
                self.check(dep in evidence_ids,
                           f"Task {task['id']} depends_on_evidence '{dep}' not found in corpus")
            for trap in task.get("trap_evidence", []):
                self.check(trap in evidence_ids,
                           f"Task {task['id']} trap_evidence '{trap}' not found in corpus")
            for dist in task.get("distractor_evidence", []):
                self.check(dist in evidence_ids,
                           f"Task {task['id']} distractor_evidence '{dist}' not found in corpus")

    def _validate_no_future_leakage(self, tasks, corpus):
        evidence_by_id = {ev["evidence_id"]: ev for ev in corpus.get("evidence", [])}
        for task in tasks:
            task_checkpoint = task.get("checkpoint", 0)
            for dep in task.get("depends_on_evidence", []):
                ev = evidence_by_id.get(dep)
                if ev:
                    available_from = ev.get("available_from", ev.get("checkpoint", 0))
                    self.check(available_from <= task_checkpoint,
                               f"Task {task['id']} (checkpoint {task_checkpoint}) depends on future evidence {dep} (available_from {available_from})")

    def _validate_task_counts(self, tasks, spec):
        scenario_counts = {}
        for t in tasks:
            sc = t["scenario"]
            scenario_counts[sc] = scenario_counts.get(sc, 0) + 1
        total = sum(scenario_counts.values())
        self.check(total == 30, f"Total tasks must be 30, got {total}")

    def _validate_task_class_counts(self, tasks, spec):
        class_counts = {}
        for t in tasks:
            tc = t["task_class"]
            class_counts[tc] = class_counts.get(tc, 0) + 1
        distinct_classes = len(class_counts)
        self.check(distinct_classes == 12, f"Expected 12 distinct task classes, got {distinct_classes}")
        total_from_classes = sum(class_counts.values())
        self.check(total_from_classes == 30, f"Task class counts sum to {total_from_classes}, expected 30")

    def _validate_task_distribution(self, tasks, spec):
        checkpoint_counts = {}
        for t in tasks:
            cp = t["checkpoint"]
            checkpoint_counts[cp] = checkpoint_counts.get(cp, 0) + 1
        distinct_checkpoints = len(checkpoint_counts)
        self.check(distinct_checkpoints >= 8,
                   f"Tasks span {distinct_checkpoints} checkpoints, need at least 8")
        pre_t14 = sum(1 for t in tasks if t["checkpoint"] < 14)
        self.check(pre_t14 >= 12,
                   f"Only {pre_t14} tasks before t14, need at least 12 for maintenance lag testing")

    def _validate_temporal_spans(self, tasks):
        for t in tasks:
            span = t.get("temporal_span", 0)
            checkpoint = t.get("checkpoint", 0)
            self.check(span <= checkpoint,
                       f"Task {t['id']} temporal_span ({span}) exceeds checkpoint ({checkpoint})")

    def _validate_epoch_boundaries(self, tasks, spec):
        for t in tasks:
            if t.get("epoch_boundary", False):
                checkpoint = t.get("checkpoint", 0)
                self.check(checkpoint >= 5,
                           f"Task {t['id']} claims epoch_boundary but checkpoint {checkpoint} < 5")

    def _validate_maintenance_arithmetic(self, spec):
        mp = spec.get("maintenance_protocol", {})
        sa = spec.get("session_arithmetic", {})
        scenarios = len(spec.get("scenarios", {}))
        transitions = mp.get("maintained_transitions_per_scenario", 14)
        maintained = sum(1 for a in spec.get("arms", {}).values() if a.get("maintained"))
        trajectories = mp.get("trajectories_per_maintained_arm", 2)
        expected = scenarios * transitions * maintained * trajectories
        actual = sa.get("maintenance_sessions", 0)
        self.check(actual == expected,
                   f"Maintenance sessions mismatch: expected {expected}, got {actual}")

    def _validate_session_arithmetic(self, spec):
        sa = spec.get("session_arithmetic", {})
        maintenance = sa.get("maintenance_sessions", 0)
        comparison = sa.get("comparison_continuation_sessions", 0)
        calibration = sa.get("calibration_sessions", 0)
        total = sa.get("total_variance_pilot_sessions", 0)
        expected_total = maintenance + comparison + calibration
        self.check(total == expected_total,
                   f"Total sessions mismatch: expected {expected_total}, got {total}")

    def _validate_model_condition(self, spec):
        mc = spec.get("model_condition", {})
        required_fields = ["model", "reasoning_effort", "temperature", "max_output_tokens", "tool_set"]
        for field in required_fields:
            self.check(field in mc, f"Model condition missing field: {field}")

    def _validate_statistical_parameters(self, spec):
        sp = spec.get("statistical_parameters", {})
        required_fields = [
            "alpha", "target_power", "minimum_meaningful_effect_delta",
            "z_one_minus_alpha_over_2", "z_power", "K_total",
            "B_NULL_exclusion_rule", "K_eligible", "psi_hat_population",
            "pairing_unit", "N_pairs_formula", "r_conf_formula",
            "r_conf_minimum", "r_conf_maximum"
        ]
        for field in required_fields:
            self.check(field in sp, f"Statistical parameters missing field: {field}")
        self.check(sp.get("K_total") == 30, f"K_total should be 30, got {sp.get('K_total')}")

    def _validate_model_identity_policy(self, spec):
        mia = spec.get("model_identity_admissibility", {})
        self.check(mia.get("policy") == "fail-closed",
                   "Model identity policy must be fail-closed")
        conditions = mia.get("conditions", {})
        required_conditions = [
            "returned_identity_missing",
            "identity_changes_within_batch",
            "maintenance_identity_not_equal_continuation_identity",
            "different_identities_across_arms",
            "provider_alias_drift",
            "identity_metadata_malformed"
        ]
        for cond in required_conditions:
            self.check(cond in conditions, f"Model identity condition missing: {cond}")
            self.check(conditions[cond] == "INVALIDATE_BATCH",
                       f"Model identity condition '{cond}' must be INVALIDATE_BATCH, got {conditions[cond]}")

    def _validate_context_budget(self, spec):
        cb = spec.get("context_budget", {})
        self.check(cb.get("primary_tier_bytes") == 6000,
                   f"Primary context budget should be 6000 bytes, got {cb.get('primary_tier_bytes')}")
        self.check(cb.get("secondary_tier_bytes") is None,
                   "Secondary context budget tier must be removed (set to null)")

    def _validate_arms(self, spec):
        arms = spec.get("arms", {})
        required_arms = ["B-NULL", "B0", "B1", "B3", "B4", "B5"]
        for arm in required_arms:
            self.check(arm in arms, f"Missing arm: {arm}")
        maintained = [name for name, a in arms.items() if a.get("maintained")]
        self.check(set(maintained) == {"B1", "B4", "B5"},
                   f"Maintained arms should be B1, B4, B5, got {maintained}")

    def _validate_historical_sealed_ids(self, spec):
        hsi = spec.get("historical_sealed_ids", {})
        self.check(
            hsi.get("R1_V1_CEILING_EFFECT_EVIDENCE") == "d99c21773b50daab9f0fd04f8b3bf34cf9f6e3ec7d11c2555132841ddcd2096b",
            "R1_V1_CEILING_EFFECT_EVIDENCE mismatch"
        )
        self.check(
            hsi.get("R1_V1_1_SEALED_COMMIT") == "ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c",
            "R1_V1_1_SEALED_COMMIT mismatch"
        )

    def _validate_scorer_support(self, oracles):
        required_types = {"require_synthesis", "require_epoch"}
        found_types = set()
        for oracle in oracles:
            if oracle.get("require_synthesis"):
                found_types.add("require_synthesis")
            if oracle.get("require_epoch"):
                found_types.add("require_epoch")
        for rt in required_types:
            self.check(rt in found_types,
                       f"Scorer must support oracle type: {rt}")

    def _validate_no_duplicate_ids(self, tasks, oracles):
        task_ids = [t["id"] for t in tasks]
        oracle_ids = [o["id"] for o in oracles]
        self.check(len(task_ids) == len(set(task_ids)),
                   f"Duplicate task IDs found: {[x for x in task_ids if task_ids.count(x) > 1]}")
        self.check(len(oracle_ids) == len(set(oracle_ids)),
                   f"Duplicate oracle IDs found: {[x for x in oracle_ids if oracle_ids.count(x) > 1]}")

    def _validate_trap_metadata(self, tasks, oracles, corpus):
        evidence_ids = {ev["evidence_id"] for ev in corpus.get("evidence", [])}
        for task in tasks:
            for trap in task.get("trap_evidence", []):
                self.check(trap in evidence_ids,
                           f"Task {task['id']} trap_evidence '{trap}' not in corpus")

    def _validate_cross_scenario_dependencies(self, tasks):
        scenario_ids = {t["scenario"] for t in tasks}
        for task in tasks:
            for dep in task.get("cross_scenario_dependencies", []):
                self.check(dep in scenario_ids,
                           f"Task {task['id']} cross_scenario_dependency '{dep}' not a valid scenario")

    def _validate_protocol_documents(self, spec, tasks):
        """Cross-check that numbers stated in the markdown protocol documents
        (PREREGISTRATION-V2.md, VARIANCE-PILOT-V2.md) match the actual JSON
        artifacts. This prevents documentation drift where prose numbers
        diverge from machine-verified state.
        """
        r1_dir = Path(__file__).parent
        pregreg_path = r1_dir / "PREREGISTRATION-V2.md"

        if pregreg_path.exists():
            text = pregreg_path.read_text()

            # Check the "tasks issued before t14" count
            actual_pre_t14 = sum(1 for t in tasks if t.get("checkpoint", 0) < 14)
            # Look for the pattern "**NN of the 30 tasks are issued before t14**"
            match = re.search(r'$$(\d+) of the (\d+) tasks? are issued before t14', text)
            if match:
                stated_pre_t14 = int(match.group(1))
                stated_total = int(match.group(2))
                actual_total = len(tasks)
                self.check(stated_pre_t14 == actual_pre_t14,
                           f"PREREGISTRATION-V2.md states {stated_pre_t14} tasks before t14, "
                           f"but actual count is {actual_pre_t14}")
                self.check(stated_total == actual_total,
                           f"PREREGISTRATION-V2.md states {stated_total} total tasks, "
                           f"but actual count is {actual_total}")

            # Check B-NULL exclusion ordering: B-NULL exclusion must be applied
            # BEFORE computing r_conf (§28 ordering)
            section_28 = re.search(r'## 28\.\s*Then.*?(?=## \d+|\Z)', text, re.DOTALL)
            if section_28:
                section_text = section_28.group(0)
                # The first numbered step must be B-NULL exclusion, not r_conf
                first_step = re.search(r'^\s*1\.\s*(.+)$', section_text, re.MULTILINE)
                if first_step:
                    step_text = first_step.group(1).strip().lower()
                    self.check('b-null' in step_text or 'b null' in step_text,
                               f"PREREGISTRATION-V2.md §28.1 must apply B-NULL exclusion first, "
                               f"got: '{first_step.group(1).strip()}'")

        variance_path = r1_dir / "VARIANCE-PILOT-V2.md"
        if variance_path.exists():
            text = variance_path.read_text()
            # Check B-NULL exclusion ordering in variance pilot
            section_10 = re.search(r'## 10\.\s*Then.*?(?=## \d+|\Z)', text, re.DOTALL)
            if section_10:
                section_text = section_10.group(0)
                first_step = re.search(r'^\s*1\.\s*(.+)$', section_text, re.MULTILINE)
                if first_step:
                    step_text = first_step.group(1).strip().lower()
                    self.check('b-null' in step_text or 'b null' in step_text,
                               f"VARIANCE-PILOT-V2.md §10.1 must apply B-NULL exclusion first, "
                               f"got: '{first_step.group(1).strip()}'")


def main():
    validator = Validator()
    passed = validator.validate()

    print("=" * 60)
    print("R1-v2 Benchmark Machine Validator")
    print("=" * 60)

    if validator.warnings:
        print(f"\nWarnings ({len(validator.warnings)}):")
        for w in validator.warnings:
            print(f"  WARNING: {w}")

    if passed:
        print(f"\nPASS: All validation checks passed")
        print(f"Errors: 0")
        return 0
    else:
        print(f"\nFAIL: {len(validator.errors)} validation error(s):")
        for e in validator.errors:
            print(f"  ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
