# Result artifacts

`results/` is the frozen machine-readable audit record for the completed run.

- `*_subject*.csv` and `*_windows.csv`: subject/window-level derived observations.
- `*_tests.csv`: inferential tables, including multiplicity-corrected values.
- `*_manifest*.json`: acquisition and inclusion/exclusion records.
- `*_complete.json` and `verification.json`: completion receipts and expected counts.
- `*.npz`: derived spectral/model caches used to make the report and figures.
- `*.log`: retained execution logs.
- `*.svg` and `*.png`: generated figures; numerical tables are authoritative.

`python verify_run.py` checks the reported row and participant counts. Use
`python make_figures.py` and `python build_report.py` to regenerate presentation
artifacts from these results.

