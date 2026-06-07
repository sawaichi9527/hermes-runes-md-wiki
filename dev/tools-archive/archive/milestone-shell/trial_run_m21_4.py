#!/usr/bin/env python3
"""M21.4 sandbox multi-proposal P0 trial runner.

This runner validates the intended mixed-state proposal workflow without
mutating trusted wiki content, importer state, or PostgreSQL indexes.

It creates an isolated sandbox under tmp/runes-trial/m21-4 by default.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "m21.4.p0.v1"
TRIAL_MARKER = "M21.4-RUNES-SHIELD-TRIAL"


@dataclass(frozen=True)
class ProposalSpec:
    proposal_id: str
    title: str
    initial_status: str
    final_status: str
    content: str


PROPOSALS = [
    ProposalSpec(
        proposal_id="proposal-a-approved",
        title="M21.4 approved proposal trial marker",
        initial_status="draft",
        final_status="approved",
        content="Approved durable knowledge marker for M21.4 multi-proposal trial.",
    ),
    ProposalSpec(
        proposal_id="proposal-b-rejected",
        title="M21.4 rejected proposal trial marker",
        initial_status="draft",
        final_status="rejected",
        content="Rejected content marker that must not become trusted evidence.",
    ),
    ProposalSpec(
        proposal_id="proposal-c-draft",
        title="M21.4 draft proposal trial marker",
        initial_status="draft",
        final_status="draft",
        content="Draft content marker that must remain untrusted and excluded from recall.",
    ),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def proposal_text(spec: ProposalSpec, status: str) -> str:
    return f"""---
proposal_id: {spec.proposal_id}
title: {spec.title}
status: {status}
trial_marker: {TRIAL_MARKER}
created_by: m21_4_sandbox_trial
created_at: {now_iso()}
trusted_memory: false
---

# {spec.title}

{spec.content}

This file belongs to an isolated M21.4 sandbox trial and is not trusted wiki content.
"""


def write_proposal(path: Path, spec: ProposalSpec, status: str) -> None:
    path.write_text(proposal_text(spec, status), encoding="utf-8")


def read_texts(directory: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(directory.glob("*.md")):
        result[path.name] = path.read_text(encoding="utf-8")
    return result


def contains_marker(texts: dict[str, str], marker: str) -> bool:
    return any(marker in text for text in texts.values())


def run_trial(workspace: Path, clean: bool = True) -> dict[str, Any]:
    if workspace.exists() and clean:
        shutil.rmtree(workspace)

    draft_dir = workspace / "proposals" / "draft"
    approved_dir = workspace / "proposals" / "approved"
    rejected_dir = workspace / "proposals" / "rejected"
    trusted_dir = workspace / "trusted_indexed"
    recall_dir = workspace / "recall_results"

    for directory in (draft_dir, approved_dir, rejected_dir, trusted_dir, recall_dir):
        directory.mkdir(parents=True, exist_ok=True)

    paths: dict[str, dict[str, str]] = {}

    # 1. Create three draft proposals.
    for spec in PROPOSALS:
        path = draft_dir / f"{spec.proposal_id}.md"
        write_proposal(path, spec, spec.initial_status)
        paths[spec.proposal_id] = {"draft": str(path.relative_to(workspace))}

    # 2. Human approves A in sandbox.
    spec_a = PROPOSALS[0]
    path_a = draft_dir / f"{spec_a.proposal_id}.md"
    approved_a = approved_dir / path_a.name
    write_proposal(approved_a, spec_a, "approved")
    path_a.unlink()
    paths[spec_a.proposal_id]["approved"] = str(approved_a.relative_to(workspace))

    # 3. Human rejects B in sandbox.
    spec_b = PROPOSALS[1]
    path_b = draft_dir / f"{spec_b.proposal_id}.md"
    rejected_b = rejected_dir / path_b.name
    write_proposal(rejected_b, spec_b, "rejected")
    path_b.unlink()
    paths[spec_b.proposal_id]["rejected"] = str(rejected_b.relative_to(workspace))

    # 4. C remains draft.
    spec_c = PROPOSALS[2]
    path_c = draft_dir / f"{spec_c.proposal_id}.md"
    paths[spec_c.proposal_id]["remaining_draft"] = str(path_c.relative_to(workspace))

    # 5. Import approved content into sandbox trusted index only.
    trusted_a = trusted_dir / approved_a.name
    trusted_a.write_text(
        approved_a.read_text(encoding="utf-8").replace("trusted_memory: false", "trusted_memory: true"),
        encoding="utf-8",
    )
    paths[spec_a.proposal_id]["trusted_indexed"] = str(trusted_a.relative_to(workspace))

    # 6. Simulated recall reads only sandbox trusted index.
    trusted_texts = read_texts(trusted_dir)
    approved_visible = contains_marker(trusted_texts, spec_a.content)
    rejected_visible = contains_marker(trusted_texts, spec_b.content)
    draft_visible = contains_marker(trusted_texts, spec_c.content)

    recall_result = {
        "query": TRIAL_MARKER,
        "approved_visible": approved_visible,
        "rejected_visible": rejected_visible,
        "draft_visible": draft_visible,
        "trusted_files": sorted(trusted_texts),
    }
    (recall_dir / "recall.json").write_text(json.dumps(recall_result, ensure_ascii=False, indent=2), encoding="utf-8")

    checks = {
        "created_three_proposals": len(paths) == 3,
        "approved_imported_visible": approved_visible is True,
        "rejected_not_trusted_visible": rejected_visible is False,
        "draft_not_trusted_visible": draft_visible is False,
        "approved_file_exists": approved_a.exists(),
        "rejected_file_exists": rejected_b.exists(),
        "draft_file_exists": path_c.exists(),
        "trusted_index_contains_only_approved": sorted(trusted_texts) == [approved_a.name],
    }

    status = "PASS" if all(checks.values()) else "FAIL"

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": "M21.4 Multi-proposal P0 sandbox trial",
        "status": status,
        "mode": "sandbox_write_only",
        "workspace": str(workspace),
        "trusted_wiki_mutated": False,
        "database_mutated": False,
        "proposal_created_in_real_forge_inbox": False,
        "scenario": [
            "create proposal A/B/C as draft in sandbox",
            "approve A in sandbox",
            "reject B in sandbox",
            "leave C draft in sandbox",
            "import approved A into sandbox trusted index",
            "recall only sandbox trusted index",
            "verify rejected and draft markers are excluded",
        ],
        "checks": checks,
        "paths": paths,
        "recall_result": recall_result,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run M21.4 sandbox multi-proposal trial.")
    parser.add_argument("--workspace", help="Optional sandbox workspace path.")
    parser.add_argument("--no-clean", action="store_true", help="Do not clean existing workspace before running.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else root / "tmp" / "runes-trial" / "m21-4"
    result = run_trial(workspace, clean=not args.no_clean)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result['suite']}: {result['status']}")
        print(f"workspace={result['workspace']}")
        print("Use --json for details.")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
