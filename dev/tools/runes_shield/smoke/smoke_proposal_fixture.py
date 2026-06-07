#!/usr/bin/env python3

import json

from validate_proposal_fixture import validate_fixture


def main():
    print("== M37.2 Proposal Fixture Smoke ==")

    result = validate_fixture()

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] != "PASS":
        raise SystemExit("proposal fixture validation must pass")

    if result["write"] is not False:
        raise SystemExit("write flag must remain false")

    if result["blocked_status_detected"]:
        raise SystemExit("blocked status must not be detected")

    if not result["allowed_status_validation"]:
        raise SystemExit("status must remain within allowed draft states")

    if not result["role_validation"]:
        raise SystemExit("role validation must pass")

    print("PASS: proposal fixture validation completed")


if __name__ == "__main__":
    main()
