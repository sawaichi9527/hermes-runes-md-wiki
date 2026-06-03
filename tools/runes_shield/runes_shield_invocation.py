#!/usr/bin/env python3

import argparse
import json

from build_proposal_manifest import build_manifest
from proposal_controlled_trial_run import build_trial_run
from proposal_governance_history import build_history
from proposal_governance_integrity import build_integrity
from proposal_governance_observation_export import build_observation_export
from proposal_governance_timeline import build_timeline
from proposal_review_queue import build_queue
from proposal_state_projection import build_projection

OUTPUT_CHOICES = ("table", "json")
TOOL_VERSION = "m51-runes-shield-invocation-v1"
DEFAULT_PROFILE = "p0"

BLOCKED_CAPABILITIES = {
    "trusted_wiki_write",
    "direct_markdown_mutation",
    "direct_database_mutation",
    "automatic_apply",
    "automatic_promotion",
    "background_worker",
    "unmediated_decision_write",
}

TOOL_REGISTRY = {
    "manifest.list": {
        "description": "List proposal manifest entries.",
        "risk": "low",
        "write": False,
        "args": [],
    },
    "review_queue.list": {
        "description": "List proposals pending human review.",
        "risk": "low",
        "write": False,
        "args": [],
    },
    "state_projection.list": {
        "description": "List derived proposal lifecycle states.",
        "risk": "low",
        "write": False,
        "args": [],
    },
    "governance.timeline": {
        "description": "Show governance timeline for one proposal_id.",
        "risk": "low",
        "write": False,
        "args": ["proposal_id"],
    },
    "governance.history": {
        "description": "Show governance history across proposals.",
        "risk": "low",
        "write": False,
        "args": [],
    },
    "governance.integrity": {
        "description": "Run cross-layer governance integrity validation.",
        "risk": "low",
        "write": False,
        "args": [],
    },
    "trial_run.controlled": {
        "description": "Run P0 controlled governance trial-run summary.",
        "risk": "low",
        "write": False,
        "args": [],
    },
    "observation.export": {
        "description": "Export read-only governance observation events.",
        "risk": "low",
        "write": False,
        "args": [],
    },
}


def discover_tools():
    tools = []
    for name, spec in sorted(TOOL_REGISTRY.items()):
        tools.append(
            {
                "name": name,
                "description": spec["description"],
                "risk": spec["risk"],
                "write": spec["write"],
                "args": spec["args"],
            }
        )

    return {
        "shield_version": TOOL_VERSION,
        "interface": "Runes Shield",
        "subtitle": "A governed invocation boundary for trusted Markdown memory.",
        "tool_count": len(tools),
        "write": False,
        "blocked_capabilities": sorted(BLOCKED_CAPABILITIES),
        "tools": tools,
    }


def invoke_tool(tool_name, proposal_id=None, profile=DEFAULT_PROFILE):
    if tool_name not in TOOL_REGISTRY:
        return _blocked_result(
            tool_name,
            "tool_not_allowlisted",
            f"Tool is not allowlisted through {TOOL_VERSION}.",
        )

    spec = TOOL_REGISTRY[tool_name]
    if spec["write"] is not False:
        return _blocked_result(
            tool_name,
            "write_tool_blocked",
            "Runes Shield P0 invocation does not expose write tools.",
        )

    missing = [arg for arg in spec["args"] if arg == "proposal_id" and not proposal_id]
    if missing:
        return _blocked_result(
            tool_name,
            "missing_required_argument",
            f"Missing required argument(s): {', '.join(missing)}.",
        )

    payload = _dispatch(tool_name, proposal_id=proposal_id, profile=profile)
    status = payload.get("status", "PASS")

    return {
        "shield_version": TOOL_VERSION,
        "tool": tool_name,
        "status": status,
        "risk": spec["risk"],
        "write": False,
        "blocked_capabilities": sorted(BLOCKED_CAPABILITIES),
        "payload": payload,
    }


def _dispatch(tool_name, proposal_id=None, profile=DEFAULT_PROFILE):
    if tool_name == "manifest.list":
        return build_manifest()
    if tool_name == "review_queue.list":
        return build_queue()
    if tool_name == "state_projection.list":
        return build_projection()
    if tool_name == "governance.timeline":
        return build_timeline(proposal_id)
    if tool_name == "governance.history":
        return build_history()
    if tool_name == "governance.integrity":
        return build_integrity()
    if tool_name == "trial_run.controlled":
        return build_trial_run(profile=profile)
    if tool_name == "observation.export":
        return build_observation_export(profile=profile)
    raise AssertionError(f"unhandled allowlisted tool: {tool_name}")


def _blocked_result(tool_name, reason_code, reason):
    return {
        "shield_version": TOOL_VERSION,
        "tool": tool_name,
        "status": "BLOCKED",
        "reason_code": reason_code,
        "reason": reason,
        "risk": "blocked",
        "write": False,
        "blocked_capabilities": sorted(BLOCKED_CAPABILITIES),
        "payload": None,
    }


def render_table(payload):
    if "tools" in payload:
        lines = [
            f"shield_version: {payload['shield_version']}",
            f"interface: {payload['interface']}",
            f"tool_count: {payload['tool_count']}",
            f"write: {payload['write']}",
            "tools:",
        ]
        for tool in payload["tools"]:
            args = ",".join(tool["args"]) if tool["args"] else "-"
            lines.append(
                f"  - {tool['name']} risk={tool['risk']} write={tool['write']} args={args}"
            )
        return "\n".join(lines)

    lines = [
        f"shield_version: {payload['shield_version']}",
        f"tool: {payload['tool']}",
        f"status: {payload['status']}",
        f"risk: {payload['risk']}",
        f"write: {payload['write']}",
    ]

    if payload["status"] == "BLOCKED":
        lines.append(f"reason_code: {payload['reason_code']}")
        lines.append(f"reason: {payload['reason']}")
    else:
        inner = payload["payload"]
        if isinstance(inner, dict):
            for key in ("status", "entry_count", "proposal_count", "issue_count", "event_count"):
                if key in inner:
                    lines.append(f"payload_{key}: {inner[key]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Runes Shield governed invocation boundary for trusted Markdown memory."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", help="Discover allowlisted Runes Shield tools.")
    discover_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    invoke_parser = subparsers.add_parser("invoke", help="Invoke one allowlisted Runes Shield tool.")
    invoke_parser.add_argument("tool")
    invoke_parser.add_argument("--proposal-id")
    invoke_parser.add_argument("--profile", default=DEFAULT_PROFILE)
    invoke_parser.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    args = parser.parse_args()

    if args.command == "discover":
        payload = discover_tools()
        if args.format == "json":
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return
        print(render_table(payload))
        return

    if args.command == "invoke":
        payload = invoke_tool(
            args.tool,
            proposal_id=args.proposal_id,
            profile=args.profile,
        )
        if args.format == "json":
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return
        print(render_table(payload))
        return


if __name__ == "__main__":
    main()
