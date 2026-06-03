#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "runes_shield"
ADAPTER = TOOLS / "hermes_agent_adapter.py"
BASELINE = TOOLS / "runes_shield_baseline.py"
VERITY = TOOLS / "runes_verity.py"
WORKFLOW_VERSION = "m58-agent-governed-workflow-v1"
OUTPUT_CHOICES = ("table", "json")

DEFAULT_PROPOSAL_ID = "proposal-m37.2-fixture-001"
DEFAULT_AGENT = "hermes-agent"
DEFAULT_CONVERSATION_ID = "conv-m58-governed-workflow"

WORKFLOW_STEPS = [
    {
        "step": "discover_tools",
        "intent": "discover_tools",
        "description": "Discover the governed Runes Shield invocation surface.",
    },
    {
        "step": "check_integrity",
        "intent": "check_integrity",
        "description": "Check cross-layer governance integrity.",
    },
    {
        "step": "list_review_queue",
        "intent": "list_review_queue",
        "description": "Inspect proposals waiting for human review.",
    },
    {
        "step": "list_state_projection",
        "intent": "list_state_projection",
        "description": "Inspect derived proposal lifecycle states.",
    },
    {
        "step": "show_timeline",
        "intent": "show_timeline",
        "requires_proposal_id": True,
        "description": "Inspect the governance timeline for one proposal.",
    },
    {
        "step": "show_history",
        "intent": "show_history",
        "description": "Inspect proposal governance history.",
    },
    {
        "step": "run_controlled_trial",
        "intent": "run_controlled_trial",
        "description": "Run P0 controlled governance trial summary.",
    },
    {
        "step": "export_observations",
        "intent": "export_observations",
        "description": "Export read-only governance observations.",
    },
]

BLOCKED_PROBES = [
    "write_wiki",
    "apply_wiki",
    "mutate_database",
    "promote_memory",
    "spawn_background_worker",
]

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
    "audit_log_written",
}


def run_json(args, timeout, input_text=None):
    completed = subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return json.loads(completed.stdout)


def adapter_call(request, timeout):
    return run_json(
        [ADAPTER, "--raw-json", json.dumps(request), "--format", "json"],
        timeout=timeout,
    )


def build_agent_request(intent, agent, conversation_id, proposal_id=None, profile="p0"):
    request = {
        "agent": agent,
        "conversation_id": conversation_id,
        "intent": intent,
        "profile": profile,
    }
    if proposal_id:
        request["proposal_id"] = proposal_id
    return request


def run_workflow(agent=DEFAULT_AGENT, conversation_id=DEFAULT_CONVERSATION_ID, proposal_id=DEFAULT_PROPOSAL_ID, profile="p0", timeout=15):
    issues = []
    steps = []

    for spec in WORKFLOW_STEPS:
        request = build_agent_request(
            spec["intent"],
            agent=agent,
            conversation_id=conversation_id,
            proposal_id=proposal_id if spec.get("requires_proposal_id") else None,
            profile=profile,
        )
        payload = adapter_call(request, timeout=timeout)
        violations = []
        collect_forbidden_effects(payload, spec["step"], violations)

        ok = payload.get("status") == "PASS" and payload.get("write") is False and not violations
        if not ok:
            issues.append(_issue("workflow_step_failed", f"Step {spec['step']} failed governed workflow expectations."))

        steps.append({
            "step": spec["step"],
            "intent": spec["intent"],
            "description": spec["description"],
            "status": "PASS" if ok else "FAIL",
            "adapter_status": payload.get("status"),
            "tool": payload.get("tool"),
            "write": payload.get("write"),
            "reason_code": payload.get("reason_code"),
            "forbidden_effect_violation_count": len(violations),
            "summary": summarize_payload(payload),
        })

    blocked = []
    for intent in BLOCKED_PROBES:
        request = build_agent_request(
            intent,
            agent=agent,
            conversation_id=conversation_id,
            profile=profile,
        )
        payload = adapter_call(request, timeout=timeout)
        violations = []
        collect_forbidden_effects(payload, f"blocked_probe.{intent}", violations)
        ok = (
            payload.get("status") == "BLOCKED"
            and payload.get("reason_code") == "intent_blocked"
            and payload.get("write") is False
            and not violations
        )
        if not ok:
            issues.append(_issue("blocked_probe_failed", f"Blocked probe {intent} did not remain blocked."))
        blocked.append({
            "intent": intent,
            "status": "PASS" if ok else "FAIL",
            "adapter_status": payload.get("status"),
            "reason_code": payload.get("reason_code"),
            "write": payload.get("write"),
            "forbidden_effect_violation_count": len(violations),
        })

    verity = run_json([VERITY, "--format", "json", "--max-events", "25", "--max-recent-days", "3"], timeout=timeout + 10)
    baseline = run_json([BASELINE, "--format", "json"], timeout=timeout + 20)

    if verity.get("status") != "PASS" or verity.get("write") is not False:
        issues.append(_issue("verity_failed", "Runes Mouth of Verity did not pass after agent workflow."))
    if baseline.get("status") != "PASS" or baseline.get("write") is not False:
        issues.append(_issue("baseline_failed", "M57 baseline did not pass after agent workflow."))

    collect_forbidden_effects(verity, "verity", issues)
    collect_forbidden_effects(baseline, "baseline", issues)

    load_safety = verity.get("load_safety", {})
    for key in ("background_worker", "recursive_invocation", "unbounded_audit_scan", "automatic_remediation"):
        if load_safety.get(key) is not False:
            issues.append(_issue("load_safety_drift", f"{key} must remain false."))
    if load_safety.get("bounded_execution") is not True:
        issues.append(_issue("load_safety_drift", "bounded_execution must remain true."))
    if load_safety.get("single_shot") is not True:
        issues.append(_issue("load_safety_drift", "single_shot must remain true."))

    return {
        "workflow_version": WORKFLOW_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "agent-facing-governed-workflow",
        "scale": "personal-local",
        "agent": agent,
        "conversation_id": conversation_id,
        "proposal_id": proposal_id,
        "profile": profile,
        "write": False,
        "workflow_policy": {
            "trusted_wiki_write": False,
            "markdown_mutation": False,
            "database_mutation": False,
            "automatic_apply": False,
            "automatic_promotion": False,
            "background_worker": False,
            "recursive_invocation": False,
            "unbounded_audit_scan": False,
            "automatic_remediation": False,
        },
        "steps": steps,
        "blocked_probes": blocked,
        "post_workflow_verification": {
            "verity_status": verity.get("status"),
            "verity_version": verity.get("verity_version"),
            "verity_write": verity.get("write"),
            "baseline_status": baseline.get("status"),
            "baseline_version": baseline.get("baseline_version"),
            "baseline_write": baseline.get("write"),
            "locked_surface_counts": baseline.get("locked_surface_counts"),
            "load_safety": {
                "bounded_execution": load_safety.get("bounded_execution"),
                "single_shot": load_safety.get("single_shot"),
                "background_worker": load_safety.get("background_worker"),
                "recursive_invocation": load_safety.get("recursive_invocation"),
                "unbounded_audit_scan": load_safety.get("unbounded_audit_scan"),
                "automatic_remediation": load_safety.get("automatic_remediation"),
                "max_events_checked": load_safety.get("max_events_checked"),
                "max_recent_days": load_safety.get("max_recent_days"),
            },
        },
        "side_effect_boundary": {
            "status": "PASS" if not any(issue["code"] == "forbidden_effect_true" for issue in issues) else "FAIL",
            "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
        },
        "issue_count": len(issues),
        "issues": issues,
    }


