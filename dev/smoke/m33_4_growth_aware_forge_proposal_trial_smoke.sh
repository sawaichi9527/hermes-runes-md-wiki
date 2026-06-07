#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.4 Growth-Aware Forge Proposal Trial Smoke =="

tool="tools/runes/growth_aware_forge_proposal.py"

echo "[1/8] growth-aware proposal helper exists"
test -f "$tool" || { echo "FAIL missing $tool"; fail=1; }
test -x "$tool" || { echo "FAIL helper is not executable"; fail=1; }

echo "[2/8] green / stable recommendation"
python3 "$tool" \
  --path wiki/k6-freelancer/services.md \
  --incoming-summary "新增 Telegram 操作知識" \
  --json >/tmp/m33_4_green.json || {
    echo "FAIL green recommendation failed"
    fail=1
  }

python3 - <<'PY' || exit 10
import json
from pathlib import Path

data = json.loads(Path("/tmp/m33_4_green.json").read_text(encoding="utf-8"))

assert data["schema"] == "m33_growth_aware_forge_proposal_trial_v1"
assert data["readiness"]["growth_zone"] == "green"
assert data["readiness"]["rune_state"] == "stable"
assert data["proposal_strategy"] == "targeted_section_patch"
assert data["placement"] == "existing_markdown_source"
assert data["direct_append_allowed"] is True
assert data["split_required"] is False
assert data["should_warn_user"] is False
assert "section patch" in data["recommendation_zh"]
assert "proposal / review / controlled apply" in data["recommendation_zh"]

print(json.dumps({
    "zone": data["readiness"]["growth_zone"],
    "strategy": data["proposal_strategy"],
    "placement": data["placement"],
}, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL green validation failed"
  fail=1
fi

echo "[3/8] yellow / heated recommendation"
python3 "$tool" \
  --path wiki/k6-freelancer/file-header-metadata-standard.md \
  --incoming-summary "新增 metadata header 規則" \
  --json >/tmp/m33_4_yellow.json || {
    echo "FAIL yellow recommendation failed"
    fail=1
  }

python3 - <<'PY' || exit 11
import json
from pathlib import Path

data = json.loads(Path("/tmp/m33_4_yellow.json").read_text(encoding="utf-8"))

assert data["readiness"]["growth_zone"] == "yellow"
assert data["readiness"]["rune_state"] == "heated"
assert data["proposal_strategy"] == "new_topic_file_or_targeted_section_patch"
assert data["placement"] == "prefer_new_topic_file"
assert data["direct_append_allowed"] is False
assert data["split_required"] is False
assert data["should_warn_user"] is True
assert "不建議 broad append" in data["recommendation_zh"]
assert "獨立 topic file" in data["recommendation_zh"]
assert "section patch" in data["recommendation_zh"]

print(json.dumps({
    "zone": data["readiness"]["growth_zone"],
    "strategy": data["proposal_strategy"],
    "placement": data["placement"],
}, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL yellow validation failed"
  fail=1
fi

echo "[4/8] red / overloaded synthetic recommendation"
python3 "$tool" \
  --synthetic-zone red \
  --path wiki/k6-freelancer/large-overloaded-example.md \
  --incoming-summary "新增大型混合主題知識" \
  --json >/tmp/m33_4_red.json || {
    echo "FAIL red recommendation failed"
    fail=1
  }

python3 - <<'PY' || exit 12
import json
from pathlib import Path

data = json.loads(Path("/tmp/m33_4_red.json").read_text(encoding="utf-8"))

assert data["readiness"]["growth_zone"] == "red"
assert data["readiness"]["rune_state"] == "overloaded"
assert data["readiness"]["refinement_level"] == "+8"
assert data["proposal_strategy"] == "split_proposal_or_new_topic_file"
assert data["placement"] == "avoid_existing_markdown_source"
assert data["direct_append_allowed"] is False
assert data["split_required"] is True
assert data["should_warn_user"] is True
assert "過載符文" in data["agent_guidance_zh"]
assert "split proposal" in data["recommendation_zh"]
assert "不建議繼續直接鑄入新知識" in data["recommendation_zh"]

print(json.dumps({
    "zone": data["readiness"]["growth_zone"],
    "strategy": data["proposal_strategy"],
    "placement": data["placement"],
    "split_required": data["split_required"],
}, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL red validation failed"
  fail=1
fi

echo "[5/8] governance boundaries remain explicit"
python3 - <<'PY' || exit 13
import json
from pathlib import Path

for p in ["/tmp/m33_4_green.json", "/tmp/m33_4_yellow.json", "/tmp/m33_4_red.json"]:
    data = json.loads(Path(p).read_text(encoding="utf-8"))
    gb = data["governance_boundary"]
    assert gb["decision_support_only"] is True
    assert gb["permission_grant"] is False
    assert gb["automatic_approval"] is False
    assert gb["automatic_promotion"] is False
    assert gb["human_review_required"] is True
    assert gb["controlled_apply_required"] is True
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL governance boundary validation failed"
  fail=1
fi

echo "[6/8] helper depends on forge readiness signal"
grep -q "markdown_source_health.py" "$tool" || {
  echo "FAIL helper does not reference markdown_source_health.py"
  fail=1
}
grep -q "Runes Shield Forge Readiness Check" "$tool" || {
  echo "FAIL helper does not preserve readiness concept"
  fail=1
}

echo "[7/8] helper is trial-only and read-only"
if grep -qE "INSERT|UPDATE|DELETE|psycopg|sqlite3|open\\(.+['\"]w" "$tool"; then
  echo "FAIL helper appears to contain write/database operation"
  fail=1
fi

grep -q "trial" "$tool" || {
  echo "FAIL helper does not identify itself as trial"
  fail=1
}

echo "[8/8] no secret-like output"
if grep -RInE 'API_KEY|TOKEN|PASSWORD|SECRET|postgresql://|TELEGRAM' \
  /tmp/m33_4_green.json /tmp/m33_4_yellow.json /tmp/m33_4_red.json \
  >/tmp/m33_4_secret_scan.txt 2>/dev/null; then
  echo "FAIL output appears to contain secret-like strings"
  cat /tmp/m33_4_secret_scan.txt
  fail=1
fi

if [ "$fail" = "0" ]; then
  echo "PASS: M33.4 Growth-Aware Forge Proposal Trial smoke"
else
  echo "FAIL: M33.4 Growth-Aware Forge Proposal Trial smoke"
  exit 1
fi
