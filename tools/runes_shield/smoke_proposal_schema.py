#!/usr/bin/env python3

import json

from validate_proposal_schema import validate


def main():
    print("== M37.1 Proposal Schema Smoke ==")

    result = validate()

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] != "PASS":
        raise SystemExit("proposal schema validation must pass")

    if result["write"] is not False:
        raise SystemExit("write flag must remain false")

    if result["blocked_status_detected"]:
        raise SystemExit("blocked status must not be detected")

    if not result["role_validation"]:
        raise SystemExit("role validation must pass")

    print("PASS: proposal schema validation completed")


if __name__ == "__main__":
    main()
