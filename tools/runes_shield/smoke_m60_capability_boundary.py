#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m60" / "capability-boundary-trial.json"
PROFILE_DIR = ROOT / "tools" / "runes_shield" / "agent_profiles"

EXPECTED_PROBES = {
    "profile_grants_write",
    "bypass_runes_shield",
    "direct_wiki_mutation",
    "direct_database_mutation",
    "automatic_apply",
    "automatic_promotion",
    "fake_pass",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "Capability boundary fixture missing",
        })
        payload = {
            "smoke_version": "m60.3-capability-boundary-smoke-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    privacy = fixture.get("privacy_boundary", {})
    if privacy.get("public_safe") is not True:
        issues.append({
            "code": "public_safe_violation",
            "message": "Boundary fixture must remain public-safe",
        })

    probes = fixture.get("boundary_probes", [])
    discovered = {probe.get("probe_id") for probe in probes}

    if discovered != EXPECTED_PROBES:
        issues.append({
            "code": "probe_set_drift",
            "expected": sorted(EXPECTED_PROBES),
            "actual": sorted(discovered),
        })

    for probe in probes:
        if probe.get("expected") != "false":
            issues.append({
                "code": "probe_expected_value_violation",
                "probe": probe.get("probe_id"),
            })

    profiles = list(PROFILE_DIR.glob("*.json"))

    for profile_path in profiles:
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
        governance = payload.get("governance_notes", {})

        if governance.get("profile_grants_permissions") is not False:
            issues.append({
                "code": "profile_permission_violation",
                "profile": profile_path.name,
            })

        if governance.get("write_access") is not False:
            issues.append({
                "code": "profile_write_access_violation",
                "profile": profile_path.name,
            })

        if governance.get("runes_shield_required") is not True:
            issues.append({
                "code": "shield_requirement_violation",
                "profile": profile_path.name,
            })

    payload = {
        "smoke_version": "m60.3-capability-boundary-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "agent-capability-boundary-validation",
        "write": False,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "profile_count": len(profiles),
        "probe_count": len(probes),
        "expected_outcome": fixture.get("expected_outcome"),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
