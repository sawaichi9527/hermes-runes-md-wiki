#!/usr/bin/env python3

import argparse
import json

from runes_agent_workflow import (
    DEFAULT_PROPOSAL_ID,
    OUTPUT_CHOICES,
    run_workflow,
)

WORKFLOW_VERSION = "m58-governed-agent-workflow-v1"
DEFAULT_AGENT = "generic-governed-agent"
DEFAULT_CONVERSATION_ID = "conv-m58-generic-governed-workflow"
AGENT_SCOPE = "agent-agnostic"
REFERENCE_AGENT_NOTE = (
    "The caller may be Hermes-agent, OpenClaw, or any future governed agent. "
    "Hermes-agent is only a development/reference caller, not a required runtime identity."
)


def run_governed_workflow(agent, conversation_id, proposal_id, profile, timeout):
    payload = run_workflow(
        agent=agent,
        conversation_id=conversation_id,
        proposal_id=proposal_id,
        profile=profile,
        timeout=timeout,
    )

    payload["workflow_version"] = WORKFLOW_VERSION
    payload["agent_scope"] = AGENT_SCOPE
    payload["reference_agent_note"] = REFERENCE_AGENT_NOTE
    payload["default_agent"] = DEFAULT_AGENT
    payload["compatibility_alias"] = "runes_agent_workflow.py"
    payload["formal_cli"] = "runes_governed_agent_workflow.py"

    return payload


def render_table(payload):
    lines = [
        f"workflow_version: {payload['workflow_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"agent_scope: {payload['agent_scope']}",
        f"scale: {payload['scale']}",
        f"agent: {payload['agent']}",
        f"default_agent: {payload['default_agent']}",
        f"formal_cli: {payload['formal_cli']}",
        f"compatibility_alias: {payload['compatibility_alias']}",
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
        description="M58 agent-agnostic governed workflow for any Runes Shield-compatible governed agent."
    )
    parser.add_argument("--agent", default=DEFAULT_AGENT)
    parser.add_argument("--conversation-id", default=DEFAULT_CONVERSATION_ID)
    parser.add_argument("--proposal-id", default=DEFAULT_PROPOSAL_ID)
    parser.add_argument("--profile", default="p0")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = run_governed_workflow(
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
