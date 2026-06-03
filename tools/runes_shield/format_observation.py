#!/usr/bin/env python3

import json

from observe_health import observe_health


def format_observation():
    data = observe_health()

    runtime_ok = all(item["exists"] for item in data["runtime_files"])
    docs_ok = all(item["exists"] for item in data["system_docs"])

    lines = [
        "Runes Shield Runtime: PASS" if data["status"] == "PASS" else "Runes Shield Runtime: WARN",
        f"Runtime files: {'healthy' if runtime_ok else 'missing files detected'}",
        f"System docs: {'healthy' if docs_ok else 'missing docs detected'}",
        f"Write authority: {'disabled' if data['write'] is False else 'enabled'}",
        "Observation mode: read-only",
    ]

    boundary = data.get("boundary", {})

    for key, value in boundary.items():
        lines.append(f"{key}: {str(value).lower()}")

    return {
        "status": data["status"],
        "write": False,
        "summary_lines": lines,
        "raw": data,
    }


def main():
    print(json.dumps(format_observation(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
