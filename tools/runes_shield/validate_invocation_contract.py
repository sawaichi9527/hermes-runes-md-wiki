#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVOCATION = ROOT / "tools" / "runes_shield" / "runes_shield_invocation.py"
ADAPTER = ROOT / "tools" / "runes_shield" / "hermes_agent_adapter.py"
CONTRACT_VERSION = "m56.5-invocation-contract-v1"
OUTPUT_CHOICES = ("table", "json")

EXPECTED_TOOLS = {
    "governance.history": {"args": [], "risk": "low", "write": False},
    "governance.integrity": {"args": [], "risk": "low", "write": False},
    "governance.timeline": {"args": ["proposal_id"], "risk": "low", "write": False},
    "manifest.list": {"args": [], "risk": "low", "write": False},
    "observation.export": {"args": [], "risk": "low", "write": False},
    "review_queue.list": {"args": [], "risk": "low", "write": False},
    "state_projection.list": {"args": [], "risk": "low", "write": False},
    "trial_run.controlled": {"args": [], "risk": "low", "write": False},
}

EXPECTED_INTENT_TOOL_MAP = {
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

EXPECTED_BLOCKED_INTENTS = {
    "write_wiki",
    "apply_wiki",
    "mutate_database",
    "promote_memory",
    "write_decision",
    "auto_approve",
    "spawn_background_worker",
}

EXPECTED_BLOCKED_CAPABILITIES = {
    "automatic_apply",
    "automatic_promotion",
    "background_worker",
    "direct_database_mutation",
    "direct_markdown_mutation",
    "trusted_wiki_write",
    "unmediated_decision_write",
}

FORBIDDEN_TRUE_EFFECTS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
}


def run_process(args, timeout, raw_request=None):
    cmd = [sys.executable, *[str(arg) for arg in args]]
    if raw_request is not None:
        cmd.extend(["--raw-json", json.dumps(raw_request)])
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return json.loads(completed.stdout)


def discover_invocation(timeout):
    return run_process([INVOCATION, "discover", "--format", "json"], timeout=timeout)


def invoke_tool(tool, timeout, proposal_id=None):
    args = [INVOCATION, "invoke", tool, "--format", "json"]
    if proposal_id:
        args.extend(["--proposal-id", proposal_id])
    return run_process(args, timeout=timeout)


def adapter_request(request, timeout):
    return run_process([ADAPTER, "--format", "json"], timeout=timeout, raw_request=request)


