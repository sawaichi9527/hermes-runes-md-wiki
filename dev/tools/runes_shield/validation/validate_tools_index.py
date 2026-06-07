#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "tools" / "runes_shield" / "runes_shield_tools_index.json"

REQUIRED_TOOL_NAMES = {
    "proposal_registry.list",
    "proposal_registry.show",
    "proposal_registry.show_payload",
    "proposal_review_queue.list",
    "proposal_review_queue.show",
    "proposal_review_queue.show_payload",
    "smoke.proposal_registry_all",
    "smoke.proposal_review_queue_all",
}

BLOCKED_TOOL_NAMES = {
    "proposal.apply",
    "proposal.approve",
    "proposal.promote",
    "wiki.write",
    "database.mutate",
}


def main():
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    tool_names = {tool["name"] for tool in data["tools"]}
    blocked_names = set(data["blocked_tool_names"])

    missing_tools = sorted(REQUIRED_TOOL_NAMES - tool_names)
    missing_blocked = sorted(BLOCKED_TOOL_NAMES - blocked_names)

    result = {
        "status": "PASS"
        if not missing_tools and not missing_blocked
        else "FAIL",
        "index_version": data["index_version"],
        "write": data["write"],
        "tool_count": len(tool_names),
        "missing_tools": missing_tools,
        "missing_blocked_tools": missing_blocked,
        "blocked_capabilities": data["blocked_capabilities"],
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] != "PASS":
        raise SystemExit("tool index validation failed")


if __name__ == "__main__":
    main()
