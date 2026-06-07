#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m60" / "real-onboarding-transcript-fixture.json"

REQUIRED_TOP_LEVEL_KEYS = {
    "fixture_version",
    "fixture_id",
    "status",
    "purpose",
    "privacy_boundary",
    "agent_profile",
    "transcript_kind",
    "onboarding_path",
    "expected_lock_summary",
    "expected_locked_surfaces",
    "forbidden_claims",
    "notes",
}

EXPECTED_LOCKED_SURFACES = {
    "verity_checks": 10,
    "invocation_tools": 8,
    "adapter_safe_intents": 9,
    "adapter_blocked_intents": 7,
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M60 onboarding transcript fixture missing",
        })
        payload = {
            "smoke_version": "m60.2-transcript-fixture-smoke-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    missing = REQUIRED_TOP_LEVEL_KEYS - set(fixture.keys())
    if missing:
        issues.append({
            "code": "missing_top_level_keys",
            "missing": sorted(missing),
        })

    privacy = fixture.get("privacy_boundary", {})

    expected_false = [
        "contains_secrets",
        "contains_private_user_data",
        "contains_full_chat_history",
        "contains_raw_prompt_dump",
        "contains_runtime_credentials",
    ]

    for key in expected_false:
        if privacy.get(key) is not False:
            issues.append({
                "code": "privacy_boundary_violation",
                "field": key,
                "message": f"{key} must remain false",
            })

    if privacy.get("public_safe") is not True:
        issues.append({
            "code": "public_safe_violation",
            "message": "Fixture must remain public-safe",
        })

    lock_summary = fixture.get("expected_lock_summary", {})

    if lock_summary.get("status") != "PASS":
        issues.append({
            "code": "lock_status_drift",
            "message": "Expected lock summary must remain PASS",
        })

    if lock_summary.get("write") is not False:
        issues.append({
            "code": "lock_write_violation",
            "message": "Expected lock summary write must remain false",
        })

    if lock_summary.get("ready_for_governed_access") is not True:
        issues.append({
            "code": "governed_access_violation",
            "message": "ready_for_governed_access must remain true",
        })

    locked = fixture.get("expected_locked_surfaces", {})
    if locked != EXPECTED_LOCKED_SURFACES:
        issues.append({
            "code": "locked_surface_drift",
            "expected": EXPECTED_LOCKED_SURFACES,
            "actual": locked,
        })

    onboarding_path = fixture.get("onboarding_path", [])
    if len(onboarding_path) != 4:
        issues.append({
            "code": "onboarding_path_length_drift",
            "message": "Fixture onboarding path must remain 4 steps",
        })

    payload = {
        "smoke_version": "m60.2-transcript-fixture-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "real-onboarding-transcript-fixture-validation",
        "write": False,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "transcript_kind": fixture.get("transcript_kind"),
        "onboarding_step_count": len(onboarding_path),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
