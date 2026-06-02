#!/usr/bin/env python3
"""Runes Shield agent-facing CLI.

P0 scope:
- capabilities: read-only capability discovery
- guidance: read-only invocation guidance
- offer: deterministic recommendation for whether Hermes-agent should ask the user about creating a governed proposal

This CLI intentionally does not create proposals, approve/reject content,
promote notes, import content, rebuild indexes, or mutate trusted memory.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from offer_policy import classify_offer_intent, decision_to_dict
except ImportError:  # pragma: no cover - fallback for module execution contexts
    from tools.runes.offer_policy import classify_offer_intent, decision_to_dict

SCHEMA_VERSION = "m21.3.p0.v1"
TOOL_NAME = "runes"
SHIELD_NAME = "Runes Shield"
SHIELD_SUBTITLE = "A governed invocation boundary for trusted Markdown memory."
SHIELD_SLOGAN = "Hermes-agent may invoke the runes, but must never breach the shield."
SHIELD_SLOGAN_ZH = "Hermes-agent 可以召喚符文，但不得突破護盾。"

CANONICAL_FILES = [
    "wiki/hermes_runes_index.md",
    "wiki/_system/runes_shield_contract.md",
    "wiki/_system/runes_invocation_policy.md",
    "wiki/_system/runes_agent_guidance.md",
]

ALLOWED_AGENT_CAPABILITIES = [
    {
        "name": "capabilities",
        "command": "runes capabilities --json",
        "write": False,
        "description": "Discover Runes Shield capabilities, safety boundaries, and human-only operations.",
    },
    {
        "name": "guidance",
        "command": "runes guidance --json",
        "write": False,
        "description": "Read agent-facing invocation guidance, consent rules, and durable-memory trigger guidance.",
    },
    {
        "name": "offer",
        "command": "runes offer --text '<message>' --json",
        "write": False,
        "description": "Deterministically decide whether Hermes-agent should ask the user about creating a governed proposal.",
    },
    {
        "name": "propose",
        "command": "runes propose --json",
        "write": True,
        "p0_status": "planned_not_implemented_in_m21_3",
        "requires_user_consent": True,
        "creates_trusted_memory": False,
        "description": "Create a governed draft proposal after user consent. Not implemented in M21.3.",
    },
    {
        "name": "proposal_list",
        "command": "runes proposal list --json",
        "write": False,
        "p0_status": "planned_not_implemented_in_m21_3",
        "description": "Inspect proposal states without mutating them. Not implemented in M21.3.",
    },
    {
        "name": "proposal_show",
        "command": "runes proposal show --json",
        "write": False,
        "p0_status": "planned_not_implemented_in_m21_3",
        "description": "Inspect one proposal without mutating it. Not implemented in M21.3.",
    },
    {
        "name": "recall",
        "command": "runes recall --json",
        "write": False,
        "p0_status": "planned_wrapper_not_implemented_in_m21_3",
        "description": "Retrieve trusted indexed memory evidence through a Runes Shield wrapper. Existing recall tools remain separate until wrapped.",
    },
    {
        "name": "smoke",
        "command": "runes smoke --json",
        "write": False,
        "p0_status": "planned_wrapper_not_implemented_in_m21_3",
        "description": "Verify Runes Shield and memory tool health. Not implemented in M21.3.",
    },
]

FORBIDDEN_AGENT_OPERATIONS = [
    "directly read arbitrary internal wiki files as operational authority",
    "write or edit wiki/*.md directly",
    "write or edit wiki/_system/*.md directly",
    "move proposal files between states",
    "approve proposals",
    "reject proposals",
    "promote reviewed proposals into curated wiki notes",
    "import reviewed content outside controlled wrapper behavior",
    "rebuild indexes outside controlled wrapper behavior",
    "delete, archive, or mutate trusted memory content",
    "write PostgreSQL / FTS / pgvector records",
    "mutate importer artifacts",
    "bypass human approval",
    "treat draft or rejected proposal content as trusted memory",
]

HUMAN_ONLY_OPERATIONS = [
    "approve proposal",
    "reject proposal",
    "promote reviewed proposal into curated wiki note",
    "direct wiki edit",
    "destructive delete / archive",
    "database rebuild / schema mutation",
    "policy mutation",
    "importer lifecycle changes beyond controlled wrapper behavior",
]

TRIGGER_CANDIDATES = [
    "project decision",
    "architecture decision",
    "frozen baseline",
    "verification result",
    "PASS / FAIL marker",
    "service layout decision",
    "command procedure",
    "troubleshooting outcome",
    "future action item",
    "naming decision",
    "governance rule",
    "repeated knowledge likely to be asked about later",
    "explicit user request to remember, solidify, write into Runes, write into wiki, or make long-term memory",
]

NON_TRIGGER_CANDIDATES = [
    "casual one-off conversation",
    "unverified speculation",
    "brainstorming not accepted by the user",
    "raw logs with secrets",
    "credentials / tokens / passwords",
    "private keys or API keys",
    "personal data not clearly approved for persistence",
    "transient debugging output not useful later",
    "content conflicting with existing trusted memory without review",
    "content that may require sanitization first",
]

CONSENT_EXAMPLES = [
    "go",
    "好",
    "可以",
    "建立 proposal",
    "寫進 Runes",
    "寫進 roadmap",
    "固化",
    "記到 wiki",
    "yes, create the proposal",
]

SECRET_WARNINGS = [
    "API keys",
    "database passwords",
    "Telegram bot tokens",
    "LM Studio / OpenAI-compatible API keys",
    "Tavily keys",
    "private credentials",
    "private tokens",
    "raw secret-bearing logs",
]


def find_repo_root() -> Path:
    env_root = os.environ.get("HERMES_RUNES_ROOT") or os.environ.get("HERMES_MEMORY_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    # tools/runes/runes.py -> repo root is two parents up.
    return Path(__file__).resolve().parents[2]


def file_status(root: Path) -> list[dict[str, Any]]:
    result = []
    for rel in CANONICAL_FILES:
        path = root / rel
        result.append(
            {
                "path": rel,
                "exists": path.exists(),
                "required_for_p0_bootstrap": True,
            }
        )
    return result


def base_payload(root: Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "shield": {
            "name": SHIELD_NAME,
            "subtitle": SHIELD_SUBTITLE,
            "slogan": SHIELD_SLOGAN,
            "slogan_zh": SHIELD_SLOGAN_ZH,
        },
        "repo_root": str(root),
        "canonical_p0_files": file_status(root),
        "p0_boundary": {
            "agent_must_use_runes_provided_interfaces": True,
            "agent_direct_internal_mutation_allowed": False,
            "human_approval_required_for_trusted_memory": True,
            "draft_or_rejected_proposals_are_trusted_memory": False,
        },
    }


def capabilities_payload(root: Path) -> dict[str, Any]:
    payload = base_payload(root)
    payload.update(
        {
            "command": "capabilities",
            "status": "PASS",
            "mode": "read_only",
            "implemented_in_m21_3": ["capabilities", "guidance", "offer"],
            "capabilities": ALLOWED_AGENT_CAPABILITIES,
            "forbidden_agent_operations": FORBIDDEN_AGENT_OPERATIONS,
            "human_only_operations": HUMAN_ONLY_OPERATIONS,
            "notes": [
                "M21.3 exposes read-only capability, guidance, and offer-policy discovery only.",
                "Offer policy recommends whether Hermes-agent should ask the user; it does not create proposals.",
                "Proposal creation and proposal inspection are documented P0 targets but not implemented in this milestone.",
                "Hermes-agent must not infer operational behavior from incidental local wiki documents.",
            ],
        }
    )
    return payload


def guidance_payload(root: Path) -> dict[str, Any]:
    payload = base_payload(root)
    payload.update(
        {
            "command": "guidance",
            "status": "PASS",
            "mode": "read_only",
            "agent_interaction": {
                "should_offer_runes_when": TRIGGER_CANDIDATES,
                "should_not_offer_runes_when": NON_TRIGGER_CANDIDATES,
                "consent_required_before_propose": True,
                "clear_consent_examples": CONSENT_EXAMPLES,
                "recommended_prompt_zh": "這段內容看起來像是後續會重複使用的專案知識。要不要我幫你建立一筆 Hermes Runes governed proposal，先放入待審核區，之後由你確認後再固化成 Markdown wiki？",
                "short_prompt_zh": "這看起來值得固化成長期專案記憶。要不要我透過 Runes Shield 建立一筆 governed proposal？",
                "recommended_prompt_en": "This looks like durable project knowledge that may be useful later. Would you like me to create a governed Hermes Runes proposal for human review before it becomes trusted Markdown memory?",
            },
            "proposal_input_guidance": {
                "include": [
                    "concise title",
                    "source context",
                    "accepted decision or fact",
                    "rationale when available",
                    "scope",
                    "non-goals / exclusions",
                    "suggested target domain or project",
                    "sensitivity notes",
                    "user consent marker",
                ],
                "exclude": [
                    "secrets",
                    "raw credentials",
                    "raw API keys",
                    "full unfiltered logs with private data",
                    "unsupported claims as trusted facts",
                    "model speculation without user acceptance",
                ],
            },
            "secret_warnings": SECRET_WARNINGS,
            "recall_guidance": {
                "runes_recall_is_evidence_not_final_truth": True,
                "agent_should_compare_with": [
                    "current user instruction",
                    "current conversation context",
                    "native memory",
                    "third-party notes or RAG",
                    "web search results when freshness matters",
                    "direct user corrections",
                ],
            },
        }
    )
    return payload


def offer_payload(root: Path, text: str) -> dict[str, Any]:
    payload = base_payload(root)
    decision = decision_to_dict(classify_offer_intent(text))
    payload.update(
        {
            "command": "offer",
            "status": "PASS",
            "mode": "read_only",
            "input_chars": len(text or ""),
            "decision": decision,
            "notes": [
                "This command only recommends whether Hermes-agent should ask the user about a governed proposal.",
                "This command never creates proposals and never mutates memory.",
                "User consent is still required before any future runes propose command.",
            ],
        }
    )
    return payload


def emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    print(f"{payload['shield']['name']}: {payload['shield']['subtitle']}")
    print(payload["shield"]["slogan"])
    print(payload["shield"]["slogan_zh"])
    print(f"status={payload.get('status', 'UNKNOWN')} command={payload.get('command', 'unknown')}")
    if payload.get("command") == "offer":
        decision = payload.get("decision", {})
        print(f"should_offer={decision.get('should_offer')} action={decision.get('action')} confidence={decision.get('confidence')}")
    print("Use --json for agent-facing structured output.")
    return 0


def read_text_arg(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("runes offer requires --text, --file, or stdin input")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="runes",
        description="Runes Shield agent-facing CLI for governed Markdown memory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("capabilities", "guidance"):
        sub = subparsers.add_parser(command, help=f"Run read-only {command} command.")
        sub.add_argument(
            "--json",
            action="store_true",
            help="Emit stable JSON output for agent/tool consumption.",
        )

    offer = subparsers.add_parser(
        "offer",
        help="Decide whether Hermes-agent should ask the user about creating a governed proposal.",
    )
    offer.add_argument("--text", help="Text to classify.")
    offer.add_argument("--file", help="UTF-8 text file to classify.")
    offer.add_argument(
        "--json",
        action="store_true",
        help="Emit stable JSON output for agent/tool consumption.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    root = find_repo_root()

    if args.command == "capabilities":
        return emit(capabilities_payload(root), args.json)
    if args.command == "guidance":
        return emit(guidance_payload(root), args.json)
    if args.command == "offer":
        return emit(offer_payload(root, read_text_arg(args)), args.json)

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
