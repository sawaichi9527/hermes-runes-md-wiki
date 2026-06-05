#!/usr/bin/env python3
"""Post-P0 trial-use observation lock smoke."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRIAL = ROOT / "wiki" / "k6-freelancer" / "post-p0-trial-use.md"
LOCK = ROOT / "wiki" / "k6-freelancer" / "verification-post-p0-trial-use.md"


def main() -> int:
    issues: list[str] = []

    if not TRIAL.exists():
        issues.append("missing post-p0-trial-use.md")

    if not LOCK.exists():
        issues.append("missing verification-post-p0-trial-use.md")
    else:
        text = LOCK.read_text(encoding="utf-8")

        required = [
            "T001: P0 baseline fact",
            "T002: design decision",
            "T003: operational workflow",
            "T004: known limitation / future task",
            "PASS / smoke verified / observation baseline",
            "personal-local",
            "Markdown-native",
        ]

        for marker in required:
            if marker not in text:
                issues.append(f"missing marker: {marker}")

    result = {
        "smoke_version": "post-p0-trial-use-lock-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "post-p0-trial-use-lock",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "locked_trial_case_count": 4,
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
