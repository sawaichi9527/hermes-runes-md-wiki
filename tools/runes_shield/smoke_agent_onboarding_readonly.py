#!/usr/bin/env python3
"""Read-only smoke test for Hermes-agent onboarding guide readiness.

This smoke test does not start Hermes-agent, does not mutate trusted memory,
and does not touch PostgreSQL. It only validates that the local repository
contains the guide files and onboarding prompt required for a human-triggered
Hermes-agent read-only onboarding trial.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "wiki/README.md",
    "wiki/hermes_runes_index.md",
    "wiki/_system/README.md",
    "wiki/_system/runes_shield_contract.md",
    "wiki/_system/runes_invocation_policy.md",
    "wiki/_system/memory-policy.md",
    "wiki/_system/security-policy.md",
    "docs/fresh-install-manual.md",
]

REQUIRED_PROMPT_MARKERS = [
    "## Hermes-agent onboarding prompt",
    "請讀取 ~/workspace/hermes-runes-md-wiki",
    "專案用途",
    "Hermes-agent 如何接入",
    "recall 怎麼用",
    "memory proposal 怎麼建立",
    "哪些操作禁止",
    "請不要修改任何檔案",
    "不要直接寫入 trusted wiki",
    "不要保存 secrets",
    "./bin/hermes-backend-check",
    "./bin/hermes-recall",
    "./bin/hermes-memory-smoke",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run(root: Path) -> dict[str, Any]:
    root = root.resolve()
    failures: list[dict[str, str]] = []
    checked_files: list[str] = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            failures.append({
                "check": "required_file_exists",
                "path": rel,
                "reason": "missing",
            })
            continue
        if not path.is_file():
            failures.append({
                "check": "required_file_is_file",
                "path": rel,
                "reason": "not_a_file",
            })
            continue
        try:
            _read_text(path)
        except UnicodeDecodeError:
            failures.append({
                "check": "required_file_utf8",
                "path": rel,
                "reason": "not_utf8",
            })
            continue
        checked_files.append(rel)

    install_guide = root / "docs/fresh-install-manual.md"
    if install_guide.exists():
        text = _read_text(install_guide)
        for marker in REQUIRED_PROMPT_MARKERS:
            if marker not in text:
                failures.append({
                    "check": "onboarding_prompt_marker",
                    "path": "docs/fresh-install-manual.md",
                    "reason": f"missing marker: {marker}",
                })

    status = "PASS" if not failures else "FAIL"
    return {
        "suite": "M209 Hermes-agent Onboarding Read-only Smoke",
        "status": status,
        "write": False,
        "mutates_trusted_memory": False,
        "starts_agent": False,
        "touches_database": False,
        "root": str(root),
        "checked_files": checked_files,
        "required_file_count": len(REQUIRED_FILES),
        "checked_file_count": len(checked_files),
        "required_prompt_marker_count": len(REQUIRED_PROMPT_MARKERS),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to two levels above this script.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON. This is the default-friendly output for automation.",
    )
    args = parser.parse_args()

    if args.root:
        root = Path(args.root)
    else:
        root = Path(__file__).resolve().parents[2]

    result = run(root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['suite']}: {result['status']}")
        if result["failures"]:
            for failure in result["failures"]:
                print(f"- {failure['check']} {failure['path']}: {failure['reason']}")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
