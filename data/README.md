# Data layout and provenance

This directory is the only canonical location for analysis inputs. Files from the
four source datasets remain governed by their original licenses and terms. Their
presence in this repository does not relicense them.

| Path | Cohort / role | Versioned here | Rebuild or acquisition route |
|---|---|---:|---|
| `participants.tsv` | OpenNeuro ds004504 labels | No | Acquire ds004504 v1.0.9 |
| `openneuro_first8s_waveforms.npz` | Frozen 8-second OpenNeuro waveforms | No | Reconstruct from ds004504 v1.0.9 |
| `source60/` | First/middle/last 60-second OpenNeuro derivatives | No | `python spectral_controls.py --extract PATH_TO_DERIVATIVES` |
| `EEG_data.zip` | Florida OSF AD/healthy recordings | No | Acquire the recorded revision from OSF 2v5md |
| `lemon/` | MPI-LEMON EC/EO inputs and acquisition records | Partially | `python download_lemon.py` |
| `cap/` | Final CAP W/S1/S2 extracts and records | Yes, where listed | `python download_cap.py` |
| `cap_first30_pilot/` | Superseded CAP pilot, retained for audit | Yes, where listed | Historical only; do not use for final inference |

Run `python verify_repository.py` for the authoritative, hash-based inventory. It
distinguishes available files from the external inputs still required for a full
rerun. `SHA256SUMS` at the repository root records the completed package hashes.

Do not add new raw participant data to Git without first checking the source
license, consent/data-use conditions, de-identification status, and file size.

