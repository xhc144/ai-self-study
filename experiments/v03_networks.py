#!/usr/bin/env python3
"""Original, CPU-only numerical lessons for chapters 5--7; no old results touched."""
import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
import numpy as np

SEED = 144


def softmax(scores):
    """Finite logits only; the masked routine below handles excluded entries."""
    shifted = scores - np.max(scores, axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=-1, keepdims=True)


def ce(logits, targets):
    rows = logits.reshape(-1, logits.shape[-1])
    y = np.asarray(targets).ravel()
    top = rows.max(1, keepdims=True)
    logsum = np.log(np.exp(rows - top).sum(1))
    loss = np.mean(logsum - (rows[np.arange(len(y)), y] - top[:, 0]))
    grad = softmax(rows)
    grad[np.arange(len(y)), y] -= 1
    return float(loss), (grad / len(y)).reshape(logits.shape)


def init_batch(rng):
    return dict(E=rng.normal(0, .3, (5, 3)), P=rng.normal(0, .2, (3, 3)),
                W1=rng.normal(0, .4, (3, 4)), b1=rng.normal(0, .1, 4),
                W2=rng.normal(0, .4, (4, 3)), U=rng.normal(0, .3, (3, 3)),
                b2=rng.normal(0, .1, 3))


def batch_loss_grad(params, ids, targets, omit_direct=False):
    """Gather + position broadcast + nonlinear branch + direct logits branch."""
    p = params
    x = p['E'][ids] + p['P'][:ids.shape[1]]
    h = np.tanh(x @ p['W1'] + p['b1'])
    loss, dz = ce(h @ p['W2'] + x @ p['U'] + p['b2'], targets)
    da = (dz @ p['W2'].T) * (1 - h * h)
    flatx, flath = x.reshape(-1, 3), h.reshape(-1, 4)
    g = dict(W2=flath.T @ dz.reshape(-1, 3), U=flatx.T @ dz.reshape(-1, 3),
             b2=dz.sum(axis=(0, 1)), W1=flatx.T @ da.reshape(-1, 4),
             b1=da.sum(axis=(0, 1)))
    dx = da @ p['W1'].T
    if not omit_direct:
        dx = dx + dz @ p['U'].T
    g['P'] = np.zeros_like(p['P'])
    g['P'][:ids.shape[1]] = dx.sum(axis=0)
    g['E'] = np.zeros_like(p['E'])
    np.add.at(g['E'], ids, dx)
    return loss, g


def finite_difference(loss_fn, params, grads, eps=1e-5):
    """All coordinates, normalized by max(1, |numeric|, |analytic|)."""
    result = {}
    for key, array in params.items():
        errors = []
        for idx in np.ndindex(array.shape):
            old = float(array[idx])
            try:
                array[idx] = old + eps
                plus = loss_fn()
                array[idx] = old - eps
                minus = loss_fn()
            finally:
                array[idx] = old
            numeric = (plus - minus) / (2 * eps)
            analytic = float(grads[key][idx])
            if not np.isfinite([numeric, analytic]).all():
                raise FloatingPointError(f'{key}{idx}')
            errors.append(abs(numeric - analytic) / max(1., abs(numeric), abs(analytic)))
        result[key] = float(max(errors))
    return result


def batch_experiment(seed):
    p = init_batch(np.random.default_rng(seed))
    ids = np.array([[1, 1, 2], [2, 3, 1]])
    y = np.array([[0, 2, 1], [1, 0, 2]])
    loss, g = batch_loss_grad(p, ids, y)
    correct = finite_difference(lambda: batch_loss_grad(p, ids, y)[0], p, g)
    _, bad = batch_loss_grad(p, ids, y, omit_direct=True)
    fault = finite_difference(lambda: batch_loss_grad(p, ids, y)[0], p, bad)
    repeated_loss, repeated_g = batch_loss_grad(p, np.tile(ids, (2, 1)), np.tile(y, (2, 1)))
    duplicate_gap = max(float(np.max(abs(g[k] - repeated_g[k]))) for k in g)
    updated = {k: v - .05 * g[k] for k, v in p.items()}
    return dict(seed=seed, shape={'B': 2, 'T': 3, 'D': 3, 'hidden': 4, 'classes': 3},
                checked_coordinates=sum(v.size for v in p.values()), loss_before=loss,
                loss_after=batch_loss_grad(updated, ids, y)[0], learning_rate=.05,
                finite_difference_step=1e-5, correct_errors=correct,
                omitted_direct_errors=fault,
                failing_groups=[k for k, v in fault.items() if v > 1e-7],
                duplicated_batch_loss_gap=abs(loss - repeated_loss),
                duplicated_batch_gradient_max_gap=duplicate_gap,
                gradient_norms={k: float(np.linalg.norm(v)) for k, v in g.items()})


