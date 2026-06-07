from pathlib import Path
import json
import subprocess
import sys

ROOT = Path.home() / "workspace/hermes-memory"
IMPORTER = ROOT / "tools/importer"


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run(cmd):
    proc = subprocess.run(
        cmd,
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        fail(f"command failed: {' '.join(cmd)}")
    return proc.stdout


# 1. Static profile smoke.
out = run([sys.executable, "model_profiles.py"])
expected = {
    "Qwen3.6-35B-A3B -> qwen-forced-thinking",
    "gemma-3-27b-it -> gemma-clean-structured",
    "llama-3.3-70b-instruct -> llama-instruction-following",
    "unknown-model -> default",
}
missing = [line for line in expected if line not in out]
if missing:
    fail(f"profile matcher missing expected output: {missing}")


# 2. Live answer_generator metadata smoke.
out = run([
    sys.executable,
    "answer_generator.py",
    "Telegram integration 是什麼？",
    "--project", "k6-freelancer",
    "--path", "services.md",
    "--heading", "Telegram",
    "--max-tokens", "768",
    "--json",
])

try:
    data = json.loads(out)
except Exception as e:
    print(out)
    fail(f"answer_generator did not return valid JSON: {e}")

if data.get("selected_model_profile") != "qwen-forced-thinking":
    fail(f"unexpected selected_model_profile: {data.get('selected_model_profile')}")

if "extraction_path" not in data:
    fail("missing extraction_path")

if "reasoning_fallback_used" not in data:
    fail("missing reasoning_fallback_used")

if "finish_reason" not in data:
    fail("missing finish_reason")

if not data.get("answer"):
    fail("answer is empty")

print(json.dumps({
    "suite": "M8.4.6 Multi-model Governance Smoke",
    "status": "PASS",
    "selected_model_profile": data.get("selected_model_profile"),
    "extraction_path": data.get("extraction_path"),
    "reasoning_fallback_used": data.get("reasoning_fallback_used"),
    "finish_reason": data.get("finish_reason"),
    "answer_preview": data.get("answer", "")[:120],
}, ensure_ascii=False, indent=2))
