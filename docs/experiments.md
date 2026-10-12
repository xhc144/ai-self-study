# 实验与证据范围

所有已公布数值来自实际执行，环境文件记录 Python、依赖、种子及适用的代码/设计/结果哈希。运行时请把 `--out` 指向新目录；不需要改公开参考结果。

| 入口 | 实际检验对象 | 可支持的结论及限制 |
|---|---|---|
| `run_all.py` | 七个基础实验；`--experiment attention_walkthrough`、`residual_debug --seed 19`、`micro_research` | 手算/梯度/注意力、有限语法和15次小研究；不是大模型复现 |
| `v03_foundations.py` | SVD/条件数、概率评分、梯度与优化 | 特定数学机制和数值条件 |
| `v03_networks.py` | LN、多头因果梯度、在线softmax、校准/选择 | 梯度与掩码契约，合成分布评价 |
| `v03_language.py` | ICL Bayes、采样、KV、LoRA、奖励与验证器 | 受指定分布和有限支持限制的机制 |
| `v03_research.py` | 权限/误拒、多步错误、探针干预、程序选择、循环 | 符号执行器与已知函数，不含 LLM |
| `research_bridges.py` | 稀疏查表共享梯度、相关伪参考 | 原创数值机制，不是 Engram/CaT 性能复现 |
| `standard_transformer_study.py` | 2层pre-norm/GELU/2头，3种子×2频率条件 | 实际训练18,026参数；6 vs36行每步不等FLOPs，留出只有2句 |
| `public_model_diagnostics.py` | 两份固定135M权重，18记录位×3条件 | 54条输出，实际12不同输入/36不同输入—条件组合；映射4不同、冲突2不同，确定性重复不独立；非训练/榜单 |

所有脚本支持 `--help`。四个 `v03_*.py`、`research_bridges.py` 默认种子 144。标准 Transformer 的 JSON 设计固定 144/145/146 三种子；公开模型诊断固定 144，贪心生成最多12 token。标准模型及公开诊断的设计文件在运行之前冻结，不能看测试结果后替换。

`python -m unittest discover -s tests -v` 共58项。纯 NumPy 环境会跳过2项 Torch 架构检查和2项构建依赖的PDF链接检查；安装可选 CPU 与构建依赖后58项全部实际通过。可选测试不下载模型。测试覆盖梯度、共享依赖、因果前向及未来梯度、奖励/评分与留出契约，不能代替论文数学或阅读审查。

本版公开诊断的第二次缓存运行与首次指标文件逐字节相同。冻结设计及原指标不覆盖；[输入审计](../research/public-model-input-audit-v03.json)补充重复分组与唯一输入计数，运行 `python scripts/audit_public_model_inputs.py --out /tmp/public-model-input-audit.json` 可从保存的设计/结果重新核查，不运行模型。按记录位常选A为10/18，按不同输入各计一次为6/12；后者只是原结果的后验重计数，不是预注册指标。受限 A/B 概率只在两条指定续写中归一化，不能叫校准置信度；严格生成正确率为零与知识完全缺失是两种判断。六次标准训练保留全部原始结果和自产 NumPy 参数快照，不挑种子、不删失败。

下载权重需显式 `--allow-download`，总约538 MB，缓存默认 `/tmp/ai-hf-cache`。模型许可 Apache 2.0，权重保持仓库外；代码禁止 `trust_remote_code`，只用safetensors。没有收费API、GPU购买或巨型模型下载。