def _validate_attention(q, k, v, allowed):
    if q.ndim != 2 or k.ndim != 2 or v.ndim != 2:
        raise ValueError('Q,K,V must be matrices')
    if q.shape[1] == 0 or q.shape[1] != k.shape[1] or k.shape[0] != v.shape[0]:
        raise ValueError('incompatible attention dimensions')
    if allowed.shape != (q.shape[0], k.shape[0]) or allowed.dtype != np.bool_:
        raise ValueError('allowed must be a boolean query-by-key matrix')
    if not np.all(allowed.any(1)):
        raise ValueError('every query must have an allowed key')
    if not all(np.isfinite(a).all() for a in (q, k, v)):
        raise ValueError('finite inputs required')


def dense_attention(q, k, v, allowed):
    _validate_attention(q, k, v, allowed)
    scores = q @ k.T / np.sqrt(q.shape[1])
    scores = np.where(allowed, scores, -np.inf)
    weights = np.exp(scores - scores.max(1, keepdims=True))
    weights /= weights.sum(1, keepdims=True)
    return weights @ v, weights


def attention_backward(q, k, v, weights, gc):
    ga = gc @ v.T
    gs = weights * (ga - (weights * ga).sum(1, keepdims=True))
    return dict(Q=gs @ k / np.sqrt(q.shape[1]),
                K=gs.T @ q / np.sqrt(q.shape[1]), V=weights.T @ gc)


def blocked_attention(q, k, v, allowed, query_block=8, key_block=7):
    """Online stable softmax; no T-by-T scores or probabilities are allocated.

    The pedagogical boolean mask is supplied by the caller and may itself be T².
    The memory claim applies to score/probability workspace, not the given mask.
    Entirely forbidden blocks are skipped, including before the first valid key.
    """
    _validate_attention(q, k, v, allowed)
    if query_block < 1 or key_block < 1:
        raise ValueError('positive block sizes required')
    out = np.zeros((len(q), v.shape[1]), dtype=np.float64)
    for start in range(0, len(q), query_block):
        end = min(start + query_block, len(q))
        size = end - start
        maximum = np.full(size, -np.inf)
        normalizer = np.zeros(size)
        numerator = np.zeros((size, v.shape[1]))
        for j in range(0, len(k), key_block):
            stop = min(j + key_block, len(k))
            mask = allowed[start:end, j:stop]
            active = mask.any(1)
            if not active.any():
                continue
            score = q[start:end][active] @ k[j:stop].T / np.sqrt(q.shape[1])
            score = np.where(mask[active], score, -np.inf)
            new_max = np.maximum(maximum[active], score.max(1))
            old_scale = np.exp(maximum[active] - new_max)
            exp = np.exp(score - new_max[:, None])
            normalizer[active] = old_scale * normalizer[active] + exp.sum(1)
            numerator[active] = old_scale[:, None] * numerator[active] + exp @ v[j:stop]
            maximum[active] = new_max
        out[start:end] = numerator / normalizer[:, None]
    return out


