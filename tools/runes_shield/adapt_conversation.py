#!/usr/bin/env python3

import argparse
import json

from integrate_observation import integrate

CONFIRMATION_TEXT = "少年啊，你確定要讓世界樹震動，開啟諸神的黃昏嗎？"

CORE_TERMS = [
    "諸神的黃昏",
    "世界樹",
]

CONTEXT_TERMS = [
    "Hermes Runes",
    "Runes Shield",
    "runes shield",
    "hermes-runes-md-wiki",
    "符文",
    "記憶",
]

ACTIVATION_TERMS = [
    "開啟",
    "啟動",
    "喚起",
    "詠唱",
    "執行",
]

AFFIRM_TERMS = [
    "是",
    "對",
    "確定",
    "確認",
    "go",
    "yes",
    "y",
]

FICTION_TERMS = [
    "神話",
    "遊戲",
    "小說",
    "劇情",
    "角色",
    "God of War",
    "FFXIV",
]


def contains_any(text, terms):
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def classify_message(message, pending_confirmation=False):
    text = message.strip()

    if pending_confirmation and contains_any(text, AFFIRM_TERMS):
        return "CONFIRM_MATCH"

    has_core = all(term in text for term in CORE_TERMS)
    has_context = contains_any(text, CONTEXT_TERMS)
    has_activation = contains_any(text, ACTIVATION_TERMS)
    is_fiction = contains_any(text, FICTION_TERMS)

    if is_fiction:
        return "NO_MATCH"

    if has_core and has_context and has_activation:
        return "MATCH"

    if has_core and has_activation:
        return "CONFIRM"

    return "NO_MATCH"


def adapt(message, pending_confirmation=False):
    state = classify_message(message, pending_confirmation=pending_confirmation)
    result = integrate(state)

    if state == "CONFIRM":
        result["confirmation_text"] = CONFIRMATION_TEXT

    return {
        "status": result["status"],
        "input": message,
        "pending_confirmation": pending_confirmation,
        "classified_state": state,
        "write": False,
        "result": result,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Adapt a user message into the Runes Shield runtime chain."
    )
    parser.add_argument("message", help="User message to classify and route")
    parser.add_argument(
        "--pending-confirmation",
        action="store_true",
        help="Treat this message as a reply to a pending confirmation challenge",
    )
    args = parser.parse_args()

    print(
        json.dumps(
            adapt(args.message, pending_confirmation=args.pending_confirmation),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
