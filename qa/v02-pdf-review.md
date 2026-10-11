# v0.2 PDF 独立交付审查

结论：**最终 41 页 PDF 的视觉、导航结构与当前源码干净重编译检查通过。** 最终 ZIP 在本报告定稿后生成，其归档核验另存交付收据，避免归档哈希自引用。此处没有提前宣称尚未完成的 ZIP、13 项测试或 10 个实验入口核验已通过。

日期：2026-10-11 UTC。审查者为未编写正文与实验的独立 AI agent；不是人类同行评审，也不是全书数学结论的形式化验证。本次只写本报告，未修改正文、PDF、用户 Skill、权限或 MIT 工作区。

## 绑定文件与实际视觉覆盖

PDF：`dist/ai-self-study.pdf`，41 页，SHA-256 `53795a888ab79e1160c8ed08c7fd0820c892c1497692fc54fc596908fffea690`。源码入口为 `book/main.tex`，13 章与 33 条参考文献。

依用户 `math-latex-typesetting` 固定模板和 `latex-pdf-editorial` 的逐页交付检查要求执行。先从初版 42 页 PDF 独立渲染 120 dpi，实际以 `view_image` 打开全部 21 张双页图，并放大密集页。返修 41 页版本再渲染全部页面，实际打开全部 20 张双页图和单页 41。最后图浮动/数值格式修订后，再渲染冻结版全部 41 页并逐页比较像素；只有页 23、31、32 有变化，这三页已重新实际放大查看，其余 38 页像素与刚实际看过的 41 页版本完全相同。**没有用自动 PASS 代替实际视觉检查。**

中文、公式上下标、矩阵、表格、代码块、页眉、页码、章/节与语义环境编号可读，未见缺字、裁切、溢出、页眉重叠或 QED 悬空。三个原创图的坐标、图例和图题完整。长正文、推导与部分习题/答案按正常内容分页续接；各章标题与首节正文相接。第 12 页章节边界余白与末页文献余白有结构原因；没有空白页或只含末两条目录的额外页。

## 最终逐页记录

| 页码 | 实际观察 |
| --- | --- |
| 1 | 标题、前言与目录起始正常；中文清楚。 |
| 2 | 目录第 4–8 章页码和点线对齐。 |
| 3 | 目录第 9–13 章与参考文献完整收尾，13.8 编号有间隔；已消除第四张稀疏目录页。 |
| 4 | 第 1 章标题、依赖路线与定义正常。 |
| 5 | 证据定义、两道习题/解答与第 2 章首节连续，QED 正常。 |
| 6 | 内积、正规方程、正定命题与例题清楚。 |
| 7 | 特征分解、条件数、岭惩罚与习题正常。 |
| 8 | 第 3 章与概率/似然/KL 证明正常。 |
| 9 | 交叉熵段落保留两行连续收尾；softmax 公式与练习正常。 |
| 10 | 第 4 章与 Frobenius 内积、矩阵微分三行展开清楚。 |
| 11 | 偏置求和、例题与步长证明正常；随机梯度首段完整。 |
| 12 | Adam 动量说明与四行更新式整组同页；有限差分与练习清楚。 |
| 13 | 第 5 章与经验风险段落连续，风险界证明、偏差分解正常。 |
| 14 | 快捷特征、评估习题和第 6 章首节衔接正常。 |
| 15 | 单样本梯度、批次轴与零起编号清楚。 |
| 16 | 共享权重、重复索引累加例题与代码块可读；代码包含 NumPy 导入。 |
| 17 | LayerNorm 行内公式完整，原创 XOR 曲线/图例/图题及两道习题正常。 |
| 18 | 第 7 章标题与注意力定义、因果位置、多头说明清楚。 |
| 19 | 完整注意力反传及两位置算例矩阵可读；页末梯度式未拆开。 |
| 20 | 算例实际更新与科学计数法清楚；批量实现代码块未裁切。 |
| 21 | 公式—形状—代码表整张完整；残差漏项与误差、因果检查正常。 |
| 22 | 注意力练习、QED 与第 8 章首节连续；序列目标正常。 |
| 23 | 小模型训练结果正文先完整结束，再放原创 NLL 曲线；已消除图 8.1 隔开“叫声位置准确率”的断句。 |
| 24 | KV 缓存、LoRA 与偏好正则化数学清楚。 |
| 25 | DPO 损失与分数定义整组同页；练习、第 9 章与首节连续。 |
| 26 | 规模预算推导与涌现说明正常。 |
| 27 | 第 9 章练习与第 10 章衔接正常，采样/验证定义清楚。 |
| 28 | 策略梯度、研究范围与习题正常；后一习题解答延至下页有正常编号承接。 |
| 29 | 解答、第 11 章首节、授权命题与 QED 正常。 |
| 30 | 玩具注入边界、安全研究与练习清楚。 |
| 31 | 第 12 章、积分归因等式及干预正文正常。 |
| 32 | 原创 IID/shifted 柱图与图题可读；研究计划段落保持连续，已消除图 12.1 插入句尾。 |
| 33 | 前章解答与第 13 章衔接正常，研究与自改进区分清楚。 |
| 34 | 状态空间、扩散与收缩推导未裁切。 |
| 35 | 冻结划分表完整，干预与原始答案概率差式清楚。 |
| 36 | 三张研究结果/逐种子/逐位置表均完整可读，无列碰撞；误差说明连续。 |
| 37 | 二项模型、两种尾反演与严格导数式清楚，区间解释未裁切。 |
| 38 | 统计段落连续、四组 CLI 命令与探索标记可读，练习首题正常。 |
| 39 | 练习与 QED 正常，参考文献 1–7 连续。 |
| 40 | 参考文献 8–22 完整，长 URL 换行无裁切。 |
| 41 | 参考文献 23–33 完整，最后 NIST 链接及页码清楚，无孤立末条。 |

