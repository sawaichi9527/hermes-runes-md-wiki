#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M31.4 Archive Move Lock Smoke =="

echo "[1/5] root milestone shell archive count"
shell_count="$(find archive/root-milestone-shell -maxdepth 1 -type f -name '*.sh' | wc -l)"
test "$shell_count" = "13" || { echo "FAIL shell_count=$shell_count expected=13"; fail=1; }

echo "[2/5] root has no active m24/m25/m26 shell"
root_count="$(find . -maxdepth 1 -type f \( -name 'm24_*.sh' -o -name 'm25_*.sh' -o -name 'm26_*.sh' \) | wc -l)"
test "$root_count" = "0" || { echo "FAIL root_count=$root_count expected=0"; fail=1; }

echo "[3/5] archived milestone python tools exist"
py_count="$(find tools/archive/milestone-shell -maxdepth 1 -type f -name '*.py' | wc -l)"
test "$py_count" -ge "23" || { echo "FAIL py_count=$py_count expected>=23"; fail=1; }

echo "[4/5] active runes tree has no archived milestone-era tools"
active_count="$(find tools/runes -maxdepth 1 -type f | grep -E 'm21|m22|m23|m24|m25|m26|import_refresh_m28_2|offer_policy' | wc -l || true)"
test "$active_count" = "0" || { echo "FAIL active_count=$active_count expected=0"; fail=1; }

echo "[5/5] archive README exists"
test -f tools/archive/milestone-shell/README.md || { echo "FAIL missing tools/archive/milestone-shell/README.md"; fail=1; }

if [ "$fail" = "0" ]; then
  echo "PASS: M31.4 archive move lock smoke"
else
  echo "FAIL: M31.4 archive move lock smoke"
  exit 1
fi
