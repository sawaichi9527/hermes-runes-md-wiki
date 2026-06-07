#!/usr/bin/env python3
# M26.3 apply preflight confirmation / blocking smoke test.

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_PATH = "wiki/k6-freelancer/services.md"
TARGET_ABS = ROOT / TARGET_PATH
PROPOSAL_ID = "m26-3-preflight-smoke"
INSERT_TEXT = "- M26.3 apply preflight confirmation smoke evidence."


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

    from promotion_apply_preflight_m26_2 import build_apply_preflight, render_preflight_markdown

    payload = build_apply_preflight(
        root=ROOT,
        project="k6-freelancer",
        proposal_id=PROPOSAL_ID,
        target_path=TARGET_PATH,
        heading="Telegram Integration",
        insert_text=INSERT_TEXT,
        reason="M26.3 smoke dry-run",
    )

    required_token = payload.get("confirmation", {}).get("required_confirmation_token")

    results.append(check(payload.get("status") == "PASS", "base preflight status PASS"))
    results.append(check(payload.get("mode") == "dry_run_only", "base preflight mode dry_run_only"))
    results.append(check(payload.get("target", {}).get("path_ok") is True, "wiki target path accepted"))
    results.append(check(payload.get("preflight", {}).get("ready_for_future_apply") is True, "base preflight ready for future apply"))
    results.append(check(payload.get("confirmation", {}).get("human_confirmation_required") is True, "confirmation is required"))
    results.append(check(bool(required_token), "required confirmation token generated"))
    results.append(check(payload.get("confirmation", {}).get("confirmation_matches") is False, "confirmation does not match when absent"))
    results.append(check(payload.get("confirmation", {}).get("confirmation_does_not_apply_now") is True, "confirmation does not apply now"))

    confirmed = build_apply_preflight(
        root=ROOT,
        project="k6-freelancer",
        proposal_id=PROPOSAL_ID,
        target_path=TARGET_PATH,
        heading="Telegram Integration",
        insert_text=INSERT_TEXT,
        human_confirmation=required_token,
        reason="M26.3 confirmation smoke dry-run",
    )

    results.append(check(confirmed.get("status") == "PASS", "confirmed preflight status PASS"))
    results.append(check(confirmed.get("confirmation", {}).get("confirmation_matches") is True, "provided confirmation token matches"))
    results.append(check(confirmed.get("confirmation", {}).get("confirmation_does_not_apply_now") is True, "matched confirmation still does not apply now"))

    bad_hash = build_apply_preflight(
        root=ROOT,
        project="k6-freelancer",
        proposal_id=PROPOSAL_ID,
        target_path=TARGET_PATH,
        heading="Telegram Integration",
        insert_text=INSERT_TEXT,
        expected_pre_hash="deadbeef",
        reason="M26.3 hash mismatch smoke dry-run",
    )

    results.append(check(bad_hash.get("status") == "BLOCKED", "hash mismatch blocks preflight"))
    results.append(check(bad_hash.get("target", {}).get("expected_pre_hash_matches") is False, "hash mismatch reported"))
    results.append(check("expected pre-apply hash does not match current target file hash" in " ".join(bad_hash.get("preflight", {}).get("hard_errors", [])), "hash mismatch error reported"))

    non_wiki = build_apply_preflight(
        root=ROOT,
        project="k6-freelancer",
        proposal_id=PROPOSAL_ID,
        target_path="README.md",
        heading="Telegram Integration",
        insert_text=INSERT_TEXT,
        reason="M26.3 non-wiki path smoke dry-run",
    )

    results.append(check(non_wiki.get("status") == "BLOCKED", "non-wiki target blocks preflight"))
    results.append(check(non_wiki.get("target", {}).get("path_ok") is False, "non-wiki target path rejected"))
    results.append(check("target path must be under wiki/" in " ".join(non_wiki.get("preflight", {}).get("hard_errors", [])), "non-wiki path error reported"))

    outside_root = build_apply_preflight(
        root=ROOT,
        project="k6-freelancer",
        proposal_id=PROPOSAL_ID,
        target_path="../outside.md",
        heading="Telegram Integration",
        insert_text=INSERT_TEXT,
        reason="M26.3 outside-root path smoke dry-run",
    )

    results.append(check(outside_root.get("status") == "BLOCKED", "outside-root target blocks preflight"))
    results.append(check(outside_root.get("target", {}).get("path_ok") is False, "outside-root target rejected"))

    markdown = render_preflight_markdown(payload)
    results.append(check("Human-approved Promotion Apply Preflight" in markdown, "markdown preflight title present"))
    results.append(check("Required confirmation token" in markdown, "markdown confirmation token present"))
    results.append(check("M26.2 does not apply the patch" in markdown, "markdown no-apply boundary present"))

    cli_json = run_cmd([
        "bin/runes",
        "promotion",
        "preflight",
        "--proposal-id",
        PROPOSAL_ID,
        "--target-path",
        TARGET_PATH,
        "--heading",
        "Telegram Integration",
        "--insert-text",
        INSERT_TEXT,
        "--reason",
        "M26.3 CLI JSON smoke",
        "--dry-run",
        "--json",
    ])

    results.append(check(cli_json.returncode == 0, "CLI JSON preflight return code is zero", {"stderr": cli_json.stderr[-400:]}))
    try:
        cli_payload = json.loads(cli_json.stdout)
    except Exception as exc:
        cli_payload = {}
        results.append(check(False, "CLI JSON preflight parses", {"error": str(exc), "stdout": cli_json.stdout[-400:]}))
    else:
        results.append(check(cli_payload.get("status") == "PASS", "CLI JSON preflight status PASS"))
        results.append(check(cli_payload.get("confirmation", {}).get("human_confirmation_required") is True, "CLI JSON confirmation required true"))
        results.append(check(cli_payload.get("mutations", {}).get("target_file_written") is False, "CLI JSON target file not written"))
        results.append(check(cli_payload.get("mutations", {}).get("database_mutated") is False, "CLI JSON database not mutated"))
        results.append(check(cli_payload.get("mutations", {}).get("operation_record_written") is False, "CLI JSON operation record not written"))
        results.append(check(cli_payload.get("mutations", {}).get("rollback_snapshot_written") is False, "CLI JSON rollback snapshot not written"))

    cli_blocked = run_cmd([
        "bin/runes",
        "promotion",
        "preflight",
        "--proposal-id",
        PROPOSAL_ID,
        "--target-path",
        TARGET_PATH,
        "--heading",
        "Telegram Integration",
        "--insert-text",
        INSERT_TEXT,
        "--expected-pre-hash",
        "deadbeef",
        "--reason",
        "M26.3 CLI blocked smoke",
        "--dry-run",
        "--json",
    ])

    results.append(check(cli_blocked.returncode == 2, "CLI blocked preflight returns 2"))
    try:
        cli_blocked_payload = json.loads(cli_blocked.stdout)
    except Exception as exc:
        results.append(check(False, "CLI blocked JSON parses", {"error": str(exc), "stdout": cli_blocked.stdout[-400:]}))
    else:
        results.append(check(cli_blocked_payload.get("status") == "BLOCKED", "CLI blocked status BLOCKED"))
        results.append(check(cli_blocked_payload.get("target", {}).get("expected_pre_hash_matches") is False, "CLI blocked hash mismatch false"))

    after_hash = sha256_file(TARGET_ABS)
    results.append(check(before_hash == after_hash, "target Markdown file hash unchanged", {"before": before_hash, "after": after_hash}))

    for payload_name, tested_payload in [
        ("base", payload),
        ("confirmed", confirmed),
        ("bad_hash", bad_hash),
        ("non_wiki", non_wiki),
        ("outside_root", outside_root),
    ]:
        mutations = tested_payload.get("mutations", {})
        for key in [
            "target_file_written",
            "proposal_state_mutated",
            "trusted_memory_created",
            "curated_wiki_mutated",
            "database_mutated",
            "importer_mutated",
            "operation_record_written",
            "rollback_snapshot_written",
            "files_written",
        ]:
            results.append(check(mutations.get(key) is False, f"{payload_name} mutation boundary {key} is false"))

    failed = [item for item in results if item["status"] != "PASS"]
    report = {
        "suite": "M26.3 Apply preflight confirmation and blocking smoke test",
        "status": "PASS" if not failed else "FAIL",
        "failed": len(failed),
        "total": len(results),
        "boundary": {
            "dry_run_only": True,
            "confirmation_token_preview_only": True,
            "hash_mismatch_blocks_preflight": True,
            "non_wiki_path_blocks_preflight": True,
            "target_file_written": False,
            "database_mutation_allowed": False,
            "operation_record_written": False,
            "rollback_snapshot_written": False,
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
