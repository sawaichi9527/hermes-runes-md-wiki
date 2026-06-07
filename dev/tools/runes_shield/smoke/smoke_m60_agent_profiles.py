#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = ROOT / "tools" / "runes_shield" / "agent_profiles"

REQUIRED_TOP_LEVEL_KEYS = {
    "profile_version",
    "profile_id",
    "agent_name",
    "agent_kind",
    "interface_type",
    "description",
    "interface_features",
    "governance_notes",
    "recommended_checks",
}

EXPECTED_PROFILES = {
    "generic-cli-agent.json",
    "generic-openai-agent.json",
    "generic-mcp-agent.json",
}

EXPECTED_RECOMMENDED_CHECKS = {
    "m57_baseline",
    "m58_workflow",
    "m58_docs",
    "m58_integration",
    "m59_onboarding_lock",
}


def main():
    issues = []
    profiles = []

    if not PROFILE_DIR.exists():
        issues.append({
            "code": "missing_profile_dir",
            "message": "agent_profiles directory missing",
        })
    else:
        discovered = {path.name for path in PROFILE_DIR.glob("*.json")}

        if discovered != EXPECTED_PROFILES:
            issues.append({
                "code": "profile_set_drift",
                "expected": sorted(EXPECTED_PROFILES),
                "actual": sorted(discovered),
            })

        for path in sorted(PROFILE_DIR.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            profiles.append(payload.get("profile_id"))

            missing = REQUIRED_TOP_LEVEL_KEYS - set(payload.keys())
            if missing:
                issues.append({
                    "code": "missing_top_level_keys",
                    "profile": path.name,
                    "missing": sorted(missing),
                })

            governance = payload.get("governance_notes", {})

            if governance.get("profile_grants_permissions") is not False:
                issues.append({
                    "code": "profile_permission_violation",
                    "profile": path.name,
                    "message": "Profiles must not grant permissions.",
                })

            if governance.get("write_access") is not False:
                issues.append({
                    "code": "write_access_violation",
                    "profile": path.name,
                })

            if governance.get("automatic_apply") is not False:
                issues.append({
                    "code": "automatic_apply_violation",
                    "profile": path.name,
                })

            if governance.get("automatic_promotion") is not False:
                issues.append({
                    "code": "automatic_promotion_violation",
                    "profile": path.name,
                })

            checks = set(payload.get("recommended_checks", []))
            if checks != EXPECTED_RECOMMENDED_CHECKS:
                issues.append({
                    "code": "recommended_check_drift",
                    "profile": path.name,
                    "expected": sorted(EXPECTED_RECOMMENDED_CHECKS),
                    "actual": sorted(checks),
                })

    payload = {
        "smoke_version": "m60.1-agent-profile-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "agent-runtime-profile-validation",
        "write": False,
        "profile_dir": str(PROFILE_DIR.relative_to(ROOT)),
        "profile_count": len(profiles),
        "profiles": profiles,
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
