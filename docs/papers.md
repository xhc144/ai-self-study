# 论文与教材索引

按正文依赖顺序阅读。`relevant_sections` 表示只读列出的相关部分，`abstract_only` 只核验摘要，`metadata_only` 仅核验官方书籍/课程信息；没有一条冒称通读全文。公式推导、中文解释和实验实现由本项目自行完成。引用不赋予第三方材料再分发权。

## cs229 · [CS229 Lecture Notes: Supervised Learning](https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf)

Andrew Ng，2003。

- 先修：线代、导数、概率
- 阅读问题：线性回归、logistic 回归与最大似然如何连接?
- 贡献：监督学习从模型、目标到梯度的经典主线。
- 已核验范围：`relevant_sections`；Part I: linear regression, logistic regression
- 限制：经典讲义; 不是当前课程所有内容。正文只引用与原创解释, 不镜像。
- 权利：第三方版权保留; 未获取开放改编许可

## d2l · [Dive into Deep Learning](https://d2l.ai/)

Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola，1.0.3。

- 先修：Python、基础微积分
- 阅读问题：怎样将数学对象落实为张量与训练代码?
- 贡献：提供从基础到网络、注意力和优化的可执行教材。
- 已核验范围：`relevant_sections`；11.3 attention scoring, 11.7 Transformer
- 限制：本项目代码独立实现, 未复制该教材代码或译文。
- 权利：正文 CC BY-SA 4.0; 样例代码另有 LICENSE-SAMPLECODE

## dl · [Deep Learning](https://www.deeplearningbook.org/)

Ian Goodfellow, Yoshua Bengio, Aaron Courville，2016。

- 先修：线代、概率、微积分
- 阅读问题：如何系统补齐表示、数值与优化基础?
- 贡献：作为第3–8章和第11章的后续学习读物。
- 已核验范围：`metadata_only`；官方目录与免费阅读说明
- 限制：首版未逐章通读; 公式推导为本项目自行给出。
- 权利：MIT Press 版权; 免费阅读不代表可翻译或镜像

## cs336 · [CS336: Language Modeling from Scratch](https://cs336.stanford.edu/)

Tatsunori Hashimoto, Percy Liang 等，Spring 2026。

- 先修：已有ML/DL、Python、线代概率
- 阅读问题：怎样串起分词、模型、系统、数据、后训练与评价?
- 贡献：官方课程明确完整语言模型开发链条及先修。
- 已核验范围：`relevant_sections`；Content, Prerequisites, Assignments, 2026 schedule
- 限制：完整作业涉及 GPU 与系统; 本项目只做原创 CPU 机制实验。
- 权利：课程内容保留原许可; 具体作业代码需单独核对

## mml · [Mathematics for Machine Learning](https://mml-book.github.io/)

Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong，2020。

- 先修：高中代数、导数
- 阅读问题：如何补齐线代、概率、优化与经典模型?
- 贡献：建议按 Ch2–7 补基础, Ch9–10 学线性回归和降维。
- 已核验范围：`metadata_only`；官方书籍主页
- 限制：进一步阅读, 首版不声称通读或复现全书。
- 权利：免费书稿阅读; 不声明开放全文改编许可

## boyd · [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)

Stephen Boyd, Lieven Vandenberghe，2004。

- 先修：多变量微积分、线代
- 阅读问题：何时局部最优能推出全局最优?
- 贡献：后续可读 Ch2–5 与 Ch9, 系统学习凸性和优化。
- 已核验范围：`metadata_only`；作者官方书籍主页
- 限制：本项目不镜像出版社 PDF 或翻译整章。
- 权利：Cambridge University Press 版权保留

## attention · [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

Ashish Vaswani 等，2017; v7 2023。

- 先修：网络、softmax、矩阵微分
- 阅读问题：怎样用内容匹配代替顺序循环?
- 贡献：点积注意力、多头、位置与前馈层的原始架构。
- 已核验范围：`relevant_sections`；v7 §§3.1–3.5, §4
- 限制：原始翻译 encoder-decoder; 不是智能产生的充分理论。
- 权利：arXiv non-exclusive; 文首另有图表学术/新闻署名使用许可, 此项目不复用

