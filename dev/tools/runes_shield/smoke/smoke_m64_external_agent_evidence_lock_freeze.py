#!/usr/bin/env python3

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKES = [
    {
        "id": "m64_1_evidence_classification",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m64_evidence_classification.py",
    },
    {
        "id": "m64_2_evidence_retention_boundary",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m64_evidence_retention_boundary.py",
    },
    {
        "id": "m64_3_public_safe_evidence",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m64_public_safe_evidence.py",
    },
    {
        "id": "m64_4_evidence_provenance_verification",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m64_evidence_provenance_verification.py",
    },
    {
        "id": "m64_5_governance_interpretation_consistency",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m64_governance_interpretation_consistency.py",
    },
    {
        "id": "m64_6_evidence_replay_boundary",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m64_evidence_replay_boundary.py",
    },
]


def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_component(smoke):
    issues = []

    if not smoke["path"].exists():
        return {
            "id": smoke["id"],
            "status": "FAIL",
            "write": False,
            "issues": [{"code": "missing_smoke"}],
        }

    try:
        module = load_module(smoke["path"])
        fixture_name = smoke["path"].name.replace("smoke_", "").replace(".py", "")
    except Exception as exc:
        return {
            "id": smoke["id"],
            "status": "FAIL",
            "write": False,
            "issues": [{"code": "component_load_failed", "message": str(exc)}],
        }

    if not hasattr(module, "FIXTURE"):
        issues.append({"code": "missing_fixture_reference"})
    else:
        fixture = json.loads(module.FIXTURE.read_text(encoding="utf-8"))

        if fixture.get("scale") != "personal-local":
            issues.append({"code": "scale_drift"})

        expected = fixture.get("expected_result", {})

        if expected.get("status") != "PASS":
            issues.append({"code": "expected_status_violation"})

        if expected.get("authoritative") is not False:
            issues.append({"code": "authoritative_violation"})

        if expected.get("write") is not False:
            issues.append({"code": "write_violation"})

        if expected.get("issue_count") != 0:
            issues.append({"code": "issue_count_violation"})

    return {
        "id": smoke["id"],
        "status": "PASS" if not issues else "FAIL",
        "write": False,
        "issue_count": len(issues),
        "issues": issues,
    }


def main():
    components = [run_component(smoke) for smoke in SMOKES]
    issues = []

    for component in components:
        if component.get("status") != "PASS":
            issues.append({
                "code": "component_not_pass",
                "component": component.get("id"),
            })

    payload = {
        "smoke_version": "m64.7-external-agent-evidence-lock-freeze-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "external-agent-evidence-lock-freeze",
        "scale": "personal-local",
        "write": False,
        "authoritative": False,
        "freeze_target": "M64 External Agent Evidence Lock",
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
