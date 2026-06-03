#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from runes_shield_session import build_session_envelope

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AUDIT_ROOT = ROOT / "logs" / "runes_shield" / "audit"
PERSISTENCE_VERSION = "m54-runtime-audit-persistence-v1"
OUTPUT_CHOICES = ("table", "json", "jsonl")

PERSISTENCE_SCHEMA = {
    "audit_root": "optional path; defaults to logs/runes_shield/audit",
    "write": "explicit boolean; false by default",
    "session_request": "required object passed to M53 runtime session layer",
}


def load_request(path=None, raw=None):
    if raw is not None:
        return json.loads(raw)
    if path is None or path == "-":
        return json.loads(sys.stdin.read())
    return json.loads(Path(path).read_text(encoding="utf-8"))


def persist_audit(session_request, write=False, audit_root=None):
    if audit_root is None:
        audit_root = DEFAULT_AUDIT_ROOT
    else:
        audit_root = Path(audit_root)
        if not audit_root.is_absolute():
            audit_root = ROOT / audit_root

    session = build_session_envelope(session_request)
    events = build_audit_events(session)
    output_path = derive_audit_path(audit_root)

    if write:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("a", encoding="utf-8") as fh:
            for event in events:
                fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    return {
        "persistence_version": PERSISTENCE_VERSION,
        "status": session["status"],
        "mode": "write" if write else "dry-run",
        "write": bool(write),
        "audit_root": str(audit_root.relative_to(ROOT)) if _is_relative_to(audit_root, ROOT) else str(audit_root),
        "output_path": str(output_path.relative_to(ROOT)) if _is_relative_to(output_path, ROOT) else str(output_path),
        "event_count": len(events),
        "session_id": session["session_id"],
        "request_id": session["request_id"],
        "trace_id": session["trace_id"],
        "agent": session["agent"],
        "conversation_id": session["conversation_id"],
        "session_status": session["status"],
        "persistence_schema": PERSISTENCE_SCHEMA,
        "effects": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "index_update": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "database_mutation": False,
            "observation_ingested_to_rag": False,
            "audit_log_written": bool(write),
            "session_persisted": bool(write),
        },
        "events": events,
    }


def build_audit_events(session):
    persisted_at = datetime.now(timezone.utc).isoformat()
    events = []

    for item in session["audit_chain"]:
        events.append(
            {
                "event_version": "m54-runtime-audit-persistence-event-v1",
                "event_type": "runtime_audit_persistence",
                "persisted_at_utc": persisted_at,
                "session_version": session["session_version"],
                "session_id": session["session_id"],
                "request_id": session["request_id"],
                "trace_id": session["trace_id"],
                "agent": session["agent"],
                "conversation_id": session["conversation_id"],
                "session_status": session["status"],
                "layer": item["layer"],
                "layer_status": item["status"],
                "layer_write": item["write"],
                "intent": item.get("intent"),
                "tool": item.get("tool"),
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

    return events


def derive_audit_path(audit_root):
    now = datetime.now(timezone.utc)
    return audit_root / now.strftime("%Y-%m") / f"{now.strftime('%Y%m%d')}.jsonl"


def _is_relative_to(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def render_jsonl(payload):
    return "\n".join(
        json.dumps(event, ensure_ascii=False, sort_keys=True)
        for event in payload["events"]
    )


def render_table(payload):
    lines = [
        f"persistence_version: {payload['persistence_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"write: {payload['write']}",
        f"audit_root: {payload['audit_root']}",
        f"output_path: {payload['output_path']}",
        f"event_count: {payload['event_count']}",
        f"session_id: {payload['session_id']}",
        f"request_id: {payload['request_id']}",
        f"trace_id: {payload['trace_id']}",
        f"session_status: {payload['session_status']}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Persist runtime invocation audit events as local append-only JSONL."
    )
    parser.add_argument("--request", help="Path to session request JSON. Use '-' or omit for stdin.")
    parser.add_argument("--raw-json", help="Inline session request JSON string.")
    parser.add_argument("--audit-root", help="Audit root directory. Defaults to logs/runes_shield/audit.")
    parser.add_argument("--write", action="store_true", help="Actually append JSONL audit events. Default is dry-run.")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    session_request = load_request(path=args.request, raw=args.raw_json)
    payload = persist_audit(
        session_request,
        write=args.write,
        audit_root=args.audit_root,
    )

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if args.format == "jsonl":
        print(render_jsonl(payload))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
