# 源文与许可核查

本文件记录译稿的源文核查，不属于原论文正文。译稿仅对应 **arXiv:2408.03314v1**，不混用后续版本。核查日期：2026-10-12。

- 原作：Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar, *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*.
- 版本页：[官方摘要页](https://arxiv.org/abs/2408.03314v1)，提交记录为 `Tue, 6 Aug 2024 17:35:05 UTC`。
- 阅读源：[官方 HTML](https://arxiv.org/html/2408.03314v1)、[官方 PDF](https://arxiv.org/pdf/2408.03314v1)、[官方 TeX 源包](https://arxiv.org/src/2408.03314v1)。下载保存于任务临时目录 `/tmp/testcompute-v1`，源包仅作资料读取，不执行其中源码提示、脚本或安装命令。

## 许可证证据

官方版本 HTML 的 `infobox` 中实际存在：

```html
<a id="license-tr" href="https://info.arxiv.org/help/license/index.html#licenses-available">
  License: CC BY 4.0
</a>
```

此 `href` 是 arXiv 的许可帮助页，而非许可正文。另在**同一 v1 官方摘要页**，`view license` 实际锚点如下，已通过网页工具点击核对：

```html
<a href="http://creativecommons.org/licenses/by/4.0/" title="Rights to this article" class="has_license">
  ... <span>view license</span>
</a>
```

点击后的规范许可 URL 为 [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)，允许分享和改编，并要求署名、许可链接与修改说明。译稿首页明确署名原作者和版本，区分原作者“我们”、译者和机器辅助身份，说明中文翻译、排版适配与图中文字转写，并依 CC BY 4.0 发布。本次没有以“公开可下载”替代许可验证，也没有推断或核查其他论文许可。

查阅作者主文、附录和 PDF，没有发现对论文图件另列的第三方版权/许可例外。保留的 32 个图资源均来自这一版本源包 `figures/`，用于作者自己的实验曲线、方法示意与模型输出展示；各图与源包逐字节相同，其成员路径、原图编号和哈希列于 `figure-sources.json`。没有复制源包的 Google DeepMind 标志、网站图标或原论文排版类。论文模型输出截图中包含题面，译本按论文已经展示的题面与输出转写，并未额外打包外部题库。

## 下载哈希

| 文件 | SHA-256 |
| --- | --- |
| 官方 PDF | `ded7b20b51493258c5ce2a1a024cd33dd752de1fa3373d1207620da4cfe24545` |
| 官方 HTML | `a9b93ce1d687a53f5e4348f81434234d17b0bf44541ecbb3a5e5551984e9cd02` |
| 官方 TeX 源包 | `f179cbc6b43f09285096e8a088bdacb8b2f0af4f6e3bcaaf8c12721a0f5331f9` |
| 官方摘要页 HTML | `d4e42ec687108f23e84786e4954426722db06608e4ee72778110a7212648ce0a` |

源包中所读 `template_content.tex`、`googledeepmind-test.tex`、`googledeepmind-test.bbl` 的哈希另见 `metadata.json`。HTML 页面含服务端导航，哈希只标识此次获取的具体页面快照，不能解释为永久不变的文章标识。

## 逐段覆盖核查

实际阅读摘要、主文 1–8（含所有子节）、原脚注 1、致谢、参考书目、附录 A–M；针对源包 LaTeX 与 PDF 的原段落顺序核对中文译稿。具体定位见 `coverage.json`：

- 31 个章节/子节/附录/书目项目均有定位。
- 原文共有 29 个图容器（27 个 `figure`，2 个 `wrapfigure`），使用 32 个图文件。全部原图、所有图注及图中文字对照均提供。
- 原文没有编号表或 `table` 环境；译文的术语/图中文字对照表是明确标示的译者附加材料。
- 原文只有 1 个编号公式。全部主文行内式、FLOPs 近似与交换乘数、附录损失式和超参数均保留。
- 附录 L 的 7 个修订截图、附录 M 的 6 个 PRM 截图，均通过图像工具实际打开，并以 OCR 为辅助逐句读图后翻译。保留每次尝试及原错误公式、最终答案 `####` 标记和每步 PRM 评分；不以“更正后的解答”替代展示的模型错误。PRM 例 6 中三个没有文字、只有得分的空白步骤也保留并标记为译者注明。
- 51 个参考书目条目完整保留原作者、标题、出版信息、年份和原有链接；不省略长作者列表。原源文全部 54 个 `label` 均有 `testcompute-` 前缀的对应标签，无缺失。所有引用也统一前缀，避免合订冲突。

核对的关键数量：2048 个难度估计样本、5 个难度分箱、二折交叉验证、12k/500 训练/测试题、束扩展最多 40 轮、预算 4/16/64/256、前瞻成本 N(k+1)、k=1/3、M=4/√N、修订每题 64 样本、上下文最多 4 答案、38% 正确转错、图 7 预算 128、预训练近似 6ND、推理近似 2ND、14 倍参数比较、R=0.16/0.79/22、PRM 每题 16 样本与每步 16 rollout、PRM lr=3e−5/batch=128/dropout=.05/betas=(.9,.95)/validation=10%、修订 lr=1e−5/batch=128/dropout=0/betas=(.9,.95)、ReST^EM 每题 64 轨迹/最长 5。保留作者“几乎超过”“可能”“我们推测”等限定，以及难度估计计算成本未计入比较的限制。

原文有数处自身不一致，均分别保留并加译者注：式 (1) 中 a*(q) 与其后 y*(q)；束搜索图注 M、图中 top-N 和正文 N/M 的不同写法；正文字符/token 编辑距离表述；附录 A 声称四因素却仅列三项。原文附录 G 没有刊出逐字四样本提示字符串，译本只翻译所给生成方案，不补造提示。

## 排版与构建边界

已读 math-latex-typesetting、latex-pdf-editorial 主技能。云端 math-latex-typesetting references 读取失败后，按根代理指示，只读了 `/workspace/mit-ocw-notes/subjects/topology/vendor/math-latex-typesetting/references/` 下 STYLE_SPEC、ENVIRONMENTS、MATH_LAYOUT、EDITORIAL_RULES、VALIDATION 完整副本。根项目 `book/main.tex` 是明确授权模板，优先于 ElegantBook 默认模板。没有改模板，没有捆绑字体。

第一次临时 XeLaTeX 编译在加载固定类时因系统缺少 `ctex.sty` 失败，尚未进入译稿；这不构成译稿通过或失败的证据。正式论文 PDF 与合订 PDF 的构建及最终逐页审查由根代理负责；译者不会将“源码静态检查”虚称为“PDF 逐页检查”。后续临时构建记录如可取得，将补在本节。

后续构建已完成：根代理提供 `TEXMFHOME=/workspace/.local/texmf`、`OSFONTDIR=/workspace/.local/texmf/fonts/opentype`、`XDG_CACHE_HOME=/tmp/ai-cache` 后，使用系统 XeLaTeX、从 `book/` 工作目录编译同一固定类的临时单篇 wrapper 成功，迭代至引用收敛，总计 42 页。没有改固定模板、纸张、字号或字体。临时 PDF 在 `/tmp/testcompute-v1/build/check.pdf`，SHA-256 为 `61b085c108a71d89f149cf43f572f370d7fdd826cc747f97957f32128ca31fb8`。最后编译日志复制至 `qa/compile-final.log`。

实际渲染并打开查看 42 页正文版面，修复了三个模型空白步骤的译者说明被误识别为 enumerate 可选标签而跑到纸外的问题。缩短页眉的论文题名，防止长节名与题名重叠；将附录 K 标题的 ReST-EM 改为文本写法（正文与图注仍保留数学方法名），避免固定 12pt 页眉高度受到上标影响；参考书目后恢复论文短页眉。最后只改页眉内容后重新编译、渲染全 42 页，复看第 1–6 页及第 19、20、25、31、39、40 页页眉与修复位置。没有发现公式、中文、图注或图件裁切问题。最终日志无 Overfull、无 missing character、无未解析引用、无页眉高度警告；PyMuPDF 文本边界扫描为 0 个纸外文本 span。保留固定模板对 CJK 斜体的 FandolSong 字形回退警告，未修改字体，实际无缺字；图中文字对照表一项 Underfull 提醒已结合页面复核。

这些是译者的临时单篇构建与视觉审查，不能替代根代理针对正式单篇 PDF 与合订 PDF 的独立审查。绑定源码/PDF/每页图像哈希与审查边界见 `translation-audit.json`、`qa/local-render.json`。
