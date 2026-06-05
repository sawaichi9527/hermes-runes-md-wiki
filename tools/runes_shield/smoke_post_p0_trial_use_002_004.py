#!/usr/bin/env python3
"""Post-P0 trial-use T002-T004 smoke."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRIAL = ROOT / "wiki" / "k6-freelancer" / "post-p0-trial-use.md"


def main() -> int:
    issues: list[str] = []

    if not TRIAL.exists():
        issues.append("missing post-p0 trial-use record")
    else:
        text = TRIAL.read_text(encoding="utf-8")

        required_markers = [
            "T002 Design Decision Memory Candidate",
            "T003 Operational Workflow Memory Candidate",
            "T004 Known Limitation / Future Task Candidate",
            "post-p0-trial-use-t002",
            "post-p0-trial-use-t003",
            "post-p0-trial-use-t004",
            "enterprise workflow expansion",
            "Markdown-native and deterministic",
            "real-world observation",
        ]

        for marker in required_markers:
            if marker not in text:
                issues.append(f"missing marker: {marker}")

        if text.count("secret_content: false") < 4:
            issues.append("expected 4 secret_content flags")

        if text.count("runtime_change: false") < 4:
            issues.append("expected 4 runtime_change flags")

    result = {
        "smoke_version": "post-p0-trial-use-002-004-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "post-p0-trial-use-002-004",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "trial_case_count": 3,
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
