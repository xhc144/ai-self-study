> 历史审查范围：v0.1（33页）。v0.2新增内容与当前PDF另见 `v02-math-review.md`、`v02-pdf-review.md`。

# PDF 与源码包独立交付审查

结论：**最终 33 页 PDF 的视觉与链接结构检查通过。** 已独立完成初归档快照的干净重编译、7 项代码测试和全部 7 个实验重跑。最终归档在本报告定稿之后生成，其再次核验记录放在外部交付记录，避免让 ZIP 哈希自引用。

审查日期：2026-10-11 UTC。审查者是独立 AI agent；这不是人类同行评审，不是全书数学结论的形式化验证，也不等于所有软件/浏览器环境都已测试。

## 最终文件与视觉覆盖

最终 PDF：`dist/ai-self-study.pdf`，33 页，SHA256 `e7d26f256140c767e7e02982dfa71ab8406a7a0c918f02a56d21a1c319ff0a15`。源码入口 `book/main.tex`，包含 13 章与参考文献。

通过 `view_image` 实际打开最初 32 页的全部双页组合，并放大密集页面；正文终审后的 33 页版本也实际打开全部 16 张双页组合与单页 33。对最后的分页修订，另以 PyMuPDF 的 96 dpi 像素哈希比较前后快照，发现页 2、3、9–26 共 20 页有变化，已再实际查看覆盖这些页的所有双页组合，放大页 15 的 LayerNorm 公式。其余 13 页的像素完全一致，保留前次实际视觉观察。**没有用自动 PASS 代替逐页视觉检查。**

所用规范：用户的 `math-latex-typesetting` 固定模板负责项目版式，`latex-pdf-editorial` 提供逐页渲染与交付核验要求。本审查未修改正文、PDF、锁定模板或 Git 提交，只写本报告。未访问或修改 MIT 工作区。

观察结果：中文、数学、页眉、页码、定义/命题/例题/习题编号均清楚；未见缺字方块、裁切、长公式溢出、页眉碰撞、QED 悬空或重叠。三个原创图的坐标、图例和图题可读，标题与图保持完整。部分习题与解答按正常正文分页分在相邻页，内容和编号连续。第 26 页在章节边界有留白，目录最后一页也有余白，均有明确结构原因；没有空白页或仅剩一条参考文献的末页。

## 最终逐页记录

| 页码 | 实际观察 |
| --- | --- |
| 1 | 标题、前言与目录起始清楚，无页眉线碰撞。 |
| 2 | 目录分页连续，点线和页码对齐，已更新章节页码。 |
| 3 | 目录收尾完整，剩余留白符合结构。 |
| 4 | 路线、定义与自测正文正常。 |
| 5 | 两道习题与解答 QED 正常，第 2 章与首节正文相接。 |
| 6 | 正规方程、正定条件、命题和算例正常。 |
| 7 | 特征分解、条件数、岭惩罚与习题正常。 |
| 8 | 概率、似然、熵/KL 推导与 QED 正常。 |
| 9 | Softmax 公式、例题与习题正常；已消除页末孤立的第 4 章标题。 |
| 10 | 第 4 章标题与首节同页，Jacobian 与二次目标公式清楚。 |
| 11 | 下降估计、Adam 和有限差分公式未裁切；习题顺序正常。 |
| 12 | 解答与第 5 章衔接正常，风险界证明与分解公式清楚。 |
| 13 | 快捷特征与评估习题正常；无孤立第 6 章标题。 |
| 14 | 第 6 章与首节同页，反传梯度上下标清楚，例题 QED 正常。 |
| 15 | LayerNorm 短公式完整保留在同一行，原创 XOR 损失图及图题可读。 |
| 16 | 第 7 章标题与首节正文同页，注意力定义与例题正常。 |
| 17 | 因果位置说明与完整注意力反向传播未裁切，矩阵式清楚。 |
| 18 | 注意力习题与第 8 章衔接正常，序列概率与训练目标清楚。 |
| 19 | 原创小语言模型曲线坐标/图例清楚，图题完整。 |
| 20 | KV 缓存、LoRA 与 DPO 正文清楚；DPO 损失与 s_theta 定义已保持整组同页。 |
| 21 | DPO 实验说明和练习连续，第 9 章与首节同页。 |
| 22 | 规模预算推导、涌现与练习正常。 |
| 23 | 前章解答与第 10 章衔接清楚，采样与验证公式正常。 |
| 24 | 策略梯度、R1 范围和推理练习正常。 |
| 25 | 第 11 章与首节正文同页，安全定义、授权命题与 QED 正常。 |
| 26 | 玩具注入范围、研究说明和习题清楚；章节边界留白有理由。 |
| 27 | 第 12 章与首节同页，积分归因推导清楚。 |
| 28 | 原创 IID/shifted 柱图、图题、稀疏特征与练习正常。 |
| 29 | 前章解答与第 13 章衔接正常，研究与自改进区分清楚。 |
| 30 | 状态空间、扩散与潜空间循环公式未裁切。 |
| 31 | 独立研究段落和练习正常，已消除跨页“子.”单字残行。 |
| 32 | 参考文献 1–16 连续，长 URL 换行无裁切。 |
| 33 | 参考文献 17–32 完整，最后条目文字与页码没有碰撞。 |

