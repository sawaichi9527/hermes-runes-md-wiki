#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m60" / "summoned-brave-trial-report.json"

EXPECTED_LANGUAGES = {"zh-TW", "en-US"}
EXPECTED_REPORT_MODES = {"PASS", "FAIL"}
EXPECTED_TEMPLATE_VARIABLES = {
    "agent_display_name",
    "optional_title",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "Summoned brave trial report fixture missing",
        })
        payload = {
            "smoke_version": "m60.4-trial-report-smoke-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    if fixture.get("runtime_dependency") is not False:
        issues.append({
            "code": "runtime_dependency_violation",
            "message": "Trial report fixture must remain runtime-independent",
        })

    if fixture.get("memory_dependency") is not False:
        issues.append({
            "code": "memory_dependency_violation",
            "message": "Trial report fixture must remain memory-independent",
        })

    if fixture.get("ephemeral_only") is not True:
        issues.append({
            "code": "ephemeral_boundary_violation",
            "message": "Trial report fixture must remain ephemeral-only",
        })

    privacy = fixture.get("privacy_boundary", {})
    if privacy.get("public_safe") is not True:
        issues.append({
            "code": "public_safe_violation",
            "message": "Trial report fixture must remain public-safe",
        })

    languages = set(fixture.get("supported_languages", []))
    if languages != EXPECTED_LANGUAGES:
        issues.append({
            "code": "language_set_drift",
            "expected": sorted(EXPECTED_LANGUAGES),
            "actual": sorted(languages),
        })

    report_modes = set(fixture.get("report_modes", []))
    if report_modes != EXPECTED_REPORT_MODES:
        issues.append({
            "code": "report_mode_drift",
            "expected": sorted(EXPECTED_REPORT_MODES),
            "actual": sorted(report_modes),
        })

    variables = set(fixture.get("template_variables", []))
    if variables != EXPECTED_TEMPLATE_VARIABLES:
        issues.append({
            "code": "template_variable_drift",
            "expected": sorted(EXPECTED_TEMPLATE_VARIABLES),
            "actual": sorted(variables),
        })

    constraints = fixture.get("constraints", {})

    required_true = [
        "optional_ux_only",
        "not_runtime_requirement",
        "not_authorization",
        "not_memory_source",
        "bounded",
        "personal_local",
    ]

    for key in required_true:
        if constraints.get(key) is not True:
            issues.append({
                "code": "constraint_violation",
                "constraint": key,
            })

    payload = {
        "smoke_version": "m60.4-trial-report-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "summoned-brave-trial-report-validation",
        "write": False,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "language_count": len(languages),
        "report_mode_count": len(report_modes),
        "template_variable_count": len(variables),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
