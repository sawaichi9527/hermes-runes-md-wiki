#!/usr/bin/env python3

import argparse
import json

from resolve_route import resolve_route


def handle_observe(route):
    return {
        "status": "PASS",
        "handler": "observe",
        "state": route["state"],
        "route_id": route["route_id"],
        "write": False,
        "summary": "Observation handler selected. No write authority granted.",
        "allowed_outputs": route["allowed_outputs"],
        "blocked_behaviors": route["blocked_behaviors"],
    }


def handle_confirm(route):
    return {
        "status": "CONFIRM_REQUIRED",
        "handler": "confirm",
        "state": route["state"],
        "route_id": route["route_id"],
        "write": False,
        "summary": "Confirmation handler selected. Explicit human confirmation required.",
        "allowed_outputs": route["allowed_outputs"],
        "blocked_behaviors": route["blocked_behaviors"],
    }


def handle_none(route):
    return {
        "status": "BYPASS",
        "handler": "none",
        "state": route["state"],
        "route_id": route["route_id"],
        "write": False,
        "summary": "No Runes Shield handler selected. Continue normal assistant handling.",
        "allowed_outputs": route["allowed_outputs"],
        "blocked_behaviors": route["blocked_behaviors"],
    }


def dispatch(state):
    route = resolve_route(state)

    if route["write"] is not False:
        return {
            "status": "BLOCKED",
            "handler": "none",
            "state": route["state"],
            "route_id": route["route_id"],
            "write": False,
            "summary": "Route blocked because write authority is not allowed in P0 dispatcher.",
            "allowed_outputs": [],
            "blocked_behaviors": ["write_route_dispatch"],
        }

    tool = route["tool"]

    if tool == "observe":
        return handle_observe(route)

    if tool == "confirm":
        return handle_confirm(route)

    return handle_none(route)


def main():
    parser = argparse.ArgumentParser(
        description="Dispatch a Runes Shield invocation state to a minimal handler."
    )
    parser.add_argument("state", help="Invocation state, e.g. MATCH")
    args = parser.parse_args()

    result = dispatch(args.state)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
