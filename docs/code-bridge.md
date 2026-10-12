# 从公式到代码

| 阅读对象 | 实现与结果 |
|---|---|
| 数学工具附录的病态矩阵、对数似然、梯度 | `experiments/v03_foundations.py` → `results/v03-foundations/` |
| 教材参数学习、归一化、多头和在线softmax | `experiments/v03_networks.py` → `results/v03-networks/` |
| 一次注意力完整更新/残差漏梯度 | `run_all.py --experiment attention_walkthrough` / `--experiment residual_debug --seed 19` |
| 文本预测、后训练、推理预算 | `experiments/v03_language.py` → `results/v03-language/` |
| 完整标准因果Transformer与数据重复 | `experiments/standard_transformer_study.py` → `results/standard-transformer-v03/` |
| 公开模型评分、模板与完整生成 | `experiments/public_model_diagnostics.py` → `results/public-models-v03/` |
| 权限、误拒、多步错误、探针干预、评估器投机、稳定错误状态 | `experiments/v03_research.py` → `results/v03-research/` |
| 条件查表与相关伪参考 | `experiments/research_bridges.py` → `results/research-bridges-v03/` |
| 初版15次有限语法小研究 | `run_all.py --experiment micro_research` → `results/micro_research/` |

先确定每个张量的形状和共享关系，再读函数。数值表由 `scripts/write_v02_results.py` 和 `scripts/write_v03_results.py` 从已执行JSON生成；正文的数学推导不靠数值抽样当证明。所有长源代码仍是文本，论文图为授权图件或可编辑内容重绘，未用截图拼贴正文。
