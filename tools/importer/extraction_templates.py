from typing import List, Optional


PROFILE_MARKERS = {
    "qwen-forced-thinking": [
        "Draft Answer (Internal Refinement - Traditional Chinese):",
        "Draft Answer:",
        "Final Answer:",
        "Synthesize Answer",
    ],

    "gemma-clean-structured": [
        "Final Answer:",
    ],

    "llama-instruction-following": [
        "Final Answer:",
    ],
}


STOP_MARKERS = [
    "\n5.  **Check against Rules",
    "\n6.  **Check against Rules",
    "\n[Output Generation]",
    "\nSelf-Correction",
    "\nThe draft looks solid",
]


def extract_from_reasoning(
    reasoning: str,
    profile_name: str,
) -> Optional[str]:
    reasoning = reasoning or ""

    markers: List[str] = PROFILE_MARKERS.get(profile_name, [])

    matches = []

    for marker in markers:
        idx = reasoning.rfind(marker)
        if idx >= 0:
            matches.append((idx, marker))

    if not matches:
        return None

    matches.sort(reverse=True)

    for idx, marker in matches:
        text = reasoning[idx + len(marker):].strip()

        for stop in STOP_MARKERS:
            if stop in text:
                text = text.split(stop, 1)[0].strip()

        # Remove leading markdown bullets / separators.
        text = text.lstrip(":*- \n").strip()

        if text:
            return text

    return None


if __name__ == "__main__":
    sample = """
4.  Draft Answer (Internal Refinement - Traditional Chinese):
Telegram integration 是 Hermes Agent 的入口通道 [Source 1]。

5.  Check against Rules:
"""

    print(
        extract_from_reasoning(
            sample,
            "qwen-forced-thinking",
        )
    )
