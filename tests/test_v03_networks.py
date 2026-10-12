"""Checks independent derivative approximations and mathematical invariants."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments'))
from v03_networks import (init_batch, batch_loss_grad, batch_experiment, dense_attention,
                         blocked_attention, attention_experiment, layernorm_forward,
                         layernorm_backward, calibration_experiment, selection_experiment)


class NetworkLessons(unittest.TestCase):
    def test_all_batch_coordinates_and_localized_fault(self):
        r = batch_experiment(144)
        self.assertEqual(r['checked_coordinates'], 64)
        self.assertLess(max(r['correct_errors'].values()), 1e-7)
        self.assertEqual(set(r['failing_groups']), {'E', 'P'})
        self.assertLess(r['loss_after'], r['loss_before'])
        self.assertLess(r['duplicated_batch_gradient_max_gap'], 1e-14)

    def test_gather_unused_row_and_batch_permutation(self):
        p = init_batch(np.random.default_rng(9))
        ids = np.array([[1, 1, 2], [1, 2, 1]])
        y = np.array([[0, 1, 2], [1, 2, 0]])
        loss, g = batch_loss_grad(p, ids, y)
        permuted_loss, permuted = batch_loss_grad(p, ids[::-1], y[::-1])
        np.testing.assert_array_equal(g['E'][[0, 3, 4]], np.zeros((3, 3)))
        self.assertAlmostEqual(loss, permuted_loss)
        for key in g:
            np.testing.assert_allclose(g[key], permuted[key], atol=1e-14)

    def test_attention_closed_form_and_late_allowed_block(self):
        q = np.array([[1.], [1.]])
        k = np.array([[0.], [np.log(3.)]])
        v = np.array([[2., 0.], [0., 4.]])
        mask = np.array([[True, True], [False, True]])
        expected = np.array([[.5, 3.], [0., 4.]])
        np.testing.assert_allclose(dense_attention(q, k, v, mask)[0], expected, atol=1e-14)
        np.testing.assert_allclose(blocked_attention(q, k, v, mask, 2, 1), expected, atol=1e-14)

    def test_attention_degenerate_mask_rejected(self):
        z = np.ones((2, 2)); mask = np.array([[False, False], [True, True]])
        for fn in (dense_attention, blocked_attention):
            with self.assertRaises(ValueError):
                fn(z, z, z, mask)

    def test_online_equivalence_causal_invariance_and_derivatives(self):
        r = attention_experiment(144)
        self.assertLess(max(r['blocked_max_abs_gaps'].values()), 1e-12)
        self.assertLess(r['extreme_score_gap'], 1e-12)
        self.assertEqual(r['masked_prefix_max_abs_gap'], 0.)
        self.assertGreater(r['unmasked_prefix_max_abs_gap'], 1e-2)
        self.assertEqual(r['forbidden_weight_max'], 0.)
        self.assertLess(max(r['backward_errors'].values()), 1e-7)

    def test_layernorm_directional_derivative_and_translation(self):
        rng = np.random.default_rng(17)
        x, gamma, beta = rng.normal(size=(2, 3, 4)), rng.normal(size=4), rng.normal(size=4)
        u, direction = rng.normal(size=x.shape), rng.normal(size=x.shape)
        y, cache = layernorm_forward(x, gamma, beta)
        shifted, _ = layernorm_forward(x + 10., gamma, beta)
        np.testing.assert_allclose(y, shifted, atol=1e-12)
        dx = layernorm_backward(u, gamma, cache)['x']
        eps = 1e-5
        numeric = np.sum(u * (layernorm_forward(x+eps*direction, gamma, beta)[0]-
                              layernorm_forward(x-eps*direction, gamma, beta)[0]))/(2*eps)
        self.assertAlmostEqual(numeric, float(np.sum(dx*direction)), places=7)
        np.testing.assert_allclose(dx.sum(-1), 0., atol=1e-12)
        with self.assertRaises(ValueError):
            layernorm_forward(x, gamma, beta, eps=0.)

    def test_temperature_preserves_labels_and_improves_controlled_nll(self):
        r = calibration_experiment(144)
        self.assertEqual(r['test_before']['accuracy'], r['test_after']['accuracy'])
        self.assertLess(r['test_after']['nll'], r['test_before']['nll'])
        self.assertLess(r['test_after']['brier'], r['test_before']['brier'])
        self.assertAlmostEqual(r['chosen_temperature'], 3., delta=.6)

    def test_selection_bias_known_population_risk(self):
        r = selection_experiment(144)
        means = [row['validation_selected_mean'] for row in r['rows']]
        self.assertTrue(all(a >= b for a, b in zip(means, means[1:])))
        self.assertGreater(r['rows'][-1]['optimism_mean'], .2)
        for row in r['rows']:
            self.assertAlmostEqual(row['independent_test_mean'], .5, delta=.01)

    def test_cli_records_actual_code_and_environment(self):
        script = ROOT / 'experiments' / 'v03_networks.py'
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, '-B', str(script), '--out', tmp, '--seed', '144'],
                           check=True, stdout=subprocess.PIPE)
            env = json.loads((Path(tmp) / 'environment.json').read_text())
            metrics = json.loads((Path(tmp) / 'metrics.json').read_text())
            self.assertEqual(env['code_sha256'], hashlib.sha256(script.read_bytes()).hexdigest())
            self.assertEqual(env['seed'], 144)
            self.assertEqual(set(metrics), {'batch', 'attention', 'layernorm', 'calibration', 'selection'})


if __name__ == '__main__':
    unittest.main()
