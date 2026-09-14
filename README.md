# ADAP — ad-alpha-parameterization

Reproducible research repository for the Minier EEG alpha-pattern experiments and the September 14, 2026 control run.

## Current result

The source-cohort posterior alpha finding remained lower in AD across the first, middle, and last one-minute source periods after correction. The posterior/frontal difference also persisted across those three periods when an individualized frequency band was centered on each participant's eligible posterior spectral peak. Candidate peak-frequency differences themselves did not survive correction.

The frozen score is state-sensitive in healthy controls. In LEMON, eyes opening increased the score in **30/34** paired older healthy participants (Holm-corrected p ≈ **0.0008**). In CAP, stage-2 theta/alpha increased in **11/11** eligible paired participants (Holm-corrected p ≈ **0.004**). These are physiological sensitivity controls, not evidence that sleep or eye state caused the AD/control result.

The analyses do **not** establish Alzheimer specificity, cholinergic damage, synaptic loss, amyloid/tau mechanism, or impaired AD alpha reactivity. The AD recordings used here contain eyes-closed data only.

Start with [`FINDINGS.md`](FINDINGS.md), [`MATH.md`](MATH.md), [`LIMITATIONS_PARAGRAPH.md`](LIMITATIONS_PARAGRAPH.md), and [`LITERATURE_CONTEXT.md`](LITERATURE_CONTEXT.md).

## What is versioned here

This repository contains the audit layer of the completed control package: analysis and acquisition code, frozen plans and protocol amendments, dependency lock, execution receipt, exact subject-level/statistical result tables, inclusion/exclusion manifests, figures, the illustrated report, result binaries, and the package `SHA256SUMS` manifest.

The CAP extracts that were uploaded separately have been restored to their original package locations under `data/cap/` and `data/cap_first30_pilot/`. Other large waveform/source inputs may still need to be reacquired or reconstructed from the cited public datasets. Their source identities, selection rules, extraction/acquisition code, and expected hashes are recorded here.

The package's original README is preserved byte-for-byte as [`PACKAGE_README.md`](PACKAGE_README.md); the repository README you are reading distinguishes what is actually present in Git from what exists in the larger completed package.

See [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md) and [`REPRODUCE.md`](REPRODUCE.md).

## Verify the repository snapshot

From a clean clone:

```bash
python verify_repository.py
```

This validates every manifest-listed file that is available in the repository. The verifier maps the package manifest's `README.md` entry to `PACKAGE_README.md`, because the root README is repository-level documentation. Missing external/reconstructed `data/` assets are reported separately; any missing non-data audit artifact or hash mismatch is an error.

## Full signal-level reproduction

Use Python 3.12 and the pinned environment:

```bash
python -m pip install -r requirements-lock.txt
```

Acquire/reconstruct the remaining documented EEG inputs as described in [`REPRODUCE.md`](REPRODUCE.md), then run:

```bash
python validate_spectral_fit.py
python spectral_controls.py
python individual_peak_controls.py
python state_controls.py
python make_figures.py
python build_report.py
python verify_run.py
```

`spectral_controls.py --extract /path/to/full/OpenNeuro/derivatives` rebuilds the first/middle/last 60-second source snippets from the full OpenNeuro derivatives.

## Data sources

- OpenNeuro ds004504 v1.0.9: https://openneuro.org/datasets/ds004504/versions/1.0.9
- Florida OSF dataset: https://osf.io/2v5md/
- MPI-LEMON: https://fcon_1000.projects.nitrc.org/indi/retro/MPI_LEMON.html
- CAP Sleep Database: https://physionet.org/content/capslpdb/1.0.0/
- Spectral model reference: Donoghue et al. 2020, DOI 10.1038/s41593-020-00744-x
- Relevant EEG/MRI precedent: Schumacher et al. 2020, DOI 10.1186/s13195-020-00613-6

Original data licenses and attribution requirements apply. No blanket relicensing of third-party EEG recordings is asserted here.

## Scope

This is retrospective research analysis, not a validated clinical diagnostic device. Statistical intervals are pointwise. Documented amendments are preserved rather than hidden, and healthy-state controls are interpreted as sensitivity analyses rather than perfectly matched disease controls.
