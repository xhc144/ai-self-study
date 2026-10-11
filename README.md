# 人工智能自学与研究入门

一份从数学基础走向可检验研究问题的中文自学教材。v0.2 共41页、13章、30道习题及解答，包含基础推导、手算例子、每章习题与答案、10 个已实际运行的 CPU 实验入口，以及区分证据与猜想的前沿导论。新增矩阵梯度—张量—代码的桥接、两位置注意力完整更新、残差故障诊断和三划分×五种子的微研究。

**开始阅读：[教材 PDF](dist/ai-self-study.pdf) · [完整源码 ZIP](dist/ai-self-study-source.zip) · [依赖路线](docs/roadmap.md) · [33 项论文与教材索引](docs/papers.md)**

[内容范围与章节页数](docs/scope.md) 列明可复算推导、所调用的先修工具、简化模型的实现范围及尚属导读的前沿内容。

先修是高中代数、单变量导数和基本 Python。多变量微分、概率、信息论和矩阵计算按后文需要引入；积分基本定理、谱定理与欧氏空间完备性明确作为工具调用。它是一份有内容的研究入门首版，完整强化学习理论、分布式训练和前沿大模型复现仍需后续课程。

## 学习路线

|阶段|章节|完成后应能做到|
|---|---|---|
|数学基础|1 路线与研究问题；2 向量与最小二乘；3 概率与预测损失；4 微分与优化|自己推导正规方程、交叉熵梯度、链式法则与步长条件|
|机器学习与网络|5 统计学习与评估；6 神经网络与反传；7 注意力与 Transformer|正确划分数据、实现反传、检查张量维度和因果掩码|
|语言模型与推理|8 训练、推理、LoRA 与 DPO；9 进步与资源；10 推理与验证|区分训练与推理预算，理解采样、KV缓存、偏好优化和验证器|
|走向研究|11 安全与提示词注入；12 可解释性；13 AI辅助研究与新范式|提出有基线、干预、评价和失败判据的小研究问题|

每节建议：先复算，再运行实验，写出改变量后的预测，最后比较实际结果。练习答案紧随题目，第一次尝试时遮住答案。

## 运行实验

Python 3.11+，只有 NumPy 是实验依赖；无需收费 API、GPU、模型下载或外部数据。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/run_all.py
python -m unittest discover -s tests -v
```

结果写入 `results/metrics.json`，环境、线程、种子、时间和源码哈希写入 `results/environment.json`。若希望保留首版参考结果，用 `--out /tmp/my-ai-results` 指定另一目录。

|实验|学习问题|
|---|---|
|ridge|相关特征、条件数、正则化、SVD参考与梯度下降|
|mlp|XOR非线性表示、手写反传与有限差分|
|language_model|2,538参数因果注意力、完整组合划分、训练推理与泄漏检查|
|spurious|同分布高分与快捷特征偏移失败|
|search_verifier|候选覆盖、精确验证、预算和pass@N边界|
|injection|合成资料如何越过信任边界，执行器怎样限制动作|
|preference|八动作DPO、带噪偏好、真实奖励与KL解析最优策略|
|attention_walkthrough|T=2、D=1因果注意力，前向→标量损失→完整反向→一次更新|
|residual_debug|故意漏掉恒等残差梯度，206坐标差分定位E/P|
|micro_research|三组预冻组合划分×五初始化、两个基线、逐文档干预与不确定性|

`all` 保留原七项实验；新增入口按名称选择。保留参考结果时指定独立输出目录：

```bash
python experiments/run_all.py --experiment attention_walkthrough --out /tmp/my-attention
python experiments/run_all.py --experiment residual_debug --seed 19 --out /tmp/my-residual
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/run_all.py --experiment micro_research --out /tmp/my-study
python experiments/run_all.py --experiment language_model --seed 145 --steps 200 --lr .01 --width 8 --out /tmp/my-lm
```

单实验支持其适用的 `--seed --steps --lr --width`，微研究支持 `--design --seeds` 并标记探索性覆盖。v0.2.1 修复了显式 `--design` 的记录：即使没有其他命令行覆盖，也会在 `exploratory_overrides.design` 中保存设计的绝对路径与文件 SHA-256；显式指定冻结设计文件也保留这一探索标记。参数、环境和代码哈希自动记录。教材 PDF 仍为 v0.2。详见 [公式—变量—形状—代码](docs/code-bridge.md) 与 [实验报告](docs/experiments.md)。

[首个已完成微研究](research/micro-study-v02.md) 报告全部15次训练：叫声全对，但完整测试NLL仍高；每个固定划分的5/5整次成功只给出条件性95%区间[0.4782,1]。干预全部回到训练组合，三个划分重叠；没有把文档/token当IID或用bootstrap缩小误差。原单种子语言模型实验仍单列。候选搜索与玩具注入路由器不能当成大模型能力或安全评测。

## 编译与复现

源码是可编辑 LaTeX，不是页面截图。需要 XeLaTeX、ctex、Fandol 与 Computer Modern Unicode 字体及常见 LaTeX 宏包。项目不捆绑字体。

```bash
# 仅重编译教材；已包含来自实际结果的图和数值片段
bash scripts/build_pdf.sh

# 重新生成原创实验图，再编译
python -m pip install -r requirements-build.txt
python scripts/plot_results.py
bash scripts/build_pdf.sh

# PDF结构、目录、超链接、逐页渲染与来源/文件哈希
python scripts/audit_delivery.py
```

系统安装示例和干净目录重编译方法见 [构建说明](docs/build.md)。机械检查、独立 AI 读者审查和实际视觉检查分别记录在 `qa/`；它们不代表人类同行评审或全书无误证明。

## 研究专题

- [研究起点](research/questions.md)：主语检索与近邻捷径、可解码表征与因果使用。
- [证据笔记](research/notebook.md)：优化和泛化的分离、DPO奖励与KL权衡、验证器与权限边界。
- 前沿配读：规模规律与Chinchilla；R1与可验证奖励；2026 IH-Challenge；2025局部电路与2026 CHIVE负结果；FunSearch、AlphaEvolve与系统级自改进；Mamba、扩散语言模型、2026循环动力学。

[扩大语法与表征研究方案](research/questions.md) 仍未执行并明确标为方案。论文只提供官方链接和原创中文解释，不镜像全文、课程整章、数据集或第三方图。

## 许可

原创教材、研究笔记和实验图采用 **CC BY 4.0**；原创 Python、Shell 与测试代码采用 **MIT**。排版适配模板单列来源与适用范围，第三方论文、教材、字体和软件的许可保留各自权利。详见 [LICENSE](LICENSE) 与 [来源说明](docs/third-party.md)。
