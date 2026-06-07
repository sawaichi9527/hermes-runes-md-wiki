#!/usr/bin/env bash
set -euo pipefail
cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cat > tools/runes/smoke_m25_3_promotion_patch.py <<'PY'
#!/usr/bin/env python3
# M25.3 curated promotion patch smoke test.

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_PATH = "wiki/k6-freelancer/services.md"
TARGET_ABS = ROOT / TARGET_PATH


def sha256_file(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, name: str, details: dict | None = None) -> dict:
    return {
        "name": name,
        "status": "PASS" if condition else "FAIL",
        "details": details or {},
    }


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    before_hash = sha256_file(TARGET_ABS)
    results: list[dict] = []

    from promotion_patch_m25_2 import build_promotion_patch_preview, render_patch_markdown_preview

    payload = build_promotion_patch_preview(
        root=ROOT,
        project="k6-freelancer",
        proposal_id="m25-3-smoke-proposal",
        target_path=TARGET_PATH,
        heading="Telegram Integration",
        insert_text="- M25.3 curated promotion patch smoke evidence.",
        reason="M25.3 smoke dry-run",
    )

    results.append(check(payload.get("status") == "PASS", "helper returns PASS"))
    results.append(check(payload.get("mode") == "dry_run_only", "helper mode is dry_run_only"))
    results.append(check(payload.get("suite") == "M25.2 Curated promotion patch dry-run", "helper suite matches M25.2 baseline"))
    results.append(check(payload.get("promotion", {}).get("forge_suggestion") is True, "forge suggestion is true"))
    results.append(check(payload.get("promotion", {}).get("promotion_execution_implemented") is False, "promotion execution remains unimplemented"))
    results.append(check(payload.get("promotion", {}).get("trusted_wiki_mutation_allowed") is False, "trusted wiki mutation is not allowed"))

    preview = payload.get("preview", {})
    mutations = payload.get("mutations", {})

    for key in [
        "would_write_target_file",
        "would_update_proposal_state",
        "would_promote_to_wiki",
        "would_mutate_database",
        "would_run_importer",
    ]:
        results.append(check(preview.get(key) is False, f"preview boundary {key} is false"))

    for key in [
        "target_file_written",
        "proposal_state_mutated",
        "trusted_memory_created",
        "curated_wiki_mutated",
        "database_mutated",
        "importer_mutated",
        "files_written",
    ]:
        results.append(check(mutations.get(key) is False, f"mutation boundary {key} is false"))

    diff_text = payload.get("unified_diff") or ""
    results.append(check("--- a/" + TARGET_PATH in diff_text, "unified diff has source path"))
    results.append(check("+++ b/" + TARGET_PATH in diff_text, "unified diff has target path"))
    results.append(check("M25.3 curated promotion patch smoke evidence" in diff_text, "unified diff contains candidate evidence"))

    markdown = render_patch_markdown_preview(payload)
    results.append(check("Curated Promotion Patch Preview" in markdown, "markdown preview title present"))
    results.append(check("forge suggestion, not forge execution" in markdown, "markdown preview explains forge boundary"))
    results.append(check("M25.2 does not apply the patch" in markdown, "markdown preview explains no apply"))

    cli_json = run_cmd([
        "bin/runes",
        "promotion",
        "preview",
        "--proposal-id",
        "m25-3-smoke-proposal",
        "--target-path",
        TARGET_PATH,
        "--heading",
        "Telegram Integration",
        "--insert-text",
        "- M25.3 curated promotion patch smoke evidence.",
        "--reason",
        "M25.3 smoke dry-run",
        "--dry-run",
        "--json",
    ])

    results.append(check(cli_json.returncode == 0, "CLI JSON return code is zero", {"stderr": cli_json.stderr[-400:]}))
    try:
        cli_payload = json.loads(cli_json.stdout)
    except Exception as exc:
        cli_payload = {}
        results.append(check(False, "CLI JSON parses", {"error": str(exc), "stdout": cli_json.stdout[-400:]}))
    else:
        results.append(check(cli_payload.get("status") == "PASS", "CLI JSON status PASS"))
        results.append(check(cli_payload.get("mutations", {}).get("database_mutated") is False, "CLI JSON database mutation false"))
        results.append(check(cli_payload.get("mutations", {}).get("target_file_written") is False, "CLI JSON target file written false"))
        results.append(check(cli_payload.get("promotion", {}).get("promotion_execution_implemented") is False, "CLI JSON promotion execution false"))

    cli_markdown = run_cmd([
        "bin/runes",
        "promotion",
        "preview",
        "--proposal-id",
        "m25-3-smoke-proposal",
        "--target-path",
        TARGET_PATH,
        "--heading",
        "Telegram Integration",
        "--insert-text",
        "- M25.3 curated promotion patch smoke evidence.",
        "--reason",
        "M25.3 smoke dry-run",
        "--dry-run",
        "--markdown",
    ])

    results.append(check(cli_markdown.returncode == 0, "CLI Markdown return code is zero", {"stderr": cli_markdown.stderr[-400:]}))
    results.append(check("Curated Promotion Patch Preview" in cli_markdown.stdout, "CLI Markdown title present"))
    results.append(check("forge suggestion, not forge execution" in cli_markdown.stdout, "CLI Markdown forge boundary present"))
    results.append(check("M25.2 does not apply the patch" in cli_markdown.stdout, "CLI Markdown no-apply boundary present"))

    after_hash = sha256_file(TARGET_ABS)
    results.append(check(before_hash == after_hash, "target Markdown file hash unchanged", {"before": before_hash, "after": after_hash}))

    failed = [item for item in results if item["status"] != "PASS"]
    report = {
        "suite": "M25.3 Curated Promotion Patch smoke test",
        "status": "PASS" if not failed else "FAIL",
        "failed": len(failed),
        "total": len(results),
        "boundary": {
            "dry_run_only": True,
            "trusted_wiki_mutation_allowed": False,
            "database_mutation_allowed": False,
            "promotion_execution_implemented": False,
            "target_file_written": False,
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
PY

cat >> wiki/k6-freelancer/roadmap.md <<'MD'

---

## M25.3 Promotion Patch Smoke Test

Status: PASS / REGRESSION BASELINE

Verification target:

- `tools/runes/smoke_m25_3_promotion_patch.py`

Scope:

- validate promotion patch helper payload
- validate JSON preview
- validate Markdown preview
- validate CLI route through `bin/runes promotion preview`
- validate target Markdown hash remains unchanged
- validate no trusted wiki mutation
- validate no database mutation
- validate no importer mutation
- validate no promotion execution

Boundary:

M25.3 is still dry-run only. It does not apply any promotion patch.

Next:

- M25.4 Roadmap / verification lock

MD

python3 -m py_compile \
  tools/runes/promotion_patch_m25_2.py \
  tools/runes/smoke_m25_3_promotion_patch.py \
  tools/runes/runes.py

python3 tools/runes/smoke_m25_3_promotion_patch.py

git add \
  tools/runes/smoke_m25_3_promotion_patch.py \
  wiki/k6-freelancer/roadmap.md

git diff --cached

git commit -m "Add M25.3 promotion patch smoke test"

git push origin main

git log --oneline -4
