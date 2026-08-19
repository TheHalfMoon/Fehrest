#!/usr/bin/env python3
"""Fail-closed verifier for the R1 v1 -> v1.1 execution-plumbing amendment."""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import seal_digest

BASE_HEAD = "685b390d93fd58c65b8d9e33f4869c6c986259d3"
FROZEN_SOURCE_COMMIT = "5902460c2dfe4912825d2adfe62ae8142399f113"
FROZEN_SOURCE_TREE = "501004e0be6630eb2d2a90b196012f9cbb596c5a"
EXPECTED_BASE_BENCHMARK_FILESET = "c7203d3ff0ccdd859a21841ef0cac25b46c5224cf35980cb02fc0c5a1590e28f"
EXPECTED_V1_1_BENCHMARK_FILESET = "5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2"
EXPECTED_EXTERNAL_BUNDLE = "17934f84a07afef08e469b0526d343d26e5597ea3455e575b5f9c46ae91c321e"
EXPECTED_RUNNER_FILESET = "30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f"

ALLOWED_CHANGED_PATHS = {
    "bench/R1/ADDENDUM-X1.md",
    "bench/R1/HANDOFF.md",
    "bench/R1/PREREGISTRATION-V1.1.md",
    "bench/R1/STATUS.md",
    "bench/R1/external-runner/.gitignore",
    "bench/R1/external-runner/README.md",
    "bench/R1/external-runner/r1_runner.py",
    "bench/R1/external-runner/test_r1_runner.py",
    "bench/R1/harness/main.rs",
    "bench/R1/seal_digest.py",
    "bench/R1/verify_v1_1.py",
}
FROZEN_FUNCTIONS = (
    "parse_scenario",
    "load_scenarios",
    "load_tasks",
    "load_oracles",
    "fold_maintenance",
    "arm_b0",
    "arm_b1",
    "arm_b3",
    "arm_b4",
    "arm_b5",
    "parse_response",
    "score_one",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=repo)


def function_bytes(source: str, name: str) -> bytes:
    match = re.search(rf"(?m)^fn\s+{re.escape(name)}\s*\(", source)
    if match is None:
        raise RuntimeError(f"function not found: {name}")
    start = match.start()
    brace = source.find("{", match.end())
    if brace < 0:
        raise RuntimeError(f"opening brace not found: {name}")
    depth = 0
    in_string = False
    escaped = False
    for i in range(brace, len(source)):
        ch = source[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                while end < len(source) and source[end] in " \t":
                    end += 1
                if end < len(source) and source[end] == "\r":
                    end += 1
                if end < len(source) and source[end] == "\n":
                    end += 1
                return source[start:end].encode("utf-8")
    raise RuntimeError(f"closing brace not found: {name}")


def changed_paths(repo: Path) -> set[str]:
    committed_or_tracked = set(
        git(repo, "diff", "--name-only", BASE_HEAD, "--").decode().splitlines()
    )
    untracked = set(
        git(repo, "ls-files", "--others", "--exclude-standard").decode().splitlines()
    )
    return {p for p in committed_or_tracked | untracked if p}


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    r1 = repo / "bench" / "R1"
    harness_rel = "bench/R1/harness/main.rs"
    failed = 0

    # The amendment must descend from the exact pre-outcome base, never replace it.
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_HEAD, "HEAD"], cwd=repo
    ).returncode == 0
    print(f"BASE_HEAD_ANCESTOR_STATUS={'PASS' if ancestor else 'FAIL'}")
    failed += int(not ancestor)

    base = git(repo, "show", f"{BASE_HEAD}:{harness_rel}").decode("utf-8")
    current = (repo / harness_rel).read_text(encoding="utf-8")
    for name in FROZEN_FUNCTIONS:
        before = function_bytes(base, name)
        after = function_bytes(current, name)
        same = before == after
        print(
            f"FROZEN_FUNCTION={name} STATUS={'PASS' if same else 'FAIL'} "
            f"BASE_SHA256={sha256(before)} CURRENT_SHA256={sha256(after)}"
        )
        failed += int(not same)

    source_tree = git(repo, "rev-parse", f"{FROZEN_SOURCE_COMMIT}:src").decode().strip()
    current_source_tree = git(repo, "rev-parse", "HEAD:src").decode().strip()
    source_ok = source_tree == FROZEN_SOURCE_TREE and current_source_tree == FROZEN_SOURCE_TREE
    print(f"FROZEN_SOURCE_TREE_STATUS={'PASS' if source_ok else 'FAIL'} TREE={current_source_tree}")
    failed += int(not source_ok)

    # Compare product bytes against X0, not merely against the working index. This
    # remains meaningful after the amendment is committed.
    product_diff = git(
        repo, "diff", BASE_HEAD, "--", "src/", "tests/", "Cargo.toml", "Cargo.lock"
    )
    product_clean = not product_diff
    print(f"PRODUCT_FILES_CHANGED={'NO' if product_clean else 'YES'}")
    failed += int(not product_clean)

    observed_paths = changed_paths(repo)
    scope_ok = observed_paths == ALLOWED_CHANGED_PATHS
    print(f"CHANGE_SCOPE_STATUS={'PASS' if scope_ok else 'FAIL'}")
    if not scope_ok:
        print(f"CHANGE_SCOPE_MISSING={sorted(ALLOWED_CHANGED_PATHS - observed_paths)}")
        print(f"CHANGE_SCOPE_UNEXPECTED={sorted(observed_paths - ALLOWED_CHANGED_PATHS)}")
    failed += int(not scope_ok)

    base_manifest = seal_digest.canonical_manifest(
        r1, seal_digest.BENCHMARK_FILES, BASE_HEAD
    )
    base_digest = sha256(base_manifest)
    base_digest_ok = base_digest == EXPECTED_BASE_BENCHMARK_FILESET
    print(
        f"ORIGINAL_CANONICAL_FILESET_STATUS={'PASS' if base_digest_ok else 'FAIL'} "
        f"SHA256={base_digest}"
    )
    failed += int(not base_digest_ok)

    current_manifest = seal_digest.canonical_manifest(r1, seal_digest.BENCHMARK_FILES)
    current_digest = sha256(current_manifest)
    current_digest_ok = current_digest == EXPECTED_V1_1_BENCHMARK_FILESET
    print(
        f"V1_1_CANONICAL_FILESET_STATUS={'PASS' if current_digest_ok else 'FAIL'} "
        f"SHA256={current_digest}"
    )
    failed += int(not current_digest_ok)

    bundle_digest = sha256((r1 / "dist" / "r1-external-bundle.tar.gz").read_bytes())
    bundle_ok = bundle_digest == EXPECTED_EXTERNAL_BUNDLE
    print(f"EXTERNAL_BUNDLE_STATUS={'PASS' if bundle_ok else 'FAIL'} SHA256={bundle_digest}")
    failed += int(not bundle_ok)

    runner_manifest = seal_digest.canonical_manifest(r1, seal_digest.RUNNER_FILES)
    runner_digest = sha256(runner_manifest)
    runner_ok = runner_digest == EXPECTED_RUNNER_FILESET
    print(
        f"RUNNER_CANONICAL_FILESET_STATUS={'PASS' if runner_ok else 'FAIL'} "
        f"SHA256={runner_digest}"
    )
    failed += int(not runner_ok)

    print(f"V1_1_SEMANTIC_FREEZE_STATUS={'PASS' if failed == 0 else 'FAIL'}")
    return int(failed != 0)


if __name__ == "__main__":
    raise SystemExit(main())
