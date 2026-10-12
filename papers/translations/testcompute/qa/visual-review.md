# 译者单篇版面检查

临时 wrapper 使用根 book/main.tex 的固定适配类，仅设置 graphicx、booktabs、longtable 并 input 本篇 body.tex。工作目录 book，输出全部在 /tmp/testcompute-v1/build。没有修改根模板或其他论文。

42 页全部渲染，逐页打开正文版面检查了中文、数学式、长公式、图注、原图、书目、截图转写、列表和跨页。实际观察并修复：长论文题名在页眉与节名重叠；ReST^EM 页眉上标造成 headheight 警告；三个空白步骤的方括号被 enumerate 解释为自定义列表标签、文字跑出纸外。修复均只涉及本篇内容写法，固定模板不变。

最终修复后 42 页重新渲染。最后一步仅将参考书目后的页眉恢复为短论文题名，随后复看第 1–6 页及第 19、20、25、31、39、40 页。最终 PDF 的公式、列表、图注与图件完整，图中文字较小的原截图同时具备逐句中文正文转写，全部模型错误和 PRM 得分都保留。末页短是原示意图文字对照的自然结束，未添填充内容。

最后日志：0 Overfull，0 missing character，0 undefined reference/citation，0 headheight warning，0 纸外文字 span。仍有固定模板 FandolSong 中文斜体回退正体提醒；没有缺字，未改模板字体。长表一处 Underfull 提醒经过实际页检查，无溢出或裁切。

本检查为译者检查；根代理仍需独立构建并审查正式单篇和合订成品。证据摘要与页图哈希见 translation-audit.json 和 qa/local-render.json，具体日志 qa/compile-final.log。
