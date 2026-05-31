from typing import Any, Dict, List


HARD_RETRY_ISSUES = {
    "answer_empty",
    "ends_mid_sentence",
    "dangling_citation",
    "dangling_markdown",
}


def decide_retry(
    quality: Dict[str, Any],
    selected_model_profile: str = "",
    retry_count: int = 0,
    max_retries: int = 1,
) -> Dict[str, Any]:
    quality_issues: List[str] = quality.get("quality_issues") or []
    risk_signals: List[str] = quality.get("risk_signals") or []
    quality_ok = bool(quality.get("ok"))

    if retry_count >= max_retries:
        return {
            "retry_should_run": False,
            "retry_reason": "retry_limit_reached",
            "retry_mode": "none",
        }

    hard_hits = [issue for issue in quality_issues if issue in HARD_RETRY_ISSUES]

    if hard_hits:
        return {
            "retry_should_run": True,
            "retry_reason": "quality_issue:" + ",".join(hard_hits),
            "retry_mode": "compact_reask",
        }

    if quality_ok:
        if risk_signals:
            return {
                "retry_should_run": False,
                "retry_reason": "quality_ok_with_risk_signals",
                "retry_mode": "none",
            }

        return {
            "retry_should_run": False,
            "retry_reason": "quality_ok",
            "retry_mode": "none",
        }

    return {
        "retry_should_run": False,
        "retry_reason": "no_retry_rule_matched",
        "retry_mode": "none",
    }


if __name__ == "__main__":
    import json

    samples = [
        {
            "name": "ok_length_signal",
            "quality": {
                "ok": True,
                "quality_issues": [],
                "risk_signals": ["finish_reason_length"],
            },
        },
        {
            "name": "mid_sentence",
            "quality": {
                "ok": False,
                "quality_issues": ["ends_mid_sentence"],
                "risk_signals": ["finish_reason_length"],
            },
        },
    ]

    for sample in samples:
        print(json.dumps({
            "sample": sample["name"],
            **decide_retry(sample["quality"], selected_model_profile="qwen-forced-thinking"),
        }, ensure_ascii=False))
