#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path.home() / "workspace/hermes-memory"
OPERATIONS_MD = ROOT / "wiki/k6-freelancer/operations.md"


TOOLS = {
    "memory.check": {
        "cmd": ["hermes-memory-check"],
        "risk": "low",
        "write": False,
        "timeout": 60,
        "description": "Check Hermes Memory environment, commands, and DB schema probe.",
    },
    "memory.eval": {
        "cmd": ["hermes-memory-eval"],
        "risk": "medium",
        "write": True,
        "timeout": 420,
        "description": "Run Hermes Memory smoke/eval suites.",
    },
    "memory.import": {
        "cmd": ["hermes-memory-import"],
        "risk": "medium",
        "write": True,
        "timeout": 300,
        "description": "Run incremental Markdown memory import.",
    },
    "memory.backup": {
        "cmd": ["hermes-memory-backup"],
        "risk": "medium",
        "write": True,
        "timeout": 300,
        "description": "Create Hermes Memory backup.",
    },
    "memory.restore_dry_run": {
        "cmd": "__dynamic_restore_latest__",
        "risk": "low",
        "write": False,
        "timeout": 180,
        "description": "Verify latest Hermes Memory backup with restore dry-run.",
    },
}


def latest_backup_dir() -> str:
    backups = ROOT / "backups"
    dirs = sorted(
        [p for p in backups.glob("hermes-memory-backup-*") if p.is_dir()],
        key=lambda p: p.name,
    )
    if not dirs:
        raise RuntimeError("No backup directory found.")
    return str(dirs[-1])


def resolve_cmd(tool_name: str):
    spec = TOOLS[tool_name]
    cmd = spec["cmd"]

    if cmd == "__dynamic_restore_latest__":
        return ["hermes-memory-restore", latest_backup_dir(), "--dry-run"]

    return list(cmd)


