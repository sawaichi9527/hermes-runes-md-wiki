#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.2b Markdown Source Granularity Audit Smoke =="

tool="tools/runes/markdown_source_health_audit.py"
out_dir="reports/m33-markdown-source-health"
latest_json="$out_dir/latest.json"
latest_md="$out_dir/latest.md"

echo "[1/9] audit tool exists"
test -f "$tool" || { echo "FAIL missing $tool"; fail=1; }
test -x "$tool" || { echo "FAIL tool is not executable"; fail=1; }

echo "[2/9] run audit"
python3 "$tool" >/tmp/m33_2b_audit_stdout.txt || {
  echo "FAIL audit execution failed"
  cat /tmp/m33_2b_audit_stdout.txt
  fail=1
}

echo "[3/9] report files exist"
test -f "$latest_json" || { echo "FAIL missing $latest_json"; fail=1; }
test -f "$latest_md" || { echo "FAIL missing $latest_md"; fail=1; }

echo "[4/9] JSON schema and summary are valid"
python3 - <<'PY' || exit 10
import json
from pathlib import Path

p = Path("reports/m33-markdown-source-health/latest.json")
data = json.loads(p.read_text(encoding="utf-8"))

assert data["schema"] == "m33_markdown_source_health_audit_v1"
assert data["scan_root"] == "wiki"
assert isinstance(data["files"], list)
assert len(data["files"]) > 0

summary = data["summary"]
for key in [
    "files_scanned",
    "green",
    "yellow",
    "red",
    "max_size_kb",
    "max_refinement_level",
]:
    assert key in summary, key

assert summary["files_scanned"] == len(data["files"])
assert summary["green"] + summary["yellow"] + summary["red"] == summary["files_scanned"]
assert summary["max_refinement_level"] >= 0

print(json.dumps(summary, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL JSON schema validation failed"
  fail=1
fi

echo "[5/9] every file has required health fields"
python3 - <<'PY' || exit 11
import json
from pathlib import Path

data = json.loads(Path("reports/m33-markdown-source-health/latest.json").read_text(encoding="utf-8"))

required = [
    "path",
    "size_bytes",
    "size_kb",
    "chars",
    "cjk_chars",
    "estimated_tokens_en",
    "estimated_tokens_cjk",
    "estimated_tokens_pressure",
    "heading_count",
    "chunk_estimate",
    "largest_heading_span_lines",
    "largest_heading_span_est_tokens",
    "level_components",
    "growth_zone",
    "refinement_level",
    "rune_state",
    "recommended_action",
]

for item in data["files"]:
    missing = [key for key in required if key not in item]
    assert not missing, f"{item.get('path')} missing {missing}"
    assert item["growth_zone"] in {"green", "yellow", "red"}
    assert item["rune_state"] in {"stable", "heated", "overloaded"}
    assert str(item["refinement_level"]).startswith("+")
    assert item["recommended_action"]

print(f"validated_files={len(data['files'])}")
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL per-file health field validation failed"
  fail=1
fi

echo "[6/9] markdown report contains interpretation"
grep -q "M33 Markdown Source Health Audit" "$latest_md" || { echo "FAIL markdown title missing"; fail=1; }
grep -q "Stable Rune / 穩定符文" "$latest_md" || { echo "FAIL Stable Rune interpretation missing"; fail=1; }
grep -q "Heated Rune / 熾熱符文" "$latest_md" || { echo "FAIL Heated Rune interpretation missing"; fail=1; }
grep -q "Overloaded Rune / 過載符文" "$latest_md" || { echo "FAIL Overloaded Rune interpretation missing"; fail=1; }
grep -q "This audit is read-only" "$latest_md" || { echo "FAIL read-only statement missing"; fail=1; }

echo "[7/9] single-file JSON query works"
python3 "$tool" --path wiki/k6-freelancer/services.md --json >/tmp/m33_2b_single_file.json || {
  echo "FAIL single-file query failed"
  fail=1
}

python3 - <<'PY' || exit 12
import json
from pathlib import Path

data = json.loads(Path("/tmp/m33_2b_single_file.json").read_text(encoding="utf-8"))
assert data["path"] == "wiki/k6-freelancer/services.md"
assert data["growth_zone"] in {"green", "yellow", "red"}
assert data["refinement_level"].startswith("+")
assert data["rune_state"] in {"stable", "heated", "overloaded"}
assert data["recommended_action"]
print(json.dumps({
    "path": data["path"],
    "growth_zone": data["growth_zone"],
    "refinement_level": data["refinement_level"],
    "rune_state": data["rune_state"],
    "recommended_action": data["recommended_action"],
}, ensure_ascii=False, indent=2))
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL single-file JSON validation failed"
  fail=1
fi

echo "[8/9] audit is positioned as Ragnarok evidence source, not full bundle scope"
grep -q "Ragnarok Observation Bundle" wiki/_system/ragnarok_observation_bundle_policy.md || {
  echo "FAIL Ragnarok policy missing"
  fail=1
}

grep -q "Markdown source health reports" wiki/_system/ragnarok_observation_bundle_policy.md || {
  echo "FAIL Ragnarok policy does not list Markdown source health reports as bundle scope"
  fail=1
}

echo "[9/9] audit did not create tracked operations or secrets"
if git ls-files operations | grep -q .; then
  echo "FAIL operations should remain local-only and untracked"
  git ls-files operations
  fail=1
fi

if grep -RInE 'API_KEY|TOKEN|PASSWORD|SECRET|postgresql://|TELEGRAM' "$out_dir" >/tmp/m33_2b_secret_scan.txt 2>/dev/null; then
  echo "FAIL report appears to contain secret-like strings"
  cat /tmp/m33_2b_secret_scan.txt
  fail=1
fi

if [ "$fail" = "0" ]; then
  echo "PASS: M33.2b Markdown Source Granularity Audit smoke"
else
  echo "FAIL: M33.2b Markdown Source Granularity Audit smoke"
  exit 1
fi
