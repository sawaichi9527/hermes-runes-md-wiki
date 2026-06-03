#!/usr/bin/env python3

import argparse
import json

from build_proposal_manifest import build_manifest
from proposal_apply_execute import request_apply
from proposal_apply_preview import build_previews
from proposal_governance_history import build_history
from proposal_governance_timeline import build_timeline
from proposal_review_queue import build_queue
from proposal_state_projection import build_projection

OUTPUT_CHOICES = ("table", "json")
REVIEWABLE_STATUSES = {"pending_human_review"}
APPROVED_STATE = "approved_pending_apply"
BLOCKED_EXECUTION_STATUS = "BLOCKED"
LATEST_EVENT = "apply_execution_requested"
FORBIDDEN_TRUE_KEYS = {
    "trusted_wiki_write",
    "automatic_approval",
    "automatic_promotion",
    "apply_execution",
    "database_mutation",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "proposal_file_modified",
}


def build_integrity():
    manifest = build_manifest()
    queue = build_queue()
    projection = build_projection()
    previews = build_previews()
    history = build_history()

    issues = []

    _check_read_only_payload(issues, "manifest", manifest)
    _check_read_only_payload(issues, "review_queue", queue)
    _check_read_only_payload(issues, "state_projection", projection)
    _check_read_only_payload(issues, "apply_preview", previews)
    _check_read_only_payload(issues, "governance_history", history)

    manifest_by_id = _index_by_id(manifest["entries"])
    queue_by_id = _index_by_id(queue["entries"])
    state_by_id = _index_by_id(projection["states"])
    preview_by_id = _index_by_id(previews["previews"])
    history_by_id = _index_by_id(history["histories"])

    _check_unique_ids(issues, "manifest", manifest["entries"])
    _check_unique_ids(issues, "review_queue", queue["entries"])
    _check_unique_ids(issues, "state_projection", projection["states"])
    _check_unique_ids(issues, "apply_preview", previews["previews"])
    _check_unique_ids(issues, "governance_history", history["histories"])

    if manifest["entry_count"] != len(manifest["entries"]):
        _add_issue(
            issues,
            "manifest_entry_count_mismatch",
            "manifest",
            None,
            "Manifest entry_count does not match entries length.",
        )

    if queue["entry_count"] != len(queue["entries"]):
        _add_issue(
            issues,
            "queue_entry_count_mismatch",
            "review_queue",
            None,
            "Review queue entry_count does not match entries length.",
        )

    if projection["entry_count"] != len(projection["states"]):
        _add_issue(
            issues,
            "projection_entry_count_mismatch",
            "state_projection",
            None,
            "State projection entry_count does not match states length.",
        )

    if previews["entry_count"] != len(previews["previews"]):
        _add_issue(
            issues,
            "preview_entry_count_mismatch",
            "apply_preview",
            None,
            "Apply preview entry_count does not match previews length.",
        )

    if history["proposal_count"] != len(history["histories"]):
        _add_issue(
            issues,
            "history_proposal_count_mismatch",
            "governance_history",
            None,
            "Governance history proposal_count does not match histories length.",
        )

    for proposal_id, entry in manifest_by_id.items():
        queue_entry = queue_by_id.get(proposal_id)
        state = state_by_id.get(proposal_id)
        preview = preview_by_id.get(proposal_id)
        history_entry = history_by_id.get(proposal_id)
        timeline = build_timeline(proposal_id)
        execution = request_apply(proposal_id)

        _check_read_only_payload(issues, "governance_timeline", timeline, proposal_id)
        _check_read_only_payload(issues, "apply_execution_boundary", execution, proposal_id)

        if state is None:
            _add_issue(
                issues,
                "missing_state_projection",
                "state_projection",
                proposal_id,
                "Manifest proposal is missing from state projection.",
            )
            continue

        if state["validation_status"] != entry["validation_status"]:
            _add_issue(
                issues,
                "validation_status_mismatch",
                "state_projection",
                proposal_id,
                "State projection validation_status differs from manifest.",
            )

        if state["sample_status"] != entry["sample_status"]:
            _add_issue(
                issues,
                "sample_status_mismatch",
                "state_projection",
                proposal_id,
                "State projection sample_status differs from manifest.",
            )

        should_be_queued = (
            entry["validation_status"] == "PASS"
            and entry["sample_status"] in REVIEWABLE_STATUSES
        )
        if should_be_queued and queue_entry is None:
            _add_issue(
                issues,
                "missing_review_queue_entry",
                "review_queue",
                proposal_id,
                "Reviewable proposal is missing from review queue.",
            )
        if not should_be_queued and queue_entry is not None:
            _add_issue(
                issues,
                "unexpected_review_queue_entry",
                "review_queue",
                proposal_id,
                "Non-reviewable proposal appeared in review queue.",
            )

        if history_entry is None:
            _add_issue(
                issues,
                "missing_governance_history",
                "governance_history",
                proposal_id,
                "Proposal is missing from governance history.",
            )
        else:
            if history_entry["event_count"] != timeline["event_count"]:
                _add_issue(
                    issues,
                    "history_timeline_event_count_mismatch",
                    "governance_history",
                    proposal_id,
                    "Governance history event_count differs from timeline.",
                )
            if history_entry["latest_event"] != _latest_event(timeline):
                _add_issue(
                    issues,
                    "history_timeline_latest_event_mismatch",
                    "governance_history",
                    proposal_id,
                    "Governance history latest_event differs from timeline.",
                )

        if timeline["event_count"] != len(timeline["events"]):
            _add_issue(
                issues,
                "timeline_event_count_mismatch",
                "governance_timeline",
                proposal_id,
                "Timeline event_count does not match events length.",
            )

        if _latest_event(timeline) != LATEST_EVENT:
            _add_issue(
                issues,
                "unexpected_timeline_latest_event",
                "governance_timeline",
                proposal_id,
                "Timeline latest event must remain apply_execution_requested.",
            )

        if execution["status"] != BLOCKED_EXECUTION_STATUS:
            _add_issue(
                issues,
                "execution_boundary_not_blocked",
                "apply_execution_boundary",
                proposal_id,
                "P0 apply execution boundary must remain BLOCKED.",
            )

        if execution.get("write") is not False:
            _add_issue(
                issues,
                "execution_boundary_write_not_false",
                "apply_execution_boundary",
                proposal_id,
                "P0 apply execution boundary must remain read-only/write=false.",
            )

        if state["effective_state"] == APPROVED_STATE:
            if preview is None:
                _add_issue(
                    issues,
                    "approved_missing_apply_preview",
                    "apply_preview",
                    proposal_id,
                    "Approved proposal is missing an apply preview.",
                )
            if not execution.get("preview_available"):
                _add_issue(
                    issues,
                    "approved_execution_missing_preview_reference",
                    "apply_execution_boundary",
                    proposal_id,
                    "Approved proposal execution boundary should reference the available preview.",
                )
            if not _timeline_has_event(timeline, "human_attunement_decision"):
                _add_issue(
                    issues,
                    "approved_missing_attunement_event",
                    "governance_timeline",
                    proposal_id,
                    "Approved proposal timeline is missing human attunement decision event.",
                )
            if not _timeline_has_event(timeline, "apply_preview_generated"):
                _add_issue(
                    issues,
                    "approved_missing_apply_preview_event",
                    "governance_timeline",
                    proposal_id,
                    "Approved proposal timeline is missing apply preview generation event.",
                )
        else:
            if preview is not None:
                _add_issue(
                    issues,
                    "non_approved_has_apply_preview",
                    "apply_preview",
                    proposal_id,
                    "Only approved_pending_apply proposals may have apply previews.",
                )

    for proposal_id in queue_by_id:
        if proposal_id not in manifest_by_id:
            _add_issue(
                issues,
                "queue_orphan_proposal",
                "review_queue",
                proposal_id,
                "Review queue contains proposal_id not present in manifest.",
            )

    for proposal_id in preview_by_id:
        if proposal_id not in manifest_by_id:
            _add_issue(
                issues,
                "preview_orphan_proposal",
                "apply_preview",
                proposal_id,
                "Apply preview contains proposal_id not present in manifest.",
            )

    for proposal_id in history_by_id:
        if proposal_id not in manifest_by_id:
            _add_issue(
                issues,
                "history_orphan_proposal",
                "governance_history",
                proposal_id,
                "Governance history contains proposal_id not present in manifest.",
            )

    return {
        "integrity_version": "m49-governance-integrity-v1",
        "status": "PASS" if not issues else "FAIL",
        "proposal_count": manifest["entry_count"],
        "issue_count": len(issues),
        "write": False,
        "checked_layers": [
            "manifest",
            "review_queue",
            "state_projection",
            "apply_preview",
            "apply_execution_boundary",
            "governance_timeline",
            "governance_history",
        ],
        "issues": issues,
    }


