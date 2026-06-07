#!/usr/bin/env python3
# M27.2 human-approved promotion apply controlled-write MVP.

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from promotion_apply_preflight_m26_2 import build_apply_preflight, ensure_wiki_path, sha256_file
    from promotion_patch_m25_2 import candidate_lines
except ImportError:  # pragma: no cover
    from tools.runes.promotion_apply_preflight_m26_2 import build_apply_preflight, ensure_wiki_path, sha256_file
    from tools.runes.promotion_patch_m25_2 import candidate_lines

SCHEMA_VERSION = "m27.2.p0.v1"
DEFAULT_PROJECT = "freelancer"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def safe_slug(value: str) -> str:
    keep = []
    for ch in value.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in {"-", "_", "."}:
            keep.append(ch)
        else:
            keep.append("-")
    slug = "".join(keep).strip("-._")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:96] or "unknown"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_candidate_text(abs_path: Path, heading: str, insert_text: str) -> tuple[str, dict[str, Any]]:
    original = abs_path.read_text(encoding="utf-8").splitlines(keepends=True) if abs_path.exists() else []
    candidate, meta = candidate_lines(original, heading, insert_text)
    return "".join(candidate), meta


def build_apply_result(
    *,
    root: Path,
    project: str,
    proposal_id: str,
    target_path: str,
    heading: str,
    insert_text: str,
    expected_pre_hash: str | None,
    human_confirmation: str | None,
    reason: str | None,
    apply: bool,
    actor: str,
) -> dict[str, Any]:
    abs_path, path_ok, path_error = ensure_wiki_path(root, target_path)
    pre_hash = sha256_file(abs_path) if path_ok else None

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

    required_token = preflight["confirmation"]["required_confirmation_token"]
    confirmation_matches = human_confirmation == required_token
    expected_hash_matches = expected_pre_hash is not None and expected_pre_hash == pre_hash

    hard_errors: list[str] = []
    if not apply:
        hard_errors.append("--apply is required for M27.2 controlled write")
    if not path_ok:
        hard_errors.append(path_error or "target path failed policy")
    if not abs_path.exists() and path_ok:
        hard_errors.append("target file must already exist for M27.2 MVP")
    if expected_pre_hash is None:
        hard_errors.append("--expected-pre-hash is required")
    elif not expected_hash_matches:
        hard_errors.append("expected pre-apply hash does not match current target file hash")
    if not confirmation_matches:
        hard_errors.append("human confirmation token does not match required token")

    if hard_errors:
        return {
            "schema_version": SCHEMA_VERSION,
            "suite": "M27.2 Human-approved controlled promotion apply",
            "status": "BLOCKED",
            "mode": "controlled_apply",
            "project": project,
            "proposal_id": proposal_id,
            "actor": actor,
            "target": {
                "path": target_path,
                "exists": abs_path.exists() if path_ok else False,
                "path_ok": path_ok,
                "path_error": path_error,
                "pre_apply_sha256": pre_hash,
                "expected_pre_hash": expected_pre_hash,
                "expected_pre_hash_matches": expected_hash_matches,
            },
            "confirmation": {
                "required_confirmation_token": required_token,
                "provided_confirmation_token": human_confirmation,
                "confirmation_matches": confirmation_matches,
            },
            "preflight_status": preflight.get("status"),
            "hard_errors": [item for item in hard_errors if item],
            "mutations": {
                "target_file_written": False,
                "rollback_snapshot_written": False,
                "operation_record_written": False,
                "database_mutated": False,
                "importer_mutated": False,
                "proposal_state_mutated": False,
            },
        }

    before_text = abs_path.read_text(encoding="utf-8")
    candidate_text, candidate_meta = build_candidate_text(abs_path, heading, insert_text)
    post_hash = sha256_text(candidate_text)

    stamp = utc_stamp()
    proposal_slug = safe_slug(proposal_id)
    target_slug = safe_slug(target_path.replace("/", "__"))

    backup_dir = root / "backups" / "runes-apply" / stamp[:8]
    op_dir = root / "operations" / "runes-apply" / stamp[:8]
    backup_dir.mkdir(parents=True, exist_ok=True)
    op_dir.mkdir(parents=True, exist_ok=True)

    rollback_snapshot = backup_dir / f"{stamp}-{proposal_slug}-{target_slug}.snapshot.md"
    operation_record = op_dir / f"{stamp}-{proposal_slug}-{target_slug}.json"

    rollback_snapshot.write_text(before_text, encoding="utf-8")
    abs_path.write_text(candidate_text, encoding="utf-8")

    actual_post_hash = sha256_file(abs_path)

    record = {
        "schema_version": SCHEMA_VERSION,
        "operation": "promotion.apply.controlled",
        "status": "PASS",
        "timestamp_utc": stamp,
        "project": project,
        "proposal_id": proposal_id,
        "actor": actor,
        "reason": reason,
        "target_path": target_path,
        "heading": heading,
        "candidate_meta": candidate_meta,
        "pre_apply_sha256": pre_hash,
        "post_apply_sha256": actual_post_hash,
        "expected_pre_hash": expected_pre_hash,
        "confirmation_token_used": human_confirmation,
        "rollback_snapshot": str(rollback_snapshot.relative_to(root)),
        "post_apply_verification_required": True,
        "database_mutated": False,
        "importer_mutated": False,
        "proposal_state_mutated": False,
    }
    operation_record.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M27.2 Human-approved controlled promotion apply",
        "status": "PASS",
        "mode": "controlled_apply",
        "project": project,
        "proposal_id": proposal_id,
        "actor": actor,
        "target": {
            "path": target_path,
            "exists": True,
            "path_ok": True,
            "pre_apply_sha256": pre_hash,
            "post_apply_sha256": actual_post_hash,
            "expected_pre_hash": expected_pre_hash,
            "expected_pre_hash_matches": expected_hash_matches,
            "post_hash_matches_candidate": actual_post_hash == post_hash,
            "candidate_meta": candidate_meta,
        },
        "confirmation": {
            "required_confirmation_token": required_token,
            "provided_confirmation_token": human_confirmation,
            "confirmation_matches": confirmation_matches,
        },
        "evidence": {
            "rollback_snapshot": str(rollback_snapshot.relative_to(root)),
            "operation_record": str(operation_record.relative_to(root)),
            "post_apply_verification_required": True,
        },
        "mutations": {
            "target_file_written": True,
            "rollback_snapshot_written": True,
            "operation_record_written": True,
            "database_mutated": False,
            "importer_mutated": False,
            "proposal_state_mutated": False,
        },
        "boundaries": {
            "single_target_only": True,
            "trusted_wiki_mutation_human_approved": True,
            "autonomous_apply": False,
            "importer_refresh_required_separately": True,
        },
    }