## adam · [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980)

Diederik P. Kingma, Jimmy Ba，2014; ICLR 2015。

- 先修：梯度、随机优化
- 阅读问题：如何自适应缩放逐坐标更新?
- 贡献：指数一二阶平均与启动偏差修正。
- 已核验范围：`abstract_only`；v9 abstract; 算法公式本稿自行推导与实现
- 限制：不据摘要宣称任意非凸问题全局收敛。
- 权利：保留第三方论文许可; 不再分发全文

## kaplan · [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)

Jared Kaplan 等，2020。

- 先修：交叉熵、幂律、预算
- 阅读问题：资源变化能否预测平均语言损失?
- 贡献：作者报告研究范围内参数、数据、计算近似幂律。
- 已核验范围：`abstract_only`；abstract
- 限制：损失规律不直接推出意识、可靠性或所有下游能力。
- 权利：arXiv non-exclusive; 仅链接与原创解释

## chinchilla · [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)

Jordan Hoffmann 等，2022。

- 先修：规模规律、优化
- 阅读问题：固定训练预算应如何分给参数与数据?
- 贡献：比较400余模型实验, 并给出损失参数拟合与预算平衡。
- 已核验范围：`relevant_sections`；§§2–3, §3.3 parametric loss, Table2
- 限制：最优点随数据、架构、推理成本改变; 不把经验比值当永恒常数。
- 权利：arXiv non-exclusive; 不镜像

## flash · [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)

Tri Dao 等，2022。

- 先修：注意力、内存层次
- 阅读问题：减少数据搬运能否加速精确注意力?
- 贡献：分块与重计算降低高带宽内存读写和存储需求。
- 已核验范围：`relevant_sections`；algorithm overview and IO complexity
- 限制：改进 IO 不等于一般精确稠密注意力算术复杂度线性。
- 权利：仅链接与原创解释; 不复用代码

## instruct · [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)

Long Ouyang 等，2022。

- 先修：语言建模、偏好与策略
- 阅读问题：用户偏好如何改变生成行为?
- 贡献：示范SFT、偏好奖励模型与RLHF流程。
- 已核验范围：`abstract_only`；abstract
- 限制：作者分布上偏好改善不等于所有回答真实安全。
- 权利：arXiv non-exclusive; 不镜像

## lora · [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

Edward J. Hu 等，2021。

- 先修：矩阵秩、网络梯度
- 阅读问题：如何降低可训练参数量?
- 贡献：冻结原权重, 以低秩矩阵乘积参数化更新。
- 已核验范围：`abstract_only`；abstract
- 限制：低秩限制不适合所有目标, 不消除全部训练内存。
- 权利：论文non-exclusive; 微软代码MIT另许可, 本项目未复制

## dpo · [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)

Rafael Rafailov 等，2023; v3 2024。

- 先修：KL、softmax、最大似然
- 阅读问题：偏好能否直接优化策略?
- 贡献：KL奖励最优策略与Bradley–Terry偏好差分构成DPO。
- 已核验范围：`relevant_sections`；v3 §4, Appendix A.1–A.2
- 限制：有限数据、偏好假设与参数化误差限制效用。
- 权利：CC BY 4.0; 本项目独立推导和实现

## cot · [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)

Jason Wei 等，2022; v6 2023。

- 先修：自回归、任务评价
- 阅读问题：示范中间步骤能否改变解题结果?
- 贡献：报告算术、常识和符号任务中的行为改善。
- 已核验范围：`abstract_only`；abstract
- 限制：可见文字不等于内部完整因果过程; 不保证所有任务。
- 权利：论文许可见原页面; 不再分发全文

## testcompute · [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314)

Charlie Snell 等，2024。

- 先修：语言模型、搜索、评估
- 阅读问题：怎样按难度分配推理计算?
- 贡献：测试时计算策略与预算关系是研究对象。
- 已核验范围：`abstract_only`；abstract
- 限制：模型、任务、选择器和预算需一起标记。
- 权利：CC BY 4.0; 仅原创摘要性解释

## r1 · [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)

DeepSeek-AI 等，2025; v2 2026-01-04。

