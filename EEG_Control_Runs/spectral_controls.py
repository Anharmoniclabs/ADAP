from pathlib import Path
import io,json,zipfile,hashlib,sys,warnings
import numpy as np,pandas as pd
from scipy.io import loadmat
from scipy.signal import welch,resample_poly
from scipy.integrate import trapezoid
from scipy.stats import mannwhitneyu,spearmanr
from fooof import FOOOF
from audit_metrics import CHANNELS,holm
R=Path(__file__).resolve().parent;D=R/'data';O=R/'results';O.mkdir(exist_ok=True)
POST=[CHANNELS.index(c) for c in ['P3','P4','Pz','O1','O2']];FRONT=[CHANNELS.index(c) for c in ['Fp1','Fp2','F3','F4','F7','F8','Fz']]
def psd(x):return welch(x,fs=128,nperseg=1024,noverlap=512 if x.shape[-1]>1024 else 0,window='hann',detrend='constant',axis=-1)
def band(f,s,lo=8,hi=13):
 m=(f>=lo)&(f<hi);return trapezoid(s[...,m],f[m],axis=-1)
def factors(x,record):
 f,s=psd(x);row=dict(record);models=[]
 for name,ix in [('posterior',POST),('frontal',FRONT)]:
  p=s[ix].mean(0);row['log_'+name+'_alpha']=float(np.log(band(f,p)))
  fm=FOOOF(peak_width_limits=[1,8],max_n_peaks=6,min_peak_height=.1,peak_threshold=2,aperiodic_mode='fixed',verbose=False)
  fm.fit(f,p,[2,30]);ok=fm.has_model and fm.r_squared_>=.8 and fm.error_<=.15
  row[name+'_fit_r2']=fm.r_squared_;row[name+'_fit_error']=fm.error_;row[name+'_fit_ok']=bool(ok)
  row[name+'_exponent']=fm.aperiodic_params_[1] if ok else np.nan
  sel=(fm.freqs>=8)&(fm.freqs<13)
  row[name+'_periodic_alpha']=float(fm._peak_fit[sel].mean()) if ok else np.nan
  peaks=fm.peak_params_;peaks=peaks[(peaks[:,0]>=8)&(peaks[:,0]<=13)]
  row[name+'_has_alpha_peak']=bool(len(peaks)) if ok else np.nan
  row[name+'_alpha_peak_hz']=float(peaks[np.argmax(peaks[:,1]),0]) if ok and len(peaks) else np.nan
  models.append(np.vstack([fm.freqs,fm.power_spectrum,fm.fooofed_spectrum_,fm._ap_fit,fm._peak_fit]))
 row['log_posterior_frontal_alpha']=row['log_posterior_alpha']-row['log_frontal_alpha']
 row['periodic_alpha_contrast']=row['posterior_periodic_alpha']-row['frontal_periodic_alpha']
 row['exponent_contrast']=row['posterior_exponent']-row['frontal_exponent']
 return row,s,np.stack(models)
