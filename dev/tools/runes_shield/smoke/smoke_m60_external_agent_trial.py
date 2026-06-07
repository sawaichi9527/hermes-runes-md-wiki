#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"

COMMANDS = {
    "m59_onboarding_lock": [TOOLS / "runes_agent_onboarding_lock.py", "--format", "json"],
    "m60_1_agent_profiles": [TOOLS / "smoke_m60_agent_profiles.py"],
    "m60_2_transcript_fixture": [TOOLS / "smoke_m60_transcript_fixture.py"],
    "m60_3_capability_boundary": [TOOLS / "smoke_m60_capability_boundary.py"],
    "m60_4_trial_report": [TOOLS / "smoke_m60_trial_report.py"],
}

EXPECTED_LOCKED_SURFACES = {
    "verity_checks": 10,
    "invocation_tools": 8,
    "adapter_safe_intents": 9,
    "adapter_blocked_intents": 7,
}


def run_json(command, timeout=120):
    completed = subprocess.run(
        [sys.executable, *[str(part) for part in command]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return json.loads(completed.stdout)


def main():
    issues = []
    results = {}

    for name, command in COMMANDS.items():
        try:
            payload = run_json(command)
        except Exception as exc:
            issues.append({
                "code": "component_exception",
                "component": name,
                "message": str(exc),
            })
            results[name] = {"status": "FAIL", "write": None, "issue_count": None}
            continue

        results[name] = payload

        if payload.get("status") != "PASS":
            issues.append({
                "code": "component_failed",
                "component": name,
                "message": f"{name} did not report PASS",
            })

        if payload.get("write") is not False:
            issues.append({
                "code": "component_write_not_false",
                "component": name,
                "message": f"{name} write must remain false",
            })

        if payload.get("issue_count") not in (0, None):
            issues.append({
                "code": "component_issue_count_nonzero",
                "component": name,
                "message": f"{name} reported non-zero issues",
            })

    onboarding = results.get("m59_onboarding_lock", {})
    profiles = results.get("m60_1_agent_profiles", {})
    transcript = results.get("m60_2_transcript_fixture", {})
    boundary = results.get("m60_3_capability_boundary", {})
    report = results.get("m60_4_trial_report", {})

    readiness = onboarding.get("readiness", {})
    if readiness.get("ready_for_governed_access") is not True:
        issues.append({
            "code": "onboarding_readiness_violation",
            "message": "M59 must report ready_for_governed_access true",
        })

    if onboarding.get("agent_scope") != "agent-agnostic":
        issues.append({
            "code": "agent_scope_drift",
            "message": "M59 onboarding lock must remain agent-agnostic",
        })

    locked_sets = onboarding.get("locked_surface_counts", {})
    for label, locked in locked_sets.items():
        if locked != EXPECTED_LOCKED_SURFACES:
            issues.append({
                "code": "locked_surface_drift",
                "surface": label,
                "message": f"Locked surface drifted for {label}",
            })

    if profiles.get("profile_count") != 3:
        issues.append({
            "code": "profile_count_drift",
            "message": "M60.1 must keep exactly 3 initial generic profiles",
        })

    if transcript.get("onboarding_step_count") != 4:
        issues.append({
            "code": "transcript_step_count_drift",
            "message": "M60.2 transcript fixture must keep 4 onboarding steps",
        })

    if boundary.get("probe_count") != 7:
        issues.append({
            "code": "boundary_probe_count_drift",
            "message": "M60.3 boundary trial must keep 7 probes",
        })

    if boundary.get("expected_outcome") != "BLOCKED_OR_NOT_GRANTED":
        issues.append({
            "code": "boundary_expected_outcome_drift",
            "message": "M60.3 expected outcome must remain BLOCKED_OR_NOT_GRANTED",
        })

    if report.get("language_count") != 2 or report.get("report_mode_count") != 2:
        issues.append({
            "code": "trial_report_shape_drift",
            "message": "M60.4 trial report must keep 2 languages and 2 report modes",
        })

    payload = {
        "smoke_version": "m60.5-external-agent-trial-lock-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "first-external-agent-trial-lock",
        "scale": "personal-local",
        "write": False,
        "agent_scope": onboarding.get("agent_scope"),
        "trial_target": "First External Agent Integration Trial",
        "components": {
            name: {
                "status": result.get("status"),
                "write": result.get("write"),
                "issue_count": result.get("issue_count"),
            }
            for name, result in results.items()
        },
        "readiness": {
            "ready_for_governed_access": readiness.get("ready_for_governed_access"),
            "runtime_workflow": readiness.get("runtime_workflow"),
            "baseline": readiness.get("baseline"),
            "docs": readiness.get("docs"),
            "integration": readiness.get("integration"),
        },
        "m60_summary": {
            "profile_count": profiles.get("profile_count"),
            "transcript_kind": transcript.get("transcript_kind"),
            "onboarding_step_count": transcript.get("onboarding_step_count"),
            "boundary_probe_count": boundary.get("probe_count"),
            "boundary_expected_outcome": boundary.get("expected_outcome"),
            "trial_report_languages": report.get("language_count"),
            "trial_report_modes": report.get("report_mode_count"),
        },
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
