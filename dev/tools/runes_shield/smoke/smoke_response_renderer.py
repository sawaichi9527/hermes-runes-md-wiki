#!/usr/bin/env python3

import json

from render_response import render


CASES = [
    {
        "id": "match",
        "message": "詠唱諸神的黃昏，開啟世界樹，交給 Hermes Runes 記憶系統處理",
        "pending": False,
        "state": "MATCH",
        "response_type": "governed_observation",
        "must_contain": "Runes Shield runtime observation completed.",
    },
    {
        "id": "confirm",
        "message": "詠唱諸神的黃昏，開啟世界樹",
        "pending": False,
        "state": "CONFIRM",
        "response_type": "confirmation_challenge",
        "must_contain": "少年啊，你確定要讓世界樹震動",
    },
    {
        "id": "confirm_match",
        "message": "確定",
        "pending": True,
        "state": "CONFIRM_MATCH",
        "response_type": "governed_observation",
        "must_contain": "Runes Shield runtime observation completed.",
    },
    {
        "id": "no_match",
        "message": "請介紹北歐神話裡的諸神的黃昏與世界樹",
        "pending": False,
        "state": "NO_MATCH",
        "response_type": "normal_handling",
        "must_contain": "normal assistant handling",
    },
]


def main():
    print("== M36.4 Response Renderer Smoke ==")

    for case in CASES:
        data = render(case["message"], pending_confirmation=case["pending"])

        print(json.dumps(data, indent=2, ensure_ascii=False))

        if data["classified_state"] != case["state"]:
            raise SystemExit(
                f"{case['id']} state mismatch: {data['classified_state']}"
            )

        if data["response_type"] != case["response_type"]:
            raise SystemExit(
                f"{case['id']} response mismatch: {data['response_type']}"
            )

        if data["write"] is not False:
            raise SystemExit(f"{case['id']} write flag must remain false")

        if case["must_contain"] not in data["text"]:
            raise SystemExit(f"{case['id']} rendered text missing expected phrase")

    print("PASS: response renderer validation completed")


if __name__ == "__main__":
    main()
