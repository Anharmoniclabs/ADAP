# Download and reproduce ADAP

Datasets do not have to live in Git. This repository provides pinned source links,
hashes, extraction code, the recorded environment, frozen outputs, and an executable
reproduction workflow.

## One command after cloning

Install Python 3.12 and run from the repository root:

```bash
python3.12 reproduce.py
```

On Windows: `py -3.12 reproduce.py`. The original run used Python 3.12.14.
The launcher creates a new sibling `adap-runs/YYYYMMDD-HHMMSS` directory and a
virtual environment, installs `requirements-lock.txt`, and saves separate frozen
`reference-results`. Your checkout and published outputs remain intact.

It downloads the Florida archive (OSF file heaw6, version 1), the pinned OpenNeuro
participant table, and 88 OpenNeuro v1.0.9 derivative recordings. Source SHA-256
checks precede extraction. It reconstructs the recorded first-eight-second and
first/middle/last 60-second inputs and requires **all 423 original package hashes**
to match before analysis. Missing inputs or different bytes stop the run.

It then executes spectral-fit validation, spectral controls, individualized-peak
controls, state controls, figures, report generation, and recorded-count checks.
CSV tables are compared with frozen references using `rtol=1e-7`, `atol=1e-10`,
equal missing values, exact nonnumeric values, and matching row/column order.
`comparison.json` records the outcome; differences cause failure. These tolerances
are declared comparison criteria, not a claim that a full fresh run has passed.

## Existing pack or cached sources

```bash
python3.12 reproduce.py --control-pack /path/to/Minier_EEG_Control_Runs.zip
python3.12 reproduce.py --prepare-only
python3.12 reproduce.py --check-links
python3.12 reproduce.py --source-dir /path/to/cached/set/files
python3.12 reproduce.py --workdir /path/to/new-run-directory
```

Pack mode imports only manifest-listed data and verifies each hash before writing.
It does not overwrite analysis code or extract arbitrary archive paths.
A separately hosted pack can be used with
`--pack-url https://YOUR-HOST/control-pack.zip --pack-sha256 ACTUAL_SHA256`.
This is an optional interface; no public pack URL is invented or assumed.

`--prepare-only` installs the environment and verifies inputs without analysis.
`--check-links` probes the Florida metadata/hash, participant URL, and one OpenNeuro
object; it does not test every recording. `--source-dir` retains and reuses source
files after hash verification. Existing run directories are rejected.

## Resources and original sources

Without a pack, expect several gigabytes of network transfer. One OpenNeuro
recording is processed at a time; its temporary source copy is deleted after
extraction unless a source directory is supplied. Allow several gigabytes of disk
space for the environment, package, references, and outputs. Runtime depends on
CPU/network. Downloads retry three times; interrupted partial downloads restart.
Original hosts and pinned dependencies must be available.

| Input | Source | Integrity |
|---|---|---|
| OpenNeuro | [ds004504 v1.0.9](https://openneuro.org/datasets/ds004504/versions/1.0.9) | 88 source hashes and pinned metadata revision |
| Florida | [OSF project](https://osf.io/2v5md/) / [archive version 1](https://osf.io/download/heaw6/?version=1) | SHA-256 f5b30df4fd0d18e3224dde0bd564e2a5cea61845ae5a9b8142ae722c5d99ba93 |
| LEMON | [MPI-LEMON](https://fcon_1000.projects.nitrc.org/indi/retro/MPI_LEMON.html) | Recorded extracts already in Git; package hashes |
| CAP | [CAP v1.0.0](https://physionet.org/content/capslpdb/1.0.0/) | Recorded extracts already in Git; package hashes |

`reproduction/sources.json` contains pinned acquisition routes and source hashes.
Original source terms and citations apply. Florida is downloaded from its original
host by the person reproducing the analysis; it is not redistributed by this change.
The optional multipart full-source archive is not required.

## Validation status

- Recovered control pack and launcher pack import: all 423 hashes pass.
- One real downloaded OpenNeuro source: source hash verified, three regenerated
  60-second extracts byte-identical, and first-eight-second samples identical.
- Repacking the recorded first-eight-second arrays reproduces the NPZ hash.
- Launcher syntax and source-link probes checked.
- Florida archive downloaded from the versioned OSF URL: exact SHA-256 match.
- CSV comparison accepts matching data and rejects a deliberately changed value.

**A complete new download and end-to-end numerical rerun has not been completed.**
This is an executable workflow with integrity gates, not a claim of independent
replication or clinical validation. See FINDINGS.md and LIMITATIONS_PARAGRAPH.md.