def extract60(fullroot):
 out=D/'source60';out.mkdir(exist_ok=True);receipts=[]
 for p in sorted(Path(fullroot).glob('*.set')):
  sid=p.name.split('_')[0];dest=out/(sid+'.npz')
  if dest.exists():continue
  z=loadmat(p,squeeze_me=True,struct_as_record=False);labels=[str(c.labels) for c in z['chanlocs']];x=z['data'][[labels.index(c) for c in CHANNELS]];fs=int(z['srate']);N=x.shape[1];starts=[0,(N-60*fs)//2,N-60*fs]
  assert fs==500 and min(starts)>=0
  v={k:resample_poly(x[:,t:t+60*fs],32,125,axis=1).astype('float32') for k,t in zip(['first60','middle60','last60'],starts)}
  np.savez_compressed(dest,**v);receipts.append(dict(subject=sid,source_name=p.name,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_fs=fs,starts=starts))
  print('EXTRACT',sid,flush=True)
 if receipts:(D/'source60_extraction.json').write_text(json.dumps(receipts,indent=2))
def run():
 meta=pd.read_csv(D/'participants.tsv',sep='\t').set_index('participant_id');rows=[];spectra={};fits={}
 def add(x,cohort,sid,g,window):
  key=f'{cohort}_{sid}_{window}';r,s,m=factors(x,dict(cohort=cohort,subject=sid,group=g,window=window));rows.append(r);spectra[key]=s;fits[key]=m
 with np.load(D/'openneuro_first8s_waveforms.npz') as z:
  for sid in sorted(z.files):add(resample_poly(z[sid],32,125,axis=1),'OpenNeuro',sid,meta.loc[sid,'Group'],'first8')
 for p in sorted((D/'source60').glob('*.npz')):
  with np.load(p) as z:
   for win in z.files:add(z[win],'OpenNeuro',p.stem,meta.loc[p.stem,'Group'],win)
 with zipfile.ZipFile(D/'EEG_data.zip') as z:
  for group,code in [('AD','A'),('Healthy','C')]:
   pref=f'EEG_data/{group}/Eyes_closed/';folders=sorted({str(Path(p).parent) for p in z.namelist() if p.startswith(pref) and p.endswith('.txt')})
   for folder in folders:
    x=np.stack([np.loadtxt(io.BytesIO(z.read(folder+'/'+c+'.txt'))) for c in CHANNELS]);add(x,'Florida','OSF_'+group+'_'+Path(folder).name,code,'first8')
 df=pd.DataFrame(rows);df.to_csv(O/'spectral_subject_windows.csv',index=False);np.savez_compressed(O/'channel_psds.npz',**spectra);np.savez_compressed(O/'regional_spectral_fits.npz',**fits)
 features=json.loads((R/'PLAN.json').read_text())['group_features'];tests=[]
 for (cohort,window),dd in df.groupby(['cohort','window']):
  for case,ctrl in [('A','C')]+([('A','F')] if cohort=='OpenNeuro' else []):
   for col in features:
    a=dd.loc[dd.group==case,col].dropna().to_numpy();b=dd.loc[dd.group==ctrl,col].dropna().to_numpy();u,p=mannwhitneyu(a,b,alternative='two-sided') if min(len(a),len(b))>=3 else (np.nan,np.nan)
    rng=np.random.default_rng(20260914);boot=np.median(rng.choice(a,(5000,len(a))),axis=1)-np.median(rng.choice(b,(5000,len(b))),axis=1) if min(len(a),len(b))>=3 else np.array([np.nan])
    tests.append(dict(cohort=cohort,window=window,case=case,comparison=ctrl,factor=col,n_case=len(a),n_comparison=len(b),case_median=np.median(a),comparison_median=np.median(b),median_difference=np.median(a)-np.median(b),ci_low=np.quantile(boot,.025),ci_high=np.quantile(boot,.975),p=p))
 tab=pd.DataFrame(tests);good=tab.p.notna();tab.loc[good,'holm_all_group_tests']=holm(tab.p.fillna(1))[good];tab.to_csv(O/'spectral_group_tests.csv',index=False)
 stability=[]
 for col in features:
  pivot=df[(df.cohort=='OpenNeuro')&(df.group.isin(['A','C']))].pivot(index='subject',columns='window',values=col)
  for win in ['middle60','last60']:
   q=pivot[['first60',win]].dropna();rho,p=spearmanr(q.first60,q[win]);stability.append(dict(factor=col,comparison=win,n=len(q),rho=rho,p=p))
 pd.DataFrame(stability).to_csv(O/'source_window_stability.csv',index=False)
 print(tab[(tab.comparison=='C')&tab.factor.isin(['log_posterior_alpha','log_frontal_alpha','periodic_alpha_contrast','exponent_contrast'])].to_string(index=False),flush=True)
 (O/'spectral_complete.json').write_text(json.dumps({'subject_windows':len(df),'tests':len(tab),'method':'FOOOF1.1.1; mean log10 periodic contribution in8-13, not direct neuronal oscillation amplitude'}))
if __name__=='__main__':
 if '--extract' in sys.argv:extract60(sys.argv[sys.argv.index('--extract')+1])
 run()
