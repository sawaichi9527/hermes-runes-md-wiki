#!/usr/bin/env python3

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKES = [
    {
        "id": "m63_1_generic_cli_wrapper_validation",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m63_generic_cli_wrapper_validation.py",
        "expected_mode": "generic-cli-wrapper-validation",
    },
    {
        "id": "m63_2_openclaw_compatibility_validation",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m63_openclaw_compatibility_validation.py",
        "expected_mode": "openclaw-style-compatibility-validation",
    },
    {
        "id": "m63_3_openai_compatible_wrapper_validation",
        "path": ROOT / "tools" / "runes_shield" / "smoke_m63_openai_compatible_wrapper_validation.py",
        "expected_mode": "openai-compatible-wrapper-validation",
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
            "issue_count": 1,
            "issues": [{
                "code": "missing_smoke",
                "path": str(smoke["path"].relative_to(ROOT)),
            }],
        }

    try:
        module = load_module(smoke["path"])
        fixture = json.loads(module.FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:  # defensive freeze smoke
        return {
            "id": smoke["id"],
            "status": "FAIL",
            "write": False,
            "issue_count": 1,
            "issues": [{
                "code": "component_load_failed",
                "message": str(exc),
            }],
        }

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "expected": "personal-local",
            "actual": fixture.get("scale"),
        })

    if fixture.get("agent_scope") != "agent-agnostic":
        issues.append({
            "code": "agent_scope_drift",
            "expected": "agent-agnostic",
            "actual": fixture.get("agent_scope"),
        })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("write") is not False:
        issues.append({
            "code": "write_boundary_violation",
            "actual": expected_result.get("write"),
        })

    if expected_result.get("issue_count") != 0:
        issues.append({
            "code": "expected_issue_count_violation",
            "actual": expected_result.get("issue_count"),
        })

    boundaries = fixture.get("required_boundaries", {})
    for key, value in boundaries.items():
        if value is not True:
            issues.append({
                "code": "boundary_violation",
                "boundary": key,
            })

    return {
        "id": smoke["id"],
        "status": "PASS" if not issues else "FAIL",
        "write": False,
        "mode": smoke["expected_mode"],
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
                "component_issues": component.get("issues", []),
            })

        if component.get("write") is not False:
            issues.append({
                "code": "component_write_violation",
                "component": component.get("id"),
            })

    payload = {
        "smoke_version": "m63.4-real-external-agent-trial-freeze-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "real-external-agent-trial-freeze",
        "scale": "personal-local",
        "write": False,
        "freeze_target": "M63 Real External Agent Trial-run",
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
