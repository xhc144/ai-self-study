import unittest
import numpy as np
from experiments.research_bridges import lookup_objective,run
class ResearchBridges(unittest.TestCase):
    def test_shared_lookup_accumulates_and_unread_rows_are_zero(self):
        table=np.array([[0.,0.],[1.,2.],[3.,4.]])
        ids=np.array([1,1]);targets=np.array([[0.,0.],[3.,4.]])
        value,grad=lookup_objective(table,ids,targets)
        self.assertAlmostEqual(value,3.25)
        np.testing.assert_array_equal(grad,[[0,0],[-.5,0],[0,0]])
    def test_balanced_opposite_dependencies_cancel(self):
        table=np.array([[0.]])
        value,grad=lookup_objective(table,np.array([0,0]),np.array([[1.],[-1.]]))
        self.assertEqual(value,.5);self.assertEqual(grad[0,0],0.)
    def test_imposed_shared_error_is_not_independent_evidence(self):
        result=run(144)
        for row in result['consensus']['rows']:
            if row['dependence']=='shared_error':
                self.assertEqual(row['unanimous_group_fraction'],1.)
                self.assertEqual(row['pseudo_reference_error'],row['marginal_sample_error'])
        self.assertLess(result['lookup']['finite_difference_max_error'],1e-8)
