#!/usr/bin/env python3
import subprocess
import sys

SUITES = [
    ["python", "smoke/eval_smoke_m5_2.py"],
    ["python", "smoke/eval_smoke_m6_6.py"],
    ["python", "smoke/eval_smoke_m6_7_2_backup.py"],
    ["python", "smoke/eval_smoke_m6_7_3_restore.py"],
    ["python", "smoke/eval_smoke_m7_2_tool_runner.py"],
]

failed = 0

for cmd in SUITES:
    print(f"\n=== RUN: {' '.join(cmd)} ===")
    rc = subprocess.call(cmd)
    if rc != 0:
        failed += 1

print(f"\nsummary: failed={failed} total={len(SUITES)}")
sys.exit(1 if failed else 0)
