#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.0 Runes Markdown Source Health Concept Smoke =="

policy="wiki/_system/runes_markdown_source_health.md"
readme="wiki/_system/README.md"

echo "[1/7] policy file exists"
test -f "$policy" || { echo "FAIL missing $policy"; fail=1; }

echo "[2/7] formal concept name exists"
grep -q "Runes Markdown Source Health" "$policy" || { echo "FAIL missing Runes Markdown Source Health"; fail=1; }

echo "[3/7] shield readiness concept exists"
grep -q "Runes Shield Forge Readiness Check" "$policy" || { echo "FAIL missing Runes Shield Forge Readiness Check"; fail=1; }
grep -q "Runes 符文鑄造前適性檢查" "$policy" || { echo "FAIL missing Chinese display name"; fail=1; }

echo "[4/7] refinement levels exist"
grep -q "+0.*+3.*Stable Rune" "$policy" || { echo "FAIL missing Stable Rune level"; fail=1; }
grep -q "+4.*+6.*Heated Rune" "$policy" || { echo "FAIL missing Heated Rune level"; fail=1; }
grep -q "+7.*+9.*Overloaded Rune" "$policy" || { echo "FAIL missing Overloaded Rune level"; fail=1; }

echo "[5/7] agent-facing warning language exists"
grep -q "符文附魔已達" "$policy" || { echo "FAIL missing agent-facing template"; fail=1; }
grep -q "符文品質下降" "$policy" || { echo "FAIL missing quality degradation warning"; fail=1; }
grep -q "召回品質劣化" "$policy" || { echo "FAIL missing recall degradation warning"; fail=1; }

echo "[6/7] governance boundary remains explicit"
grep -q "decision support only" "$policy" || { echo "FAIL missing decision support boundary"; fail=1; }
grep -q "permission grant" "$policy" || { echo "FAIL missing permission boundary"; fail=1; }
grep -q "human review" "$policy" || { echo "FAIL missing human review boundary"; fail=1; }

echo "[7/7] system README indexes policy"
grep -q "runes_markdown_source_health.md" "$readme" || { echo "FAIL README does not index policy"; fail=1; }
grep -q "Runes Shield Forge Readiness Check" "$readme" || { echo "FAIL README missing readiness concept"; fail=1; }

if [ "$fail" = "0" ]; then
  echo "PASS: M33.0 Runes Markdown Source Health concept lock"
else
  echo "FAIL: M33.0 Runes Markdown Source Health concept lock"
  exit 1
fi