def summarize_payload(payload):
    inner = payload.get("payload") if isinstance(payload, dict) else None
    summary = {}
    if isinstance(inner, dict):
        for key in ("status", "tool_count", "proposal_count", "queue_count", "history_count", "issue_count", "write"):
            if key in inner:
                summary[key] = inner[key]
        nested = inner.get("payload")
        if isinstance(nested, dict):
            for key in ("status", "proposal_count", "queue_count", "history_count", "issue_count", "write"):
                if key in nested:
                    summary[f"nested_{key}"] = nested[key]
    return summary


def collect_forbidden_effects(value, path, issues):
    violations = []
    _collect(value, path, violations)
    for violation in violations:
        issues.append(_issue("forbidden_effect_true", f"{violation['path']} became true."))
    return violations


def _collect(value, path, violations):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    violations.append({"path": f"{path}.effects.{key}", "effect": key})
        for key, child in value.items():
            if key == "payload":
                # Nested payloads are still checked by explicit component verifiers; keep this workflow summary light.
                continue
            _collect(child, f"{path}.{key}", violations)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _collect(child, f"{path}[{index}]", violations)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"workflow_version: {payload['workflow_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"agent: {payload['agent']}",
        f"conversation_id: {payload['conversation_id']}",
        f"proposal_id: {payload['proposal_id']}",
        f"write: {payload['write']}",
        f"issue_count: {payload['issue_count']}",
        "steps:",
    ]
    for step in payload["steps"]:
        lines.append(
            f"  - {step['step']}: status={step['status']} intent={step['intent']} tool={step['tool'] or '-'} write={step['write']}"
        )
    lines.append("blocked_probes:")
    for probe in payload["blocked_probes"]:
        lines.append(
            f"  - {probe['intent']}: status={probe['status']} adapter_status={probe['adapter_status']} reason={probe['reason_code']} write={probe['write']}"
        )
    verification = payload["post_workflow_verification"]
    lines.extend([
        "post_workflow_verification:",
        f"  verity_status: {verification['verity_status']}",
        f"  baseline_status: {verification['baseline_status']}",
        f"  locked_surface_counts: {verification['locked_surface_counts']}",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="M58 agent-facing governed workflow for Hermes-agent and Runes Shield."
    )
    parser.add_argument("--agent", default=DEFAULT_AGENT)
    parser.add_argument("--conversation-id", default=DEFAULT_CONVERSATION_ID)
    parser.add_argument("--proposal-id", default=DEFAULT_PROPOSAL_ID)
    parser.add_argument("--profile", default="p0")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = run_workflow(
        agent=args.agent,
        conversation_id=args.conversation_id,
        proposal_id=args.proposal_id,
        profile=args.profile,
        timeout=args.timeout,
    )

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
