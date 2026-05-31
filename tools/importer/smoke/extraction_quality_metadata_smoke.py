from pathlib import Path
import json
import subprocess
import sys

ROOT = Path.home() / "workspace/hermes-memory"
IMPORTER = ROOT / "tools/importer"


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


proc = subprocess.run(
    [
        sys.executable,
        "answer_generator.py",
        "Telegram integration 是什麼？",
        "--project", "k6-freelancer",
        "--path", "services.md",
        "--heading", "Telegram",
        "--max-tokens", "768",
        "--json",
    ],
    cwd=IMPORTER,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if proc.returncode != 0:
    print(proc.stdout)
    print(proc.stderr)
    fail("answer_generator failed")

try:
    data = json.loads(proc.stdout)
except Exception as e:
    print(proc.stdout)
    fail(f"invalid JSON: {e}")

required = [
    "selected_model_profile",
    "extraction_path",
    "reasoning_fallback_used",
    "finish_reason",
    "extraction_quality_ok",
    "extraction_quality_issues",
    "retry_recommended",
    "answer_chars",
]

for key in required:
    if key not in data:
        fail(f"missing key: {key}")

if data["selected_model_profile"] != "qwen-forced-thinking":
    fail(f"unexpected selected_model_profile: {data['selected_model_profile']}")

if not isinstance(data["extraction_quality_issues"], list):
    fail("extraction_quality_issues must be a list")

if not data.get("answer"):
    fail("answer is empty")

if data.get("answer_chars", 0) <= 0:
    fail("answer_chars must be positive")

print(json.dumps({
    "suite": "M8.5.2b Extraction Quality Metadata Smoke",
    "status": "PASS",
    "selected_model_profile": data.get("selected_model_profile"),
    "extraction_path": data.get("extraction_path"),
    "reasoning_fallback_used": data.get("reasoning_fallback_used"),
    "finish_reason": data.get("finish_reason"),
    "extraction_quality_ok": data.get("extraction_quality_ok"),
    "extraction_quality_issues": data.get("extraction_quality_issues"),
    "retry_recommended": data.get("retry_recommended"),
    "answer_chars": data.get("answer_chars"),
}, ensure_ascii=False, indent=2))
