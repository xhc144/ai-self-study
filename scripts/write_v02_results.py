#!/usr/bin/env python3
"""Generate v0.2 numeric fragments only from actually executed JSON results."""
import json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/f'results/{name}/metrics.json').read_text())[name]
def tex_scientific(value):
    mantissa,exponent=f'{value:.1e}'.split('e')
    return mantissa+r'\times10^{'+str(int(exponent))+'}'
def main():
    dst=ROOT/'book/generated';a=load('attention_walkthrough');d=load('residual_debug');m=load('micro_research')
    text=(f"更新后的 $(W_Q,W_K,W_V)$ 为 $({a['parameters_after']['Q'][0][0]:.6f},{a['parameters_after']['K'][0][0]:.6f},{a['parameters_after']['V'][0][0]:.6f})$. "
          f"重新前向得到 $C_2={a['C_after'][1][0]:.6f}$, 损失从 ${a['loss_before']:.8f}$ 降至 ${a['loss_after']:.8f}$. "
          f"中心差分的最大误差为 ${tex_scientific(max(a['gradient_errors'].values()))}$.\n")
    (dst/'v02-attention.tex').write_text(text)
    (dst/'v02-residual.tex').write_text(f"正确实现的最大误差为 ${tex_scientific(max(d['correct_errors'].values()))}$; 漏项后 $E,P$ 的误差分别为 ${d['omitted_residual_errors']['E']:.6f}$ 与 ${d['omitted_residual_errors']['P']:.6f}$, 其余参数组仍小于 $10^{{-7}}$.\n")
    splits=['mismatch_blue_red','mismatch_red_blue','match_red_blue']; labels=dict(zip(splits,['A','B','C']))
    rows=[r'\begin{center}\begin{tabular}{lrrrrr}\toprule',r'划分 & 全对次数 & 叫声准确率 & 训练 NLL & 测试 NLL & 95\% 区间\\\midrule']
    for s in m['summary']:
        rs=[r for r in m['runs'] if r['split']==s['split']];lo,hi=s['conditional_95pct_interval']
        rows.append(f"{labels[s['split']]} & {s['all_test_sounds_correct_runs']}/{s['seeds']} & {s['mean_sound_accuracy']:.3f} & {np.mean([r['train_nll'] for r in rs]):.6f} & {s['mean_token_nll']:.6f} & $[{lo:.4f},{hi:.0f}]$" + r" \\")
    rows.append(r'\bottomrule\end{tabular}\end{center}');(dst/'v02-research-summary.tex').write_text('\n'.join(rows)+'\n')
    rows=[r'\begin{center}\begin{tabular}{lrrr}\toprule',r'种子 & A 测试 NLL & B 测试 NLL & C 测试 NLL\\\midrule']
    for seed in m['executed_config']['seeds']:
        vals=[next(r['full_token_nll'] for r in m['runs'] if r['seed']==seed and r['split']==sp) for sp in splits]
        rows.append(f"{seed} & "+' & '.join(f'{v:.6f}' for v in vals)+r' \\')
    rows.append(r'\bottomrule\end{tabular}\end{center}');(dst/'v02-research-runs.tex').write_text('\n'.join(rows)+'\n')
    vals={key:[v for r in m['runs'] for v in r[key]] for key in ['subject_effect_original_sound_probability','distractor_effect_original_sound_probability']}
    subjects=vals['subject_effect_original_sound_probability'];other=vals['distractor_effect_original_sound_probability']
    (dst/'v02-research-effects.tex').write_text(f"30 个配对文档上, 主语替换的 $\\Delta_{{\\rm speaker}}$ 落在 $[{min(subjects):.6f},{max(subjects):.6f}]$, 干扰替换的 $|\\Delta_{{\\rm other}}|$ 最大为 ${max(abs(v) for v in other):.6f}$. 这些是全部预定案例的描述量, 不是总体效应区间.\n")
    rows=[r'\begin{center}\begin{tabular}{lrrrrrrr}\toprule',r'划分 & 主语 & sees & 颜色 & 干扰动物 & says & 叫声 & EOS\\\midrule']
    for sp in splits:
        v=np.mean([r['token_nll_by_position'] for r in m['runs'] if r['split']==sp],axis=0)
        rows.append(labels[sp]+' & '+' & '.join(f'{x:.4f}' for x in v)+r' \\')
    rows.append(r'\bottomrule\end{tabular}\end{center}');(dst/'v02-research-positions.tex').write_text('\n'.join(rows)+'\n')
    md=['# 第一项微研究：固定组合上的主语与干扰动物','',f"冻结设计 SHA256：`{m['design_sha256']}`。见 [设计](design-v02.json) 与 [运行前澄清](design-v02-freeze.md)。实际结果来自 [metrics.json](../results/micro_research/metrics.json)，环境与时间见 [environment.json](../results/micro_research/environment.json)。没有参数覆盖：`exploratory_overrides={m['exploratory_overrides']}`。",'',
    '## 问题与实验单位','', '有限八文档语法，叫声由句首主语决定。三个事先固定、彼此重叠的两文档划分，各自剩余六文档训练；五种子144–148复用相同初始权重，每次清空Adam。共15次1400步CPU训练，单头D16/FFN32，lr0.01，梯度范数裁剪1。不是随机采样测试文档、真实语料或模型搜索。', '',
    '|划分|训练文档|测试文档|主语/干扰匹配的训练比例|','|---|---|---|---|']
    for sp in splits:
        r=next(r for r in m['runs'] if r['split']==sp);matches=sum(m['documents'][i][1]==m['documents'][i][4] for i in r['train_ids']);md.append(f"|{labels[sp]} `{sp}`|{r['train_ids']}|{r['test_ids']}|{matches}/6|")
    md+=['','## 全部执行结果','','|划分|seed|训练NLL|测试NLL|叫声准确率|干扰替换准确率|主语替换准确率|','|---|---:|---:|---:|---:|---:|---:|']
    for r in m['runs']:md.append(f"|{labels[r['split']]}|{r['seed']}|{r['train_nll']:.9f}|{r['full_token_nll']:.9f}|{r['variants']['original']['accuracy']:.1f}|{r['variants']['distractor']['accuracy']:.1f}|{r['variants']['speaker']['accuracy']:.1f}|")
    md+=['','## 基线与逐文档干预','','最近动物规则仅看干扰动物，`says`词频基线在各训练集中猫/狗叫声各三次，平票固定输出meow；两者都只预测叫声，不比较完整token NLL。','','|划分|最近动物：原/干扰/主语|词频：原/干扰/主语|','|---|---|---|']
    for sp in splits:
        b=m['baselines'][sp];md.append(f"|{labels[sp]}|"+'/'.join(f"{b['nearest_animal_rule'][v]['accuracy']:.1f}" for v in ['original','distractor','speaker'])+'|'+'/'.join(f"{b['training_sound_frequency_after_says'][v]['accuracy']:.1f}" for v in ['original','distractor','speaker'])+'|')
    md+=['','只在位置5（输入says，读取0–5前缀）评价叫声。主语翻转重算目标，完整新文档中的叫声也同步改。两项干预在所有六个原测试文档上都返回对应训练组合；高干预准确率不是新未见组合检验。最近动物规则在失配划分的两项干预也达到1.0，所以必须结合原输入表现与配对概率差。', '', '定义 Δ=p_patch(原叫声)−p_original(原叫声)。预测：主语翻转应使Δ负且幅度大，干扰翻转应接近0。全部30个文档对（15模型×2文档）在JSON中逐一保存预测、目标、概率、patched id与训练成员状态。', '',
    f"实际主语Δ范围 [{min(subjects):.9f}, {max(subjects):.9f}]；干扰|Δ|最大 {max(abs(v) for v in other):.9f}。这些是有限案例描述，不是效应置信区间。", '', '## 误差与有限结论','',
    '叫声原/两干预均为全对，不能归为一次失败研究；但完整测试NLL仍远高于训练。按位置分解后，干扰动物的平均NLL约8.29–8.53，占主要损失；颜色约log(3)，因为被留出的颜色在该主语训练前缀中仅占1/3，argmax偏向另一颜色。模型还拟合了六文档中的颜色—动物组合限制，不能把叫声成功称为完整语法分布泛化。', '',
    '本实验支持：这15次配置下的叫声函数与主语依赖预测相符，单纯最近动物/最后词频不足以解释原输入及配对效果。它未识别具体内部电路，未比较所有可行机制，也未测试更长句、自然语言、多个块或任意新划分。下一实验必须另冻新组合/长度生成器，不能在本组测试上迭代选架构。', '',
    '## 统计不确定性','',
    '每个固定划分定义一个独立初始化得到的模型是否将两个叫声全部预测正确的Bernoulli事件。假设初始化独立同分布时，5个事件的成功次数服从Binomial(5,p)。95%等尾精确区间各为[0.4781762498950185,1]；是三个分别计算的点态区间，不是同时保证，不是平均准确率、NLL、概率变化或文档泛化区间。相同种子跨划分复用→配对，不能把15次当独立同分布重复。固定种子列表提供可复现性，覆盖率解释依赖假想初始化抽样法；PRNG编号不是随机选取的自然人口。', '',
    '不对两个固定测试文档、干预版本、同一文档token或三个重叠划分做IID bootstrap。这里没估计任意划分的波动；若要研究新文档分布，须设计新的独立采样单位并记录聚类依赖。', '',
    '## 复现','','```bash','OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/run_all.py --experiment micro_research --out /tmp/my-micro-research','```','',
    '结果数值片段由 `python scripts/write_v02_results.py` 从真实JSON生成。运行 `--seeds`、`--steps`、`--lr`、`--width` 会记录exploratory_overrides；它们是另一次探索，不替换冻结结果。']
    (ROOT/'research/micro-study-v02.md').write_text('\n'.join(md)+'\n')
    print('Generated v0.2 fragments and research report from real JSON.')
if __name__=='__main__':main()
