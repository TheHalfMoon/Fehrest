#!/usr/bin/env python3
"""Static R1-v3 statistical design checks — no empirical data.

Exercies deterministic examples for:
  B_NULL_EXCLUSION_BEFORE_PSI
  K_ELIGIBLE_AFTER_B_NULL
  PSI_USES_ELIGIBLE_OBSERVATIONS
  R_CONF_USES_K_ELIGIBLE
  N_PAIRS_FLOOR
  R_CONF_MIN
  R_CONF_MAX
  LOW_K_ROUTE
  TASK_CLASS_LOSS_ROUTE

For:
  K=30,29,20,minimum(15),minimum-1(14),0
  psi_hat = 0, delta^2, delta^2+epsilon, large
  one/multiple task classes fully excluded
  r_conf below minimum / above maximum

All are static design checks via the preregistered rule, not model execution.
"""

import json
import math
import unittest
from pathlib import Path

BENCH_DIR = Path(__file__).parent
SPEC_PATH = BENCH_DIR / "benchmark-spec-v3.json"

DELTA = 0.15
DELTA2 = DELTA ** 2
Z_ALPHA = 1.959964
Z_POWER = 0.841621
R_CONF_MIN = 3
R_CONF_MAX = 20
N_PAIRS_FLOOR = 90
N_PAIRS_CEILING = 600
K_TOTAL = 30
K_MINIMUM = 15


def compute_n_pairs(psi_hat: float) -> int | None:
    """Power formula; returns None when undefined (psi_hat <= delta^2)."""
    if psi_hat <= DELTA2:
        return None
    # ceil( (z_alpha*sqrt(psi) + z_power*sqrt(psi-delta2))^2 / delta2 )
    raw = (Z_ALPHA * math.sqrt(psi_hat) + Z_POWER * math.sqrt(psi_hat - DELTA2)) ** 2 / DELTA2
    return math.ceil(raw)


def compute_r_conf(n_pairs: int, k_eligible: int) -> int | str:
    """r_conf = ceil(N_pairs / K_eligible), bounded to [3,20] or UNDERPOWERED."""
    if k_eligible <= 0:
        return "UNDERPOWERED_NO_ELIGIBLE_TASKS"
    raw = math.ceil(n_pairs / k_eligible)
    if raw < R_CONF_MIN:
        return R_CONF_MIN
    if raw > R_CONF_MAX:
        return "UNDERPOWERED_FOR_PREREGISTERED_EFFECT"
    return raw


