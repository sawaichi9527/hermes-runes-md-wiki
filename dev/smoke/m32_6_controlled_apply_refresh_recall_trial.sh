#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M32.6 Controlled Apply + Import Refresh + Recall Verification Trial =="

scenario_file="wiki/k6-freelancer/p0-trial-scenarios.md"
marker_add="M29.1_ADD_KNOWLEDGE_CANONICAL_MARKER"
marker_correction="M29.3_CORRECTION_UPDATE_CANONICAL_MARKER"

echo "[1/8] trusted scenario evidence exists"
test -f "$scenario_file" || { echo "FAIL missing $scenario_file"; fail=1; }
grep -q "$marker_add" "$scenario_file" || { echo "FAIL missing add-knowledge marker"; fail=1; }
grep -q "$marker_correction" "$scenario_file" || { echo "FAIL missing correction marker"; fail=1; }

echo "[2/8] controlled apply operation evidence exists"
apply_count="$(find operations/runes-apply -type f -name '*.json' 2>/dev/null | wc -l || true)"
echo "apply_count=$apply_count"
test "$apply_count" -ge 1 || { echo "FAIL missing controlled apply operation evidence"; fail=1; }

echo "[3/8] importer refresh operation evidence exists"
refresh_count="$(find operations/runes-refresh -type f -name '*.json' 2>/dev/null | wc -l || true)"
echo "refresh_count=$refresh_count"
test "$refresh_count" -ge 1 || { echo "FAIL missing importer refresh operation evidence"; fail=1; }

echo "[4/8] recall verification operation evidence exists"
recall_count="$(find operations/runes-recall-verify -type f -name '*.json' 2>/dev/null | wc -l || true)"
echo "recall_count=$recall_count"
test "$recall_count" -ge 1 || { echo "FAIL missing recall verification operation evidence"; fail=1; }

echo "[5/8] reject/no-promotion evidence exists"
reject_count="$(find operations/runes-reject -type f -name '*.json' 2>/dev/null | wc -l || true)"
echo "reject_count=$reject_count"
test "$reject_count" -ge 1 || { echo "FAIL missing reject/no-promotion evidence"; fail=1; }

echo "[6/8] recall can find controlled apply marker"
./bin/hermes-recall "$marker_add" \
  --project k6-freelancer \
  --path "$scenario_file" \
  --limit 5 \
  --json >/tmp/m32_6_marker_add_recall.json

grep -q "$marker_add" /tmp/m32_6_marker_add_recall.json || {
  echo "FAIL recall did not find add marker"
  cat /tmp/m32_6_marker_add_recall.json
  fail=1
}

echo "[7/8] recall can find correction marker"
./bin/hermes-recall "$marker_correction" \
  --project k6-freelancer \
  --path "$scenario_file" \
  --limit 5 \
  --json >/tmp/m32_6_marker_correction_recall.json

grep -q "$marker_correction" /tmp/m32_6_marker_correction_recall.json || {
  echo "FAIL recall did not find correction marker"
  cat /tmp/m32_6_marker_correction_recall.json
  fail=1
}

echo "[8/8] operations remain local-only"
grep -q '^operations/$' .gitignore || {
  echo "FAIL operations/ is not ignored as local-only"
  fail=1
}

if git ls-files operations | grep -q .; then
  echo "FAIL operations/ should not be tracked"
  git ls-files operations
  fail=1
fi

if [ "$fail" = "0" ]; then
  echo "PASS: M32.6 controlled apply + refresh + recall verification trial"
else
  echo "FAIL: M32.6 controlled apply + refresh + recall verification trial"
  exit 1
fi
