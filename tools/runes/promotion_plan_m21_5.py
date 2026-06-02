#!/usr/bin/env python3
"""M21.5 human-only curated promotion plan / dry-run.

This script reads an approved proposal from the M21.4 sandbox trial workspace
and generates a dry-run promotion plan for a curated Markdown wiki note.

It does not write curated wiki files, mutate trusted memory, move proposal state,
run importer, or update PostgreSQL indexes.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m21.5.p0.v1"
DEFAULT_DOMAIN = "k6-freelancer"
DEFAULT_WORKSPACE_REL = Path("tmp") / "runes-trial" / "m21-4"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "curated-note"


def parse_frontmatter_and_body(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    raw_meta = parts[1]
    body = parts[2]
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body.strip()


def ensure_trial_workspace(root: Path, workspace: Path) -> None:
    approved_dir = workspace / "proposals" / "approved"
    if approved_dir.exists() and list(approved_dir.glob("*.md")):
        return

    runner = root / "tools" / "runes" / "trial_run_m21_4.py"
    subprocess.run(
        [sys.executable, str(runner), "--workspace", str(workspace), "--json"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def load_approved_proposal(workspace: Path, proposal: str | None) -> tuple[Path, dict[str, str], str]:
    approved_dir = workspace / "proposals" / "approved"
    if proposal:
        path = approved_dir / proposal
        if not path.suffix:
            path = path.with_suffix(".md")
    else:
        candidates = sorted(approved_dir.glob("*.md"))
        if not candidates:
            raise FileNotFoundError(f"no approved proposal found under {approved_dir}")
        path = candidates[0]

    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter_and_body(text)
    return path, meta, body


def build_curated_note_preview(meta: dict[str, str], body: str, source_path: Path, target_path: str) -> str:
    title = meta.get("title") or source_path.stem
    proposal_id = meta.get("proposal_id") or source_path.stem
    trial_marker = meta.get("trial_marker", "")

    return f"""---
title: {title}
source_proposal_id: {proposal_id}
source_status: approved
promotion_mode: human_only_dry_run
trusted_memory: pending_human_promotion
created_from: {source_path.as_posix()}
planned_target: {target_path}
planned_at: {now_iso()}
---

# {title}

> Promotion plan only. This preview is not written to the curated wiki by M21.5.

## Accepted Knowledge

{body}

## Provenance

- Source proposal: `{proposal_id}`
- Source path: `{source_path.as_posix()}`
- Trial marker: `{trial_marker}`
- Promotion authority: human-only during P0

## P0 Guardrail

Hermes-agent may request or inspect this promotion plan, but must not directly write the curated note.
"""


def promotion_plan(root: Path, workspace: Path, domain: str, proposal: str | None) -> dict[str, Any]:
    ensure_trial_workspace(root, workspace)
    source_path, meta, body = load_approved_proposal(workspace, proposal)

    title = meta.get("title") or source_path.stem
    proposal_id = meta.get("proposal_id") or source_path.stem
    slug = slugify(title)
    target_rel = f"wiki/{domain}/{slug}.md"
    target_abs = root / target_rel
    preview = build_curated_note_preview(meta, body, source_path, target_rel)

    checks = {
        "source_proposal_exists": source_path.exists(),
        "source_status_is_approved": meta.get("status") == "approved",
        "target_is_under_wiki_domain": target_rel.startswith(f"wiki/{domain}/"),
        "curated_write_performed": False,
        "database_mutated": False,
        "proposal_state_mutated": False,
        "requires_human_final_action": True,
    }

    status = "PASS" if all(checks.values()) else "FAIL"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M21.5 Human-only curated promotion path",
        "status": status,
        "mode": "dry_run_only",
        "workspace": str(workspace),
        "source": {
            "proposal_id": proposal_id,
            "status": meta.get("status"),
            "path": str(source_path),
            "title": title,
        },
        "target": {
            "domain": domain,
            "planned_path": target_rel,
            "exists_now": target_abs.exists(),
        },
        "checks": checks,
        "human_only": True,
        "agent_may_promote": False,
        "curated_write_performed": False,
        "database_mutated": False,
        "proposal_state_mutated": False,
        "next_human_actions": [
            "review the promotion plan",
            "review the preview content",
            "manually approve or edit the curated target path",
            "perform final curated wiki write outside Hermes-agent authority",
            "run importer / recall / smoke after human-approved promotion",
        ],
        "preview": preview,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate M21.5 human-only promotion plan / dry-run.")
    parser.add_argument("--workspace", help="M21.4 sandbox workspace path.")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help="Target wiki domain for planned curated note.")
    parser.add_argument("--proposal", help="Approved proposal filename or id under proposals/approved.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else root / DEFAULT_WORKSPACE_REL
    result = promotion_plan(root, workspace, args.domain, args.proposal)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result['suite']}: {result['status']}")
        print(f"source={result['source']['path']}")
        print(f"planned_target={result['target']['planned_path']}")
        print("Use --json for details.")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
