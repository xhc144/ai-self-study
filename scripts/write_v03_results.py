#!/usr/bin/env python3
"""Generate displayed tables solely from recorded, actually executed runs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    output=ROOT/'book/generated';output.mkdir(exist_ok=True)
    actual=json.loads((ROOT/'results/standard-transformer-v03/metrics.json').read_text())
    table=['\\begin{center}\\begin{tabular}{clrrr}\\toprule','种子 & 条件 & 加权训练 NLL & 均衡训练 NLL & 留出 NLL \\\\ \\midrule']
    for row in actual['runs']:
        label='均衡' if row['condition']=='balanced' else '单条重复'
        table.append(f"{row['seed']} & {label} & {row['weighted_train_nll']:.4f} & {row['balanced_train_nll']:.4f} & {row['test_nll']:.4f} \\\\")
    table+=['\\bottomrule\\end{tabular}\\end{center}']
    (output/'v03-standard-table.tex').write_text('\n'.join(table)+'\n')
    actual=json.loads((ROOT/'results/public-models-v03/metrics.json').read_text())
    table=['\\begin{center}\\begin{tabular}{llrrr}\\toprule','权重 & 输入 & 两选项正确 & 格式通过 & 严格生成正确 \\\\ \\midrule']
    for row in actual['summary']:
        if row['kind']!='all':continue
        label='基础' if not row['model'].endswith('Instruct') else '指令'
        cond='统一文本' if row['condition']=='matched_plain' else '原生聊天'
        fields=[round(row[k]*row['n']) for k in ['forced_choice_accuracy','valid_format_rate','strict_generated_accuracy']]
        table.append(f"{label} & {cond} & {fields[0]}/{row['n']} & {fields[1]}/{row['n']} & {fields[2]}/{row['n']} \\\\")
    table+=['\\bottomrule\\end{tabular}\\end{center}']
    (output/'v03-public-table.tex').write_text('\n'.join(table)+'\n')
    print(json.dumps({'generated':['v03-standard-table.tex','v03-public-table.tex'],'forced_choice_counts':{m+' '+c:{v:sum(r['forced_choice']==v for r in actual['rows'] if r['model']==m and r['condition']==c) for v in ['A','B']} for m,c in {(r['model'],r['condition']) for r in actual['rows']}}}))
if __name__=='__main__':main()
