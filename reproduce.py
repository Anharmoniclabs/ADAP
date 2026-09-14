#!/usr/bin/env python3
"""Download, verify and rerun ADAP in an isolated directory (Python 3.12)."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
import venv
import zipfile

ROOT = Path(__file__).resolve().parent
PIPELINE = ['validate_spectral_fit.py', 'spectral_controls.py',
            'individual_peak_controls.py', 'state_controls.py',
            'make_figures.py', 'build_report.py', 'verify_run.py']


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def download(url, target, expected):
    target = Path(target)
    if target.exists():
        if sha256(target) == expected:
            return
        raise RuntimeError(f'Existing file has wrong checksum: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + '.partial')
    for attempt in range(3):
        try:
            print('DOWNLOAD', url, flush=True)
            with urllib.request.urlopen(url, timeout=90) as response, partial.open('wb') as out:
                shutil.copyfileobj(response, out, 1024 * 1024)
            if sha256(partial) != expected:
                raise RuntimeError(f'Source checksum mismatch: {url}')
            partial.replace(target)
            return
        except Exception:
            partial.unlink(missing_ok=True)
            if attempt == 2:
                raise


def manifest(root):
    return {p: h for h, p in (line.split(None, 1)
            for line in (root / 'SHA256SUMS').read_text().splitlines() if line.strip())}


def verify_all(root):
    errors = []
    for p, expected in manifest(root).items():
        f = root / ('PACKAGE_README.md' if p == 'README.md' else p)
        if not f.is_file() or sha256(f) != expected:
            errors.append(p)
    if errors:
        raise RuntimeError('Missing or mismatched package files:\n' + '\n'.join(errors))
    print('INPUT GATE PASS: all 423 original package files match SHA-256', flush=True)


def restore_pack(pack, root):
    """Import only manifest-listed data, with hashes checked before writing."""
    with zipfile.ZipFile(pack) as archive:
        for p, expected in manifest(root).items():
            if not p.startswith('data/'):
                continue
            target = root / p
            if target.exists() and sha256(target) == expected:
                continue
            candidates = [n for n in archive.namelist() if n == p or n.endswith('/' + p)]
            if len(candidates) != 1:
                raise RuntimeError(f'Archive must contain exactly one {p}')
            content = archive.read(candidates[0])
            if hashlib.sha256(content).hexdigest() != expected:
                raise RuntimeError(f'Archive checksum mismatch: {p}')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)


def acquire(root, source_dir=None):
    import numpy as np
    from scipy.io import loadmat
    from scipy.signal import resample_poly
    from audit_metrics import CHANNELS

    config = json.loads((root / 'reproduction/sources.json').read_text())
    data = root / 'data'
    download(config['participants']['url'], data / 'participants.tsv', config['participants']['sha256'])
    download(config['florida']['url'], data / 'EEG_data.zip', config['florida']['sha256'])
    expected = manifest(root)
    first_path = data / 'openneuro_first8s_waveforms.npz'
    need_first = not first_path.exists() or sha256(first_path) != expected['data/openneuro_first8s_waveforms.npz']
    first = {}
    (data / 'source60').mkdir(exist_ok=True)
    for entry in config['openneuro']:
        sid = entry['subject']
        dest = data / 'source60' / (sid + '.npz')
        if not need_first and dest.exists() and sha256(dest) == expected[f'data/source60/{sid}.npz']:
            continue
        source = (Path(source_dir) if source_dir else root / 'source-cache') / entry['source_name']
        download(entry['url'], source, entry['source_sha256'])
        z = loadmat(source, squeeze_me=True, struct_as_record=False)
        labels = [str(c.labels) for c in z['chanlocs']]
        x = z['data'][[labels.index(c) for c in CHANNELS]]
        if int(z['srate']) != 500 or not np.isfinite(x).all():
            raise RuntimeError(f'Unexpected source signal: {sid}')
        starts = [0, (x.shape[1] - 30000) // 2, x.shape[1] - 30000]
        if starts != entry['starts'] or min(starts) < 0:
            raise RuntimeError(f'Extraction receipt differs: {sid}')
        if need_first:
            first[sid] = x[:, :4000].astype('float64')
        arrays = {k: resample_poly(x[:, t:t + 30000], 32, 125, axis=1).astype('float32')
                  for k, t in zip(['first60', 'middle60', 'last60'], starts)}
        np.savez_compressed(dest, **arrays)
        if sha256(dest) != expected[f'data/source60/{sid}.npz']:
            raise RuntimeError(f'Reconstructed cache differs: {sid}; check pinned environment')
        if source_dir is None:
            source.unlink()
        print('VERIFIED', sid, flush=True)
    if need_first:
        np.savez_compressed(first_path, **first)
    shutil.copyfile(root / 'reproduction/source60_extraction.json', data / 'source60_extraction.json')
    verify_all(root)


def compare_results(reference, generated):
    import numpy as np
    import pandas as pd
    reports = []
    for old in sorted(reference.glob('*.csv')):
        new = generated / old.name
        try:
            a, b = pd.read_csv(old), pd.read_csv(new)
        except pd.errors.EmptyDataError:
            reports.append({'file': old.name, 'passed': old.read_bytes() == new.read_bytes()})
            continue
        passed = list(a.columns) == list(b.columns) and a.shape == b.shape
        if passed:
            for col in a.columns:
                if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]):
                    passed = passed and np.allclose(a[col], b[col], rtol=1e-7, atol=1e-10, equal_nan=True)
                else:
                    passed = passed and a[col].fillna('').equals(b[col].fillna(''))
        reports.append({'file': old.name, 'passed': bool(passed)})
    result = {'rtol': 1e-7, 'atol': 1e-10, 'csv_comparisons': reports,
              'passed': all(r['passed'] for r in reports)}
    (generated.parent / 'comparison.json').write_text(json.dumps(result, indent=2))
    if not result['passed']:
        raise RuntimeError('Numerical comparison differs; see comparison.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', type=Path, help='New isolated output directory')
    parser.add_argument('--control-pack', type=Path, help='Existing Minier_EEG_Control_Runs.zip')
    parser.add_argument('--pack-url', help='Optional HTTPS URL for a complete control pack')
    parser.add_argument('--pack-sha256', help='Required SHA-256 when using --pack-url')
    parser.add_argument('--source-dir', type=Path, help='Reuse downloaded OpenNeuro .set files')
    parser.add_argument('--prepare-only', action='store_true', help='Acquire and verify without analysis')
    parser.add_argument('--check-links', action='store_true', help='Check source metadata and one byte range; no dataset download')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.check_links:
        config = json.loads((ROOT / 'reproduction/sources.json').read_text())
        with urllib.request.urlopen('https://api.osf.io/v2/files/63f9068e9d447902b932cc89/', timeout=90) as response:
            remote = json.load(response)['data']['attributes']['extra']['hashes']['sha256']
        if remote != config['florida']['sha256']:
            raise RuntimeError('Florida source hash changed')
        for url in [config['participants']['url'], config['openneuro'][0]['url'] + '&probe=1']:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'Range': 'bytes=0-127'}), timeout=90) as response:
                response.read(128)
        print('Source-link probe passed; this is not an end-to-end reproduction')
        return
    if not args.worker:
        if sys.version_info[:2] != (3, 12):
            parser.error('Use Python 3.12 for the recorded environment (original patch version 3.12.14).')
        work = (args.workdir or ROOT.parent / 'adap-runs' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S')).resolve()
        if work == ROOT or ROOT in work.parents:
            parser.error('--workdir must be outside the source checkout')
        if work.exists():
            parser.error('--workdir must be a new directory; existing runs are preserved')
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))
        shutil.copytree(work / 'results', work / 'reference-results')
        env = work / '.venv'
        venv.EnvBuilder(with_pip=True).create(env)
        python = env / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
        subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(work / 'requirements-lock.txt')], check=True)
        command = [str(python), str(work / 'reproduce.py'), '--worker']
        for flag, value in [('--control-pack', args.control_pack), ('--source-dir', args.source_dir),
                            ('--pack-url', args.pack_url), ('--pack-sha256', args.pack_sha256)]:
            if value:
                command += [flag, str(value.resolve() if isinstance(value, Path) else value)]
        if args.prepare_only:
            command += ['--prepare-only']
        print('ISOLATED RUN', work, flush=True)
        subprocess.run(command, cwd=work, check=True)
        return
    if args.pack_url:
        if not args.pack_url.startswith('https://') or not args.pack_sha256:
            parser.error('--pack-url requires HTTPS and --pack-sha256')
        args.control_pack = ROOT / 'control-pack.zip'
        download(args.pack_url, args.control_pack, args.pack_sha256)
    if args.control_pack:
        restore_pack(args.control_pack, ROOT)
        verify_all(ROOT)
    else:
        acquire(ROOT, args.source_dir)
    if args.prepare_only:
        return
    for script in PIPELINE:
        subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)
    compare_results(ROOT / 'reference-results', ROOT / 'results')
    print('Pipeline and declared CSV comparisons passed. See comparison.json.', flush=True)


if __name__ == '__main__':
    main()
