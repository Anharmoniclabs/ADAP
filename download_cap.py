from pathlib import Path
import requests,json,hashlib,concurrent.futures,math,re,sys
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
   r=requests.get(url,headers=hdr,timeout=45);r.raise_for_status()
   if a is not None:assert r.status_code==206 and r.headers.get('Content-Range','').startswith(f'bytes {a}-{b}/') and len(r.content)==b-a+1
   return r
  except Exception:
   if attempt==2:raise

def seconds(t):
 h,m,s=map(float,t.replace('.',':').split(':'));return h*3600+m*60+s

def one(i):
 sid=f'n{i}';dest=D/(sid+'.npz')
 if dest.exists():
  cached=json.loads((D/(sid+'.json')).read_text())
  if 'ranges' in cached:return cached
 if (D/(sid+'.json')).exists():
  cached=json.loads((D/(sid+'.json')).read_text())
  if cached.get('reason','').startswith('No matching frontal/occipital') and not re.search(r'F[34]A[12]',cached.get('reason','')):return cached
 rec={'subject':sid}
 try:
  u=BASE+sid+'.edf';initial=get(u,0,255);a=initial.content;total_bytes=int(initial.headers['Content-Range'].split('/')[-1]);nh=int(a[184:192]);header=get(u,0,nh-1).content;ns=int(a[252:256]);dur=float(a[244:252]);nr=int(a[236:244]);start=seconds(a[176:184].decode());off=256
  def field(width,typ=str):
   nonlocal off
   v=[typ(header[off+j*width:off+(j+1)*width].decode().strip()) for j in range(ns)];off+=ns*width;return v
  labels=field(16);trans=field(80);units=field(8);pmin=np.array(field(8,float));pmax=np.array(field(8,float));dmin=np.array(field(8,float));dmax=np.array(field(8,float));pref=field(80);samples=np.array(field(8,int));reserved=field(32)
  # Require genuinely recorded same-side frontal/occipital channels with same reference.
  normalized=[re.sub(r'^(F[34]|O[12])(A[12])$',r'\1-\2',s.upper().replace('EEG','').replace(' ','')) for s in labels];pair=None
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
  bs=int(samples.sum()*2)
  if nr<0:
   assert (total_bytes-nh)%bs==0,'EDF length not integral number of records'
   nr=(total_bytes-nh)//bs
  records=nr;annotations=get(BASE+sid+'.txt').content;(D/(sid+'.txt')).write_bytes(annotations);selected_epochs=[];counts={'W':0,'S1':0,'S2':0}
  for line in annotations.decode(errors='replace').splitlines():
   fields=line.split('\t')
   event_indices=[j for j,v in enumerate(fields) if v in ['SLEEP-S0','SLEEP-S1','SLEEP-S2']]
   if not event_indices:continue
   j=event_indices[0]
   if j<1 or j+1>=len(fields) or ':' not in fields[j-1]:continue
   stage={'SLEEP-S0':'W','SLEEP-S1':'S1','SLEEP-S2':'S2'}[fields[j]];t=(seconds(fields[j-1])-start)%86400;length=float(fields[j+1])
   if length<30 or t+30>records*dur or counts[stage]>=10:continue
   selected_epochs.append((t,stage));counts[stage]+=1
  if not selected_epochs:raise ValueError('No eligible scored stages in recording')
  # Merge nearby requests while bounding each transfer to about5minutes.
  chunks=[]
  for t,stage in sorted(selected_epochs):
   lo=max(0,int((t-1)//dur));hi=min(records,int(math.ceil((t+31)/dur)))
   if chunks and lo<=chunks[-1][1] and hi-chunks[-1][0]<=int(302/dur):chunks[-1][1]=max(chunks[-1][1],hi);chunks[-1][2].append((t,stage))
   else:chunks.append([lo,hi,[(t,stage)]])
  epochs=[];stages=[];onsets=[];ranges=[];selected=[labels[j] for j in ix]
  if algebra:selected=['F4-A1','O2-A1']+selected[4:]
  for lo,hi,events in chunks:
   aa=nh+lo*bs;bb=nh+hi*bs-1;raw=get(u,aa,bb).content;vals=np.frombuffer(raw,dtype='<i2').reshape(hi-lo,int(samples.sum()));offsets=np.r_[0,np.cumsum(samples)];signals=[]
   for j in ix:
    y=vals[:,offsets[j]:offsets[j+1]].ravel().astype(float);y=(y-dmin[j])*(pmax[j]-pmin[j])/(dmax[j]-dmin[j])+pmin[j];fs=samples[j]/dur;frac=Fraction(128/fs).limit_denominator(10000);signals.append(resample_poly(y,frac.numerator,frac.denominator).astype('float32'))
   x=np.stack(signals)
   if algebra:x=np.vstack([x[0]+x[3],x[3]-x[1]-x[2],x[4:]])
   for t,stage in events:
    t0=round((t-lo*dur)*128);ep=x[:,t0:t0+3840];assert ep.shape[1]==3840;epochs.append(ep);stages.append(stage);onsets.append(t)
   ranges.append({'bytes':f'{aa}-{bb}','sha256':hashlib.sha256(raw).hexdigest()})
   print(sid,'range complete',lo*dur,hi*dur,flush=True)
  np.savez_compressed(dest,epochs=np.stack(epochs),stages=np.array(stages),onsets=np.array(onsets),channel_names=np.array(selected))
  (D/(sid+'_header.bin')).write_bytes(header)
  rec.update(status='included',counts=counts,selected_channels=selected,algebraic_reconstruction=bool(algebra),contributing_channels=[labels[j] for j in ix],all_channels=labels,units=[units[j] for j in ix],start_seconds=start,record_count=nr,record_duration=dur,fs=[float(samples[j]/dur) for j in ix],source_url=u,ranges=ranges,header_sha256=hashlib.sha256(header).hexdigest(),annotation_sha256=hashlib.sha256(annotations).hexdigest())
 except Exception as e:rec.update(status='excluded',reason=str(e))
 (D/(sid+'.json')).write_text(json.dumps(rec,indent=2));print(sid,rec.get('counts'),rec.get('reason',''),flush=True);return rec
ids=list(map(int,sys.argv[1].split(','))) if len(sys.argv)>1 else list(range(1,17))
with concurrent.futures.ThreadPoolExecutor(4) as ex:rows=list(ex.map(one,ids))
manifest='cap_download_manifest_retry.json' if len(sys.argv)>1 else 'cap_download_manifest.json'
(R/'results'/manifest).write_text(json.dumps(rows,indent=2));print('DONE',len(rows),sum(r['status']=='included' for r in rows),flush=True)
