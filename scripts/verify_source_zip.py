#!/usr/bin/env python3
"""Clean extraction, all-PDF reconstruction, actual tests and CPU result replay."""
import argparse,hashlib,json,os,re,subprocess,sys,tempfile,zipfile
from pathlib import Path
import fitz

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pdf_content(path):
    with fitz.open(path) as pdf:
        pages=[];links=[]
        for p in pdf:
            pages.append({'text_sha256':hashlib.sha256(p.get_text().encode()).hexdigest(),'pixel_sha256':hashlib.sha256(p.get_pixmap(alpha=False).samples).hexdigest()})
            row=[]
            for a in p.get_links():
                item={'kind':a['kind'],'from':[round(v,3) for v in a['from']]}
                if a['kind']==fitz.LINK_NAMED:
                    point=pdf.resolve_link('#nameddest='+a['nameddest']);assert point and 0<=point[0]<len(pdf)
                    item.update(nameddest=a['nameddest'],page=point[0],to=[round(point[1],3),round(point[2],3)])
                elif a['kind']==fitz.LINK_GOTO:
                    assert 0<=a['page']<len(pdf);item.update(page=a['page'],to=[round(v,3) for v in a.get('to',[])])
                elif a.get('uri'):item['uri']=a['uri']
                else:raise ValueError('Unexpected PDF link')
                row.append(item)
            links.append(row)
        return {'pages':pages,'toc':pdf.get_toc(),'links':links}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);p.add_argument('--report',type=Path);p.add_argument('--include-models',action='store_true');p.add_argument('--logs-dir',type=Path);p.add_argument('--model-cache',type=Path,default=Path('/tmp/ai-hf-cache'));a=p.parse_args()
    archive=a.archive.resolve();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',HF_HUB_DISABLE_XET='1')
    with tempfile.TemporaryDirectory(prefix='ai-source-v03-rebuild-') as tmp:
        temp=Path(tmp)
        with zipfile.ZipFile(archive) as z:
            names=set()
            for member in z.infolist():
                target=(temp/member.filename).resolve()
                if member.filename in names or not target.is_relative_to(temp) or member.external_attr>>16 & 0o170000==0o120000:raise ValueError('Unsafe/duplicate ZIP member')
                names.add(member.filename)
            z.extractall(temp)
        root=temp/'ai-self-study';manifest=json.loads((root/'SOURCE-MANIFEST.json').read_text())
        for name,expected in manifest['files'].items():
            target=(root/name).resolve()
            if not target.is_relative_to(root) or sha(target)!=expected['sha256']:raise ValueError('Manifest mismatch: '+name)
        def run(args,label):
            print(json.dumps({'stage':label}),flush=True)
            result=subprocess.run(args,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            if a.logs_dir:
                a.logs_dir.mkdir(parents=True,exist_ok=True);log=a.logs_dir/(re.sub('[^a-zA-Z0-9_-]+','-',label)+'.txt');log.write_bytes(result.stdout)
            if result.returncode:raise RuntimeError(label+' failed:\n'+result.stdout.decode(errors='replace')[-7000:])
            return result
        refs=[root/'dist/ai-self-study.pdf']+sorted((root/'dist/papers').glob('*.pdf'));before={p.relative_to(root).as_posix():pdf_content(p) for p in refs}
        run(['bash','scripts/build_pdf.sh'],'rebuild textbook')
        run([sys.executable,'scripts/build_collection.py'],'rebuild all 12 research components and collections')
        for name,signature in before.items():assert signature==pdf_content(root/name),'PDF content differs: '+name
        expected=json.loads((root/'qa/v03-pdf-signatures.json').read_text())
        for name in ['dist/ai-papers-zh.pdf','dist/ai-self-study-complete.pdf']:assert expected[name]==pdf_content(root/name),'Combined PDF content/links differ: '+name
        tests=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'tests');match=re.search(rb'Ran (\d+) tests',tests.stdout);assert match
        skipped=re.search(rb'skipped=(\d+)',tests.stdout);skip=int(skipped[1]) if skipped else 0
        if a.include_models and skip:raise AssertionError('Full model validation requested but tests were skipped')
        comparisons=[]
        def result_match(cmd,result,label):
            out=temp/label;run([sys.executable]+cmd+['--out',str(out)],label);assert (root/result/'metrics.json').read_bytes()==(out/'metrics.json').read_bytes(),'Metrics differ: '+label;comparisons.append(label)
        result_match(['experiments/run_all.py'],'results','original seven')
        for name,extra in [('attention_walkthrough',[]),('residual_debug',['--seed','19']),('micro_research',[])]:result_match(['experiments/run_all.py','--experiment',name]+extra,'results/'+name,name)
        for key in ['foundations','networks','language','research']:result_match(['experiments/v03_'+key+'.py'],'results/v03-'+key,'v03-'+key)
        result_match(['experiments/research_bridges.py'],'results/research-bridges-v03','research-bridges-v03')
        if a.include_models:
            result_match(['experiments/standard_transformer_study.py'],'results/standard-transformer-v03','standard-transformer-v03')
            result_match(['experiments/public_model_diagnostics.py','--cache',str(a.model_cache.resolve())],'results/public-models-v03','public-models-v03 cached only')
        generated={p.relative_to(root):p.read_bytes() for p in (root/'book/generated').glob('v0*.tex')}
        generated[Path('research/micro-study-v02.md')]=(root/'research/micro-study-v02.md').read_bytes()
        run([sys.executable,'scripts/write_v02_results.py'],'regenerate v02 numeric fragments')
        run([sys.executable,'scripts/write_v03_results.py'],'regenerate v03 numeric fragments')
        assert all((root/k).read_bytes()==v for k,v in generated.items()),'Numeric fragment differs'
        report={'status':'PASS','release':manifest['release'],'archive_sha256':sha(archive),'manifest_files':len(manifest['files']),'all_component_pdfs':len(refs),'component_text_pixels_toc_links_identical':True,'collection_text_pixels_toc_links_identical':True,'pages':{'book':len(before['dist/ai-self-study.pdf']['pages']),'papers':len(expected['dist/ai-papers-zh.pdf']['pages']),'complete':len(expected['dist/ai-self-study-complete.pdf']['pages'])},'tests_run':int(match[1]),'tests_skipped':skip,'actual_metrics_byte_comparisons':comparisons,'model_runs_included':a.include_models,'model_downloads':False,'numeric_fragments_regenerated_identically':True,'scope':'Fresh extraction; same recorded fonts/TeX, Python/NumPy/Torch and recorded script-specific CPU thread settings. PDF time/IDs may differ; content pixels/text/bookmarks/links compared. No code inside translated papers executed.'}
    if a.report:a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
