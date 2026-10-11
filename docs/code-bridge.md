# 从公式到 NumPy：TinyDecoder

先读教材4章矩阵梯度、6章广播/共享路径、7章数值闭环与故障练习，再对照 [run_all.py](../experiments/run_all.py) 的 `TinyDecoder.forward/loss_grad`。模型单头单块、tanh FFN、有两次残差，没有归一化；不是标准大模型完整实现。

B=文档数，T=输入位置数，D=特征数，V0=词表大小。首个语言实验为B=6、T=7、D=16、V0=10，研究测试B2。批次、位置、词编号采用Python零起下标；编号1指数组第二行。`ids` 是整数编号，`target` 是向左移一位的正确下一个token。

|数学对象/运算|变量|形状|代码|
|---|---|---|---|
|查表+共享位置|x|B,T,D|`p['E'][ids]+p['P'][:T]`|
|Q/K/V投影|q/k/v|B,T,D|`x@p[n]`|
|按批次收缩特征|s|B,T,T|`q@k.transpose(0,2,1)/sqrt(D)`|
|下三角允许j≤i|mask|T,T（广播B）|`np.where(mask,s,-np.inf)`|
|逐查询归一化|a|B,T,T|`softmax(s)`（最后轴）|
|检索值|c|B,T,D|`a@v`|
|投影与注意力残差|h|B,T,D|`x+c@p['O']`|
|非线性前馈|f|B,T,2D|`tanh(h@p['F']+p['bF'])`|
|前馈残差|z|B,T,D|`h+f@p['G']+p['bG']`|
|分类分数|logits|B,T,V0|`z@p['U']+p['bU']`|
|平均交叉熵系数|dl|B,T,V0|`(softmax-one_hot)/(B*T)`|
|所有使用位置的权重梯度|g['U']|D,V0|`mm(z,dl)`|
|共享偏置梯度|g['bU']|V0|`dl.sum(axis=(0,1))`|
|两残差路径累加|dh/dx|B,T,D|`dh=dz+df@F.T`; `dx=dh+dq@Q.T+dk@K.T+dv@V.T`|
|重复词的参数路径累加|g['E']|V0,D|`np.add.at(g['E'],ids,dx)`|
|跨文档共享的位置梯度|g['P']|context,D|`g['P'][:T]=dx.sum(0)`|

`transpose(0,2,1)` 只交换位置和特征轴，保留批次；三维 `.T` 会反转全部轴。`@` 在最后两个轴作乘法、在前轴匹配或广播。

`mm(x,y)` 把B,T展平成BT行：`x.reshape(-1,x.shape[-1]).T @ y.reshape(-1,y.shape[-1])`。这是在收集共享矩阵的梯度，激活梯度保留B,T；展平本身既不平均也不求和。CE已经平均一次，后面不能再除B或BT。

Frobenius梯度由 `dℓ = sum_ij G_ij dW_ij` 决定，和W同形。先写独立坐标的系数，再整理成矩阵乘法，就能推出转置方向。

可运行练习：

```bash
python experiments/run_all.py --experiment attention_walkthrough --out /tmp/my-attention
python experiments/run_all.py --experiment residual_debug --seed 19 --out /tmp/my-residual
```

第二项前向完全一致，只漏attention残差直接dh。先预测失败参数组，运行后检查206坐标误差，答案是词表E和位置P；修复后上游共享路径恢复。默认故障实验不会训练错误模型或混入正常研究结果。
