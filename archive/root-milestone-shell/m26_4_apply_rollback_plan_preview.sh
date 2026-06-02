#!/usr/bin/env bash
set -euo pipefail
cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cat > tools/runes/promotion_rollback_plan_m26_4.py <<'PY'
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
PY

python3 - <<'PY'
from pathlib import Path
p = Path("tools/runes/runes.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "from promotion_apply_preflight_m26_2 import build_apply_preflight, print_preflight, render_preflight_markdown\n",
    "from promotion_apply_preflight_m26_2 import build_apply_preflight, print_preflight, render_preflight_markdown\n"
    "    from promotion_rollback_plan_m26_4 import build_rollback_plan_preview, print_rollback_preview, render_rollback_markdown\n",
)
s = s.replace(
    "from tools.runes.promotion_apply_preflight_m26_2 import build_apply_preflight, print_preflight, render_preflight_markdown\n",
    "from tools.runes.promotion_apply_preflight_m26_2 import build_apply_preflight, print_preflight, render_preflight_markdown\n"
    "    from tools.runes.promotion_rollback_plan_m26_4 import build_rollback_plan_preview, print_rollback_preview, render_rollback_markdown\n",
)

if '"promotion_rollback_plan",' not in s:
    s = s.replace(
        '                "promotion_apply_preflight",\n',
        '                "promotion_apply_preflight",\n                "promotion_rollback_plan",\n',
    )

if '"implemented_in_m26_4"' not in s:
    s = s.replace(
        '            "implemented_in_m26_2": ["promotion_apply_preflight"],\n',
        '            "implemented_in_m26_2": ["promotion_apply_preflight"],\n            "implemented_in_m26_4": ["promotion_rollback_plan"],\n',
    )

if '"promotion_rollback_plan"' not in s:
    s = s.replace(
        '                {"name": "promotion_apply_preflight", "command": "runes promotion preflight --proposal-id \'<proposal_id>\' --target-path wiki/k6-freelancer/services.md --heading \'<heading>\' --insert-text \'<markdown>\' --dry-run --json|--markdown", "write": False, "p0_status": "m26_2_dry_run_implemented"},\n',
        '                {"name": "promotion_apply_preflight", "command": "runes promotion preflight --proposal-id \'<proposal_id>\' --target-path wiki/k6-freelancer/services.md --heading \'<heading>\' --insert-text \'<markdown>\' --dry-run --json|--markdown", "write": False, "p0_status": "m26_2_dry_run_implemented"},\n'
        '                {"name": "promotion_rollback_plan", "command": "runes promotion rollback-plan --proposal-id \'<proposal_id>\' --target-path wiki/k6-freelancer/services.md --heading \'<heading>\' --insert-text \'<markdown>\' --dry-run --json|--markdown", "write": False, "p0_status": "m26_4_dry_run_implemented"},\n',
    )

if "M26.4 adds rollback plan preview dry-run." not in s:
    s = s.replace(
        '                "M26.2 adds human-approved promotion apply preflight dry-run.",\n',
        '                "M26.2 adds human-approved promotion apply preflight dry-run.",\n                "M26.4 adds rollback plan preview dry-run.",\n',
    )

if 'promotion_rollback = promotion_sub.add_parser("rollback-plan")' not in s:
    marker = '    promotion_preflight.add_argument("--markdown", action="store_true")\n'
    block = (
        '\n'
        '    promotion_rollback = promotion_sub.add_parser("rollback-plan")\n'
        '    promotion_rollback.add_argument("--project", default="k6-freelancer")\n'
        '    promotion_rollback.add_argument("--proposal-id", required=True)\n'
        '    promotion_rollback.add_argument("--target-path", required=True)\n'
        '    promotion_rollback.add_argument("--heading", required=True)\n'
        '    promotion_rollback.add_argument("--insert-text", required=True)\n'
        '    promotion_rollback.add_argument("--expected-pre-hash")\n'
        '    promotion_rollback.add_argument("--human-confirmation")\n'
        '    promotion_rollback.add_argument("--reason")\n'
        '    promotion_rollback.add_argument("--dry-run", action="store_true", required=True)\n'
        '    promotion_rollback.add_argument("--json", action="store_true")\n'
        '    promotion_rollback.add_argument("--markdown", action="store_true")\n'
    )
    s = s.replace(marker, marker + block)

