#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.3 Runes Shield Forge Readiness Check Smoke =="

tool="tools/runes/markdown_source_health.py"

stable_path="wiki/k6-freelancer/services.md"
heated_path="wiki/k6-freelancer/file-header-metadata-standard.md"

echo "[1/8] readiness helper exists"
test -f "$tool" || { echo "FAIL missing $tool"; fail=1; }
test -x "$tool" || { echo "FAIL helper is not executable"; fail=1; }

echo "[2/8] stable rune JSON signal works"
python3 "$tool" --path "$stable_path" --json >/tmp/m33_3_stable.json || {
  echo "FAIL stable rune query failed"
  fail=1
}

python3 - <<'PY' || exit 10
import json
from pathlib import Path

data = json.loads(Path("/tmp/m33_3_stable.json").read_text(encoding="utf-8"))

assert data["schema"] == "m33_runes_shield_forge_readiness_v1"
assert data["check"] == "Runes Shield Forge Readiness Check"
assert data["display_name_zh"] == "Runes 符文鑄造前適性檢查"
assert data["health_subject"] == "markdown_source"
assert data["path"] == "wiki/k6-freelancer/services.md"
assert data["growth_zone"] == "green"
assert data["rune_state"] == "stable"
assert data["rune_state_label_zh"] == "穩定符文"
assert data["risk_level"] == "low"
assert data["refinement_level"].startswith("+")
assert data["recommended_write_behavior"] == "section_patch_ok_small_append_ok"
assert "符文附魔已達" in data["agent_guidance_zh"]
assert "proposal / review / controlled apply" in data["agent_guidance_zh"]

gb = data["governance_boundary"]
assert gb["decision_support_only"] is True
assert gb["permission_grant"] is False
assert gb["automatic_approval"] is False
assert gb["automatic_promotion"] is False
assert gb["human_review_required"] is True

print(json.dumps({
    "path": data["path"],
    "growth_zone": data["growth_zone"],
    "refinement_level": data["refinement_level"],
    "rune_state": data["rune_state"],
}, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL stable rune JSON validation failed"
  fail=1
fi

echo "[3/8] heated rune JSON signal works"
python3 "$tool" --path "$heated_path" --json >/tmp/m33_3_heated.json || {
  echo "FAIL heated rune query failed"
  fail=1
}

python3 - <<'PY' || exit 11
import json
from pathlib import Path

data = json.loads(Path("/tmp/m33_3_heated.json").read_text(encoding="utf-8"))

assert data["schema"] == "m33_runes_shield_forge_readiness_v1"
assert data["path"] == "wiki/k6-freelancer/file-header-metadata-standard.md"
assert data["growth_zone"] == "yellow"
assert data["refinement_level"] == "+4"
assert data["rune_state"] == "heated"
assert data["rune_state_label_zh"] == "熾熱符文"
assert data["risk_level"] == "medium"
assert data["recommended_write_behavior"] == "avoid_broad_append_prefer_new_topic_file_or_targeted_section_patch"
assert "符文品質下降" in data["agent_guidance_zh"]
assert "召回精準度" in data["agent_guidance_zh"]
assert "避免 broad append" in data["agent_guidance_zh"]
assert data["source_health"]["level_components"]["headings"] == 4

print(json.dumps({
    "path": data["path"],
    "growth_zone": data["growth_zone"],
    "refinement_level": data["refinement_level"],
    "rune_state": data["rune_state"],
    "level_components": data["source_health"]["level_components"],
}, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL heated rune JSON validation failed"
  fail=1
fi

echo "[4/8] text guidance mode works"
python3 "$tool" --path "$heated_path" >/tmp/m33_3_heated_text.txt || {
  echo "FAIL heated text mode failed"
  fail=1
}

grep -q "符文附魔已達 +4 精練狀態" /tmp/m33_3_heated_text.txt || {
  echo "FAIL text guidance missing refinement phrase"
  fail=1
}
grep -q "熾熱符文" /tmp/m33_3_heated_text.txt || {
  echo "FAIL text guidance missing heated rune label"
  fail=1
}

echo "[5/8] source health metrics are included"
python3 - <<'PY' || exit 12
import json
from pathlib import Path

for p in ["/tmp/m33_3_stable.json", "/tmp/m33_3_heated.json"]:
    data = json.loads(Path(p).read_text(encoding="utf-8"))
    sh = data["source_health"]
    for key in [
        "size_kb",
        "estimated_tokens_pressure",
        "heading_count",
        "chunk_estimate",
        "largest_heading_span_lines",
        "largest_heading_span_est_tokens",
        "level_components",
    ]:
        assert key in sh, key
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL source health metrics missing"
  fail=1
fi

echo "[6/8] policy concept is documented"
grep -q "Runes Shield Forge Readiness Check" wiki/_system/runes_markdown_source_health.md || {
  echo "FAIL concept policy missing readiness check"
  fail=1
}
grep -q "Runes 符文鑄造前適性檢查" wiki/_system/runes_markdown_source_health.md || {
  echo "FAIL concept policy missing Chinese readiness check"
  fail=1
}

echo "[7/8] helper uses audit layer and stays read-only"
grep -q "markdown_source_health_audit.py" "$tool" || {
  echo "FAIL helper does not reference audit tool"
  fail=1
}

if grep -qE "INSERT|UPDATE|DELETE|psycopg|sqlite3|open\\(.+['\"]w" "$tool"; then
  echo "FAIL helper appears to contain write/database operation"
  fail=1
fi

echo "[8/8] no secret-like output"
if grep -RInE 'API_KEY|TOKEN|PASSWORD|SECRET|postgresql://|TELEGRAM' /tmp/m33_3_stable.json /tmp/m33_3_heated.json /tmp/m33_3_heated_text.txt >/tmp/m33_3_secret_scan.txt 2>/dev/null; then
  echo "FAIL readiness output appears to contain secret-like strings"
  cat /tmp/m33_3_secret_scan.txt
  fail=1
fi

if [ "$fail" = "0" ]; then
  echo "PASS: M33.3 Runes Shield Forge Readiness Check smoke"
else
  echo "FAIL: M33.3 Runes Shield Forge Readiness Check smoke"
  exit 1
fi
