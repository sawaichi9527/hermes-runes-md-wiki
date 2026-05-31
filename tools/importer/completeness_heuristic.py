import re
from typing import Dict, Any


SUSPICIOUS_ENDINGS = (
    "：",
    ":",
    "-",
    "*",
    "如下",
    "包括",
    "分為",
)

LIST_TRIGGER_TERMS = (
    "如何",
    "哪些",
    "分別",
    "差異",
    "比較",
    "區分",
    "包含",
    "包括",
)


def evaluate_completeness(
    question: str,
    answer: str,
) -> Dict[str, Any]:
    question = (question or "").strip()
    answer = (answer or "").strip()

    issues = []

    if not answer:
        issues.append("empty_answer")

    # Suspicious abrupt endings.
    for token in SUSPICIOUS_ENDINGS:
        if answer.endswith(token):
            issues.append("suspicious_ending")
            break

    # Looks like list/comparison question but answer too short.
    if any(term in question for term in LIST_TRIGGER_TERMS):
        bullet_count = len(re.findall(r"^\s*[-*]", answer, flags=re.MULTILINE))

        if bullet_count <= 1 and len(answer) < 180:
            issues.append("possibly_incomplete_list_answer")

    # Truncated markdown bullet.
    if re.search(r"\n\s*[-*]\s*$", answer):
        issues.append("dangling_bullet")

    # Truncated citation.
    if re.search(r"\[S(?:o(?:u(?:r(?:c(?:e)?)?)?)?)?$", answer):
        issues.append("dangling_citation")

    ok = len(issues) == 0

    return {
        "ok": ok,
        "issues": issues,
    }


if __name__ == "__main__":
    import json

    samples = [
        {
            "q": "quality issues 與 risk signals 如何區分？",
            "a": "Risk signals 不會自動觸發 retry。",
        },
        {
            "q": "quality issues 與 risk signals 如何區分？",
            "a": "* Risk signals：不會自動觸發 retry。\n*",
        },
        {
            "q": "有哪些類型？",
            "a": "包括：",
        },
    ]

    for s in samples:
        print(json.dumps({
            "question": s["q"],
            "answer": s["a"],
            **evaluate_completeness(s["q"], s["a"]),
        }, ensure_ascii=False))
