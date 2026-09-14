#!/usr/bin/env python3
"""Verify the Git snapshot against the completed control-package SHA256 manifest."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"
PATH_ALIASES = {"README.md": "PACKAGE_README.md"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not MANIFEST.exists():
        print("FAIL: SHA256SUMS is missing")
        return 2

    present_ok = 0
    mismatches: list[tuple[str, str, str]] = []
    missing_data: list[str] = []
    missing_audit: list[str] = []

    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        expected, manifest_rel = raw.split(None, 1)
        manifest_rel = manifest_rel.strip()
        repo_rel = PATH_ALIASES.get(manifest_rel, manifest_rel)
        path = ROOT / repo_rel
        if not path.exists():
            if manifest_rel.startswith("data/"):
                missing_data.append(manifest_rel)
            else:
                missing_audit.append(manifest_rel)
            continue
        actual = sha256(path)
        if actual != expected:
            mismatches.append((manifest_rel, expected, actual))
        else:
            present_ok += 1

    print(f"Verified manifest-listed files present in Git: {present_ok}")
    print(f"External/reconstructed data assets absent from Git: {len(missing_data)}")
    print(f"Missing non-data audit artifacts: {len(missing_audit)}")
    print(f"Hash mismatches: {len(mismatches)}")

    if missing_data:
        print("\nStill-required external/reconstructed inputs (first 25 shown):")
        for rel in missing_data[:25]:
            print("  -", rel)
        if len(missing_data) > 25:
            print(f"  ... and {len(missing_data) - 25} more")
    if missing_audit:
        print("\nFAIL — missing non-data audit artifacts:")
        for rel in missing_audit:
            print("  -", rel)
    if mismatches:
        print("\nFAIL — SHA256 mismatches:")
        for rel, expected, actual in mismatches:
            print(f"  - {rel}\n      expected {expected}\n      actual   {actual}")

    verification_path = ROOT / "results" / "verification.json"
    if verification_path.exists():
        print("\nRecorded completed-run verification:")
        print(json.dumps(json.loads(verification_path.read_text(encoding="utf-8")), indent=2))

    if missing_audit or mismatches:
        return 1
    print("\nPASS: every available manifest-listed artifact matches the completed package,")
    print("and no non-data audit artifact is missing.")
    if missing_data:
        print("A complete signal-level rerun still requires the data/ inputs listed above.")
    else:
        print("All manifest-listed inputs are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
