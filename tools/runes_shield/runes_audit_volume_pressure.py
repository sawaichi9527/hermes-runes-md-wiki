#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMP_ROOT = ROOT / "tmp" / "m56-3-audit-pressure"
PERSIST = ROOT / "tools" / "runes_shield" / "runes_shield_audit_persistence.py"
RECALL = ROOT / "tools" / "runes_shield" / "runes_shield_audit_recall.py"
VERITY = ROOT / "tools" / "runes_shield" / "runes_verity.py"
PRESSURE_VERSION = "m56.3-audit-volume-pressure-v1"
OUTPUT_CHOICES = ("table", "json")

FORBIDDEN_TRUE_EFFECTS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "session_reexecuted",
    "adapter_reinvoked",
}


def run_process(args, timeout):
    return subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )


def generate_audit_events(audit_root, sessions, timeout):
    generated = []
    for index in range(sessions):
        request = {
            "agent": "hermes-agent",
            "conversation_id": f"conv-m56-3-pressure-{index + 1:03d}",
            "request": {
                "intent": "check_integrity" if index % 2 == 0 else "discover_tools",
            },
        }
        completed = run_process(
            [
                PERSIST,
                "--raw-json",
                json.dumps(request),
                "--audit-root",
                str(audit_root.relative_to(ROOT)),
                "--write",
                "--format",
                "json",
            ],
            timeout=timeout,
        )
        payload = json.loads(completed.stdout)
        generated.append(
            {
                "index": index + 1,
                "status": payload.get("status"),
                "session_id": payload.get("session_id"),
                "event_count": payload.get("event_count"),
                "write": payload.get("write"),
                "output_path": payload.get("output_path"),
            }
        )
    return generated


def run_recall_summary(audit_root, timeout):
    completed = run_process(
        [
            RECALL,
            "summary",
            "--audit-root",
            str(audit_root.relative_to(ROOT)),
            "--format",
            "json",
        ],
        timeout=timeout,
    )
    return json.loads(completed.stdout)


def run_verity(audit_root, max_events, max_recent_days, timeout):
    completed = run_process(
        [
            VERITY,
            "--audit-root",
            str(audit_root.relative_to(ROOT)),
            "--max-events",
            str(max_events),
            "--max-recent-days",
            str(max_recent_days),
            "--timeout",
            str(timeout),
            "--format",
            "json",
        ],
        timeout=timeout + 10,
    )
    return json.loads(completed.stdout)


