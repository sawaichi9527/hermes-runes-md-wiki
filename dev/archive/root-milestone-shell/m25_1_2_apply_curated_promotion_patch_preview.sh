#!/usr/bin/env bash
set -euo pipefail
cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cat > wiki/k6-freelancer/verification-m25-curated-promotion-preview.md <<'MD'
# M25 Curated Promotion Patch Preview Verification

Status: DESIGN LOCK / DRY-RUN CLI BASELINE
Milestone: M25 Curated Promotion Patch Preview / Dry-run
Chinese: M25 精選升格補丁預覽 / 乾跑

## Purpose

M25 defines a preview-only curated promotion patch layer.

It lets Hermes-agent recommend how an attuned proposal could be promoted into trusted Markdown wiki content, without granting autonomous write authority.

## Core Principle

Forge suggestion, not forge execution.

- proposal is not trusted memory
- patch preview is not wiki mutation
- forge preview is not promotion execution
- human review is required before any future apply

## M25.1 Design Scope

M25.1 defines:

- curated promotion terminology
- candidate Markdown diff semantics
- single-target patch preview philosophy
- promotion evidence vs trusted memory distinction
- preview-only / no-mutation boundary

## M25.2 CLI Baseline

M25.2 introduces:

```text
runes promotion preview --proposal-id '<proposal_id>' --target-path '<path>' --heading '<heading>' --insert-text '<markdown>' --dry-run --json
```

Supported previews:

- terminal-readable preview
- Markdown diff preview
- JSON preview

## Locked Boundaries

- promotion execution: not implemented
- trusted wiki mutation: forbidden
- proposal state mutation: forbidden
- database mutation: forbidden
- importer mutation: forbidden
- autonomous promotion execution: forbidden
- autonomous trusted-memory mutation: forbidden

## Verification Status

M25.1 Curated Promotion Patch Design Lock: PASS

M25.2 Promotion Patch Dry-run CLI: PASS

Overall:

M25 Curated Promotion Patch Preview / Dry-run:
DESIGN LOCK / DRY-RUN CLI BASELINE
MD

cat > tools/runes/promotion_patch_m25_2.py <<'PY'
#!/usr/bin/env python3
# M25.2 curated promotion patch dry-run helper.

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m25.2.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"


def parse_heading(line: str) -> tuple[int, str] | None:
    stripped = line.strip()
    if not stripped.startswith("#"):
        return None
    level = len(stripped) - len(stripped.lstrip("#"))
    return level, stripped[level:].strip()


def find_heading(lines: list[str], heading: str) -> tuple[int, int] | None:
    wanted = heading.strip().lower()
    for idx, line in enumerate(lines):
        parsed = parse_heading(line)
        if parsed and parsed[1].lower() == wanted:
            return idx, parsed[0]
    return None


def section_end(lines: list[str], start: int, level: int) -> int:
    for idx in range(start + 1, len(lines)):
        parsed = parse_heading(lines[idx])
        if parsed and parsed[0] <= level:
            return idx
    return len(lines)


def as_lines(text: str) -> list[str]:
    out = [line.rstrip() + "\n" for line in text.splitlines()]
    if out and out[-1].strip():
        out.append("\n")
    return out


def candidate_lines(original: list[str], heading: str, insert_text: str) -> tuple[list[str], dict[str, Any]]:
    found = find_heading(original, heading)
    add = as_lines(insert_text)
    if found:
        start, level = found
        end = section_end(original, start, level)
        spacer = [] if end > 0 and original[end - 1].strip() == "" else ["\n"]
        return original[:end] + spacer + add + original[end:], {
            "target_heading_found": True,
            "operation": "append_to_existing_heading",
            "heading_start_line": start + 1,
            "insertion_line": end + 1,
        }

    new_section = ["\n", f"## {heading}\n", "\n"] + add
    return original + new_section, {
        "target_heading_found": False,
        "operation": "append_new_heading_at_end",
        "heading_start_line": None,
        "insertion_line": len(original) + 1,
    }