def attention_experiment(seed):
    rng = np.random.default_rng(seed)
    t, dk, dv = 37, 5, 7
    q, k, v = rng.normal(size=(t, dk)), rng.normal(size=(t, dk)), rng.normal(size=(t, dv))
    allowed = np.tri(t, dtype=bool)
    dense, a = dense_attention(q, k, v, allowed)
    gaps = {}
    for br, bc in [(1, 1), (4, 6), (8, 7), (50, 50)]:
        gaps[f'{br}x{bc}'] = float(np.max(abs(dense - blocked_attention(q, k, v, allowed, br, bc))))
    # Scale dot products into the saturated regime, without exponential overflow.
    extreme, _ = dense_attention(q * 100., k * 100., v, allowed)
    extreme_gap = float(np.max(abs(extreme - blocked_attention(q * 100., k * 100., v, allowed))))
    # Shared-input self-attention: change all future Q/K/V, retain the prefix.
    x = rng.normal(size=(t, 5)); wq, wk = rng.normal(size=(5, 5)), rng.normal(size=(5, 5))
    wv = rng.normal(size=(5, 7)); changed = x.copy(); cut = 15
    changed[cut:] += rng.normal(0, 9., size=changed[cut:].shape)
    def output(z, mask):
        return dense_attention(z @ wq, z @ wk, z @ wv, mask)[0]
    masked_gap = float(np.max(abs(output(x, allowed)[:cut] - output(changed, allowed)[:cut])))
    full = np.ones((t, t), dtype=bool)
    unmasked_gap = float(np.max(abs(output(x, full)[:cut] - output(changed, full)[:cut])))
    # The derivative check is of an arbitrary linear downstream loss, not just a norm.
    params = {'Q': q[:4].copy(), 'K': k[:4].copy(), 'V': v[:4].copy()}
    small_mask = np.tri(4, dtype=bool); gc = rng.normal(size=(4, dv))
    _, weights = dense_attention(params['Q'], params['K'], params['V'], small_mask)
    grads = attention_backward(**dict(q=params['Q'], k=params['K'], v=params['V'], weights=weights, gc=gc))
    errors = finite_difference(lambda: float(np.sum(dense_attention(params['Q'], params['K'], params['V'], small_mask)[0] * gc)), params, grads)
    return dict(seed=seed, T=t, dk=dk, dv=dv, prefix_length=cut,
                blocked_max_abs_gaps=gaps, extreme_score_gap=extreme_gap,
                masked_prefix_max_abs_gap=masked_gap, unmasked_prefix_max_abs_gap=unmasked_gap,
                forbidden_weight_max=float(a[~allowed].max()), row_sum_max_error=float(abs(a.sum(1) - 1).max()),
                backward_errors=errors, checked_coordinates=sum(z.size for z in params.values()),
                workspace_note='Counts below are maximum elements in one score array, not process peak memory. Given dense boolean mask is not counted.',
                dense_score_elements=t*t, blocked_score_elements=8*7,
                note='CPU NumPy equivalence check; no CUDA/FlashAttention speed claim.')


def layernorm_forward(x, gamma, beta, eps=1e-5):
    if eps <= 0:
        raise ValueError('eps must be positive')
    centered = x - x.mean(-1, keepdims=True)
    inv = 1. / np.sqrt((centered * centered).mean(-1, keepdims=True) + eps)
    normalized = centered * inv
    return normalized * gamma + beta, (normalized, inv)


def layernorm_backward(upstream, gamma, cache):
    normalized, inv = cache
    u = upstream * gamma
    dx = inv * (u - u.mean(-1, keepdims=True) - normalized * (u * normalized).mean(-1, keepdims=True))
    axes = tuple(range(upstream.ndim - 1))
    return dict(x=dx, gamma=(upstream * normalized).sum(axis=axes), beta=upstream.sum(axis=axes))


def layernorm_experiment(seed):
    rng = np.random.default_rng(seed)
    p = dict(x=rng.normal(size=(2, 3, 4)), gamma=rng.normal(size=4), beta=rng.normal(size=4))
    up = rng.normal(size=p['x'].shape)
    _, cache = layernorm_forward(**p)
    grads = layernorm_backward(up, p['gamma'], cache)
    errors = finite_difference(lambda: float(np.sum(layernorm_forward(**p)[0] * up)), p, grads)
    constant = np.full((1, 4), 3.)
    _, constant_cache = layernorm_forward(constant, np.ones(4), np.zeros(4))
    constant_grad = layernorm_backward(np.array([[1., 2., 3., 4.]]), np.ones(4), constant_cache)['x']
    return dict(seed=seed, eps=1e-5, shape=[2, 3, 4], finite_difference_errors=errors,
                constant_row_gradient=constant_grad.tolist(),
                constant_row_gradient_norm=float(np.linalg.norm(constant_grad)),
                note='Positive epsilon prevents singularity but can produce a large finite derivative near zero variance.')


def sigmoid(x):
    return np.exp(-np.logaddexp(0., -x))


