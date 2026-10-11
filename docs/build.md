# 构建与干净目录复现

正文采用用户指定的 `math-latex-typesetting` 固定模板。使用 XeLaTeX，禁止 shell escape。`scripts/build_pdf.sh` 连续编译三轮，使目录与交叉引用收敛；输出 `dist/ai-self-study.pdf`。

依赖：TeX Live（XeTeX、ctex、Fandol、amsmath、amsthm、xurl、geometry、setspace、fancyhdr、enumitem、needspace、booktabs、graphicx、longtable、hyperref）和 Computer Modern Unicode。常见 Debian 系统可由管理员安装 `texlive-xetex texlive-lang-chinese texlive-latex-extra fonts-cmu`；其他系统用对应 TeX Live/MiKTeX 包管理器。项目不静默替换字体。

本次环境已有 XeLaTeX 2024/2025 系统包，ctex/Fandol/CMU 位于独立 TeX 用户树 `/workspace/.local/texmf`。构建时显式指定 `TEXMFHOME` 与 `OSFONTDIR`，仅使用现成环境，没有修改系统或 MIT 工作区。该路径不是源码的硬编码依赖。

```bash
# 标准完整 TeX 安装
bash scripts/build_pdf.sh

# 若字体和宏包位于自定义用户树，按本机路径配置
TEXMFHOME=/path/to/texmf OSFONTDIR=/path/to/texmf/fonts/opentype bash scripts/build_pdf.sh
```

`book/generated/` 已包含来自首版实际结果的三个矢量图与数值片段；v0.2片段由 `python scripts/write_v02_results.py` 从新增结果JSON生成。因此仅编译 PDF 无需安装 NumPy 或下载资料。若重新运行实验并更新图，需要 NumPy、Matplotlib；最终交付 PDF 和章节、图、JSON 的哈希在 `qa/delivery.json` 中绑定。

源码 ZIP 的干净重编译：

```bash
mkdir /tmp/ai-rebuild
python -m zipfile -e dist/ai-self-study-source.zip /tmp/ai-rebuild
cd /tmp/ai-rebuild/ai-self-study
bash scripts/build_pdf.sh
python -m unittest discover -s tests -v
```

同一内容多次编译 PDF 的时间戳、内部对象ID等元数据可能不同，不能仅以 PDF 二进制哈希是否相同判断内容一致。本项目比较页数、逐页抽取文本和渲染像素；链接也独立核对。

安装 `requirements-build.txt` 后，可以执行完整归档验证；自定义TeX环境仍按上文配置：

```bash
python scripts/package_source.py
python scripts/verify_source_zip.py dist/ai-self-study-source.zip --report /tmp/ai-zip-rebuild.json
```

源码包采用显式文件清单，包含PDF、LaTeX、原创图、代码、实际结果、文献账本与许可证；不包含Git配置、虚拟环境、字体、第三方全文或渲染缓存。内含 `SOURCE-MANIFEST.json`，验证器先核对每个文件哈希，再在临时目录重编译、检查文本/像素/书签/链接，并重跑13项测试、原七项实验及三个v0.2入口（微研究含15次训练）。测试目录会自动清理；同一环境下要求实验JSON完全一致，跨平台浮点一致性应另行设容差。

`qa/` 分别记录自动检查、未参与写作的 AI 读者检查和视觉审查。使用的固定模板 skill 检查器已运行；另一 PDF skill 的独立 `tex_preflight.py` 附件未在当前可用资源中找到，以项目预检、XeLaTeX 日志和 PDF 审核完成对应检查，不虚报运行缺失脚本。
