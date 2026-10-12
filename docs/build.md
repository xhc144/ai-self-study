# 构建教材、论文和源码包

正文、公式、表格、算法和长示例为可编辑文本。授权原作者图保留数据；图中文字另附中文说明。构建不执行论文内代码，也不需要下载原英文全文。

需要 XeLaTeX、ctex、fontspec、amsmath/amsthm、booktabs、longtable、fvextra、tabularx、TikZ、hyperref/xurl，以及 Fandol 和 Computer Modern Unicode 字体。推荐完整 TeX Live；字体由本机提供，源码不捆绑。Python 3.12及构建依赖：

```bash
python -m pip install -r requirements-build.txt
bash scripts/build_pdf.sh
python scripts/build_collection.py
python -m scripts.write_release_index
```

第一条生成教材 `dist/ai-self-study.pdf`；第二条为三份研究说明和九篇论文各编译三遍，生成论文资料与完整合订本。第三条从正式组件生成准确页码索引并合订。每篇输入在 `book/` 工作目录解析；脚本生成的独立LaTeX主文件也包含在源码中。默认关闭shell escape。

交付机器使用 XeTeX 0.999996/TeX Live 2025-dev（Debian），额外TeX包和字体在本机TEXMF树。复核时环境为：

```bash
export TEXMFHOME=/workspace/.local/texmf
export OSFONTDIR=/workspace/.local/texmf/fonts/opentype
export XDG_CACHE_HOME=/tmp/ai-cache
```

这三条只描述本次机器；在读者机器上应指向实际字体/TeX安装，或使用其系统默认路径。不是要求创建相同私有目录。固定模板的类区域保持原金标准，附加论文工具在类外加载。

打包及干净重编译：

```bash
python scripts/package_source.py
python scripts/verify_source_zip.py dist/ai-self-study-source.zip --report /tmp/source-check.json
```

源码ZIP含所有编辑源码、授权图件、实际结果及教材/各组件参考PDF。两个较大的合订PDF由组件重建，不重复塞进ZIP。校验器比较全部组件的文本/逐页像素/书签/链接，以及合订本的全部链接；同一记录的环境与脚本线程设置下重新跑基础和新增NumPy实验。安装可选CPU依赖后，还重新训练六次标准Transformer并对已有模型缓存复跑54条公开诊断；不自动下载模型。纯NumPy环境会报告可选项未执行，不能称为全部模型复现。

`qa/v03-reproducibility.json`和`dist/ai-self-study-source-check.json`是对已冻结ZIP的闭环证据，位于仓库旁证，避免把含ZIP自身哈希的报告递归打包。PDF二进制中的日期可能不同；验收比较实际文本、栅格像素、书签和链接，而不是要求PDF文件时间字段相同。结果JSON只在记录的依赖、硬件和线程范围内承诺本次逐字节一致。
