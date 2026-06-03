#!/usr/bin/env python3

import argparse
import json

from build_proposal_manifest import build_manifest
from proposal_apply_execute import request_apply
from proposal_apply_preview import build_previews
from proposal_governance_history import build_history
from proposal_governance_integrity import build_integrity
from proposal_governance_timeline import build_timeline
from proposal_review_queue import build_queue
from proposal_state_projection import build_projection

OUTPUT_CHOICES = ("table", "json")
EXPECTED_INTEGRITY_STATUS = "PASS"
BLOCKED_EXECUTION_STATUS = "BLOCKED"
TRIAL_PROFILES = {
    "baseline": "Read-only controlled trial-run over current proposal governance state.",
    "p0": "P0 controlled trial-run preserving blocked apply execution and read-only governance.",
}


def build_trial_run(profile="p0"):
    if profile not in TRIAL_PROFILES:
        raise SystemExit(f"unknown trial profile: {profile}")

    manifest = build_manifest()
    queue = build_queue()
    projection = build_projection()
    previews = build_previews()
    history = build_history()
    integrity = build_integrity()

    states = projection["states"]
    preview_ids = {preview["proposal_id"] for preview in previews["previews"]}
    history_by_id = {
        item["proposal_id"]: item
        for item in history["histories"]
    }

    observations = []
    execution_statuses = []

    for state in states:
        proposal_id = state["proposal_id"]
        timeline = build_timeline(proposal_id)
        execution = request_apply(proposal_id)
        history_entry = history_by_id.get(proposal_id)
        execution_statuses.append(execution["status"])

        observations.append(
            {
                "proposal_id": proposal_id,
                "validation_status": state["validation_status"],
                "sample_status": state["sample_status"],
                "effective_state": state["effective_state"],
                "decision_count": state["decision_count"],
                "has_apply_preview": proposal_id in preview_ids,
                "execution_status": execution["status"],
                "timeline_event_count": timeline["event_count"],
                "history_event_count": (
                    history_entry["event_count"] if history_entry else None
                ),
                "latest_event": (
                    history_entry["latest_event"] if history_entry else None
                ),
                "write": False,
            }
        )

    effective_state_counts = _count_by(observations, "effective_state")
    execution_status_counts = _count_values(execution_statuses)

    issues = []
    if integrity["status"] != EXPECTED_INTEGRITY_STATUS:
        issues.append(
            {
                "severity": "error",
                "code": "integrity_not_pass",
                "message": "M50 trial-run requires M49 integrity status PASS.",
            }
        )

    if integrity["issue_count"] != 0:
        issues.append(
            {
                "severity": "error",
                "code": "integrity_has_issues",
                "message": "M50 trial-run requires zero M49 integrity issues.",
            }
        )

    if any(status != BLOCKED_EXECUTION_STATUS for status in execution_statuses):
        issues.append(
            {
                "severity": "error",
                "code": "apply_execution_unblocked",
                "message": "P0 controlled trial-run requires all apply execution requests to remain BLOCKED.",
            }
        )

    if _payload_has_write_enabled(integrity):
        issues.append(
            {
                "severity": "error",
                "code": "integrity_write_enabled",
                "message": "M49 integrity payload must remain write=false throughout M50.",
            }
        )

    return {
        "trial_run_version": "m50-controlled-trial-run-v1",
        "profile": profile,
        "profile_description": TRIAL_PROFILES[profile],
        "status": "PASS" if not issues else "FAIL",
        "proposal_count": manifest["entry_count"],
        "queue_count": queue["entry_count"],
        "preview_count": previews["entry_count"],
        "history_count": history["proposal_count"],
        "integrity_status": integrity["status"],
        "integrity_issue_count": integrity["issue_count"],
        "effective_state_counts": effective_state_counts,
        "execution_status_counts": execution_status_counts,
        "write": False,
        "effects": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "index_update": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "database_mutation": False,
        },
        "observations": observations,
        "issues": issues,
    }


def _count_by(items, key):
    return _count_values(item[key] for item in items)


def _count_values(values):
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _payload_has_write_enabled(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "write" and child is not False:
                return True
            if _payload_has_write_enabled(child):
                return True
    elif isinstance(value, list):
        return any(_payload_has_write_enabled(child) for child in value)
    return False


def render_table(payload):
    lines = [
        f"trial_run_version: {payload['trial_run_version']}",
        f"profile: {payload['profile']}",
        f"status: {payload['status']}",
        f"proposal_count: {payload['proposal_count']}",
        f"queue_count: {payload['queue_count']}",
        f"preview_count: {payload['preview_count']}",
        f"history_count: {payload['history_count']}",
        f"integrity_status: {payload['integrity_status']}",
        f"integrity_issue_count: {payload['integrity_issue_count']}",
        f"write: {payload['write']}",
        "effective_state_counts:",
    ]

    for state, count in payload["effective_state_counts"].items():
        lines.append(f"  {state}: {count}")

    lines.append("execution_status_counts:")
    for status, count in payload["execution_status_counts"].items():
        lines.append(f"  {status}: {count}")

    if payload["issues"]:
        lines.append("issues:")
        for issue in payload["issues"]:
            lines.append(f"  - [{issue['severity']}] {issue['code']}: {issue['message']}")
    else:
        lines.append("issues: []")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Controlled read-only governance trial-run summary."
    )
    parser.add_argument("--profile", choices=tuple(TRIAL_PROFILES), default="p0")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()
    payload = build_trial_run(profile=args.profile)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
