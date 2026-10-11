#!/usr/bin/env python3
"""Generate original plots and TeX text from executed metrics only."""
import json, os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/ai-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
r=ROOT/'results'
m=json.loads((r/'metrics.json').read_text())
dest=ROOT/'book/generated';dest.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'figure.figsize':(6,3),'savefig.bbox':'tight'})
for name in ['mlp','language_model']:
    tr=np.array(m[name]['trace']);fig,ax=plt.subplots()
    ax.plot(tr[:,0],tr[:,1],label='train')
    if tr.shape[1]==3:ax.plot(tr[:,0],tr[:,2],label='held-out combinations')
    ax.set(xlabel='Updates',ylabel='Mean token NLL' if name=='language_model' else 'Cross entropy')
    ax.legend();fig.savefig(dest/(name+'.pdf'));plt.close(fig)
models=m['spurious']['models'];fig,ax=plt.subplots()
x=np.arange(2);w=.35
ax.bar(x-w/2,[a['iid_accuracy'] for a in models],w,label='IID')
ax.bar(x+w/2,[a['shifted_accuracy'] for a in models],w,label='shifted')
ax.set(xticks=x,xticklabels=['both features','robust feature'],ylim=(0,1.05),ylabel='Accuracy')
ax.legend();fig.savefig(dest/'spurious.pdf');plt.close(fig)
a=m['language_model'];g=max(a['gradient_errors'].values())
mantissa,exponent=f'{g:.2e}'.split('e')
g_tex=mantissa+r'\times10^{'+str(int(exponent))+'}'
summary=(
 f"本次实际执行的训练平均交叉熵为 ${a['train_loss']:.4f}$, 两个留出组合的平均交叉熵为 ${a['test_loss']:.4f}$. "
 f"叫声位置准确率为 ${a['sound_accuracy']:.0%}$, 只看最后一个词的基线为 ${a['last_token_baseline_accuracy']:.0%}$. "
 f"各参数组抽样梯度检查的最大误差为 ${g_tex}$, 因果前缀检查的最大 logit 差为 ${a['causal_prefix_max_error']:.1f}$. "
 "这些数值仅对应当前代码、种子与划分.\n")
(dest/'summary.tex').write_text(summary.replace('%',r'\%'))
print('Generated plots and summary from metrics.json')
