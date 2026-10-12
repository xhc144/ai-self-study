# v0.3 独立读者审查

当前结论：**PASS（教材与下列三份原创研究说明的内容、数学条件和测量范围）**。首轮失败及其修复追踪保留如下；不包含 PDF 编译/逐页视觉或完整论文许可审计。

首轮结论：NEEDS_REVISION。当时待作者修订以下问题及补入标准 Transformer/公开模型小节；以下是首轮历史记录，最终修复状态见增量复查部分。

## 身份、范围与实际阅读

审查者是没有撰写本稿的独立模型 Agent，不是人类专家。以高中代数、单变量导数、基本 Python 为读者基线，按 main 的实际顺序连续阅读全部 11 个主线单元与 3 个工具附录：01 → language-prediction → 06 → 07 → 05 → 09 → posttraining → 10 → 11 → 12 → 13 → 02 → 03 → 04。08.tex 是拆分前未被 main 输入的旧稿，不作为当前教材主线。阅读完整文本，未凭文件名或摘要替代阅读；分批输出被截断处已单独补读。未查重复的 26 篇许可账本；未把 v0.2 的 metadata_depth 当作当前全稿阅读程度。

读取 math-lecture-writing 与 math-latex-typesetting 的完整 SKILL.md。通过 skills.read 访问其 writing-and-proof/review-gates 等附属资源失败；不伪称读取了无法访问的资源。本轮据实际可访问主文件中的教学、数学及诚实交付要求复核内容。没有运行模板验证器、编译教材，也没有实际查看任何教材 PDF 页面；不签发版式机械或逐页视觉 PASS。

## 必须修正

| 编号 | 严重度 | 初读位置 | 问题与可执行修正 |
|---|---|---|---|
| R1 | 高，编译/版本一致性 | main.tex originalpreface 定义和正文前言 | 初读时新前言误进入 `\newcommand{\originalpreface` 的定义位置，破坏宏，正文又保留“全部合成数据/不需外部权重”“不打包第三方论文全文”等与当前公开模型及译文交付矛盾的旧说法。作者正在并发修改，该中间态不作为最终结果；最终必须恢复完整宏，并统一实际版本范围。 |
| R2 | 高，教学依赖 | language-prediction.tex:3、77–100 | “上一章给出了因果注意力”“前章的算子”与新的顺序不符。代码桥梁在计算图及注意力前使用 QKᵀ、AV、残差。改开头，并将这块明确安排为先读任务轮廓、随后模型单元讲完再回来复算，给精确章节引用。不能假定首次读者已掌握尚未教授的算子。 |
| R3 | 中，条件遗漏 | language-prediction.tex:121–134 | 仅说 ε 的分量独立，不蕴含 ε 独立于 w，后验似然推导需要后者。明确 ε 独立于 w；新查询噪声 ε* 独立于 w 及训练噪声。 |
| R4 | 中，按需先修定位 | language-prediction.tex:113–136 | 连续 ICL 例首次使用协方差、正定、逆、det 和高斯积分，不能只靠总前言“回查工具”支撑。标出矩阵/概率附录的具体节，明确一维数字例为首次阅读入口；高斯积分/归一化性质是调用工具而非本书已证的新结论。已有配方与均值方差推导本身正确。 |
| R5 | 中，集合条件 | 07.tex:228–241 | 在线 softmax 合并公式对应尚未处理的新键块，必须写 J∩B=∅；若块重叠，求和会重复计数，而并集不会。补不相交条件即可。 |
| R6 | 中，实际算法身份 | posttraining.tex:72–76 | 整序列概率比裁剪是一个可讲解的代理项，但 R1/GRPO 实际采用 token 级概率比及序列内部权重。明确当前式为序列级教学替代项，不是完整 GRPO，并提供原文 token 级版本定位/公式，以免据此实现错误算法。 |
| R7 | 低，边界 | 10.tex:132 | 剔除自身均值含 G−1 分母，需要 G≥2。添加边界条件，G=1 时组均值更新本来恒零。 |
| R8 | 中，表格与目标口径 | 13.tex:39–50 | 错误评估器公式含 0.01cost，但表中 x²+x（cost=3）与查表（cost=7）的“错误开发损失”写0。JSON中 faulty_dev_loss 实际仅是单侧数据误差。保留数据并把列改为“单侧开发误差（不含成本）”，或表出含成本的0.03/0.07，不要暗换目标。 |
| R9 | 中，期望定义 | 13.tex:119–125 | LLaDA 的期望没有指定 t 分布。写 t~U(0,1]，固定 t 的枚举算例明确是在条件于该 t 的期望中计算。 |
| R10 | 低，名称 | 09.tex:95 | “FineWeb v2”容易被误读成多语言 FineWeb2 数据集；本来源实际是 arXiv:2406.17557v2。改为“FineWeb 论文的 v2 版本”。 |

