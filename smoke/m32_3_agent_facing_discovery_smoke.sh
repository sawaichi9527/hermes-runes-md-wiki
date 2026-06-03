#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M32.3 Agent-Facing Runes Shield Discovery Smoke =="

check_file() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo "FAIL missing file: $file"
    fail=1
  fi
}

check_grep() {
  local pattern="$1"
  local file="$2"
  local label="$3"

  if ! grep -qiE "$pattern" "$file"; then
    echo "FAIL missing [$label] in $file"
    fail=1
  fi
}

echo "[1/8] bootstrap files exist"
check_file AGENTS.md
check_file wiki/hermes_runes_index.md
check_file wiki/_system/README.md

echo "[2/8] system guidance files exist"
check_file wiki/_system/runes_shield_contract.md
check_file wiki/_system/runes_invocation_policy.md
check_file wiki/_system/runes_agent_guidance.md
check_file wiki/_system/agent-style-overlay.md
check_file wiki/_system/access-boundary.md
check_file wiki/_system/wiki-operation-policy.md
check_file wiki/_system/security-policy.md

echo "[3/8] root bootstrap points to system discovery"
check_grep 'first-time AI-agent onboarding' AGENTS.md 'first-time onboarding'
check_grep 'wiki/hermes_runes_index\.md' AGENTS.md 'top-level wiki index'
check_grep 'wiki/_system/README\.md' AGENTS.md 'system README'
check_grep 'not.*full operating policy|full operating policy' AGENTS.md 'root is not full policy'

echo "[4/8] top-level index identifies Runes Shield"
check_grep 'Runes Shield|符文護盾' wiki/hermes_runes_index.md 'Runes Shield identity'
check_grep 'wiki/_system' wiki/hermes_runes_index.md 'system policy path'

echo "[5/8] system README indexes required policy files"
check_grep 'runes_shield_contract\.md' wiki/_system/README.md 'shield contract index'
check_grep 'runes_invocation_policy\.md' wiki/_system/README.md 'invocation policy index'
check_grep 'runes_agent_guidance\.md' wiki/_system/README.md 'agent guidance index'
check_grep 'agent-style-overlay\.md' wiki/_system/README.md 'style overlay index'

echo "[6/8] shield contract defines governed boundary"
check_grep 'governed invocation boundary|治理護盾|受控工具介面' wiki/_system/runes_shield_contract.md 'governed invocation boundary'
check_grep '不得|must not|do not' wiki/_system/runes_shield_contract.md 'negative authority boundary'
check_grep 'directly operate|直接操作|直接.*wiki|Markdown wiki' wiki/_system/runes_shield_contract.md 'no direct internal operation'

echo "[7/8] agent guidance separates proposal, approval, and trusted mutation"
check_grep 'proposal|forge|草案|鑄造' wiki/_system/runes_agent_guidance.md 'proposal/forge path'
check_grep 'human|approval|review|調律|approve' wiki/_system/runes_agent_guidance.md 'human review/approval'
check_grep 'trusted|wiki|memory|記憶' wiki/_system/runes_agent_guidance.md 'trusted memory awareness'

echo "[8/8] style overlay is presentation only"
check_grep 'style overlay only' wiki/_system/agent-style-overlay.md 'style only'
check_grep 'does not override|not.*replacement.*soul\.md|soul\.md' wiki/_system/agent-style-overlay.md 'does not override soul'
check_grep 'must not change what Hermes-agent is allowed to do|not.*permission|not.*authority' wiki/_system/agent-style-overlay.md 'style not authority'

if [ "$fail" = "0" ]; then
  echo "PASS: M32.3 agent-facing Runes Shield discovery smoke"
else
  echo "FAIL: M32.3 agent-facing Runes Shield discovery smoke"
  exit 1
fi
