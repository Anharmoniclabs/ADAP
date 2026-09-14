from pathlib import Path
import numpy as np,pandas as pd
from scipy.integrate import trapezoid
from scipy.stats import mannwhitneyu
from fooof import FOOOF
from audit_metrics import CHANNELS,holm
R=Path(__file__).resolve().parent;O=R/'results';P=[CHANNELS.index(c) for c in ['P3','P4','Pz','O1','O2']];F=[CHANNELS.index(c) for c in ['Fp1','Fp2','F3','F4','F7','F8','Fz']];meta=pd.read_csv(R/'data/participants.tsv',sep='\t').set_index('participant_id');rows=[]
f=np.arange(513)/8
with np.load(O/'channel_psds.npz') as z:
 for key in z.files:
  if not key.startswith('OpenNeuro') or key.endswith('first8'):continue
  _,sid,win=key.split('_');s=z[key];p=s[P].mean(0);q=s[F].mean(0);fm=FOOOF(peak_width_limits=[1,8],max_n_peaks=6,min_peak_height=.1,peak_threshold=2,aperiodic_mode='fixed',verbose=False);fm.fit(f,p,[2,30]);valid=fm.has_model and fm.r_squared_>=.8 and fm.error_<=.15;peaks=fm.peak_params_;peaks=peaks[(peaks[:,0]>=4)&(peaks[:,0]<=14)]
  row=dict(subject=sid,group=meta.loc[sid,'Group'],window=win,fit_valid=bool(valid),candidate_peak_hz=np.nan,individualized_log_ratio=np.nan)
  if valid and len(peaks):
   peak=peaks[np.argmax(peaks[:,1]),0];m=(f>=peak-2)&(f<peak+2);row['candidate_peak_hz']=peak;row['individualized_log_ratio']=float(np.log(trapezoid(p[m],f[m])/trapezoid(q[m],f[m])))
  rows.append(row)
x=pd.DataFrame(rows);x.to_csv(O/'individual_peak_subjects.csv',index=False);tests=[]
for win,d in x.groupby('window'):
 for col in ['candidate_peak_hz','individualized_log_ratio']:
  a=d.loc[d.group=='A',col].dropna().to_numpy();c=d.loc[d.group=='C',col].dropna().to_numpy();u,p=mannwhitneyu(a,c,alternative='two-sided');rng=np.random.default_rng(20260914);boot=np.median(rng.choice(a,(5000,len(a))),axis=1)-np.median(rng.choice(c,(5000,len(c))),axis=1)
  tests.append(dict(window=win,factor=col,n_AD=len(a),n_control=len(c),AD_median=np.median(a),control_median=np.median(c),difference=np.median(a)-np.median(c),ci_low=np.quantile(boot,.025),ci_high=np.quantile(boot,.975),p=p))
t=pd.DataFrame(tests);t['holm6_exploratory']=holm(t.p);t.to_csv(O/'individual_peak_tests.csv',index=False);print(t.to_string(index=False))
