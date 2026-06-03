#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AUDIT_ROOT = ROOT / "logs" / "runes_shield" / "audit"
RECALL_VERSION = "m55-governance-audit-recall-v1"
OUTPUT_CHOICES = ("table", "json", "jsonl")


def load_events(audit_root=None):
    root = _resolve_root(audit_root)
    events = []

    if not root.exists():
        return []

    for path in sorted(root.glob("**/*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            event["_source_path"] = str(path.relative_to(ROOT)) if _is_relative_to(path, ROOT) else str(path)
            event["_source_line"] = line_no
            events.append(event)

    return events


def build_recall(audit_root=None, session_id=None, request_id=None, trace_id=None, agent=None, status=None):
    root = _resolve_root(audit_root)
    events = load_events(root)
    filtered = []

    for event in events:
        if session_id and event.get("session_id") != session_id:
            continue
        if request_id and event.get("request_id") != request_id:
            continue
        if trace_id and event.get("trace_id") != trace_id:
            continue
        if agent and event.get("agent") != agent:
            continue
        if status and event.get("session_status") != status and event.get("layer_status") != status:
            continue
        filtered.append(event)

    return {
        "recall_version": RECALL_VERSION,
        "status": "PASS",
        "mode": "read-only",
        "write": False,
        "audit_root": str(root.relative_to(ROOT)) if _is_relative_to(root, ROOT) else str(root),
        "event_count": len(filtered),
        "session_count": len({event.get("session_id") for event in filtered}),
        "request_count": len({event.get("request_id") for event in filtered}),
        "trace_count": len({event.get("trace_id") for event in filtered}),
        "filters": {
            "session_id": session_id,
            "request_id": request_id,
            "trace_id": trace_id,
            "agent": agent,
            "status": status,
        },
        "effects": _effects(),
        "events": filtered,
    }


def build_replay(audit_root=None, session_id=None):
    if not session_id:
        raise SystemExit("replay requires --session-id")

    recall = build_recall(audit_root=audit_root, session_id=session_id)
    events = sorted(
        recall["events"],
        key=lambda event: (
            event.get("persisted_at_utc") or "",
            event.get("_source_path") or "",
            event.get("_source_line") or 0,
        ),
    )

    chain = []
    for event in events:
        chain.append(
            {
                "layer": event.get("layer"),
                "layer_status": event.get("layer_status"),
                "intent": event.get("intent"),
                "tool": event.get("tool"),
                "source_path": event.get("_source_path"),
                "source_line": event.get("_source_line"),
                "write": False,
            }
        )

    return {
        "replay_version": "m55-governance-audit-replay-v1",
        "status": "PASS" if chain else "EMPTY",
        "mode": "read-only-reconstruction",
        "write": False,
        "session_id": session_id,
        "event_count": len(events),
        "chain_count": len(chain),
        "session_statuses": sorted({event.get("session_status") for event in events if event.get("session_status")}),
        "agents": sorted({event.get("agent") for event in events if event.get("agent")}),
        "conversation_ids": sorted({event.get("conversation_id") for event in events if event.get("conversation_id")}),
        "effects": _effects(),
        "chain": chain,
    }


def build_summary(audit_root=None):
    recall = build_recall(audit_root=audit_root)
    events = recall["events"]

    return {
        "summary_version": "m55-governance-audit-summary-v1",
        "status": "PASS",
        "mode": "read-only",
        "write": False,
        "audit_root": recall["audit_root"],
        "event_count": len(events),
        "session_count": recall["session_count"],
        "request_count": recall["request_count"],
        "trace_count": recall["trace_count"],
        "session_status_counts": _count_values(event.get("session_status") for event in events),
        "layer_status_counts": _count_values(event.get("layer_status") for event in events),
        "layer_counts": _count_values(event.get("layer") for event in events),
        "intent_counts": _count_values(event.get("intent") for event in events if event.get("intent")),
        "tool_counts": _count_values(event.get("tool") for event in events if event.get("tool")),
        "effects": _effects(),
    }


def _count_values(values):
    counts = {}
    for value in values:
        if value is None:
            continue
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _effects():
    return {
        "trusted_wiki_write": False,
        "markdown_mutation": False,
        "index_update": False,
        "automatic_apply": False,
        "automatic_promotion": False,
        "database_mutation": False,
        "observation_ingested_to_rag": False,
        "audit_log_written": False,
        "session_reexecuted": False,
        "adapter_reinvoked": False,
    }


def _resolve_root(audit_root):
    if audit_root is None:
        return DEFAULT_AUDIT_ROOT
    root = Path(audit_root)
    if root.is_absolute():
        return root
    return ROOT / root


def _is_relative_to(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def render_jsonl(payload):
    rows = payload.get("events") or payload.get("chain") or []
    return "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)


def render_table(payload):
    lines = [
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"write: {payload['write']}",
    ]

    for key in ("audit_root", "event_count", "session_count", "request_count", "trace_count", "chain_count"):
        if key in payload:
            lines.append(f"{key}: {payload[key]}")

    if "session_status_counts" in payload:
        lines.append("session_status_counts:")
        for key, value in payload["session_status_counts"].items():
            lines.append(f"  {key}: {value}")

    if "chain" in payload:
        lines.append("chain:")
        for item in payload["chain"]:
            lines.append(
                "  - "
                f"layer={item['layer']} status={item['layer_status']} "
                f"intent={item['intent'] or '-'} tool={item['tool'] or '-'}"
            )

    return "\n".join(lines)


def emit(payload, fmt):
    if fmt == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    if fmt == "jsonl":
        print(render_jsonl(payload))
        return
    print(render_table(payload))


def main():
    parser = argparse.ArgumentParser(
        description="Read-only recall and replay over persisted Runes Shield runtime audit JSONL."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--audit-root")
        p.add_argument("--format", choices=OUTPUT_CHOICES, default="table")

    recall_parser = subparsers.add_parser("recall", help="Recall runtime audit events.")
    add_common(recall_parser)
    recall_parser.add_argument("--session-id")
    recall_parser.add_argument("--request-id")
    recall_parser.add_argument("--trace-id")
    recall_parser.add_argument("--agent")
    recall_parser.add_argument("--status")

    replay_parser = subparsers.add_parser("replay", help="Reconstruct one session audit chain without re-executing it.")
    add_common(replay_parser)
    replay_parser.add_argument("--session-id", required=True)

    summary_parser = subparsers.add_parser("summary", help="Summarize runtime audit events.")
    add_common(summary_parser)

    args = parser.parse_args()

    if args.command == "recall":
        payload = build_recall(
            audit_root=args.audit_root,
            session_id=args.session_id,
            request_id=args.request_id,
            trace_id=args.trace_id,
            agent=args.agent,
            status=args.status,
        )
        emit(payload, args.format)
        return

    if args.command == "replay":
        payload = build_replay(audit_root=args.audit_root, session_id=args.session_id)
        emit(payload, args.format)
        return

    if args.command == "summary":
        payload = build_summary(audit_root=args.audit_root)
        emit(payload, args.format)
        return


if __name__ == "__main__":
    main()
