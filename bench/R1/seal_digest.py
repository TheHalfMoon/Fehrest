#!/usr/bin/env python3
"""Portable R1 v1.1 fileset digests.

The legacy v1 document published an aggregate digest plus a shell pipeline whose
aggregate bytes were not fully specified across platforms. v1.1 keeps that legacy
identifier as historical evidence and uses this canonical UTF-8/LF manifest rule for
new seals. This script never reads model output or credentials.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

BENCHMARK_FILES = (
    "MAINTENANCE.md",
    "PROTOCOL.md",
    "harness/main.rs",
    "oracles/oracles.json",
    "scenarios/S1-beacon.scn",
    "scenarios/S2-marisol.scn",
    "scenarios/S3-harbor.scn",
    "tasks/tasks.json",
)
RUNNER_FILES = (
    "external-runner/.gitignore",
    "external-runner/README.md",
    "external-runner/r1_runner.py",
    "external-runner/test_r1_runner.py",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(repo: Path, ref: str, repo_rel: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{repo_rel}"], cwd=repo
    )


def canonical_manifest(
    r1: Path, files: tuple[str, ...], git_ref: str | None = None
) -> bytes:
    repo = r1.parent.parent
    lines: list[str] = []
    for rel in sorted(files):
        if git_ref is None:
            data = (r1 / rel).read_bytes()
        else:
            data = git_bytes(repo, git_ref, f"bench/R1/{rel}")
        lines.append(f"{sha256(data)}  {rel}\n")
    return "".join(lines).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("benchmark", "runner"))
    parser.add_argument("--r1", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--git-ref")
    args = parser.parse_args()

    files = BENCHMARK_FILES if args.kind == "benchmark" else RUNNER_FILES
    manifest = canonical_manifest(args.r1, files, args.git_ref)
    print(manifest.decode("utf-8"), end="")
    print(f"CANONICAL_FILESET_SHA256={sha256(manifest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
