# AlphaProof 正式译本的来源、许可与范围

原作：Thomas Hubert、Rishi Mehta、Laurent Sartran 等 39 位作者，Google DeepMind，**Olympiad-level formal mathematical reasoning with reinforcement learning**，Nature 651, 607–613 (2026)，DOI `10.1038/s41586-025-09833-y`。

## 固定版本

本译本固定 Version of Record **2026-03-13**。首次在线发表为 **2025-11-12**，期次日期 **2026-03-19**，投稿 **2025-06-03**，接受 **2025-10-30**。这些日期来自实际读取的官方文章 About this article，而不是凭 DOI 年份推测。

- [官方 HTML](https://www.nature.com/articles/s41586-025-09833-y)，实际读取全部科学内容、Methods、Extended Data、元信息与 Rights and permissions。下载文件 `/tmp/alphaproof-translation-source/article.html`。
- [官方正式 PDF](https://www.nature.com/articles/s41586-025-09833-y.pdf)，实际下载文件 `/tmp/alphaproof-translation-source/official.pdf`，25 页，6,644,928 字节。SHA-256：`ef6ea043c1acd4712c43369a294f6c8581d47c8f3dc2c660f69f5dd2a7c96f30`。
- 官方三个表页面 `/tables/1`、`/tables/2`、`/tables/3`。主表读取实际 HTML；扩展表是图片，实际查看正式 PDF 第 24、25 页后逐格转录。元数据保留原表数据及源图支持文件。

读取范围：正式科学文章本体全部部分。引用文献的 80 条书目信息按原文保留并提供题名中译；没有声称逐篇通读或核验这 80 篇被引论文。

## 授权与逐图 credit

官方 HTML Rights and permissions 及正式 PDF 第 7 页明确给出 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。许可允许在署名、链接许可并说明修改的条件下翻译、改编和再分发。文章明确：图像和第三方材料纳入文章许可，除非 credit line 另有声明。

逐图检查了 5 幅主图和 9 幅 Extended Data 图的实际官方 HTML/PDF 图注：

- 主图 2：`Figure adapted from ref. 28, Google DeepMind.`
- 主图 5：`Figure reproduced from ref. 28, Google DeepMind.`
- Extended Data 图 2：`Credit: Google DeepMind.`
- Extended Data 图 7、8、9：`Figure adapted from ref. 28.`
- 其他图注没有另外声明排除许可。

这些来源署名均在中文图注保留。上述 credit 没有印出排除文章 CC 许可或仅限特定使用的声明，依文章明确的默认规则使用。metadata.json 逐图记录原文 credit、来源页、图域坐标、SHA-256 和判断。原图保留完整代码、状态、曲线、数值、数学符号与高亮，不重绘曲线，不声称有原始训练数据。

译者 `ai-self-study contributors`，机器辅助、非官方。修改包括中文翻译、重新排版、从正式 PDF 导出完整图域、在图外提供自然语言完整中文对应和明确标示的译注。译文和改编部分按 CC BY 4.0 提供，不将许可套到另一版本或独立附件。

## 完整范围

正式本体包括主文 1–7 页、Methods 及其参考/声明 8–14 页、Extended Data 15–25 页。译文保留：摘要；Main；AlphaProof 全部子部分；基准、主 RL 进展、推断扩展、最终评估、IMO 协议和成绩、讨论；Methods 的全部 76 个原文段落及其小标题；4 个无编号显示搜索公式（HTML ID Equa–Equd）；所有行内定义和算法参数；5 主图、1 主表、9 扩展图、2 扩展表；数据与代码可用性；39 人完整署名及贡献、致谢、通讯、利益冲突、同行评审、出版声明与许可；80 条原参考。

所有图中 Lean 代码与证明状态保持原图完整内容，原文图内自然语言题面、注释、描述和图注另给完整中文对应。Extended Data 图 7–9 的完整证明没有改写成摘要或局部截图；它们是源文证明产物的忠实复制，并未由译者执行、重新编译或独立验证。图中没有提供的交互悬停状态不被虚构；原文指向的交互工具链接保留。

## 独立补充材料

实际读取独立 Supplementary Information PDF 的封面、元数据及许可文本检索：9 页，未找到 Creative Commons / CC BY 声明。独立 Supplementary Data 1 ZIP 在 `/tmp` 读取成员目录与 Python 文件文本，仅有目录 `2025-06-13867A-s2/` 与 `pseudocode.py`，没有独立 LICENSE 文件，代码没有明确再分发许可声明。

因此不自动将这两个独立附件镜像、全文翻译或当作上述 25 页正文的一部分。正文原有引用、附件说明与代码可用性声明完整保留。正式文章称伪代码文件为 `alphaproof_pseudocode.py`，实际 ZIP 成员为 `pseudocode.py`；译文正文保持作者原说法，这一差异在本记录和元数据说明。没有执行附件代码。

网站推荐内容、访问和引用动态计数、搜索作者按钮、分享界面等不是科学文章内容，未纳入所谓“全文”范围。

## 原文异常与限制

1. AND 节点说明称最难子目标具有 `largest V(s,a) or smallest Q(s,a)`，同时 V 为剩余步骤的负值、Q 为 `gamma^(-V-1)`、AND 回传最小 V。译文保留全部原表述和公式，明确标出可能的符号关系问题，不静默改字。
2. 主表 1 的 12 TPU 小时 PutnamBench-test 为 39.4%，扩展表 2 和图 4 为 39.5%。miniF2F-valid 的若干图与表标注也略异。各值忠实保留，不人工统一。
3. 正式 PDF 的 P2 英文题面注释里 n 与 N 间比较符号显示不完整；相邻 Lean 形式命题清楚为 `∀ n ≥ N`。中文题面据此恢复为 n≥N，注明依据；原图未修补。
4. IMO 的 28/42 分是 AlphaProof P1/P2/P6 加 AlphaGeometry 2 P4 的联合成绩。P3/P5 未解；五道非几何题人工形式化；Gemini 产生 k=500 候选；每个 AlphaProof 成功解答耗时 2–3 日 TTRL。所有条件完整保留。
5. 自动形式化的语法有效、形式证明的内核正确以及忠实于自然语言原题，按原文分开。训练可利用偏离原题的命题不等于评估时自然语言翻译已经正确。
6. 可读正文与方法译文不冒充算法复现。没有训练 AlphaProof、运行 Lean 图中代码或对其性能作新的实验验证。

覆盖映射在 coverage.json；各文件、源件及图域哈希在 metadata.json/verification.json。本作者核对不是独立翻译审稿；独立审者由父层另外安排。
