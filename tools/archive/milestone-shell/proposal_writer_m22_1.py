#!/usr/bin/env python3
"""M22.1 governed draft proposal writer.

This is the first controlled step beyond M21 dry-run/sandbox behavior.
It may create a draft proposal file only after explicit consent is supplied.
It never approves, rejects, promotes, imports, indexes, or mutates trusted memory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from offer_policy import classify_offer_intent, decision_to_dict
except ImportError:  # pragma: no cover
    from tools.runes.offer_policy import classify_offer_intent, decision_to_dict

SCHEMA_VERSION = "m22.1.p0.v1"
DEFAULT_PROJECT = "k6-freelancer"
DEFAULT_PROPOSAL_DIR = "forge-inbox"
CONSENT_MARKERS = {
    "go",
    "好",
    "可以",
    "建立 proposal",
    "寫進 runes",
    "寫進 wiki",
    "寫進 roadmap",
    "固化",
    "記到 wiki",
    "yes",
    "yes, create the proposal",
    "create proposal",
}


@dataclass(frozen=True)
class ProposalWriteResult:
    status: str
    path: str | None
    proposal_id: str | None
    reason: str | None
    data: dict[str, Any]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "proposal"


def safe_project(project: str) -> str:
    project = project.strip()
    if not re.fullmatch(r"[a-zA-Z0-9._-]+", project):
        raise ValueError(f"unsafe project name: {project!r}")
    return project


def consent_ok(consent: str | None) -> bool:
    if not consent:
        return False
    normalized = consent.strip().lower()
    return normalized in {marker.lower() for marker in CONSENT_MARKERS}


def read_input_text(text: str | None, file: str | None) -> str:
    if text is not None:
        return text
    if file:
        return Path(file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("proposal writer requires --text, --file, or stdin input")


def build_proposal_body(
    *,
    proposal_id: str,
    title: str,
    project: str,
    source_context: str,
    content: str,
    consent: str,
    created_at: str,
) -> str:
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"""---
proposal_id: {proposal_id}
title: {title}
project: {project}
status: draft
trusted_memory: false
created_by: runes_propose_m22_1
created_at: {created_at}
source_context: {source_context}
user_consent_marker: {consent}
content_sha256: {content_hash}
---

# {title}

## Proposal Status

- Status: draft
- Trusted memory: false
- Human approval required: true
- Agent may approve: false
- Agent may promote: false

## Source Context

{source_context}

## Proposed Knowledge

{content.strip()}

## P0 Guardrails

This file is a governed draft proposal only.

It is not trusted memory until a human reviews, approves, promotes, imports, and verifies it through the governed path.

Hermes-agent must not directly move this proposal to approved/rejected state, promote it into curated wiki content, mutate importer artifacts, or write database/index records.
"""


def write_proposal(
    *,
    root: Path,
    title: str,
    text: str,
    project: str,
    source_context: str,
    consent: str | None,
    output_root: str | None,
) -> ProposalWriteResult:
    offer_decision = decision_to_dict(classify_offer_intent(text))

    base = {
        "schema_version": SCHEMA_VERSION,
        "suite": "M22.1 Governed draft proposal writer",
        "mode": "draft_write_only",
        "project": project,
        "title": title,
        "source_context": source_context,
        "offer_decision": offer_decision,
        "requires_user_consent": True,
        "trusted_memory_created": False,
        "approved": False,
        "promoted": False,
        "database_mutated": False,
        "importer_mutated": False,
        "proposal_state": "draft",
    }

    if not consent_ok(consent):
        data = {
            **base,
            "status": "REFUSED",
            "reason": "missing_or_invalid_user_consent_marker",
            "proposal_created": False,
        }
        return ProposalWriteResult("REFUSED", None, None, data["reason"], data)

    blockers = offer_decision.get("blockers") or []
    if blockers:
        data = {
            **base,
            "status": "REFUSED",
            "reason": "offer_policy_blocker_present",
            "blockers": blockers,
            "proposal_created": False,
        }
        return ProposalWriteResult("REFUSED", None, None, data["reason"], data)

    created_at = now_utc().isoformat()
    date_prefix = now_utc().strftime("%Y%m%d-%H%M%S")
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]
    proposal_id = f"m22-1-{slugify(title)}-{date_prefix}-{content_hash}"

    if output_root:
        out_dir = Path(output_root).expanduser().resolve() / safe_project(project) / DEFAULT_PROPOSAL_DIR
    else:
        out_dir = root / "wiki" / safe_project(project) / DEFAULT_PROPOSAL_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{proposal_id}.md"

    body = build_proposal_body(
        proposal_id=proposal_id,
        title=title,
        project=project,
        source_context=source_context,
        content=text,
        consent=consent or "",
        created_at=created_at,
    )
    path.write_text(body, encoding="utf-8")

    data = {
        **base,
        "status": "PASS",
        "proposal_created": True,
        "proposal_id": proposal_id,
        "path": str(path),
        "relative_path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path),
        "checks": {
            "proposal_file_exists": path.exists(),
            "proposal_state_is_draft": True,
            "trusted_memory_created": False,
            "approved": False,
            "promoted": False,
            "database_mutated": False,
            "importer_mutated": False,
            "consent_recorded": True,
        },
    }
    return ProposalWriteResult("PASS", str(path), proposal_id, None, data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a governed draft proposal after explicit consent.")
    parser.add_argument("--title", required=True, help="Proposal title.")
    parser.add_argument("--text", help="Proposal text.")
    parser.add_argument("--file", help="UTF-8 file containing proposal text.")
    parser.add_argument("--project", default=DEFAULT_PROJECT, help="Target project/domain, e.g. k6-freelancer.")
    parser.add_argument("--source-context", default="user_provided", help="Short provenance/source context.")
    parser.add_argument("--consent", help="Explicit user consent marker, e.g. 'go' or '建立 proposal'.")
    parser.add_argument("--output-root", help="Optional alternate root for sandbox/smoke proposal writes.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = repo_root()
    text = read_input_text(args.text, args.file)
    try:
        result = write_proposal(
            root=root,
            title=args.title,
            text=text,
            project=args.project,
            source_context=args.source_context,
            consent=args.consent,
            output_root=args.output_root,
        )
    except Exception as exc:  # pragma: no cover - command-line safety wrapper
        payload = {
            "schema_version": SCHEMA_VERSION,
            "suite": "M22.1 Governed draft proposal writer",
            "status": "FAIL",
            "error": str(exc),
            "proposal_created": False,
            "trusted_memory_created": False,
            "database_mutated": False,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 1

    if args.json:
        print(json.dumps(result.data, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{result.data['suite']}: {result.status}")
        if result.path:
            print(f"path={result.path}")
        if result.reason:
            print(f"reason={result.reason}")
        print("Use --json for details.")

    return 0 if result.status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
