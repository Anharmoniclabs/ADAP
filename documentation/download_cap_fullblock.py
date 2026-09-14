from pathlib import Path
import requests,json,hashlib,concurrent.futures,math,re
import numpy as np
from scipy.signal import resample_poly
from fractions import Fraction
R=Path(__file__).resolve().parent;D=R/'data/cap';D.mkdir(exist_ok=True);BASE='https://physionet.org/files/capslpdb/1.0.0/'
def get(u,a=None,b=None):
 for attempt in range(3):
  try:
   hdr={'Range':f'bytes={a}-{b}'} if a is not None else {}
   # Unique range URL avoids intermediary caches reusing an earlier smaller range.
   url=u+(f'?range={a}-{b}' if a is not None else '')
   r=requests.get(url,headers=hdr,timeout=120);r.raise_for_status()
   if a is not None:assert r.status_code==206 and r.headers.get('Content-Range','').startswith(f'bytes {a}-{b}/') and len(r.content)==b-a+1
   return r
  except Exception:
   if attempt==2:raise

def seconds(t):
 h,m,s=map(float,t.replace('.',':').split(':'));return h*3600+m*60+s

def one(i):
 sid=f'n{i}';dest=D/(sid+'.npz')
 if dest.exists():return json.loads((D/(sid+'.json')).read_text())
 rec={'subject':sid}
 try:
  u=BASE+sid+'.edf';a=get(u,0,255).content;nh=int(a[184:192]);header=get(u,0,nh-1).content;ns=int(a[252:256]);dur=float(a[244:252]);nr=int(a[236:244]);start=seconds(a[176:184].decode());off=256
  def field(width,typ=str):
   nonlocal off
   v=[typ(header[off+j*width:off+(j+1)*width].decode().strip()) for j in range(ns)];off+=ns*width;return v
  labels=field(16);trans=field(80);units=field(8);pmin=np.array(field(8,float));pmax=np.array(field(8,float));dmin=np.array(field(8,float));dmax=np.array(field(8,float));pref=field(80);samples=np.array(field(8,int));reserved=field(32)
  # Require genuinely recorded same-side frontal/occipital channels with same reference.
  normalized=[s.upper().replace('EEG','').replace(' ','') for s in labels];pair=None
  for f,o in [('F3','O1'),('F4','O2')]:
   for ref in ['A1','A2']:
    if f+'-'+ref in normalized and o+'-'+ref in normalized:pair=[normalized.index(f+'-'+ref),normalized.index(o+'-'+ref)];break
   if pair:break
  algebra=None
  chain=['F4-C4','C4-P4','P4-O2','C4-A1']
  if pair is None and all(c in normalized for c in chain):
   algebra=[normalized.index(c) for c in chain];pair=algebra
   if len({units[j] for j in algebra})!=1:raise ValueError('incompatible units in bipolar chain')
  if pair is None:raise ValueError('No matching frontal/occipital reference pair: '+str(labels))
  extra=[j for j,s in enumerate(labels) if any(k in s.upper() for k in ['ECG','EKG','EOG','ROC','LOC'])];ix=pair+[j for j in extra if j not in pair]
  records=min(nr,int(1800/dur));bs=int(samples.sum()*2);raw=get(u,nh,nh+records*bs-1).content;vals=np.frombuffer(raw,dtype='<i2').reshape(records,int(samples.sum()));offsets=np.r_[0,np.cumsum(samples)];signals=[]
  for j in ix:
   y=vals[:,offsets[j]:offsets[j+1]].ravel().astype(float);y=(y-dmin[j])*(pmax[j]-pmin[j])/(dmax[j]-dmin[j])+pmin[j];fs=samples[j]/dur;frac=Fraction(128/fs).limit_denominator(10000);signals.append(resample_poly(y,frac.numerator,frac.denominator).astype('float32'))
  x=np.stack(signals);selected=[labels[j] for j in ix]
  if algebra:
   x=np.vstack([x[0]+x[3],x[3]-x[1]-x[2],x[4:]]);selected=['F4-A1','O2-A1']+selected[4:]
  annotations=get(BASE+sid+'.txt').content;(D/(sid+'.txt')).write_bytes(annotations);epochs=[];stages=[];onsets=[]
  counts={'W':0,'S1':0,'S2':0}
  for line in annotations.decode(errors='replace').splitlines():
   fields=line.split('\t')
   if len(fields)<5 or fields[3] not in ['SLEEP-S0','SLEEP-S1','SLEEP-S2']:continue
   stage={'SLEEP-S0':'W','SLEEP-S1':'S1','SLEEP-S2':'S2'}[fields[3]];t=(seconds(fields[2])-start)%86400;length=float(fields[4]);t0=round(t*128)
   if length<30 or t+30>records*dur or counts[stage]>=10:continue
   epochs.append(x[:,t0:t0+3840]);stages.append(stage);onsets.append(t);counts[stage]+=1
  if not epochs:raise ValueError('No eligible stages in first30min')
  np.savez_compressed(dest,epochs=np.stack(epochs),stages=np.array(stages),onsets=np.array(onsets),channel_names=np.array(selected))
  (D/(sid+'_header.bin')).write_bytes(header)
  rec.update(status='included',counts=counts,selected_channels=selected,algebraic_reconstruction=bool(algebra),contributing_channels=[labels[j] for j in ix],all_channels=labels,units=[units[j] for j in ix],start_seconds=start,record_duration=dur,fs=[float(samples[j]/dur) for j in ix],source_url=u,range=f'{nh}-{nh+records*bs-1}',range_sha256=hashlib.sha256(raw).hexdigest(),header_sha256=hashlib.sha256(header).hexdigest(),annotation_sha256=hashlib.sha256(annotations).hexdigest())
 except Exception as e:rec.update(status='excluded',reason=str(e))
 (D/(sid+'.json')).write_text(json.dumps(rec,indent=2));print(sid,rec.get('counts'),rec.get('reason',''),flush=True);return rec
with concurrent.futures.ThreadPoolExecutor(4) as ex:rows=list(ex.map(one,range(1,17)))
(R/'results/cap_download_manifest.json').write_text(json.dumps(rows,indent=2));print('DONE',len(rows),sum(r['status']=='included' for r in rows),flush=True)
