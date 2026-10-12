#!/usr/bin/env python3
"""Bind learner-facing version/page maps to the actual final component PDFs."""
import json,hashlib
from pathlib import Path
import fitz
from scripts.build_collection import PAPERS,STUDIES,merge,ROOT
VERSIONS={'dpo':'2305.18290v3 · 2024-07-29','testcompute':'2408.03314v1 · 2024-08-06','r1-nature':'Nature · 2025-09-17','chive':'2608.16747v1 · 2026-08-17','dgm':'2505.22954v3 · 2026-03-12','stars':'2605.26733v1 · 2026-05-26','alphaproof':'Nature VOR · 2026-03-13','engram':'2601.07372v2 · 2026-07-12','cat':'2509.14234v3 · 2026-05-09'}
BRIDGES={'dpo':'教材7：KL最优策略→偏好似然→梯度','testcompute':'教材8：验证器、难度与并行/顺序预算','r1-nature':'教材7–8：RLVR与实际证据；配原创R1说明','chive':'教材10：解释→反事实预测→干预证据','dgm':'教材11：代码更新、档案搜索、评估器投机','stars':'教材11：稳定性、有效性与局部理论条件','alphaproof':'教材11：AND/OR搜索、形式核验与题意对应','engram':'教材11：查表梯度、容量/计算/存储分配','cat':'教材8/11：伪参考、相关错误与监督闭环'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    paths=[(title,ROOT/'dist/papers'/('study-'+key+'.pdf')) for key,title in STUDIES.items()]+[(title,ROOT/'dist/papers'/(key+'.pdf')) for key,title in PAPERS.items()]
    merge(paths,ROOT/'dist/ai-papers-zh.pdf','现代AI中文论文研究资料')
    merge([('现代人工智能研究学习教材',ROOT/'dist/ai-self-study.pdf'),('中文论文与原创研究说明',ROOT/'dist/ai-papers-zh.pdf')],ROOT/'dist/ai-self-study-complete.pdf','现代人工智能研究学习合订本')
    book_pages=len(fitz.open(ROOT/'dist/ai-self-study.pdf'));offset=0;mapping=[]
    for (title,path),key in zip(paths,['study-'+x for x in STUDIES]+list(PAPERS)):
        with fitz.open(path) as d:pages=len(d)
        mapping.append({'id':key,'title':title,'pdf':path.relative_to(ROOT).as_posix(),'component_pages':pages,'collection_pages':[offset+1,offset+pages],'complete_pages':[book_pages+offset+1,book_pages+offset+pages],'sha256':sha(path)})
        offset+=pages
    text='# 中文论文研究资料\n\n按问题读材料：DPO→R1→Snell→CaT讨论反馈与预算，Engram讨论容量与计算，CHIVE讨论机制证据，DGM→AlphaProof讨论研究闭环，STARS讨论循环计算的稳定性。每篇配版本、许可、逐节覆盖与核查记录。\n\n'
    text+='## 指定版本全文译文\n\n均为CC BY4.0机器辅助非官方译文；完整指指定版本本体及其中包含的附录，原英文书目保留，原图内标签附中文解释。未声称人工专家校订。\n\n| 资料/版本 | PDF/源码 | 学习入口 |\n|---|---|---|\n'
    for key,title in PAPERS.items():
        row=next(x for x in mapping if x['id']==key);n=row['component_pages']
        text+=f'| {title}；{VERSIONS[key]} | [PDF（{n}页）](../dist/papers/{key}.pdf) · [LaTeX](translations/{key}/body.tex) · [覆盖](translations/{key}/coverage.json) | {BRIDGES[key]} |\n'
    text+='\nR1 Nature的独立83页Supplementary与AlphaProof的独立9页Supplementary/伪代码ZIP未确认单独再分发许可，未镜像，未纳入“全文”完成范围；原文仍保留指向附件的引用。Nature许可不借给不同arXiv版本。\n\n## 原创研究说明\n\n'
    for key,title in STUDIES.items():text+=f'- [{title}](../dist/papers/study-{key}.pdf) · [可编辑源码](studies/{key}.tex)：原创问题、数学、实际CPU机制和练习；不是未许可原文的全文译本。\n'
    text+='\n## 三项重点来源的定位\n\n| 原始研究来源 | 教材 | 本项目资料/论文资料页码 |\n|---|---|---|\n'
    text+='| [OpenAI IH-Challenge官方说明](https://openai.com/index/instruction-hierarchy-challenge/)（2026-03-10）及v1论文 | 第9章，55–61页 | `studies/ih-challenge.tex`；研究说明PDF4页；论文资料1–4页 |\n'
    text+='| [Anthropic浏览器注入防御](https://www.anthropic.com/research/prompt-injection-defenses)（2025-11-24） | 第9章，55–61页 | `studies/browser-injection.tex`；研究说明PDF4页；论文资料5–8页 |\n'
    r1=next(x for x in mapping if x['id']=='r1-nature');text+=f'| [R1 Nature正式论文](https://www.nature.com/articles/s41586-025-09422-z)（2025-09-17） | 第7–8章，44–54页 | `translations/r1-nature/body.tex`；正式译文18页；论文资料{r1["collection_pages"][0]}–{r1["collection_pages"][1]}页；另有原创R1说明9–11页 |\n'
    text+='\n## 全部组件实际页码\n\n| 组件 | 独立PDF页数 | 论文资料PDF | 合订本PDF |\n|---|---:|---|---|\n'
    for a in mapping:text+=f'| {a["title"]} | {a["component_pages"]} | {a["collection_pages"][0]}–{a["collection_pages"][1]} | {a["complete_pages"][0]}–{a["complete_pages"][1]} |\n'
    text+='\n[合订资料PDF](../dist/ai-papers-zh.pdf) · [教材与资料完整合订PDF](../dist/ai-self-study-complete.pdf) · [机器可读页码](page-map.json) · [许可判定](LICENSE-DECISIONS.md)。源代码的相对输入以 `book/` 为工作目录，统一构建见[构建说明](../docs/build.md)。\n'
    (ROOT/'papers/README.md').write_text(text);(ROOT/'papers/page-map.json').write_text(json.dumps({'release':'0.3.0','book_pages':book_pages,'paper_collection_pages':offset,'complete_pages':book_pages+offset,'components':mapping},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'book':book_pages,'papers':offset,'complete':book_pages+offset,'components':len(mapping)}))
if __name__=='__main__':main()
