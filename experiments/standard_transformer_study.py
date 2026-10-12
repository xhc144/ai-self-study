#!/usr/bin/env python3
"""A complete small pre-norm causal Transformer trained on original finite grammar.
CPU only; optional torch dependency; no external data or pretrained weights.
The same train/test split is fixed before all runs. Repetition is a data intervention.
"""
import argparse,hashlib,json,platform,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build_model(vocab=10,width=32,heads=2,layers=2,ffn=64,context=7):
    import torch
    from torch import nn
    class Decoder(nn.Module):
        def __init__(self):
            super().__init__();self.tokens=nn.Embedding(vocab,width);self.positions=nn.Embedding(context,width)
            layer=nn.TransformerEncoderLayer(width,heads,ffn,dropout=0.,activation='gelu',batch_first=True,norm_first=True)
            self.blocks=nn.TransformerEncoder(layer,layers,enable_nested_tensor=False);self.final_norm=nn.LayerNorm(width);self.readout=nn.Linear(width,vocab)
        def forward(self,ids):
            t=ids.shape[1];x=self.tokens(ids)+self.positions(torch.arange(t,device=ids.device))
            mask=torch.triu(torch.full((t,t),float('-inf'),device=ids.device),diagonal=1)
            return self.readout(self.final_norm(self.blocks(x,mask=mask)))
    return Decoder()

def grammar():
    words=['<bos>','cat','dog','sees','red','blue','says','meow','woof','<eos>'];enc={w:i for i,w in enumerate(words)};docs=[]
    for speaker in ['cat','dog']:
        for color in ['red','blue']:
            for other in ['cat','dog']:
                docs.append([enc[w] for w in ['<bos>',speaker,'sees',color,other,'says','meow' if speaker=='cat' else 'woof','<eos>']])
    return words,docs

def main():
    import numpy as np,torch
    from torch.nn import functional as F
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,default=ROOT/'results/standard-transformer-v03')
    parser.add_argument('--design',type=Path,default=ROOT/'research/design-standard-transformer-v03.json');args=parser.parse_args()
    raw=args.design.read_bytes();cfg=json.loads(raw);torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    args.out.mkdir(parents=True,exist_ok=True);start=time.perf_counter();words,rows=grammar();docs=torch.tensor(rows,dtype=torch.long)
    train_ids=cfg['train_ids'];test_ids=cfg['test_ids'];runs=[]
    def loss(model,ids):
        logits=model(ids[:,:-1]);y=ids[:,1:];return F.cross_entropy(logits.reshape(-1,len(words)),y.reshape(-1))
    for seed in cfg['seeds']:
        for condition in cfg['conditions']:
            torch.manual_seed(seed);np.random.seed(seed);model=build_model(**cfg['architecture']);optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['lr'],weight_decay=cfg['weight_decay'])
            initial=hashlib.sha256(b''.join(k.encode()+v.detach().numpy().tobytes() for k,v in sorted(model.state_dict().items()))).hexdigest()
            ids=train_ids if condition=='balanced' else train_ids+[train_ids[0]]*cfg['additional_copies']
            train=docs[ids];trace=[]
            for step in range(1,cfg['steps']+1):
                model.train();optimizer.zero_grad();value=loss(model,train);value.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip']);optimizer.step()
                if step==1 or step%100==0 or step==cfg['steps']:trace.append([step,float(value.detach())])
            model.eval()
            with torch.inference_mode():
                test=docs[test_ids];logits=model(test[:,:-1]);targets=test[:,1:];probs=torch.softmax(logits[:,5],dim=-1)
                other=test.clone();other[:,4]=3-other[:,4];speaker=test.clone();speaker[:,1]=3-speaker[:,1];speaker[:,6]=15-speaker[:,6]
                variants=[]
                for name,xx in [('original',test),('distractor',other),('speaker',speaker)]:
                    pp=torch.softmax(model(xx[:,:-1])[:,5],dim=-1);truth=xx[:,6];pred=pp.argmax(-1)
                    variants.append({'name':name,'predictions':pred.tolist(),'truth':truth.tolist(),'correct':(pred==truth).tolist(),'target_probability':pp[torch.arange(len(truth)),truth].tolist()})
                changed=test[:,:-1].clone();changed[:,-1]=(changed[:,-1]+1)%len(words)
                causal_error=float((model(changed)[:,:-1]-logits[:,:-1]).abs().max())
                result={'seed':seed,'condition':condition,'training_row_ids_with_repetitions':ids,'train_unique_rows':len(set(ids)),'train_rows':len(ids),'initial_parameters_sha256':initial,'parameters':sum(p.numel() for p in model.parameters()),'trace':trace,'weighted_train_nll':float(loss(model,train)),'balanced_train_nll':float(loss(model,docs[train_ids])),'test_nll':float(loss(model,test)),'test_position_nll':[float(F.cross_entropy(logits[:,j],targets[:,j])) for j in range(7)],'test_position_accuracy':(logits.argmax(-1)==targets).float().mean(0).tolist(),'sound_variants':variants,'future_edit_prefix_error':causal_error}
            snapshot=args.out/f'weights-{condition}-{seed}.npz';np.savez_compressed(snapshot,**{k:v.detach().numpy() for k,v in model.state_dict().items()});result['snapshot_sha256']=hashlib.sha256(snapshot.read_bytes()).hexdigest();runs.append(result)
    report={'design_sha256':hashlib.sha256(raw).hexdigest(),'config':cfg,'vocabulary':words,'documents':rows,'runs':runs,'selection':cfg['selection'],'scope':cfg['scope']}
    text=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n';(args.out/'metrics.json').write_text(text)
    env={'python':sys.version,'platform':platform.platform(),'torch':torch.__version__,'numpy':np.__version__,'device':'CPU','dtype':'float32','threads':1,'seconds':time.perf_counter()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'design_sha256':report['design_sha256'],'metrics_sha256':hashlib.sha256(text.encode()).hexdigest()};(args.out/'environment.json').write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'runs':len(runs),'parameters':runs[0]['parameters'],'summary':[{'seed':r['seed'],'condition':r['condition'],'test_nll':r['test_nll'],'sound_correct':r['sound_variants'][0]['correct'],'causal_error':r['future_edit_prefix_error']} for r in runs],'seconds':env['seconds']}))

if __name__=='__main__':main()
