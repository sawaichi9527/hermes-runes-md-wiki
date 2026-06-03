#!/usr/bin/env python3

import json
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "tool_boundary",
    "write_default",
    "entries",
    "reserved",
}

REQUIRED_ENTRY_KEYS = {
    "id",
    "state",
    "tool",
    "routing_enabled",
    "write",
    "requires_confirmation",
    "authority",
    "risk",
    "allowed_outputs",
    "blocked_behaviors",
    "notes",
}

ALLOWED_STATES = {
    "MATCH",
    "CONFIRM",
    "CONFIRM_MATCH",
    "NO_MATCH",
}


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_registry(data):
    missing = REQUIRED_TOP_LEVEL_KEYS - set(data.keys())

    if missing:
        raise ValueError(f"missing top-level keys: {sorted(missing)}")

    entries = data.get("entries", [])

    if not isinstance(entries, list) or not entries:
        raise ValueError("entries must be a non-empty list")

    seen_states = set()

    for entry in entries:
        missing_entry = REQUIRED_ENTRY_KEYS - set(entry.keys())

        if missing_entry:
            raise ValueError(
                f"entry missing keys: {sorted(missing_entry)}"
            )

        state = entry["state"]

        if state not in ALLOWED_STATES:
            raise ValueError(f"invalid state: {state}")

        seen_states.add(state)

        if entry["write"] is not False:
            raise ValueError(
                f"write flag must remain false in P0 registry: {entry['id']}"
            )

    if seen_states != ALLOWED_STATES:
        raise ValueError(
            f"registry states mismatch: {sorted(seen_states)}"
        )

    return {
        "status": "PASS",
        "entries": len(entries),
        "states": sorted(seen_states),
        "write_default": data["write_default"],
    }


if __name__ == "__main__":
    registry = load_registry()
    result = validate_registry(registry)

    print(json.dumps(result, indent=2, ensure_ascii=False))
