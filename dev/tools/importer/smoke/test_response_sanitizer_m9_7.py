import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from response_sanitizer import sanitize_answer


def check(name, raw, expected):
    got = sanitize_answer(raw)
    if got != expected:
        raise AssertionError(f"{name}\nEXPECTED:\n{expected!r}\nGOT:\n{got!r}")
    print(f"PASS: {name}")


check(
    "citation normalization",
    "Telegram integration 是入口 [Source1]",
    "Telegram integration 是入口 [Source 1]",
)

check(
    "strip artifact lines",
    "Draft:\nTelegram integration 是入口 [Source1]\nin Traditional Chinese:",
    "Telegram integration 是入口 [Source 1]",
)

check(
    "trim check against rules",
    "正式回答 [Source1]\n\n4. Check against Rules:\n不要輸出這段",
    "正式回答 [Source 1]",
)

check(
    "trim final review",
    "正式回答 [Source2]\n\nFinal Review:\nmeta review",
    "正式回答 [Source 2]",
)

check(
    "duplicated regenerated answer",
    "第一版回答完成 [Source1]\n\nDraft:\n第二版回答不應保留 [Source1]",
    "第一版回答完成 [Source 1]",
)

print("M9.7 response sanitizer smoke: PASS")
