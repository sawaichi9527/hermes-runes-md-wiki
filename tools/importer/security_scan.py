#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
import os


ROOT = Path(os.environ.get("HERMES_MEMORY_ROOT", str(Path(__file__).resolve().parents[2]))).expanduser()
WIKI_DIR = ROOT / "wiki"


SECRET_PATTERNS = [
    {
        "name": "telegram_bot_token",
        "severity": "HIGH",
        "regex": re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
        "hint": "Possible Telegram bot token",
    },
    {
        "name": "openai_like_api_key",
        "severity": "HIGH",
        "regex": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        "hint": "Possible OpenAI-compatible API key",
    },
    {
        "name": "github_token",
        "severity": "HIGH",
        "regex": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
        "hint": "Possible GitHub token",
    },
    {
        "name": "postgres_url_with_password",
        "severity": "HIGH",
        "regex": re.compile(r"postgres(?:ql)?://[^:\s]+:[^@\s]+@[^/\s]+/[^\s]+", re.IGNORECASE),
        "hint": "Possible PostgreSQL DSN containing password",
    },
    {
        "name": "password_assignment",
        "severity": "MEDIUM",
        "regex": re.compile(r"\b(?:POSTGRES_PASSWORD|PGPASSWORD|PASSWORD|DB_PASSWORD)\s*=\s*['\"]?[^'\"\s]+", re.IGNORECASE),
        "hint": "Possible password assignment",
    },
    {
        "name": "api_key_assignment",
        "severity": "MEDIUM",
        "regex": re.compile(r"\b(?:API_KEY|OPENAI_API_KEY|TAVILY_API_KEY|TOKEN|BOT_TOKEN)\s*=\s*['\"]?[^'\"\s]+", re.IGNORECASE),
        "hint": "Possible API key or token assignment",
    },
]


ALLOWLIST_PATTERNS = [
    re.compile(r"your[_-]?api[_-]?key", re.IGNORECASE),
    re.compile(r"example", re.IGNORECASE),
    re.compile(r"dummy", re.IGNORECASE),
    re.compile(r"placeholder", re.IGNORECASE),
    re.compile(r"<[^>]+>"),
    re.compile(r"\$\{[^}]+\}"),
]


def mask_secret(value: str) -> str:
    value = value.strip()
    if len(value) <= 12:
        return "***"
    return value[:6] + "..." + value[-4:]


def is_allowlisted(line: str) -> bool:
    return any(p.search(line) for p in ALLOWLIST_PATTERNS)


def scan_file(path: Path):
    findings = []
    rel = str(path.relative_to(ROOT))

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    for lineno, line in enumerate(text.splitlines(), start=1):
        if is_allowlisted(line):
            continue

        for rule in SECRET_PATTERNS:
            for match in rule["regex"].finditer(line):
                findings.append(
                    {
                        "file": rel,
                        "line": lineno,
                        "rule": rule["name"],
                        "severity": rule["severity"],
                        "hint": rule["hint"],
                        "match_masked": mask_secret(match.group(0)),
                    }
                )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="M6.3a scan Markdown wiki for possible secrets.")
    parser.add_argument("--path", default=str(WIKI_DIR), help="Path to scan. Default: wiki directory.")
    parser.add_argument("--fail-on-findings", action="store_true", help="Exit non-zero if findings exist.")
    args = parser.parse_args()

    scan_root = Path(args.path).expanduser()
    if not scan_root.is_absolute():
        scan_root = ROOT / scan_root

    report = {
        "suite": "M6.3a security scan",
        "root": str(ROOT),
        "scan_path": str(scan_root),
        "status": "UNKNOWN",
        "files_scanned": 0,
        "findings_count": 0,
        "findings": [],
        "notes": [],
    }

    if not scan_root.exists():
        report["status"] = "FAIL"
        report["notes"].append(f"scan path not found: {scan_root}")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    paths = [scan_root] if scan_root.is_file() else sorted(scan_root.rglob("*.md"))

    for path in paths:
        if not path.is_file():
            continue
        report["files_scanned"] += 1
        report["findings"].extend(scan_file(path))

    report["findings_count"] = len(report["findings"])

    if report["findings_count"] == 0:
        report["status"] = "PASS"
        report["notes"].append("no obvious secrets found")
    else:
        report["status"] = "FINDINGS"
        report["notes"].append("possible secrets found; review before import")

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.fail_on_findings and report["findings_count"] > 0:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
