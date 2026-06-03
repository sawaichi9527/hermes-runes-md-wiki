#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

file="AGENTS.md"

echo "== M32.2 Root Bootstrap Self-Awareness Smoke =="

test -f "$file"

grep -q "Hermes Runes MD Wiki" "$file"
grep -q "first-time AI-agent onboarding" "$file"
grep -q "wiki/hermes_runes_index.md" "$file"
grep -q "wiki/_system/README.md" "$file"
grep -q "Do not treat this root file as the full operating policy" "$file"
grep -q "Runes Shield / governed workflow" "$file"

line_count="$(wc -l < "$file")"
test "$line_count" -le 20 || {
  echo "FAIL: AGENTS.md should remain a short bootstrap pointer, line_count=$line_count"
  exit 1
}

echo "PASS: M32.2 root bootstrap self-awareness key"
