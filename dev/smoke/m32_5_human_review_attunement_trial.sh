#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M32.5 Human Review / Attunement Trial =="

approved="wiki/k6-freelancer/forge-inbox/m20-2-agent-proposal-write-trial-forge-20260601-224400-aa10dfd9.md"
draft="wiki/k6-freelancer/forge-inbox/m22-1-m22-1-manual-draft-proposal-test-20260602-063134-a831adf4fc.md"

echo "[1/7] proposal evidence files exist"
test -f "$approved" || { echo "FAIL missing approved proposal evidence"; fail=1; }
test -f "$draft" || { echo "FAIL missing draft proposal evidence"; fail=1; }

echo "[2/7] approved proposal carries human review metadata"
grep -q "status: approved" "$approved" || { echo "FAIL approved proposal status missing"; fail=1; }
grep -q "trust_class: reviewed" "$approved" || { echo "FAIL approved proposal trust_class reviewed missing"; fail=1; }
grep -q "reviewed_by: human" "$approved" || { echo "FAIL approved proposal reviewed_by human missing"; fail=1; }

echo "[3/7] draft proposal remains untrusted"
grep -q "status: draft" "$draft" || { echo "FAIL draft proposal status missing"; fail=1; }
grep -q "trusted_memory: false" "$draft" || { echo "FAIL draft trusted_memory false missing"; fail=1; }
grep -q "Human approval required: true" "$draft" || { echo "FAIL draft human approval requirement missing"; fail=1; }
grep -q "Agent may approve: false" "$draft" || { echo "FAIL draft agent approval prohibition missing"; fail=1; }
grep -q "Agent may promote: false" "$draft" || { echo "FAIL draft agent promotion prohibition missing"; fail=1; }

echo "[4/7] reviewed proposal does not claim trusted wiki mutation"
if grep -qiE "trusted_memory:[[:space:]]*true|trusted wiki mutation:[[:space:]]*yes|direct wiki mutation" "$approved"; then
  echo "FAIL approved proposal appears to claim direct trusted mutation"
  fail=1
fi

echo "[5/7] attunement / review guidance exists"
grep -qiE "human|approval|review|attunement|調律" wiki/_system/runes_agent_guidance.md || {
  echo "FAIL runes_agent_guidance lacks review/attunement language"
  fail=1
}

grep -qiE "proposal|forge|draft|trusted" wiki/_system/runes_agent_guidance.md || {
  echo "FAIL runes_agent_guidance lacks proposal/trusted boundary language"
  fail=1
}

echo "[6/7] promotion governance smoke remains PASS"
(
  cd tools/importer
  if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source ".venv/bin/activate"
  fi
  python promotion_governance_smoke.py >/tmp/m32_5_promotion_governance_smoke.json
)

grep -q '"status": "PASS"' /tmp/m32_5_promotion_governance_smoke.json || {
  echo "FAIL promotion governance smoke did not PASS"
  cat /tmp/m32_5_promotion_governance_smoke.json
  fail=1
}

echo "[7/7] no new trusted wiki mutation required for review trial"
git diff --quiet || {
  echo "FAIL working tree has unstaged changes before commit"
  fail=1
}

if [ "$fail" = "0" ]; then
  echo "PASS: M32.5 human review / attunement trial"
else
  echo "FAIL: M32.5 human review / attunement trial"
  exit 1
fi