def _index_by_id(items):
    return {
        item["proposal_id"]: item
        for item in items
        if item.get("proposal_id") is not None
    }


def _check_unique_ids(issues, layer, items):
    seen = set()
    for item in items:
        proposal_id = item.get("proposal_id")
        if proposal_id is None:
            _add_issue(
                issues,
                "missing_proposal_id",
                layer,
                None,
                f"{layer} entry is missing proposal_id.",
            )
            continue
        if proposal_id in seen:
            _add_issue(
                issues,
                "duplicate_proposal_id",
                layer,
                proposal_id,
                f"{layer} contains duplicate proposal_id.",
            )
        seen.add(proposal_id)


def _check_read_only_payload(issues, layer, payload, proposal_id=None):
    for path, key, value in _walk_payload(payload):
        if key == "write" and value is not False:
            _add_issue(
                issues,
                "write_flag_not_false",
                layer,
                proposal_id,
                f"Read-only write flag must be false at {path}.",
            )
        if key in FORBIDDEN_TRUE_KEYS and value is True:
            _add_issue(
                issues,
                "forbidden_effect_enabled",
                layer,
                proposal_id,
                f"Forbidden P0 effect/capability is true at {path}.",
            )


def _walk_payload(value, prefix="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            yield path, key, child
            yield from _walk_payload(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_payload(child, f"{prefix}[{index}]")


def _timeline_has_event(timeline, event_name):
    return any(event.get("event") == event_name for event in timeline["events"])


def _latest_event(timeline):
    if not timeline["events"]:
        return None
    return timeline["events"][-1]["event"]


def _add_issue(issues, code, layer, proposal_id, message):
    issues.append(
        {
            "severity": "error",
            "code": code,
            "layer": layer,
            "proposal_id": proposal_id,
            "message": message,
        }
    )


def render_table(payload):
    lines = [
        f"status: {payload['status']}",
        f"proposal_count: {payload['proposal_count']}",
        f"issue_count: {payload['issue_count']}",
        "checked_layers:",
    ]
    lines.extend(f"  - {layer}" for layer in payload["checked_layers"])

    if payload["issues"]:
        lines.append("issues:")
        for issue in payload["issues"]:
            proposal_id = issue["proposal_id"] or "-"
            lines.append(
                f"  - [{issue['severity']}] {issue['code']} "
                f"layer={issue['layer']} proposal_id={proposal_id}: "
                f"{issue['message']}"
            )
    else:
        lines.append("issues: []")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Cross-layer governance consistency validator."
    )
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()
    payload = build_integrity()

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
