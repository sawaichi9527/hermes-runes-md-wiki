#!/usr/bin/env bash
set -euo pipefail

cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cat > tools/runes/smoke_m24_4_attunement_trail.py <<'PY'
#!/usr/bin/env python3
"""M24.4 Runes Attunement Trail smoke test.

Verifies:
- trail dry-run JSON payload
- terminal-readable preview renderer
- Markdown preview renderer
- no trail/proposal/wiki/database/importer mutation flags
"""

from __future__ import annotations

import json
from pathlib import Path

from attunement_trail_m24_2 import (
    build_attunement_trail_dry_run,
    print_trail_preview,
    render_trail_markdown_preview,
)


def check(condition: bool, name: str, details: dict | None = None) -> dict:
    return {
        "name": name,
        "status": "PASS" if condition else "FAIL",
        "details": details or {},
    }


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    project = "k6-freelancer"
    proposal_id = "nonexistent-proposal"

    cases = [
        ("attune", {}),
        ("reject", {}),
        ("supersede", {"superseded_by": "newer-nonexistent-proposal"}),
    ]

    results = []

    for action, extra in cases:
        payload = build_attunement_trail_dry_run(
            root=root,
            project=project,
            proposal_id=proposal_id,
            action=action,
            reason="M24.4 smoke dry-run",
            actor="human",
            superseded_by=extra.get("superseded_by"),
        )

        event = payload.get("event_preview", {})
        preview = payload.get("preview", {})
        mutations = payload.get("mutations", {})
        trail = payload.get("trail", {})
        markdown = render_trail_markdown_preview(payload)

        results.extend([
            check(payload.get("suite") == "M24.2 Runes Attunement trail dry-run", f"{action}: suite stable"),
            check(payload.get("mode") == "dry_run_only", f"{action}: dry_run_only"),
            check(payload.get("status") == "PASS", f"{action}: status PASS"),
            check(trail.get("append_only_design") is True, f"{action}: append-only design"),
            check(trail.get("trail_write_implemented") is False, f"{action}: trail write not implemented"),
            check(trail.get("trusted_memory") is False, f"{action}: trail is not trusted memory"),
            check(trail.get("governance_evidence") is True, f"{action}: trail is governance evidence"),
            check(event.get("dry_run") is True, f"{action}: event dry_run true"),
            check(event.get("promotion_executed") is False, f"{action}: promotion not executed"),
            check(event.get("database_mutated") is False, f"{action}: event no database mutation"),
            check(event.get("trusted_wiki_mutated") is False, f"{action}: event no trusted wiki mutation"),
            check(preview.get("would_write_trail_file") is False, f"{action}: no trail file write now"),
            check(preview.get("would_append_event_later") is True, f"{action}: append later preview"),
            check(preview.get("would_update_proposal_metadata") is False, f"{action}: no proposal metadata update"),
            check(preview.get("would_promote_to_wiki") is False, f"{action}: no wiki promotion"),
            check(mutations.get("trail_file_written") is False, f"{action}: mutation no trail file write"),
            check(mutations.get("proposal_state_mutated") is False, f"{action}: mutation no proposal state change"),
            check(mutations.get("trusted_memory_created") is False, f"{action}: mutation no trusted memory creation"),
            check(mutations.get("curated_wiki_mutated") is False, f"{action}: mutation no curated wiki change"),
            check(mutations.get("database_mutated") is False, f"{action}: mutation no database change"),
            check(mutations.get("importer_mutated") is False, f"{action}: mutation no importer change"),
            check(mutations.get("files_written") is False, f"{action}: mutation no files written"),
            check("Runes Attunement Trail Event Preview" in markdown, f"{action}: markdown heading"),
            check("This is a Markdown preview only" in markdown, f"{action}: markdown preview-only note"),
        ])

    payload = build_attunement_trail_dry_run(
        root=root,
        project=project,
        proposal_id=proposal_id,
        action="attune",
        reason="M24.4 smoke terminal render",
    )
    print_trail_preview(payload)
    results.append(check(True, "terminal renderer callable"))

    failed = [item for item in results if item["status"] != "PASS"]
    summary = {
        "suite": "M24.4 Runes Attunement Trail smoke test",
        "status": "PASS" if not failed else "FAIL",
        "failed": len(failed),
        "total": len(results),
        "results": results,
        "boundary": {
            "dry_run_only": True,
            "trail_file_write_allowed": False,
            "proposal_state_mutation_allowed": False,
            "trusted_wiki_mutation_allowed": False,
            "database_mutation_allowed": False,
            "promotion_execution_implemented": False,
        },
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
PY

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M24.4 Attunement Trail Smoke Test

Status: PASS / REGRESSION BASELINE

Scope:

- Verify trail dry-run JSON payload.
- Verify terminal-readable trail preview renderer.
- Verify Markdown trail preview renderer.
- Verify no trail/proposal/wiki/database/importer mutation boundary.

Boundary:

- no trail file write
- no proposal state mutation
- no trusted wiki mutation
- no database mutation
- no importer mutation
- no promotion execution

Current milestone:

- M24.4 Attunement Trail Smoke Test: PASS / regression baseline

Next:

- M24.5 Roadmap / verification lock

MD

python3 -m py_compile \
  tools/runes/attunement_trail_m24_2.py \
  tools/runes/smoke_m24_4_attunement_trail.py \
  tools/runes/runes.py

python3 tools/runes/smoke_m24_4_attunement_trail.py

bin/runes trail attunement \
  --action reject \
  --id "nonexistent-proposal" \
  --reason "M24.4 CLI smoke" \
  --dry-run \
  --markdown | grep -n "Runes Attunement Trail Event Preview\\|Markdown preview only\\|Database mutation now: False"

git add \
  tools/runes/smoke_m24_4_attunement_trail.py \
  wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Add M24.4 attunement trail smoke test"

git push origin main

git log --oneline -3
