#!/usr/bin/env python3

import json

from dispatch_invocation import dispatch
from observe_health import observe_health


def main():
    print("== M36 Observe Handler Smoke ==")

    health = observe_health()
    print(json.dumps(health, indent=2, ensure_ascii=False))

    if health["status"] != "PASS":
        raise SystemExit("observe health must pass")

    if health["write"] is not False:
        raise SystemExit("observe health write flag must remain false")

    dispatched = dispatch("MATCH")
    print(json.dumps(dispatched, indent=2, ensure_ascii=False))

    if dispatched["handler"] != "observe":
        raise SystemExit("MATCH must dispatch to observe handler")

    if dispatched["write"] is not False:
        raise SystemExit("dispatcher write flag must remain false")

    if dispatched.get("observation", {}).get("status") != "PASS":
        raise SystemExit("dispatcher observation payload must pass")

    print("PASS: observe handler validation completed")


if __name__ == "__main__":
    main()