在第 33 页，最后条目文字下缘为 y=745.02 pt，页码上缘为 y=757.22 pt，净距约 12.20 pt；最后一条已实际放大检查，局部 `enlargethispage` 没有造成重叠。

曾要求作者修复并已复查通过的项目：DPO 一组公式分页，第 12 章孤立章标题，第 13.5 段落页顶单字；正文增补后的第 4/7 章孤立标题，以及 LayerNorm 短公式跨页。没有以删内容、改小字号或修改锁定模板来掩盖问题。

## 最终 PDF 链接与字体

使用 PyMuPDF 1.26.6 的 `resolve_names()`、`Page.get_links()`、`get_toc()` 核验最终 PDF：

- 191 个 named destination：13 chapter、57 section、32 cite、33 page、20 theorem、27 exercise、4 example、3 figure、Doc-Start 与 bibliography 的 section*；全部目标页有效。
- 105 个内部链接注释，103 个不同目标。所有目标名称存在且解析正确，注释区域均位于源页面内。
- 71 条目录书签：去除编号/空白后，全部标题在其目标页的文字层找到。
- 47 个外链注释合并为 32 个 unique HTTPS URI。跨行 URL 产生多个注释属于正常现象，URI 无嵌入空白；最终 URL 集与以下实际 HTTP 检查相同。
- `pdffonts` 检查 21 个字体对象均为 `emb=yes`，包括图中 Type3 的字形。PyMuPDF 中文与公式文字层能够提取。未因此宣称 PDF 已通过完整无障碍认证。

这是 PDF 结构与标题/目标页核验，没有声称在 GUI 阅读器中逐个点击了全部链接。

## 外站可达性实际范围

2026-10-11 16:40 UTC 左右，从本环境对全部 32 个 unique URI 分别执行一次允许重定向的 HTTP GET（每站最多读取 64 KiB）。全部返回 200。HTML 提取 `<title>` 检查来源身份；CS229 PDF 检查 Content-Type 与 `%PDF-` 文件头。Nature 两站重定向后含 `error=cookies_not_supported` 参数，但取得匹配论文标题的 HTML。此检查证明当时的 HTTP 可达性，不保证以后可达、所有浏览器表现相同、全文免费阅读或引用主张均正确；没有重新评审各论文全文。