## 已检查而无需推倒重写的内容

现代问题首章直接从条件语言模型/提示/训练/搜索/工具的区分进入，数学工具后置，未要求先读传统 ML 全部算法。注意力、数据、后训练、推理预算与机制检验能够持续回到相同的问题与证据单位。后半部不是只列术语的提纲；有推导、算例、失败对照、练习及完整解答。

数学复核覆盖：矩阵行列约定与 Frobenius 梯度、共享 gather/广播/残差累加；LayerNorm 含 ε 完整导数及 D=1/常量输入边界；RoPE 行向量旋转及相对点积、不把周期公式当外推保证；完整注意力/多头/pre-norm/共享输出梯度；在线 softmax 前后向不变量；错位目标、padding 与 tokens 分母、温度/top-p、KV 等价与成本；ICL 离散 Bayes 和连续配方；DPO KL 最优分布、BT 概率、参考支持及梯度；策略梯度支持/奖励不依参数/独立基线、组均值(1−1/G)偏差；Hoeffding 固定候选/非有界 NLL 范围；探针可解码≠因果使用、SAE 尺度与非唯一性、IG 条件及基线；收缩/谱半径/语义正确的区分；多项式有限验证证书、二项区间与随机单位。除上表精确条件问题外，主计算链可重建，没有发现需重写核心证明的错误。

特别确认：正文没有将收缩当作语义正确证明，没有将探针准确率当作原模型使用该信息的证据，没有将有限 pass@256 当作无限支持定理，也没有将理想符号来源规则误称为模型学会 IH。

## 实际独立验证

实际执行 `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_v03_*.py' -v`：36 项测试全部通过，耗时 2.233s。测试检查导数、重复词累计、掩码边界、在线算法、基线、解析奖励解、收缩反例、留出和复现契约；它们不替代上述数学和教学审查。没有修改冻结设计、调用收费服务、重训到好结果、下载新模型或改变正文/代码。

已读两个新增真实模型实验的脚本、设计哈希、环境和 metrics。标准 Transformer 为2层 pre-norm/GELU/2头、18,026参数，3种子×2条件全部6次；同种子的初始参数哈希配对一致，未来编辑的前缀误差均0。balanced 训练NLL约0.25648、测试1.27731–1.31589；重复某组合后的加权训练NLL约0.08990–0.09000、平衡训练NLL约0.431、测试1.34748–1.39847。应明确这是同更新步数的频率重加权，重复组每步36行、对照6行，处理token/FLOPs并不匹配。叫声成功与整句随机分支失败应同时报告。

公开135M诊断保留2个固定 revision 的真实权重、54条原始记录；全部严格生成正确率/AB格式率均0，而受限二候选分数准确率为10/18（约0.5556），各子类为0.5/0.6667/0.5。分数只归一化候选字符串的概率，不能写成校准信心。native_chat 与 matched_plain 分开，不能将模板加权重联合变化唯一归因于后训练；本诊断没有进行RLVR训练或复现R1/能力边界论文。正文新增小节待作者补入后复核。

