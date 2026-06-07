#!/usr/bin/env bash
set -euo pipefail

cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

python3 - <<'PY'
from pathlib import Path

p = Path("tools/runes/attunement_trail_m24_2.py")
s = p.read_text(encoding="utf-8")

if "def render_trail_markdown_preview" not in s:
    insert = '''
def render_trail_markdown_preview(result: dict[str, Any]) -> str:
    event = result.get("event_preview") or {}
    mutations = result.get("mutations") or {}
    preview = result.get("preview") or {}

    lines = [
        "## Runes Attunement Trail Event Preview",
        "",
        f"Status: {result.get('status')}",
        f"Mode: {result.get('mode')}",
        f"Project: {result.get('project')}",
        f"Proposal ID: {result.get('proposal_id')}",
        f"Action: {result.get('action')}",
        "",
        "### Event",
        "",
        f"- Event ID: {event.get('event_id')}",
        f"- Event type: {event.get('event_type')}",
        f"- Old state: {event.get('old_state')}",
        f"- New state: {event.get('new_state')}",
        f"- Actor: {event.get('actor')}",
        f"- Decision reason: {event.get('decision_reason')}",
        f"- Timestamp: {event.get('timestamp')}",
        f"- Dry-run: {event.get('dry_run')}",
        "",
        "### Boundary",
        "",
        "- Trail is governance evidence, not trusted wiki memory.",
        f"- Would write trail file now: {preview.get('would_write_trail_file', False)}",
        f"- Would append event later: {preview.get('would_append_event_later', False)}",
        f"- Proposal state mutation now: {mutations.get('proposal_state_mutated', False)}",
        f"- Trusted wiki mutation now: {mutations.get('curated_wiki_mutated', False)}",
        f"- Trusted memory created now: {mutations.get('trusted_memory_created', False)}",
        f"- Database mutation now: {mutations.get('database_mutated', False)}",
        f"- Importer mutation now: {mutations.get('importer_mutated', False)}",
        f"- Files written now: {mutations.get('files_written', False)}",
        "",
        "### Current scope",
        "",
        "This is a Markdown preview only. M24.3 does not write an append-only trail file.",
        "",
    ]

    superseded_by = event.get("superseded_by")
    if superseded_by:
        lines.insert(16, f"- Superseded by: {superseded_by}")

    return "\n".join(lines)
'''
    s = s.replace("\ndef print_trail_preview(result: dict[str, Any]) -> None:\n", insert + "\ndef print_trail_preview(result: dict[str, Any]) -> None:\n")

if '--markdown' not in s:
    s = s.replace(
        '    parser.add_argument("--json", action="store_true")\n',
        '    parser.add_argument("--json", action="store_true")\n    parser.add_argument("--markdown", action="store_true")\n',
        1,
    )

if "elif args.markdown" not in s:
    s = s.replace(
        '    if args.json:\n        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))\n    else:\n        print_trail_preview(result)\n',
        '    if args.json:\n        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))\n    elif args.markdown:\n        print(render_trail_markdown_preview(result))\n    else:\n        print_trail_preview(result)\n',
    )

p.write_text(s, encoding="utf-8")
PY

python3 - <<'PY'
from pathlib import Path

p = Path("tools/runes/runes.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "from attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview\n",
    "from attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview, render_trail_markdown_preview\n",
)
s = s.replace(
    "from tools.runes.attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview\n",
    "from tools.runes.attunement_trail_m24_2 import build_attunement_trail_dry_run, print_trail_preview, render_trail_markdown_preview\n",
)

if '"implemented_in_m24_3"' not in s:
    s = s.replace(
        '            "implemented_in_m24_2": ["attunement_trail_dry_run"],\n',
        '            "implemented_in_m24_2": ["attunement_trail_dry_run"],\n'
        '            "implemented_in_m24_3": ["attunement_trail_markdown_preview"],\n',
    )

s = s.replace(
    '"runes trail attunement --action attune --id \'<proposal_id>\' --dry-run --json"',
    '"runes trail attunement --action attune --id \'<proposal_id>\' --dry-run --json|--markdown"',
)

if "M24.3 adds Markdown trail event previews." not in s:
    s = s.replace(
        '                "M24.2 adds Runes Attunement trail dry-run previews.",\n',
        '                "M24.2 adds Runes Attunement trail dry-run previews.",\n'
        '                "M24.3 adds Markdown trail event previews.",\n',
    )

if 'attunement_trail.add_argument("--markdown", action="store_true")' not in s:
    s = s.replace(
        '    attunement_trail.add_argument("--json", action="store_true")\n',
        '    attunement_trail.add_argument("--json", action="store_true")\n    attunement_trail.add_argument("--markdown", action="store_true")\n',
    )

if "elif args.markdown:" not in s:
    s = s.replace(
        '            if args.json:\n                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))\n            else:\n                print_trail_preview(payload)\n',
        '            if args.json:\n                print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))\n            elif args.markdown:\n                print(render_trail_markdown_preview(payload))\n            else:\n                print_trail_preview(payload)\n',
    )

p.write_text(s, encoding="utf-8")
PY

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M24.3 Attunement Trail Markdown Preview

Status: PASS / PREVIEW-ONLY

Scope:

- Add Markdown rendering for attunement trail event previews.
- Keep JSON and terminal-readable previews intact.
- Preserve dry-run-only behavior.
- Do not write append-only trail files yet.

Boundary:

- no trail file write
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no promotion execution

Current milestone:

- M24.3 Attunement Trail Markdown Preview: PASS / preview-only

Next:

- M24.4 Attunement trail smoke test

MD

python3 -m py_compile   tools/runes/attunement_trail_m24_2.py   tools/runes/runes.py

bin/runes trail attunement   --action attune   --id "nonexistent-proposal"   --reason "M24.3 markdown preview smoke"   --dry-run   --markdown

bin/runes trail attunement   --action attune   --id "nonexistent-proposal"   --reason "M24.3 markdown preview smoke"   --dry-run   --json | grep -n "M24.2 Runes Attunement trail dry-run\|trail_file_written\|database_mutated"

git add   tools/runes/attunement_trail_m24_2.py   tools/runes/runes.py   wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Add M24.3 attunement trail Markdown preview"

git push origin main

git log --oneline -3
