#!/usr/bin/env python3
# M26.2 human-approved promotion apply preflight dry-run helper.

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from promotion_patch_m25_2 import build_promotion_patch_preview
except ImportError:  # pragma: no cover
    from tools.runes.promotion_patch_m25_2 import build_promotion_patch_preview

SCHEMA_VERSION = "m26.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_wiki_path(root: Path, target_path: str) -> tuple[Path, bool, str | None]:
    rel = Path(target_path)
    abs_path = (root / rel).resolve()
    try:
        abs_path.relative_to(root.resolve())
    except ValueError:
        return abs_path, False, "target path escapes repository root"

    rel_from_root = abs_path.relative_to(root.resolve())

    if not str(rel_from_root).startswith("wiki/"):
        return abs_path, False, "target path must be under wiki/"

    if ".env" in rel_from_root.parts:
        return abs_path, False, "target path must not contain .env"

    if any(part.startswith(".") for part in rel_from_root.parts):
        return abs_path, False, "target path must not include hidden path parts"

    return abs_path, True, None


def build_apply_preflight(
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
    abs_path, path_ok, path_error = ensure_wiki_path(root, target_path)

    current_hash = sha256_file(abs_path)

    patch_preview = build_promotion_patch_preview(
        root=root,
        project=project,
        proposal_id=proposal_id,
        target_path=target_path,
        heading=heading,
        insert_text=insert_text,
        reason=reason,
    )

    candidate_evidence = json.dumps(
        {
            "target_path": target_path,
            "heading": heading,
            "insert_text": insert_text,
            "patch_preview_schema": patch_preview.get("schema_version"),
            "unified_diff": patch_preview.get("unified_diff"),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    candidate_evidence_hash = sha256_text(candidate_evidence)

    confirmation_required = f"APPLY-PREFLIGHT:{proposal_id}:{target_path}:{current_hash or 'missing'}"
    confirmation_matches = human_confirmation == confirmation_required

    pre_hash_matches = True
    pre_hash_error = None
    if expected_pre_hash is not None:
        pre_hash_matches = expected_pre_hash == current_hash
        if not pre_hash_matches:
            pre_hash_error = "expected pre-apply hash does not match current target file hash"

    hard_errors = []
    if not path_ok:
        hard_errors.append(path_error)
    if expected_pre_hash is not None and not pre_hash_matches:
        hard_errors.append(pre_hash_error)

    status = "PASS" if not hard_errors else "BLOCKED"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M26.2 Human-approved promotion apply preflight dry-run",
        "status": status,
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "target": {
            "path": target_path,
            "exists": abs_path.exists(),
            "path_ok": path_ok,
            "path_error": path_error,
            "current_sha256": current_hash,
            "expected_pre_hash": expected_pre_hash,
            "expected_pre_hash_matches": pre_hash_matches,
        },
        "confirmation": {
            "human_confirmation_required": True,
            "required_confirmation_token": confirmation_required,
            "provided_confirmation_token": human_confirmation,
            "confirmation_matches": confirmation_matches,
            "confirmation_is_required_for_future_apply": True,
            "confirmation_does_not_apply_now": True,
        },
        "patch_preview": {
            "status": patch_preview.get("status"),
            "mode": patch_preview.get("mode"),
            "unified_diff": patch_preview.get("unified_diff"),
            "candidate_evidence_hash": candidate_evidence_hash,
        },
        "rollback_plan": {
            "rollback_available_later": True,
            "rollback_strategy": "restore target file content using pre_apply_hash and operation record snapshot",
            "requires_future_snapshot": True,
            "pre_apply_hash": current_hash,
            "target_path": target_path,
            "implemented_now": False,
        },
        "operation_record_preview": {
            "would_record_operation_later": True,
            "operation_type": "promotion.apply.preflight",
            "append_only_record_required_for_future_apply": True,
            "implemented_now": False,
        },
        "preflight": {
            "ready_for_future_apply": bool(path_ok and pre_hash_matches),
            "hard_errors": [item for item in hard_errors if item],
            "human_confirmation_still_required": True,
            "post_apply_verification_required": True,
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
            "files_written": False,
        },
    }


def render_preflight_markdown(result: dict[str, Any]) -> str:
    target = result["target"]
    confirmation = result["confirmation"]
    preflight = result["preflight"]
    mutations = result["mutations"]
    rollback = result["rollback_plan"]
    patch = result["patch_preview"]

    return "\n".join([
        "## Human-approved Promotion Apply Preflight",
        "",
        f"Status: {result['status']}",
        f"Mode: {result['mode']}",
        f"Project: {result['project']}",
        f"Proposal ID: {result['proposal_id']}",
        f"Target path: {target['path']}",
        "",
        "### Preflight checks",
        "",
        f"- Target path OK: {target['path_ok']}",
        f"- Target exists: {target['exists']}",
        f"- Current SHA256: {target['current_sha256']}",
        f"- Expected pre-apply hash matches: {target['expected_pre_hash_matches']}",
        f"- Ready for future apply: {preflight['ready_for_future_apply']}",
        "",
        "### Human confirmation",
        "",
        f"- Human confirmation required: {confirmation['human_confirmation_required']}",
        f"- Required confirmation token: `{confirmation['required_confirmation_token']}`",
        f"- Confirmation matches: {confirmation['confirmation_matches']}",
        f"- Confirmation does not apply now: {confirmation['confirmation_does_not_apply_now']}",
        "",
        "### Patch evidence",
        "",
        f"- Patch preview status: {patch['status']}",
        f"- Candidate evidence hash: {patch['candidate_evidence_hash']}",
        "",
        "```diff",
        patch.get("unified_diff") or "",
        "```",
        "",
        "### Rollback preview",
        "",
        f"- Rollback available later: {rollback['rollback_available_later']}",
        f"- Requires future snapshot: {rollback['requires_future_snapshot']}",
        f"- Implemented now: {rollback['implemented_now']}",
        "",
        "### Boundary",
        "",
        f"- Target file written now: {mutations['target_file_written']}",
        f"- Trusted wiki mutation now: {mutations['curated_wiki_mutated']}",
        f"- Database mutation now: {mutations['database_mutated']}",
        f"- Importer mutation now: {mutations['importer_mutated']}",
        f"- Operation record written now: {mutations['operation_record_written']}",
        f"- Rollback snapshot written now: {mutations['rollback_snapshot_written']}",
        "",
        "This is a preflight dry-run only. M26.2 does not apply the patch.",
        "",
    ])


def print_preflight(result: dict[str, Any]) -> None:
    print("Human-approved Promotion Apply Preflight")
    print("========================================")
    print(render_preflight_markdown(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Human-approved promotion apply preflight dry-run helper.")
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
    payload = build_apply_preflight(
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
        print(render_preflight_markdown(payload))
    else:
        print_preflight(payload)

    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