## Primary 来源核对

实际读取 [IH 官方研究网页](https://openai.com/index/instruction-hierarchy-challenge/) 的 Results/能力表及 [IH 论文](https://arxiv.org/html/2603.10521v1) 摘要、§4和表2–4：84.1→94.1、聊天/偏好下降等与正文相符；训练行为证据与执行器有限保证的身份区分合理。读取 [Anthropic 官方浏览器防御报告](https://www.anthropic.com/research/prompt-injection-defenses) 的日期、防御方法及攻击预算：100次自适应尝试、约1%与未解决限制均与正文相符。未把自适应预算ASR换算为IID单次概率。

读取 [FineWeb 原论文v2](https://arxiv.org/html/2406.17557v2) §3.1、§3.4、§4及附录E，1.71B/28B/350B、两个初始化/子样本及全局去重约90%的出处可定位，正文没有夸大全域保证。读取 [RLVR 能力边界原论文v5](https://arxiv.org/html/2504.13837v5) 的理论/实验定义及表4，25.1→28.3与68.3→63.9准确；正文对有限覆盖结论的限定比原作者全称解释更谨慎。R1 Nature在线读取返回错误，当前核对只读取本地指定译文及来源记录中的Fig1数字；不虚报已经成功在线读取Nature全文。CHIVE/STARS内容身份与局限已审，但本轮未再完整独立读取其原论文。

## 补充低严重度文字检查

12.tex:22 的平均损失对 u_i 导数应含 1/n；后续总参数公式含该因子且正确。把该句改为“单样本交叉熵对 u_i 的导数为 p_i−y_i”即可。13.tex:217 的1.44–1.47是各划分五种子平均，实际已公开单跑表约1.161–1.585，应加“各划分的五种子平均”。

已补读全部实际引入的 generated/v02-attention、residual、research-summary、research-runs、research-effects、research-positions。两个新增模型实验的 code/design/metrics 记录哈希与当前文件实际独立比较，6项绑定全部为True。

## 初轮快照

以下哈希记录在完整初读之后计算，代表下述时刻工作树；作者并发修改的main中间态已告知，不声称初读每一行均来自不可变文件系统。最终复查将重读改动并绑定最终快照。

记录时刻：2026-10-12T01:44:58.922130+00:00

| 文件 | SHA-256 |
|---|---|
| book/main.tex | `cc9bd3cfa63500a2cf2bde1ee5d7ad3ef6f35c2fcae80890875555f468e8be59` |
| book/chapters/01.tex | `0fa88d765b6089acabbe1d5bdf60549ec9bdd8c9b390a6644ec0686e38f7b1d7` |
| book/chapters/language-prediction.tex | `19bb76698fdc2cc4d4bfc6f646545d9ed442776f4efe8686a17bc861edcd203b` |
| book/chapters/06.tex | `36c12f508dbfffdcd7b2f01683128ef70a7100ae3b87fe643c513839d15cb503` |
| book/chapters/07.tex | `fb2305513db4d6b3c90bd4584a767b7d644032a5e59470400b7a6e21a4f2dfa3` |
| book/chapters/05.tex | `afc7dcdd55c69241c4fb6a5be976060244bbeb5c47c459f2ea305d126408a9bb` |
| book/chapters/09.tex | `0adc3183de91ed9babd59d40aea63b03b3172b2e7c7c7bd3ccbcc8b88ca89605` |
| book/chapters/posttraining.tex | `cf3d94660f5d31a30db10155ccb093fb4a15daa791c6ec219ea3edafe46aa40f` |
| book/chapters/10.tex | `aa8038eaecaa04daa43855ea06dd0ae1aad221dccacf040510473853d703180d` |
| book/chapters/11.tex | `700f3b3dfc56c51b147b5c595216cfae4f3d1dd521425452ae602322137bd8ae` |
| book/chapters/12.tex | `9952797f799c68893cfb3fcf826ed31908c32630d52af6e6a90cf3b632a5a999` |
| book/chapters/13.tex | `18a1840a7bf4600b826d9887d756da2b86b2e282f574ea4fede40ba6590e3eeb` |
| book/chapters/02.tex | `9fdbf5ff16efb0b2883e93c91649b0a616e7559fcb2310eac938190ba8f7accf` |
| book/chapters/03.tex | `db77613bd0d3a8ffd788aef0fd00d00994938fb8eb5e9b863386decd88be4dea` |
| book/chapters/04.tex | `b23179240e0f090be6874934ab8dc36981069fb1147d84cf1c8ab0d5561418df` |
| book/references.tex | `6515f9db4f4a844804ded948958545f2e2a7f9d81ed9da357040ed70aa9a47bd` |
| results/standard-transformer-v03/metrics.json | `223ea684596ea7e9f61cb2f1376795ba37933c088bc47ebedeb4f115d2b56c29` |
| results/standard-transformer-v03/environment.json | `99528296934ef398c4487befc5c55d5687bb0d5f385c86a643915bc8f1ee1a57` |
| results/public-models-v03/metrics.json | `f4681922622d8c218f434db82aebf8f60103833d0294a95e2db4df11047e49d0` |
| results/public-models-v03/environment.json | `aac768d47cc7fca1664cd213d3c6cb46001b90ecaaac8c07b834522761fcc36d` |
| experiments/standard_transformer_study.py | `a62b9b5036d6de396e722c3adf2485a4fcc343af3766febeb1d4318eb8400e13` |
| experiments/public_model_diagnostics.py | `5d0ba971d93e74bb486f754a53f9278dae1b980279154dc5875e3f341bfbd07d` |


## 冻结增量的独立复查与最终结论

实际复查全部 R1–R10 及两项追加文字问题，完整连读 book/sections/standard-model.tex、public-models.tex、它们实际引入的两张 generated 表和 papers/studies/ih-challenge.tex、browser-injection.tex、r1-reading.tex。未变化单元沿用首轮全文读取；变化单元重读修订及相邻推导。当前没有未处理的内容/数学阻断项，签发上述限定范围的 PASS。此 PASS 不是“所有事实无误”的保证，不签发九篇译文或其他论文的许可/忠实性总审查，也不替代另轮 PDF 检查。

| 首轮问题 | 实际复查证据与状态 |
|---|---|
| R1 | 当前 main 的锁定 class 与 git HEAD 对应区块逐字节相等（独立脚本实际比较True）；原始宏恢复，正文前言描述 NumPy/标准模型/公开135M 的不同运行条件。当前译文数量由作者更新为九篇；本审查仅核对文字与本任务范围，不代替其独立许可队列。已解决。 |
| R2 | language-prediction 开头先定义任务，精确引用后面的 ch:nn/ch:attention；代码桥梁明确第一次只读输入/输出/损失轮廓，完成后续算子单元再复算。已解决。 |
| R3 | 命题明确训练噪声独立于 w、新噪声独立于 w 与全部训练噪声。已解决。 |
| R4 | 在连续 ICL 前标出线性代数/概率附录，允许一维算例作为初读入口，连续密度与积分性质明示调用。已解决。 |
| R5 | 更新及命题均写 J∩B=∅，合并不变量对应互不相交键块。已解决。 |
| R6 | 初轮“Nature 实际采用 token 级”的判断不准确，正式撤回这部分判断。当前正文正确区分 Nature Methods式(1)的整输出记号、预印本 token 级式和本地序列教学示意，给出逐token平均及乘积裁剪≠逐项裁剪的说明。该澄清可保留，但不能把 Nature 原式误报成 token 式。 |
| R7 | 留一基线明确 G≥2。已解决。 |
| R8 | 表格列明确单侧开发误差“不含成本”，与原JSON的数据误差字段一致。已解决。 |
| R9 | t明确 Unif(0,1]，枚举依固定t给不同结果；带权/未带权和边缘/联合差异保持。已解决。 |
| R10 | 09写“FineWeb论文的v2版本”，与实际 arXiv版本对应。已解决。 |
| 追加 probe | 对u_i的p_i−y_i明确是单样本交叉熵，完整平均梯度保留1/n。已解决。 |
| 追加 NLL | 1.44–1.47明确为各划分五种子平均；单跑全表保留。已解决。 |

### 首轮 R6 的 primary 原件更正

增量阶段实际读取了已下载的 [Nature正式原文](https://www.nature.com/articles/s41586-025-09422-z) HTML `/tmp/r1-nature-translation-source/article.html` 中 Methods/GRPO 的式(1)–(3)及相邻正文。HTML SHA-256为 `3a99f19b58a480e518f7db0a7db61b9eae4343fbc958fc0f6e6ebfbd18203f8d`。式(1)的比值确实是 πθ(o_i|q)/πold(o_i|q)。因此根代理的纠正有原件依据。本轮只对这一小段独立读取，不声称重读了整篇Nature论文。本文首轮对原算法粒度的过度概括是审查者自身错误，已纠正，未要求篡改正式译文。

### 两个新增实测小节

标准模型小节的六行表与原metrics一致。数据重加权公式正确，重复组31份指定句加5份其他句共36；同种子初始化一致、同600更新步，6vs36处理行和FLOPs不匹配明确写出。训练目标改善、平衡分布恶化、留出NLL提高、叫声仍正确与干预重叠全部保留，没有把它升级为FineWeb或大模型复现。

公开模型小节完整报告三个条件10/18、格式/严格生成0/18；独立核对记录中54条forced_choice全部为A，55.6%恰等于常选A基线。受限两个指定续写字符串概率与自由生成的区别、完整输出格式失败≠无知识、聊天模板和权重不能唯一因果归因、非RLVR/非IH复现都已明示。原文输出举例与记录一致。两个metrics的当前哈希与environment绑定仍为True；本轮未另下载或改冻结模型设计。

### 三份原创研究说明

完整连读后的数学计算与测量身份正确：IH将格式、知识和高优先级权威分开；拒绝捷径的分组算例和联合得分可复算；模型结果、符号对照和公开模型诊断区别明确。浏览器说明的IID并集式、非独立并集界、多步数值及零成功的单侧区间可复算，未将100次自适应ASR换算为实际单次概率。R1说明区分奖励梯度/评分器、无偏基线/含自身组基线、输出与token两个粒度、pass@k与无限支持；两token裁剪算例为1与0.85正确。

增量初读新增两项条件问题，经反馈后再次实际核对：r1-reading的策略梯度现在明确固定支持、严格正概率、可微、奖励无显式θ及求导交换条件；browser-injection的乘法式现在明确P(M)>0、P(P|M)>0，并为后者为0单独返回0而不调用未定义因子。两项均已解决。

三份均明确原创研究说明而非全文译本，有primary来源引用，无长段原文、原图或原始提示的复制；示意、原创例题和本地结果注明身份，未以arXiv非独占分发许可宣称取得翻译授权，R1正式本体与独立附件版本区分清楚。本轮版权检查限于这三份可见文本及身份标注，不代替逐篇授权/图片credit line审计。

### 独立测试与检查范围

实际执行默认环境全测试：53项，51项通过、2项因缺少可选PyTorch而跳过，2.814s。随后在 `/tmp/ai-model-env/bin/python` 实际运行 test_model_protocols.py 的3项（包括这2项可选测试），全部通过，0.886s。所以53项功能覆盖均有本审查者实际运行证据，而非把skipped写作通过。未对已经通过的主数值实验重新调参或重训。实际对阅读范围的cite/bibitem做机械交叉核对，缺失key列表为空。

教材 PDF 编译、版式机械验证、所有页的视觉检查仍由另轮负责，本轮没有打开PDF或将其视觉状态标为完成。首轮无法访问的skill附属资源限制仍保留，不以自动测试替代内容阅读。

## 最终阅读快照

以下哈希在上述修订内容阅读完成后生成；final PASS绑定这一范围。时间：2026-10-12T02:04:40.006821+00:00。

| 文件 | SHA-256 |
|---|---|
| book/main.tex | `ef575198f84c7b2060f2d954c24df12183b744cfecb8d9099bd6f6cb85d454a3` |
| book/chapters/01.tex | `0fa88d765b6089acabbe1d5bdf60549ec9bdd8c9b390a6644ec0686e38f7b1d7` |
| book/chapters/language-prediction.tex | `20d8efe61bea6ddd774c2e9b9377f4a3df3c847ab04b18db628793f13e0bbce5` |
| book/chapters/06.tex | `36c12f508dbfffdcd7b2f01683128ef70a7100ae3b87fe643c513839d15cb503` |
| book/chapters/07.tex | `1fb1c730cd83eab2954fa55f19382151f8dcc940e3e983fb24e14a8c962488bf` |
| book/chapters/05.tex | `afc7dcdd55c69241c4fb6a5be976060244bbeb5c47c459f2ea305d126408a9bb` |
| book/chapters/09.tex | `b6201c62bbdff859e54214fb80ed1b79d1f69df6c0ffb3bc561fb1c7a1d066d4` |
| book/chapters/posttraining.tex | `61b7c793755e44b180390d3cdc4d0619d9980d26d2427f124575727d1b1524dc` |
| book/chapters/10.tex | `d218e48baf81c17bd8e98908e5feaeaeaed190a6adff496543546e30d67bd9fd` |
| book/chapters/11.tex | `700f3b3dfc56c51b147b5c595216cfae4f3d1dd521425452ae602322137bd8ae` |
| book/chapters/12.tex | `802b32f06f48b56a3c34581b2fbe201eea28220522c42c6ab4d239873e94edc9` |
| book/chapters/13.tex | `f9a03b57beee8b59e8d039bac78c2324e22b3dcf8a805d3925b3a736b0a4f8b0` |
| book/chapters/02.tex | `9fdbf5ff16efb0b2883e93c91649b0a616e7559fcb2310eac938190ba8f7accf` |
| book/chapters/03.tex | `db77613bd0d3a8ffd788aef0fd00d00994938fb8eb5e9b863386decd88be4dea` |
| book/chapters/04.tex | `b23179240e0f090be6874934ab8dc36981069fb1147d84cf1c8ab0d5561418df` |
| book/references.tex | `2cf035a1d74ed30e1806c8d32b0a633d5899db9ac09f265fb441b16018c00c82` |
| book/sections/standard-model.tex | `ff0aabea6c8d01622ea7eb10628c5c595b802acd8945abd1807b9bf1cd868581` |
| book/sections/public-models.tex | `51a6751284b459d1bce5124f018668d610f0dc307f2e4387df66865c3285f221` |
| book/generated/v03-standard-table.tex | `4dc309404a021d336065c8e0ee65b0db507df881f57634876d7e5392c0596882` |
| book/generated/v03-public-table.tex | `2c5bb0772c1a8f1394aea2329577c907b414fc2c34314237a55e4b048cd18aee` |
| papers/studies/ih-challenge.tex | `7064549a30795cc12a5f81ed27b37d9ecee0fb5576c38dea7a89c7d396a431b5` |
| papers/studies/browser-injection.tex | `00e95fe9588b47fb0fdf14c84cb0820e2567f3dff6ad2537b0fbedcfe94e0b88` |
| papers/studies/r1-reading.tex | `4bb7099c88271488a762cadd3a0d94aa2955b900637691d302895bb33edb65dd` |
| results/standard-transformer-v03/metrics.json | `223ea684596ea7e9f61cb2f1376795ba37933c088bc47ebedeb4f115d2b56c29` |
| results/public-models-v03/metrics.json | `f4681922622d8c218f434db82aebf8f60103833d0294a95e2db4df11047e49d0` |


## 最后新增 research-bridges 的增量内容复查

已完整读取 Engram→CaT→AlphaProof 三小节、research_bridges.py、对应seed144结果与环境。初读发现离散token与隐藏向量共用x、哈希/hidden共用h的类型歧义，已反馈根代理；修订后再次读取，现用u_t/H/a_t/e_t/V/g分别指定token、哈希、隐藏向量、表向量、投影与连续门控，维度相容。这一项已解决。

共享lookup梯度按所有访问求和，三次重复2号表项与未访问行零梯度说明正确；实际51坐标有限差分误差4.9445e−11。单头257地址/双头1000签名的范围明确限于指定整数例，没有语义无碰撞保证。CaT多数投票的二元IID/共享Bernoulli条件与二项尾证明正确；对G=9/33的实际数值均与metrics一致，未把人为相关性模拟当成LLM或医疗可靠性研究。独立精确二项尾约0.09880866/0.00782066，有限20,000组模拟0.10055/0.00795的差异属于采样波动。AlphaProof部分把AND/OR搜索排序与形式证明核证书区分，并保留人工形式化、联合系统、题意、公理和成本边界。

实际独立执行新增test_research_bridges.py三项全部通过（0.041s）；另直接调用run(144)，整个返回对象与保存metrics逐项相等。环境中code/metrics的SHA-256绑定均实际为True。本轮无需重复其余53项已通过的测试；56项的完整范围由此前53加本轮3组成。内容/数学PASS扩展到本次新增三小节，之前的审查历史与有限范围保持。

`book/chapters/13.tex` SHA-256: `55eaf93e06641a63851d88bc0c8c4359d2fdd52e9480e9e4bac07d546e90c1d6`。

`book/sections/research-bridges.tex` SHA-256: `6da733fedc6705569c7378690b1dd33dfec57f2387be548336fcd505faf28be4`。

`experiments/research_bridges.py` SHA-256: `63a54e9f93d66f318579c598f2073233fb6bdcc273804c79f158206a2e597e75`。

`results/research-bridges-v03/metrics.json` SHA-256: `cbea4fc6e418d3dad08f12e62f528cac31a71244e843ce69c16942ba24f0e10b`。

`results/research-bridges-v03/environment.json` SHA-256: `ace5e6f8721ed7daa7576fa95d02d4d8856955340d3c2a579f07ab2300782126`。

`tests/test_research_bridges.py` SHA-256: `3efd18779497afba819166eff5dd38a56fc9563ad344578d5f34e2227fbffea5`。


最终PDF返修只将 standard-model.tex 的代码文件名改为可断行path，内容不变。当前源码/PDF绑定见独立PDF报告 qa/v03-final-pdf-book-studies.md/json；本内容PASS仍有效。

`book/main.tex` 最终SHA-256：`ef575198f84c7b2060f2d954c24df12183b744cfecb8d9099bd6f6cb85d454a3`。

`book/chapters/13.tex` 最终SHA-256：`55eaf93e06641a63851d88bc0c8c4359d2fdd52e9480e9e4bac07d546e90c1d6`。

`book/sections/research-bridges.tex` 最终SHA-256：`6da733fedc6705569c7378690b1dd33dfec57f2387be548336fcd505faf28be4`。

`book/sections/standard-model.tex` 最终SHA-256：`223d4ad098190257bd47d1bbf869bed324092e4a7236c83ad6dd688bd703ee70`。

`dist/ai-self-study.pdf` 最终SHA-256：`c9bdf9aa359158ce80fea766aabb35d3796adefa36364283b3bdb03491edd4d9`。
