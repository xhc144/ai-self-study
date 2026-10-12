from pathlib import Path, PurePosixPath
import json,hashlib,os,re,stat,subprocess,sys,tempfile,zipfile
import fitz
WORK=Path('/workspace/ai-self-study');ARCHIVE=WORK/'dist/ai-self-study-source.zip';BASE=Path('/tmp/ai-self-study-v03-public-clone');LOGS=WORK/'qa/reproduction-logs-v031';REPORT=WORK/'qa/v031-reproducibility.json'
EXPECTED='2afd163dc3684d3a8b720fa7b0967943ffe1e1dae53ac16f9e76f89541f30383';OLD='8633d6bc81e57e7675e2840b693c5fb16b2c632746a5a294fa319d73a0094f84'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(label,data):
    print(json.dumps({'stage':label,'evidence':data},ensure_ascii=False),flush=True)
    target=LOGS/('fresh-'+label+'.txt');assert not target.exists(),'Would overwrite '+str(target)
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def signature(path):
    with fitz.open(path) as pdf:
        pages=[];links=[]
        for p in pdf:
            pages.append({'text_sha256':hashlib.sha256(p.get_text().encode()).hexdigest(),'pixel_sha256':hashlib.sha256(p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples).hexdigest()})
            row=[]
            for a in p.get_links():
                item={'kind':a['kind'],'from':[round(v,3) for v in a['from']]}
                if a['kind']==fitz.LINK_NAMED:
                    point=pdf.resolve_link('#nameddest='+a['nameddest']);assert point and 0<=point[0]<len(pdf)
                    item.update(nameddest=a['nameddest'],page=point[0],to=[round(point[1],3),round(point[2],3)])
                elif a['kind']==fitz.LINK_GOTO:
                    assert 0<=a['page']<len(pdf);item.update(page=a['page'],to=[round(v,3) for v in a.get('to',[])])
                elif a['kind']==fitz.LINK_URI:item['uri']=a['uri']
                else:raise ValueError('Unexpected link kind')
                if 'page' in item:
                    x,y=item['to'];assert -.01<=x<=pdf[item['page']].rect.width+.01 and -.01<=y<=pdf[item['page']].rect.height+.01
                row.append(item)
            links.append(row)
        return {'pages':pages,'toc':pdf.get_toc(),'links':links}
def sizes(path):
    with fitz.open(path) as pdf:return [list(p.rect) for p in pdf]
def protected(name):return name.startswith(('experiments/','results/','tests/')) or name.startswith('research/design-')
def record(root,name):
    p=root/name;return {'sha256':sha(p),'size_bytes':p.stat().st_size}