- 先修：预训练、策略梯度、验证器
- 阅读问题：可验证反馈怎样影响推理轨迹?
- 贡献：R1-Zero和R1的流程及奖励设计需区分。
- 已核验范围：`relevant_sections`；v2 §§2.2, 3.2 and limitations
- 限制：没有推理SFT不等于没有预训练、人类知识、设计和计算。
- 权利：许可见原论文; 此项目不复用权重/语料

## emergence · [Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004)

Rylan Schaeffer, Brando Miranda, Sanmi Koyejo，2023。

- 先修：概率、连续指标、评测
- 阅读问题：指标能否制造突变的视觉印象?
- 贡献：分析部分涌现声明中的指标与统计作用。
- 已核验范围：`abstract_only`；abstract
- 限制：不否认实际提升, 不证明一切新能力都不存在。
- 权利：仅链接与原创解释

## injection · [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)

Kai Greshake 等，2023。

- 先修：工具系统、信任边界
- 阅读问题：低信任文档怎样影响高权限应用?
- 贡献：提出并展示间接注入的系统风险。
- 已核验范围：`abstract_only`；abstract
- 限制：2023产品实例不代表2026所有产品仍同样失败。
- 权利：仅链接与原创解释, 不复现外部攻击

## ih · [IH-Challenge: A Training Dataset to Improve Instruction Hierarchy on Frontier LLMs](https://arxiv.org/abs/2603.10521)

Chuan Guo 等，2026-03-11。

- 先修：指令层级、威胁模型、评估
- 阅读问题：训练能否改善冲突下的优先级执行?
- 贡献：可评分冲突、避免过拒绝和对抗训练改善作者评测。
- 已核验范围：`relevant_sections`；§4.2 and §5.2 plus abstract
- 限制：固定模型和评测的作者报告; 高分不是一般安全证明。
- 权利：arXiv non-exclusive; 未复制数据

## biology · [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)

Jack Lindsey 等，2025-03-27。

- 先修：表征、替代模型、干预
- 阅读问题：能否识别局部语言行为的电路?
- 贡献：归因图与干预给出部分精选案例机制证据。
- 已核验范围：`relevant_sections`；Introduction, Method Overview, Limitations
- 限制：作者约四分之一尝试有满意洞见; 替代模型不完全等同原模型。
- 权利：作者技术论文; 本项目不复用图或全文

## chive · [Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments](https://arxiv.org/abs/2608.16747)

Adam Karvonen, Euan Ong, Subhash Kantamneni, Samuel Marks，2026-08-17。

- 先修：可解释性、反事实与基线
- 阅读问题：解释工具能否提高未见反事实行为预测?
- 贡献：该设置中三种激活读取工具未胜过仅看对话基线。
- 已核验范围：`relevant_sections`；§§3.2–3.3, §5
- 限制：特定工具与评价的负结果, 不是所有可解释性都无用。
- 权利：CC BY 4.0; 仅链接和原创说明

## workspace · [Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html)

Jack Lindsey 等，2026-07-06。

- 先修：表征、功能理论、干预
- 阅读问题：可言语化表征是否有特殊功能?
- 贡献：测量与干预考察局部全局工作空间功能。
- 已核验范围：`relevant_sections`；Introduction: conscious access vs subjective experience
- 限制：原文不对主观体验作判断; 本稿不据此断言意识。
- 权利：作者技术论文; 未复用图或全文

## funsearch · [Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6)

Bernardino Romera-Paredes 等，2023-12-14。

- 先修：搜索、验证、程序评价
- 阅读问题：冻结生成器加档案搜索能否改善构造?
- 贡献：报告cap-set构造与装箱启发式进展。
- 已核验范围：`relevant_sections`；abstract, FunSearch overview, evaluator/program database
- 限制：不是解决整个cap-set问题, 生成模型权重不在搜索中更新。
- 权利：Nature第三方文章, 仅链接与原创解释

## alphaevolve · [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131)

Alexander Novikov 等，2025-06-16。

