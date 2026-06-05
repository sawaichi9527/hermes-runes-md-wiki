#!/usr/bin/env python3
"""Post-P0 trial-use T001 smoke."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRIAL = ROOT / "wiki" / "k6-freelancer" / "post-p0-trial-use.md"
M82 = ROOT / "wiki" / "k6-freelancer" / "verification-m82.md"
NEXT = ROOT / "wiki" / "k6-freelancer" / "next-actions.md"


def contains(path: Path, text: str) -> bool:
    return path.exists() and text in path.read_text(encoding="utf-8")


def main() -> int:
    issues: list[str] = []

    if not TRIAL.exists():
        issues.append("missing post-p0 trial-use record")
    else:
        trial_text = TRIAL.read_text(encoding="utf-8")
        for marker in [
            "T001 P0 Baseline Memory Candidate",
            "post-p0-trial-use-t001",
            "verification-m82.md",
            "next-actions.md",
            "secret_content: false",
            "runtime_change: false",
        ]:
            if marker not in trial_text:
                issues.append(f"missing trial marker: {marker}")

    if not contains(M82, "M82 P0 Governed Memory Operating Baseline"):
        issues.append("missing M82 source reference")

    if not contains(NEXT, "Post-P0 Trial-use Observation"):
        issues.append("missing next-actions trial-use reference")

    result = {
        "smoke_version": "post-p0-trial-use-001-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "post-p0-trial-use-001",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "target_path": str(TRIAL.relative_to(ROOT)),
        "source_reference_count": 2,
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
