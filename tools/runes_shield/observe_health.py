#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = ROOT / "tools" / "runes_shield"
DOC_DIR = ROOT / "wiki" / "_system"

RUNTIME_FILES = [
    "registry.json",
    "load_registry.py",
    "discover_registry.py",
    "resolve_route.py",
    "dispatch_invocation.py",
    "smoke_boundary_regression.py",
]

DOC_FILES = [
    "m35-runtime-registry-mvp.md",
    "m35-1-discovery-output-generator.md",
    "m35-2-route-resolver.md",
    "m35-3-invocation-dispatcher-mvp.md",
    "m35-4-runtime-boundary-regression-smoke.md",
    "m35-5-verification-roadmap-lock.md",
]


def collect(base, names):
    rows = []

    for name in names:
        path = base / name
        rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "exists": path.is_file(),
            }
        )

    return rows


def observe_health():
    runtime = collect(TOOL_DIR, RUNTIME_FILES)
    docs = collect(DOC_DIR, DOC_FILES)
    missing = [item for item in runtime + docs if not item["exists"]]

    return {
        "status": "PASS" if not missing else "WARN",
        "handler": "observe",
        "write": False,
        "summary": "Read-only runtime health observation completed.",
        "runtime_files": runtime,
        "system_docs": docs,
        "missing": missing,
        "boundary": {
            "write_default": False,
            "autonomous_apply": False,
            "hidden_escalation": False,
            "trusted_memory_mutation": False,
        },
    }


def main():
    print(json.dumps(observe_health(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