- 先修：程序搜索、评估器、档案
- 阅读问题：演化编码能否得到算法改善?
- 贡献：白皮书报告多个任务, 特定4×4复矩阵48次标量乘法。
- 已核验范围：`relevant_sections`；abstract and introduction; matrix multiplication setting
- 限制：白皮书/部署报告/独立复现应区分, 非无限自我改进证据。
- 权利：白皮书许可见原文; 不复用代码

## alphafold · [Highly accurate protein structure prediction with AlphaFold](https://www.nature.com/articles/s41586-021-03819-2)

John Jumper 等，2021。

- 先修：科学盲评、结构任务
- 阅读问题：专门学习系统如何推进科学工具?
- 贡献：CASP14结构预测提供盲评证据。
- 已核验范围：`abstract_only`；abstract
- 限制：结构不等于动力学、功能、疾病或药物有效性已解决。
- 权利：原文许可见来源; 不复用数据、图或权重

## dgm · [Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954)

Jenny Zhang 等，2025; v3 2026-03-12。

- 先修：代理代码、评价、搜索
- 阅读问题：代理自身工具和代码能否改善?
- 贡献：通过候选档案与编码评测选择系统变体。
- 已核验范围：`abstract_only`；abstract
- 限制：系统代码变化不等于基础模型权重更新, 有限评测不是形式净收益证明。
- 权利：论文链接, 未复用代理代码

## mamba · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)

Albert Gu, Tri Dao，2023; v2 2024。

- 先修：线性递推、序列建模
- 阅读问题：有限状态能否选择性保留信息?
- 贡献：输入依赖选择的状态空间与高效实现。
- 已核验范围：`relevant_sections`；§3 selective state space overview
- 限制：线性时间不等于所有检索任务能力相同。
- 权利：论文链接, 本项目未复制实现

## rag · [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)

Patrick Lewis 等，2020。

- 先修：检索、概率生成
- 阅读问题：外部记忆能否补充参数知识?
- 贡献：结合参数模型与非参数文档检索。
- 已核验范围：`abstract_only`；abstract
- 限制：检索正确、文档可信、回答忠实需要分别验证。
- 权利：论文链接, 未复用检索语料

## llada · [Large Language Diffusion Models](https://arxiv.org/abs/2502.09992)

Shen Nie 等，2025。

- 先修：语言建模、去噪目标
- 阅读问题：非自回归去噪生成有哪些取舍?
- 贡献：探索大规模离散扩散语言模型。
- 已核验范围：`abstract_only`；abstract
- 限制：本稿简化遮蔽目标不是完整LLaDA算法或复现。
- 权利：论文链接, 未复用权重或实现

## latent · [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](https://arxiv.org/abs/2502.05171)

Jonas Geiping 等，2025。

- 先修：隐状态、循环、计算预算
- 阅读问题：更多隐层循环能否增加推理计算?
- 贡献：共享计算模块与循环深度作为推理预算。
- 已核验范围：`abstract_only`；abstract
- 限制：循环次数不是正确性的保证。
- 权利：论文链接, 未复用实现

## stars · [Stabilizing Recurrent Dynamics for Test-Time Scalable Latent Reasoning in Looped Language Models](https://arxiv.org/abs/2605.26733)

Xiao-Wen Yang 等，2026-05-26; ICML 2026。

- 先修：动力系统、稳定性、循环网络
- 阅读问题：怎样缓解更多循环后的表现退化?
- 贡献：以稳定性相关约束改善作者的算术与部分数学任务。
- 已核验范围：`relevant_sections`；§5 and §6, Appendix A limitations
- 限制：状态稳定不等于语义正确, 非通用架构替代证明。
- 权利：CC BY 4.0; 本稿收缩证明为独立教学推导

## nist-ci · [NIST/SEMATECH: Confidence intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)

NIST/SEMATECH 在线统计手册，2026-10-11 核验。

- 先修：有限概率、二项分布
- 阅读问题：少样本且全部成功时怎样避免零宽区间?
- 贡献：精确等尾区间的尾概率反演及数值检查。
- 已核验范围：`relevant_sections`；Exact Intervals 及 n=20, k=4, alpha=.10 算例。
- 限制：本项目只条件性地用于固定划分上的整次训练事件；不是依赖文档、NLL或新划分区间。
- 权利：仅链接与原创中文推导，不转载网页或程序。
