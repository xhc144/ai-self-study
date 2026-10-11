"""New numerical invariants, shared-path faults and CLI parameter evidence."""
import hashlib,json,math,subprocess,sys,tempfile,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from attention_walkthrough import attention_walkthrough,residual_debug
from micro_research import exact_binomial_interval

class RevisionChecks(unittest.TestCase):
    def test_attention_closed_form_and_update(self):
        r=attention_walkthrough();a=1/(1+math.exp(2));res=2-a-1.5
        self.assertAlmostEqual(r['loss_before'],res**2/2,places=14)
        self.assertAlmostEqual(r['parameter_gradients']['Q'][0][0],2*a*(1-a)*res,places=14)
        self.assertAlmostEqual(r['parameter_gradients']['V'][0][0],(2-a)*res,places=14)
        self.assertLess(r['loss_after'],r['loss_before'])
    def test_deliberate_fault_localizes_before_embedding(self):
        r=residual_debug(seed=19)
        self.assertLess(max(r['correct_errors'].values()),1e-7)
        failing={k for k,v in r['omitted_residual_errors'].items() if v>1e-7}
        self.assertEqual(failing,{'E','P'})
    def test_duplicate_gather_gradient_accumulates(self):
        grad=np.zeros((3,2));np.add.at(grad,[1,1],[[2,-1],[3,4]])
        np.testing.assert_array_equal(grad,[[0,0],[5,3],[0,0]])
    def test_binomial_boundaries_and_primary_reference_case(self):
        low,high=exact_binomial_interval(5,5)
        self.assertAlmostEqual(low,.025**.2,places=14);self.assertEqual(high,1)
        low,high=exact_binomial_interval(0,5)
        self.assertEqual(low,0);self.assertAlmostEqual(high,1-.025**.2,places=14)
        low,high=exact_binomial_interval(4,20,alpha=.1)
        self.assertAlmostEqual(low,.071354,delta=1e-6);self.assertAlmostEqual(high,.401029,delta=1e-6) # handbook decimal precision
    def test_discrete_interval_coverage_for_fixed_n(self):
        # Enumerate all possible counts, rather than sampling the implementation.
        n=5;intervals=[exact_binomial_interval(k,n) for k in range(n+1)]
        for p in np.linspace(0,1,1001):
            coverage=sum(math.comb(n,k)*p**k*(1-p)**(n-k) for k,(a,b) in enumerate(intervals) if a<=p<=b)
            self.assertGreaterEqual(coverage,.95-1e-12)
    def test_cli_selected_parameters_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(ROOT/'experiments/run_all.py'),'--experiment','language_model','--seed','7','--steps','2','--width','4','--lr','.005','--out',tmp],check=True,stdout=subprocess.PIPE)
            metrics=json.loads((Path(tmp)/'metrics.json').read_text())['language_model']
            env=json.loads((Path(tmp)/'environment.json').read_text())
            self.assertEqual(metrics['seed'],7);self.assertEqual(metrics['steps'],2)
            self.assertEqual(env['executed_parameters']['language_model'],{'seed':7,'steps':2,'lr':.005,'width':4})
    def test_cli_explicit_design_is_exploratory(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);design=folder/'custom-design.json'
            config=json.loads((ROOT/'research/design-v02.json').read_text())
            config.update(steps=1,seeds=[149])
            design.write_text(json.dumps(config))
            expected_hash=hashlib.sha256(design.read_bytes()).hexdigest()
            out=folder/'custom-results'
            subprocess.run([sys.executable,str(ROOT/'experiments/run_all.py'),
                            '--experiment','micro_research','--design',str(design),
                            '--out',str(out)],check=True,stdout=subprocess.PIPE)
            metrics=json.loads((out/'metrics.json').read_text())['micro_research']
            self.assertEqual(metrics['exploratory_overrides'],
                             {'design':{'path':str(design.resolve()),'sha256':expected_hash}})
            self.assertEqual(metrics['design_sha256'],expected_hash)
            self.assertEqual(metrics['executed_config'],config)
            self.assertEqual(len(metrics['runs']),3)
            self.assertTrue(all(r['seed']==149 and r['train_trace'][0][0]==1
                                for r in metrics['runs']))
            # Even explicitly selecting the frozen file must keep its CLI provenance.
            out=folder/'explicit-frozen-results';frozen=ROOT/'research/design-v02.json'
            subprocess.run([sys.executable,str(ROOT/'experiments/run_all.py'),
                            '--experiment','micro_research','--design',str(frozen),
                            '--steps','1','--seeds','149','--out',str(out)],
                           check=True,stdout=subprocess.PIPE)
            overrides=json.loads((out/'metrics.json').read_text())['micro_research']['exploratory_overrides']
            self.assertEqual(overrides,{'design':{'path':str(frozen.resolve()),
                                                'sha256':hashlib.sha256(frozen.read_bytes()).hexdigest()},
                                        'steps':1,'seeds':[149]})

if __name__=='__main__':unittest.main()
