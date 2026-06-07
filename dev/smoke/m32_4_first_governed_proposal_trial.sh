#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M32.4 First P0 Governed Proposal Trial =="

proposal_dir="wiki/k6-freelancer/forge-inbox"

echo "[1/6] forge inbox exists"
test -d "$proposal_dir" || {
  echo "FAIL missing forge inbox"
  fail=1
}

echo "[2/6] governed proposal artifacts exist"

proposal_count="$(
  find "$proposal_dir" -maxdepth 1 -type f -name '*.md' | wc -l
)"

echo "proposal_count=$proposal_count"

test "$proposal_count" -ge 1 || {
  echo "FAIL expected at least one governed proposal artifact"
  fail=1
}

echo "[3/6] proposal artifacts remain outside trusted wiki"

if find wiki/k6-freelancer \
  -maxdepth 1 \
  -type f \
  -name '*proposal*applied*' \
  | grep -q .; then
  echo "FAIL detected suspicious applied proposal artifact"
  fail=1
fi

echo "[4/6] shield discovery chain exists"

test -f AGENTS.md || fail=1
test -f wiki/hermes_runes_index.md || fail=1
test -f wiki/_system/runes_shield_contract.md || fail=1
test -f wiki/_system/runes_agent_guidance.md || fail=1

echo "[5/6] style overlay remains non-authoritative"

grep -qi "style overlay only" wiki/_system/agent-style-overlay.md || {
  echo "FAIL style overlay authority boundary missing"
  fail=1
}

echo "[6/6] proposal flow remains governed"

grep -qiE 'proposal|forge|draft|human|approval|review|trusted' \
  wiki/_system/runes_agent_guidance.md || {
  echo "FAIL governed proposal guidance incomplete"
  fail=1
}

if [ "$fail" = "0" ]; then
  echo "PASS: M32.4 first P0 governed proposal trial"
else
  echo "FAIL: M32.4 first P0 governed proposal trial"
  exit 1
fi
