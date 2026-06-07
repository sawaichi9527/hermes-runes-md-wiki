#!/usr/bin/env bash
set -euo pipefail
cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

python3 - <<'PY'
from pathlib import Path

p = Path("tools/runes/promotion_apply_preflight_m26_2.py")
s = p.read_text(encoding="utf-8")

start = s.index("def build_apply_preflight(")
end = s.index("\ndef render_preflight_markdown", start)

new_func = '''def build_apply_preflight(
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

    current_hash = sha256_file(abs_path) if path_ok else None

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

    if status == "PASS":
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
        patch_preview_payload = {
            "status": patch_preview.get("status"),
            "mode": patch_preview.get("mode"),
            "unified_diff": patch_preview.get("unified_diff"),
            "candidate_evidence_hash": candidate_evidence_hash,
        }
    else:
        patch_preview_payload = {
            "status": "SKIPPED",
            "mode": "dry_run_only",
            "unified_diff": "",
            "candidate_evidence_hash": None,
            "skipped_reason": "preflight blocked before patch preview generation",
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M26.2 Human-approved promotion apply preflight dry-run",
        "status": status,
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "target": {
            "path": target_path,
            "exists": abs_path.exists() if path_ok else False,
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
        "patch_preview": patch_preview_payload,
        "rollback_plan": {
            "rollback_available_later": bool(path_ok),
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
'''

p.write_text(s[:start] + new_func + s[end:], encoding="utf-8")
PY

python3 -m py_compile \
  tools/runes/promotion_apply_preflight_m26_2.py \
  tools/runes/smoke_m26_3_apply_preflight.py \
  tools/runes/runes.py

python3 tools/runes/smoke_m26_3_apply_preflight.py

git add \
  tools/runes/promotion_apply_preflight_m26_2.py \
  tools/runes/smoke_m26_3_apply_preflight.py \
  wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Fix M26.2 preflight blocking before patch preview"

git push origin main

git log --oneline -5
