#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M33.6 Ragnarok Observation Bundle MVP Smoke =="

tool="tools/runes/ragnarok_observation_bundle.py"
bundle_id="smoke-m33-6"

echo "[1/9] bundle generator exists"
test -f "$tool" || { echo "FAIL missing $tool"; fail=1; }
test -x "$tool" || { echo "FAIL generator is not executable"; fail=1; }

echo "[2/9] bundles path is git-ignored"
grep -q "bundles/ragnarok-observation/" .gitignore || {
  echo "FAIL bundles/ragnarok-observation/ is not ignored"
  fail=1
}

echo "[3/9] generate deterministic smoke bundle"
rm -rf "bundles/ragnarok-observation/$bundle_id"

python3 "$tool" --bundle-id "$bundle_id" --json >/tmp/m33_6_bundle_result.json || {
  echo "FAIL bundle generation failed"
  cat /tmp/m33_6_bundle_result.json
  fail=1
}

bundle_path="$(python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/m33_6_bundle_result.json").read_text(encoding="utf-8"))
print(data["path"])
PY
)"

test "$bundle_path" = "bundles/ragnarok-observation/$bundle_id" || {
  echo "FAIL unexpected bundle path: $bundle_path"
  fail=1
}

test -d "$bundle_path" || {
  echo "FAIL missing generated bundle directory: $bundle_path"
  fail=1
}

echo "[4/9] required bundle files exist"
for file in \
  "$bundle_path/bundle-metadata.json" \
  "$bundle_path/repository-state/status-short.txt" \
  "$bundle_path/repository-state/status-branch.txt" \
  "$bundle_path/repository-state/log-oneline-20.txt" \
  "$bundle_path/repository-state/tracked-files.txt" \
  "$bundle_path/repository-state/repository-summary.json" \
  "$bundle_path/smoke-verification/smoke-script-inventory.json" \
  "$bundle_path/smoke-verification/known-lock-smokes.json" \
  "$bundle_path/reports/reports-inventory.json" \
  "$bundle_path/reports/m33-markdown-source-health/latest.json" \
  "$bundle_path/reports/m33-markdown-source-health/latest.md" \
  "$bundle_path/operations-summary/operations-summary.json" \
  "$bundle_path/observation-summary/observation-summary.json" \
  "$bundle_path/tool-runtime-inventory/tool-runtime-inventory.json"
do
  test -f "$file" || { echo "FAIL missing bundle file: $file"; fail=1; }
done

echo "[5/9] metadata schema and exclusions are valid"
python3 - <<'PY' || exit 10
import json
from pathlib import Path

meta = json.loads(Path("bundles/ragnarok-observation/smoke-m33-6/bundle-metadata.json").read_text(encoding="utf-8"))

assert meta["schema"] == "m33_ragnarok_observation_bundle_mvp_v1"
assert meta["bundle_id"] == "smoke-m33-6"
assert meta["profile"] == "ragnarok-observation-mvp"
assert meta["local_only"] is True
assert meta["secret_exclusion_required"] is True

excluded = set(meta["excluded_by_policy"])
for item in [
    ".env",
    "API keys",
    "PostgreSQL passwords",
    "Telegram bot tokens",
    "raw full prompts",
    "raw full answers",
    "raw full memory context",
    "database dumps",
    "vector embeddings",
    "shell history",
    "unrestricted raw logs",
]:
    assert item in excluded, item

included = set(meta["included_categories"])
for item in [
    "repository_state",
    "smoke_verification_inventory",
    "operations_metadata_summary",
    "observation_summary",
    "reports_inventory_and_selected_reports",
    "markdown_source_health_reports",
    "tool_runtime_inventory",
    "bundle_metadata",
]:
    assert item in included, item

print("metadata_ok")
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL metadata validation failed"
  fail=1
fi

echo "[6/9] summaries are metadata-only"
python3 - <<'PY' || exit 11
import json
from pathlib import Path

ops = json.loads(Path("bundles/ragnarok-observation/smoke-m33-6/operations-summary/operations-summary.json").read_text(encoding="utf-8"))
obs = json.loads(Path("bundles/ragnarok-observation/smoke-m33-6/observation-summary/observation-summary.json").read_text(encoding="utf-8"))

assert "metadata summary only" in ops["note"]
assert "summary only" in obs["note"]

for forbidden in ["prompt", "answer", "context", "messages"]:
    assert forbidden not in ops, forbidden
    assert forbidden not in obs, forbidden

print("summary_only_ok")
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL summary-only validation failed"
  fail=1
fi

echo "[7/9] source health report is included as one branch"
python3 - <<'PY' || exit 12
import json
from pathlib import Path

health = json.loads(Path("bundles/ragnarok-observation/smoke-m33-6/reports/m33-markdown-source-health/latest.json").read_text(encoding="utf-8"))
assert health["schema"] == "m33_markdown_source_health_audit_v1"
assert health["summary"]["files_scanned"] > 0
assert "files" in health
print("source_health_branch_ok")
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "FAIL source health branch validation failed"
  fail=1
fi

echo "[8/9] generated bundle remains untracked"
if git ls-files "$bundle_path" | grep -q .; then
  echo "FAIL generated bundle should not be tracked"
  git ls-files "$bundle_path"
  fail=1
fi

if git status --short --ignored "$bundle_path" | grep -q '^??'; then
  echo "FAIL generated bundle appears unignored"
  git status --short --ignored "$bundle_path"
  fail=1
fi

echo "[9/9] secret-like scan of bundle"
if grep -RInE 'API_KEY|TOKEN|PASSWORD|SECRET|postgresql://|TELEGRAM_BOT|HF_TOKEN' "$bundle_path" >/tmp/m33_6_secret_scan.txt 2>/dev/null; then
  echo "FAIL bundle appears to contain secret-like strings"
  cat /tmp/m33_6_secret_scan.txt
  fail=1
fi

if [ "$fail" = "0" ]; then
  echo "PASS: M33.6 Ragnarok Observation Bundle MVP smoke"
else
  echo "FAIL: M33.6 Ragnarok Observation Bundle MVP smoke"
  exit 1
fi
