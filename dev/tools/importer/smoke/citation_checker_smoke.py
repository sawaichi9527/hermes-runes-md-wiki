import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from citation_checker import evaluate_citation_integrity


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


good = evaluate_citation_integrity(
    answer="Telegram integration 是入口通道 [Source 1]。",
    selected_chunks_count=1,
)

if good["ok"] is not True:
    fail(f"good citation should pass: {good}")

bad = evaluate_citation_integrity(
    answer="Telegram integration [Source 3]",
    selected_chunks_count=1,
)

if "invalid_citation_reference" not in bad["issues"]:
    fail(f"invalid citation not detected: {bad}")

missing = evaluate_citation_integrity(
    answer="Telegram integration 是入口通道。",
    selected_chunks_count=1,
)

if "missing_citation" not in missing["issues"]:
    fail(f"missing citation not detected: {missing}")

print("PASS: M9.3a citation checker smoke")
