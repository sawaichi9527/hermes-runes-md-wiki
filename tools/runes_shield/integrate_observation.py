#!/usr/bin/env python3

import argparse
import json

from dispatch_invocation import dispatch
from format_observation import format_observation


def integrate(state):
    dispatched = dispatch(state)

    if dispatched["handler"] == "observe" and dispatched["status"] == "PASS":
        formatted = format_observation()

        return {
            "status": "PASS",
            "state": dispatched["state"],
            "handler": "observe",
            "write": False,
            "response_type": "governed_observation",
            "summary_lines": formatted["summary_lines"],
            "dispatch": dispatched,
        }

    if dispatched["handler"] == "confirm":
        return {
            "status": "CONFIRM_REQUIRED",
            "state": dispatched["state"],
            "handler": "confirm",
            "write": False,
            "response_type": "confirmation_challenge",
            "summary_lines": [dispatched["summary"]],
            "dispatch": dispatched,
        }

    return {
        "status": "BYPASS",
        "state": dispatched["state"],
        "handler": "none",
        "write": False,
        "response_type": "normal_handling",
        "summary_lines": [dispatched["summary"]],
        "dispatch": dispatched,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run the invocation-to-observation integration path."
    )
    parser.add_argument("state", help="Invocation state, e.g. MATCH")
    args = parser.parse_args()

    print(json.dumps(integrate(args.state), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
