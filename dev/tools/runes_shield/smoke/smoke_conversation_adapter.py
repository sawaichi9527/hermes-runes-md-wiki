#!/usr/bin/env python3

import json

from adapt_conversation import adapt


CASES = [
    {
        "id": "match",
        "message": "詠唱諸神的黃昏，開啟世界樹，交給 Hermes Runes 記憶系統處理",
        "pending": False,
        "state": "MATCH",
        "response_type": "governed_observation",
    },
    {
        "id": "confirm",
        "message": "詠唱諸神的黃昏，開啟世界樹",
        "pending": False,
        "state": "CONFIRM",
        "response_type": "confirmation_challenge",
    },
    {
        "id": "confirm_match",
        "message": "確定",
        "pending": True,
        "state": "CONFIRM_MATCH",
        "response_type": "governed_observation",
    },
    {
        "id": "no_match_fiction",
        "message": "請介紹北歐神話裡的諸神的黃昏與世界樹",
        "pending": False,
        "state": "NO_MATCH",
        "response_type": "normal_handling",
    },
    {
        "id": "no_match_generic",
        "message": "檢查一般系統狀態",
        "pending": False,
        "state": "NO_MATCH",
        "response_type": "normal_handling",
    },
]


def main():
    print("== M36.3 Conversation Adapter Smoke ==")

    for case in CASES:
        data = adapt(case["message"], pending_confirmation=case["pending"])

        print(json.dumps(data, indent=2, ensure_ascii=False))

        if data["classified_state"] != case["state"]:
            raise SystemExit(
                f"{case['id']} state mismatch: {data['classified_state']}"
            )

        if data["result"]["response_type"] != case["response_type"]:
            raise SystemExit(
                f"{case['id']} response mismatch: {data['result']['response_type']}"
            )

        if data["write"] is not False:
            raise SystemExit(f"{case['id']} write flag must remain false")

    print("PASS: conversation adapter validation completed")


if __name__ == "__main__":
    main()
