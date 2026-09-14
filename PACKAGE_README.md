# Minier EEG: spectral and healthy-state controls

Run in Python 3.12 after installing `requirements-lock.txt`:

```
python validate_spectral_fit.py
python spectral_controls.py
python individual_peak_controls.py
python state_controls.py
python make_figures.py
```

The included waveform extracts allow offline analysis after dependency installation. Download scripts are acquisition/provenance tools and are not required to reproduce the statistical results from the included inputs. `spectral_controls.py --extract /path/to/full/OpenNeuro/derivatives` rebuilds the source60 snippets if they are absent. Original full-length source recordings are in the earlier full data package.

Read FINDINGS.md for the outcome and limitations, PLAN.json and the separately recorded metadata/ECG amendments for choices, MATH.md for formulas, and results/ for all subject-level observations and tests. This is research analysis, not a calibrated clinical diagnostic device.

## Inputs and exclusions

- OpenNeuro ds004504 v1.0.9: all88 source derivative recordings, first8seconds plus first/middle/last60second snippets. AD36 vs control29 is primary; AD36 vsFTD23 is the disease-specificity comparison. Full source hashes and extraction indices are included.
- Florida OSF2v5md original EEG_data.zip revision1: AD80/control12, all eight-second eyes-closed recordings, all19 named channels. No longer Florida recordings are created or assumed.
- LEMON: all74 older entries in the published participant table are considered. Include only available paired preprocessed EC/EO files with all19 required channels and enough boundary-free windows. The alias mapping is T3/T7,T4/T8,T5/P7,T6/P8. Missing electrodes are never interpolated. Actual inclusion/exclusion receipts are included. Analyzed data are the first60seconds of each concatenated condition, not a continuous alternation experiment recreated from raw markers.
- CAP: all16 healthy IDs are considered. Up to10 first complete30second epochs per W/S1/S2 state anywhere in the recording, following the documented metadata-driven amendment; the original first30minute pilot often preceded the scored data. Each state requires3epochs for paired inference. Use a recorded same-reference frontal/occipital pair, or the explicitly documented exact bipolar-chain identities. Missing signals are never inferred from scalp coordinates. Sleep states are externally scored, not inferred using our alpha score.

No new Alzheimer's test cohort is introduced by LEMON or CAP; these are healthy-state sensitivity controls. Recording setups differ, so absolute levels across datasets are not treated as directly comparable.

## Data sources and methods

- Source documentation: https://github.com/OpenNeuroDatasets/ds004504
- Source release: https://openneuro.org/datasets/ds004504/versions/1.0.9
- Florida: https://osf.io/2v5md/
- LEMON portal and terms: https://fcon_1000.projects.nitrc.org/indi/retro/MPI_LEMON.html
- LEMON EEG acquisition instructions and original direct download addresses are in documentation/EEG_Info and the saved S3 listings. LEMON is distributed under PDDL according to the portal.
- CAP: https://physionet.org/content/capslpdb/1.0.0/ . Open Data Commons Attribution License v1.0. Cite Terzano et al., Atlas, rules, and recording techniques for the scoring of cyclic alternating pattern (CAP) in human sleep, Sleep Medicine2(6):537–553,2001, and the PhysioNet resource.
- Spectral model: Donoghue et al.2020, https://doi.org/10.1038/s41593-020-00744-x . Pinned FOOOF1.1.1 is used for numerical reproducibility; its deprecation notice is not a fit failure.

Original data terms apply. Files include the exact resampled analysis extracts, not full LEMON/CAP recordings. Source URLs, byte ranges, hashes, metadata, and extraction scripts document their origin. Range hashes authenticate downloaded portions rather than claiming a whole-file hash.

After the analysis commands, run `python build_report.py` and `python verify_run.py`. The input SHA256SUMS file authenticates the supplied package bytes; figures regenerated later can differ in embedded rendering metadata while preserving the numerical results.
