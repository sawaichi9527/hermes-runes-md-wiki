#!/usr/bin/env python3

import json

from format_observation import format_observation


def main():
    print("== M36.1 Observation Formatter Smoke ==")

    data = format_observation()

    print(json.dumps(data, indent=2, ensure_ascii=False))

    if data["status"] != "PASS":
        raise SystemExit("formatter status must pass")

    if data["write"] is not False:
        raise SystemExit("formatter write flag must remain false")

    if not data["summary_lines"]:
        raise SystemExit("summary lines must not be empty")

    print("PASS: observation formatter validation completed")


if __name__ == "__main__":
    main()
