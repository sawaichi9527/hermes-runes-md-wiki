#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone

from proposal_controlled_trial_run import build_trial_run

OUTPUT_CHOICES = ("table", "json", "jsonl")
EXPORT_PROFILES = {
    "p0": "P0 read-only governance observation export from controlled trial-run.",
}


def build_observation_export(profile="p0"):
    if profile not in EXPORT_PROFILES:
        raise SystemExit(f"unknown observation export profile: {profile}")

    trial_run = build_trial_run(profile=profile)
    exported_at = datetime.now(timezone.utc).isoformat()
    events = []

    for observation in trial_run["observations"]:
        events.append(
            {
                "event_version": "m50.1-governance-observation-event-v1",
                "event_type": "governance_trial_observation",
                "exported_at_utc": exported_at,
                "trial_run_version": trial_run["trial_run_version"],
                "trial_profile": trial_run["profile"],
                "proposal_id": observation["proposal_id"],
                "validation_status": observation["validation_status"],
                "sample_status": observation["sample_status"],
                "effective_state": observation["effective_state"],
                "decision_count": observation["decision_count"],
                "has_apply_preview": observation["has_apply_preview"],
                "execution_status": observation["execution_status"],
                "timeline_event_count": observation["timeline_event_count"],
                "history_event_count": observation["history_event_count"],
                "latest_event": observation["latest_event"],
                "integrity_status": trial_run["integrity_status"],
                "integrity_issue_count": trial_run["integrity_issue_count"],
                "write": False,
                "effects": {
                    "trusted_wiki_write": False,
                    "markdown_mutation": False,
                    "index_update": False,
                    "automatic_apply": False,
                    "automatic_promotion": False,
                    "database_mutation": False,
                    "observation_ingested_to_rag": False,
                },
            }
        )

    return {
        "observation_export_version": "m50.1-governance-observation-export-v1",
        "profile": profile,
        "profile_description": EXPORT_PROFILES[profile],
        "status": "PASS" if trial_run["status"] == "PASS" else "FAIL",
        "exported_at_utc": exported_at,
        "trial_run_status": trial_run["status"],
        "trial_run_version": trial_run["trial_run_version"],
        "proposal_count": trial_run["proposal_count"],
        "event_count": len(events),
        "integrity_status": trial_run["integrity_status"],
        "integrity_issue_count": trial_run["integrity_issue_count"],
        "write": False,
        "effects": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "index_update": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "database_mutation": False,
            "observation_ingested_to_rag": False,
        },
        "events": events,
        "issues": trial_run["issues"],
    }


def render_table(payload):
    lines = [
        f"observation_export_version: {payload['observation_export_version']}",
        f"profile: {payload['profile']}",
        f"status: {payload['status']}",
        f"trial_run_status: {payload['trial_run_status']}",
        f"proposal_count: {payload['proposal_count']}",
        f"event_count: {payload['event_count']}",
        f"integrity_status: {payload['integrity_status']}",
        f"integrity_issue_count: {payload['integrity_issue_count']}",
        f"write: {payload['write']}",
        "events:",
    ]

    for event in payload["events"]:
        lines.append(
            "  - "
            f"proposal_id={event['proposal_id']} "
            f"state={event['effective_state']} "
            f"execution={event['execution_status']} "
            f"latest={event['latest_event']}"
        )

    if payload["issues"]:
        lines.append("issues:")
        for issue in payload["issues"]:
            lines.append(f"  - [{issue['severity']}] {issue['code']}: {issue['message']}")
    else:
        lines.append("issues: []")

    return "\n".join(lines)


def render_jsonl(payload):
    return "\n".join(
        json.dumps(event, ensure_ascii=False, sort_keys=True)
        for event in payload["events"]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Export read-only governance observations from controlled trial-run."
    )
    parser.add_argument("--profile", choices=tuple(EXPORT_PROFILES), default="p0")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()
    payload = build_observation_export(profile=args.profile)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if args.format == "jsonl":
        print(render_jsonl(payload))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
