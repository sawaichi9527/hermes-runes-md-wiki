#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from hermes_agent_adapter import handle_request

SESSION_VERSION = "m53-runtime-invocation-session-v1"
OUTPUT_CHOICES = ("table", "json", "jsonl")
DEFAULT_AGENT = "hermes-agent"

SESSION_SCHEMA = {
    "session_id": "optional string; generated when missing",
    "request_id": "optional string; generated when missing",
    "agent": "optional string; defaults to hermes-agent",
    "conversation_id": "optional string",
    "trace_id": "optional string; generated when missing",
    "request": "required object passed to M52 adapter",
}


def load_session_request(path=None, raw=None):
    if raw is not None:
        return json.loads(raw)
    if path is None or path == "-":
        return json.loads(sys.stdin.read())
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_session_envelope(session_request):
    validation = validate_session_request(session_request)
    now = datetime.now(timezone.utc).isoformat()

    if validation["status"] != "PASS":
        return _session_response(
            session_request=session_request,
            status="BLOCKED",
            reason_code=validation["reason_code"],
            reason=validation["reason"],
            started_at_utc=now,
            completed_at_utc=now,
            adapter_response=None,
        )

    request = dict(session_request["request"])
    request.setdefault("agent", session_request.get("agent", DEFAULT_AGENT))

    started_at = now
    adapter_response = handle_request(request)
    completed_at = datetime.now(timezone.utc).isoformat()

    return _session_response(
        session_request=session_request,
        status=adapter_response["status"],
        started_at_utc=started_at,
        completed_at_utc=completed_at,
        adapter_response=adapter_response,
    )


def validate_session_request(session_request):
    if not isinstance(session_request, dict):
        return _validation_block("invalid_session_request_type", "Session request must be a JSON object.")

    request = session_request.get("request")
    if request is None:
        return _validation_block("missing_request", "Session request is missing required object: request.")

    if not isinstance(request, dict):
        return _validation_block("invalid_request_type", "Session request.request must be a JSON object.")

    for field in ("session_id", "request_id", "agent", "conversation_id", "trace_id"):
        if field in session_request and not isinstance(session_request[field], str):
            return _validation_block(
                f"invalid_{field}_type",
                f"Session field {field} must be a string when provided.",
            )

    return {"status": "PASS"}


def _validation_block(reason_code, reason):
    return {
        "status": "BLOCKED",
        "reason_code": reason_code,
        "reason": reason,
    }


def _session_response(
    session_request,
    status,
    started_at_utc,
    completed_at_utc,
    adapter_response,
    reason_code=None,
    reason=None,
):
    session_id = _field_or_generated(session_request, "session_id", "session")
    request_id = _field_or_generated(session_request, "request_id", "request")
    trace_id = _field_or_generated(session_request, "trace_id", "trace")
    agent = session_request.get("agent", DEFAULT_AGENT) if isinstance(session_request, dict) else DEFAULT_AGENT

    result = {
        "session_version": SESSION_VERSION,
        "status": status,
        "session_id": session_id,
        "request_id": request_id,
        "trace_id": trace_id,
        "agent": agent,
        "conversation_id": session_request.get("conversation_id") if isinstance(session_request, dict) else None,
        "started_at_utc": started_at_utc,
        "completed_at_utc": completed_at_utc,
        "write": False,
        "session_schema": SESSION_SCHEMA,
        "effects": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "index_update": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "database_mutation": False,
            "observation_ingested_to_rag": False,
            "session_persisted": False,
            "audit_log_written": False,
        },
        "audit_chain": [
            {
                "layer": "m53-runtime-session",
                "status": status,
                "write": False,
            }
        ],
        "adapter_response": adapter_response,
    }

    if adapter_response is not None:
        result["audit_chain"].append(
            {
                "layer": adapter_response.get("adapter_version", "m52-adapter"),
                "status": adapter_response.get("status"),
                "intent": adapter_response.get("intent"),
                "tool": adapter_response.get("tool"),
                "write": adapter_response.get("write"),
            }
        )

    if reason_code:
        result["reason_code"] = reason_code
    if reason:
        result["reason"] = reason

    return result


def _field_or_generated(payload, field, prefix):
    if isinstance(payload, dict) and payload.get(field):
        return payload[field]
    return f"{prefix}-{uuid4()}"


def render_table(payload):
    lines = [
        f"session_version: {payload['session_version']}",
        f"status: {payload['status']}",
        f"session_id: {payload['session_id']}",
        f"request_id: {payload['request_id']}",
        f"trace_id: {payload['trace_id']}",
        f"agent: {payload['agent']}",
        f"conversation_id: {payload['conversation_id'] or '-'}",
        f"write: {payload['write']}",
        "audit_chain:",
    ]

    for item in payload["audit_chain"]:
        lines.append(
            f"  - layer={item['layer']} status={item['status']} write={item['write']}"
        )

    if payload.get("reason_code"):
        lines.append(f"reason_code: {payload['reason_code']}")
        lines.append(f"reason: {payload['reason']}")

    return "\n".join(lines)


def render_jsonl(payload):
    audit_events = []
    for item in payload["audit_chain"]:
        audit_events.append(
            {
                "event_version": "m53-runtime-invocation-audit-event-v1",
                "event_type": "runtime_invocation_audit",
                "session_id": payload["session_id"],
                "request_id": payload["request_id"],
                "trace_id": payload["trace_id"],
                "agent": payload["agent"],
                "conversation_id": payload["conversation_id"],
                "layer": item["layer"],
                "status": item["status"],
                "write": item["write"],
                "started_at_utc": payload["started_at_utc"],
                "completed_at_utc": payload["completed_at_utc"],
            }
        )
    return "\n".join(json.dumps(event, ensure_ascii=False, sort_keys=True) for event in audit_events)


def main():
    parser = argparse.ArgumentParser(
        description="Runtime invocation session envelope for Runes Shield agent calls."
    )
    parser.add_argument("--request", help="Path to session request JSON. Use '-' or omit for stdin.")
    parser.add_argument("--raw-json", help="Inline session request JSON string.")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    session_request = load_session_request(path=args.request, raw=args.raw_json)
    payload = build_session_envelope(session_request)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if args.format == "jsonl":
        print(render_jsonl(payload))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
