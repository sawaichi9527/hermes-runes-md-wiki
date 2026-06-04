#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPONENTS = [
    "smoke_m66_lightweight_governance_drift_observation.py",
    "smoke_m66_wrapper_drift_observation.py",
    "smoke_m66_replay_boundary_drift_observation.py",
    "smoke_m66_provenance_boundary_drift_observation.py",
    "smoke_m66_retention_public_safe_drift_observation.py",
]


def main():
    issues = []
    components = []

    for filename in COMPONENTS:
        path = ROOT / "tools" / "runes_shield" / filename
        component = {
            "id": filename.replace("smoke_", "").replace(".py", ""),
            "status": "PASS" if path.exists() else "FAIL",
            "exists": path.exists(),
            "write": False,
            "authoritative": False,
        }

        if not path.exists():
            component["issues"] = ["missing_component"]
            issues.append({
                "code": "missing_component",
                "component": filename,
            })
        else:
            component["issues"] = []

        components.append(component)

    payload = {
        "smoke_version": "m66.6-lightweight-governance-drift-observation-freeze-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "lightweight-governance-drift-observation-freeze",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "observation_only": True,
        "freeze_target": "M66 Lightweight Governance Drift Observation",
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
