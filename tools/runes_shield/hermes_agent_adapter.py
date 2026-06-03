#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

from runes_shield_invocation import BLOCKED_CAPABILITIES, TOOL_REGISTRY, discover_tools, invoke_tool

ADAPTER_VERSION = "m52-hermes-agent-adapter-v1"
OUTPUT_CHOICES = ("table", "json")
DEFAULT_PROFILE = "p0"
REQUEST_SCHEMA = {
    "adapter_version": "optional string",
    "agent": "optional string",
    "intent": "required string",
    "tool": "optional string",
    "proposal_id": "optional string",
    "profile": "optional string",
}

INTENT_TOOL_MAP = {
    "discover_tools": None,
    "list_manifest": "manifest.list",
    "list_review_queue": "review_queue.list",
    "list_state_projection": "state_projection.list",
    "show_timeline": "governance.timeline",
    "show_history": "governance.history",
    "check_integrity": "governance.integrity",
    "run_controlled_trial": "trial_run.controlled",
    "export_observations": "observation.export",
}

BLOCKED_INTENTS = {
    "write_wiki",
    "apply_wiki",
    "mutate_database",
    "promote_memory",
    "write_decision",
    "auto_approve",
    "spawn_background_worker",
}


def load_request(path=None, raw=None):
    if raw is not None:
        return json.loads(raw)
    if path is None or path == "-":
        return json.loads(sys.stdin.read())
    return json.loads(Path(path).read_text(encoding="utf-8"))


def handle_request(request):
    validation = validate_request(request)
    if validation["status"] != "PASS":
        return _response(
            status="BLOCKED",
            reason_code=validation["reason_code"],
            reason=validation["reason"],
            request=request,
        )

    intent = request["intent"]
    profile = request.get("profile", DEFAULT_PROFILE)

    if intent in BLOCKED_INTENTS:
        return _response(
            status="BLOCKED",
            reason_code="intent_blocked",
            reason=f"Intent is blocked by {ADAPTER_VERSION}.",
            request=request,
        )

    if intent == "discover_tools":
        payload = discover_tools()
        return _response(
            status="PASS",
            request=request,
            tool=None,
            payload=payload,
        )

    tool_name = request.get("tool") or INTENT_TOOL_MAP.get(intent)
    if tool_name is None:
        return _response(
            status="BLOCKED",
            reason_code="intent_not_mapped",
            reason=f"Intent is not mapped to an allowlisted Runes Shield tool: {intent}",
            request=request,
        )

    if tool_name not in TOOL_REGISTRY:
        shield_result = invoke_tool(
            tool_name,
            proposal_id=request.get("proposal_id"),
            profile=profile,
        )
        return _response(
            status="BLOCKED",
            reason_code=shield_result.get("reason_code", "tool_not_allowlisted"),
            reason=shield_result.get("reason", "Tool is not allowlisted."),
            request=request,
            tool=tool_name,
            payload=shield_result,
        )

    shield_result = invoke_tool(
        tool_name,
        proposal_id=request.get("proposal_id"),
        profile=profile,
    )

    return _response(
        status=shield_result["status"],
        request=request,
        tool=tool_name,
        payload=shield_result,
    )


def validate_request(request):
    if not isinstance(request, dict):
        return _validation_block("invalid_request_type", "Request must be a JSON object.")

    intent = request.get("intent")
    if not intent:
        return _validation_block("missing_intent", "Request is missing required field: intent.")

    if not isinstance(intent, str):
        return _validation_block("invalid_intent_type", "Request intent must be a string.")

    if "tool" in request and not isinstance(request["tool"], str):
        return _validation_block("invalid_tool_type", "Request tool must be a string when provided.")

    if "proposal_id" in request and not isinstance(request["proposal_id"], str):
        return _validation_block("invalid_proposal_id_type", "Request proposal_id must be a string when provided.")

    if "profile" in request and not isinstance(request["profile"], str):
        return _validation_block("invalid_profile_type", "Request profile must be a string when provided.")

    if intent == "show_timeline" and not request.get("proposal_id"):
        return _validation_block("missing_proposal_id", "show_timeline requires proposal_id.")

    return {"status": "PASS"}


def _validation_block(reason_code, reason):
    return {
        "status": "BLOCKED",
        "reason_code": reason_code,
        "reason": reason,
    }


def _response(status, request, reason_code=None, reason=None, tool=None, payload=None):
    result = {
        "adapter_version": ADAPTER_VERSION,
        "status": status,
        "agent": request.get("agent", "unknown") if isinstance(request, dict) else "unknown",
        "intent": request.get("intent") if isinstance(request, dict) else None,
        "tool": tool,
        "write": False,
        "request_schema": REQUEST_SCHEMA,
        "blocked_capabilities": sorted(BLOCKED_CAPABILITIES),
        "effects": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "index_update": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "database_mutation": False,
            "observation_ingested_to_rag": False,
        },
        "payload": payload,
    }

    if reason_code:
        result["reason_code"] = reason_code
    if reason:
        result["reason"] = reason

    return result


def render_table(payload):
    lines = [
        f"adapter_version: {payload['adapter_version']}",
        f"status: {payload['status']}",
        f"agent: {payload['agent']}",
        f"intent: {payload['intent']}",
        f"tool: {payload['tool'] or '-'}",
        f"write: {payload['write']}",
    ]

    if payload["status"] == "BLOCKED":
        lines.append(f"reason_code: {payload.get('reason_code')}")
        lines.append(f"reason: {payload.get('reason')}")
    elif isinstance(payload.get("payload"), dict):
        inner = payload["payload"]
        if "status" in inner:
            lines.append(f"payload_status: {inner['status']}")
        if "tool_count" in inner:
            lines.append(f"payload_tool_count: {inner['tool_count']}")
        if "payload" in inner and isinstance(inner["payload"], dict):
            nested = inner["payload"]
            for key in ("status", "proposal_count", "issue_count", "event_count"):
                if key in nested:
                    lines.append(f"nested_{key}: {nested[key]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Hermes-agent adapter for Runes Shield governed invocation."
    )
    parser.add_argument("--request", help="Path to request JSON. Use '-' or omit for stdin.")
    parser.add_argument("--raw-json", help="Inline request JSON string.")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    request = load_request(path=args.request, raw=args.raw_json)
    payload = handle_request(request)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
