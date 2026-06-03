#!/usr/bin/env python3

import argparse
import json

from adapt_conversation import adapt


def render_text(adapted):
    state = adapted["classified_state"]
    result = adapted["result"]
    response_type = result["response_type"]

    if response_type == "governed_observation":
        lines = [
            "Runes Shield runtime observation completed.",
            "",
        ]
        lines.extend(f"- {line}" for line in result["summary_lines"])
        lines.extend(
            [
                "",
                f"Invocation state: {state}",
                "Write authority: disabled",
            ]
        )
        return "\n".join(lines)

    if response_type == "confirmation_challenge":
        confirmation_text = result.get(
            "confirmation_text",
            "Explicit confirmation is required before continuing.",
        )
        return "\n".join(
            [
                confirmation_text,
                "",
                f"Invocation state: {state}",
                "Write authority: disabled",
            ]
        )

    return "\n".join(
        [
            "No Runes Shield invocation was selected.",
            "The message should continue through normal assistant handling.",
            "",
            f"Invocation state: {state}",
            "Write authority: disabled",
        ]
    )


def render(message, pending_confirmation=False):
    adapted = adapt(message, pending_confirmation=pending_confirmation)

    return {
        "status": adapted["status"],
        "classified_state": adapted["classified_state"],
        "response_type": adapted["result"]["response_type"],
        "write": False,
        "text": render_text(adapted),
        "adapted": adapted,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Render a Runes Shield conversation response."
    )
    parser.add_argument("message", help="User message to adapt and render")
    parser.add_argument(
        "--pending-confirmation",
        action="store_true",
        help="Treat this message as a reply to a pending confirmation challenge",
    )
    args = parser.parse_args()

    print(
        json.dumps(
            render(args.message, pending_confirmation=args.pending_confirmation),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
