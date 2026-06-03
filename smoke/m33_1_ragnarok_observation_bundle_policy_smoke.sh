#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.1 Ragnarok Observation Bundle Policy Smoke =="

policy="wiki/_system/ragnarok_observation_bundle_policy.md"
readme="wiki/_system/README.md"

echo "[1/9] policy file exists"
test -f "$policy" || { echo "FAIL missing $policy"; fail=1; }

echo "[2/9] formal concept names exist"
grep -q "Ragnarok Observation Bundle" "$policy" || { echo "FAIL missing Ragnarok Observation Bundle"; fail=1; }
grep -q "諸神的黃昏觀測封包" "$policy" || { echo "FAIL missing Chinese bundle name"; fail=1; }
grep -q "Ragnarok Incantation Boundary" "$policy" || { echo "FAIL missing incantation boundary"; fail=1; }

echo "[3/9] required core incantation exists"
grep -q "諸神的黃昏" "$policy" || { echo "FAIL missing 諸神的黃昏"; fail=1; }
grep -q "Ragnarok" "$policy" || { echo "FAIL missing Ragnarok"; fail=1; }

echo "[4/9] activation intent examples exist"
grep -q "啟動" "$policy" || { echo "FAIL missing 啟動"; fail=1; }
grep -q "詠唱" "$policy" || { echo "FAIL missing 詠唱"; fail=1; }
grep -q "開 Ragnarok" "$policy" || { echo "FAIL missing 開 Ragnarok"; fail=1; }
grep -q "跑 Ragnarok" "$policy" || { echo "FAIL missing 跑 Ragnarok"; fail=1; }

echo "[5/9] non-match contexts exist"
grep -q "Ragnarok Online" "$policy" || { echo "FAIL missing game non-match example"; fail=1; }
grep -q "北歐神話" "$policy" || { echo "FAIL missing mythology non-match example"; fail=1; }
grep -q "collect logs" "$policy" || { echo "FAIL missing generic diagnostic non-trigger"; fail=1; }

echo "[6/9] ritual confirmation phrase exists"
grep -q "少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？" "$policy" || {
  echo "FAIL missing canonical ritual confirmation phrase"
  fail=1
}

echo "[7/9] world tree semantics exist"
grep -q "World Tree" "$policy" || { echo "FAIL missing World Tree"; fail=1; }
grep -q "Shaking the World Tree" "$policy" || { echo "FAIL missing Shaking the World Tree"; fail=1; }
grep -q "震動世界樹" "$policy" || { echo "FAIL missing 震動世界樹"; fail=1; }

echo "[8/9] safety boundaries exist"
grep -q "not.*security boundary" "$policy" || { echo "FAIL missing not security boundary"; fail=1; }
grep -q "must not include" "$policy" || { echo "FAIL missing exclusion section"; fail=1; }
grep -q "API keys" "$policy" || { echo "FAIL missing API key exclusion"; fail=1; }
grep -q "PostgreSQL passwords" "$policy" || { echo "FAIL missing PostgreSQL password exclusion"; fail=1; }
grep -q "raw full prompts" "$policy" || { echo "FAIL missing raw prompt exclusion"; fail=1; }

echo "[9/9] README indexes policy"
grep -q "ragnarok_observation_bundle_policy.md" "$readme" || { echo "FAIL README missing policy index"; fail=1; }
grep -q "少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？" "$readme" || {
  echo "FAIL README missing confirmation phrase"
  fail=1
}

if [ "$fail" = "0" ]; then
  echo "PASS: M33.1 Ragnarok Observation Bundle policy lock"
else
  echo "FAIL: M33.1 Ragnarok Observation Bundle policy lock"
  exit 1
fi