def validate(timeout=15):
    issues = []
    discovery = discover_invocation(timeout)
    tools = {tool["name"]: tool for tool in discovery.get("tools", [])}

    if discovery.get("shield_version") != "m51-runes-shield-invocation-v1":
        issues.append(_issue("shield_version_drift", "M51 shield version drifted."))
    if discovery.get("write") is not False:
        issues.append(_issue("discovery_write_not_false", "Discovery write must remain false."))
    if discovery.get("tool_count") != len(EXPECTED_TOOLS):
        issues.append(_issue("tool_count_drift", "Allowlisted tool count drifted."))
    if set(tools) != set(EXPECTED_TOOLS):
        issues.append(_issue("tool_set_drift", f"Expected tools {sorted(EXPECTED_TOOLS)}, got {sorted(tools)}"))

    blocked_caps = set(discovery.get("blocked_capabilities", []))
    if blocked_caps != EXPECTED_BLOCKED_CAPABILITIES:
        issues.append(_issue("blocked_capability_drift", "Blocked capability set drifted."))

    for name, expected in EXPECTED_TOOLS.items():
        tool = tools.get(name)
        if not tool:
            continue
        if tool.get("write") is not expected["write"]:
            issues.append(_issue("tool_write_drift", f"Tool {name} write drifted."))
        if tool.get("risk") != expected["risk"]:
            issues.append(_issue("tool_risk_drift", f"Tool {name} risk drifted."))
        if tool.get("args") != expected["args"]:
            issues.append(_issue("tool_args_drift", f"Tool {name} args drifted."))

    safe_invocations = []
    for tool_name in sorted(EXPECTED_TOOLS):
        proposal_id = "proposal-m37.2-fixture-001" if "proposal_id" in EXPECTED_TOOLS[tool_name]["args"] else None
        payload = invoke_tool(tool_name, timeout=timeout, proposal_id=proposal_id)
        safe_invocations.append(_summarize_invocation(tool_name, payload))
        if payload.get("status") != "PASS":
            issues.append(_issue("safe_tool_invocation_failed", f"Tool {tool_name} did not return PASS."))
        if payload.get("write") is not False:
            issues.append(_issue("safe_tool_write_not_false", f"Tool {tool_name} write was not false."))
        _collect_forbidden_effects(payload, f"tool.{tool_name}", issues)

    blocked_invocations = []
    for tool_name in ("wiki.apply", "database.write", "memory.promote"):
        payload = invoke_tool(tool_name, timeout=timeout)
        blocked_invocations.append(_summarize_invocation(tool_name, payload))
        if payload.get("status") != "BLOCKED":
            issues.append(_issue("blocked_tool_not_blocked", f"Tool {tool_name} was not BLOCKED."))
        if payload.get("reason_code") != "tool_not_allowlisted":
            issues.append(_issue("blocked_tool_reason_drift", f"Tool {tool_name} reason drifted."))
        if payload.get("write") is not False:
            issues.append(_issue("blocked_tool_write_not_false", f"Tool {tool_name} write was not false."))

    adapter_safe = []
    for intent, tool_name in EXPECTED_INTENT_TOOL_MAP.items():
        request = {"agent": "hermes-agent", "intent": intent}
        if intent == "show_timeline":
            request["proposal_id"] = "proposal-m37.2-fixture-001"
        payload = adapter_request(request, timeout=timeout)
        adapter_safe.append(_summarize_adapter(intent, payload))
        if payload.get("status") != "PASS":
            issues.append(_issue("adapter_safe_intent_failed", f"Intent {intent} did not return PASS."))
        if payload.get("tool") != tool_name:
            issues.append(_issue("adapter_tool_mapping_drift", f"Intent {intent} mapped to {payload.get('tool')}, expected {tool_name}."))
        if payload.get("write") is not False:
            issues.append(_issue("adapter_write_not_false", f"Intent {intent} write was not false."))
        _collect_forbidden_effects(payload, f"intent.{intent}", issues)

    adapter_blocked = []
    for intent in sorted(EXPECTED_BLOCKED_INTENTS):
        payload = adapter_request({"agent": "hermes-agent", "intent": intent}, timeout=timeout)
        adapter_blocked.append(_summarize_adapter(intent, payload))
        if payload.get("status") != "BLOCKED":
            issues.append(_issue("blocked_intent_not_blocked", f"Intent {intent} was not BLOCKED."))
        if payload.get("reason_code") != "intent_blocked":
            issues.append(_issue("blocked_intent_reason_drift", f"Intent {intent} reason drifted."))
        if payload.get("write") is not False:
            issues.append(_issue("blocked_intent_write_not_false", f"Intent {intent} write was not false."))
        _collect_forbidden_effects(payload, f"blocked_intent.{intent}", issues)

    missing_arg = invoke_tool("governance.timeline", timeout=timeout)
    if missing_arg.get("status") != "BLOCKED" or missing_arg.get("reason_code") != "missing_required_argument":
        issues.append(_issue("missing_argument_contract_drift", "governance.timeline missing proposal_id must be BLOCKED."))

    adapter_missing_arg = adapter_request({"agent": "hermes-agent", "intent": "show_timeline"}, timeout=timeout)
    if adapter_missing_arg.get("status") != "BLOCKED" or adapter_missing_arg.get("reason_code") != "missing_proposal_id":
        issues.append(_issue("adapter_missing_argument_contract_drift", "show_timeline missing proposal_id must be BLOCKED."))

    return {
        "contract_version": CONTRACT_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "invocation-contract-freeze",
        "scale": "personal-local",
        "write": False,
        "locked_contract": {
            "expected_tools": EXPECTED_TOOLS,
            "expected_intent_tool_map": EXPECTED_INTENT_TOOL_MAP,
            "expected_blocked_intents": sorted(EXPECTED_BLOCKED_INTENTS),
            "expected_blocked_capabilities": sorted(EXPECTED_BLOCKED_CAPABILITIES),
            "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
        },
        "discovery": {
            "shield_version": discovery.get("shield_version"),
            "tool_count": discovery.get("tool_count"),
            "write": discovery.get("write"),
            "blocked_capabilities": discovery.get("blocked_capabilities"),
        },
        "safe_invocations": safe_invocations,
        "blocked_invocations": blocked_invocations,
        "adapter_safe_intents": adapter_safe,
        "adapter_blocked_intents": adapter_blocked,
        "argument_validation": {
            "invocation_missing_proposal_id": {
                "status": missing_arg.get("status"),
                "reason_code": missing_arg.get("reason_code"),
                "write": missing_arg.get("write"),
            },
            "adapter_missing_proposal_id": {
                "status": adapter_missing_arg.get("status"),
                "reason_code": adapter_missing_arg.get("reason_code"),
                "write": adapter_missing_arg.get("write"),
            },
        },
        "issue_count": len(issues),
        "issues": issues,
    }


def _summarize_invocation(name, payload):
    return {
        "tool": name,
        "status": payload.get("status"),
        "reason_code": payload.get("reason_code"),
        "write": payload.get("write"),
        "payload_status": payload.get("payload", {}).get("status") if isinstance(payload.get("payload"), dict) else None,
    }


def _summarize_adapter(intent, payload):
    return {
        "intent": intent,
        "status": payload.get("status"),
        "tool": payload.get("tool"),
        "reason_code": payload.get("reason_code"),
        "write": payload.get("write"),
    }


def _collect_forbidden_effects(value, path, issues):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    issues.append(_issue("forbidden_effect_true", f"{path}.effects.{key} became true."))
        for key, child in value.items():
            _collect_forbidden_effects(child, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _collect_forbidden_effects(child, f"{path}[{index}]", issues)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"contract_version: {payload['contract_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"tool_count: {payload['discovery']['tool_count']}",
        f"safe_invocations: {len(payload['safe_invocations'])}",
        f"blocked_invocations: {len(payload['blocked_invocations'])}",
        f"adapter_safe_intents: {len(payload['adapter_safe_intents'])}",
        f"adapter_blocked_intents: {len(payload['adapter_blocked_intents'])}",
        f"issue_count: {payload['issue_count']}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate frozen Runes Shield invocation and Hermes adapter contracts."
    )
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = validate(timeout=args.timeout)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
