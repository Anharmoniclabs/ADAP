from pathlib import Path
import json
import numpy as np,pandas as pd
from scipy.signal import welch,resample_poly
from scipy.integrate import trapezoid
from audit_metrics import CHANNELS,corr_distance,holm
R=Path(__file__).resolve().parent;D=R/'data';O=R/'results'
POST=[CHANNELS.index(c) for c in ['P3','P4','Pz','O1','O2']];FRONT=[CHANNELS.index(c) for c in ['Fp1','Fp2','F3','F4','F7','F8','Fz']]
def bands(x):
 f,s=welch(x,fs=128,nperseg=1024,noverlap=512 if x.shape[-1]>1024 else 0,detrend='constant',window='hann',axis=-1)
 return np.stack([trapezoid(s[..., (f>=lo)&(f<hi)],f[(f>=lo)&(f<hi)],axis=-1) for lo,hi in [(1,4),(4,8),(8,13),(13,30)]])
def feature19(x,template):
 b=bands(x);ra=b[2]/b.sum(0)
 return dict(score=float(corr_distance(ra[None,:],template)[0]),log_posterior_frontal_alpha=float(np.log(b[2,POST].mean()/b[2,FRONT].mean())),log_theta_alpha=float(np.log(b[1].mean()/b[2].mean())))
def paired(d,cohort,condition,reference,factor):
 p=d.pivot(index='subject',columns='state',values=factor)
 if condition not in p or reference not in p:return dict(cohort=cohort,condition=condition,reference=reference,factor=factor,n=0,p=np.nan)
 p=p[[reference,condition]].dropna();diff=(p[condition]-p[reference]).to_numpy();n=len(diff)
 if n<3:return dict(cohort=cohort,condition=condition,reference=reference,factor=factor,n=n,p=np.nan)
 rng=np.random.default_rng(20260914);obs=diff.mean();null=(rng.choice([-1,1],(10000,n))*diff).mean(1);boot=rng.choice(diff,(5000,n)).mean(1)
 return dict(cohort=cohort,condition=condition,reference=reference,factor=factor,n=n,reference_mean=p[reference].mean(),condition_mean=p[condition].mean(),mean_paired_difference=obs,ci_low=np.quantile(boot,.025),ci_high=np.quantile(boot,.975),p=(1+(np.abs(null)>=abs(obs)-1e-14).sum())/10001,n_increase=int((diff>0).sum()),n_decrease=int((diff<0).sum()))
