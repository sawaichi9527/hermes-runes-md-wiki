#!/usr/bin/env python3

import argparse
import json

from load_registry import load_registry, validate_registry


def resolve_route(state):
    state = state.upper()
    registry = load_registry()
    validate_registry(registry)

    for entry in registry["entries"]:
        if entry["state"] == state:
            return {
                "status": "PASS",
                "state": entry["state"],
                "route_id": entry["id"],
                "tool": entry["tool"],
                "routing_enabled": entry["routing_enabled"],
                "authority": entry["authority"],
                "write": entry["write"],
                "requires_confirmation": entry["requires_confirmation"],
                "risk": entry["risk"],
                "allowed_outputs": entry["allowed_outputs"],
                "blocked_behaviors": entry["blocked_behaviors"],
                "notes": entry["notes"],
            }

    return {
        "status": "BLOCKED",
        "state": state,
        "route_id": None,
        "tool": "none",
        "routing_enabled": False,
        "authority": "none",
        "write": False,
        "requires_confirmation": False,
        "risk": "low",
        "allowed_outputs": ["normal_assistant_handling"],
        "blocked_behaviors": ["unknown_state_routing"],
        "notes": "Unknown state is blocked by default.",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Resolve a Runes Shield route from an invocation state."
    )
    parser.add_argument("state", help="Invocation state, e.g. MATCH")
    args = parser.parse_args()

    result = resolve_route(args.state)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
