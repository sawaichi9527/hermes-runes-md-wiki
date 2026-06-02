#!/usr/bin/env python3
"""Runes Shield agent-facing CLI."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from cleanup_plan_m22_4 import cleanup_plan
    from offer_policy import classify_offer_intent, decision_to_dict
    from proposal_hygiene_m22_3 import hygiene_report
    from proposal_reader_m22_2 import list_proposals, show_proposal
    from proposal_writer_m22_1 import write_proposal
except ImportError:  # pragma: no cover
    from tools.runes.cleanup_plan_m22_4 import cleanup_plan
    from tools.runes.offer_policy import classify_offer_intent, decision_to_dict
    from tools.runes.proposal_hygiene_m22_3 import hygiene_report
    from tools.runes.proposal_reader_m22_2 import list_proposals, show_proposal
    from tools.runes.proposal_writer_m22_1 import write_proposal

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
    "restricted material",
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

FORBIDDEN_AGENT_OPERATIONS = [
    "read arbitrary internal wiki files as operational authority",
    "edit trusted wiki files outside controlled commands",
    "move proposal files between states",
    "approve proposals",
    "reject proposals",
    "promote reviewed proposals into curated wiki notes",
    "import reviewed content outside controlled wrapper behavior",
    "rebuild indexes outside controlled wrapper behavior",
    "delete, archive, or mutate trusted memory content",
    "write index records",
    "mutate importer artifacts",
    "treat draft or rejected proposal content as trusted memory",
]

HUMAN_ONLY_OPERATIONS = [
    "approve proposal",
    "reject proposal",
    "promote reviewed proposal into curated wiki note",
    "direct wiki edit",
    "destructive delete / archive",
    "index rebuild / schema mutation",
    "policy mutation",
    "importer lifecycle changes beyond controlled wrapper behavior",
]


def find_repo_root() -> Path:
    env_root = os.environ.get("HERMES_RUNES_ROOT") or os.environ.get("HERMES_MEMORY_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def file_status(root: Path) -> list[dict[str, Any]]:
    return [
        {"path": rel, "exists": (root / rel).exists(), "required_for_p0_bootstrap": True}
        for rel in CANONICAL_FILES
    ]


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
            "implemented": [
                "capabilities",
                "guidance",
                "offer",
                "propose",
                "proposal_list",
                "proposal_show",
                "proposal_hygiene",
                "proposal_cleanup_plan",
            ],
            "implemented_in_m21_3": ["capabilities", "guidance", "offer"],
            "implemented_in_m22_1": ["propose"],
            "implemented_in_m22_2": ["proposal_list", "proposal_show"],
            "implemented_in_m22_3": ["proposal_hygiene"],
            "implemented_in_m22_5": ["proposal_cleanup_plan"],
            "capabilities": [
                {"name": "capabilities", "command": "runes capabilities --json", "write": False},
                {"name": "guidance", "command": "runes guidance --json", "write": False},
                {"name": "offer", "command": "runes offer --text '<message>' --json", "write": False},
                {"name": "propose", "command": "runes propose --title '<title>' --text '<text>' --consent '<marker>' --json", "write": True, "requires_user_consent": True, "creates_trusted_memory": False, "p0_status": "m22_1_draft_only_implemented"},
                {"name": "proposal_list", "command": "runes proposal list --json", "write": False, "p0_status": "m22_2_read_only_implemented"},
                {"name": "proposal_show", "command": "runes proposal show --id '<proposal_id>' --json", "write": False, "p0_status": "m22_2_read_only_implemented"},
                {"name": "proposal_hygiene", "command": "runes proposal hygiene --json", "write": False, "p0_status": "m22_3_read_only_implemented"},
                {"name": "proposal_cleanup_plan", "command": "runes proposal cleanup-plan --json", "write": False, "p0_status": "m22_5_dry_run_implemented"},
                {"name": "recall", "command": "runes recall --json", "write": False, "p0_status": "planned_wrapper_not_implemented_in_m22_5"},
                {"name": "smoke", "command": "runes smoke --json", "write": False, "p0_status": "planned_wrapper_not_implemented_in_m22_5"},
            ],
            "forbidden_agent_operations": FORBIDDEN_AGENT_OPERATIONS,
            "human_only_operations": HUMAN_ONLY_OPERATIONS,
            "notes": [
                "M22.1 adds controlled draft proposal creation after explicit consent.",
                "M22.2 adds read-only proposal list/show inspection.",
                "M22.3 adds read-only proposal status hygiene reporting.",
                "M22.5 adds cleanup-plan CLI dry-run.",
                "Draft proposals are not trusted memory.",
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
                "include": ["concise title", "source context", "accepted decision or fact", "scope", "user consent marker"],
                "exclude": ["restricted material", "unsupported claims as trusted facts", "model speculation without user acceptance"],
            },
            "secret_warnings": ["restricted material should be excluded from proposals"],
            "recall_guidance": {"runes_recall_is_evidence_not_final_truth": True},
        }
    )
    return payload


def offer_payload(root: Path, text: str) -> dict[str, Any]:
    payload = base_payload(root)
    decision = decision_to_dict(classify_offer_intent(text))
    payload.update({"command": "offer", "status": "PASS", "mode": "read_only", "input_chars": len(text or ""), "decision": decision})
    return payload


def emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if "shield" in payload:
        print(f"{payload['shield']['name']}: {payload['shield']['subtitle']}")
        print(payload["shield"]["slogan"])
        print(payload["shield"]["slogan_zh"])
    print(f"status={payload.get('status', 'UNKNOWN')} command={payload.get('command', 'unknown')}")
    if payload.get("command") == "offer":
        decision = payload.get("decision", {})
        print(f"should_offer={decision.get('should_offer')} action={decision.get('action')} confidence={decision.get('confidence')}")
    if "count" in payload:
        print(f"count={payload['count']}")
    if "issue_count" in payload:
        print(f"issue_count={payload['issue_count']}")
    if "planned_action_count" in payload:
        print(f"planned_action_count={payload['planned_action_count']}")
    print("Use --json for agent-facing structured output.")
    return 0


def read_text_arg(args: argparse.Namespace) -> str:
    if getattr(args, "text", None) is not None:
        return args.text
    if getattr(args, "file", None):
        return Path(args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit(f"runes {args.command} requires --text, --file, or stdin input")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="runes", description="Runes Shield agent-facing CLI for governed Markdown memory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("capabilities", "guidance"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--json", action="store_true")

    offer = subparsers.add_parser("offer")
    offer.add_argument("--text")
    offer.add_argument("--file")
    offer.add_argument("--json", action="store_true")

    propose = subparsers.add_parser("propose")
    propose.add_argument("--title", required=True)
    propose.add_argument("--text")
    propose.add_argument("--file")
    propose.add_argument("--project", default="k6-freelancer")
    propose.add_argument("--source-context", default="user_provided")
    propose.add_argument("--consent")
    propose.add_argument("--output-root")
    propose.add_argument("--json", action="store_true")

    proposal = subparsers.add_parser("proposal")
    proposal_sub = proposal.add_subparsers(dest="proposal_command", required=True)

    proposal_list = proposal_sub.add_parser("list")
    proposal_list.add_argument("--project", default="k6-freelancer")
    proposal_list.add_argument("--state", default="all", choices=["all", "draft", "approved", "rejected"])
    proposal_list.add_argument("--output-root")
    proposal_list.add_argument("--json", action="store_true")

    proposal_show = proposal_sub.add_parser("show")
    proposal_show.add_argument("--project", default="k6-freelancer")
    proposal_show.add_argument("--id", required=True)
    proposal_show.add_argument("--output-root")
    proposal_show.add_argument("--no-body", action="store_true")
    proposal_show.add_argument("--json", action="store_true")

    proposal_hygiene = proposal_sub.add_parser("hygiene")
    proposal_hygiene.add_argument("--project", default="k6-freelancer")
    proposal_hygiene.add_argument("--output-root")
    proposal_hygiene.add_argument("--json", action="store_true")

    cleanup = proposal_sub.add_parser("cleanup-plan")
    cleanup.add_argument("--project", default="k6-freelancer")
    cleanup.add_argument("--output-root")
    cleanup.add_argument("--json", action="store_true")

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
    if args.command == "propose":
        result = write_proposal(root=root, title=args.title, text=read_text_arg(args), project=args.project, source_context=args.source_context, consent=args.consent, output_root=args.output_root)
        if args.json:
            print(json.dumps(result.data, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print(f"{result.data['suite']}: {result.status}")
            if result.path:
                print(f"path={result.path}")
            if result.reason:
                print(f"reason={result.reason}")
            print("Use --json for details.")
        return 0 if result.status == "PASS" else 2
    if args.command == "proposal":
        if args.proposal_command == "list":
            return emit(list_proposals(root, args.project, args.state, args.output_root), args.json)
        if args.proposal_command == "show":
            return emit(show_proposal(root, args.project, args.id, args.output_root, include_body=not args.no_body), args.json)
        if args.proposal_command == "hygiene":
            return emit(hygiene_report(root, args.project, args.output_root), args.json)
        if args.proposal_command == "cleanup-plan":
            return emit(cleanup_plan(root, args.project, args.output_root), args.json)

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
