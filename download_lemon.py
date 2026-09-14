from pathlib import Path
import requests,io,json,hashlib,concurrent.futures,xml.etree.ElementTree as E
import numpy as np,pandas as pd
from scipy.io import loadmat
from scipy.signal import resample_poly
from audit_metrics import CHANNELS
R=Path(__file__).resolve().parent;D=R/'data/lemon';D.mkdir(exist_ok=True);DOC=R/'documentation';BASE='https://fcp-indi.s3.amazonaws.com/'
NS={'s':'http://s3.amazonaws.com/doc/2006-03-01/'}
keys=[v.find('s:Key',NS).text for v in E.parse(DOC/'lemon_uncompressed.xml').findall('s:Contents',NS)]
lookup={Path(k).name:k for k in keys if 'Preprocessed' in k};meta=pd.read_csv(DOC/'lemon_phenotype.txt');eligible=meta[meta.Age.str.split('-').str[0].astype(int)>=55].sort_values('ID')
( R/'lemon_selection_before_scores.json').write_text(json.dumps(eligible.to_dict('records'),indent=2))
alias={'T3':'T7','T4':'T8','T5':'P7','T6':'P8'}
def get(u,headers=None):
 for attempt in range(3):
  try:
   r=requests.get(u,headers=headers,timeout=90);r.raise_for_status();return r
  except Exception:
   if attempt==2:raise

def one(row):
 sid=row['ID'];out=D/(sid+'.npz');record=dict(subject=sid,age_bin=row['Age'],sex_code=row[meta.columns[1]])
 if out.exists():return json.loads((D/(sid+'.json')).read_text())
 try:
  data={};info={}
  for state in ['EC','EO']:
   name=f'{sid}_{state}.set'
   if name not in lookup:raise ValueError('preprocessed set unavailable: '+state)
   r=get(BASE+lookup[name]);raw=r.content;e=loadmat(io.BytesIO(raw),squeeze_me=True,struct_as_record=False)['EEG'];labels=[str(c.labels) for c in e.chanlocs];needed=[alias.get(c,c) for c in CHANNELS];missing=[c for c in needed if c not in labels]
   if missing:raise ValueError('missing required channels '+','.join(missing))
   fs=int(e.srate);n=int(e.nbchan);N=min(int(e.pnts),60*fs)
   if N<60*fs:raise ValueError('less than60seconds')
   fname=f'{sid}_{state}.fdt';key=lookup[fname];size=N*n*4;rr=get(BASE+key,{'Range':f'bytes=0-{size-1}'})
   if rr.status_code!=206 or not rr.headers.get('Content-Range','').startswith(f'bytes 0-{size-1}/') or len(rr.content)!=size:raise ValueError('range validation failed')
   x=np.frombuffer(rr.content,dtype='<f4').reshape((n,N),order='F')[[labels.index(c) for c in needed]]
   assert fs==250 and np.isfinite(x).all()
   data[state]=resample_poly(x,64,125,axis=1).astype('float32')
   events=[]
   for ev in np.atleast_1d(e.event):
    lat=float(ev.latency)
    if lat<=N and str(ev.type)=='boundary':events.append((lat-1)/fs)
   data[state+'_boundary_seconds']=np.array(events)
   info[state]=dict(set_url=BASE+lookup[name],fdt_url=BASE+key,set_sha256=hashlib.sha256(raw).hexdigest(),range=rr.headers['Content-Range'],range_sha256=hashlib.sha256(rr.content).hexdigest(),native_fs=fs,channel_names=labels,selected_names=needed,boundary_seconds=events)
   (D/name).write_bytes(raw)
  np.savez_compressed(out,**data);record.update(status='included',conditions=info)
 except Exception as e:record.update(status='excluded',reason=str(e))
 (D/(sid+'.json')).write_text(json.dumps(record,indent=2));print(sid,record['status'],record.get('reason',''),flush=True);return record
with concurrent.futures.ThreadPoolExecutor(6) as ex:records=list(ex.map(one,eligible.to_dict('records')))
(R/'results/lemon_download_manifest.json').write_text(json.dumps(records,indent=2));print('DONE',len(records),sum(r['status']=='included' for r in records),flush=True)
