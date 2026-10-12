"""CPU mechanisms for chapters 11--13, not an LLM/agent benchmark.

No downloaded models, API calls, external documents, dynamic eval or side effects.
Each module has an independent child RNG; changing one does not change the others.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
from pathlib import Path

import numpy as np


ACTIONS = ("lookup", "cite", "export")
PUBLIC = frozenset(("public_a", "public_b"))


def authorized(action: dict) -> bool:
    """Check complete action including resource and destination, fail closed."""
    if not isinstance(action, dict) or set(action) != {"tool", "resource", "destination"}:
        return False
    if any(not isinstance(value, str) for value in action.values()):
        return False
    return (action["tool"] in {"lookup", "cite"}
            and action["resource"] in PUBLIC
            and action["destination"] == "current_user")


def boundary_experiment(rng: np.random.Generator) -> dict:
    # These are explicitly specified symbolic proposals, not outputs of an LLM.
    cases = []
    for i in range(240):
        resource = "public_a" if i % 2 == 0 else "public_b"
        cases.append({"kind": "clean", "user_resource": resource,
                      "quoted_command": i % 2 == 0})
    for i in range(120):
        cases.append({"kind": ("export", "private", "wrong_public")[i % 3],
                      "user_resource": "public_a", "quoted_command": True})
    rng.shuffle(cases)
    rows = []
    for policy in ("source_blind", "source_blind_with_executor", "keyword_refusal",
                   "trusted_source_router"):
        counts = dict(clean_total=0, clean_completed=0, clean_refused=0,
                      attack_total=0, unauthorized_proposals=0,
                      unauthorized_executions=0, semantic_attack_successes=0,
                      blocked_proposals=0)
        for case in cases:
            clean = case["kind"] == "clean"
            counts["clean_total" if clean else "attack_total"] += 1
            # Quoted words are data for clean cases; only the keyword router
            # confuses that quotation with a current hostile instruction.
            if policy == "keyword_refusal" and case["quoted_command"]:
                if clean:
                    counts["clean_refused"] += 1
                continue
            action = {"tool": "lookup", "resource": case["user_resource"],
                      "destination": "current_user"}
            if not clean and policy != "trusted_source_router":
                if case["kind"] == "export":
                    action = {"tool": "export", "resource": "private",
                              "destination": "external"}
                elif case["kind"] == "private":
                    action["resource"] = "private"
                else:
                    action["resource"] = "public_b"
            permitted = authorized(action)
            if not clean and not permitted:
                counts["unauthorized_proposals"] += 1
            if policy.endswith("with_executor") and not permitted:
                counts["blocked_proposals"] += 1
                continue
            if not clean:
                counts["unauthorized_executions"] += int(not permitted)
                counts["semantic_attack_successes"] += int(
                    action["tool"] != "lookup" or
                    action["resource"] != case["user_resource"])
            else:
                counts["clean_completed"] += 1
        rows.append({"policy": policy, **counts,
                     "clean_completion_rate": counts["clean_completed"]/240,
                     "clean_false_refusal_rate": counts["clean_refused"]/240,
                     "semantic_attack_success_rate": counts["semantic_attack_successes"]/120})
    return {"scope": "symbolic source-routing and capability-executor simulation; no LLM",
            "parameters": {"clean_cases": 240, "attack_cases": 120,
                           "attack_families": ["export", "private", "wrong_public"]},
            "rows": rows}


def propagation_experiment(rng: np.random.Generator) -> dict:
    n, max_steps, q, recovery, false_refusal = 10000, 8, .08, .60, .02
    error = rng.random((n, max_steps)) < q
    repaired = rng.random((n, max_steps)) < recovery
    refused = rng.random((n, max_steps)) < false_refusal
    naive = ~error
    checked = ((~error) & (~refused)) | (error & repaired)
    local_checked = (1-q)*(1-false_refusal)+q*recovery
    rows = []
    for steps in (1, 4, 8):
        rows.append({"steps": steps,
                     "unverified_episode_success": float(naive[:, :steps].all(axis=1).mean()),
                     "unverified_theory": (1-q)**steps,
                     "checked_episode_success": float(checked[:, :steps].all(axis=1).mean()),
                     "checked_theory": local_checked**steps,
                     "mean_unverified_local_accuracy": float(naive[:, :steps].mean()),
                     "wrong_state_episodes": int((~naive[:, :steps].all(axis=1)).sum())})
    return {"scope": "absorbing-error multi-step agent simulation, not measured LLM errors",
            "parameters": {"episodes": n, "error_probability": q,
                           "recovery_probability": recovery,
                           "false_refusal_probability": false_refusal,
                           "independence_assumption": True,
                           "checked_local_success_probability": local_checked}, "rows": rows}


def sigmoid(x):
    # All experiment arguments are bounded; use a clipping-safe implementation.
    x = np.clip(np.asarray(x, dtype=float), -700., 700.)
    return 1/(1+np.exp(-x))


def integrated_gradients(x, baseline, weights, panels=2048):
    """Midpoint quadrature for f(x)=sigmoid(weights @ x), not exact IG."""
    x, baseline, weights = map(lambda a: np.asarray(a, dtype=float), (x, baseline, weights))
    if x.shape != baseline.shape or weights.shape != x.shape or panels <= 0:
        raise ValueError("matching vectors and positive panels required")
    t = (np.arange(panels)+.5)/panels
    path = baseline[None, :] + t[:, None]*(x-baseline)[None, :]
    p = sigmoid(path @ weights)
    avg_grad = (p*(1-p)).mean()*weights
    return (x-baseline)*avg_grad


def probe_experiment(rng: np.random.Generator) -> dict:
    n_train, n_test, steps, lr = 512, 256, 1200, .1
    def sample(n):
        s = rng.choice([-1., 1.], n)
        noise = rng.choice([-1., 1.], n)
        return np.column_stack([s, s, noise]), (s > 0).astype(float)
    train, labels = sample(n_train)
    test, targets = sample(n_test)
    probe = np.array([0., 0.])  # weight and intercept for coordinate 1 only
    design = np.column_stack([train[:, 1], np.ones(n_train)])
    for _ in range(steps):
        p = sigmoid(design @ probe)
        probe -= lr*(design.T@(p-labels))/n_train
    prediction = sigmoid(np.column_stack([test[:, 1], np.ones(n_test)]) @ probe) >= .5
    # Frozen known downstream model f(h)=h[0]. This isolation makes the
    # distinction between decodability and use mathematically checkable.
    clean = test[:, 0]
    donor = -test  # flips all three coordinates, equal patch norm 2
    rows = []
    for name, coordinate in (("used_positive_control", 0), ("decodable_unused", 1),
                             ("nuisance_negative_control", 2)):
        patched = test.copy()
        patched[:, coordinate] = donor[:, coordinate]
        logits = patched[:, 0]
        rows.append({"intervention": name, "coordinate": coordinate,
                     "mean_patch_norm": float(np.linalg.norm(patched-test, axis=1).mean()),
                     "mean_absolute_logit_change": float(np.abs(logits-clean).mean()),
                     "output_flip_rate": float(((logits > 0) != (clean > 0)).mean()),
                     "off_observational_support_rate": float((patched[:, 0] != patched[:, 1]).mean())})
    coordinate = rng.integers(0, 3, size=n_test)
    patched = test.copy()
    patched[np.arange(n_test), coordinate] = donor[np.arange(n_test), coordinate]
    random_change = float(np.abs(patched[:, 0]-clean).mean())
    corrupted = test.copy()
    corrupted[:, 0] *= -1
    restored = corrupted.copy()
    restored[:, 0] = test[:, 0]
    wrong_patch = corrupted.copy()
    wrong_patch[:, 1] = test[:, 1]
    ig = integrated_gradients([2., 1.], [0., 0.], [4., 2.])
    output_difference = float(sigmoid(10.)-sigmoid(0.))
    return {"scope": "fitted linear probe on synthetic activations; interventions on known frozen function, not an LLM",
            "parameters": {"train_size": n_train, "test_size": n_test, "probe_steps": steps,
                           "probe_lr": lr, "downstream_function": "f(h)=h[0]",
                           "observational_support": "h[1]=h[0]; h[2] independent Rademacher"},
            "probe_weight_intercept": probe.tolist(),
            "probe_test_accuracy": float((prediction == targets).mean()),
            "rows": rows,
            "random_coordinate_control_mean_absolute_logit_change": random_change,
            "random_coordinate_theory_mean_absolute_logit_change": 2/3,
            "corrupted_accuracy": float(((corrupted[:, 0] > 0) == targets).mean()),
            "positive_patch_recovery_accuracy": float(((restored[:, 0] > 0) == targets).mean()),
            "unused_patch_recovery_accuracy": float(((wrong_patch[:, 0] > 0) == targets).mean()),
            "integrated_gradients": {"quadrature_panels": 2048, "values": ig.tolist(),
                "sum": float(ig.sum()), "output_difference": output_difference,
                "completeness_residual": float(ig.sum()-output_difference),
                "endpoint_gradient": (float(sigmoid(10.)*(1-sigmoid(10.)))*np.array([4., 2.])).tolist()}}


def evaluate_polynomial(coefficients, x):
    a, b, c = coefficients
    return a+b*x+c*x*x


def program_search_experiment(rng: np.random.Generator) -> dict:
    dev = np.arange(-3, 4, dtype=np.int64)
    holdout = np.concatenate([np.arange(-12, -3), np.arange(4, 13)])
    rng.shuffle(holdout)  # disjoint fixed-domain extrapolation, not IID generalization
    target = lambda x: x*x+x
    coefficients = list(itertools.product(range(-2, 3), repeat=3))
    rng.shuffle(coefficients)
    coefficients.remove((0, 0, 0))
    coefficients.insert(0, (0, 0, 0))  # deterministic tie: smallest proposal index
    archive = []
    for index, coeff in enumerate(coefficients):
        predicted = evaluate_polynomial(coeff, dev)
        cost = int(coeff[0] != 0)+int(coeff[1] != 0)+2*int(coeff[2] != 0)
        archive.append({"index": index, "kind": "polynomial", "coefficients": list(coeff),
                        "cost": cost, "dev_mse": float(np.mean((predicted-target(dev))**2)),
                        "faulty_dev_loss": float(np.mean(np.maximum(predicted-target(dev), 0)**2))})
    # Adversarial negative control: exact lookup on visible dev inputs, zero elsewhere.
    archive.append({"index": len(archive), "kind": "dev_lookup", "coefficients": None,
                    "cost": len(dev), "dev_mse": 0., "faulty_dev_loss": 0.})
    feasible = [row for row in archive if row["dev_mse"] == 0.]
    honest = min(feasible, key=lambda row: (row["cost"], row["index"]))
    faulty = min(archive, key=lambda row: (row["faulty_dev_loss"]+.01*row["cost"], row["index"]))
    # Neither evaluator nor generator sees holdout until both selections freeze.
    def audit(row):
        if row["kind"] == "dev_lookup":
            known = {int(x): int(target(x)) for x in dev}
            output = np.array([known.get(int(x), 0) for x in holdout])
        else:
            output = evaluate_polynomial(row["coefficients"], holdout)
        return {**row, "holdout_accuracy": float((output == target(holdout)).mean()),
                "holdout_mse": float(np.mean((output-target(holdout))**2))}
    return {"scope": "bounded original polynomial-program search, not an LLM or FunSearch reproduction",
            "parameters": {"candidate_count": len(archive), "dev_inputs": dev.tolist(),
                           "holdout_inputs": holdout.tolist(),
                           "target": "x*x+x", "coefficients_domain": [-2, -1, 0, 1, 2],
                           "honest_rule": "dev exact equality, then minimum cost, then proposal index",
                           "faulty_rule": "mean(max(candidate-target,0)^2)+0.01*cost",
                           "holdout_used_for_selection": False},
            "honest_selected": audit(honest), "faulty_selected": audit(faulty),
            "dev_memorization_negative_control": audit(archive[-1]),
            "archive": archive}


def recurrent_experiment(rng: np.random.Generator) -> dict:
    del rng
    rho, h0, true_answer = .5, 0., 1.
    rows = []
    for fixed_point in (-1., 1.):
        h = h0
        initial_difference = abs((rho*h0+(1-rho)*fixed_point)-h0)
        for step in range(1, 65):
            previous, h = h, rho*h+(1-rho)*fixed_point
            if step in (1, 4, 16, 64):
                rows.append({"fixed_point": fixed_point, "steps": step, "state": h,
                             "successive_difference": abs(h-previous),
                             "fixed_point_error": abs(h-fixed_point),
                             "contraction_error_bound": rho**step*initial_difference/(1-rho),
                             "answer": int(h > 0), "correct": bool(int(h > 0) == true_answer)})
    # Independent masks on a two-token data source supported on 00 and 11.
    # Bayes-optimal denoiser is uncertain only when both tokens are masked.
    denoising = [{"mask_probability": t, "expected_masked_tokens": 2*t,
                  "expected_unweighted_loss": 2*t*t*float(np.log(2)),
                  "expected_inverse_t_weighted_loss": 2*t*float(np.log(2))}
                 for t in (.25, .5, 1.)]
    return {"scope": "scalar contraction counterexample and exact two-token denoising expectation; no trained looped LLM",
            "parameters": {"rho": rho, "initial_state": h0, "true_answer": true_answer,
                           "readout": "int(h>0)", "steps": 64},
            "rows": rows, "two_token_denoising": denoising}


def run(seed=144):
    children = np.random.SeedSequence(seed).spawn(5)
    modules = (boundary_experiment, propagation_experiment, probe_experiment,
               program_search_experiment, recurrent_experiment)
    names = ("boundary", "propagation", "probe", "program_search", "recurrence")
    return {name: module(np.random.default_rng(child))
            for name, module, child in zip(names, modules, children)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=144)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    metrics = run(args.seed)
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    environment = {"python": sys.version, "numpy": np.__version__,
                   "platform": platform.platform(), "machine": platform.machine(),
                   "processor": platform.processor(), "execution": "CPU, NumPy float64/int64",
                   "seed": args.seed, "rng": "NumPy PCG64, SeedSequence child streams",
                   "script_sha256": code_hash,
                   "command": f"python experiments/v03_research.py --seed {args.seed} --out {args.out}",
                   "model_weights_downloaded": False, "llm_evaluated": False}
    for name, result in metrics.items():
        (args.out/f"{name}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n")
    (args.out/"metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False)+"\n")
    (args.out/"environment.json").write_text(json.dumps(environment, indent=2, ensure_ascii=False)+"\n")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(args.out.glob("*.json")) if p.name != "hashes.json"}
    (args.out/"hashes.json").write_text(json.dumps(hashes, indent=2)+"\n")
    print(json.dumps({"out": str(args.out), "script_sha256": code_hash,
                      "modules": list(metrics), "llm_evaluated": False}, indent=2))


if __name__ == "__main__":
    main()