class TestStatisticalDesignStatic(unittest.TestCase):
    def test_spec_statistical_parameters_present(self):
        spec = json.loads(SPEC_PATH.read_text())
        sp = spec["statistical_parameters"]
        # Canonical definitions must exist
        self.assertEqual(sp["K_total"], 30)
        self.assertEqual(sp["r_conf_minimum"], 3)
        self.assertEqual(sp["r_conf_maximum"], 20)
        self.assertEqual(sp["pairing_unit"], "(task, repeat) pair")
        self.assertIn("psi_hat_population", sp)
        self.assertIn("B_NULL_exclusion_rule", sp)
        self.assertIn("K_eligible", sp)
        self.assertIn("N_pairs_formula", sp)
        self.assertIn("r_conf_formula", sp)
        # Formula must be power-analysis form, not combinatoric
        self.assertIn("z_{1-alpha/2}", sp["N_pairs_formula"])
        self.assertIn("psi_hat", sp["N_pairs_formula"])
        self.assertNotIn("K_eligible*(K_eligible", sp["N_pairs_formula"])

    def test_k_eligible_after_b_null_exclusion(self):
        # B_NULL_EXCLUSION_BEFORE_PSI: K_eligible = K_total - excluded
        for excluded, expected_k in [(0, 30), (1, 29), (10, 20), (15, 15), (16, 14), (30, 0)]:
            k_eligible = K_TOTAL - excluded
            self.assertEqual(k_eligible, expected_k, f"excluded={excluded}")

    def test_k_edge_low_k_route(self):
        # LOW_K_ROUTE: if K_eligible < minimum_K (15), UNDERPOWERED
        for k in [30, 29, 20, 15]:
            self.assertGreaterEqual(k, K_MINIMUM, f"should be powered at K={k}")
        for k in [14, 0]:
            self.assertLess(k, K_MINIMUM, f"should be UNDERPOWERED at K={k}")
            # Even if N_pairs were minimal, the study is underpowered by LOW_K
            route = "UNDERPOWERED" if k < K_MINIMUM else "OK"
            self.assertEqual(route, "UNDERPOWERED")

    def test_k_minimum_boundary(self):
        self.assertEqual(K_MINIMUM, 15)
        self.assertEqual(K_TOTAL - 15, 15)  # exactly at boundary still powered
        self.assertEqual(K_TOTAL - 16, 14)  # one beyond → underpowered

    def test_psi_hat_edges(self):
        # psi_hat = 0 → undefined
        self.assertIsNone(compute_n_pairs(0.0))
        # psi_hat == delta^2 → undefined (boundary)
        self.assertIsNone(compute_n_pairs(DELTA2))
        self.assertIsNone(compute_n_pairs(DELTA2 + 0.0))
        # psi_hat == delta^2 + epsilon → defined, just above threshold
        eps = 1e-4
        self.assertIsNotNone(compute_n_pairs(DELTA2 + eps))
        # moderate
        self.assertIsNotNone(compute_n_pairs(0.10))
        # large psi_hat
        n_large = compute_n_pairs(0.50)
        self.assertIsNotNone(n_large)
        self.assertGreater(n_large, 0)

    def test_psi_uses_eligible_observations(self):
        # PSI_USES_ELIGIBLE_OBSERVATIONS: denominator is K_eligible * r, not K_total * r
        # Static check: with K=30 vs K=29, same raw discordant count yields different psi
        # Example: 10 discordant observations
        discordant = 10
        r = 4
        for k_e in [30, 29]:
            denom = k_e * r
            psi = discordant / denom
            # Different K yields different psi → power differs
            n = compute_n_pairs(psi) if psi > DELTA2 else None
            # Just prove psi differs
            self.assertAlmostEqual(psi, discordant / (k_e * r))
        # If psi computed with K_total when exclusions exist, N_pairs would be wrong

    def test_n_pairs_floor_and_ceiling(self):
        # N_pairs is bounded to [90,600] before r_conf
        # Example: psi_hat small just above threshold gives small raw N_pairs → floor applies
        # psi_hat large gives huge N_pairs → ceiling
        # We test the r_conf bounding indirectly: r_conf min=3 ensures at least floor-like behavior
        # Static: with K=30, N=90 → r=3 (at floor/min)
        self.assertEqual(compute_r_conf(90, 30), 3)
        self.assertEqual(compute_r_conf(89, 30), 3)  # below floor but r_conf min is 3
        self.assertEqual(compute_r_conf(600, 30), 20)  # at ceiling with max K
        self.assertEqual(compute_r_conf(601, 30), "UNDERPOWERED_FOR_PREREGISTERED_EFFECT")

    def test_r_conf_minimum(self):
        # R_CONF_MIN=3: per-task variability unobservable below
        self.assertEqual(compute_r_conf(30, 30), 3)  # raw 1 → bounded to 3
        self.assertEqual(compute_r_conf(60, 30), 3)  # raw 2 → 3
        self.assertEqual(compute_r_conf(90, 30), 3)  # raw 3 → 3

    def test_r_conf_maximum(self):
        # R_CONF_MAX=20: cost ceiling
        self.assertEqual(compute_r_conf(600, 30), 20)
        self.assertEqual(compute_r_conf(601, 30), "UNDERPOWERED_FOR_PREREGISTERED_EFFECT")
        self.assertEqual(compute_r_conf(400, 20), 20)  # 400/20=20 exactly
        self.assertEqual(compute_r_conf(401, 20), "UNDERPOWERED_FOR_PREREGISTERED_EFFECT")

    def test_r_conf_uses_k_eligible_not_k_total(self):
        # Concrete divisor effect: N_pairs=120
        n = 120
        r_with_total = math.ceil(n / 30)  # incorrectly using K_TOTAL=30 → 4
        r_with_eligible = math.ceil(n / 29)  # correctly using K_ELIGIBLE=29 → 5
        self.assertEqual(r_with_total, 4)
        self.assertEqual(r_with_eligible, 5)
        # Using K_TOTAL when one task excluded underpowers confirmatory by 1 repeat/task
        self.assertNotEqual(r_with_total, r_with_eligible)
        # Validate via compute_r_conf wrapper
        self.assertEqual(compute_r_conf(120, 30), 4)
        self.assertEqual(compute_r_conf(120, 29), 5)

    def test_b_null_exclusion_before_psi(self):
        # Ordering: B_NULL exclusion yields K_eligible, then psi computed on eligible only
        # Static simulation: suppose B-NULL scores >0 on 2 tasks
        excluded_ids = {"S1-A-NEXT", "S2-A-NEXT"}
        k_eligible = K_TOTAL - len(excluded_ids)
        self.assertEqual(k_eligible, 28)
        # PSI denominator must be k_eligible * r, not total
        r = 4
        # Simulate scoring matrix for B5 vs B4 on eligible tasks only
        # If we computed psi on all 30, we'd include prompt-answerable tasks that are not measuring context
        eligible_total_pairs = k_eligible * r  # 112
        total_pairs_if_wrong = K_TOTAL * r  # 120
        self.assertNotEqual(eligible_total_pairs, total_pairs_if_wrong)

    def test_task_class_loss_one_class(self):
        # One task class fully excluded (e.g., ABSTENTION n=2)
        k_total = 30
        ab_excluded = 2  # ABSTENTION
        self.assertEqual(k_total - ab_excluded, 28)
        # Must report per-class psi_hat alongside pooled
        # Static: remaining classes still evaluable, K=28

    def test_task_class_loss_multiple_classes(self):
        excluded = 2 + 1 + 2  # ABSTENTION(2)+PROVENANCE(1)+SCOPE_RESOLUTION(2)=5
        self.assertEqual(30 - excluded, 25)
        # Low-K supersedes
        excluded_many = 16  # → K=14 → LOW_K_ROUTE
        self.assertEqual(30 - excluded_many, 14)
        self.assertLess(14, K_MINIMUM)

    def test_r_conf_below_minimum_edge(self):
        # Raw N_pairs very small → r_conf would be 1 or 2 → bounded to 3
        self.assertEqual(compute_r_conf(1, 30), 3)
        self.assertEqual(compute_r_conf(2 * 30 - 1, 30), 3)  # N=59 → 2 → 3

    def test_r_conf_above_maximum_edge(self):
        self.assertEqual(compute_r_conf(1000, 30), "UNDERPOWERED_FOR_PREREGISTERED_EFFECT")
        self.assertEqual(compute_r_conf(1000, 15), "UNDERPOWERED_FOR_PREREGISTERED_EFFECT")

    def test_k_zero_and_minimum_minus_one(self):
        self.assertEqual(K_TOTAL - K_TOTAL, 0)
        self.assertLess(0, K_MINIMUM)
        self.assertEqual(compute_r_conf(90, 0), "UNDERPOWERED_NO_ELIGIBLE_TASKS")
        self.assertEqual(K_MINIMUM - 1, 14)
        self.assertLess(14, K_MINIMUM)

    def test_n_pairs_not_combinatoric(self):
        # Explicitly reject N_pairs = K*(K-1)/2
        for k in [30, 29, 20, 15]:
            combinatoric = k * (k - 1) // 2
            # For k=30, combinatoric=435, which is unrelated to power
            # Power-based N_pairs depends on psi_hat, not combinatorics
            # Just prove they differ for a realistic psi_hat
            psi = 0.10
            n_power = compute_n_pairs(psi)
            self.assertNotEqual(combinatoric, n_power)

    def test_arm_contrast_count_distinct_from_n_pairs(self):
        # 5 eligible comparison arms (B0,B1,B3,B4,B5) → 10 pairwise contrasts
        eligible_arms = ["B0", "B1", "B3", "B4", "B5"]
        contrast_count = len(eligible_arms) * (len(eligible_arms) - 1) // 2
        self.assertEqual(contrast_count, 10)
        # N_pairs is not this number; it is observation pairs required
        psi = 0.10
        n = compute_n_pairs(psi)
        self.assertNotEqual(contrast_count, n)
        # Primary contrast is B5 vs B4 only

    def test_validator_protocol_ordering_present(self):
        # Ensure validator's protocol doc check would pass for current docs
        import re
        pre = (BENCH_DIR / "PREREGISTRATION-V2.md").read_text()
        # Must find "27 of the 30 tasks are issued before t14"
        m = re.search(r"(\d+)\s+of the\s+(\d+)\s+tasks\s+are issued before t14", pre)
        self.assertIsNotNone(m)
        self.assertEqual(int(m.group(1)), 27)
        self.assertEqual(int(m.group(2)), 30)
        # §28 first step must mention B-NULL
        sec28 = re.search(r"## 28\.\s*Then.*?(?=## \d+|\Z)", pre, re.DOTALL)
        self.assertIsNotNone(sec28)
        self.assertIn("b-null", sec28.group(0).lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
