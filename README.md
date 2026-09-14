# ADAP — ad-alpha-parameterization

Reproducible research materials for the Minier EEG alpha-pattern analysis and its control experiments.

## Current result

The source-cohort posterior alpha finding survives the tested individualized-frequency adjustment across the first, middle, and last one-minute source periods. The frozen spatial score is also sensitive to ordinary physiological state changes: in older healthy LEMON participants it increased with eyes open in 30/34 paired participants (Holm-corrected p ≈ 0.0008), and CAP stage-2 sleep increased theta/alpha in 11/11 eligible participants (Holm-corrected p ≈ 0.004). These controls establish state sensitivity; they do not establish Alzheimer specificity, cholinergic damage, synaptic loss, or impaired AD alpha reactivity.

Start with:

- [`EEG_Control_Runs/FINDINGS.md`](EEG_Control_Runs/FINDINGS.md)
- [`EEG_Control_Runs/MATH.md`](EEG_Control_Runs/MATH.md)
- [`EEG_Control_Runs/LIMITATIONS_PARAGRAPH.md`](EEG_Control_Runs/LIMITATIONS_PARAGRAPH.md)
- [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md)

## Experiments

| Directory | Purpose |
| --- | --- |
| `EEG_Control_Runs/` | Latest source-window, individualized-frequency, healthy eye-opening, sleep-stage, and limited ECG sensitivity analyses |
| `EEG_Factor_Tests/` | Original alpha-pattern factor analysis and external Florida comparison |
| `EEG_Geometry_Test/` | Electrode mapping and spatial-geometry sensitivity analysis |

## Reproduce the latest analyses

Use Python 3.12 and the pinned environment in `EEG_Control_Runs/requirements-lock.txt`.

```bash
cd EEG_Control_Runs
python -m pip install -r requirements-lock.txt
python validate_spectral_fit.py
python spectral_controls.py
python individual_peak_controls.py
python state_controls.py
python make_figures.py
python build_report.py
python verify_run.py
```

The repository versions the analysis code, frozen decisions/amendments, subject-level numerical outputs, provenance, checksums, and vector figures needed to audit the work. Large waveform caches and full third-party source recordings are not treated as ordinary Git source files; acquisition/reconstruction instructions and hashes are provided in `DATA_AVAILABILITY.md` and the experiment manifests.

## Scientific scope

This is retrospective research analysis, not a validated clinical diagnostic device. The AD recordings contain eyes-closed data only. Healthy eye-opening and sleep-stage datasets are physiological sensitivity controls, not matched AD controls. The analyses do not measure amyloid, tau, cholinergic integrity, synaptic loss, or causal mechanism.

A directly relevant EEG/MRI precedent is Schumacher et al. (2020), DOI: 10.1186/s13195-020-00613-6. That literature supports a biological hypothesis; it does not convert the present observations into a mechanistic measurement.
