from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'Minier_EEG_Parts.json').read_text())
output=root/m['output']
if output.exists():
    raise SystemExit('Output already exists; keep it or move it before rebuilding.')
for part in m['parts']:
    p=root/part['name']
    if not p.is_file() or p.stat().st_size!=part['bytes']:
        raise SystemExit('Missing or wrong-sized part: '+part['name'])
tmp=output.with_suffix('.zip.assembling')
if tmp.exists():raise SystemExit('Previous assembly exists; inspect it before retrying.')
total=hashlib.sha256()
try:
    with tmp.open('xb') as out:
        for part in m['parts']:
            h=hashlib.sha256()
            with (root/part['name']).open('rb') as f:
                for block in iter(lambda:f.read(1048576),b''):
                    h.update(block);total.update(block);out.write(block)
            if h.hexdigest()!=part['sha256']:raise ValueError('Part checksum mismatch: '+part['name'])
            print('Verified',part['name'],flush=True)
    if total.hexdigest()!=m['sha256']:raise ValueError('Full archive checksum mismatch')
    tmp.rename(output)
    print('SUCCESS:',output)
except Exception:
    tmp.unlink(missing_ok=True)
    raise
