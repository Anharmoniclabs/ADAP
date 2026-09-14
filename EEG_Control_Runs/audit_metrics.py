"""Subject-level audit. Runs on shipped features; does not assert raw-data provenance.
All computed results are written by this script, not transcribed from chat.
One-sided tests use the recorded hypothesis: larger deviation in the case group.
"""
from pathlib import Path
import argparse,json,hashlib,platform,time
import numpy as np
import pandas as pd
import scipy
from scipy.stats import rankdata,mannwhitneyu
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import sklearn

CHANNELS=['Fp1','Fp2','F3','F4','C3','C4','P3','P4','O1','O2','F7','F8','T3','T4','T5','T6','Fz','Cz','Pz']
BANDS=['delta','theta','alpha','beta','gamma']

def corr_distance(X,t):
    X=np.asarray(X,float);t=np.asarray(t,float)
    if X.ndim!=2 or t.shape!=(X.shape[1],) or not np.isfinite(X).all() or not np.isfinite(t).all():raise ValueError('Invalid maps')
    xc=X-X.mean(1,keepdims=True);tc=t-t.mean()
    den=np.sqrt((xc*xc).sum(1)*(tc*tc).sum())
    if np.any(den<=1e-15):raise ValueError('Flat map or template: no defined spatial correlation')
    return 1-(xc*tc).sum(1)/den

def matrix(df,band):
    return df[[f'{band}_{c}' for c in CHANNELS]].to_numpy(float)

def oof(X,y,seed=42):
    X=np.asarray(X,float);y=np.asarray(y,int);pred=np.full(len(y),np.nan);folds=np.zeros(len(y),int)
    if min(np.bincount(y))<5:raise ValueError('5-fold scoring needs 5 subjects in each group')
    for k,(tr,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=seed).split(X,y),1):
        pred[te]=corr_distance(X[te],X[tr][y[tr]==0].mean(0));folds[te]=k
    return pred,folds

def auc_fast(y,s):
    y=np.asarray(y,int);n1=int(y.sum());n0=len(y)-n1
    return float((rankdata(s)[y==1].sum()-n1*(n1+1)/2)/(n1*n0))

def bootstrap_auc(y,s,B=5000,seed=1701):
    """Stratified subject bootstrap conditional on the already fitted scores."""
    a=np.asarray(s)[np.asarray(y)==1];c=np.asarray(s)[np.asarray(y)==0]
    q=(a[:,None]>c[None,:]).astype(float)+.5*(a[:,None]==c[None,:])
    r=np.random.default_rng(seed); vals=[]
    for _ in range(B):
        ia=r.integers(len(a),size=len(a));ic=r.integers(len(c),size=len(c));vals.append(q[ia[:,None],ic[None,:]].mean())
    return np.quantile(vals,[.025,.975]).tolist()

def perm_auc(X,y,s,mode,B=2000,seed=1702):
    r=np.random.default_rng(seed);obs=auc_fast(y,s);v=np.empty(B)
    for b in range(B):
        yp=r.permutation(y)
        sp=oof(X,yp)[0] if mode=='local_oof' else s
        v[b]=auc_fast(yp,sp)
    return float((1+sum(v>=obs-1e-14))/(B+1)),v

def map_similarity(X):
    xc=X-X.mean(1,keepdims=True);norm=np.linalg.norm(xc,axis=1)
    if np.any(norm<=1e-15):raise ValueError('Flat map')
    return (xc/norm[:,None])@(xc/norm[:,None]).T

def group_mean(R,ind):
    n=len(ind);return float((R[np.ix_(ind,ind)].sum()-n)/(n*(n-1)))

def group_test(X,y,B=5000,seed=1703):
    R=map_similarity(X);a=np.flatnonzero(y==1);c=np.flatnonzero(y==0)
    ra=group_mean(R,a);rc=group_mean(R,c);obs=rc-ra;r=np.random.default_rng(seed);null=[]
    for _ in range(B):
        yp=r.permutation(y);null.append(group_mean(R,np.flatnonzero(yp==0))-group_mean(R,np.flatnonzero(yp==1)))
    return dict(r_cases=ra,r_controls=rc,gap_control_minus_case=obs,p_greater=(1+sum(v>=obs-1e-14 for v in null))/(B+1))

def holm(p):
    p=np.asarray(p,float);o=np.argsort(p);q=np.maximum.accumulate(p[o]*(len(p)-np.arange(len(p))));out=np.empty(len(p));out[o]=np.minimum(1,q);return out

