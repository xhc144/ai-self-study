"""Mathematical invariants and boundary failures in the foundation tools."""
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from v03_foundations import adam_step,binomial_interval,hand_examples,information,ridge_svd,run


class FoundationsChecks(unittest.TestCase):
    def test_rank_deficient_projection_and_minimum_norm(self):
        x=np.array([[1.,1.],[2.,2.]]);y=np.array([1.,0.])
        w=np.linalg.lstsq(x,y,rcond=None)[0]
        np.testing.assert_allclose(w,[.1,.1],atol=1e-14)
        np.testing.assert_allclose(x.T@(y-x@w),0,atol=1e-14)
        for a in [-10,-1,0,1,10]:
            alternative=w+a*np.array([1.,-1.])
            np.testing.assert_allclose(x@alternative,x@w,atol=1e-14)
            self.assertGreaterEqual(np.linalg.norm(alternative),np.linalg.norm(w))

    def test_ridge_diagonal_closed_form_including_null_direction(self):
        x=np.diag([3.,1.,0.]);y=np.array([2.,-4.,7.]);lam=.2
        expected=np.array([6/(9+3*lam),-4/(1+3*lam),0])
        np.testing.assert_allclose(ridge_svd(x,y,lam),expected,rtol=1e-14)
        self.assertRaises(ValueError,ridge_svd,x,y,0)

    def test_kl_support_and_independent_formula(self):
        result=information([.5,.5],[.9,.1])
        self.assertAlmostEqual(result['kl'],math.log(25/9)/2,places=14)
        self.assertEqual(information([1,0],[1,0])['kl'],0)
        self.assertTrue(math.isinf(information([1,0],[0,1])['kl']))
        self.assertRaises(ValueError,information,[1,1],[.5,.5])

    def test_softmax_gradient_and_curvature(self):
        z=np.array([.4,-.7,1.2]);p=np.array([.2,.3,.5])
        def loss(v):
            a=v.max();return -p@v+a+np.log(np.exp(v-a).sum())
        q=np.exp(z-z.max());q/=q.sum();grad=q-p
        for i in range(3):
            e=np.eye(3)[i]*1e-5
            self.assertAlmostEqual((loss(z+e)-loss(z-e))/2e-5,grad[i],places=9)
        h=np.diag(q)-np.outer(q,q)
        np.testing.assert_allclose(h@np.ones(3),0,atol=1e-15)
        self.assertGreaterEqual(np.linalg.eigvalsh(h).min(),-1e-15)

    def test_matrix_gradients_and_shared_embedding_accumulation(self):
        x=np.array([[1.,2.],[-1.,3.]])
        w=np.array([[.2,-.4],[.7,.9]])
        target=np.array([[1.,0.],[0.,1.]])
        gy=x@w-target;gradient=x.T@gy
        for i,j in itertools.product(range(2),repeat=2):
            delta=np.zeros_like(w);delta[i,j]=1e-5
            fd=(np.sum((x@(w+delta)-target)**2)-np.sum((x@(w-delta)-target)**2))/4e-5
            self.assertAlmostEqual(fd,gradient[i,j],places=8)
        indices=np.array([0,1,0]);downstream=np.array([[1.,2.],[3.,4.],[-2.,5.]])
        accumulated=np.zeros((2,2));np.add.at(accumulated,indices,downstream)
        np.testing.assert_array_equal(accumulated,[[-1,7],[3,4]])

    def test_gd_strict_step_boundary(self):
        r=run()['optimization']['gd']
        by_lr={v['lr']:v for v in r}
        self.assertLess(by_lr[.1]['final_loss'],1e-7)
        self.assertAlmostEqual(abs(by_lr[.2]['final_w'][1]),1,places=14)
        self.assertGreater(by_lr[.21]['final_loss'],1e7)
        for a,b in zip(by_lr[.19]['trace'],by_lr[.19]['trace'][1:]):
            self.assertLessEqual(b,a+1e-14)

    def test_sgd_variance_recurrence_by_enumerating_noise(self):
        # Exact finite distribution, rather than a noisy Monte Carlo pass/fail.
        eta=.1;a=2.;sigma=.5;steps=6;coefficient=1-eta*a
        values=[]
        for signs in itertools.product([-1.,1.],repeat=steps):
            w=0.
            for sign in signs:w=coefficient*w-eta*sigma*sign
            values.append(w)
        expected=eta**2*sigma**2*sum(coefficient**(2*j) for j in range(steps))
        self.assertAlmostEqual(np.var(values),expected,places=15)

    def test_adam_initialization_correction_and_loss_increase(self):
        grad=np.array([2.,-3.]);zero=np.zeros(2)
        after,m,v=adam_step(zero,grad,zero,zero,1,.01)
        np.testing.assert_allclose(m/(1-.9),grad,rtol=1e-14)
        np.testing.assert_allclose(v/(1-.999),grad*grad,rtol=1e-14)
        np.testing.assert_allclose(after,-.01*grad/(np.abs(grad)+1e-8),rtol=1e-14)
        sample=hand_examples()['adam_increase_example']
        self.assertGreater(sample['loss_after'],sample['loss_before']*9000)
        # Bias correction is a weighted history, not the latest gradient.
        m=np.zeros(1);v=np.zeros(1);w=np.zeros(1)
        for t,g in enumerate([1.,3.],1):w,m,v=adam_step(w,np.array([g]),m,v,t,.01)
        self.assertAlmostEqual((m/(1-.9**2))[0],(0.9+3)/1.9,places=14)
        self.assertNotAlmostEqual((m/(1-.9**2))[0],3.)

    def test_exact_interval_boundaries_and_coverage(self):
        n=5;intervals=[binomial_interval(k,n) for k in range(n+1)]
        self.assertAlmostEqual(intervals[0][1],1-.025**(1/n),places=14)
        self.assertAlmostEqual(intervals[-1][0],.025**(1/n),places=14)
        for p in np.linspace(0,1,401):
            mass=sum(math.comb(n,k)*p**k*(1-p)**(n-k) for k,(lo,hi) in enumerate(intervals) if lo<=p<=hi)
            self.assertGreaterEqual(mass,.95-1e-12)
        for args in [(1,0),(7,5),(-1,5),(1,5,1)]:self.assertRaises(ValueError,binomial_interval,*args)

    def test_cli_provenance_and_determinism(self):
        with tempfile.TemporaryDirectory() as tmp:
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
            subprocess.run([sys.executable,str(ROOT/'experiments/v03_foundations.py'),'--out',tmp],check=True,stdout=subprocess.PIPE,env=env)
            metrics=json.loads((Path(tmp)/'metrics.json').read_text())
            record=json.loads((Path(tmp)/'environment.json').read_text())
            self.assertEqual(metrics,run(seed=144))
            self.assertEqual(record['seed'],144)
            self.assertEqual(record['code_sha256'],hashlib.sha256((ROOT/'experiments/v03_foundations.py').read_bytes()).hexdigest())
            self.assertEqual(record['executed_parameters']['probability']['n'],100)

if __name__=='__main__':unittest.main()
