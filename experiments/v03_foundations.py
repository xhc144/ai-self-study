"""Reproducible CPU illustrations for chapters 2--4. NumPy only; seed 144."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
import sys
from pathlib import Path
import numpy as np


def binomial_interval(k: int, n: int, alpha: float = .05) -> tuple[float, float]:
    """Invert exact binomial tails (Clopper--Pearson), without SciPy."""
    if not isinstance(n, int) or not isinstance(k, int) or n <= 0 or not 0 <= k <= n or not 0 < alpha < 1:
        raise ValueError("require integers 0 <= k <= n, n > 0 and 0 < alpha < 1")
    def tail(p, lo, hi):
        return sum(math.comb(n, j) * p**j * (1-p)**(n-j) for j in range(lo, hi+1))
    def bisect(fn, increasing):
        left, right = 0., 1.
        for _ in range(70):
            mid = (left+right)/2
            below = fn(mid) < alpha/2
            if below == increasing:
                left = mid
            else:
                right = mid
        return (left+right)/2
    lower = 0. if k == 0 else bisect(lambda p: tail(p,k,n), True)
    upper = 1. if k == n else bisect(lambda p: tail(p,0,k), False)
    return lower, upper


def ridge_svd(x, y, lam):
    """Minimize ||Xw-y||^2/(2n) + lam ||w||^2/2; lam > 0."""
    if lam <= 0:
        raise ValueError("positive lambda required")
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    return vt.T @ ((s/(s*s + len(y)*lam))*(u.T@y))


def information(p, q):
    p, q = np.asarray(p,dtype=float), np.asarray(q,dtype=float)
    if p.shape != q.shape or np.any(p < 0) or np.any(q < 0) or not np.isclose(p.sum(),1) or not np.isclose(q.sum(),1):
        raise ValueError("probability vectors required")
    mask = p > 0
    entropy = float(-np.sum(p[mask]*np.log(p[mask])))
    ce = float(-np.sum(p[mask]*np.log(q[mask]))) if np.all(q[mask] > 0) else math.inf
    return {"entropy":entropy,"cross_entropy":ce,"kl":ce-entropy}


def adam_step(w, grad, m, v, t, lr, beta1=.9, beta2=.999, eps=1e-8):
    if t < 1:
        raise ValueError("Adam steps start at 1")
    m = beta1*m+(1-beta1)*grad
    v = beta2*v+(1-beta2)*grad*grad
    return w-lr*(m/(1-beta1**t))/(np.sqrt(v/(1-beta2**t))+eps),m,v


def linear_experiment(rng):
    rank_x = np.array([[1.,1.],[2.,2.]])
    rank_y = np.array([1.,0.])
    w = np.linalg.lstsq(rank_x,rank_y,rcond=None)[0]
    n = 80
    a, z = rng.normal(size=(2,n))
    x = np.column_stack([a,a+1e-5*z])
    y = 2*a + .02*rng.normal(size=n)
    perturbation = 1e-4*z
    ordinary = np.linalg.lstsq(x,y,rcond=None)[0]
    perturbed = np.linalg.lstsq(x,y+perturbation,rcond=None)[0]
    lam = .01
    regular = ridge_svd(x,y,lam)
    reg_pert = ridge_svd(x,y+perturbation,lam)
    s = np.linalg.svd(x,compute_uv=False)
    return {"parameters":{"n":n,"collinear_noise":1e-5,"label_noise":.02,"perturbation_scale":1e-4,"lambda":lam},
            "rank_deficient":{"rank":int(np.linalg.matrix_rank(rank_x)),"minimum_norm_weights":w.tolist(),"prediction":(rank_x@w).tolist(),"residual":(rank_y-rank_x@w).tolist(),"normal_equation_residual":float(np.linalg.norm(rank_x.T@(rank_x@w-rank_y)))},
            "singular_values":s.tolist(),"condition_x":float(s[0]/s[-1]),"condition_gram_from_singular_values":float((s[0]/s[-1])**2),
            "condition_regularized":float((s[0]**2/n+lam)/(s[-1]**2/n+lam)),
            "ordinary_weights":ordinary.tolist(),"ridge_weights":regular.tolist(),
            "ordinary_weight_change":float(np.linalg.norm(perturbed-ordinary)),"ridge_weight_change":float(np.linalg.norm(reg_pert-regular)),
            "ordinary_prediction_change":float(np.linalg.norm(x@(perturbed-ordinary))),
            "ridge_prediction_change":float(np.linalg.norm(x@(reg_pert-regular)))}


def probability_experiment(rng):
    p = .7
    n = 100
    k = int(rng.binomial(n,p))
    lower,upper = binomial_interval(k,n)
    probabilities = np.array([.2,.8])
    group_size = 2000
    observed = rng.binomial(1, probabilities[:,None],size=(2,group_size))
    calibrated = probabilities
    overconfident = np.array([.05,.95])
    def score(q):
        nll = float(-np.mean(observed*np.log(q[:,None])+(1-observed)*np.log1p(-q[:,None])))
        true_ce = float(np.mean(-probabilities*np.log(q)-(1-probabilities)*np.log1p(-q)))
        return {"probabilities":q.tolist(),"empirical_nll":nll,"population_cross_entropy":true_ce,
                "accuracy":float(np.mean(observed == (q[:,None]>.5))),
                "group_calibration_gap":float(np.mean(np.abs(observed.mean(axis=1)-q)))}
    repetitions = 3000
    counts = rng.binomial(n,p,size=repetitions)
    intervals = [binomial_interval(j,n) for j in range(n+1)]
    covered = sum(intervals[int(j)][0] <= p <= intervals[int(j)][1] for j in counts)
    return {"parameters":{"true_p":p,"n":n,"alpha":.05,"ci_repetitions":repetitions,"group_size":group_size},
            "count":k,"mle":k/n,"exact_binomial_interval":[lower,upper],"coverage_simulation":covered/repetitions,
            "chebyshev_95_radius":math.sqrt(1/(4*n*.05)),
            "group_observed_frequencies":observed.mean(axis=1).tolist(),"calibrated":score(calibrated),"overconfident":score(overconfident),
            "balanced":information([.5,.5],[.5,.5]),"unbalanced":information([.5,.5],[.9,.1]),
            "bayes_positive_disease":(.9*.01)/(.9*.01+.05*.99)}


def optimization_experiment(rng):
    h = np.array([1.,10.])
    w0 = np.array([1.,1.])
    steps = 80
    records = []
    for lr in [.1,.19,.2,.21]:
        w = w0.copy()
        losses = [float(.5*np.sum(h*w*w))]
        for _ in range(steps):
            w -= lr*h*w
            losses.append(float(.5*np.sum(h*w*w)))
        records.append({"lr":lr,"steps":steps,"initial_loss":losses[0],"final_loss":losses[-1],"final_w":w.tolist(),"trace":losses})
    stochastic_steps = 1000
    noise_std = .5
    noise = rng.normal(0,noise_std,size=(stochastic_steps,2))
    runs = {}
    for name,lr in [("sgd",.05),("adam",.03)]:
        w=w0.copy();m=np.zeros(2);v=np.zeros(2);tail=[];trace=[]
        for t in range(1,stochastic_steps+1):
            grad=h*w+noise[t-1]
            if name == "sgd":
                w -= lr*grad
            else:
                w,m,v=adam_step(w,grad,m,v,t,lr)
            loss=float(.5*np.sum(h*w*w))
            if t > 800: tail.append(loss)
            if t in [1,10,100,500,1000]: trace.append([t,loss])
        runs[name]={"lr":lr,"final_w":w.tolist(),"final_loss":loss,"mean_last_200_loss":float(np.mean(tail)),"trace":trace}
    gradient = np.array([2.,-3.])
    _,m,v=adam_step(np.zeros(2),gradient,np.zeros(2),np.zeros(2),1,.01)
    return {"parameters":{"hessian_diagonal":h.tolist(),"initial_w":w0.tolist(),"gd_steps":steps,"stochastic_steps":stochastic_steps,"gradient_noise_std":noise_std,"shared_noise":True,"beta1":.9,"beta2":.999,"epsilon":1e-8},
            "gd":records,"stochastic":runs,"adam_first_step":{"m":m.tolist(),"v":v.tolist(),"corrected_m":(m/.1).tolist(),"corrected_v":(v/.001).tolist()},
            "sgd_stationary_coordinate_variance":[.05*noise_std**2/(hi*(2-.05*hi)) for hi in h]}


def hand_examples():
    joint = np.array([[.3,.2],[.1,.4]])
    logits = np.array([0.,math.log(3)])
    probs = np.exp(logits)/np.exp(logits).sum()
    x = np.array([[1.,2.]])
    w = np.array([[3.],[4.]])
    gy = x@w-10
    tiny = np.array([.001])
    after,_,_ = adam_step(tiny,tiny,np.zeros(1),np.zeros(1),1,.1)
    return {"sequence_joint":joint.tolist(),"second_a_given_first_a":float(joint[0,0]/joint[0].sum()),
            "second_a_marginal":float(joint[:,0].sum()),"softmax_probabilities":probs.tolist(),
            "softmax_hard_label_loss":float(-np.log(probs[0])),"softmax_gradient":(probs-np.array([1.,0.])).tolist(),
            "matrix_y":(x@w).tolist(),"matrix_grad_w":(x.T@gy).tolist(),"matrix_grad_x":(gy@w.T).tolist(),
            "adam_increase_example":{"w_before":tiny.tolist(),"w_after":after.tolist(),
                                     "loss_before":float(.5*np.sum(tiny*tiny)),"loss_after":float(.5*np.sum(after*after))}}


def run(seed=144):
    # Separate streams keep chapter results stable if another experiment changes.
    streams = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(3)]
    return {"seed":seed,"hand_examples":hand_examples(),"linear":linear_experiment(streams[0]),"probability":probability_experiment(streams[1]),"optimization":optimization_experiment(streams[2])}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=Path("results/v03-foundations"))
    parser.add_argument("--seed",type=int,default=144)
    args=parser.parse_args()
    result=run(args.seed)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"metrics.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    environment={"python":sys.version,"numpy":np.__version__,"platform":platform.platform(),"dtype":"float64","seed":args.seed,
                 "executed_parameters":{k:result[k]["parameters"] for k in ["linear","probability","optimization"]},
                 "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"command":[sys.executable,*sys.argv]}
    (args.out/"environment.json").write_text(json.dumps(environment,indent=2)+"\n")
    print(json.dumps({"out":str(args.out),"seed":args.seed,"code_sha256":environment["code_sha256"]}))

if __name__ == "__main__":
    main()