LOGS.mkdir(parents=True,exist_ok=True)
assert sha(ARCHIVE)==EXPECTED and ARCHIVE.stat().st_size==58743118
with tempfile.TemporaryDirectory(prefix='ai-source-v031-delta-') as temp_name:
    temp=Path(temp_name)
    with zipfile.ZipFile(ARCHIVE) as z:
        names=set()
        for member in z.infolist():
            name=member.filename;target=(temp/name).resolve();mode=member.external_attr>>16
            assert name not in names and target.is_relative_to(temp) and not PurePosixPath(name).is_absolute() and '\\' not in name and not member.flag_bits&1
            assert stat.S_IFMT(mode) in [0,stat.S_IFREG] and not member.is_dir()
            names.add(name)
        z.extractall(temp)
    root=temp/'ai-self-study';manifest=json.loads((root/'SOURCE-MANIFEST.json').read_text());files=manifest['files']
    assert manifest['release']=='0.3.1' and len(files)==478
    assert names=={'ai-self-study/'+n for n in files}|{'ai-self-study/SOURCE-MANIFEST.json'}
    for name,expected in files.items():
        p=(root/name).resolve();assert p.is_relative_to(root) and record(root,name)==expected,'Manifest SHA/size mismatch '+name
    emit('manifest',{'archive_sha256':EXPECTED,'archive_bytes':58743118,'manifest_files':len(files),'all_file_sha_and_size_valid':True,'no_unlisted_zip_members':True,'safe_fresh_extraction':True})
    old=json.loads((BASE/'dist/source-manifest.json').read_text())['files'];prior=json.loads((BASE/'qa/v03-reproducibility.json').read_text())
    assert sha(BASE/'dist/ai-self-study-source.zip')==OLD
    assert prior['status']=='PASS' and prior['archive_sha256']==OLD and prior['tests_run']==58 and prior['tests_skipped']==0 and len(prior['actual_metrics_byte_comparisons'])==11 and prior['model_runs_included']
    protected_names=sorted(n for n in files if protected(n));assert set(protected_names)=={n for n in old if protected(n)}
    frozen=[]
    for name in protected_names:
        assert files[name]==old[name] and record(BASE,name)==old[name] and record(root,name)==old[name],name
        frozen.append({'path':name,**old[name]})
    common=['book/main.tex','book/references.tex','scripts/build_collection.py']
    for name in common:assert files[name]==old[name] and record(BASE,name)==old[name]
    unchanged=['study-browser-injection','study-r1-reading','testcompute','chive','dgm','stars','alphaproof','cat']
    changed=['textbook','study-ih-challenge','dpo','r1-nature','engram'];dependency_checks=[];exclusions=[]
    for key in unchanged:
        pdf='dist/papers/'+key+'.pdf';assert files[pdf]==old[pdf] and record(BASE,pdf)==old[pdf]
        wrapper='book/'+key+'.tex';assert files[wrapper]==old[wrapper] and record(BASE,wrapper)==old[wrapper]
        prefix='papers/studies/'+key.removeprefix('study-')+'.tex' if key.startswith('study-') else 'papers/translations/'+key+'/'
        actual={n for n in files if n==prefix or n.startswith(prefix)};previous={n for n in old if n==prefix or n.startswith(prefix)}
        allowed=lambda n:Path(n).name in ['metadata.json','coverage.json'] or 'snapshot' in Path(n).name.lower()
        deps=sorted(n for n in actual|previous if not allowed(n));assert {n for n in actual if not allowed(n)}=={n for n in previous if not allowed(n)}
        for name in deps:assert files[name]==old[name] and record(BASE,name)==old[name],name
        for name in sorted(actual|previous):
            if allowed(name) and files.get(name)!=old.get(name):exclusions.append({'component':key,'path':name,'old':old.get(name),'new':files.get(name),'reason':'metadata/coverage/snapshot, not compiled body/asset'})
        dependency_checks.append({'component':key,'pdf_sha256':files[pdf]['sha256'],'wrapper_sha256':files[wrapper]['sha256'],'compiled_dependency_files_identical':deps})
    for key in changed:
        name='dist/ai-self-study.pdf' if key=='textbook' else 'dist/papers/'+key+'.pdf';assert files[name]['sha256']!=old[name]['sha256'],'Claimed changed PDF not changed '+key
    emit('bind-prior-evidence',{'prior_archive_sha256':OLD,'prior_report_sha256':sha(BASE/'qa/v03-reproducibility.json'),'prior_full_replay_classes':prior['actual_metrics_byte_comparisons'],'frozen_experiment_result_test_design_files_identical':len(frozen),'changed_components':changed,'unchanged_components':unchanged,'unchanged_component_dependency_checks':dependency_checks,'noncompiled_disclosure_exclusions':exclusions,'common_build_dependency_files_unchanged':common})
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',HF_HUB_DISABLE_XET='1',TEXMFHOME='/workspace/.local/texmf',OSFONTDIR='/workspace/.local/texmf/fonts/opentype',XDG_CACHE_HOME='/tmp/ai-cache')
    commands=[]
    def run(args,label):
        print(json.dumps({'stage':label,'command':args}),flush=True)
        log=LOGS/('fresh-'+label+'.txt');assert not log.exists(),'Would overwrite '+str(log)
        result=subprocess.run(args,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log.write_bytes(result.stdout)
        commands.append({'label':label,'argv':args,'cwd':'fresh extracted ai-self-study','returncode':result.returncode,'log':log.relative_to(WORK).as_posix()})
        assert result.returncode==0,label+' failed '+result.stdout.decode(errors='replace')[-6000:]
        return result.stdout
    audit=temp/'fresh-public-input-audit.json';run([sys.executable,'scripts/audit_public_model_inputs.py','--out',str(audit)],'input-audit')
    assert audit.read_bytes()==(root/'research/public-model-input-audit-v03.json').read_bytes()
    audit_result=json.loads(audit.read_text())
    tests=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'tests');count=re.search(rb'Ran (\d+) tests',tests);skip=re.search(rb'skipped=(\d+)',tests)
    assert count and int(count[1])==58 and (int(skip[1]) if skip else 0)==0
    refs=[root/'dist/ai-self-study.pdf']+sorted((root/'dist/papers').glob('*.pdf'));assert len(refs)==13
    before={p.relative_to(root).as_posix():signature(p) for p in refs};before_sizes={p.relative_to(root).as_posix():sizes(p) for p in refs};expected=json.loads((root/'qa/v03-pdf-signatures.json').read_text())
    run(['bash','scripts/build_pdf.sh'],'rebuild-textbook')
    ih="from scripts.build_collection import ROOT,STUDIES,run_tex; import re; text=(ROOT/'papers/studies/ih-challenge.tex').read_text(); wanted={k for group in re.findall(r'\\\\cite\\{([^}]+)\\}',text) for k in group.split(',')}; refs='\\\\begin{thebibliography}{99}\\n'+'\\n'.join(line for line in (ROOT/'book/references.tex').read_text().splitlines() if any(line.startswith('\\\\bibitem{'+k+'}') for k in wanted))+'\\n\\\\end{thebibliography}'; run_tex('study-ih-challenge','\\\\input{../papers/studies/ih-challenge.tex}\\n'+refs,STUDIES['ih-challenge'])"
    # Write an ordinary source file to avoid multiple command/string escaping layers.
    helper=root/'fresh_rebuild_ih.py';helper.write_text("from scripts.build_collection import ROOT,STUDIES,run_tex\nimport re\ntext=(ROOT/'papers/studies/ih-challenge.tex').read_text()\nwanted={k for group in re.findall(r'\\\\cite\\{([^}]+)\\}',text) for k in group.split(',')}\nrefs='\\\\begin{thebibliography}{99}\\n'+'\\n'.join(line for line in (ROOT/'book/references.tex').read_text().splitlines() if any(line.startswith('\\\\bibitem{'+k+'}') for k in wanted))+'\\n\\\\end{thebibliography}'\nrun_tex('study-ih-challenge','\\\\input{../papers/studies/ih-challenge.tex}\\n'+refs,STUDIES['ih-challenge'])\n")
    run([sys.executable,'fresh_rebuild_ih.py'],'rebuild-study-ih-challenge');helper.unlink()
    for key in ['dpo','r1-nature','engram']:
        program="from scripts.build_collection import run_tex,PAPERS; run_tex("+repr(key)+","+repr('\\input{../papers/translations/'+key+'/body.tex}')+",PAPERS["+repr(key)+"])"
        run([sys.executable,'-c',program],'rebuild-'+key)
    run([sys.executable,'-m','scripts.write_release_index'],'rebuild-collections')
    component_checks=[]
    for name,b in before.items():
        current=root/name;assert b==signature(current), 'Component signature mismatch '+name;assert before_sizes[name]==sizes(current)
        if Path(name).stem in unchanged:assert record(root,name)==old[name]
        component_checks.append({'path':name,'pages':len(b['pages']),'rebuilt':name=='dist/ai-self-study.pdf' or Path(name).stem not in unchanged,'text_pixels_size_toc_links_identical':True,'reference_pdf_sha256':files[name]['sha256']})
    collections=[]
    for name in ['dist/ai-papers-zh.pdf','dist/ai-self-study-complete.pdf']:
        assert expected[name]==signature(root/name),'Collection expected signature mismatch '+name
        collections.append({'path':name,'pages':len(expected[name]['pages']),'text_pixels_toc_links_identical':True})
    # Recheck protected bytes after all new commands and archive stability.
    for name in protected_names:assert record(root,name)==old[name]
    assert sha(ARCHIVE)==EXPECTED
    emit('final-comparisons',{'components':component_checks,'collections':collections,'input_audit_byte_identical':True,'audit_record_slots':audit_result['record_slots'],'audit_unique_inputs':audit_result['unique_system_user_inputs'],'archive_unchanged':True})
    logs={p.name:{'sha256':sha(p),'size_bytes':p.stat().st_size} for p in sorted(LOGS.glob('fresh-*.txt'))}
    report={'status':'PASS','release':'0.3.1','archive_sha256':EXPECTED,'archive_bytes':58743118,'manifest_files':478,'safe_fresh_extraction':True,'manifest_all_file_hashes_and_sizes_valid':True,'changed_components_rebuilt':changed,'changed_components_count':5,'unchanged_components_reused':unchanged,'unchanged_components_count':8,'unchanged_component_pdfs_byte_identical_to_prior':True,'unchanged_compiled_dependencies_identical_to_prior':True,'common_build_dependencies_unchanged':common,'noncompiled_disclosure_exclusions':exclusions,'all_component_pdfs':13,'component_text_pixels_size_toc_links_identical':True,'collection_text_pixels_toc_links_identical':True,'component_checks':component_checks,'collection_checks':collections,'pages':{'book':99,'papers':393,'complete':492},'tests_run':58,'tests_skipped':0,'input_audit_byte_identical':True,'input_audit_sha256':sha(audit),'input_audit_record_slots':audit_result['record_slots'],'input_audit_unique_inputs':audit_result['unique_system_user_inputs'],'input_audit_unique_input_model_format_combinations':audit_result['unique_input_model_format_combinations'],'new_model_experiment_runs':0,'new_training_or_diagnostic_replays':0,'model_downloads':False,'prior_full_experiment_replay':{'archive_sha256':OLD,'report_sha256':sha(BASE/'qa/v03-reproducibility.json'),'actual_metrics_byte_comparisons':prior['actual_metrics_byte_comparisons'],'frozen_files_identical_count':len(frozen),'frozen_files':frozen},'commands':commands,'actual_logs':logs,'scope':'Fresh delta source rebuild of five changed components and both collections; eight unchanged PDFs retained only after byte and compiled-dependency identity checks. Fresh 58 tests include synthetic CPU model contract checks, but no experiment training or public-model diagnostic inference replay and no downloads. Prior v0.3 eleven-class full experiment replay remains bound through unchanged experiments/results/tests/frozen designs and original archive SHA. This does not claim all thirteen components were newly compiled.'}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','report':str(REPORT),'changed':5,'unchanged':8,'tests':58,'skipped':0,'new_model_experiment_runs':0,'archive_sha256':EXPECTED}),flush=True)
