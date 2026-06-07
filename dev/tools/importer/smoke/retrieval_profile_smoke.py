import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval_profiles import select_retrieval_profile


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


name, profile = select_retrieval_profile(
    "verification_lookup"
)

if name != "verification_lookup":
    fail(f"wrong profile selected: {name}")

if profile.get("prefer_exact_keyword") is not True:
    fail(f"expected prefer_exact_keyword=true: {profile}")

fallback, profile = select_retrieval_profile(
    "unknown_profile"
)

if fallback != "default":
    fail(f"default fallback failed: {fallback}")

print("PASS: M9.6a retrieval profile smoke")