def main(root,B=2000,boot=5000,scrambles=1000):
    root=Path(root);out=root/'results';out.mkdir(exist_ok=True)
    src=pd.read_csv(root/'data'/'frozen_features_full88.csv')
    fsu=pd.read_csv(root/'data'/'florida_external_frozen_features.csv')
    cz=pd.read_csv(root/'data'/'czech_reconstructed_features.csv')
    for name,d in [('source',src),('florida',fsu),('czech',cz)]:
        if d.subject.duplicated().any():raise ValueError(f'{name} duplicate subject')
    rows=[];predrows=[];groups=[];abl=[]
    tasks=[('source',src,'A','alpha','local_oof'),('source',src,'F','alpha','local_oof'),
           ('source',src,'A','delta','local_oof'),('source',src,'F','delta','local_oof'),
           ('florida',fsu,'A','alpha','local_oof'),('florida',fsu,'A','alpha','source_template'),
           ('florida',fsu,'A','delta','local_oof'),('florida',fsu,'A','delta','source_template'),
           ('czech',cz,'A','alpha','local_oof'),('czech',cz,'A','alpha','source_template'),
           ('czech',cz,'MCI','alpha','local_oof'),('czech',cz,'MCI','alpha','source_template')]
    for name,df,case,band,mode in tasks:
        d=df[df.group.isin([case,'C'])].reset_index(drop=True);y=(d.group==case).astype(int).to_numpy();X=matrix(d,band)
        t=matrix(src[src.group=='C'],band).mean(0)
        if mode=='local_oof':s,fold=oof(X,y)
        else:s=corr_distance(X,t);fold=np.zeros(len(y),int)
        auc=auc_fast(y,s);ci=bootstrap_auc(y,s,boot);p,v=perm_auc(X,y,s,mode,B)
        namekey=f'{name}_{case}_{band}_{mode}'
        np.save(out/(namekey+'_perm.npy'),v)
        U,pmw=mannwhitneyu(s[y==1],s[y==0],alternative='greater',method='auto')
        row=dict(cohort=name,cases=case,band=band,mode=mode,n_cases=int(y.sum()),n_controls=int((y==0).sum()),auc=auc,ci_low=ci[0],ci_high=ci[1],p_permutation=p,permutations=B,MW_descriptive_p=float(pmw),cases_mean=float(s[y==1].mean()),controls_mean=float(s[y==0].mean()),effect_rank_biserial=2*auc-1)
        rows.append(row)
        for sid,grp,yy,ss,k in zip(d.subject,d.group,y,s,fold):predrows.append(dict(test=namekey,subject=sid,group=grp,label=int(yy),score=float(ss),fold=int(k)))
        if mode=='source_template':
            rng=np.random.default_rng(1704);vals=[]
            for _ in range(scrambles):
                xp=np.take_along_axis(X,np.argsort(rng.random(X.shape),axis=1),axis=1);vals.append(auc_fast(y,corr_distance(xp,t)))
            sv=auc_fast(y,corr_distance(np.sort(X,axis=1),np.sort(t)))
            pi=np.random.default_rng(11).permutation(19)
            err=float(np.max(np.abs(corr_distance(X[:,pi],t[pi])-s)))
            abl.append(dict(test=namekey,real_auc=auc,shuffle_median=float(np.median(vals)),shuffle_low=float(np.quantile(vals,.025)),shuffle_high=float(np.quantile(vals,.975)),sorting_auc=sv,common_permutation_max_score_error=err))
        print(namekey,'AUC',round(auc,6),'CI',ci,'p',p,flush=True)
        pd.DataFrame(rows).to_csv(out/'recomputed_metrics.csv',index=False)
    for name,df,case in [('source',src,'A'),('source',src,'F'),('florida',fsu,'A'),('czech',cz,'A'),('czech',cz,'MCI')]:
        d=df[df.group.isin([case,'C'])].reset_index(drop=True);y=(d.group==case).astype(int).to_numpy()
        res=group_test(matrix(d,'alpha'),y,B=max(B,5000));groups.append(dict(cohort=name,cases=case,**res))
    tab=pd.DataFrame(rows);tab['p_holm_12_audit_tests']=holm(tab.p_permutation);tab.to_csv(out/'recomputed_metrics.csv',index=False)
    pd.DataFrame(predrows).to_csv(out/'subject_predictions.csv',index=False);pd.DataFrame(groups).to_csv(out/'topographic_agreement.csv',index=False);pd.DataFrame(abl).to_csv(out/'spatial_ablations.csv',index=False)
    repeat=[]
    for name,df,case,band,mode in tasks:
        if mode!='local_oof':continue
        d=df[df.group.isin([case,'C'])].reset_index(drop=True);y=(d.group==case).astype(int).to_numpy();X=matrix(d,band)
        v=[auc_fast(y,oof(X,y,k)[0]) for k in range(100)]
        repeat.append(dict(cohort=name,cases=case,band=band,mean=np.mean(v),sd=np.std(v,ddof=1),minimum=min(v),maximum=max(v)))
    pd.DataFrame(repeat).to_csv(out/'repeated_splits.csv',index=False)
    (out/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,seed_scheme='1701 bootstrap, 1702 label permutations, 1703 agreement, 1704 scrambling; folds=42',bootstrap_interpretation='fixed-score conditional subject bootstrap; excludes model fitting and selection uncertainty'),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--permutations',type=int,default=2000);p.add_argument('--bootstrap',type=int,default=5000);p.add_argument('--scrambles',type=int,default=1000);a=p.parse_args()
    main(a.root,a.permutations,a.bootstrap,a.scrambles)
