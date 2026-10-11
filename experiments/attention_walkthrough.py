"""Tiny deterministic causal attention example and a deliberate residual bug."""
import numpy as np
from run_all import softmax, gradient_error, TinyDecoder


def attention_walkthrough(lr=.1):
    x=np.array([[1.],[2.]])
    p={k:np.ones((1,1)) for k in ['Q','K','V']}
    def calc(back=False):
        q,k,v=(x@p[n] for n in ['Q','K','V'])
        s=q@k.T
        a=softmax(np.where(np.tril(np.ones((2,2),bool)),s,-np.inf))
        c=a@v;loss=float(.5*(c[1,0]-1.5)**2)
        gc=np.array([[0.],[c[1,0]-1.5]])
        ga=gc@v.T;gv=a.T@gc
        gs=a*(ga-(a*ga).sum(-1,keepdims=True))
        gq=gs@k;gk=gs.T@q
        grads={'Q':x.T@gq,'K':x.T@gk,'V':x.T@gv}
        values={'X':x,'Q':q,'K':k,'V':v,'S_unmasked':s,'A':a,'C':c,
                'G_C':gc,'G_A':ga,'G_S':gs,'G_Q':gq,'G_K':gk,'G_V':gv,
                'G_X':gq@p['Q'].T+gk@p['K'].T+gv@p['V'].T}
        return loss,grads,values
    before,g,v=calc();errors=gradient_error(lambda:calc()[0],p,g,np.random.default_rng(0),checks=10000)
    assert max(errors.values())<1e-7
    for k in p:p[k]-=lr*g[k]
    after,_,new=calc()
    return {'shape':{'B':1,'T':2,'D':1},'target_last_output':1.5,'lr':lr,
            'before':{k:a.tolist() for k,a in v.items()},'parameter_gradients':{k:a.tolist() for k,a in g.items()},
            'parameters_after':{k:a.tolist() for k,a in p.items()},'C_after':new['C'].tolist(),
            'loss_before':before,'loss_after':after,'gradient_errors':errors,
            'note':'One head, no FFN/residual/output classifier; squared scalar loss at last position. Only Q/K/V projections update; X is fixed.'}


def residual_debug(seed=19):
    m=TinyDecoder(vocab=6,context=3,width=4,seed=seed)
    x=np.array([[0,1,2],[3,4,1]]);y=np.array([[1,2,5],[4,1,5]])
    loss,correct=m.loss_grad(x,y)
    _,broken=m.loss_grad(x,y,omit_attention_residual=True)
    check=lambda g:gradient_error(lambda:m.loss_grad(x,y)[0],m.p,g,np.random.default_rng(seed+1),checks=10000)
    good=check(correct);bad=check(broken)
    # Repeated token id=1 occurs twice, hence two input-gradient contributions add.
    return {'seed':seed,'checked_coordinates':sum(v.size for v in m.p.values()),
            'input_ids':x.tolist(),'targets':y.tolist(),'loss':loss,
            'correct_errors':good,'omitted_residual_errors':bad,
            'fault':'drop the direct x -> h = x + C@O derivative from dx; forward values unchanged',
            'expected_localization':'E and P fail; Q/K/V/O/FFN/U parameter derivatives remain correct',
            'repair':'restore dx = dh + dq@Q.T + dk@K.T + dv@V.T'}
