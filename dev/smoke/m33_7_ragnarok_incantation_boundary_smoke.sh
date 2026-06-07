#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.7 Ragnarok Incantation Boundary Smoke =="

tool="tools/runes/ragnarok_incantation_boundary.py"

echo "[1/8] incantation boundary tool exists"
test -f "$tool" || { echo "FAIL missing $tool"; fail=1; }
test -x "$tool" || { echo "FAIL tool is not executable"; fail=1; }

check_status() {
  local text="$1"
  local expected="$2"
  local out="$3"
  shift 3

  python3 "$tool" "$text" "$@" --json > "$out" || {
    echo "FAIL classifier execution failed: $text"
    fail=1
    return
  }

  python3 - "$out" "$expected" <<'PY' || exit 10
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
expected = sys.argv[2]
data = json.loads(path.read_text(encoding="utf-8"))
assert data["status"] == expected, data
print(json.dumps({
    "text_file": str(path),
    "status": data["status"],
    "reason": data["reason"],
    "invoke_bundle": data["invoke_bundle"],
}, ensure_ascii=False, indent=2))
PY
  local rc=$?
  if [ "$rc" != "0" ]; then
    echo "FAIL expected $expected for: $text"
    cat "$out"
    fail=1
  fi
}

echo "[2/8] MATCH requires core + activation + Hermes Runes context"
check_status \
  "Hermes，開始詠唱諸神的黃昏 observation bundle" \
  "MATCH" \
  /tmp/m33_7_match.json

grep -q '"invoke_bundle": true' /tmp/m33_7_match.json || {
  echo "FAIL MATCH should invoke bundle"
  fail=1
}

echo "[3/8] CONFIRM when core + activation but context unclear"
check_status \
  "啟動諸神的黃昏" \
  "CONFIRM" \
  /tmp/m33_7_confirm.json

grep -q "少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？" /tmp/m33_7_confirm.json || {
  echo "FAIL missing canonical ritual confirmation phrase"
  fail=1
}

grep -q '"invoke_bundle": false' /tmp/m33_7_confirm.json || {
  echo "FAIL CONFIRM should not invoke bundle yet"
  fail=1
}

echo "[4/8] CONFIRM_MATCH after pending confirmation"
check_status \
  "來吧" \
  "CONFIRM_MATCH" \
  /tmp/m33_7_confirm_match.json \
  --confirmation-pending

grep -q '"invoke_bundle": true' /tmp/m33_7_confirm_match.json || {
  echo "FAIL CONFIRM_MATCH should invoke bundle"
  fail=1
}

echo "[5/8] accepted flexible Ragnarok variants"
check_status "開 Ragnarok" "CONFIRM" /tmp/m33_7_open_ragnarok.json
check_status "跑 Ragnarok" "CONFIRM" /tmp/m33_7_run_ragnarok.json
check_status "進入諸神的黃昏" "CONFIRM" /tmp/m33_7_enter_twilight.json
check_status "讓 Hermes 詠唱諸神的黃昏" "MATCH" /tmp/m33_7_hermes_chant.json

echo "[6/8] NO_MATCH for mythology / games / fiction context"
check_status "我最近在玩 Ragnarok Online" "NO_MATCH" /tmp/m33_7_ragnarok_online.json
check_status "北歐神話的諸神的黃昏是什麼？" "NO_MATCH" /tmp/m33_7_mythology.json
check_status "電影 Ragnarok 的劇情是什麼？" "NO_MATCH" /tmp/m33_7_movie.json

echo "[7/8] NO_MATCH for generic diagnostic/export requests without core incantation"
check_status "幫我打包觀測資料" "NO_MATCH" /tmp/m33_7_generic_bundle.json
check_status "collect logs" "NO_MATCH" /tmp/m33_7_collect_logs.json
check_status "developer observation bundle" "NO_MATCH" /tmp/m33_7_dev_bundle.json

echo "[8/8] policy documents canonical boundary"
grep -q "Ragnarok Incantation Boundary" wiki/_system/ragnarok_observation_bundle_policy.md || {
  echo "FAIL policy missing incantation boundary"
  fail=1
}
grep -q "少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？" wiki/_system/ragnarok_observation_bundle_policy.md || {
  echo "FAIL policy missing canonical confirmation phrase"
  fail=1
}
grep -q "Mentions of Ragnarok or 諸神的黃昏 in mythology, games, fiction, movies, or unrelated discussion must not trigger this workflow" wiki/_system/ragnarok_observation_bundle_policy.md || {
  echo "FAIL policy missing non-match context rule"
  fail=1
}

if [ "$fail" = "0" ]; then
  echo "PASS: M33.7 Ragnarok Incantation Boundary smoke"
else
  echo "FAIL: M33.7 Ragnarok Incantation Boundary smoke"
  exit 1
fi
