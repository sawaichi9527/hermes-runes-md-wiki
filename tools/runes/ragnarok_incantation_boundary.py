#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from typing import Any

CORE_PATTERNS = [
    r"諸神的黃昏",
    r"\bragnarok\b",
]

ACTIVATION_HINTS = [
    r"開始",
    r"啟動",
    r"進入",
    r"開",
    r"跑",
    r"詠唱",
    r"讓.*hermes",
    r"來吧",
]

RUNTIME_CONTEXT_HINTS = [
    r"hermes",
    r"shield",
    r"world tree",
    r"世界樹",
    r"observation",
    r"bundle",
    r"觀測",
    r"封包",
    r"diagnostic",
    r"log",
    r"observe",
    r"wiki",
    r"runes",
]

NON_MATCH_CONTEXTS = [
    r"ragnarok online",
    r"仙境傳說",
    r"北歐神話",
    r"動畫",
    r"電影",
    r"漫畫",
    r"遊戲",
]

CONFIRMATION_RESPONSES = [
    r"是",
    r"來吧",
    r"開始",
    r"啟動",
    r"確認",
    r"進行",
]


def any_match(patterns: list[str], text: str) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)


def classify(text: str, prior_confirmation_pending: bool = False) -> dict[str, Any]:
    normalized = text.strip()

    has_core = any_match(CORE_PATTERNS, normalized)
    has_activation = any_match(ACTIVATION_HINTS, normalized)
    has_runtime = any_match(RUNTIME_CONTEXT_HINTS, normalized)
    has_non_match = any_match(NON_MATCH_CONTEXTS, normalized)

    if has_non_match:
        return {
            "status": "NO_MATCH",
            "reason": "non_runes_context",
            "invoke_bundle": False,
        }

    if prior_confirmation_pending:
        if any_match(CONFIRMATION_RESPONSES, normalized):
            return {
                "status": "CONFIRM_MATCH",
                "reason": "confirmation_response_after_pending_state",
                "invoke_bundle": True,
            }

        return {
            "status": "NO_MATCH",
            "reason": "confirmation_not_received",
            "invoke_bundle": False,
        }

    if has_core and has_activation and has_runtime:
        return {
            "status": "MATCH",
            "reason": "core_incantation_with_runtime_context",
            "invoke_bundle": True,
        }

    if has_core and has_activation:
        return {
            "status": "CONFIRM",
            "reason": "core_incantation_without_clear_runtime_context",
            "invoke_bundle": False,
            "ritual_confirmation_zh": "少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？",
        }

    return {
        "status": "NO_MATCH",
        "reason": "insufficient_incantation_signal",
        "invoke_bundle": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="M33.7 Ragnarok incantation boundary trial.")
    parser.add_argument("text")
    parser.add_argument("--confirmation-pending", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = classify(args.text, prior_confirmation_pending=args.confirmation_pending)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["status"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
