"""Execute a frozen finite-grammar study; no automatic model or split selection."""
import hashlib,json,math
from pathlib import Path
import numpy as np
from run_all import TinyDecoder,softmax,cross_entropy,gradient_error


def exact_binomial_interval(k,n,alpha=.05):
    if not 0<=k<=n or n<1 or not 0<alpha<1:raise ValueError('Invalid binomial count/confidence')
    def tail(p,indices):return sum(math.comb(n,j)*p**j*(1-p)**(n-j) for j in indices)
    def root(indices,target,increasing):
        lo,hi=0.,1.
        for _ in range(100):
            mid=(lo+hi)/2;v=tail(mid,indices)
            if (v<target)==increasing:lo=mid
            else:hi=mid
        return (lo+hi)/2
    return [root(range(k,n+1),alpha/2,True) if k else 0.,
            root(range(k+1),alpha/2,False) if k<n else 1.]


def grammar():
    words=['<bos>','cat','dog','sees','red','blue','says','meow','woof','<eos>']
    enc={w:i for i,w in enumerate(words)};docs=[]
    for speaker in ['cat','dog']:
        for color in ['red','blue']:
            for other in ['cat','dog']:
                docs.append([enc[w] for w in ['<bos>',speaker,'sees',color,other,'says','meow' if speaker=='cat' else 'woof','<eos>']])
    return words,np.array(docs)


def train(model,x,y,steps,lr):
    mom={k:np.zeros_like(v) for k,v in model.p.items()};vel={k:v.copy() for k,v in mom.items()}
    trace=[]
    for t in range(1,steps+1):
        loss,g=model.loss_grad(x,y);size=np.sqrt(sum((v*v).sum() for v in g.values()))
        for k in model.p:
            gg=g[k]/max(1.,size);mom[k]=.9*mom[k]+.1*gg;vel[k]=.999*vel[k]+.001*gg*gg
            model.p[k]-=lr*(mom[k]/(1-.9**t))/(np.sqrt(vel[k]/(1-.999**t))+1e-8)
        if t==1 or t%100==0 or t==steps:trace.append([t,model.loss_grad(x,y)[0]])
    return trace


def evaluate(model,docs,train_ids,test_ids):
    x,y=docs[test_ids,:-1],docs[test_ids,1:]
    other=x.copy();other[:,4]=3-other[:,4] # cat=1, dog=2
    speaker=x.copy();speaker[:,1]=3-speaker[:,1]
    sound=y[:,5];flipped=15-sound # meow=7, woof=8
    speaker[:,6]=flipped # future token is not read at says, but full patched document stays valid
    inputs={'original':x,'distractor':other,'speaker':speaker}
    targets={'original':sound,'distractor':sound,'speaker':flipped}
    variants={}
    for name,xx in inputs.items():
        logits,_=model.forward(xx);probs=softmax(logits[:,5]);pred=logits[:,5].argmax(-1)
        variants[name]={'predicted_sound':pred.tolist(),'target_sound':targets[name].tolist(),
                        'target_probability':probs[np.arange(len(xx)),targets[name]].tolist(),
                        'original_sound_probability':probs[np.arange(len(xx)),sound].tolist(),
                        'accuracy':float((pred==targets[name]).mean()),'all_correct':bool((pred==targets[name]).all())}
        if name!='original':
            # Match complete modified document including its semantically correct sound.
            modified=docs[test_ids].copy();modified[:,:-1]=xx;modified[:,6]=targets[name]
            variants[name]['patched_document_ids']=[int(np.where((docs==row).all(1))[0][0]) for row in modified]
            variants[name]['patched_is_training']=[i in train_ids for i in variants[name]['patched_document_ids']]
    ll=model.forward(x)[0]
    return {'full_token_nll':cross_entropy(ll,y)[0],
            'sound_nll':cross_entropy(ll[:,5],sound)[0],
            'token_nll_by_position':[cross_entropy(ll[:,j],y[:,j])[0] for j in range(y.shape[1])],
            'token_accuracy_by_position':(ll.argmax(-1)==y).mean(0).tolist(),
            'token_predictions':ll.argmax(-1).tolist(), 'variants':variants,
            'subject_effect_original_sound_probability':(np.array(variants['speaker']['original_sound_probability'])-np.array(variants['original']['original_sound_probability'])).tolist(),
            'distractor_effect_original_sound_probability':(np.array(variants['distractor']['original_sound_probability'])-np.array(variants['original']['original_sound_probability'])).tolist()}