def run():
 meta=pd.read_csv(D/'participants.tsv',sep='\t').set_index('participant_id');templates={}
 with np.load(D/'openneuro_first8s_waveforms.npz') as z:
  for ref in ['native','average19']:
   maps=[]
   for sid in z.files:
    if meta.loc[sid,'Group']!='C':continue
    x=resample_poly(z[sid],32,125,axis=1)
    if ref=='average19':x=x-x.mean(0)
    b=bands(x);maps.append(b[2]/b.sum(0))
   templates[ref]=np.mean(maps,axis=0)
 np.savez(O/'frozen_templates.npz',**templates)
 lrows=[];windows=[];exclusions=[]
 for p in sorted((D/'lemon').glob('*.npz')):
  with np.load(p) as z:
   for state in ['EC','EO']:
    x=z[state];bounds=z[state+'_boundary_seconds'];observations=[]
    for start in range(0,x.shape[1]-1024+1,512):
     t=start/128
     if np.any((bounds>t)&(bounds<t+8)):continue
     w=x[:,start:start+1024];r=feature19(w,templates['native']);r['score_average19']=feature19(w-w.mean(0),templates['average19'])['score'];r.update(subject=p.stem,state=state,start_seconds=t);windows.append(r);observations.append(r)
    if len(observations)<3:exclusions.append(dict(subject=p.stem,state=state,reason='fewer than3 boundary-free8s windows'));continue
    q=pd.DataFrame(observations);r=dict(subject=p.stem,state=state,n_windows=len(q))
    for col in ['score','score_average19','log_posterior_frontal_alpha','log_theta_alpha']:r[col]=q[col].median()
    for half,mask in [('first30',q.start_seconds+8<=30),('last30',q.start_seconds>=30)]:r['score_'+half]=q.loc[mask,'score'].median()
    lrows.append(r)
 ld=pd.DataFrame(lrows);ld.to_csv(O/'lemon_subject_states.csv',index=False);pd.DataFrame(windows).to_csv(O/'lemon_windows.csv',index=False);pd.DataFrame(exclusions).to_csv(O/'lemon_analysis_exclusions.csv',index=False)
 tests=[paired(ld,'LEMON','EO','EC',c) for c in ['score','score_average19','log_posterior_frontal_alpha','log_theta_alpha']]
 # CAP regional sensitivity on raw channels. ECG regression and shifted-ECG sham are descriptive only.
 crows=[]
 def cfeatures(x):
  b=bands(x[:2]);return dict(log_posterior_frontal_alpha=float(np.log(b[2,1]/b[2,0])),log_theta_alpha=float(np.log(b[1].mean()/b[2].mean())))
 for p in sorted((D/'cap').glob('*.npz')):
  with np.load(p) as z:
   names=z['channel_names'].tolist();ecg=[j for j,s in enumerate(names) if 'ECG' in s.upper() or 'EKG' in s.upper()]
   for i,(x,stage,t) in enumerate(zip(z['epochs'],z['stages'],z['onsets'])):
    vals=cfeatures(x);r=dict(subject=p.stem,state=stage,onset_seconds=t,**vals)
    if ecg:
     signal=x[ecg[0]].astype(float);signal=(signal-signal.mean())/max(signal.std(),1e-12)
     for mode,e in [('ecg',signal),('sham',np.roll(signal,5*128))]:
      Z=np.column_stack([np.ones(len(e))]+[np.roll(e,lag) for lag in [-10,-5,0,5,10]]);coef=np.linalg.lstsq(Z,x[:2].T,rcond=None)[0];clean=x[:2]-((Z@coef).T);v=cfeatures(clean[:,10:-10]);orig=cfeatures(x[:2,10:-10]);r[mode+'_ratio_change']=v['log_posterior_frontal_alpha']-orig['log_posterior_frontal_alpha'];r[mode+'_removed_variance_fraction']=float(1-np.var(clean[:,10:-10],axis=1).mean()/np.var(x[:2,10:-10],axis=1).mean())
    crows.append(r)
 cd=pd.DataFrame(crows);cd.to_csv(O/'cap_epochs.csv',index=False);cc=cd.groupby(['subject','state']).agg(n_epochs=('onset_seconds','size'),log_posterior_frontal_alpha=('log_posterior_frontal_alpha','median'),log_theta_alpha=('log_theta_alpha','median')).reset_index();cc.loc[cc.n_epochs<3,['log_posterior_frontal_alpha','log_theta_alpha']]=np.nan;cc.to_csv(O/'cap_subject_states.csv',index=False)
 for state in ['S1','S2']:
  for col in ['log_posterior_frontal_alpha','log_theta_alpha']:tests.append(paired(cc,'CAP',state,'W',col))
 tab=pd.DataFrame(tests);good=tab.p.notna();tab.loc[good,'holm_state_tests']=holm(tab.p.fillna(1))[good];tab.to_csv(O/'state_tests.csv',index=False)
 if 'ecg_ratio_change' in cd:
  cd.groupby('subject')[['ecg_ratio_change','sham_ratio_change','ecg_removed_variance_fraction','sham_removed_variance_fraction']].median().to_csv(O/'cap_ecg_sensitivity.csv')
 print(tab.to_string(index=False),flush=True)
 (O/'state_complete.json').write_text(json.dumps({'lemon_people':int(ld.subject.nunique()),'cap_people':int(cd.subject.nunique()),'lemon_windows':len(windows),'cap_epochs':len(cd),'tests':len(tab)}))
if __name__=='__main__':run()
