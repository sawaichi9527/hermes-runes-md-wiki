import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from extraction_quality import evaluate_extraction_quality


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


good = evaluate_extraction_quality(
    answer="Telegram integration 是 Hermes Agent 的入口通道。",
    finish_reason="stop",
    extraction_path="message.content",
    reasoning_fallback_used=False,
)

if good["ok"] is not True:
    fail(f"good sample should be ok: {good}")

mid = evaluate_extraction_quality(
    answer="Telegram integration 是 Hermes Agent 的入口通道，主要用於讓已批准的 Telegram",
    finish_reason="length",
    extraction_path="reasoning_content.synthesize_answer",
    reasoning_fallback_used=True,
)

for issue in ("finish_reason_length", "ends_mid_sentence", "reasoning_fallback_used"):
    if issue not in mid["issues"]:
        fail(f"missing {issue}: {mid}")

if mid["retry_recommended"] is not True:
    fail(f"mid sample should recommend retry: {mid}")

dangling = evaluate_extraction_quality(
    answer="Telegram integration 是 Hermes Agent 的入口通道 [Source",
    finish_reason="length",
    extraction_path="reasoning_content.draft_response",
    reasoning_fallback_used=True,
)

if "dangling_citation" not in dangling["issues"]:
    fail(f"dangling sample should detect dangling_citation: {dangling}")

print("PASS: M8.5.1 extraction quality checker smoke")
