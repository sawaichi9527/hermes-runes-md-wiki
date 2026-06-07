#!/usr/bin/env python3
import json
import subprocess
import sys


CASES = [
    {
        "name": "memory.check tool runner",
        "cmd": ["hermes-memory-tool", "memory.check"],
        "expect": {
            "status": "PASS",
            "tool": "memory.check",
            "risk": "low",
            "write": False,
        },
    },
    {
        "name": "memory.restore_dry_run tool runner",
        "cmd": ["hermes-memory-tool", "memory.restore_dry_run"],
        "expect": {
            "status": "PASS",
            "tool": "memory.restore_dry_run",
            "risk": "low",
            "write": False,
        },
    },
]


def run_case(case):
    proc = subprocess.run(
        case["cmd"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    result = {
        "name": case["name"],
        "status": "FAIL",
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-1600:],
        "stderr_tail": proc.stderr[-1600:],
        "failures": [],
    }

    if proc.returncode != 0:
        result["failures"].append("nonzero returncode")
        return result

    try:
        payload = json.loads(proc.stdout)
    except Exception as e:
        result["failures"].append(f"stdout is not valid JSON: {type(e).__name__}")
        return result

    for key, expected in case["expect"].items():
        actual = payload.get(key)
        if actual != expected:
            result["failures"].append(
                f"{key}: expected={expected!r} actual={actual!r}"
            )

    if not isinstance(payload.get("duration_sec"), (int, float)):
        result["failures"].append("duration_sec missing or not numeric")

    if "cmd" not in payload or not isinstance(payload["cmd"], list):
        result["failures"].append("cmd missing or not list")

    if not result["failures"]:
        result["status"] = "PASS"

    return result


def main():
    results = [run_case(case) for case in CASES]
    failed = sum(1 for r in results if r["status"] != "PASS")

    report = {
        "suite": "Phase3 M7.2 Tool Runner Smoke",
        "status": "PASS" if failed == 0 else "FAIL",
        "failed": failed,
        "total": len(results),
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
