#!/usr/bin/env python3

import json

from load_registry import load_registry, validate_registry


def build_discovery(registry):
    validation = validate_registry(registry)

    tools = []

    for entry in registry["entries"]:
        tool = entry["tool"]

        if tool == "none":
            continue

        tools.append(
            {
                "name": tool,
                "authority": entry["authority"],
                "write": entry["write"],
                "routing_enabled": entry["routing_enabled"],
                "requires_confirmation": entry["requires_confirmation"],
                "risk": entry["risk"],
                "allowed_outputs": entry["allowed_outputs"],
            }
        )

    unique_tools = []
    seen = set()

    for tool in tools:
        key = tool["name"]

        if key in seen:
            continue

        seen.add(key)
        unique_tools.append(tool)

    return {
        "status": "PASS",
        "tool_boundary": registry["tool_boundary"],
        "discovery_version": "m35.1-p0",
        "schema_version": registry["schema_version"],
        "write_default": registry["write_default"],
        "validation": validation,
        "tools": unique_tools,
        "reserved": registry.get("reserved", []),
    }


def main():
    registry = load_registry()
    discovery = build_discovery(registry)

    print(json.dumps(discovery, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
