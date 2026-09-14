# ADAP — EEG alpha-pattern experiments

Reproducible research materials for the Minier EEG alpha-pattern analysis, including analysis-ready waveform extracts, electrode mappings, mathematical definitions, statistical results, figures, and acquisition provenance.

## Experiments

| Directory | Purpose |
| --- | --- |
| [EEG_Control_Runs](EEG_Control_Runs/README.md) | Latest spectral, individualized-frequency, healthy eye-opening, sleep, and limited ECG sensitivity analyses |
| [EEG_Factor_Tests](EEG_Factor_Tests/REPORT.md) | Original alpha-pattern factor analysis and external Florida comparison |
| [EEG_Geometry_Test](EEG_Geometry_Test/REPORT.md) | Open electrode mapping and spatial geometry sensitivity analysis |

Start with [the latest findings](EEG_Control_Runs/FINDINGS.md), [mathematics](EEG_Control_Runs/MATH.md), and [limitations](EEG_Control_Runs/LIMITATIONS_PARAGRAPH.md). Download `EEG_Control_Runs/REPORT.html` and open it locally for the illustrated report.

## Scientific scope

The source AD group showed lower posterior alpha power in the first, middle, and last one-minute recording periods after multiple-comparison correction. The posterior/frontal difference persisted with individualized frequency bands among participants with detectable peaks. Healthy eye opening changed the frozen score, demonstrating state sensitivity. The sleep analysis is a physiological sensitivity reference, not a matched AD control or a quantitative bound on microsleep contamination.

These observational analyses do not establish a cellular cause, AD specificity, or AD alpha reactivity. The AD recordings contain eyes-closed data only. This repository is research material, not a validated clinical diagnostic device.

## Reproduce the latest analyses

Use Python 3.12. From the repository root:

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

For each earlier experiment, install its own `requirements-lock.txt` in a separate environment and run its `run.py`. `audit_metrics.py` is a shared utility module; it is not the entry point for these experiment folders.

The included extracts support offline analysis after installing dependencies. Full-length OpenNeuro, LEMON, and CAP recordings are not duplicated here. Download scripts and provenance document acquisition and extraction; the original Florida archive is included. Original dataset licenses and attribution requirements apply; see each experiment's documentation. No blanket license is asserted over third-party data.

## Integrity and downloadable package

Each experiment preserves its original checksum manifest and receipts. GitHub's **Code → Download ZIP** provides the repository with the scripts, data extracts, graphs, mathematics, and results. Regenerating figures may change embedded rendering metadata without changing numerical results.
