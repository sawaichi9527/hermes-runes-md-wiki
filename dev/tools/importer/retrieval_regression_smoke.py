from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

SUITE = "M17.5b Retrieval Regression Smoke"
BLACKLIST = [
    "/tmp/",
    "tmp/",
    "/logs/",
    "logs/",
    "observations/",
    "forge-manifests",
    ".jsonl",
]

QUERIES = [
    {
        "id": "sample_markdown_source",
        "query": "Markdown source-of-truth",
        "project": "sample-project",
        "expect_results": True,
    },
    {
        "id": "sample_secret_policy",
        "query": "secrets API keys passwords",
        "project": "sample-project",
        "expect_results": True,
    },
    {
        "id": "sample_first_real_write",
        "query": "First Real Write",
        "project": "sample-project",
        "expect_results": True,
    },
    {
        "id": "sample_manifest_exclusion",
        "query": "forge-manifests",
        "project": "sample-project",
        "expect_results": False,
    },
    {
        "id": "k6_m15_governance",
        "query": "M15 forge writer governance baseline",
        "project": "k6-freelancer",
        "expect_results": True,
    },
    {
        "id": "k6_m16_preview_governance",
        "query": "M16 importer preview read-only baseline",
        "project": "k6-freelancer",
        "expect_results": True,
    },
    {
        "id": "k6_operations_continuity",
        "query": "operations memory audit PASS",
        "project": "k6-freelancer",
        "expect_results": True,
    },
    {
        "id": "k6_services_continuity",
        "query": "Telegram integration service",
        "project": "k6-freelancer",
        "expect_results": True,
    },
    {
        "id": "k6_verification_continuity",
        "query": "verification smoke PASS",
        "project": "k6-freelancer",
        "expect_results": True,
    },
]


def extract_source_paths(data: Any) -> list[str]:
    paths: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"path", "source", "source_path", "file", "filename"} and isinstance(item, str):
                    paths.append(item)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(data)
    return list(dict.fromkeys(paths))


def blacklist_hits(paths: list[str]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        normalized = path.replace("\\", "/")
        for token in BLACKLIST:
            if token in normalized:
                hits.append({"path": path, "token": token})
    return hits


def run_case(root: Path, recall_bin: str, case: dict[str, Any]) -> dict[str, Any]:
    cmd = [
        recall_bin,
        case["query"],
        "--project",
        case["project"],
        "--mode",
        "hybrid",
        "--limit",
        "5",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=root,
        text=True,
        capture_output=True,
    )

    parsed: Any = None
    parse_error = None
    source_paths: list[str] = []
    hits: list[dict[str, str]] = []

    if proc.stdout.strip():
        try:
            parsed = json.loads(proc.stdout)
            source_paths = extract_source_paths(parsed)
            hits = blacklist_hits(source_paths)
        except Exception as exc:  # noqa: BLE001
            parse_error = str(exc)
    else:
        parse_error = "empty stdout"

    result_count = 0
    if isinstance(parsed, dict):
        for key in ("results", "items", "sources"):
            if isinstance(parsed.get(key), list):
                result_count = len(parsed[key])
                break
        if result_count == 0 and isinstance(parsed.get("count"), int):
            result_count = parsed["count"]

    failures: list[str] = []
    if proc.returncode != 0:
        failures.append("recall_command_failed")
    if parse_error:
        failures.append("json_parse_failed")
    if hits:
        failures.append("blacklisted_source_path")
    if case.get("expect_results") and result_count <= 0:
        failures.append("expected_results_missing")

    status = "PASS" if not failures else "FAIL"
    return {
        "id": case["id"],
        "status": status,
        "query": case["query"],
        "project": case["project"],
        "expect_results": case["expect_results"],
        "returncode": proc.returncode,
        "result_count": result_count,
        "source_paths": source_paths,
        "blacklist_hits": hits,
        "failures": failures,
        "parse_error": parse_error,
        "stderr_tail": proc.stderr[-800:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only retrieval regression smoke runner.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--recall-bin", default="./bin/hermes-recall")
    args = parser.parse_args()

    root = Path.cwd()
    results = [run_case(root, args.recall_bin, case) for case in QUERIES]
    failed = sum(1 for item in results if item["status"] != "PASS")

    payload = {
        "suite": SUITE,
        "status": "PASS" if failed == 0 else "FAIL",
        "failed": failed,
        "total": len(results),
        "read_only": True,
        "db_write": False,
        "chunk_create": False,
        "index_update": False,
        "importer_trigger": False,
        "git_write": False,
        "blacklist": BLACKLIST,
        "results": results,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"{payload['status']}: {SUITE} failed={failed} total={len(results)}")
        for item in results:
            print(f"{item['status']}: {item['id']} results={item['result_count']} failures={','.join(item['failures'])}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
