#!/usr/bin/env python3
"""M23.4 Runes Attunement smoke test.

Verifies:
- attune/reject/supersede dry-run payloads
- no proposal/wiki/database/importer mutation flags
- approved does not mean promoted
- readable preview payload availability
"""

from __future__ import annotations

import json
from pathlib import Path

from proposal_attunement_m23_2 import attunement_dry_run


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
        payload = attunement_dry_run(
            root=root,
            project=project,
            proposal_id=proposal_id,
            action=action,
            reason="M23.4 smoke dry-run",
            superseded_by=extra.get("superseded_by"),
        )

        mutations = payload.get("mutations", {})
        attunement = payload.get("attunement", {})

        results.extend([
            check(payload.get("mode") == "dry_run_only", f"{action}: dry_run_only"),
            check(payload.get("status") in {"PASS", "NOT_FOUND", "BLOCKED"}, f"{action}: valid status"),
            check(payload.get("readable_preview_available") is True, f"{action}: readable preview available"),
            check(mutations.get("proposal_state_mutated") is False, f"{action}: no proposal state mutation"),
            check(mutations.get("trusted_memory_created") is False, f"{action}: no trusted memory creation"),
            check(mutations.get("curated_wiki_mutated") is False, f"{action}: no curated wiki mutation"),
            check(mutations.get("database_mutated") is False, f"{action}: no database mutation"),
            check(mutations.get("importer_mutated") is False, f"{action}: no importer mutation"),
            check(mutations.get("files_written") is False, f"{action}: no file writes"),
        ])

        if payload.get("status") != "NOT_FOUND":
            results.append(
                check(
                    attunement.get("approved_does_not_mean_promoted") is True,
                    f"{action}: approved does not mean promoted",
                )
            )
            results.append(
                check(
                    attunement.get("promotion_execution_implemented") is False,
                    f"{action}: promotion execution not implemented",
                )
            )

    failed = [item for item in results if item["status"] != "PASS"]

    summary = {
        "suite": "M23.4 Runes Attunement smoke test",
        "status": "PASS" if not failed else "FAIL",
        "failed": len(failed),
        "total": len(results),
        "results": results,
        "boundary": {
            "dry_run_only": True,
            "trusted_wiki_mutation_allowed": False,
            "database_mutation_allowed": False,
            "promotion_execution_implemented": False,
        },
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