| URL / 取得的页面标题 | 实测状态 |
| --- | --- |
| [[1412.6980] Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) | 200 |
| [[1706.03762] Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 200 |
| [[2001.08361] Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) | 200 |
| [[2005.11401] Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | 200 |
| [[2106.09685] LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) | 200 |
| [[2201.11903] Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) | 200 |
| [[2203.02155] Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) | 200 |
| [[2203.15556] Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) | 200 |
| [[2205.14135] FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) | 200 |
| [[2302.12173] Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) | 200 |
| [[2304.15004] Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) | 200 |
| [[2305.18290] Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) | 200 |
| [[2312.00752] Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) | 200 |
| [[2408.03314] Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314) | 200 |
| [[2501.12948] DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) | 200 |
| [[2502.05171] Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](https://arxiv.org/abs/2502.05171) | 200 |
| [[2502.09992] Large Language Diffusion Models](https://arxiv.org/abs/2502.09992) | 200 |
| [[2505.22954] Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954) | 200 |
| [[2506.13131] AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) | 200 |
| [[2603.10521] IH-Challenge: A Training Dataset to Improve Instruction Hierarchy on Frontier LLMs](https://arxiv.org/abs/2603.10521) | 200 |
| [[2605.26733] Stabilizing Recurrent Dynamics for Test-Time Scalable Latent Reasoning in Looped Language Models](https://arxiv.org/abs/2605.26733) | 200 |
| [[2608.16747] Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments](https://arxiv.org/abs/2608.16747) | 200 |
| [Stanford CS336 | Language Modeling from Scratch](https://cs336.stanford.edu/) | 200 |
| [Dive into Deep Learning — Dive into Deep Learning 1.0.3 documentation](https://d2l.ai/) | 200 |
| [Mathematics for Machine Learning | Companion webpage to the book “Mathematics for Machine Learning”. Copyright 2020 by Marc Peter Deisenroth, A. Aldo Faisal, and Cheng Soon Ong. Published by Cambridge University Press.](https://mml-book.github.io/) | 200 |
| [CS229 PDF; Content-Type application/pdf; 文件头 %PDF-](https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf) | 200 |
| [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) | 200 |
| [Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html) | 200 |
| [Convex Optimization – Boyd and Vandenberghe](https://web.stanford.edu/~boyd/cvxbook/) | 200 |
| [Deep Learning](https://www.deeplearningbook.org/) | 200 |
| [Highly accurate protein structure prediction with AlphaFold | Nature](https://www.nature.com/articles/s41586-021-03819-2) | 200; Nature重定向带cookies_not_supported, 标题正确 |
| [Mathematical discoveries from program search with large language models | Nature](https://www.nature.com/articles/s41586-023-06924-6) | 200; Nature重定向带cookies_not_supported, 标题正确 |

## 已执行的源码 ZIP 测试

初归档快照 SHA256：`bd0f96804294ddd44ebe2da9513cd3569ba663453c9afd9962986a84439d4fca`，51 个归档成员，manifest 记录 50 个文件。没有路径穿越、符号链接、字体文件或 `.git` 文件；源码 manifest 核对无误。

独立脚本在 `/tmp/ai-self-study-zip-review-fw9kqdvg/ai-self-study` 新目录解压，归档本身不含 `book/build` 缓存。先删除归档带来的交付 PDF，再调用 `bash scripts/build_pdf.sh`，实际进行三遍 XeLaTeX（`-no-shell-escape`），退出码 0。重建 33 页；文字、全部书签、named destination、链接注释与所有页的 96 dpi 像素均与该归档所对应的交付快照逐项一致。两份 PDF 二进制 SHA 不同，原因范围包含生成日期/文档 ID；本检查未把内容一致伪报成二进制一致。日志无 Missing character、Overfull、Underfull、undefined citation/reference 或 Fatal 问题。

同一解压目录实际运行：

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/run_all.py --out /tmp/ai-self-study-zip-review-fw9kqdvg/rerun
```

7 项测试通过。7 个实验（ridge、mlp、language_model、spurious、search_verifier、injection、preference）全部重跑；`metrics.json` 与归档参考结果逐字节相同，SHA256 `7423b006e93853409e08793b246db281cf1df3df2f3dd7346a1779798d07dafe`。实际训练包括 MLP 的 4,000 步与 2,538 参数因果注意力模型的 1,400 步。独立运行的 MLP 最终损失 0.0024318；语言模型训练 NLL 0.255985、留出组合 NLL 1.506582、两组合叫声准确率 1.0。没有把有限玩具语法成绩推广成自然语言泛化证据；注入与搜索演示没有 LLM。这些结果仅在相同 Python/NumPy、种子、单线程 CPU 与 TeX/字体环境中核验，不保证跨平台逐位一致。

测试所用 TeX 环境：`TEXMFHOME=/workspace/.local/texmf`、`OSFONTDIR=/workspace/.local/texmf/fonts/opentype`、`XDG_CACHE_HOME=/tmp/ai-cache`。这些是构建依赖位置，字体不在归档内。

## 最终归档记录的边界

上述初归档测试后只作分页修订，正文/实验数据与代码内容没有新增。最终 PDF 的视觉与链接结论绑定前文 `e7d26f…` 哈希。为了把本报告也放进完整 ZIP，最终打包发生在报告定稿之后；最终 ZIP 将再次在新目录核验 manifest、从源码重编译、运行测试与实验。最终 ZIP 的精确哈希和实际测试结果保留在外部交付记录中，不倒填尚未执行的结果，也不将 ZIP 哈希写回其自身成员制造循环。
