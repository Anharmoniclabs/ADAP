# Data availability and reproducibility

This repository is designed to make the analysis auditable without misrepresenting third-party recordings as repository-owned data.

## Versioned in Git

The repository versions the scientific logic and audit trail: analysis scripts, frozen plans and amendments, dependency locks, source/exclusion manifests, exact subject-level CSV/JSON outputs, statistical tables, checksums, and SVG figures.

## Large waveform/source files

The completed control package contains about 349 MB uncompressed. Most of that size is derived `.npz` waveform/PSD cache data and third-party EEG source files. Those large binary caches are intentionally not required as ordinary Git source files. Their provenance, selection rules, extraction scripts, and SHA-256 records are kept with the analysis so the inputs can be reacquired/reconstructed and verified.

Primary sources used by the current controls:

- OpenNeuro ds004504 v1.0.9: https://openneuro.org/datasets/ds004504/versions/1.0.9
- Florida OSF dataset: https://osf.io/2v5md/
- MPI-LEMON: https://fcon_1000.projects.nitrc.org/indi/retro/MPI_LEMON.html
- CAP Sleep Database: https://physionet.org/content/capslpdb/1.0.0/

Original dataset licenses and attribution requirements remain in force. No blanket relicensing of third-party EEG data is asserted here.

## Integrity

`SHA256SUMS` records the supplied control-package file hashes. The final execution receipt is `receipt.json`; the run verifier is `verify_run.py`. See `data/README.md` for the canonical input layout and source-by-source acquisition status.

The completed control run reports 444 spectral subject-window rows, 34 paired LEMON participants, 16 CAP candidates with 11 included for eligible state analyses, 8 paired state tests, 6 individualized-peak tests, and 81 planned group tests.

Figures regenerated from the same numerical results can differ in embedded rendering metadata; the numerical tables and verification checks are the primary reproducibility targets.

## Automated acquisition

`python3.12 reproduce.py` acquires the 92 inputs not bundled in the clone from OpenNeuro and OSF, verifies the original 423-file package, and runs in an isolated directory. Pinned URLs and source hashes are in `reproduction/sources.json`. The existing LEMON and CAP extracts remain in the clone. No additional health data are redistributed by this change.
