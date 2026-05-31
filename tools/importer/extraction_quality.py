import re
from typing import Any, Dict, List


TERMINAL_MARKS = ("。", "！", "？", ".", "!", "?")


def evaluate_extraction_quality(
    answer: str,
    finish_reason: str = "",
    extraction_path: str = "",
    reasoning_fallback_used: bool = False,
) -> Dict[str, Any]:
    answer = (answer or "").strip()
    finish_reason = finish_reason or ""
    extraction_path = extraction_path or ""

    quality_issues: List[str] = []
    risk_signals: List[str] = []

    if not answer:
        quality_issues.append("answer_empty")

    if finish_reason == "length":
        risk_signals.append("finish_reason_length")

    if reasoning_fallback_used:
        risk_signals.append("reasoning_fallback_used")

    if answer:
        if not answer.endswith(TERMINAL_MARKS):
            quality_issues.append("ends_mid_sentence")

        if re.search(r"\s*\[$", answer) or re.search(r"\s*\[Source\s*\d*$", answer):
            quality_issues.append("dangling_citation")

        if re.search(r"(\*\*|__|~~|`)$", answer):
            quality_issues.append("dangling_markdown")

        if len(answer) < 40:
            risk_signals.append("suspicious_short_answer")

    ok = len(quality_issues) == 0

    return {
        "ok": ok,
        "quality_issues": quality_issues,
        "risk_signals": risk_signals,
        "issues": quality_issues + risk_signals,  # backward-compatible field
        "finish_reason": finish_reason,
        "extraction_path": extraction_path,
        "reasoning_fallback_used": reasoning_fallback_used,
        "answer_chars": len(answer),
    }


if __name__ == "__main__":
    import json

    samples = [
        {
            "name": "good",
            "answer": "Telegram integration 是 Hermes Agent 的入口通道。",
            "finish_reason": "stop",
            "extraction_path": "message.content",
            "reasoning_fallback_used": False,
        },
        {
            "name": "length_but_complete",
            "answer": "Telegram integration 是 Hermes Agent 的入口通道。",
            "finish_reason": "length",
            "extraction_path": "message.content",
            "reasoning_fallback_used": False,
        },
        {
            "name": "length_mid_sentence",
            "answer": "Telegram integration 是 Hermes Agent 的入口通道，主要用於讓已批准的 Telegram",
            "finish_reason": "length",
            "extraction_path": "reasoning_content.synthesize_answer",
            "reasoning_fallback_used": True,
        },
        {
            "name": "dangling_citation",
            "answer": "Telegram integration 是 Hermes Agent 的入口通道 [Source",
            "finish_reason": "length",
            "extraction_path": "reasoning_content.draft_response",
            "reasoning_fallback_used": True,
        },
    ]

    for sample in samples:
        result = evaluate_extraction_quality(
            answer=sample["answer"],
            finish_reason=sample["finish_reason"],
            extraction_path=sample["extraction_path"],
            reasoning_fallback_used=sample["reasoning_fallback_used"],
        )
        print(json.dumps({"sample": sample["name"], **result}, ensure_ascii=False))
