"""Independent invariants and finite-difference regression checks."""
import importlib.util, unittest
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location('experiment',Path(__file__).resolve().parents[1]/'experiments/run_all.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

class MathChecks(unittest.TestCase):
    def test_extreme_cross_entropy(self):
        loss,g=e.cross_entropy(np.array([[0.,-1000.]]),np.array([1]))
        self.assertEqual(loss,1000.)
        np.testing.assert_allclose(g,[[1.,-1.]])
    def test_large_common_logit_shift(self):
        loss,_=e.cross_entropy(np.array([[1e16,1e16]]),np.array([0]))
        self.assertAlmostEqual(loss,float(np.log(2)),places=14)
    def test_nonfinite_gradient_rejected(self):
        with self.assertRaises(FloatingPointError):
            e.gradient_error(lambda:float('nan'),{'z':np.array([1.])},{'z':np.array([0.])},np.random.default_rng(1))
    def test_softmax_translation(self):
        z=np.array([[.1,1.7,-.8],[2.,-.2,4.]])
        np.testing.assert_allclose(e.softmax(z),e.softmax(z+10000),atol=1e-12)
        np.testing.assert_allclose(e.softmax(z).sum(1),1.)
    def test_all_small_decoder_coordinates(self):
        m=e.TinyDecoder(vocab=6,context=3,width=4,seed=19)
        x=np.array([[0,1,2],[3,4,1]]);y=np.array([[1,2,5],[4,1,5]])
        loss,g=m.loss_grad(x,y)
        er=e.gradient_error(lambda:m.loss_grad(x,y)[0],m.p,g,np.random.default_rng(20),checks=10000)
        self.assertTrue(np.isfinite(loss));self.assertLess(max(er.values()),1e-7)
    def test_causal_prefix_for_all_future_positions(self):
        m=e.TinyDecoder(vocab=6,context=5,width=4,seed=21)
        x=np.array([[0,1,2,3,4]])
        before=m.forward(x)[0]
        for k in range(1,5):
            edited=x.copy();edited[0,k]=(edited[0,k]+1)%6
            after=m.forward(edited)[0]
            np.testing.assert_allclose(before[:,:k],after[:,:k],rtol=0,atol=0)
    def test_kl_optimal_objective_identity(self):
        ref=np.array([.15,.25,.6]);r=np.array([-1.,.2,2.]);beta=.7
        q=e.softmax(np.log(ref)+r/beta);p=np.array([.3,.2,.5])
        objective=lambda a: a@r-beta*np.sum(a*np.log(a/ref))
        gap=objective(q)-objective(p)
        self.assertAlmostEqual(gap,beta*np.sum(p*np.log(p/q)),places=12)
        self.assertGreaterEqual(gap,0.)

if __name__=='__main__':unittest.main()
