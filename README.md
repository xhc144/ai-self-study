# 现代人工智能研究学习

从语言模型的数学与训练出发，读懂近年的基础模型论文，完成可复核的小研究。教材以问题、推导、实验与失败案例连成学习路线；配套中文论文资料保留原文的公式、图表、附录和版本边界。

## 直接阅读与下载

- [中文教材 PDF](https://raw.githubusercontent.com/xhc144/ai-self-study/main/dist/ai-self-study.pdf)：11 个现代 AI 学习单元、3 个按需数学工具附录，例题、实验、习题及解答。
- [中文论文资料 PDF](https://raw.githubusercontent.com/xhc144/ai-self-study/main/dist/ai-papers-zh.pdf)：九篇指定许可版本的非官方全文译文，以及三份原创研究说明。
- [教材与论文合订 PDF](https://raw.githubusercontent.com/xhc144/ai-self-study/main/dist/ai-self-study-complete.pdf)。
- [完整可编辑源码 ZIP](https://raw.githubusercontent.com/xhc144/ai-self-study/main/dist/ai-self-study-source.zip)：LaTeX、论文图件及署名、实验代码、实际结果、研究记录、构建和测试脚本。字体与下载模型不捆绑。
- [逐篇阅读入口与页码](papers/README.md)、[路线及先修关系](docs/roadmap.md)、[公式—代码对应](docs/code-bridge.md)。

这些译文由机器辅助制作并经过独立 AI 对照审查，不是作者官方译本，也不声称完成了人工专家审校。原作者实验与本项目 CPU 实验分开标识。

## 按这条路线学

1. **问题与证据 → 文本预测**：条件概率、token 损失、生成、上下文学习；区分训练、提示和搜索。
2. **参数学习 → 注意力**：批量反向传播、归一化、残差、因果多头、位置、缓存与在线 softmax；从一次手算到完整小 Transformer。
3. **评价 → 数据与算力**：校准、污染、留出、数据去重和缩放；问比较是否匹配预算、指标是否忠实。
4. **后训练 → 推理预算**：SFT、奖励、DPO、可验证 RL、采样与验证器；结合 DPO、R1、Snell、CaT 译文。
5. **工具与信任 → 机制解释**：多步错误、RAG、指令层级、浏览器注入、探针、归因与反事实；结合原创安全研究说明和 CHIVE。
6. **可核验研究 → 新结构**：评估器投机、程序搜索、DGM、形式证明、条件记忆、循环潜在状态；结合 AlphaProof、Engram、STARS。

矩阵、概率和微分附录按公式需要回查。每一阶段都先重建一个推导，再运行实验，最后提出能被反例或留出结果推翻的小问题；不用先把传统 ML 算法目录全部学完。

## 真正运行实验

默认 NumPy 实验无 API、无模型下载，Python 3.12：

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python experiments/run_all.py --out /tmp/ai-basics
python experiments/v03_foundations.py --out /tmp/ai-foundations
python experiments/v03_networks.py --out /tmp/ai-networks
python experiments/v03_language.py --out /tmp/ai-language
python experiments/v03_research.py --out /tmp/ai-research
python experiments/research_bridges.py --out /tmp/ai-bridges
python -m unittest discover -s tests -v
```

结果与实际执行环境在 [results](results/)。所有数据是原创有限任务。输出目录用 `/tmp` 可保留仓库中的参考结果。基础套件还包含注意力逐步更新、残差漏梯度调试与 15 次小研究；[实验说明](docs/experiments.md)列出精确命令和证据范围。

另有两类可选的真实模型实验：完整 **18,026 参数标准因果 Transformer** 的六次 CPU 配对训练，以及两份固定版本 **SmolLM2-135M** 的 54 条 CPU 诊断记录。后者是 18 个记录位×3 条件，实际只有 12 个不同 `(system, user)` 输入、36 个不同输入—条件组合；冲突部分只有两种提示各出现三次。确定性贪心重复不增加独立样本或攻击覆盖，见[输入审计](research/public-model-input-audit-v03.json)。使用独立环境：

```bash
python -m venv .venv-models
. .venv-models/bin/activate
python -m pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install numpy==2.3.5 transformers==4.57.3
python experiments/standard_transformer_study.py --out /tmp/ai-standard
# 首次显式允许约 538 MB 权重下载；以后去掉 --allow-download 只读缓存。
python experiments/public_model_diagnostics.py --allow-download --cache /tmp/ai-hf-cache --out /tmp/ai-public
```

这些实验也保留失败：重复数据组的加权训练损失下降而留出损失上升；公开模型两选项评分全选 A，严格字母格式全部失败。前者没有匹配 FLOPs，后者不是能力榜单或 RLVR 复现。完整输出与冻结设计供读者检查，不用新提示替换不理想结果。

## 从读论文走向小研究

[研究问题](research/questions.md)提供可在现有代码上继续的入口；[研究记录](research/notebook.md)和[真实模型研究记录](research/model-study-v03.md)展示如何冻结问题、保存全部运行、解释失败和限制结论。建议先做来源角色交换、同预算数据重加权、错误验证器、相关伪参考或机制干预；先写判定标准，再看测试结果。

引用以官方课程、教材、论文与研究团队报告为主。[来源账本](docs/sources.json)记录读到哪里；[逐版本许可](papers/rights.json)决定全文翻译或原创解释，不以免费阅读、模型许可或代码许可代替论文许可。

## 构建、许可证与版本

[构建说明](docs/build.md)提供 XeLaTeX、所需字体和源码 ZIP 重编译流程；源码不用截图拼贴，不捆绑字体。正文采用固定王者数学版式，适配类的来源权利另记。

原创教学文本和数据用 CC BY 4.0，原创实验代码用 MIT。九篇译文及论文图件按逐篇 CC BY 4.0 署名，DGM 论文内代码属于其论文许可范围；外部软件、模型、数据和继承模板保留各自权利，详见 [LICENSE](LICENSE) 与[权利说明](docs/third-party.md)。

本版为 **0.3.1**，补充公开模型输入重复与后验计数披露、原作者版权行及现行源码哈希。旧版源码与 PDF 保留在 Git 历史及 `v0.2.1`、`v0.3.0` 标签；采用新增提交更新，保留原始版本。[独立审查与复现证据](qa/README.md)区分内容核对、编译、全页布局巡视与可读抽查。
