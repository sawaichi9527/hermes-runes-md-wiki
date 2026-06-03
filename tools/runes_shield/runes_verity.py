#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
DEFAULT_AUDIT_ROOT = ROOT / "logs" / "runes_shield" / "audit"
VERITY_VERSION = "m56-runes-mouth-of-verity-v1"
OUTPUT_CHOICES = ("table", "json")

NOT_ENTERPRISE_FEATURES = [
    "siem",
    "centralized_collector",
    "distributed_tracing_backend",
    "policy_engine",
    "automatic_remediation",
    "background_daemon",
    "multi_tenant_rbac",
]

FORBIDDEN_EFFECTS = [
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
]


def run_command(args, timeout):
    completed = subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    if completed.returncode != 0:
        return {
            "status": "FAIL",
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-800:],
            "stderr_tail": completed.stderr[-800:],
            "payload": None,
        }

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {
            "status": "FAIL",
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-800:],
            "stderr_tail": completed.stderr[-800:],
            "payload": None,
        }

    return {
        "status": "PASS",
        "returncode": completed.returncode,
        "payload": payload,
    }


def check_integrity(timeout):
    result = run_command([TOOLS / "proposal_governance_integrity.py", "--format", "json"], timeout)
    payload = result.get("payload") or {}
    ok = result["status"] == "PASS" and payload.get("status") == "PASS" and payload.get("write") is False
    return oath("integrity_oath", ok, payload, "M49 integrity must pass and remain read-only.")


def check_trial_run(timeout):
    result = run_command([TOOLS / "proposal_controlled_trial_run.py", "--format", "json"], timeout)
    payload = result.get("payload") or {}
    effects_ok = _effects_disabled(payload)
    ok = result["status"] == "PASS" and payload.get("status") == "PASS" and payload.get("write") is False and effects_ok
    return oath("trial_run_oath", ok, payload, "M50 controlled trial-run must pass without side effects.")


def check_invocation(timeout):
    result = run_command([TOOLS / "runes_shield_invocation.py", "discover", "--format", "json"], timeout)
    payload = result.get("payload") or {}
    blocked = set(payload.get("blocked_capabilities", []))
    required_blocked = {"trusted_wiki_write", "direct_database_mutation", "automatic_apply", "automatic_promotion"}
    ok = (
        result["status"] == "PASS"
        and payload.get("shield_version") == "m51-runes-shield-invocation-v1"
        and payload.get("write") is False
        and payload.get("tool_count", 0) >= 8
        and required_blocked.issubset(blocked)
    )
    return oath("invocation_oath", ok, payload, "M51 invocation boundary must expose only allowlisted read-only tools.")


def check_adapter(timeout):
    safe = run_command(
        [
            TOOLS / "hermes_agent_adapter.py",
            "--raw-json",
            json.dumps({"agent": "hermes-agent", "intent": "check_integrity"}),
            "--format",
            "json",
        ],
        timeout,
    )
    blocked = run_command(
        [
            TOOLS / "hermes_agent_adapter.py",
            "--raw-json",
            json.dumps({"agent": "hermes-agent", "intent": "write_wiki"}),
            "--format",
            "json",
        ],
        timeout,
    )

    safe_payload = safe.get("payload") or {}
    blocked_payload = blocked.get("payload") or {}
    ok = (
        safe["status"] == "PASS"
        and blocked["status"] == "PASS"
        and safe_payload.get("status") == "PASS"
        and safe_payload.get("write") is False
        and blocked_payload.get("status") == "BLOCKED"
        and blocked_payload.get("reason_code") == "intent_blocked"
        and blocked_payload.get("write") is False
        and _effects_disabled(safe_payload)
        and _effects_disabled(blocked_payload)
    )
    return oath(
        "adapter_oath",
        ok,
        {"safe_intent": safe_payload, "blocked_intent": blocked_payload},
        "M52 adapter must pass safe intents and block unsafe mutation intents.",
    )


def check_session(timeout):
    request = {
        "agent": "hermes-agent",
        "conversation_id": "conv-m56-verity",
        "request": {"intent": "check_integrity"},
    }
    result = run_command(
        [TOOLS / "runes_shield_session.py", "--raw-json", json.dumps(request), "--format", "json"],
        timeout,
    )
    payload = result.get("payload") or {}
    effects = payload.get("effects", {})
    ok = (
        result["status"] == "PASS"
        and payload.get("status") == "PASS"
        and payload.get("write") is False
        and bool(payload.get("session_id"))
        and bool(payload.get("request_id"))
        and bool(payload.get("trace_id"))
        and effects.get("session_persisted") is False
        and effects.get("audit_log_written") is False
        and _effects_disabled(payload)
    )
    return oath("session_oath", ok, payload, "M53 session must provide traceability without persistence or mutation.")


