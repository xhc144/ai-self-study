#!/usr/bin/env python3
"""Optional CPU diagnostics on two pinned public 135M models; no API or remote code.
Install requirements-models.txt first. Downloads require --allow-download.
Weights/cache stay outside the public source archive. This is not an RLVR replication.
"""
import argparse,gc,hashlib,json,platform,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def strict_letter(text):
    text=text.strip()
    return text if text in {'A','B'} else None

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design',type=Path,default=ROOT/'research/design-public-models-v03.json')
    parser.add_argument('--out',type=Path,default=ROOT/'results/public-models-v03')
    parser.add_argument('--cache',type=Path,default=Path('/tmp/ai-hf-cache'))
    parser.add_argument('--allow-download',action='store_true')
    args=parser.parse_args();raw=args.design.read_bytes();design=json.loads(raw)
    import numpy as np,torch,transformers
    from transformers import AutoModelForCausalLM,AutoTokenizer
    torch.set_num_threads(design['threads']);torch.set_num_interop_threads(1)
    torch.manual_seed(design['seed']);np.random.seed(design['seed'])
    torch.use_deterministic_algorithms(True)
    args.cache.mkdir(parents=True,exist_ok=True);args.out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter();rows=[];provenance=[]
    for model_info in design['models']:
        kw=dict(revision=model_info['revision'],cache_dir=str(args.cache),local_files_only=not args.allow_download,trust_remote_code=False)
        tokenizer=AutoTokenizer.from_pretrained(model_info['id'],**kw)
        model=AutoModelForCausalLM.from_pretrained(model_info['id'],use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager',**kw).to('cpu').eval()
        assert sum(p.numel() for p in model.parameters())==model_info['parameters']
        found=args.cache/('models--'+model_info['id'].replace('/','--'))/'snapshots'/model_info['revision']
        hashes={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in found.iterdir() if p.is_file()}
        weight_bytes=sum(x['bytes'] for n,x in hashes.items() if n.endswith('.safetensors'))
        assert weight_bytes<=design['max_total_model_weight_download_bytes']/len(design['models'])
        provenance.append(model_info|{'resolved_files':hashes,'weight_bytes':weight_bytes,'model_class':type(model).__name__})
        conditions=['matched_plain']+(['native_chat'] if model_info['type']=='instruct' else [])
        for condition in conditions:
            for case in design['cases']:
                messages=[{'role':'system','content':case['system']},{'role':'user','content':case['user']}]
                prompt=('System: '+case['system']+'\nUser: '+case['user']+'\nAssistant:') if condition=='matched_plain' else tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
                inputs=tokenizer(prompt,return_tensors='pt',add_special_tokens=False)
                prefix=inputs['input_ids'];logps=[];candidate_ids=[]
                with torch.inference_mode():
                    for continuation in design['candidate_strings']:
                        ids=tokenizer.encode(continuation,add_special_tokens=False);candidate_ids.append(ids)
                        full=torch.cat([prefix,torch.tensor([ids])],dim=1)
                        logits=model(input_ids=full,attention_mask=torch.ones_like(full)).logits
                        lp=torch.log_softmax(logits[0,prefix.shape[1]-1:full.shape[1]-1,:],dim=-1)
                        logps.append(float(lp[torch.arange(len(ids)),torch.tensor(ids)].sum()))
                    output=model.generate(**inputs,**design['generation'],pad_token_id=tokenizer.eos_token_id)
                text=tokenizer.decode(output[0,prefix.shape[1]:],skip_special_tokens=True)
                probs=np.exp(np.array(logps)-max(logps));probs/=probs.sum()
                choice=['A','B'][int(np.argmax(logps))];letter=strict_letter(text)
                rows.append({'model':model_info['id'],'revision':model_info['revision'],'condition':condition,'case':case['id'],'kind':case['kind'],'truth':case['truth'],'prompt':prompt,'input_tokens':int(prefix.shape[1]),'candidate_token_ids':candidate_ids,'candidate_logp':logps,'restricted_AB_probabilities':probs.tolist(),'forced_choice':choice,'forced_choice_correct':choice==case['truth'],'generated_text':text,'generated_tokens':int(output.shape[1]-prefix.shape[1]),'strict_letter':letter,'strict_generated_correct':letter==case['truth'],'valid_AB_format':letter is not None})
        del model;gc.collect()
    summary=[]
    for model_info in design['models']:
        conditions=sorted({r['condition'] for r in rows if r['model']==model_info['id']})
        for condition in conditions:
            for kind in ['all','arithmetic','context_mapping','role_conflict']:
                group=[r for r in rows if r['model']==model_info['id'] and r['condition']==condition and (kind=='all' or r['kind']==kind)]
                summary.append({'model':model_info['id'],'condition':condition,'kind':kind,'n':len(group),'forced_choice_accuracy':sum(r['forced_choice_correct'] for r in group)/len(group),'strict_generated_accuracy':sum(r['strict_generated_correct'] for r in group)/len(group),'valid_format_rate':sum(r['valid_AB_format'] for r in group)/len(group)})
    report={'design_sha256':hashlib.sha256(raw).hexdigest(),'models':provenance,'rows':rows,'summary':summary,'scope':design['scope'],'restricted_score_warning':'AB probabilities normalize over only two specified continuation token strings. They are not full-output correctness or calibrated confidence.','causal_warning':design['conditions'],'selection':design['selection']}
    metrics=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n';(args.out/'metrics.json').write_text(metrics)
    env={'python':sys.version,'platform':platform.platform(),'torch':torch.__version__,'transformers':transformers.__version__,'numpy':np.__version__,'device':'CPU','dtype':'float32','threads':torch.get_num_threads(),'seed':design['seed'],'elapsed_seconds':time.perf_counter()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'design_sha256':report['design_sha256'],'metrics_sha256':hashlib.sha256(metrics.encode()).hexdigest(),'cli':{'allow_download':args.allow_download,'cache':str(args.cache),'design':str(args.design)}}
    (args.out/'environment.json').write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'summary':summary,'seconds':env['elapsed_seconds']},ensure_ascii=False))

if __name__=='__main__':main()
