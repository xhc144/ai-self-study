#!/usr/bin/env python3
"""Mechanical delivery audit. Never claims mathematical or visual review."""
import hashlib,json,re
from pathlib import Path
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    pdf=ROOT/'dist/ai-self-study.pdf';doc=fitz.open(pdf)
    errors=[];external=set();internal=0;pages=[]
    out=ROOT/'qa/render';out.mkdir(parents=True,exist_ok=True)
    for pattern in ['page-*.png','pair-*.png']:
        for stale in out.glob(pattern):stale.unlink()
    for i,p in enumerate(doc):
        if abs(p.rect.width-612)>.1 or abs(p.rect.height-792)>.1:errors.append(f'page size {i+1}')
        text=p.get_text()
        if not text.strip():errors.append(f'blank page {i+1}')
        for l in p.get_links():
            if l['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and 'page' in l:
                internal+=1
                if not 0<=l['page']<len(doc):errors.append(f'link target page {i+1}')
            elif l.get('uri'):
                external.add(l['uri'])
                if not l['uri'].startswith('https://'):errors.append(f'nonhttps {l["uri"]}')
        for b in p.get_text('blocks'):
            if b[0]<-.5 or b[1]<-.5 or b[2]>p.rect.width+.5 or b[3]>p.rect.height+.5:
                errors.append(f'text outside paper page {i+1}')
        png=out/f'page-{i+1:03d}.png';p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(png)
        pages.append({'page':i+1,'render':png.relative_to(ROOT).as_posix(),'render_sha256':sha(png),
            'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
    for k in range(0,len(doc),2):
        ims=[Image.open(out/f'page-{i+1:03d}.png').convert('RGB') for i in range(k,min(k+2,len(doc)))]
        combined=Image.new('RGB',(sum(x.width for x in ims),max(x.height for x in ims)+30),'white')
        xx=0;draw=ImageDraw.Draw(combined)
        for i,im in enumerate(ims):combined.paste(im,(xx,30));draw.text((xx+20,8),f'Page {k+i+1}',fill='black');xx+=im.width
        combined.save(out/f'pair-{k+1:03d}.png')
    # Final log, not first-pass transient citation warnings.
    log=ROOT/'book/build/main.log'
    if log.exists():
        t=log.read_text(errors='replace')
        for token in ['Missing character:','Overfull \\hbox','Overfull \\vbox','There were undefined references','! LaTeX Error']:
            if token in t:errors.append(f'compile log: {token}')
    sources=sorted(p for folder in ['book/chapters','book/generated','experiments','scripts','tests','research','results']
                   for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)+[ROOT/'book/main.tex',ROOT/'book/references.tex',ROOT/'docs/sources.json',ROOT/'results/metrics.json']
    source_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in sources}
    privacy=[]
    patterns=[r'[A-Za-z0-9._%+-]+@qq\.com',r'ghu_[A-Za-z0-9]{20,}']
    for p in ROOT.rglob('*'):
        if not p.is_file() or any(a in p.parts for a in ['.git','build','render','__pycache__']):continue
        if p.suffix in ['.md','.tex','.py','.json','.txt'] or p.name in ['LICENSE','README.md']:
            # Audit's own literal detection patterns must not count as disclosed data.
            if p.name=='audit_delivery.py':continue
            text=p.read_text(errors='replace')
            if any(re.search(pat,text) for pat in patterns):privacy.append(p.relative_to(ROOT).as_posix())
    if privacy:errors.append('privacy pattern matches: '+', '.join(privacy))
    report={'pdf_sha256':sha(pdf),'pages':len(doc),'toc_entries':len(doc.get_toc()),
        'internal_links':internal,'external_links':sorted(external),'page_records':pages,
        'source_hashes':source_hashes,'errors':errors,'mechanical_status':'PASS' if not errors else 'FAIL',
        'mathematical_verification':False,'visual_review':'not_performed_by_script'}
    (ROOT/'qa/delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['pages','toc_entries','internal_links','errors','mechanical_status']},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
