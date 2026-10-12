#!/usr/bin/env python3
"""Recount frozen inputs and stored outputs; never run or alter model experiments."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit() -> dict:
    design_path = ROOT / 'research/design-public-models-v03.json'
    metrics_path = ROOT / 'results/public-models-v03/metrics.json'
    design = json.loads(design_path.read_text())
    metrics = json.loads(metrics_path.read_text())
    design_sha = hashlib.sha256(design_path.read_bytes()).hexdigest()
    assert metrics['design_sha256'] == design_sha
    cases = {c['id']: c for c in design['cases']}
    inputs = defaultdict(list)
    for c in design['cases']:
        inputs[(c['system'], c['user'])].append(c)
    for group in inputs.values():
        assert len({c['truth'] for c in group}) == 1
    rows = defaultdict(list)
    conditions = defaultdict(list)
    for row in metrics['rows']:
        c = cases[row['case']]
        assert row['truth'] == c['truth']
        key = (row['model'], row['condition'], c['system'], c['user'])
        rows[key].append(row)
    identical = all(len({json.dumps({k: v for k, v in row.items() if k != 'case'}, sort_keys=True)
                         for row in group}) == 1 for group in rows.values())
    assert identical
    actual_prompt_combinations = {
        (row['model'], row['condition'], row['prompt']) for row in metrics['rows']
    }
    assert len(actual_prompt_combinations) == len(rows)
    for key, group in rows.items():
        conditions[key[:2]].append(group[0])
    deduplicated = []
    for (model, condition), group in conditions.items():
        for kind in ['all', 'arithmetic', 'context_mapping', 'role_conflict']:
            selected = [row for row in group if kind == 'all' or row['kind'] == kind]
            deduplicated.append({
                'model': model, 'condition': condition, 'kind': kind,
                'unique_inputs': len(selected),
                'forced_choice_correct': sum(row['forced_choice_correct'] for row in selected),
                'strict_generated_correct': sum(row['strict_generated_correct'] for row in selected),
                'valid_AB_format': sum(row['valid_AB_format'] for row in selected),
            })
    return {
        'scope': 'Post-hoc descriptive audit of unchanged frozen design and stored results; not a preregistered outcome and no new model runs.',
        'design_sha256': design_sha,
        'metrics_sha256': hashlib.sha256(metrics_path.read_bytes()).hexdigest(),
        'record_slots': len(design['cases']),
        'unique_system_user_inputs': len(inputs),
        'unique_inputs_by_kind': dict(Counter(group[0]['kind'] for group in inputs.values())),
        'duplicate_case_groups': [[c['id'] for c in group] for group in inputs.values() if len(group) > 1],
        'actual_output_records': len(metrics['rows']),
        'unique_input_model_format_combinations': len(rows),
        'unique_stored_prompt_model_format_combinations': len(actual_prompt_combinations),
        'duplicate_stored_outputs_identical_except_case_id': identical,
        'generation': design['generation'],
        'sampling_warning': 'Deterministic duplicate inputs are not independent samples and do not increase task or attack coverage; 12 fixed unique inputs are not a random population sample either.',
        'deduplicated_recount': deduplicated,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.write_text(json.dumps(audit(), ensure_ascii=False, indent=2) + '\n')
