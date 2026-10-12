#!/usr/bin/env python3
"""Original CPU mechanisms: sparse lookup and correlated pseudo-reference errors.
This is not an Engram or CaT language-model reproduction.
"""
import argparse,json,hashlib,sys,platform
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def lookup_objective(table,ids,targets):
    residual=table[ids]-targets;grad=np.zeros_like(table)
    np.add.at(grad,ids,residual/len(ids))
    return float(np.sum(residual**2)/(2*len(ids))),grad

def run(seed=144):
    rng=np.random.default_rng(seed);table=rng.normal(size=(17,3));ids=np.array([2,2,7,2,11]);targets=rng.normal(size=(5,3));loss,grad=lookup_objective(table,ids,targets)
    eps=1e-5;numeric=np.zeros_like(table)
    for i in range(17):
        for j in range(3):
            plus=table.copy();minus=table.copy();plus[i,j]+=eps;minus[i,j]-=eps
            numeric[i,j]=(lookup_objective(plus,ids,targets)[0]-lookup_objective(minus,ids,targets)[0])/(2*eps)
    keys=np.arange(1000);single=(37*keys+11)%257;second=(53*keys+19)%263
    signatures=list(zip(single.tolist(),second.tolist()));collisions={'single_distinct':len(set(single.tolist())),'two_head_distinct':len(set(signatures)),'keys':len(keys),'table_sizes':[257,263],'scope':'Deterministic integer-key addressing example; not semantic N-grams, cryptographic hashing or Engram performance'}
    rows=[]
    for n in [1,9,33]:
        independent=rng.random((20000,n))<.3
        shared=rng.random((20000,1))<.3;correlated=np.repeat(shared,n,axis=1)
        for name,pred in [('independent',independent),('shared_error',correlated)]:
            # False is the known true label. A group error means selecting True.
            group_error=pred.sum(1)>n//2
            rows.append({'n':n,'dependence':name,'groups':len(pred),'pseudo_reference_error':float(group_error.mean()),'unanimous_group_fraction':float(np.all(pred==pred[:,:1],axis=1).mean()),'marginal_sample_error':float(pred.mean())})
    return {'seed':seed,'scope':'Original numeric mechanism experiment, no LLM, training data or medical task','lookup':{'loss':loss,'active_rows':np.flatnonzero(np.any(grad!=0,axis=1)).tolist(),'finite_difference_max_error':float(np.max(np.abs(grad-numeric))),'repeated_key_count':int(np.sum(ids==2)),'hash_collisions':collisions},'consensus':{'assumed_marginal_error':.3,'truth_label':False,'rows':rows,'warning':'Known synthetic oracle used only to audit pseudo-reference accuracy, not available to aggregator; independent vs shared errors are imposed by generator'}}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'results/research-bridges-v03');p.add_argument('--seed',type=int,default=144);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    text=json.dumps(run(a.seed),ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n';(a.out/'metrics.json').write_text(text)
    env={'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'seed':a.seed,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'metrics_sha256':hashlib.sha256(text.encode()).hexdigest(),'cli':['--seed',str(a.seed)]};(a.out/'environment.json').write_text(json.dumps(env,indent=2)+'\n');print(text)
if __name__=='__main__':main()
