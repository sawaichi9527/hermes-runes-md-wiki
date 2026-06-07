#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.home() / "workspace/hermes-memory"
BACKUPS = ROOT / "backups"


def latest_backup_dir():
    dirs = sorted(
        [p for p in BACKUPS.glob("hermes-memory-backup-*") if p.is_dir()],
        key=lambda p: p.name,
    )
    return dirs[-1] if dirs else None


def main():
    result = {
        "suite": "Phase3 M6.7.3 Restore Dry-run Verification Smoke",
        "status": "FAIL",
        "checks": [],
    }

    bdir = latest_backup_dir()
    if not bdir:
        result["checks"].append({
            "name": "latest backup exists",
            "status": "FAIL",
        })
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    result["backup_dir"] = str(bdir)
    result["checks"].append({
        "name": "latest backup exists",
        "status": "PASS",
    })

    proc = subprocess.run(
        ["hermes-memory-restore", str(bdir), "--dry-run"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    ok = proc.returncode == 0 and "status=PASS" in proc.stdout

    result["restore_command"] = {
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-1200:],
        "stderr_tail": proc.stderr[-1200:],
    }

    result["checks"].append({
        "name": "restore dry-run exits 0 and status PASS",
        "status": "PASS" if ok else "FAIL",
    })

    result["status"] = "PASS" if ok else "FAIL"
    result["failed"] = 0 if ok else 1
    result["total"] = len(result["checks"])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
