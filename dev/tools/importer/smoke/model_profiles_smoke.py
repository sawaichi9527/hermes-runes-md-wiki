from pathlib import Path
import sys
import yaml

ROOT = Path.home() / "workspace/hermes-memory"
CONFIG = ROOT / "config/model_profiles.yaml"

required_profiles = {
    "qwen-forced-thinking",
    "gemma-clean-structured",
    "llama-instruction-following",
    "default",
}

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

if not CONFIG.exists():
    fail(f"missing {CONFIG}")

data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))

if data.get("version") != 1:
    fail("version must be 1")

profiles = data.get("profiles")
if not isinstance(profiles, dict):
    fail("profiles must be a dict")

missing = required_profiles - set(profiles)
if missing:
    fail(f"missing profiles: {sorted(missing)}")

for name, profile in profiles.items():
    if "behavior" not in profile:
        fail(f"{name}: missing behavior")
    if "extraction" not in profile:
        fail(f"{name}: missing extraction")

    extraction = profile["extraction"]
    for key in [
        "strip_think_blocks",
        "prefer_final_content",
        "allow_reasoning_fallback",
        "max_reasoning_fallback_chars",
    ]:
        if key not in extraction:
            fail(f"{name}: missing extraction.{key}")

qwen = profiles["qwen-forced-thinking"]["extraction"]
if qwen["allow_reasoning_fallback"] is not True:
    fail("qwen-forced-thinking must allow reasoning fallback")

default = profiles["default"]["extraction"]
if default["allow_reasoning_fallback"] is not False:
    fail("default must not allow reasoning fallback")

print("PASS: M8.4 model profile baseline config is valid")
