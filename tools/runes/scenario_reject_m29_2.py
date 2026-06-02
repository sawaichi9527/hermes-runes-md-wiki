#!/usr/bin/env python3
# M29.2 P0 pre-trial reject / no-promotion scenario helper.

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from promotion_apply_preflight_m26_2 import sha256_file
    from recall_verify_m28_3 import build_recall_verification
except ImportError:  # pragma: no cover
    from tools.runes.promotion_apply_preflight_m26_2 import sha256_file
    from tools.runes.recall_verify_m28_3 import build_recall_verification

SCHEMA_VERSION = "m29.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
DEFAULT_TARGET_PATH = "wiki/k6-freelancer/p0-trial-scenarios.md"
DEFAULT_PROPOSAL_ID = "m29-2-reject-no-promotion-scenario"
DEFAULT_REJECTED_MARKER = "M29.2_REJECTED_KNOWLEDGE_SHOULD_NOT_APPEAR_IN_TRUSTED_RECALL"

REJECTED_KNOWLEDGE = f"""\
Rejected scenario content marker: {DEFAULT_REJECTED_MARKER}

This content is intentionally rejected for M29.2 and must not be promoted into trusted Markdown memory.
"""


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def find_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def write_reject_record(
    *,
    root: Path,
    project: str,
    proposal_id: str,
    actor: str,
    target_path: str,
    rejected_marker: str,
    reason: str,
    pre_hash: str | None,
    post_hash: str | None,
) -> str:
    stamp = utc_stamp()
    out_dir = root / "operations" / "runes-reject" / stamp[:8]
    out_dir.mkdir(parents=True, exist_ok=True)
    record_path = out_dir / f"{stamp}-{safe_slug(proposal_id)}.json"
    record = {
        "schema_version": SCHEMA_VERSION,
        "operation": "scenario.reject.no_promotion",
        "status": "PASS",
        "timestamp_utc": stamp,
        "project": project,
        "proposal_id": proposal_id,
        "actor": actor,
        "decision": "REJECT",
        "reason": reason,
        "target_path": target_path,
        "target_pre_sha256": pre_hash,
        "target_post_sha256": post_hash,
        "target_hash_unchanged": pre_hash == post_hash,
        "rejected_marker_sha256": sha256_text(rejected_marker),
        "rejected_content_sha256": sha256_text(REJECTED_KNOWLEDGE),
        "trusted_wiki_mutated": False,
        "controlled_apply_executed": False,
        "importer_refresh_executed": False,
        "proposal_state_mutated": False,
        "attunement_state_mutated": False,
        "promotion_state_mutated": False,
        "post_reject_recall_verification_required": True,
    }
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(record_path.relative_to(root))


def run_reject_scenario(
    *,
    root: Path,
    project: str,
    proposal_id: str,
    target_path: str,
    rejected_marker: str,
    actor: str,
    reason: str,
    verify_recall: bool,
    write_records: bool,
) -> dict[str, Any]:
    target_abs = root / target_path
    pre_hash = sha256_file(target_abs)

    operation_record: str | None = None
    post_hash = sha256_file(target_abs)
    if write_records:
        operation_record = write_reject_record(
            root=root,
            project=project,
            proposal_id=proposal_id,
            actor=actor,
            target_path=target_path,
            rejected_marker=rejected_marker,
            reason=reason,
            pre_hash=pre_hash,
            post_hash=post_hash,
        )

    recall_result: dict[str, Any] | None = None
    if verify_recall:
        recall_result = build_recall_verification(
            root=root,
            project=project,
            query=rejected_marker,
            expected_path=target_path,
            required_marker=rejected_marker,
            heading=None,
            limit=5,
            write_record=write_records,
        )

    post_verify_hash = sha256_file(target_abs)
    target_hash_unchanged = pre_hash == post_verify_hash
    recall_negative_ok = recall_result is not None and recall_result.get("status") == "FAIL" and not bool(
        recall_result.get("checks", {}).get("required_marker_found")
    )
    no_results_ok = recall_result is not None and not bool(recall_result.get("checks", {}).get("result_count_positive"))

    checks = {
        "target_hash_unchanged": target_hash_unchanged,
        "reject_record_written": operation_record is not None if write_records else True,
        "controlled_apply_not_executed": True,
        "refresh_not_executed": True,
        "trusted_wiki_not_mutated": target_hash_unchanged,
        "rejected_marker_not_found_in_trusted_recall": recall_negative_ok,
        "trusted_recall_result_count_zero": no_results_ok,
    }

    status = "PASS" if all(checks.values()) else "FAIL"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M29.2 P0 reject / no-promotion scenario",
        "status": status,
        "project": project,
        "proposal_id": proposal_id,
        "target_path": target_path,
        "rejected_marker": rejected_marker,
        "decision": "REJECT",
        "reason": reason,
        "checks": checks,
        "evidence": {
            "operation_record": operation_record,
            "target_pre_sha256": pre_hash,
            "target_post_sha256": post_verify_hash,
            "rejected_marker_sha256": sha256_text(rejected_marker),
            "rejected_content_sha256": sha256_text(REJECTED_KNOWLEDGE),
        },
        "recall": recall_result,
        "mutations": {
            "trusted_wiki_mutated": False,
            "controlled_apply_executed": False,
            "importer_refresh_executed": False,
            "proposal_state_mutated": False,
            "attunement_state_mutated": False,
            "promotion_state_mutated": False,
            "operation_record_written": operation_record is not None,
        },
        "boundaries": {
            "rejected_content_not_written_to_wiki": True,
            "rejected_content_not_refreshed_into_db": True,
            "negative_recall_expected": True,
            "trusted_recall_must_not_find_rejected_marker": True,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M29.2 reject / no-promotion P0 scenario runner.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--proposal-id", default=DEFAULT_PROPOSAL_ID)
    parser.add_argument("--target-path", default=DEFAULT_TARGET_PATH)
    parser.add_argument("--rejected-marker", default=DEFAULT_REJECTED_MARKER)
    parser.add_argument("--actor", default="human")
    parser.add_argument("--reason", default="M29.2 rejected content must not become trusted memory")
    parser.add_argument("--verify-recall", action="store_true", required=True)
    parser.add_argument("--write-records", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = run_reject_scenario(
        root=find_repo_root(),
        project=args.project,
        proposal_id=args.proposal_id,
        target_path=args.target_path,
        rejected_marker=args.rejected_marker,
        actor=args.actor,
        reason=args.reason,
        verify_recall=args.verify_recall,
        write_records=args.write_records,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
