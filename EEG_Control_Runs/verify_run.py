from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
R=Path(__file__).resolve().parent;O=R/'results';checks={}
s=pd.read_csv(O/'spectral_subject_windows.csv');assert len(s)==444 and not s.duplicated(['cohort','subject','window']).any();checks['spectral_subject_windows']=len(s)
l=pd.read_csv(O/'lemon_subject_states.csv');assert len(l)==68 and l.subject.nunique()==34 and l.n_windows.min()>=3;checks['lemon_paired_people']=34
for p in (R/'data/lemon').glob('*.npz'):
 with np.load(p) as z:
  for state in ['EC','EO']:assert z[state].shape==(19,7680) and np.isfinite(z[state]).all()
manifest=json.loads((O/'cap_download_manifest.json').read_text());assert len(manifest)==16;checks['cap_candidates']=16
for r in manifest:
 if r['status']!='included':continue
 with np.load(R/'data/cap'/(r['subject']+'.npz')) as z:
  assert np.isfinite(z['epochs']).all() and z['epochs'].shape[2]==3840 and len(z['epochs'])==sum(r['counts'].values())
  assert set(z['stages'])<=set(['W','S1','S2'])
  assert 'ranges' in r,'old first30minute cache must not enter final run'
checks['cap_included']=sum(r['status']=='included' for r in manifest)
st=pd.read_csv(O/'state_tests.csv');assert len(st)==8;checks['paired_tests']=len(st)
p=pd.read_csv(O/'individual_peak_tests.csv');assert len(p)==6;checks['individual_peak_tests']=len(p)
g=pd.read_csv(O/'spectral_group_tests.csv');assert len(g)==81;checks['planned_group_tests']=len(g)
(O/'verification.json').write_text(json.dumps({'passed':True,'checks':checks},indent=2));print(checks)
