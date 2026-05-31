import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extraction_cleanup import cleanup_extracted_answer


def check(name, raw, expected):
    got = cleanup_extracted_answer(raw)
    if got != expected:
        raise AssertionError(f"{name}\nEXPECTED:\n{expected!r}\nGOT:\n{got!r}")
    print(f"PASS: {name}")


check(
    "keep refine output",
    "Draft stuff\n\n4. Refine Output:\n正式回答 [Source 1]",
    "正式回答 [Source 1]",
)

check(
    "drop constraints",
    "正式回答 [Source 1]\n\nCheck against constraints:\ninternal",
    "正式回答 [Source 1]",
)

check(
    "final answer block",
    "internal\n\nFinal Answer:\n最終回答 [Source 1]",
    "最終回答 [Source 1]",
)

print("M9.7a extraction cleanup smoke: PASS")