def baselines(docs,train_ids,test_ids):
    x,y=docs[test_ids,:-1],docs[test_ids,1:];sound=y[:,5]
    counts=np.bincount(docs[train_ids,6],minlength=10);frequent=int(counts.argmax())
    result={}
    for name in ['nearest_animal_rule','training_sound_frequency_after_says']:
        variants={}
        for variant in ['original','distractor','speaker']:
            xx=x.copy();truth=sound.copy()
            if variant=='distractor':xx[:,4]=3-xx[:,4]
            if variant=='speaker':xx[:,1]=3-xx[:,1];truth=15-truth
            pred=np.where(xx[:,4]==1,7,8) if name=='nearest_animal_rule' else np.full(len(xx),frequent)
            variants[variant]={'predicted_sound':pred.tolist(),'target_sound':truth.tolist(),'accuracy':float((pred==truth).mean())}
        result[name]=variants
    return result


def micro_research(design=None,seeds=None,steps=None,lr=None,width=None):
    explicit_design=design is not None
    design=Path(design) if explicit_design else Path(__file__).resolve().parents[1]/'research/design-v02.json'
    raw=design.read_bytes();config=json.loads(raw);overrides={}
    design_hash=hashlib.sha256(raw).hexdigest()
    if explicit_design:
        overrides['design']={'path':str(design.resolve()),'sha256':design_hash}
    for name,value in [('seeds',seeds),('steps',steps),('lr',lr),('width',width)]:
        if value is not None:config[name]=value;overrides[name]=value
    if not config['seeds'] or len(set(config['seeds']))!=len(config['seeds']):raise ValueError('Use distinct initialization seeds')
    words,docs=grammar();runs=[];summaries=[];base={}
    for split,test_ids in config['splits'].items():
        if len(set(test_ids))!=2 or any(i not in range(8) for i in test_ids):raise ValueError('Each frozen split holds out two distinct grammar documents')
        train_ids=[i for i in range(8) if i not in test_ids];base[split]=baselines(docs,train_ids,test_ids)
        for seed in config['seeds']:
            model=TinyDecoder(len(words),width=config['width'],seed=seed)
            errors=gradient_error(lambda:model.loss_grad(docs[train_ids[:2],:-1],docs[train_ids[:2],1:])[0],model.p,model.loss_grad(docs[train_ids[:2],:-1],docs[train_ids[:2],1:])[1],np.random.default_rng(seed+1))
            assert max(errors.values())<1e-7
            initial_hash=hashlib.sha256(b''.join(k.encode()+model.p[k].tobytes() for k in sorted(model.p))).hexdigest()
            trace=train(model,docs[train_ids,:-1],docs[train_ids,1:],config['steps'],config['lr'])
            result=evaluate(model,docs,train_ids,test_ids)
            runs.append({'split':split,'seed':seed,'train_ids':train_ids,'test_ids':test_ids,
                         'gradient_errors':errors,'initial_parameters_sha256':initial_hash,'parameter_count':sum(v.size for v in model.p.values()),'train_trace':trace,'train_nll':model.loss_grad(docs[train_ids,:-1],docs[train_ids,1:])[0],**result})
        subset=[r for r in runs if r['split']==split];n=len(subset)
        k=sum(r['variants']['original']['all_correct'] for r in subset)
        summaries.append({'split':split,'seeds':n,'all_test_sounds_correct_runs':k,
                          'conditional_95pct_interval':exact_binomial_interval(k,n,config['confidence']['alpha']),
                          'mean_sound_accuracy':float(np.mean([r['variants']['original']['accuracy'] for r in subset])),
                          'mean_token_nll':float(np.mean([r['full_token_nll'] for r in subset])),
                          'mean_distractor_accuracy':float(np.mean([r['variants']['distractor']['accuracy'] for r in subset])),
                          'mean_speaker_flip_accuracy':float(np.mean([r['variants']['speaker']['accuracy'] for r in subset]))})
    # Average across the three fixed splits within each shared initialization first.
    paired=[{'seed':seed,'mean_accuracy_fixed_splits':float(np.mean([r['variants']['original']['accuracy'] for r in runs if r['seed']==seed]))} for seed in config['seeds']]
    return {'design_sha256':design_hash,'executed_config':config,'exploratory_overrides':overrides,
            'vocabulary':words,'documents':docs.tolist(),'runs':runs,'baselines':base,'summary':summaries,
            'paired_seed_means':paired,'uncertainty_scope':'Each interval is conditional on its fixed split and IID initializations; separate intervals are not simultaneous; no bootstrap or IID test-document claim.',
            'selection':'All configured runs included; no test-based tuning/retries.'}