def binary_metrics(logits, y, temperature=1., bins=10):
    z = logits / temperature
    prob = sigmoid(z)
    nll = float(np.mean(np.logaddexp(0., z) - y * z))
    binid = np.minimum((prob * bins).astype(int), bins - 1)
    table = []
    for j in range(bins):
        mask = binid == j
        if mask.any():
            table.append(dict(bin=j, count=int(mask.sum()), probability=float(prob[mask].mean()), frequency=float(y[mask].mean())))
    ece = sum(r['count'] * abs(r['probability'] - r['frequency']) for r in table) / len(y)
    return dict(nll=nll, brier=float(np.mean((prob-y)**2)), accuracy=float(np.mean((z >= 0) == y)),
                binned_probability_calibration_error=ece, bins=table)


def calibration_experiment(seed):
    rng = np.random.default_rng(seed)
    true_val = rng.normal(0, 1.5, 800); true_test = rng.normal(0, 1.5, 5000)
    yval = rng.binomial(1, sigmoid(true_val)); ytest = rng.binomial(1, sigmoid(true_test))
    temperatures = np.linspace(.5, 5., 91)
    val_scores = [binary_metrics(3 * true_val, yval, t)['nll'] for t in temperatures]
    chosen = float(temperatures[np.argmin(val_scores)])
    return dict(seed=seed, generator='x~N(0,1.5^2), y|x~Bernoulli(sigmoid(x)); model logit=3x',
                n_validation=800, n_test=5000, temperature_grid=temperatures.tolist(), chosen_temperature=chosen,
                validation_grid_nll=val_scores,
                validation_before=binary_metrics(3 * true_val, yval),
                validation_after=binary_metrics(3 * true_val, yval, chosen),
                test_before=binary_metrics(3 * true_test, ytest),
                test_after=binary_metrics(3 * true_test, ytest, chosen),
                note='Controlled overconfident model, not trained here. Temperature is selected only by validation NLL; test is measured once after selection. Bin error concerns positive-class probability, not top-class confidence ECE.')


def selection_experiment(seed):
    rng = np.random.default_rng(seed)
    reps, nval, ntest = 400, 32, 2000
    counts = [1, 8, 64, 512]
    # Independent Bernoulli loss coordinates of a fixed finite candidate family.
    validation = rng.binomial(nval, .5, size=(reps, max(counts))) / nval
    rows = []
    for m in counts:
        best = validation[:, :m].min(1)
        independent = rng.binomial(ntest, .5, size=reps) / ntest
        rows.append(dict(candidates=m, validation_selected_mean=float(best.mean()),
                         independent_test_mean=float(independent.mean()),
                         optimism_mean=float((independent-best).mean()),
                         optimism_standard_error=float((independent-best).std(ddof=1)/np.sqrt(reps))))
    return dict(seed=seed, repetitions=reps, n_validation=nval, n_test=ntest,
                true_risk_all_candidates=.5, rows=rows,
                note='Synthetic independent loss table, not fitted neural models. Test losses are sampled only for the selected candidate; all candidates have known risk 0.5.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=SEED)
    args = parser.parse_args()
    start = time.perf_counter()
    results = {name: fn(args.seed) for name, fn in [
        ('batch', batch_experiment), ('attention', attention_experiment),
        ('layernorm', layernorm_experiment), ('calibration', calibration_experiment),
        ('selection', selection_experiment)]}
    args.out.mkdir(parents=True, exist_ok=True)
    code = Path(__file__).resolve()
    evidence = dict(seed=args.seed, python=sys.version, numpy=np.__version__, platform=platform.platform(),
                    processor=platform.processor(), dtype='float64', backend='CPU NumPy',
                    script=str(code), code_sha256=hashlib.sha256(code.read_bytes()).hexdigest(),
                    command=sys.argv, elapsed_seconds=time.perf_counter()-start,
                    executed_parameters={k: {kk: vv for kk, vv in v.items() if kk in
                    {'seed','shape','eps','T','dk','dv','n_validation','n_test','repetitions','learning_rate','finite_difference_step','checked_coordinates'}}
                    for k, v in results.items()})
    (args.out / 'metrics.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    (args.out / 'environment.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in {
        'correct_errors','failing_groups','blocked_max_abs_gaps','masked_prefix_max_abs_gap',
        'unmasked_prefix_max_abs_gap','chosen_temperature','rows','finite_difference_errors'}}
        for k, v in results.items()}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
