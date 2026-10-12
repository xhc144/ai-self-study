# AlphaProof 正式版本独立审查

内容审查和最终 root 构建 39 页 PDF 的独立布局审查均完成，通过。本审者不是 AlphaProof 译者，没有把译者的 38 页自检 PDF 当作正式独立证据。

## 原件与许可

实际重新下载 [Nature 正式 PDF](https://www.nature.com/articles/s41586-025-09833-y.pdf)，25 页，SHA-256 `ef6ea043c1acd4712c43369a294f6c8581d47c8f3dc2c660f69f5dd2a7c96f30`，与译稿 metadata 一致。[官方文章](https://www.nature.com/articles/s41586-025-09833-y) 明确 Version of Record 2026-03-13、首次在线 2025-11-12、期次 2026-03-19。已实际打开 Rights and permissions、点开 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，并视觉查看原 PDF 第 7 页的许可段。fresh HTML 与留存 HTML 的原始哈希不同，属于动态网页；科学段落另行核对，Methods 的 76 段一致。

## 内容核对

- 全部 76 个 Methods 原段逐段读完，与 methods.tex 对照；允许段落合并，未发现实质遗漏。JSON 给出独立的原段哈希与译稿行号映射。
- Equa–Equd 四个搜索公式及行内条件核对一致。AND 最小回报/最长分支、未证子目标选择、1−Q 和最小 V 回传均保留。原文 largest V or smallest Q 与负剩余步骤语义存在关系异常；译文忠实保留并单独说明。通常 0<γ<1 时 dQ/dV=−log(γ)Q>0，不能把两个方向视作等价。此判断是审者推论，不冒充作者勘误。
- 39 位作者姓名、顺序与重音符号一致。80 条原书目逐项去标点/大小写/TeX 包装后完全一致；中文题名另外附加。没有声称通读这 80 篇被引文献。
- 14 幅图的官方图注/credit 全部读完；3 张表核对数字与脚注，扩展表实际打开原 PDF 第 24、25 页逐格查看。主表 39.4% 与扩展表/图 39.5% 的原差异被保留。
- 从独立下载原 PDF 重建全部 16 个图域资产：13 个逐像素一致，另 3 个同尺寸，色彩通道最大差仅 2–3/255。原图和两张支持表图分开计数；未发现内容删改。
- 五道非几何题人工形式化、P5 首日形式化未成功、额外自动形式化实验、Gemini+Python 候选生成、k=500、P1/P2/P6 反驳比例 99%/98%/7% 均保留。每个成功解答需 2–3 日 TTRL。28/42 属于 AlphaProof 解 P1/P2/P6 加 AlphaGeometry 2 解 P4 的联合银牌等级分数；P3/P5 未解，未夸成学生时限内独立整卷作答。
- 独立 Supplementary Information 和 Supplementary Data 1 不属于指定 25 页本体，排除范围透明且正文引用保留；没有将此误记为正文缺页。

## 发现与待办

`AP-COPYRIGHT-1`：原正式 PDF 第 7 页有“© The Author(s) 2025”，此项已通知 root 并修复，最终第 32 页保留“© The Author(s) 2025（© 原作者 2025）”，原年份正确。除此未发现需要改动的实质内容问题。

最终 root PDF 的全 39 页渲染、9 个关键页高清、页边界、表格脚注、完整证明图与全部 215 个链接检查已完成，见 `qa/v03-final-pdf-alphaproof.md/json`。证据与绑定哈希详见同名 JSON；原件和工作文件只在 `/tmp/alphaproof-independent-review/`。
