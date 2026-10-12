#!/usr/bin/env python3
"""CPU-only language mechanisms; synthetic examples, no downloads.
Run with PYTHONDONTWRITEBYTECODE=1 python experiments/v03_language.py.
"""
import argparse
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('v03_original_decoder', ROOT/'experiments/run_all.py')
_original = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_original)
SEED = 144


def softmax(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(z-z.max(axis=-1, keepdims=True))
    return e/e.sum(axis=-1, keepdims=True)


def sample_distribution(logits, temperature=1., top_p=1., top_k=None):
    z = np.asarray(logits, dtype=float)
    if z.ndim != 1 or not np.isfinite(z).all() or not z.size:
        raise ValueError('logits must be a finite nonempty vector')
    if not np.isfinite(temperature) or temperature <= 0 or not 0 < top_p <= 1:
        raise ValueError('positive finite temperature and 0 < top_p <= 1 required')
    if top_k is not None and (not isinstance(top_k, int) or not 1 <= top_k <= len(z)):
        raise ValueError('top_k must be an integer between one and vocabulary size')
    p = softmax(z/temperature)
    order = np.argsort(-p, kind='stable')
    if top_k is not None:
        order = order[:top_k]
    # Apply k first, normalize, then choose the smallest p-threshold prefix.
    ordered = p[order]/p[order].sum()
    count = len(order) if top_p == 1 else min(len(order), int(np.searchsorted(np.cumsum(ordered), top_p))+1)
    keep = order[:count]
    q = np.zeros_like(p)
    q[keep] = p[keep]/p[keep].sum()
    return q


class CachedDecoder:
    """Incremental evaluator sharing frozen TinyDecoder parameters, batch dimension retained."""
    def __init__(self, model):
        self.model = model
        self.keys = self.values = None
        self.position = 0

    def step(self, ids):
        ids = np.asarray(ids)
        if ids.ndim != 1:
            raise ValueError('step requires one token id per batch row')
        p = self.model.p
        if self.position >= len(p['P']):
            raise ValueError('position exceeds model context')
        if self.keys is not None and len(ids) != len(self.keys):
            raise ValueError('batch size must remain fixed')
        x = p['E'][ids][:, None, :] + p['P'][self.position]
        q, k, v = (x @ p[name] for name in ('Q', 'K', 'V'))
        self.keys = k if self.keys is None else np.concatenate((self.keys, k), axis=1)
        self.values = v if self.values is None else np.concatenate((self.values, v), axis=1)
        a = softmax(q @ self.keys.transpose(0, 2, 1)/np.sqrt(self.model.d))
        h = x + (a @ self.values) @ p['O']
        f = np.tanh(h @ p['F'] + p['bF'])
        logits = (h + f @ p['G'] + p['bG']) @ p['U'] + p['bU']
        self.position += 1
        return logits[:, 0, :]


def cache_experiment(seed=SEED):
    rng = np.random.default_rng(seed)
    batch, length, width, vocab = 3, 12, 8, 10
    m = _original.TinyDecoder(vocab, context=length, width=width, seed=seed)
    ids = rng.integers(0, vocab, (batch, length))
    cached = CachedDecoder(m)
    errors = []
    for t in range(length):
        full = m.forward(ids[:, :t+1])[0][:, -1, :]
        errors.append(float(np.max(np.abs(full-cached.step(ids[:, t])))))
    edited = ids.copy(); edited[:, -1] = (edited[:, -1]+1) % vocab
    causal_error = float(np.max(np.abs(m.forward(ids)[0][:, :-1]-m.forward(edited)[0][:, :-1])))
    return dict(seed=seed, batch=batch, length=length, width=width, vocab=vocab,
                per_position_max_logit_error=errors, max_logit_error=max(errors),
                future_edit_prefix_error=causal_error, cache_shape=list(cached.keys.shape),
                cache_elements=int(cached.keys.size+cached.values.size),
                full_prefix_score_pairs=batch*sum(t*t for t in range(1, length+1)),
                cached_score_pairs=batch*sum(range(1, length+1)),
                note='Counts are dense score entries for repeated prefixes, not measured wall-clock speedups.')


def sampling_experiment(seed=SEED):
    rng = np.random.default_rng(seed)
    logits = np.log([.4, .3, .2, .1])
    rows = []
    for temp, threshold, k in [(1., 1., None), (.5, 1., None), (2., 1., None), (1., .65, None), (1., 1., 2)]:
        q = sample_distribution(logits, temp, threshold, k)
        counts = np.bincount(rng.choice(4, 50000, p=q), minlength=4)
        rows.append(dict(temperature=temp, top_p=threshold, top_k=k, probabilities=q.tolist(),
                         sampled_frequencies=(counts/50000).tolist(),
                         entropy=float(-np.sum(q[q>0]*np.log(q[q>0])))))
    return dict(seed=seed, logits=logits.tolist(), samples_per_setting=50000, rows=rows,
                note='Distribution changes only; no claim that lower entropy gives more correct answers.')


def lora_loss_grad(A, B, X, target, W0, scale):
    # X: n,d; target: n,m; A:r,d; B:m,r; W0:m,d.
    error = X @ (W0+scale*B@A).T-target
    G = error.T @ X/len(X)
    return float(np.sum(error*error)/(2*len(X))), scale*B.T@G, scale*G@A.T


def lora_experiment(seed=SEED):
    rng = np.random.default_rng(seed)
    n, d, m, rank, scale = 7, 5, 4, 2, .75
    X, target, W0 = rng.normal(size=(n,d)), rng.normal(size=(n,m)), rng.normal(size=(m,d))
    A, B = rng.normal(size=(rank,d)), rng.normal(size=(m,rank))
    loss, ga, gb = lora_loss_grad(A,B,X,target,W0,scale)
    errors = {}
    for name, parameter, gradient in [('A',A,ga),('B',B,gb)]:
        worst = 0.
        for idx in np.ndindex(parameter.shape):
            old = parameter[idx]; eps = 1e-5
            try:
                parameter[idx] = old+eps; plus = lora_loss_grad(A,B,X,target,W0,scale)[0]
                parameter[idx] = old-eps; minus = lora_loss_grad(A,B,X,target,W0,scale)[0]
            finally:
                parameter[idx] = old
            numeric = (plus-minus)/(2*eps)
            worst = max(worst, abs(numeric-gradient[idx])/max(1.,abs(numeric),abs(gradient[idx])))
        errors[name] = worst
    zero_b = np.zeros_like(B)
    _, initial_a, initial_b = lora_loss_grad(A,zero_b,X,target,W0,scale)
    return dict(seed=seed, batch=n, input_width=d, output_width=m, rank=rank, scale=scale,
                loss=loss, finite_difference_relative_errors=errors,
                update_rank=int(np.linalg.matrix_rank(B@A)), trainable_parameters=A.size+B.size,
                full_matrix_parameters=W0.size, zero_B_A_gradient_norm=float(np.linalg.norm(initial_a)),
                zero_B_B_gradient_norm=float(np.linalg.norm(initial_b)),
                note='For these tiny dimensions r(m+d)=18 versus md=20; savings require r<md/(m+d).')


def objective(pi, reward, ref, beta):
    return float(pi@reward-beta*np.sum(pi*np.log(pi/ref)))


def objective_grad(logits, reward, ref, beta):
    pi = softmax(logits)
    u = reward-beta*(np.log(pi/ref)+1)
    return pi*(u-pi@u)


def reward_experiment(seed=SEED):
    ref = np.array([.1,.1,.77,.03]); beta = .3
    true = np.array([1.,1.,0.,0.]); proxy = np.array([1.,1.,0.,2.])
    rows = []
    for reward in (true, proxy):
        logits = np.log(ref).copy()
        for _ in range(30000):
            logits += .2*objective_grad(logits,reward,ref,beta)
        pi = softmax(logits); optimal = softmax(np.log(ref)+reward/beta)
        rows.append(dict(reward=reward.tolist(), learned_probabilities=pi.tolist(),
                         analytic_probabilities=optimal.tolist(), true_success=float(pi@true),
                         proxy_reward=float(pi@proxy), objective_gap=objective(optimal,reward,ref,beta)-objective(pi,reward,ref,beta),
                         max_probability_error=float(np.max(np.abs(pi-optimal)))))
    p = ref
    scores = np.eye(4)-p[None,:]
    no_baseline = true[:,None]*scores
    baseline = float(p@true)
    centered = (true-baseline)[:,None]*scores
    mean = np.sum(p[:,None]*no_baseline,axis=0)
    def total_variance(arr):
        return float(np.sum(p[:,None]*(arr-mean)**2))
    return dict(seed=seed, reference=ref.tolist(), beta=beta, steps=30000, learning_rate=.2,
                rows=rows, baseline=baseline, gradient_expectation=mean.tolist(),
                centered_gradient_expectation=np.sum(p[:,None]*centered,axis=0).tolist(),
                variance_without_baseline=total_variance(no_baseline),
                variance_with_mean_reward_baseline=total_variance(centered),
                note='Exact finite-action expectations; mean reward is useful here but is not universally variance optimal.')


def verifier_experiment(seed=SEED):
    rng = np.random.default_rng(seed)
    # Each independent candidate: correct=.20, highest proxy-score false=.03, other wrong=.77.
    candidates = np.array([[1,8],[8,1],[4,6],[0,0]])
    pi = np.array([.1,.1,.77,.03]); trials = 20000
    exact = np.sum(candidates*candidates,axis=1) == 65
    scores = np.array([1,1,0,2])
    rows = []
    for budget in (1,4,16,64,256):
        actions = rng.choice(4,(trials,budget),p=pi)
        correct = exact[actions]
        selected = np.argmax(scores[actions],axis=1)
        rate = float(correct[np.arange(trials),selected].mean())
        rows.append(dict(budget=budget, trials=trials, coverage=float(correct.any(axis=1).mean()),
                         coverage_exact=1-.8**budget, selected_accuracy=rate,
                         selected_accuracy_exact=.97**budget-.77**budget,
                         selection_standard_error=float(np.sqrt(rate*(1-rate)/trials))))
    return dict(seed=seed, candidates=candidates.tolist(), action_probabilities=pi.tolist(),
                exact_validity=exact.tolist(), proxy_scores=scores.tolist(), rows=rows,
                note='IID synthetic actions with replacement; exact coverage is achievable only with exact verification and abstention.')


def icl_experiment(seed=SEED):
    # Fixed Bayesian predictor, not a claim about a trained Transformer's algorithm.
    X = np.array([[1.], [2.]])
    y = np.array([2., 4.])
    prior_precision = np.eye(1)
    sigma2 = 1.
    precision = prior_precision + X.T@X/sigma2
    mean = np.linalg.solve(precision, X.T@y/sigma2)
    covariance = np.linalg.inv(precision)
    query = np.array([3.])
    return dict(seed=seed, support_inputs=X.tolist(), support_targets=y.tolist(),
                prior_mean=[0.], prior_covariance=[[1.]], noise_variance=sigma2,
                posterior_mean=mean.tolist(), posterior_covariance=covariance.tolist(),
                query=query.tolist(), predictive_mean=float(query@mean),
                predictive_variance=float(sigma2+query@covariance@query),
                prior_predictive_mean=0., prior_predictive_variance=10.,
                trainable_weight_updates=0,
                note='An exact fixed conditional predictor illustrates task inference; no LLM or universal Bayesian-mechanism claim.')


def run(seed=SEED):
    return dict(icl=icl_experiment(seed),cache=cache_experiment(seed),sampling=sampling_experiment(seed),
                lora=lora_experiment(seed),reward=reward_experiment(seed),verifier=verifier_experiment(seed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',type=int,default=SEED)
    parser.add_argument('--out',type=Path,default=ROOT/'results/v03-language')
    args=parser.parse_args()
    if args.seed<0: parser.error('seed must be nonnegative')
    metrics=run(args.seed)
    args.out.mkdir(parents=True,exist_ok=True)
    sources=[Path(__file__),ROOT/'experiments/run_all.py']
    environment=dict(seed=args.seed,python=sys.version,numpy=np.__version__,platform=platform.platform(),
                     dtype='float64',device='CPU',command='PYTHONDONTWRITEBYTECODE=1 python experiments/v03_language.py --seed '+str(args.seed),
                     source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    (args.out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    (args.out/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    print(json.dumps(dict(cache_error=metrics['cache']['max_logit_error'],lora_errors=metrics['lora']['finite_difference_relative_errors'],
                          reward_gaps=[r['objective_gap'] for r in metrics['reward']['rows']],
                          verifier_selected=[r['selected_accuracy'] for r in metrics['verifier']['rows']]),indent=2))

if __name__=='__main__': main()