曾要求修复并已核对：稀疏第四张目录页与 13.10 编号贴字；Adam 更新式跨页；交叉熵与风险段落残尾；图 8.1/12.1 隔断正文。作者以内容段落/分页调整处理，未改锁定模板。密集页的页脚间隔另以文字包围盒核验：目录页 3 为 26.57 pt，研究页 37 为 23.08 pt，文献页 39 为 19.71 pt；视觉均无碰撞。

## 目录、超链接与字体

- PyMuPDF 1.26.6 检查全部 210 个 named destination：13 chapter、63 section、33 cite、41 page、20 theorem、30 exercise、5 example、3 figure，加 Doc-Start 与 bibliography 的 section*；所有目标页有效。
- 114 个内部链接注释、110 个不同目标全部解析正确；注释源区域在页面内，链接目标页与 named destination 一致。
- 77 条目录书签去除编号/空白后，全部标题在目标页文字层找到；没有旧版页码残留。
- 49 个外链注释合为 33 个 unique HTTPS URI；跨行链接产生多个注释属正常现象，URI 无嵌入空白，最终 URL 集与实测 HTTP 集完全一致。
- `pdffonts` 的 21 个字体对象全部嵌入。中文文字层能够提取，无 U+FFFD 替代字符；40 个 QED 方框与 5 个 proof、35 个 solution 对应。没有据此宣称完整无障碍认证。

上述为 PDF 导航结构核验，未声称在 GUI 阅读器中逐个点击所有链接。

## 外站可达性边界

2026-10-11 17:26–17:27 UTC，从本环境对全部 33 个 unique URI 各实际执行一次允许重定向的 HTTP GET，超时 15 秒、最多读取 64 KiB，均返回 200。HTML 的来源/论文标题匹配；CS229 的 Content-Type 为 PDF，文件头为 `%PDF-`。Nature 的重定向含 `error=cookies_not_supported` 参数，取得的标题与论文匹配。此结果仅说明当时 HTTP 可达及页面身份，不保证以后可达、全文免费、浏览器表现一致或论文主张已获独立验证。

