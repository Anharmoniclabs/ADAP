# Recovered original source archive

Recovered on 2026-09-14 from the previously generated Minier_EEG_Reconstruction_Kit.zip.

- `Minier_EEG_Parts.json`: original sizes and SHA-256 hashes for 12 source-archive parts and the assembled archive.
- `Reassemble_Minier_EEG.py`: original offline reassembly/checking script.

Place all 12 parts next to these two files, then run:

```sh
python Reassemble_Minier_EEG.py
```

Expected assembled filename: Minier_EEG_Experiments_20260914_FULL.zip.
Expected size: 2,971,500,461 bytes.
Expected SHA-256: f4dd7fa2d9875151f557886f6016b0e80e7538c5b02ae89f46b568888f35c289.

The parts were located among the user's saved prior artifacts. They are NOT uploaded by this commit, and this document does not provide a public archive download endpoint. Original chat-local sandbox links are not durable public download URLs.

## Separate control-package recovery

The previously generated Minier_EEG_Control_Runs.zip (305,369,812 bytes) was also recovered and extracted locally. Its SHA256SUMS is byte-identical to the root manifest already in this repository. All 423 manifest entries passed `sha256sum -c SHA256SUMS`, including the 92 data inputs absent from the organized Git snapshot.

This establishes recovery and byte-level integrity of the original control package. It is NOT a new end-to-end analysis rerun or independent replication. The source archive's 12 parts were not reassembled during this recovery, so its final hash is a recorded expected hash, not a new verification.

## Remaining public reproducibility work

The 92 recovered data inputs have not been committed by this manifest-recovery change. A fresh Git clone still requires those inputs or a durable, appropriately licensed archive distribution. Data recovery does not establish diagnostic performance or clinical validation.

## Preferred public reproduction route

Use `python3.12 reproduce.py` from the repository root. It fetches original sources directly and reconstructs the recorded inputs. No multipart source pack is required. An existing control ZIP may be supplied with `--control-pack`; a separately hosted pack may be supplied with `--pack-url` and its mandatory `--pack-sha256`. No public pack URL is invented or assumed.