def build_promotion_patch_preview(
    root: Path,
    project: str,
    proposal_id: str,
    target_path: str,
    heading: str,
    insert_text: str,
    reason: str | None = None,
) -> dict[str, Any]:
    rel = Path(target_path)
    abs_path = (root / rel).resolve()
    abs_path.relative_to(root.resolve())

    original = abs_path.read_text(encoding="utf-8").splitlines(keepends=True) if abs_path.exists() else []
    candidate, meta = candidate_lines(original, heading, insert_text)
    diff = "\n".join(difflib.unified_diff(original, candidate, fromfile=f"a/{target_path}", tofile=f"b/{target_path}", lineterm=""))

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M25.2 Curated promotion patch dry-run",
        "status": "PASS",
        "mode": "dry_run_only",
        "project": project,
        "proposal_id": proposal_id,
        "target": {"path": target_path, "exists": abs_path.exists(), "heading": heading, **meta},
        "reason": reason,
        "unified_diff": diff,
        "promotion": {
            "curated_promotion": True,
            "forge_suggestion": True,
            "promotion_execution_implemented": False,
            "trusted_wiki_mutation_allowed": False,
        },
        "preview": {
            "would_write_target_file": False,
            "would_update_proposal_state": False,
            "would_promote_to_wiki": False,
            "would_mutate_database": False,
            "would_run_importer": False,
            "human_review_required_for_future_apply": True,
        },
        "mutations": {
            "target_file_written": False,
            "proposal_state_mutated": False,
            "trusted_memory_created": False,
            "curated_wiki_mutated": False,
            "database_mutated": False,
            "importer_mutated": False,
            "files_written": False,
        },
    }


def render_patch_markdown_preview(result: dict[str, Any]) -> str:
    target = result["target"]
    preview = result["preview"]
    mutations = result["mutations"]
    return "\n".join([
        "## Curated Promotion Patch Preview",
        "",
        f"Status: {result['status']}",
        f"Mode: {result['mode']}",
        f"Project: {result['project']}",
        f"Proposal ID: {result['proposal_id']}",
        f"Target path: {target['path']}",
        f"Target heading: {target['heading']}",
        "",
        "### Meaning",
        "",
        "- This is a forge suggestion, not forge execution.",
        "- Patch preview is not trusted wiki mutation.",
        "- Human review is required before any future apply.",
        "",
        "### Unified diff",
        "",
        "```diff",
        result.get("unified_diff") or "",
        "```",
        "",
        "### Boundary",
        "",
        f"- Would write target file now: {preview['would_write_target_file']}",
        f"- Would promote to wiki now: {preview['would_promote_to_wiki']}",
        f"- Target file written now: {mutations['target_file_written']}",
        f"- Trusted wiki mutation now: {mutations['curated_wiki_mutated']}",
        f"- Database mutation now: {mutations['database_mutated']}",
        f"- Importer mutation now: {mutations['importer_mutated']}",
        "",
        "This is a Markdown preview only. M25.2 does not apply the patch.",
        "",
    ])