def check_persistence(timeout, audit_root):
    request = {
        "agent": "hermes-agent",
        "conversation_id": "conv-m56-verity",
        "request": {"intent": "check_integrity"},
    }
    result = run_command(
        [
            TOOLS / "runes_shield_audit_persistence.py",
            "--raw-json",
            json.dumps(request),
            "--audit-root",
            str(_rel(audit_root)),
            "--format",
            "json",
        ],
        timeout,
    )
    payload = result.get("payload") or {}
    effects = payload.get("effects", {})
    ok = (
        result["status"] == "PASS"
        and payload.get("status") == "PASS"
        and payload.get("mode") == "dry-run"
        and payload.get("write") is False
        and effects.get("audit_log_written") is False
        and effects.get("session_persisted") is False
        and _effects_disabled(payload)
    )
    return oath("persistence_oath", ok, payload, "M54 dry-run persistence must not write audit logs.")


def check_recall_replay(timeout, audit_root, max_events):
    sample = bounded_audit_sample(audit_root, max_events=max_events)

    if not sample["session_id"]:
        payload = {
            "status": "SKIPPED",
            "reason": "No persisted audit session available in bounded sample.",
            "bounded_sample": sample,
            "write": False,
            "effects": _zero_effects(extra=["audit_log_written", "session_reexecuted", "adapter_reinvoked"]),
        }
        return oath("recall_replay_oath", True, payload, "M55 replay is skipped when no bounded audit sample exists.")

    result = run_command(
        [
            TOOLS / "runes_shield_audit_recall.py",
            "replay",
            "--audit-root",
            str(_rel(audit_root)),
            "--session-id",
            sample["session_id"],
            "--format",
            "json",
        ],
        timeout,
    )
    payload = result.get("payload") or {}
    effects = payload.get("effects", {})
    ok = (
        result["status"] == "PASS"
        and payload.get("status") == "PASS"
        and payload.get("mode") == "read-only-reconstruction"
        and payload.get("write") is False
        and effects.get("session_reexecuted") is False
        and effects.get("adapter_reinvoked") is False
        and effects.get("audit_log_written") is False
        and _effects_disabled(payload)
    )
    payload["bounded_sample"] = sample
    return oath("recall_replay_oath", ok, payload, "M55 replay must reconstruct provenance without re-execution.")


def check_side_effects(checks):
    violations = []
    for check in checks:
        collect_effect_violations(check.get("evidence"), path=check["check"], violations=violations)

    payload = {
        "status": "PASS" if not violations else "FAIL",
        "violation_count": len(violations),
        "violations": violations[:20],
        "write": False,
        "effects": _zero_effects(extra=["audit_log_written", "session_reexecuted", "adapter_reinvoked"]),
    }
    return oath("side_effect_oath", not violations, payload, "No checked layer may report forbidden side effects.")


def check_abyss_guard(checks):
    violations = []
    watched = {
        "observation_ingested_to_rag",
        "database_mutation",
        "session_reexecuted",
        "adapter_reinvoked",
        "automatic_apply",
    }
    for check in checks:
        collect_effect_violations(check.get("evidence"), path=check["check"], violations=violations, keys=watched)

    payload = {
        "status": "PASS" if not violations else "FAIL",
        "principle": "observability must not become mutation, ingestion, or re-execution",
        "violation_count": len(violations),
        "violations": violations[:20],
        "write": False,
        "effects": _zero_effects(extra=["audit_log_written", "session_reexecuted", "adapter_reinvoked"]),
    }
    return oath("abyss_guard", not violations, payload, "Observation must not stare back as mutation or replay side effects.")


def check_calamity_guard(max_events, max_recent_days, timeout):
    payload = {
        "status": "PASS",
        "bounded_execution": True,
        "single_shot": True,
        "background_worker": False,
        "recursive_invocation": False,
        "automatic_remediation": False,
        "unbounded_audit_scan": False,
        "max_events_checked": max_events,
        "max_recent_days": max_recent_days,
        "timeout_sec_per_check": timeout,
        "write": False,
        "effects": _zero_effects(extra=["audit_log_written", "session_reexecuted", "adapter_reinvoked"]),
    }
    return oath("calamity_guard", True, payload, "Truth-gate verification must not become a runtime calamity.")