def build_pressure(sessions=12, max_events=10, max_recent_days=3, timeout=15, keep_tmp=False):
    issues = []

    if sessions <= 0 or sessions > 20:
        issues.append(_issue("invalid_sessions", "sessions must be bounded in range 1..20"))
        sessions = min(max(sessions, 1), 20)

    if max_events <= 0 or max_events > 100:
        issues.append(_issue("invalid_max_events", "max_events must be bounded in range 1..100"))
        max_events = min(max(max_events, 1), 100)

    if TEMP_ROOT.exists():
        shutil.rmtree(TEMP_ROOT)

    generated = generate_audit_events(TEMP_ROOT, sessions=sessions, timeout=timeout)
    summary = run_recall_summary(TEMP_ROOT, timeout=timeout)
    verity = run_verity(TEMP_ROOT, max_events=max_events, max_recent_days=max_recent_days, timeout=timeout)

    expected_events = sessions * 2

    if summary.get("event_count") != expected_events:
        issues.append(
            _issue(
                "event_count_mismatch",
                f"expected {expected_events} audit events, got {summary.get('event_count')}",
            )
        )

    if summary.get("session_count") != sessions:
        issues.append(
            _issue(
                "session_count_mismatch",
                f"expected {sessions} sessions, got {summary.get('session_count')}",
            )
        )

    if verity.get("status") != "PASS":
        issues.append(_issue("verity_failed", "Runes Mouth of Verity failed under bounded audit pressure."))

    bounded_sample = _find_check(verity, "recall_replay_oath").get("evidence", {}).get("bounded_sample", {})
    events_checked = bounded_sample.get("events_checked")

    if events_checked is not None and events_checked > max_events:
        issues.append(
            _issue(
                "bounded_scan_violation",
                f"bounded sample checked {events_checked} events, max allowed {max_events}",
            )
        )

    load_safety = verity.get("load_safety", {})
    if load_safety.get("max_events_checked") != max_events:
        issues.append(_issue("max_events_drift", "verity max_events_checked drifted under pressure."))
    if load_safety.get("unbounded_audit_scan") is not False:
        issues.append(_issue("unbounded_scan_enabled", "unbounded_audit_scan must remain false."))
    if load_safety.get("background_worker") is not False:
        issues.append(_issue("background_worker_enabled", "background_worker must remain false."))

    effect_violations = []
    collect_forbidden_effects(summary, "summary", effect_violations)
    collect_forbidden_effects(verity, "verity", effect_violations)
    if effect_violations:
        issues.append(_issue("forbidden_effects", "forbidden effects appeared under audit volume pressure."))

    result = {
        "pressure_version": PRESSURE_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "audit-volume-pressure-test",
        "scale": "personal-local",
        "write": False,
        "audit_root": str(TEMP_ROOT.relative_to(ROOT)),
        "sessions_generated": sessions,
        "expected_event_count": expected_events,
        "max_events": max_events,
        "max_recent_days": max_recent_days,
        "generated": generated,
        "summary": {
            "status": summary.get("status"),
            "event_count": summary.get("event_count"),
            "session_count": summary.get("session_count"),
            "request_count": summary.get("request_count"),
            "trace_count": summary.get("trace_count"),
            "write": summary.get("write"),
            "effects": summary.get("effects"),
        },
        "verity": {
            "status": verity.get("status"),
            "write": verity.get("write"),
            "summary": verity.get("summary"),
            "load_safety": load_safety,
            "bounded_sample": bounded_sample,
        },
        "side_effect_boundary": {
            "status": "PASS" if not effect_violations else "FAIL",
            "violation_count": len(effect_violations),
            "violations": effect_violations[:10],
        },
        "load_safety": {
            "bounded_execution": True,
            "single_shot": True,
            "background_worker": False,
            "recursive_invocation": False,
            "unbounded_audit_scan": False,
            "automatic_remediation": False,
            "max_events_checked": max_events,
            "max_recent_days": max_recent_days,
            "timeout_sec_per_check": timeout,
        },
        "issue_count": len(issues),
        "issues": issues,
    }

    if not keep_tmp and TEMP_ROOT.exists():
        shutil.rmtree(TEMP_ROOT)

    return result


def _find_check(verity, name):
    for check in verity.get("checks", []):
        if check.get("check") == name:
            return check
    return {}


def collect_forbidden_effects(value, path, violations):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    violations.append({"path": f"{path}.effects.{key}", "effect": key})
        for key, child in value.items():
            collect_forbidden_effects(child, f"{path}.{key}", violations)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_forbidden_effects(child, f"{path}[{index}]", violations)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"pressure_version: {payload['pressure_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"sessions_generated: {payload['sessions_generated']}",
        f"expected_event_count: {payload['expected_event_count']}",
        f"summary_event_count: {payload['summary']['event_count']}",
        f"verity_status: {payload['verity']['status']}",
        f"bounded_events_checked: {payload['verity']['bounded_sample'].get('events_checked')}",
        f"max_events: {payload['max_events']}",
        f"side_effect_boundary: {payload['side_effect_boundary']['status']}",
        f"issue_count: {payload['issue_count']}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Bounded audit volume pressure test for Runes Mouth of Verity."
    )
    parser.add_argument("--sessions", type=int, default=12)
    parser.add_argument("--max-events", type=int, default=10)
    parser.add_argument("--max-recent-days", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--keep-tmp", action="store_true")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_pressure(
        sessions=args.sessions,
        max_events=args.max_events,
        max_recent_days=args.max_recent_days,
        timeout=args.timeout,
        keep_tmp=args.keep_tmp,
    )

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
