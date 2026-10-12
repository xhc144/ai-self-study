"""Mathematical contracts and end-to-end evidence for the v0.3 research modules."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("v03_research", ROOT/"experiments/v03_research.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ResearchContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = MODULE.run(144)

    def test_parameter_scope_is_enforced(self):
        good = dict(tool="lookup", resource="public_a", destination="current_user")
        self.assertTrue(MODULE.authorized(good))
        for change in ({"resource": "private"}, {"destination": "external"},
                       {"tool": "export"}, {"resource": "../private"}):
            self.assertFalse(MODULE.authorized({**good, **change}))
        self.assertFalse(MODULE.authorized({**good, "unknown": True}))
        for malformed in (None, [], {**good, "resource": []}):
            self.assertFalse(MODULE.authorized(malformed))

    def test_executor_blocks_privilege_without_claiming_semantic_safety(self):
        rows = {row["policy"]: row for row in self.results["boundary"]["rows"]}
        guarded = rows["source_blind_with_executor"]
        self.assertEqual(guarded["unauthorized_proposals"], 80)
        self.assertEqual(guarded["unauthorized_executions"], 0)
        self.assertEqual(guarded["semantic_attack_successes"], 40)
        self.assertEqual(rows["keyword_refusal"]["clean_false_refusal_rate"], .5)

    def test_monte_carlo_matches_independent_episode_law(self):
        for row in self.results["propagation"]["rows"]:
            # Six binomial standard deviations: broad numerical smoke bound,
            # not an assertion of inferential validity for real agent errors.
            for prefix in ("unverified", "checked"):
                p = row[prefix+"_theory"]
                observed = row[prefix+"_episode_success"]
                self.assertLess(abs(observed-p), 6*np.sqrt(p*(1-p)/10000))
        self.assertLess(self.results["propagation"]["rows"][-1]["unverified_episode_success"], .6)

    def test_fitted_decodability_does_not_imply_use(self):
        result = self.results["probe"]
        self.assertEqual(result["probe_test_accuracy"], 1.)
        rows = {r["intervention"]: r for r in result["rows"]}
        self.assertEqual(rows["decodable_unused"]["mean_absolute_logit_change"], 0.)
        self.assertEqual(rows["used_positive_control"]["output_flip_rate"], 1.)
        self.assertEqual({r["mean_patch_norm"] for r in result["rows"]}, {2.})
        self.assertEqual(result["positive_patch_recovery_accuracy"], 1.)
        self.assertEqual(result["unused_patch_recovery_accuracy"], 0.)

    def test_ig_numeric_integral_against_closed_form(self):
        x, baseline, weight = np.array([2., 1.]), np.zeros(2), np.array([4., 2.])
        value = MODULE.integrated_gradients(x, baseline, weight)
        # For sigmoid(w.x), IG_j = w_j*(x_j-b_j)*(f(x)-f(b))/(w.(x-b)).
        exact = weight*(x-baseline)*(MODULE.sigmoid(10)-MODULE.sigmoid(0))/10
        np.testing.assert_allclose(value, exact, rtol=1e-8, atol=1e-10)
        np.testing.assert_array_equal(MODULE.integrated_gradients(x, x, weight), np.zeros(2))

    def test_search_freezes_before_disjoint_holdout(self):
        result = self.results["program_search"]
        config = result["parameters"]
        self.assertFalse(set(config["dev_inputs"]) & set(config["holdout_inputs"]))
        self.assertFalse(config["holdout_used_for_selection"])
        self.assertEqual(result["honest_selected"]["coefficients"], [0, 1, 1])
        self.assertEqual(result["honest_selected"]["holdout_accuracy"], 1.)
        self.assertEqual(result["faulty_selected"]["faulty_dev_loss"], 0.)
        self.assertEqual(result["faulty_selected"]["holdout_accuracy"], 0.)
        self.assertEqual(result["dev_memorization_negative_control"]["dev_mse"], 0.)
        self.assertEqual(result["dev_memorization_negative_control"]["holdout_accuracy"], 0.)
        self.assertTrue(all("holdout_accuracy" not in row for row in result["archive"]))

    def test_contraction_can_be_stably_wrong(self):
        result = self.results["recurrence"]
        for row in result["rows"]:
            self.assertLessEqual(row["fixed_point_error"], row["contraction_error_bound"]+1e-15)
            self.assertEqual(row["correct"], row["fixed_point"] > 0)
        final = [r for r in result["rows"] if r["steps"] == 64 and r["fixed_point"] < 0][0]
        self.assertEqual(final["successive_difference"], 0.)
        self.assertFalse(final["correct"])

    def test_denoising_expectation_by_explicit_mask_enumeration(self):
        for row in self.results["recurrence"]["two_token_denoising"]:
            t, expectation = row["mask_probability"], 0.
            for mask in ((0, 0), (0, 1), (1, 0), (1, 1)):
                probability = np.prod([t if bit else 1-t for bit in mask])
                loss = 2*np.log(2) if mask == (1, 1) else 0.
                expectation += probability*loss
            self.assertAlmostEqual(expectation, row["expected_unweighted_loss"])
            self.assertAlmostEqual(expectation/t, row["expected_inverse_t_weighted_loss"])

    def test_reproducible_child_rng_streams(self):
        self.assertEqual(self.results, MODULE.run(144))
        self.assertNotEqual(self.results["propagation"], MODULE.run(145)["propagation"])

    def test_cli_outputs_bind_code_and_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run([sys.executable, "-B", str(ROOT/"experiments/v03_research.py"),
                            "--seed", "144", "--out", directory], check=True,
                           capture_output=True, text=True)
            out = Path(directory)
            environment = json.loads((out/"environment.json").read_text())
            actual = hashlib.sha256((ROOT/"experiments/v03_research.py").read_bytes()).hexdigest()
            self.assertEqual(environment["script_sha256"], actual)
            self.assertFalse(environment["llm_evaluated"])
            self.assertEqual(json.loads((out/"metrics.json").read_text()), self.results)
            for name, digest in json.loads((out/"hashes.json").read_text()).items():
                self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
