import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retry_policy import decide_retry


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


ok_with_risk = decide_retry(
    quality={
        "ok": True,
        "quality_issues": [],
        "risk_signals": ["finish_reason_length", "reasoning_fallback_used"],
    },
    selected_model_profile="qwen-forced-thinking",
)

if ok_with_risk["retry_should_run"] is not False:
    fail(f"quality-ok risk signal should not retry: {ok_with_risk}")

if ok_with_risk["retry_reason"] != "quality_ok_with_risk_signals":
    fail(f"unexpected retry_reason: {ok_with_risk}")

mid_sentence = decide_retry(
    quality={
        "ok": False,
        "quality_issues": ["ends_mid_sentence"],
        "risk_signals": ["finish_reason_length"],
    },
    selected_model_profile="qwen-forced-thinking",
)

if mid_sentence["retry_should_run"] is not True:
    fail(f"mid-sentence should retry: {mid_sentence}")

if mid_sentence["retry_mode"] != "compact_reask":
    fail(f"unexpected retry_mode: {mid_sentence}")

limit = decide_retry(
    quality={
        "ok": False,
        "quality_issues": ["ends_mid_sentence"],
        "risk_signals": ["finish_reason_length"],
    },
    selected_model_profile="qwen-forced-thinking",
    retry_count=1,
    max_retries=1,
)

if limit["retry_should_run"] is not False:
    fail(f"retry limit should stop retry: {limit}")

print("PASS: M8.5.2c retry policy smoke")