def render_apply_markdown(result: dict[str, Any]) -> str:
    target = result.get("target", {})
    mutations = result.get("mutations", {})
    evidence = result.get("evidence", {})
    lines = [
        "## Human-approved Controlled Promotion Apply",
        "",
        f"Status: {result.get('status')}",
        f"Mode: {result.get('mode')}",
        f"Project: {result.get('project')}",
        f"Proposal ID: {result.get('proposal_id')}",
        f"Target path: {target.get('path')}",
        "",
        "### Hash evidence",
        "",
        f"- Pre-apply SHA256: {target.get('pre_apply_sha256')}",
        f"- Expected pre-hash matches: {target.get('expected_pre_hash_matches')}",
        f"- Post-apply SHA256: {target.get('post_apply_sha256')}",
        "",
        "### Write evidence",
        "",
        f"- Target file written: {mutations.get('target_file_written')}",
        f"- Rollback snapshot written: {mutations.get('rollback_snapshot_written')}",
        f"- Operation record written: {mutations.get('operation_record_written')}",
        f"- Rollback snapshot: {evidence.get('rollback_snapshot')}",
        f"- Operation record: {evidence.get('operation_record')}",
        "",
        "### Boundary",
        "",
        f"- Database mutated: {mutations.get('database_mutated')}",
        f"- Importer mutated: {mutations.get('importer_mutated')}",
        f"- Proposal state mutated: {mutations.get('proposal_state_mutated')}",
        "",
    ]
    if result.get("hard_errors"):
        lines.extend(["### Blocking errors", ""])
        lines.extend(f"- {item}" for item in result["hard_errors"])
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Human-approved controlled promotion apply MVP.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--heading", required=True)
    parser.add_argument("--insert-text", required=True)
    parser.add_argument("--expected-pre-hash", required=True)
    parser.add_argument("--human-confirmation", required=True)
    parser.add_argument("--reason")
    parser.add_argument("--actor", default="human")
    parser.add_argument("--apply", action="store_true", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    payload = build_apply_result(
        root=root,
        project=args.project,
        proposal_id=args.proposal_id,
        target_path=args.target_path,
        heading=args.heading,
        insert_text=args.insert_text,
        expected_pre_hash=args.expected_pre_hash,
        human_confirmation=args.human_confirmation,
        reason=args.reason,
        apply=args.apply,
        actor=args.actor,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_apply_markdown(payload))
    else:
        print(render_apply_markdown(payload))
    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
