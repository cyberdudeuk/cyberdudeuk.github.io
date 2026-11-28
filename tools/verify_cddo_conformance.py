#!/usr/bin/env python3
"""Run the pinned GDS-DTX conformance checker against exact public CDDO snapshots.

This is read-only with respect to the source repositories. It clones the source
commits into a temporary directory, runs the catalogue checker's self-test and
--write locally, then compares the resulting checks/verdicts with the committed
portfolio evidence.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGUE = "https://github.com/cyberdudeuk/github-repos-asset-catalogue.git"
CATALOGUE_SHA = "229057ee48f9c7485b7fae49d01438dce3d7cebb"
TARGETS = {
    "mog-navigator": ("co-cddo/MoG-Navigator", "fefdc8e98d2f7e58e95483f505dc1046bec6482e"),
    "ocdo-data-foundations": ("co-cddo/ocdo-data-foundations", "39a05f88e554884a9ab6a1975d26114f6e93c3e4"),
    "ukgov-metadata-exchange-model": ("co-cddo/ukgov-metadata-exchange-model", "3e6c6f5eb6dda6e90ca956d0273f3698fd584212"),
}


def run(args: list[str], *, cwd: pathlib.Path | None = None, allowed_codes: tuple[int, ...] = (0,)) -> str:
    result = subprocess.run(args, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode not in allowed_codes:
        raise subprocess.CalledProcessError(result.returncode, args, output=result.stdout)
    return result.stdout


def checkout(url: str, sha: str, destination: pathlib.Path) -> None:
    destination.mkdir(parents=True)
    run(["git", "init", str(destination)])
    run(["git", "-C", str(destination), "remote", "add", "origin", url])
    run(["git", "-C", str(destination), "fetch", "--depth=1", "origin", sha])
    run(["git", "-C", str(destination), "checkout", "--detach", "FETCH_HEAD"])


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="gds-dtx-conformance-") as tmp:
        temp = pathlib.Path(tmp)
        catalogue = temp / "catalogue"
        checkout(CATALOGUE, CATALOGUE_SHA, catalogue)
        checker = catalogue / "tools" / "conformance.py"
        if not checker.is_file():
            raise RuntimeError("Pinned catalogue commit does not contain tools/conformance.py")

        self_test = run([sys.executable, "-I", str(checker), "--self-test"])
        print(self_test, end="")

        for slug, (full_name, sha) in TARGETS.items():
            source = temp / slug
            checkout(f"https://github.com/{full_name}.git", sha, source)
            meta_path = ROOT / "docs" / "portfolio" / "conformance" / slug / "meta.json"
            expected_path = ROOT / "docs" / "portfolio" / "conformance" / slug / "result.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            expected = json.loads(expected_path.read_text(encoding="utf-8"))

            output = run([
                sys.executable, "-I", str(checker), str(source),
                "--meta", str(meta_path), "--write"
            ], allowed_codes=(0, 1))
            print(output, end="")

            generated = json.loads((source / "docs" / "conformance" / "result.json").read_text(encoding="utf-8"))
            if generated["repo"] != full_name:
                raise AssertionError(f"{slug}: generated repository name mismatch")
            if generated["checks"] != expected["checks"]:
                for check in sorted(set(generated["checks"]) | set(expected["checks"])):
                    if generated["checks"].get(check) != expected["checks"].get(check):
                        print(f"MISMATCH {slug} {check}: generated={generated['checks'].get(check)!r}; committed={expected['checks'].get(check)!r}")
                raise AssertionError(f"{slug}: check results differ from committed evidence")
            if generated["verdict"] != expected["verdict"]:
                raise AssertionError(f"{slug}: verdict differs: {generated['verdict']} != {expected['verdict']}")
            if meta["full_name"] != full_name:
                raise AssertionError(f"{slug}: metadata repository name mismatch")
            print(f"PASS replay comparison: {full_name} at {sha}; {len(generated['checks'])} checks; {generated['verdict']['verdict']}")

    print("PASS all three pinned source snapshots match the committed checker-equivalent reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
