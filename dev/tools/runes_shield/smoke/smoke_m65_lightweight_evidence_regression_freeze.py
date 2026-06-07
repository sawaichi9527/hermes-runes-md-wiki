#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

COMPONENTS = [
    "smoke_m65_governance_regression_baseline.py",
    "smoke_m65_replay_boundary_regression.py",
    "smoke_m65_wrapper_interpretation_regression.py",
    "smoke_m65_provenance_regression.py",
    "smoke_m65_retention_public_safe_regression.py",
]


def main():
    issues = []
    components = []

    for filename in COMPONENTS:
        path = ROOT / "tools" / "runes_shield" / filename

        component = {
            "id": filename.replace("smoke_", "").replace(".py", ""),
            "status": "PASS",
            "write": False,
            "exists": path.exists(),
        }

        if not path.exists():
            component["status"] = "FAIL"
            component["issues"] = ["missing_component"]
            issues.append({
                "code": "missing_component",
                "component": filename,
            })
        else:
            component["issues"] = []

        components.append(component)

    payload = {
        "smoke_version": "m65.6-lightweight-evidence-regression-freeze-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "lightweight-evidence-regression-freeze",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "freeze_target": "M65 Lightweight Evidence Regression Preservation",
        "component_count": len(components),
        "components": components,
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
