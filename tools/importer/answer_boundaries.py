import re


BOUNDARY_PATTERNS = [
    r"\n4\.\s+\*\*Check",
    r"\n5\.\s+\*\*Check",
    r"\n4\.\s+\*\*Final Review",
    r"\n5\.\s+\*\*Final Review",
    r"\nDraft:",
    r"\nThe synthesis looks solid",
    r"\nOutput matches",
    r"\nReady\.?✅?",
    r"\nProceeds\.",
]


def truncate_at_answer_boundary(text: str) -> str:
    text = (text or "").strip()

    cut_positions = []

    for pattern in BOUNDARY_PATTERNS:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            cut_positions.append(m.start())

    if cut_positions:
        text = text[:min(cut_positions)].rstrip()

    return text.strip()


if __name__ == "__main__":
    sample = """
Telegram integration 是 Hermes Agent 的入口通道 [Source 1]。

4.  **Check against Rules:**
- contamination
"""

    print(truncate_at_answer_boundary(sample))
