"""Mechanism invariants: cached decoder, low-rank derivatives and finite-action feedback."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec=importlib.util.spec_from_file_location('v03',Path(__file__).resolve().parents[1]/'experiments/v03_language.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

class LanguageMechanisms(unittest.TestCase):
    def test_fixed_icl_linear_predictor(self):
        r=e.icl_experiment()
        self.assertAlmostEqual(r["posterior_mean"][0],5/3)
        self.assertAlmostEqual(r["predictive_mean"],5.)
        self.assertAlmostEqual(r["predictive_variance"],2.5)
        self.assertEqual(r["trainable_weight_updates"],0)
    def test_cached_prefix_equivalence(self):
        r=e.cache_experiment(144)
        self.assertLess(r['max_logit_error'],1e-12)
        self.assertEqual(r['future_edit_prefix_error'],0.)
        self.assertEqual(r['cache_elements'],2*3*12*8)
    def test_top_p_minimal_prefix_and_temperature(self):
        z=np.log([.4,.3,.2,.1])
        np.testing.assert_allclose(e.sample_distribution(z,top_p=.65),[4/7,3/7,0,0])
        np.testing.assert_allclose(e.sample_distribution(z,.5),np.array([16,9,4,1])/30)
        np.testing.assert_allclose(e.sample_distribution(z+10000,top_p=.65),[4/7,3/7,0,0])
        for temperature in (0.,-1.,float('nan')):
            with self.assertRaises(ValueError):e.sample_distribution(z,temperature)
    def test_lora_all_coordinates_and_initialization(self):
        r=e.lora_experiment()
        self.assertLess(max(r['finite_difference_relative_errors'].values()),1e-8)
        self.assertLessEqual(r['update_rank'],r['rank'])
        self.assertEqual(r['zero_B_A_gradient_norm'],0.)
        self.assertGreater(r['zero_B_B_gradient_norm'],0.)
    def test_kl_identity_and_gradient(self):
        ref=np.array([.2,.3,.5]);reward=np.array([-.2,.7,1.3]);beta=.8
        pi=np.array([.4,.2,.4]);q=e.softmax(np.log(ref)+reward/beta)
        gap=e.objective(q,reward,ref,beta)-e.objective(pi,reward,ref,beta)
        self.assertAlmostEqual(gap,beta*np.sum(pi*np.log(pi/q)),places=13)
        z=np.log(pi);g=e.objective_grad(z,reward,ref,beta)
        for i in range(3):
            zp=z.copy();zm=z.copy();zp[i]+=1e-5;zm[i]-=1e-5
            numeric=(e.objective(e.softmax(zp),reward,ref,beta)-e.objective(e.softmax(zm),reward,ref,beta))/2e-5
            self.assertAlmostEqual(numeric,g[i],places=9)
    def test_baseline_unbiased_and_proxy_failure(self):
        r=e.reward_experiment()
        np.testing.assert_allclose(r['gradient_expectation'],r['centered_gradient_expectation'],atol=1e-15)
        self.assertTrue(all(row['objective_gap']<1e-9 for row in r['rows']))
        self.assertGreater(r['rows'][0]['true_success'],r['rows'][1]['true_success'])
    def test_verifier_budget_matches_iid_formula(self):
        r=e.verifier_experiment()
        self.assertEqual(r['exact_validity'],[True,True,False,False])
        for row in r['rows']:
            self.assertLess(abs(row['selected_accuracy']-row['selected_accuracy_exact']),6*row['selection_standard_error']+.001)
        self.assertGreater(r['rows'][2]['selected_accuracy'],r['rows'][-1]['selected_accuracy'])

if __name__=='__main__':unittest.main()
