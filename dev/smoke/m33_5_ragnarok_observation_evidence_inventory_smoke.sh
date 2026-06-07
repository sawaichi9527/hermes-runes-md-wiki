#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.5 Ragnarok Observation Evidence Inventory Smoke =="

inventory="wiki/_system/ragnarok_observation_evidence_inventory.md"
policy="wiki/_system/ragnarok_observation_bundle_policy.md"
readme="wiki/_system/README.md"

echo "[1/8] inventory file exists"
test -f "$inventory" || { echo "FAIL missing $inventory"; fail=1; }

echo "[2/8] core concepts exist"
grep -q "Ragnarok Observation Evidence Inventory" "$inventory" || { echo "FAIL missing inventory title"; fail=1; }
grep -q "Ragnarok Observation Bundle" "$inventory" || { echo "FAIL missing Ragnarok Observation Bundle"; fail=1; }
grep -q "World Tree" "$inventory" || { echo "FAIL missing World Tree"; fail=1; }
grep -q "Markdown Source Health is one branch" "$inventory" || { echo "FAIL missing one-branch clarification"; fail=1; }

echo "[3/8] evidence categories exist"
for pattern in \
  "Repository State" \
  "Smoke and Verification Results" \
  "Operations Metadata" \
  "Observation Summaries" \
  "Reports" \
  "Markdown Source Health" \
  "Tool and Runtime Inventory" \
  "Bundle Metadata"
do
  grep -q "$pattern" "$inventory" || { echo "FAIL missing evidence category: $pattern"; fail=1; }
done

echo "[4/8] allowed evidence examples exist"
grep -q "git status --short" "$inventory" || { echo "FAIL missing git status example"; fail=1; }
grep -q "hermes-memory-smoke" "$inventory" || { echo "FAIL missing hermes-memory-smoke example"; fail=1; }
grep -q "operation count by type" "$inventory" || { echo "FAIL missing operations summary example"; fail=1; }
grep -q "reports/m33-markdown-source-health/latest.json" "$inventory" || { echo "FAIL missing source health report example"; fail=1; }
grep -q "refinement level" "$inventory" || { echo "FAIL missing refinement level"; fail=1; }

echo "[5/8] secret exclusions exist"
for pattern in \
  ".env" \
  "API keys" \
  "PostgreSQL passwords" \
  "Telegram bot tokens" \
  "raw full prompts" \
  "raw full answers" \
  "raw full memory context" \
  "database dumps" \
  "vector embeddings" \
  "shell history"
do
  grep -q "$pattern" "$inventory" || { echo "FAIL missing exclusion: $pattern"; fail=1; }
done

echo "[6/8] local output and relationship boundaries exist"
grep -q "bundles/ragnarok-observation/<timestamp>/" "$inventory" || { echo "FAIL missing local bundle output"; fail=1; }
grep -q "~/Downloads/hermes-runes-ragnarok-observation-<timestamp>.tar.gz" "$inventory" || { echo "FAIL missing optional Downloads output"; fail=1; }
grep -q "ragnarok_observation_bundle_policy.md" "$inventory" || { echo "FAIL missing relationship to policy"; fail=1; }
grep -q "not the full bundle scope" "$inventory" || { echo "FAIL missing source health scope boundary"; fail=1; }

echo "[7/8] README indexes inventory"
grep -q "ragnarok_observation_evidence_inventory.md" "$readme" || { echo "FAIL README missing inventory index"; fail=1; }
grep -q "Runes Markdown Source Health is one evidence branch" "$readme" || { echo "FAIL README missing source health branch boundary"; fail=1; }

echo "[8/8] policy and inventory both exist"
grep -q "Ragnarok Incantation Boundary" "$policy" || { echo "FAIL policy missing incantation boundary"; fail=1; }
grep -q "canonical ritual confirmation phrase" "$readme" || { echo "FAIL README missing ritual confirmation reference"; fail=1; }

if [ "$fail" = "0" ]; then
  echo "PASS: M33.5 Ragnarok Observation Evidence Inventory smoke"
else
  echo "FAIL: M33.5 Ragnarok Observation Evidence Inventory smoke"
  exit 1
fi
