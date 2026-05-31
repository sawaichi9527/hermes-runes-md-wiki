import re
from typing import Dict, Any


def validate_retry_answer(answer: str) -> Dict[str, Any]:
    answer = (answer or "").strip()

    issues = []

    if not answer:
        issues.append("retry_answer_empty")

    if len(answer) < 20:
        issues.append("retry_answer_too_short")

    if re.fullmatch(r"\[Source\s+\d+\]", answer):
        issues.append("citation_only_answer")

    if re.fullmatch(r"\s*", answer):
        issues.append("blank_answer")

    ok = len(issues) == 0

    return {
        "ok": ok,
        "issues": issues,
        "answer_chars": len(answer),
    }


if __name__ == "__main__":
    import json

    samples = [
        "Telegram integration 是 Hermes Agent 的入口通道 [Source 1]。",
        "[Source 1]",
        "",
    ]

    for s in samples:
        print(json.dumps({
            "answer": s,
            **validate_retry_answer(s),
        }, ensure_ascii=False))