def scrub(text: str) -> str:
    if not text:
        return ""

    text = text[-4000:]

    text = re.sub(
        r"(postgres(?:ql)?://[^:\s]+:)[^@\s]+(@)",
        r"\1***REDACTED***\2",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(DATABASE_URL=postgres(?:ql)?://[^:\s]+:)[^@\s]+(@)",
        r"\1***REDACTED***\2",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(PGPASSWORD=)[^\s]+",
        r"\1***REDACTED***",
        text,
        flags=re.IGNORECASE,
    )
    return text


def list_tools():
    return {
        "status": "ok",
        "tools": [
            {
                "name": name,
                "risk": spec["risk"],
                "write": spec["write"],
                "timeout": spec["timeout"],
                "description": spec["description"],
            }
            for name, spec in sorted(TOOLS.items())
        ],
    }


def extract_summary(tool_name: str, result: dict) -> list[str]:
    stdout = result.get("stdout_tail", "") or ""
    lines = []

    if tool_name == "memory.check":
        lines.append("Environment, commands, and database/schema probe completed.")
        if "status=PASS" in stdout:
            lines.append("Check status marker: PASS.")

    elif tool_name == "memory.restore_dry_run":
        lines.append("Latest backup restore dry-run verification completed.")
        m = re.search(r"backup_dir=([^\n]+)", stdout)
        if m:
            lines.append(f"Backup directory: `{m.group(1)}`.")
        if "postgres.dump readable" in stdout:
            lines.append("PostgreSQL dump readability verified.")

    elif tool_name == "memory.backup":
        lines.append("Backup command completed.")
        m = re.search(r"backup_dir=([^\n]+)", stdout)
        if m:
            lines.append(f"Backup directory: `{m.group(1)}`.")
        if "postgres.dump" in stdout:
            lines.append("PostgreSQL dump generated.")

    elif tool_name == "memory.import":
        lines.append("Markdown memory import completed.")
        m = re.search(r"summary: ([^\n]+)", stdout)
        if m:
            lines.append(f"Importer summary: `{m.group(1)}`.")

    elif tool_name == "memory.eval":
        lines.append("Hermes Memory evaluation suite completed.")
        m = re.search(r"summary: ([^\n]+)", stdout)
        if m:
            lines.append(f"Evaluation summary: `{m.group(1)}`.")
        for suite in [
            "M5.2 Evaluation Smoke Test",
            "Phase3 M6.6 Expanded Evaluation",
            "Phase3 M6.7.2 Backup Verification Smoke",
            "Phase3 M6.7.3 Restore Dry-run Verification Smoke",
            "Phase3 M7.2 Tool Runner Smoke",
        ]:
            if suite in stdout:
                lines.append(f"{suite}: observed.")

    else:
        lines.append("Tool completed.")

    return lines


def ensure_operations_md():
    OPERATIONS_MD.parent.mkdir(parents=True, exist_ok=True)
    if not OPERATIONS_MD.exists():
        OPERATIONS_MD.write_text(
            "# Operations Log\n\n"
            "This file records summarized Hermes Memory tool runs.\n\n"
            "Rules:\n"
            "- Do not store secrets.\n"
            "- Do not paste full stdout/stderr logs.\n"
            "- Store concise operational summaries only.\n\n"
            "---\n\n",
            encoding="utf-8",
        )


def append_operation_log(result: dict):
    ensure_operations_md()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    tool = result.get("tool", "unknown")
    status = result.get("status", "UNKNOWN")
    duration = result.get("duration_sec", "unknown")
    risk = result.get("risk", "unknown")
    write = result.get("write", "unknown")
    rc = result.get("returncode", "unknown")

    summary_lines = extract_summary(tool, result)

    entry = []
    entry.append(f"## O-{stamp} {tool}\n")
    entry.append(f"Status: {status}\n")
    entry.append(f"Time: {now}\n")
    entry.append(f"Duration: {duration}s\n")
    entry.append(f"Risk: {risk}\n")
    entry.append(f"Write: {write}\n")
    entry.append(f"Return code: {rc}\n")
    entry.append("\nSummary:\n")
    for line in summary_lines:
        entry.append(f"- {line}\n")
    entry.append("\n---\n\n")

    with OPERATIONS_MD.open("a", encoding="utf-8") as f:
        f.writelines(entry)

    return str(OPERATIONS_MD)


def run_tool(tool_name: str):
    if tool_name not in TOOLS:
        return {
            "status": "error",
            "error": "tool_not_allowed",
            "tool": tool_name,
            "allowed_tools": sorted(TOOLS.keys()),
        }, 2

    spec = TOOLS[tool_name]
    started = time.time()

    try:
        cmd = resolve_cmd(tool_name)

        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=spec["timeout"],
        )

        duration = round(time.time() - started, 3)

        result = {
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "tool": tool_name,
            "risk": spec["risk"],
            "write": spec["write"],
            "timeout": spec["timeout"],
            "duration_sec": duration,
            "returncode": proc.returncode,
            "cmd": cmd,
            "stdout_tail": scrub(proc.stdout),
            "stderr_tail": scrub(proc.stderr),
        }
        return result, 0 if proc.returncode == 0 else 1

    except subprocess.TimeoutExpired as e:
        duration = round(time.time() - started, 3)
        return {
            "status": "FAIL",
            "tool": tool_name,
            "risk": spec["risk"],
            "write": spec["write"],
            "timeout": spec["timeout"],
            "duration_sec": duration,
            "error": "timeout",
            "stdout_tail": scrub(e.stdout or ""),
            "stderr_tail": scrub(e.stderr or ""),
        }, 124

    except Exception as e:
        duration = round(time.time() - started, 3)
        return {
            "status": "FAIL",
            "tool": tool_name,
            "duration_sec": duration,
            "error": type(e).__name__,
            "message": str(e),
        }, 1


def main():
    parser = argparse.ArgumentParser(description="Hermes Memory local tool runner.")
    parser.add_argument("tool", nargs="?", help="Tool name, e.g. memory.check")
    parser.add_argument("--list", action="store_true", help="List allowed tools.")
    parser.add_argument("--log", action="store_true", help="Append summarized result to operations.md.")
    args = parser.parse_args()

    if args.list:
        print(json.dumps(list_tools(), ensure_ascii=False, indent=2))
        return 0

    if not args.tool:
        print(json.dumps({
            "status": "error",
            "error": "missing_tool",
            "hint": "Use --list or provide a tool name.",
        }, ensure_ascii=False, indent=2))
        return 2

    result, rc = run_tool(args.tool)

    if args.log:
        try:
            log_path = append_operation_log(result)
            result["operation_log"] = log_path
        except Exception as e:
            result["operation_log_error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            if result.get("status") == "PASS":
                result["status"] = "FAIL"
                rc = 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
