#!/usr/bin/env python3
"""P0 Runes Keystone Baseline smoke."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "wiki" / "k6-freelancer" / "baseline-p0-runes-keystone.md"
M82 = ROOT / "wiki" / "k6-freelancer" / "verification-m82.md"
OBS = ROOT / "wiki" / "k6-freelancer" / "verification-post-p0-trial-use.md"
TRIAL = ROOT / "wiki" / "k6-freelancer" / "post-p0-trial-use.md"


def has(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(encoding="utf-8")


def main() -> int:
    issues: list[str] = []

    if not BASELINE.exists():
        issues.append("missing baseline-p0-runes-keystone.md")
    else:
        text = BASELINE.read_text(encoding="utf-8")
        required = [
            "P0 Runes Keystone Baseline",
            "Codename: P0 Runes Keystone",
            "M82 P0 Governed Memory Operating Baseline",
            "T001-T004 Post-P0 Trial-use Observation Lock",
            "PASS / frozen / smoke verified / observation baseline",
            "personal-local",
            "Markdown-native",
        ]
        for marker in required:
            if marker not in text:
                issues.append(f"missing baseline marker: {marker}")

    if not has(M82, "PASS / frozen / smoke verified"):
        issues.append("M82 source is not frozen")
    if not has(OBS, "PASS / smoke verified / observation baseline"):
        issues.append("observation lock source missing")
    if not has(TRIAL, "T004 Known Limitation / Future Task Candidate"):
        issues.append("trial-use T004 source missing")

    result = {
        "smoke_version": "p0-runes-keystone-baseline-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "p0-runes-keystone-baseline",
        "codename": "P0 Runes Keystone",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "baseline_components": ["M82", "T001-T004 observation lock"],
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
