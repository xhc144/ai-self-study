# 正式来源、许可与译文范围

译文对象是 Daya Guo、Dejian Yang、Haowei Zhang 等 194 位作者的 **DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning**，Nature 645, 633–638 (2025)，DOI `10.1038/s41586-025-09422-z`。正式发表与 Version of Record 日期均为 2025-09-17，期次日期 2025-09-18。原作投稿 2025-02-14，接受 2025-07-17。

## 实际读取的原件

- [Nature 正式文章 HTML](https://www.nature.com/articles/s41586-025-09422-z)。实际下载至 `/tmp/r1-nature-translation-source/article.html`，读取所有科学内容部分、作者信息、版权许可和出版日期。检索网页只是辅助，翻译所用段落来自下载原件。
- [Nature 正式 PDF](https://www.nature.com/articles/s41586-025-09422-z.pdf)，实际文件 `/tmp/r1-nature-2025.pdf`，11 页，2,735,576 字节，SHA-256：`916fdaafc3b44143a9744481d079744f773d73d06372f82b1dba1076525927f2`。读取正文 1–6 页、Methods 7–8 页、Extended Data 9–11 页，并将 PDF 与 HTML 比较。
- 原文 [Table 1](https://www.nature.com/articles/s41586-025-09422-z/tables/1)、[Table 2](https://www.nature.com/articles/s41586-025-09422-z/tables/2)、[Extended Data Table 1](https://www.nature.com/articles/s41586-025-09422-z/tables/3)。前两表读取实际 HTML；扩展表在网页上是图片，已实际查看正式 PDF 第 11 页，完整转译题目、评估步骤和表注。
- 194 人作者名单同时核对网页可见作者署名与 citation_author 元数据。metadata.json 以正文显示格式保留完整作者，另保留网页姓在前的引文格式；不把简写封面署名当成完整名单。

读取层级为 relevant_sections / full scientific article：上述正式文章本体的科学正文全部读取；不声称通读它所引用的其他 36 篇文献。参考文献保留原书目信息和原有链接，另加题名中译，而不把引用条目记作那些被引文献本身的核验。

## 许可判断

官方 HTML 的 Rights and permissions 明确声明此文章采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，允许署名条件下改编、翻译和再分发。正式 PDF 同样印有开放获取与许可说明。原文明确写出：文章的图像或第三方材料包括在文章 Creative Commons 许可内，除非其 credit line 另有说明。

逐图检查了正式 PDF 与官方 HTML 的 Fig. 1、Fig. 2、Extended Data Fig. 1、Extended Data Fig. 2 图注，没有发现将材料排除出该许可的独立 credit line。四幅图从正式 PDF 中导出为独立图域 PDF，保留原曲线、坐标、数字、英文标签及箭头；正文提供全部标签中文对应和完整中文图注。图域坐标、来源页和 SHA-256 记录在 metadata.json。导出图不是原始数据重绘，不声称获得了曲线原始数据。

扩展数据表 1 的表注注明题目来自 2024 AIME；没有另外印出排除文章许可的声明。译文只翻译这张正式文章内的数学题示例与评分说明，不镜像第三方 AIME 整卷。

原文版权与作者署名保持；译者为 `ai-self-study contributors`，机器辅助、非官方。修改包括中文翻译、重新排版、独立标识的译注、图域提取与中文标签对应。译文与改编部分按 CC BY 4.0 提供。没有将此许可套用到 arXiv `2501.12948v2`。

## 范围与排除项

已译的正式本体包括：摘要；Main；DeepSeek-R1-Zero；DeepSeek-R1；伦理和安全声明；结论、全部能力限制与未来工作；Methods 的 GRPO、全部奖励模型与训练细节；公式 (1)–(10)；数据与代码可用性；两幅主图、两张主表；两幅扩展数据图与扩展数据表；致谢、完整作者名单、所有现地址说明、作者贡献、通讯信息、利益冲突、同行评审说明、出版者声明、权利许可、出版信息和 36 条参考文献。正式 11 页 PDF 没有这些部分之外的另一篇内附录。

独立 Supplementary Information 为 83 页，含补充章节 1–11、补充表 1–29、补充图 1–16。本次在 `/tmp/r1-nature-translation-source/supplement-inspection-only.pdf` 检查封面、元数据及全文许可关键词；未找到明确的 Creative Commons / CC BY 授权声明。文件里的 MIT license 说的是模型权重，copyright 出现在安全基准讨论中，都不是此附件的再分发许可。依任务要求，不推定主文章许可自动覆盖独立附件，不将其镜像或全文翻译。正文所有对它的引用保留，范围说明也明确它未被翻译。同行评审文件为另一独立附件，同样未镜像、未全文翻译。

网站推荐文章、动态访问/引用计数、作者检索按钮、分享界面不属于论文科学正文，没有作为“漏译段落”纳入正文。

## 忠实性注意事项

- R1-Zero 无 RL 前 SFT，与 R1 的冷启动、拒绝采样、SFT 和两阶段 RL 明确区分。RLVR 只在标识为译注的说明中出现，没有替换作者用词。
- 原文表 1 是带省略号的模型输出摘录，不含最终答案。译文保留源文省略，不从其他论文版本补写答案，不将输出包装成已核实证明。
- “顿悟”“反思”“在心中思考”和“自我演化”等保留为作者对生成行为的描述，不扩大为意识结论。
- Methods 原文第一阶段 GRPO epsilon = 10，正式 PDF/HTML 一致，按原值保留并标出译注；没有按惯常 PPO 参数擅改成 0.1 或 0.2。
- 8.2k 步后最大长度从 32,768 调整到 65,536 是原文明确设置，译文完整保留，不把长度变化只归因于自主行为。
- 式 (1) 为断行临时记 rho 为原始概率比，定义原样保留；式 (2) 原样保留单输出 KL 表达式，不改写成其他论文版本的 token-level 实现。组内标准差为零的处理没有在正式正文说明，译文不编造约定。
- 表 2 的 105 个数值及所有原始粗体显著性标记按 HTML 直接提取；原注的 t 检验、P < 0.01 保留。
- 这是译者作者核对，不是独立翻译审稿。单篇与合订 PDF 的正式交付由根代理集成。
