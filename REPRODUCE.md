# Reproduction guide

This repository separates versioned scientific artifacts from external or reconstructed EEG inputs.

## 1. Verify the Git snapshot

Use Python 3.12 or later:

```bash
python verify_repository.py
```

The checker reads `SHA256SUMS`, validates every manifest-listed file available in the clone, maps the original package `README.md` to `PACKAGE_README.md`, and reports any still-missing `data/` inputs separately. A hash mismatch or a missing non-data analysis artifact is an error.

## 2. Create the pinned environment

```bash
python -m venv .venv
# activate the environment for your platform
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
```

The completed run receipt records Python 3.12.14.

## 3. Inputs

### OpenNeuro ds004504 v1.0.9

All 88 derivative recordings were considered. The primary source contrast is 36 AD versus 29 controls; the secondary disease-specificity contrast is 36 AD versus 23 FTD. Use:

```bash
python spectral_controls.py --extract /path/to/full/OpenNeuro/derivatives
```

to rebuild first/middle/last 60-second snippets when `data/source60/` is absent. The package manifest and extraction receipt define the expected bytes/hashes.

### Florida OSF 2v5md

The completed analysis used the original `EEG_data.zip` revision captured by the package: 80 AD and 12 healthy eyes-closed recordings, eight seconds each, with all 19 named channels. No longer Florida recordings were synthesized or assumed.

### MPI-LEMON

`download_lemon.py`, `lemon_selection_before_scores.json`, and `documentation/` preserve the selection/acquisition logic and source metadata. The final analysis includes only paired EC/EO recordings satisfying the exact 19-channel and boundary-free-window requirements. Missing electrodes are not interpolated.

### CAP Sleep Database

The versioned final CAP extracts are under `data/cap/`; the original first-30-minute pilot is under `data/cap_first30_pilot/`. Read `CAP_MAPPING_AMENDMENT.txt`, `CAP_EPOCH_AMENDMENT.txt`, and `CAP_DOWNLOAD_NOTE.txt` before rerunning acquisition. The final state selection uses up to 10 complete 30-second epochs per W/S1/S2 state anywhere in the recording, with at least 3 epochs required for that state to enter paired inference. Sleep labels come from external annotations, not from the alpha score.

## 4. Run the analysis

```bash
python validate_spectral_fit.py
python spectral_controls.py
python individual_peak_controls.py
python state_controls.py
python make_figures.py
python build_report.py
python verify_run.py
```

Expected final verification counts, recorded in `receipt.json` and `results/verification.json`, are:

- 444 spectral subject-window rows
- 34 paired LEMON participants
- 16 CAP candidates
- 11 CAP recordings included for eligible state analyses
- 8 paired state tests
- 6 individualized-peak tests
- 81 planned group tests

## 5. Audit the claims

Primary machine-readable outputs include:

- `results/spectral_group_tests.csv`
- `results/spectral_subject_windows.csv`
- `results/source_window_stability.csv`
- `results/individual_peak_tests.csv`
- `results/individual_peak_subjects.csv`
- `results/state_tests.csv`
- `results/lemon_subject_states.csv`
- `results/cap_subject_states.csv`
- `results/cap_ecg_sensitivity.csv`
- `results/verification.json`

`REPORT.html` is the human-readable illustrated report. `FINDINGS.md` and `LIMITATIONS_PARAGRAPH.md` state the supported interpretation and explicit limits.

## Reproducibility boundary

A clean clone is sufficient to audit the code, decisions, source/provenance documentation, hashes, and reported numerical outputs. A fresh signal-level rerun additionally requires every input reported as missing by `verify_repository.py`. This boundary is explicit so a GitHub clone is not falsely represented as containing third-party data that are not actually present.
