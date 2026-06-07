#!/usr/bin/env python3
# M26.4 human-approved promotion rollback plan dry-run helper.

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from promotion_apply_preflight_m26_2 import build_apply_preflight
except ImportError:  # pragma: no cover
    from tools.runes.promotion_apply_preflight_m26_2 import build_apply_preflight

SCHEMA_VERSION = "m26.4.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_rollback_plan_preview(
    root: Path,
    project: str,
    proposal_id: str,
    target_path: str,
    heading: str,
    insert_text: str,
    expected_pre_hash: str | None = None,
    human_confirmation: str | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    preflight = build_apply_preflight(
        root=root,
        project=project,
        proposal_id=proposal_id,
        target_path=target_path,
        heading=heading,
        insert_text=insert_text,
        expected_pre_hash=expected_pre_hash,
        human_confirmation=human_confirmation,
        reason=reason,
    )

    target = preflight.get("target", {})
    patch = preflight.get("patch_preview", {})
    rollback = preflight.get("rollback_plan", {})
    preflight_status = preflight.get("status")

    target_abs = (root / Path(target_path)).resolve()
    current_hash = sha256_file(target_abs) if target.get("path_ok") else None

    plan_status = "PASS" if preflight_status == "PASS" else "BLOCKED"

    rollback_steps = [
        "Capture pre-apply target file snapshot before future apply.",
        "Record operation metadata in append-only operation trail.",
        "Apply candidate patch only after explicit human confirmation.",
        "Run post-apply verification/smoke.",
        "If rollback is required, restore target file from snapshot.",
        "Re-run post-rollback verification/smoke.",
        "Record rollback operation evidence in append-only trail.",
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M26.4 Promotion rollback plan preview",
        "status": plan_status,
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "target": {
            "path": target_path,
            "path_ok": target.get("path_ok"),
            "exists": target.get("exists"),
            "current_sha256": current_hash,
            "pre_apply_hash": target.get("current_sha256"),
            "expected_pre_hash": target.get("expected_pre_hash"),
            "expected_pre_hash_matches": target.get("expected_pre_hash_matches"),
        },
        "preflight": {
            "status": preflight_status,
            "ready_for_future_apply": preflight.get("preflight", {}).get("ready_for_future_apply"),
            "hard_errors": preflight.get("preflight", {}).get("hard_errors", []),
            "human_confirmation_still_required": preflight.get("preflight", {}).get("human_confirmation_still_required"),
        },
        "patch_evidence": {
            "patch_preview_status": patch.get("status"),
            "candidate_evidence_hash": patch.get("candidate_evidence_hash"),
            "unified_diff": patch.get("unified_diff"),
        },
        "rollback_preview": {
            "rollback_available_later": rollback.get("rollback_available_later"),
            "rollback_strategy": rollback.get("rollback_strategy"),
            "requires_future_snapshot": True,
            "requires_operation_record": True,
            "requires_post_rollback_verification": True,
            "implemented_now": False,
            "snapshot_written_now": False,
            "rollback_steps": rollback_steps,
        },
        "operation_record_preview": {
            "would_record_apply_later": True,
            "would_record_rollback_later": True,
            "append_only_record_required": True,
            "implemented_now": False,
        },
        "mutations": {
            "target_file_written": False,
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
            "operation_record_written": False,
            "rollback_snapshot_written": False,
            "rollback_applied": False,
            "files_written": False,
        },
    }


def render_rollback_markdown(result: dict[str, Any]) -> str:
    target = result["target"]
    preflight = result["preflight"]
    patch = result["patch_evidence"]
    rollback = result["rollback_preview"]
    mutations = result["mutations"]

    lines = [
        "## Promotion Rollback Plan Preview",
        "",
        f"Status: {result['status']}",
        f"Mode: {result['mode']}",
        f"Project: {result['project']}",
        f"Proposal ID: {result['proposal_id']}",
        f"Target path: {target['path']}",
        "",
        "### Preflight evidence",
        "",
        f"- Preflight status: {preflight['status']}",
        f"- Ready for future apply: {preflight['ready_for_future_apply']}",
        f"- Target path OK: {target['path_ok']}",
        f"- Current SHA256: {target['current_sha256']}",
        f"- Expected pre-apply hash matches: {target['expected_pre_hash_matches']}",
        f"- Candidate evidence hash: {patch['candidate_evidence_hash']}",
        "",
        "### Rollback plan",
        "",
        f"- Rollback available later: {rollback['rollback_available_later']}",
        f"- Requires future snapshot: {rollback['requires_future_snapshot']}",
        f"- Requires operation record: {rollback['requires_operation_record']}",
        f"- Requires post-rollback verification: {rollback['requires_post_rollback_verification']}",
        f"- Implemented now: {rollback['implemented_now']}",
        "",
        "### Rollback steps",
        "",
    ]

    for idx, step in enumerate(rollback.get("rollback_steps", []), start=1):
        lines.append(f"{idx}. {step}")

    lines.extend([
        "",
        "### Patch evidence",
        "",
        "```diff",
        patch.get("unified_diff") or "",
        "```",
        "",
        "### Boundary",
        "",
        f"- Target file written now: {mutations['target_file_written']}",
        f"- Trusted wiki mutation now: {mutations['curated_wiki_mutated']}",
        f"- Database mutation now: {mutations['database_mutated']}",
        f"- Importer mutation now: {mutations['importer_mutated']}",
        f"- Operation record written now: {mutations['operation_record_written']}",
        f"- Rollback snapshot written now: {mutations['rollback_snapshot_written']}",
        f"- Rollback applied now: {mutations['rollback_applied']}",
        "",
        "This is a rollback plan preview only. M26.4 does not write snapshots or apply rollback.",
        "",
    ])

    return "\n".join(lines)


def print_rollback_preview(result: dict[str, Any]) -> None:
    print("Promotion Rollback Plan Preview")
    print("===============================")
    print(render_rollback_markdown(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Promotion rollback plan dry-run helper.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--heading", required=True)
    parser.add_argument("--insert-text", required=True)
    parser.add_argument("--expected-pre-hash")
    parser.add_argument("--human-confirmation")
    parser.add_argument("--reason")
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    payload = build_rollback_plan_preview(
        root=root,
        project=args.project,
        proposal_id=args.proposal_id,
        target_path=args.target_path,
        heading=args.heading,
        insert_text=args.insert_text,
        expected_pre_hash=args.expected_pre_hash,
        human_confirmation=args.human_confirmation,
        reason=args.reason,
    )

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_rollback_markdown(payload))
    else:
        print_rollback_preview(payload)

    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
