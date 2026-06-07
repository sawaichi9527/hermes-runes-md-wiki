#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M32.7 P0 Trial Run Lock =="

echo "[1/9] working tree clean before lock"
git diff --quiet || { echo "FAIL unstaged changes exist"; fail=1; }
git diff --cached --quiet || { echo "FAIL staged changes exist"; fail=1; }

untracked="$(git ls-files --others --exclude-standard)"
if [ -n "$untracked" ]; then
  echo "FAIL untracked files exist:"
  echo "$untracked"
  fail=1
fi

echo "[2/9] M31 final verification baseline"
./smoke/m31_7_final_verification_lock.sh || fail=1

echo "[3/9] M32.1b style overlay boundary"
./smoke/m32_1b_agent_style_overlay_smoke.sh || fail=1

echo "[4/9] M32.1c style overlay extraction audit"
./smoke/m32_1c_style_overlay_extraction_audit_smoke.sh || fail=1

echo "[5/9] M32.2 root bootstrap self-awareness"
./smoke/m32_2_root_bootstrap_self_awareness_smoke.sh || fail=1

echo "[6/9] M32.3 agent-facing discovery"
./smoke/m32_3_agent_facing_discovery_smoke.sh || fail=1

echo "[7/9] M32.4 first governed proposal trial"
./smoke/m32_4_first_governed_proposal_trial.sh || fail=1

echo "[8/9] M32.5 human review / attunement trial"
./smoke/m32_5_human_review_attunement_trial.sh || fail=1

echo "[9/9] M32.6 controlled apply + refresh + recall trial"
./smoke/m32_6_controlled_apply_refresh_recall_trial.sh || fail=1

if [ "$fail" = "0" ]; then
  echo "PASS: M32.7 P0 trial run lock"
else
  echo "FAIL: M32.7 P0 trial run lock"
  exit 1
fi