def print_patch_preview(result: dict[str, Any]) -> None:
    print("Curated Promotion Patch Preview")
    print("===============================")
    print(render_patch_markdown_preview(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Curated promotion patch dry-run helper.")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--heading", required=True)
    parser.add_argument("--insert-text", required=True)
    parser.add_argument("--reason")
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    result = build_promotion_patch_preview(root, args.project, args.proposal_id, args.target_path, args.heading, args.insert_text, args.reason)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.markdown:
        print(render_patch_markdown_preview(result))
    else:
        print_patch_preview(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
PY

python3 - <<'PY'
from pathlib import Path
p = Path("tools/runes/runes.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "from attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview, render_trail_markdown_preview\n",
    "from attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview, render_trail_markdown_preview\n"
    "    from promotion_patch_m25_2 import build_promotion_patch_preview, print_patch_preview, render_patch_markdown_preview\n",
)
s = s.replace(
    "from tools.runes.attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview, render_trail_markdown_preview\n",
    "from tools.runes.attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview, render_trail_markdown_preview\n"
    "    from tools.runes.promotion_patch_m25_2 import build_promotion_patch_preview, print_patch_preview, render_patch_markdown_preview\n",
)

if '"promotion_patch_dry_run",' not in s:
    s = s.replace('                "attunement_trail_dry_run",\n', '                "attunement_trail_dry_run",\n                "promotion_patch_dry_run",\n')

if '"implemented_in_m25_2"' not in s:
    s = s.replace('            "implemented_in_m24_3": ["attunement_trail_markdown_preview"],\n', '            "implemented_in_m24_3": ["attunement_trail_markdown_preview"],\n            "implemented_in_m25_2": ["promotion_patch_dry_run"],\n')

if '"promotion_preview"' not in s:
    s = s.replace(
        '                {"name": "attunement_trail", "command": "runes trail attunement --action attune --id \'<proposal_id>\' --dry-run --json|--markdown", "write": False, "p0_status": "m24_2_dry_run_implemented"},\n',
        '                {"name": "attunement_trail", "command": "runes trail attunement --action attune --id \'<proposal_id>\' --dry-run --json|--markdown", "write": False, "p0_status": "m24_2_dry_run_implemented"},\n'
        '                {"name": "promotion_preview", "command": "runes promotion preview --proposal-id \'<proposal_id>\' --target-path wiki/k6-freelancer/services.md --heading \'<heading>\' --insert-text \'<markdown>\' --dry-run --json|--markdown", "write": False, "p0_status": "m25_2_dry_run_implemented"},\n',
    )

if "M25.2 adds curated promotion patch dry-run previews." not in s:
    s = s.replace('                "M24.3 adds Markdown trail event previews.",\n', '                "M24.3 adds Markdown trail event previews.",\n                "M25.2 adds curated promotion patch dry-run previews.",\n')

if 'promotion = subparsers.add_parser("promotion")' not in s:
    marker = '    trail = subparsers.add_parser("trail")\n'
    block = """    promotion = subparsers.add_parser("promotion")
    promotion_sub = promotion.add_subparsers(dest="promotion_command", required=True)
    promotion_preview = promotion_sub.add_parser("preview")
    promotion_preview.add_argument("--project", default="k6-freelancer")
    promotion_preview.add_argument("--proposal-id", required=True)
    promotion_preview.add_argument("--target-path", required=True)
    promotion_preview.add_argument("--heading", required=True)
    promotion_preview.add_argument("--insert-text", required=True)
    promotion_preview.add_argument("--reason")
    promotion_preview.add_argument("--dry-run", action="store_true", required=True)
    promotion_preview.add_argument("--json", action="store_true")
    promotion_preview.add_argument("--markdown", action="store_true")

"""
    s = s.replace(marker, block + marker)

if 'if args.command == "promotion":' not in s:
    marker = '    if args.command == "trail":\n'
    block = """    if args.command == "promotion":
        if args.promotion_command == "preview":
            payload = build_promotion_patch_preview(
                root=root,
                project=args.project,
                proposal_id=args.proposal_id,
                target_path=args.target_path,
                heading=args.heading,
                insert_text=args.insert_text,
                reason=args.reason,
            )
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            elif args.markdown:
                print(render_patch_markdown_preview(payload))
            else:
                print_patch_preview(payload)
            return 0 if payload.get("status") == "PASS" else 2

"""
    s = s.replace(marker, block + marker)

p.write_text(s, encoding="utf-8")
PY

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M25 Curated Promotion Patch Preview / Dry-run

Status: DESIGN LOCK / DRY-RUN CLI BASELINE

Verification record:

- `wiki/k6-freelancer/verification-m25-curated-promotion-preview.md`

Goal:

Define and implement a preview-only curated promotion patch model that lets Hermes-agent recommend Markdown wiki changes without mutating trusted memory.

Completed milestones:

- M25.1 Curated Promotion Patch Design Lock: PASS
- M25.2 Promotion Patch Dry-run CLI: PASS

Locked boundaries:

- proposal is not trusted memory
- patch preview is not wiki mutation
- forge preview is not promotion execution
- no trusted wiki mutation
- no proposal state mutation
- no database mutation
- no importer mutation
- no autonomous promotion execution

Next:

- M25.3 Promotion patch smoke test

MD

python3 -m py_compile tools/runes/promotion_patch_m25_2.py tools/runes/runes.py

bin/runes promotion preview \
  --proposal-id "nonexistent-proposal" \
  --target-path "wiki/k6-freelancer/services.md" \
  --heading "Telegram Integration" \
  --insert-text "- M25 curated promotion patch preview smoke." \
  --reason "M25.2 smoke dry-run" \
  --dry-run

bin/runes promotion preview \
  --proposal-id "nonexistent-proposal" \
  --target-path "wiki/k6-freelancer/services.md" \
  --heading "Telegram Integration" \
  --insert-text "- M25 curated promotion patch preview smoke." \
  --reason "M25.2 smoke dry-run" \
  --dry-run \
  --markdown | grep -n "Curated Promotion Patch Preview\\|forge suggestion\\|M25.2 does not apply"

bin/runes promotion preview \
  --proposal-id "nonexistent-proposal" \
  --target-path "wiki/k6-freelancer/services.md" \
  --heading "Telegram Integration" \
  --insert-text "- M25 curated promotion patch preview smoke." \
  --reason "M25.2 smoke dry-run" \
  --dry-run \
  --json | grep -n "M25.2 Curated promotion patch dry-run\\|target_file_written\\|database_mutated\\|promotion_execution_implemented"

git add tools/runes/promotion_patch_m25_2.py tools/runes/runes.py wiki/k6-freelancer/verification-m25-curated-promotion-preview.md wiki/k6-freelancer/roadmap.md
git diff --cached
git commit -m "Add M25 curated promotion patch dry-run baseline"
git push origin main
git log --oneline -3
