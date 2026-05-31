#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

IMPORTER_PARENT = Path(__file__).resolve().parents[1]
if str(IMPORTER_PARENT) not in sys.path:
    sys.path.insert(0, str(IMPORTER_PARENT))

from root_resolver import resolve_root, resolve_importer_dir


ROOT = resolve_root()
IMPORTER = resolve_importer_dir()


def main():
    proc = subprocess.run(
        [sys.executable, "observation_summary.py", "--days", "1", "--json"],
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )

    if proc.returncode != 0:
        print(json.dumps({
            "suite": "M11 Observation Summary Smoke Test",
            "status": "FAIL",
            "step": "observation_summary",
            "stderr_tail": proc.stderr[-2000:],
        }, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    data = json.loads(proc.stdout)
    issues = []

    if data.get("suite") != "M11 Observation Summary":
        issues.append("wrong_suite")

    if "records_total" not in data:
        issues.append("missing_records_total")

    if "rates" not in data:
        issues.append("missing_rates")

    if "tuning_candidates" not in data:
        issues.append("missing_tuning_candidates")

    for c in data.get("tuning_candidates", []):
        if c.get("auto_patch") is not False:
            issues.append("candidate_auto_patch_not_false")
            break

    output = {
        "suite": "M11 Observation Summary Smoke Test",
        "status": "FAIL" if issues else "PASS",
        "issues": issues,
        "summary": {
            "records_total": data.get("records_total"),
            "records_valid": data.get("records_valid"),
            "parse_errors": data.get("parse_errors"),
            "candidate_count": len(data.get("tuning_candidates", [])),
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