if 'if args.promotion_command == "rollback-plan":' not in s:
    marker = '        if args.promotion_command == "preflight":\n'
    block = (
        '        if args.promotion_command == "rollback-plan":\n'
        '            payload = build_rollback_plan_preview(\n'
        '                root=root,\n'
        '                project=args.project,\n'
        '                proposal_id=args.proposal_id,\n'
        '                target_path=args.target_path,\n'
        '                heading=args.heading,\n'
        '                insert_text=args.insert_text,\n'
        '                expected_pre_hash=args.expected_pre_hash,\n'
        '                human_confirmation=args.human_confirmation,\n'
        '                reason=args.reason,\n'
        '            )\n'
        '            if args.json:\n'
        '                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))\n'
        '            elif args.markdown:\n'
        '                print(render_rollback_markdown(payload))\n'
        '            else:\n'
        '                print_rollback_preview(payload)\n'
        '            return 0 if payload.get("status") == "PASS" else 2\n'
        '\n'
    )
    s = s.replace(marker, block + marker)

p.write_text(s, encoding="utf-8")
PY

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M26.4 Rollback Plan Preview

Status: PASS / ROLLBACK PREVIEW BASELINE

Verification target:

- `tools/runes/promotion_rollback_plan_m26_4.py`

CLI:

```text
runes promotion rollback-plan \
  --proposal-id '<proposal_id>' \
  --target-path '<wiki/path.md>' \
  --heading '<heading>' \
  --insert-text '<markdown>' \
  --dry-run
```

Scope:

- render rollback strategy preview
- expose pre-apply hash evidence
- expose candidate evidence hash
- expose ordered rollback steps
- expose operation record preview
- preserve target Markdown hash
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no operation record write
- no rollback snapshot write
- no rollback apply

Boundary:

M26.4 is still rollback plan preview only. It does not write snapshots or apply rollback.

Next:

- M26.5 M26 roadmap / verification lock

MD

python3 -m py_compile \
  tools/runes/promotion_patch_m25_2.py \
  tools/runes/promotion_apply_preflight_m26_2.py \
  tools/runes/promotion_rollback_plan_m26_4.py \
  tools/runes/smoke_m26_3_apply_preflight.py \
  tools/runes/runes.py

python3 tools/runes/promotion_rollback_plan_m26_4.py \
  --proposal-id "m26-4-rollback-smoke" \
  --target-path "wiki/k6-freelancer/services.md" \
  --heading "Telegram Integration" \
  --insert-text "- M26.4 rollback plan dry-run smoke." \
  --reason "M26.4 smoke dry-run" \
  --dry-run

bin/runes promotion rollback-plan \
  --proposal-id "m26-4-rollback-smoke" \
  --target-path "wiki/k6-freelancer/services.md" \
  --heading "Telegram Integration" \
  --insert-text "- M26.4 rollback plan dry-run smoke." \
  --reason "M26.4 smoke dry-run" \
  --dry-run \
  --markdown | grep -n "Promotion Rollback Plan Preview\\|Rollback steps\\|M26.4 does not write snapshots"

bin/runes promotion rollback-plan \
  --proposal-id "m26-4-rollback-smoke" \
  --target-path "wiki/k6-freelancer/services.md" \
  --heading "Telegram Integration" \
  --insert-text "- M26.4 rollback plan dry-run smoke." \
  --reason "M26.4 smoke dry-run" \
  --dry-run \
  --json | grep -n "M26.4 Promotion rollback plan preview\\|rollback_snapshot_written\\|rollback_applied\\|database_mutated"

git add \
  tools/runes/promotion_rollback_plan_m26_4.py \
  tools/runes/runes.py \
  wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Add M26.4 rollback plan preview"

git push origin main

git log --oneline -5
