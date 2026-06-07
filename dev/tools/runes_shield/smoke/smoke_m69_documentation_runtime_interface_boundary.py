#!/usr/bin/env python3
"""M69 Documentation / Runtime Interface Boundary smoke."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m69" / "documentation-runtime-interface-boundary.json"


def main() -> int:
    issues: list[str] = []
    data = json.loads(FIXTURE.read_text(encoding="utf-8")) if FIXTURE.exists() else {}
    if not data:
        issues.append(f"missing fixture: {FIXTURE}")

    for key in ["write", "authoritative", "runtime_dependency_required"]:
        if data.get(key) is not False:
            issues.append(f"{key} must be false")
    if data.get("scale") != "personal-local":
        issues.append("scale must be personal-local")

    semantics = data.get("required_semantics", {})
    required_true = [
        "documentation_is_not_api",
        "roadmap_is_not_permission_grant",
        "next_actions_are_not_runtime_commands",
        "verification_docs_are_not_tool_specs",
        "examples_are_not_authority",
        "runes_shield_exposes_callable_behavior",
        "wiki_docs_do_not_expose_callable_behavior",
        "agent_must_not_execute_docs_as_commands",
    ]
    required_false = [
        "automatic_tool_discovery_from_docs",
        "automatic_runtime_command_from_roadmap",
        "automatic_permission_from_documentation",
    ]
    for key in required_true:
        if semantics.get(key) is not True:
            issues.append(f"required_semantics.{key} must be true")
    for key in required_false:
        if semantics.get(key) is not False:
            issues.append(f"required_semantics.{key} must be false")

    forbidden_infra = set(data.get("forbidden_infrastructure", []))
    for forbidden in [
        "documentation-runtime-dispatcher",
        "doc-driven-tool-executor",
        "automatic-doc-command-runner",
        "runtime-doc-parser-daemon",
        "agent-command-autoloader",
    ]:
        if forbidden not in forbidden_infra:
            issues.append(f"missing forbidden infrastructure: {forbidden}")

    result = {
        "smoke_version": "m69-documentation-runtime-interface-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": data.get("mode"),
        "scale": data.get("scale"),
        "write": data.get("write"),
        "authoritative": data.get("authoritative"),
        "runtime_dependency_required": data.get("runtime_dependency_required"),
        "boundary_target_count": len(data.get("boundary_targets", [])),
        "issue_count": len(issues),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
