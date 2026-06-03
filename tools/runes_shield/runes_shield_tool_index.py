#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "tools" / "runes_shield" / "runes_shield_tools_index.json"
OUTPUT_CHOICES = ("table", "json")


def load_index():
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def find_tool(tools, name):
    for tool in tools:
        if tool["name"] == name:
            return tool
    return None


def render_tools_table(tools):
    headers = ["name", "risk", "write", "command"]
    rows = [
        [
            tool["name"],
            tool["risk"],
            str(tool["write"]),
            tool["command"],
        ]
        for tool in tools
    ]

    widths = [
        max(len(str(row[index])) for row in [headers] + rows)
        for index in range(len(headers))
    ]

    def fmt(row):
        return "  ".join(
            str(value).ljust(widths[index])
            for index, value in enumerate(row)
        )

    lines = [fmt(headers), fmt(["-" * width for width in widths])]
    lines.extend(fmt(row) for row in rows)
    return "\n".join(lines)


def render_blocked_table(blocked_names):
    return "\n".join(blocked_names)


def emit_json(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Runes Shield read-only tool discovery CLI."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list",
        help="List agent-facing safe tools.",
    )
    list_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Show one tool definition by name.",
    )
    show_parser.add_argument("tool_name")
    show_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )

    blocked_parser = subparsers.add_parser(
        "blocked",
        help="List blocked tool names that must not be exposed.",
    )
    blocked_parser.add_argument(
        "--format",
        choices=OUTPUT_CHOICES,
        default="table",
        help="Output format.",
    )

    args = parser.parse_args()
    index = load_index()

    if args.command == "list":
        tools = index["tools"]
        if args.format == "json":
            emit_json(
                {
                    "index_version": index["index_version"],
                    "write": False,
                    "tool_count": len(tools),
                    "tools": tools,
                }
            )
            return
        print(render_tools_table(tools))
        return

    if args.command == "show":
        tool = find_tool(index["tools"], args.tool_name)
        if tool is None:
            raise SystemExit(f"tool not found: {args.tool_name}")

        if tool["write"] is not False:
            raise SystemExit(f"unsafe tool exposed: {args.tool_name}")

        if args.format == "json":
            emit_json(
                {
                    "index_version": index["index_version"],
                    "write": False,
                    "tool": tool,
                }
            )
            return

        print(f"name: {tool['name']}")
        print(f"command: {tool['command']}")
        print(f"risk: {tool['risk']}")
        print(f"write: {tool['write']}")
        print(f"description: {tool['description']}")
        return

    if args.command == "blocked":
        blocked_names = index["blocked_tool_names"]
        if args.format == "json":
            emit_json(
                {
                    "index_version": index["index_version"],
                    "write": False,
                    "blocked_tool_count": len(blocked_names),
                    "blocked_tool_names": blocked_names,
                }
            )
            return
        print(render_blocked_table(blocked_names))
        return


if __name__ == "__main__":
    main()
