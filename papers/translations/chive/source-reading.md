# CHIVE 指定版本的读源与翻译依据

原作：Adam Karvonen、Euan Ong、Subhash Kantamneni、Samuel Marks，*Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments*，arXiv:2608.16747v1，2026-08-17。

使用版本固定的 PDF、HTML 与 TeX source：

- https://arxiv.org/pdf/2608.16747v1
- https://arxiv.org/html/2608.16747v1
- https://arxiv.org/src/2608.16747v1

临时原件在 `/tmp/chive-v1/`。精确哈希见 `metadata.json`。PDF 为35页；源 `main.tex` 为1133行，正文1–6、附录A–G；14图、10表、72标签。源码书目36条，实际引用且打印35条；未引用的 `lindsey2025biology` 不属于原打印书目，在 `bibliography-map.json` 明确标识，未冒充缺漏。

读取了整个源稿的正文与所有附录（1–1133行），完整书目源，PDF提取文本；直接查看了11张原PNG图。3张由TeX生成的文本图在译稿完整中文重构，代码标识符和实验计数保持原样；11张图复制后与原图SHA-256逐一相同。逐图检查源图注，无第三方credit-line许可例外。指定arXiv v1的view-license链接直接指向CC BY 4.0，且父代理另有独立许可核验。未将被引论文的许可误当成本篇许可。

`coverage.json` 将72个原标签对应到译稿位置，并记录摘要、作者、致谢、贡献、附录目录与实际打印书目。原稿没有独立编号的equation/align环境，主要数学为段内阈值、概率区间、LoRA/KL符号、AUROC变化与置信区间；它们在对应原节中保留。`table-number-check.json` 比较10表中第一midrule后数值单元格的顺序；十表全部一致。表头翻译与模型名缩写不纳入这个机械比较。这个检查不证明文字语义正确。

保留的重要证据边界：

- 解释不是评价真值，标签来自实测反事实结果。
- 可解释性评价限制只读访问，不包括steering/activation patching等干预技术。
- 三种激活工具、两个主要目标、三个预测家族的无增益结果没有扩写成“一切可解释性无效”。
- 反事实预测训练与开放解释训练是不同目标；后者混合结果及对强模拟器的损害完整保留。
- 没有特权访问证据不等于证明特权访问不可能；原作两种可能解释及数据规模局限均保留。
- 暗示资料中答案正确性与标签相关的构造局限、行为漂移、未计目标服务成本、未分析的397B推理资料均保留。

原稿自身存在少量跨图表数字差异：主文Gemma图的AO/NLA/SAE AUROC为80.9/80.3/81.0，跨模型表中Opus列为.810/.808/.812。图与表均各自原样保留，没有替作者调和或将其静默改成相同结果。D.2自由形式回答段在中文中明确指生成被分析的原始回答，避免误读成后续Yes/No训练目标；该说明与D.1目标定义一致，作为译本措辞澄清记录于metadata。

本稿为机器辅助非官方译本。由翻译代理作逐节内容、术语、公式、数字与标签复核；没有在本委托内虚称独立专业翻译审校。隔离编译与视觉检查记录见 `translation-check.json`；最终单篇与合订PDF由根代理从同版源码构建。
