# 中文论文研究资料

按问题读材料：DPO→R1→Snell→CaT讨论反馈与预算，Engram讨论容量与计算，CHIVE讨论机制证据，DGM→AlphaProof讨论研究闭环，STARS讨论循环计算的稳定性。每篇配版本、许可、逐节覆盖与核查记录。

## 指定版本全文译文

均为CC BY4.0机器辅助非官方译文；完整指指定版本本体及其中包含的附录，原英文书目保留，原图内标签附中文解释。未声称人工专家校订。

| 资料/版本 | PDF/源码 | 学习入口 |
|---|---|---|
| 直接偏好优化；2305.18290v3 · 2024-07-29 | [PDF（36页）](../dist/papers/dpo.pdf) · [LaTeX](translations/dpo/body.tex) · [覆盖](translations/dpo/coverage.json) | 教材7：KL最优策略→偏好似然→梯度 |
| 最优测试时计算；2408.03314v1 · 2024-08-06 | [PDF（43页）](../dist/papers/testcompute.pdf) · [LaTeX](translations/testcompute/body.tex) · [覆盖](translations/testcompute/coverage.json) | 教材8：验证器、难度与并行/顺序预算 |
| DeepSeek-R1 Nature 正式论文；Nature · 2025-09-17 | [PDF（18页）](../dist/papers/r1-nature.pdf) · [LaTeX](translations/r1-nature/body.tex) · [覆盖](translations/r1-nature/coverage.json) | 教材7–8：RLVR与实际证据；配原创R1说明 |
| 用反事实检验解释；2608.16747v1 · 2026-08-17 | [PDF（34页）](../dist/papers/chive.pdf) · [LaTeX](translations/chive/body.tex) · [覆盖](translations/chive/coverage.json) | 教材10：解释→反事实预测→干预证据 |
| 达尔文哥德尔机；2505.22954v3 · 2026-03-12 | [PDF（128页）](../dist/papers/dgm.pdf) · [LaTeX](translations/dgm/body.tex) · [覆盖](translations/dgm/coverage.json) | 教材11：代码更新、档案搜索、评估器投机 |
| 循环动力学稳定性；2605.26733v1 · 2026-05-26 | [PDF（19页）](../dist/papers/stars.pdf) · [LaTeX](translations/stars/body.tex) · [覆盖](translations/stars/coverage.json) | 教材11：稳定性、有效性与局部理论条件 |
| 奥林匹克形式数学推理；Nature VOR · 2026-03-13 | [PDF（39页）](../dist/papers/alphaproof.pdf) · [LaTeX](translations/alphaproof/body.tex) · [覆盖](translations/alphaproof/coverage.json) | 教材11：AND/OR搜索、形式核验与题意对应 |
| 条件记忆与稀疏查找；2601.07372v2 · 2026-07-12 | [PDF（34页）](../dist/papers/engram.pdf) · [LaTeX](translations/engram/body.tex) · [覆盖](translations/engram/coverage.json) | 教材11：查表梯度、容量/计算/存储分配 |
| 以计算作为教师；2509.14234v3 · 2026-05-09 | [PDF（31页）](../dist/papers/cat.pdf) · [LaTeX](translations/cat/body.tex) · [覆盖](translations/cat/coverage.json) | 教材8/11：伪参考、相关错误与监督闭环 |

R1 Nature的独立83页Supplementary与AlphaProof的独立9页Supplementary/伪代码ZIP未确认单独再分发许可，未镜像，未纳入“全文”完成范围；原文仍保留指向附件的引用。Nature许可不借给不同arXiv版本。

## 原创研究说明

- [指令层级研究说明](../dist/papers/study-ih-challenge.pdf) · [可编辑源码](studies/ih-challenge.tex)：原创问题、数学、实际CPU机制和练习；不是未许可原文的全文译本。
- [浏览器注入研究说明](../dist/papers/study-browser-injection.pdf) · [可编辑源码](studies/browser-injection.tex)：原创问题、数学、实际CPU机制和练习；不是未许可原文的全文译本。
- [R1 比较阅读说明](../dist/papers/study-r1-reading.pdf) · [可编辑源码](studies/r1-reading.tex)：原创问题、数学、实际CPU机制和练习；不是未许可原文的全文译本。

## 三项重点来源的定位

| 原始研究来源 | 教材 | 本项目资料/论文资料页码 |
|---|---|---|
| [OpenAI IH-Challenge官方说明](https://openai.com/index/instruction-hierarchy-challenge/)（2026-03-10）及v1论文 | 第9章，55–61页 | `studies/ih-challenge.tex`；研究说明PDF4页；论文资料1–4页 |
| [Anthropic浏览器注入防御](https://www.anthropic.com/research/prompt-injection-defenses)（2025-11-24） | 第9章，55–61页 | `studies/browser-injection.tex`；研究说明PDF4页；论文资料5–8页 |
| [R1 Nature正式论文](https://www.nature.com/articles/s41586-025-09422-z)（2025-09-17） | 第7–8章，44–54页 | `translations/r1-nature/body.tex`；正式译文18页；论文资料91–108页；另有原创R1说明9–11页 |

## 全部组件实际页码

| 组件 | 独立PDF页数 | 论文资料PDF | 合订本PDF |
|---|---:|---|---|
| 指令层级研究说明 | 4 | 1–4 | 100–103 |
| 浏览器注入研究说明 | 4 | 5–8 | 104–107 |
| R1 比较阅读说明 | 3 | 9–11 | 108–110 |
| 直接偏好优化 | 36 | 12–47 | 111–146 |
| 最优测试时计算 | 43 | 48–90 | 147–189 |
| DeepSeek-R1 Nature 正式论文 | 18 | 91–108 | 190–207 |
| 用反事实检验解释 | 34 | 109–142 | 208–241 |
| 达尔文哥德尔机 | 128 | 143–270 | 242–369 |
| 循环动力学稳定性 | 19 | 271–289 | 370–388 |
| 奥林匹克形式数学推理 | 39 | 290–328 | 389–427 |
| 条件记忆与稀疏查找 | 34 | 329–362 | 428–461 |
| 以计算作为教师 | 31 | 363–393 | 462–492 |

[合订资料PDF](../dist/ai-papers-zh.pdf) · [教材与资料完整合订PDF](../dist/ai-self-study-complete.pdf) · [机器可读页码](page-map.json) · [许可判定](LICENSE-DECISIONS.md)。源代码的相对输入以 `book/` 为工作目录，统一构建见[构建说明](../docs/build.md)。
