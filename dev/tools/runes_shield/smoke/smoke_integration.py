#!/usr/bin/env python3

import json

from integrate_observation import integrate


EXPECTED = {
    "MATCH": "governed_observation",
    "CONFIRM": "confirmation_challenge",
    "NO_MATCH": "normal_handling",
}


def main():
    print("== M36.2 Integration Smoke ==")

    for state, expected in EXPECTED.items():
        data = integrate(state)

        print(json.dumps(data, indent=2, ensure_ascii=False))

        if data["response_type"] != expected:
            raise SystemExit(
                f"unexpected response type for {state}: {data['response_type']}"
            )

        if data["write"] is not False:
            raise SystemExit(
                f"write flag must remain false: {state}"
            )

        if not data["summary_lines"]:
            raise SystemExit(
                f"summary lines missing: {state}"
            )

    print("PASS: invocation integration validation completed")


if __name__ == "__main__":
    main()