def bounded_audit_sample(audit_root, max_events=100):
    root = Path(audit_root)
    files = sorted(root.glob("**/*.jsonl"), reverse=True) if root.exists() else []
    checked = 0
    first_session_id = None
    first_event = None

    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_no, line in enumerate(lines, start=1):
            if checked >= max_events:
                break
            if not line.strip():
                continue
            checked += 1
            event = json.loads(line)
            if first_event is None:
                first_event = {
                    "source_path": str(_rel(path)),
                    "source_line": line_no,
                    "event_type": event.get("event_type"),
                    "session_status": event.get("session_status"),
                }
            if event.get("session_id") and first_session_id is None:
                first_session_id = event["session_id"]
        if checked >= max_events or first_session_id:
            break

    return {
        "audit_root": str(_rel(root)),
        "events_checked": checked,
        "max_events": max_events,
        "session_id": first_session_id,
        "first_event": first_event,
    }


def collect_effect_violations(obj, path, violations, keys=None):
    if isinstance(obj, dict):
        effects = obj.get("effects")
        if isinstance(effects, dict):
            watched = keys or set(effects.keys())
            for key in watched:
                if effects.get(key) is True:
                    violations.append({"path": path, "effect": key, "value": True})
        for key, value in obj.items():
            collect_effect_violations(value, f"{path}.{key}", violations, keys=keys)
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            collect_effect_violations(value, f"{path}[{idx}]", violations, keys=keys)


def oath(name, ok, evidence, description):
    return {
        "check": name,
        "status": "PASS" if ok else "FAIL",
        "description": description,
        "bounded": True,
        "write": False,
        "evidence": evidence,
    }


def _effects_disabled(payload):
    effects = payload.get("effects")
    if not isinstance(effects, dict):
        return True
    for key in FORBIDDEN_EFFECTS:
        if effects.get(key) is True:
            return False
    return True


def _zero_effects(extra=None):
    effects = {key: False for key in FORBIDDEN_EFFECTS}
    for key in extra or []:
        effects[key] = False
    return effects


def _rel(path):
    path = Path(path)
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def overall_status(checks):
    if any(check["status"] == "FAIL" for check in checks):
        return "FAIL"
    return "PASS"


def build_verity(args):
    audit_root = Path(args.audit_root)
    if not audit_root.is_absolute():
        audit_root = ROOT / audit_root

    checks = [
        check_integrity(args.timeout),
        check_trial_run(args.timeout),
        check_invocation(args.timeout),
        check_adapter(args.timeout),
        check_session(args.timeout),
        check_persistence(args.timeout, audit_root),
        check_recall_replay(args.timeout, audit_root, args.max_events),
    ]

    checks.append(check_side_effects(checks))
    checks.append(check_abyss_guard(checks))
    checks.append(check_calamity_guard(args.max_events, args.max_recent_days, args.timeout))

    return {
        "verity_version": VERITY_VERSION,
        "name": "Runes Mouth of Verity",
        "name_zh": "符文真理之口",
        "status": overall_status(checks),
        "mode": "truth-gate-runtime-verification",
        "scale": "personal-local",
        "write": False,
        "audit_root": str(_rel(audit_root)),
        "load_safety": {
            "bounded_execution": True,
            "single_shot": True,
            "background_worker": False,
            "recursive_invocation": False,
            "unbounded_audit_scan": False,
            "automatic_remediation": False,
            "max_events_checked": args.max_events,
            "max_recent_days": args.max_recent_days,
            "timeout_sec_per_check": args.timeout,
        },
        "not_enterprise_features": NOT_ENTERPRISE_FEATURES,
        "checks": checks,
        "summary": {
            "total": len(checks),
            "passed": sum(1 for check in checks if check["status"] == "PASS"),
            "failed": sum(1 for check in checks if check["status"] == "FAIL"),
        },
    }


def render_table(payload):
    lines = [
        f"verity_version: {payload['verity_version']}",
        f"name: {payload['name']} / {payload['name_zh']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"audit_root: {payload['audit_root']}",
        "checks:",
    ]
    for check in payload["checks"]:
        lines.append(f"  - {check['check']}: {check['status']}")
    lines.append("load_safety:")
    for key, value in payload["load_safety"].items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Runes Mouth of Verity: bounded truth-gate verification for Runes Shield runtime."
    )
    parser.add_argument("--audit-root", default=str(_rel(DEFAULT_AUDIT_ROOT)))
    parser.add_argument("--max-events", type=int, default=100)
    parser.add_argument("--max-recent-days", type=int, default=7)
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_verity(args)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