| 官方目标 / 当次页面标题 | HTTP |
| --- | --- |
| [\[1412.6980\] Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) | 200 |
| [\[1706.03762\] Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 200 |
| [\[2001.08361\] Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) | 200 |
| [\[2005.11401\] Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | 200 |
| [\[2106.09685\] LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) | 200 |
| [\[2201.11903\] Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) | 200 |
| [\[2203.02155\] Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) | 200 |
| [\[2203.15556\] Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) | 200 |
| [\[2205.14135\] FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) | 200 |
| [\[2302.12173\] Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) | 200 |
| [\[2304.15004\] Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) | 200 |
| [\[2305.18290\] Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) | 200 |
| [\[2312.00752\] Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) | 200 |
| [\[2408.03314\] Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314) | 200 |
| [\[2501.12948\] DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) | 200 |
| [\[2502.05171\] Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](https://arxiv.org/abs/2502.05171) | 200 |
| [\[2502.09992\] Large Language Diffusion Models](https://arxiv.org/abs/2502.09992) | 200 |
| [\[2505.22954\] Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954) | 200 |
| [\[2506.13131\] AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) | 200 |
| [\[2603.10521\] IH-Challenge: A Training Dataset to Improve Instruction Hierarchy on Frontier LLMs](https://arxiv.org/abs/2603.10521) | 200 |
| [\[2605.26733\] Stabilizing Recurrent Dynamics for Test-Time Scalable Latent Reasoning in Looped Language Models](https://arxiv.org/abs/2605.26733) | 200 |
| [\[2608.16747\] Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments](https://arxiv.org/abs/2608.16747) | 200 |
| [Stanford CS336 \| Language Modeling from Scratch](https://cs336.stanford.edu/) | 200 |
| [Dive into Deep Learning — Dive into Deep Learning 1.0.3 documentation](https://d2l.ai/) | 200 |
| [Mathematics for Machine Learning \| Companion webpage to the book “Mathematics for Machine Learning”. Copyright 2020 by Marc Peter Deisenroth, A. Aldo Faisal, and Cheng Soon Ong. Published by Cambridge University Press.](https://mml-book.github.io/) | 200 |
| [CS229 讲义 PDF（application/pdf；%PDF- 文件头）](https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf) | 200 |
| [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) | 200 |
| [Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html) | 200 |
| [Convex Optimization – Boyd and Vandenberghe](https://web.stanford.edu/~boyd/cvxbook/) | 200 |
| [Deep Learning](https://www.deeplearningbook.org/) | 200 |
| [7.2.4.1. Confidence intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) | 200 |
| [Highly accurate protein structure prediction with AlphaFold \| Nature](https://www.nature.com/articles/s41586-021-03819-2) | 200 |
| [Mathematical discoveries from program search with large language models \| Nature](https://www.nature.com/articles/s41586-023-06924-6) | 200 |

## 当前源码独立重编译

将当前 `book/` 内 TeX 与原创图、`scripts/build_pdf.sh` 复制到新的 `/tmp/ai-v02-source-snapshot-z5qb8vtr/`；没有复制旧 `book/build` 或交付 PDF 作为构建输入。从空目录实际运行三次 XeLaTeX，使用 `-no-shell-escape`，4.49 秒完成。最终日志无 Missing character、Overfull、Underfull、undefined 或 Fatal 项。

逐页核对重编译 PDF 与冻结交付 PDF：41 页的文字、目录书签、named destinations、全部链接注释及 96 dpi 渲染像素均完全一致；像素差异页为空。PDF 二进制日期/标识元数据可能不同，本检查不宣称二进制 SHA 相同。源码快照在复制前后均核对哈希，避免编译到混合版本。

环境：Python 3.12.14、PyMuPDF 1.26.6；XeLaTeX 与本环境已安装字体，`TEXMFHOME=/workspace/.local/texmf`、`OSFONTDIR=/workspace/.local/texmf/fonts/opentype`、`XDG_CACHE_HOME=/tmp/ai-cache`。独立命令使用 `PYTHONDONTWRITEBYTECODE=1`。这是同一 TeX/字体环境的清缓存测试，尚不代表另一操作系统或未安装字体的机器已验证。

## 归档后续核验

本报告冻结后才生成最终 v0.2 ZIP；随后将在另一个干净目录核验完整 manifest、重编译、13 项测试、原 7 项实验与新增注意力/残差/15 次微研究。残差须按公开参考命令使用种子 19，微研究使用冻结设计默认五种子与三划分。最终 ZIP 哈希和实际结果另存归档外收据，不回写本报告形成自引用。
