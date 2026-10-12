#!/usr/bin/env python3
"""Build editable LaTeX components and assemble their vector PDFs, preserving links."""
import argparse,os,subprocess,json
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
PAPERS={'dpo':'直接偏好优化','testcompute':'最优测试时计算','r1-nature':'DeepSeek-R1 Nature 正式论文','chive':'用反事实检验解释','dgm':'达尔文哥德尔机','stars':'循环动力学稳定性','alphaproof':'奥林匹克形式数学推理','engram':'条件记忆与稀疏查找','cat':'以计算作为教师'}
STUDIES={'ih-challenge':'指令层级研究说明','browser-injection':'浏览器注入研究说明','r1-reading':'R1 比较阅读说明'}

def run_tex(name,body,title):
    book=ROOT/'book';preamble=(book/'main.tex').read_text().split('\\begin{document}',1)[0]
    preamble=preamble[:preamble.index('\\hypersetup{pdftitle=')]
    preamble+='\\makeatletter\n\\newcommand{\\paperlabel}[2]{\\def\\@currentlabel{#1}\\label{#2}}\n\\makeatother\n\\usepackage{fvextra,tabularx,array,tikz}\n\\usetikzlibrary{arrows.meta,positioning,calc}\n\\renewcommand{\\figurename}{图}\n\\renewcommand{\\tablename}{表}\n'
    wrapper=preamble+'\\hypersetup{pdftitle={'+title+'},pdfauthor={ai-self-study contributors}}\n\\begin{document}\n\\mainmatter\n\\begin{center}{\\color{structurecolor}\\bfseries\\fontsize{18}{24}\\selectfont '+title+'}\\par\n非官方中文研究资料 · 0.3 · 来源与许可逐篇注明\\end{center}\n\\originalcontents\n\\clearpage\n'+body+'\n\\end{document}\n'
    source=book/(name+'.tex');source.write_text(wrapper)
    build=book/'build'/name;build.mkdir(parents=True,exist_ok=True)
    for turn in [1,2,3]:
        log=build/f'pass-{turn}.stdout'
        with log.open('w') as stream:
            result=subprocess.run(['xelatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode','-output-directory='+str(build),source.name],cwd=book,stdout=stream,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError(f'{name} build failed, see {log}')
    target=ROOT/'dist/papers'/(name+'.pdf');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((build/(name+'.pdf')).read_bytes())
    print(json.dumps({'built':name,'pages':len(fitz.open(target))}),flush=True)
    return target

def merge(paths,target,title):
    out=fitz.open();toc=[]
    for name,path in paths:
        src=fitz.open(path);offset=len(out);out.insert_pdf(src,links=False)
        for i,page in enumerate(src):
            for link in page.get_links():
                record={'from':link['from']}
                if link['kind']==fitz.LINK_NAMED:
                    destination=src.resolve_link('#nameddest='+link['nameddest'])
                    if not destination or not 0<=destination[0]<len(src):raise ValueError('Unresolved source named link: '+link['nameddest'])
                    record.update(kind=fitz.LINK_GOTO,page=destination[0]+offset,to=fitz.Point(destination[1],destination[2]))
                elif link['kind']==fitz.LINK_GOTO:
                    record.update(kind=fitz.LINK_GOTO,page=link['page']+offset,to=link.get('to',fitz.Point(0,0)))
                elif link['kind']==fitz.LINK_URI:record.update(kind=fitz.LINK_URI,uri=link['uri'])
                else:raise ValueError('Unexpected source link kind '+str(link['kind']))
                out[offset+i].insert_link(record)
        toc.append([1,name,offset+1])
        for level,text,page in src.get_toc():toc.append([level+1,text,page+offset])
        src.close()
    out.set_toc(toc);out.set_metadata({'title':title,'author':'ai-self-study contributors','subject':'Editable LaTeX sources; individually attributed research materials'})
    out.save(target,garbage=4,deflate=True);out.close()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--names',default=','.join(PAPERS));parser.add_argument('--studies-only',action='store_true');args=parser.parse_args()
    paths=[]
    for key,title in STUDIES.items():
        text=(ROOT/'papers/studies'/(key+'.tex')).read_text();wanted={k for group in __import__('re').findall(r'\\cite\{([^}]+)\}',text) for k in group.split(',')};refs='\\begin{thebibliography}{99}\n'+'\n'.join(line for line in (ROOT/'book/references.tex').read_text().splitlines() if any(line.startswith('\\bibitem{'+k+'}') for k in wanted))+'\n\\end{thebibliography}';path=run_tex('study-'+key,'\\input{../papers/studies/'+key+'.tex}\n'+refs,title);paths.append((title,path))
    study=ROOT/'dist/ai-research-studies-zh.pdf';merge(paths,study,'现代AI原创研究说明')
    if args.studies_only:return
    for key in args.names.split(','):
        title=PAPERS[key];path=run_tex(key,'\\input{../papers/translations/'+key+'/body.tex}',title);paths.append((title,path))
    merge(paths,ROOT/'dist/ai-papers-zh.pdf','现代AI中文论文研究资料')
    merge([('现代人工智能研究学习教材',ROOT/'dist/ai-self-study.pdf'),('中文论文与原创研究说明',ROOT/'dist/ai-papers-zh.pdf')],ROOT/'dist/ai-self-study-complete.pdf','现代人工智能研究学习合订本')
    print(json.dumps({'collection_pages':len(fitz.open(ROOT/'dist/ai-papers-zh.pdf')),'complete_pages':len(fitz.open(ROOT/'dist/ai-self-study-complete.pdf'))}),flush=True)
if __name__=='__main__':main()
