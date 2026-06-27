#!/usr/bin/env python3
"""Read-only PLUR runtime memory bridge helpers.

v0.7.4-dev S7-S9 scope:
- S7: read-only PLUR discovery / status check
- S8: runtime memory provider abstraction with safe Noop default
- S9: PLUR memory schema mapping

This module intentionally does not import PLUR runtime modules, read PLUR memory,
write PLUR memory, or mutate Hermes Agent configuration. It only reports local
availability signals and the project-level schema contract.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Protocol


SCHEMA_VERSION = "v0.7.4-dev-s9"
BRIDGE_POLICY = "plur-runtime-memory-bridge-v1"


@dataclass(frozen=True)
class ProviderStatus:
    """Read-only provider status payload."""

    name: str
    available: bool
    selected: bool
    read_only: bool = True
    memory_read: bool = False
    memory_write: bool = False
    writes_performed: bool = False
    notes: list[str] = field(default_factory=list)
    checks: dict[str, Any] = field(default_factory=dict)


class RuntimeMemoryProvider(Protocol):
    """Minimal provider protocol for runtime memory bridges.

    The v0.7.4-dev implementation only requires status inspection. Future
    providers may add read-only summaries and candidate dry-run support, but
    writes must remain outside this protocol until an explicit user-approved
    forge path exists.
    """

    name: str

    def status(self, *, selected: bool = False) -> ProviderStatus:
        """Return provider status without reading or writing runtime memory."""


class NoopRuntimeMemoryProvider:
    """Safe fallback provider used when PLUR is absent or intentionally disabled."""

    name = "noop"

    def status(self, *, selected: bool = False) -> ProviderStatus:
        return ProviderStatus(
            name=self.name,
            available=True,
            selected=selected,
            notes=[
                "safe fallback provider",
                "no PLUR dependency required",
                "no runtime memory read/write performed",
            ],
            checks={
                "provider_contract": "status-only",
                "degrades_without_plur": True,
            },
        )


class PlurRuntimeMemoryProvider:
    """Read-only PLUR availability detector.

    This detector intentionally avoids importing PLUR modules or invoking PLUR
    commands because this first bridge pass must not touch deployed PLUR memory.
    """

    name = "plur"

    PYTHON_MODULE_CANDIDATES = (
        "plur_hermes",
        "plur",
    )
    CLI_CANDIDATES = (
        "plur",
        "plur-hermes",
    )
    ENV_PREFIXES = (
        "PLUR_",
        "HERMES_PLUR_",
    )

    def _module_checks(self) -> dict[str, bool]:
        return {
            module: importlib.util.find_spec(module) is not None
            for module in self.PYTHON_MODULE_CANDIDATES
        }

    def _cli_checks(self) -> dict[str, bool]:
        return {command: shutil.which(command) is not None for command in self.CLI_CANDIDATES}

    def _env_prefix_checks(self) -> dict[str, bool]:
        keys = os.environ.keys()
        return {
            prefix: any(key.startswith(prefix) for key in keys)
            for prefix in self.ENV_PREFIXES
        }

    def status(self, *, selected: bool = False) -> ProviderStatus:
        module_checks = self._module_checks()
        cli_checks = self._cli_checks()
        env_prefix_checks = self._env_prefix_checks()
        available = any(module_checks.values()) or any(cli_checks.values()) or any(
            env_prefix_checks.values()
        )

        notes = [
            "availability signals only",
            "PLUR modules are not imported",
            "PLUR commands are not executed",
            "PLUR memory is not read or written",
            "environment values are not printed",
        ]
        if not available:
            notes.append("no PLUR availability signal detected; noop fallback is expected")

        return ProviderStatus(
            name=self.name,
            available=available,
            selected=selected,
            notes=notes,
            checks={
                "python_modules_present": module_checks,
                "commands_on_path": cli_checks,
                "env_prefix_present": env_prefix_checks,
                "safe_detection_only": True,
            },
        )


def select_provider(provider_name: str) -> RuntimeMemoryProvider:
    if provider_name == "noop":
        return NoopRuntimeMemoryProvider()
    if provider_name == "plur":
        return PlurRuntimeMemoryProvider()
    if provider_name == "auto":
        # Safe default for v0.7.4-dev S7-S9: auto reports PLUR availability but
        # selects noop until a later explicit read-only summary step is approved.
        return NoopRuntimeMemoryProvider()
    raise ValueError(f"unsupported provider: {provider_name}")


def build_schema_mapping() -> dict[str, Any]:
    """Return the S9 schema mapping without reading runtime memory."""

    return {
        "schema_version": SCHEMA_VERSION,
        "bridge_policy": BRIDGE_POLICY,
        "status": "pass",
        "read_only": True,
        "writes_performed": False,
        "roles": {
            "engram": {
                "plain_meaning": "compact behavioral or runtime memory",
                "examples": [
                    "user preference",
                    "interaction rule",
                    "active architecture direction",
                    "governance hint",
                ],
                "required_fields": ["id", "scope", "content", "created_at"],
                "recommended_fields": [
                    "source_pointer",
                    "last_verified_at",
                    "confidence",
                    "status",
                ],
                "default_prompt_injection": "allowed_when_small_and_current",
                "auto_promote_to_runes_wiki": False,
            },
            "episode": {
                "plain_meaning": "timestamped event or operational timeline record",
                "examples": [
                    "test run observed",
                    "Lark bot interaction happened",
                    "gateway issue observed",
                ],
                "required_fields": ["id", "scope", "event", "created_at"],
                "recommended_fields": ["source_pointer", "status"],
                "default_prompt_injection": "disabled",
                "auto_promote_to_runes_wiki": False,
            },
            "checkpoint": {
                "plain_meaning": "current working state for recovery or handoff",
                "examples": [
                    "current task state",
                    "next action",
                    "blocker",
                    "evidence pointer",
                ],
                "required_fields": ["id", "scope", "summary", "created_at"],
                "recommended_fields": ["expires_at", "supersedes", "status"],
                "default_prompt_injection": "allowed_when_active_and_relevant",
                "auto_promote_to_runes_wiki": False,
            },
            "candidate": {
                "plain_meaning": "proposed formal memory awaiting human approval",
                "examples": [
                    "candidate Runes Wiki memory",
                    "candidate policy note",
                    "candidate project decision",
                ],
                "required_fields": [
                    "id",
                    "scope",
                    "proposal",
                    "created_at",
                    "approval_state",
                ],
                "recommended_fields": [
                    "target_path",
                    "source_pointer",
                    "risk",
                    "status",
                ],
                "default_prompt_injection": "proposal_only",
                "auto_promote_to_runes_wiki": False,
                "forge_requirement": "explicit_user_approval_then_runes_shield_gate",
            },
        },
        "global_rules": [
            "scope is required",
            "episode injection is disabled by default",
            "governance hints require source_pointer and last_verified_at when available",
            "candidates do not auto-promote",
            "stale checkpoints should be marked superseded or inactive instead of heavy purge",
            "existing deployed PLUR memory is not bulk migrated, bulk deleted, or assumed canonical",
        ],
    }


def build_status(provider_name: str) -> dict[str, Any]:
    requested = provider_name
    selected_provider = select_provider(provider_name)
    noop_provider = NoopRuntimeMemoryProvider()
    plur_provider = PlurRuntimeMemoryProvider()

    provider_statuses = {
        "noop": asdict(noop_provider.status(selected=selected_provider.name == "noop")),
        "plur": asdict(plur_provider.status(selected=selected_provider.name == "plur")),
    }

    return {
        "status": "pass",
        "date": date.today().isoformat(),
        "schema_version": SCHEMA_VERSION,
        "bridge_policy": BRIDGE_POLICY,
        "provider_requested": requested,
        "provider_selected": selected_provider.name,
        "read_only": True,
        "memory_read": False,
        "memory_write": False,
        "writes_performed": False,
        "s7_discovery": "availability status only; no PLUR memory read/write",
        "s8_noop_provider": "available and selected by default for auto/noop",
        "s9_schema_mapping": SCHEMA_VERSION,
        "providers": provider_statuses,
        "non_goals_enforced": [
            "no Hermes Agent core patch",
            "no PLUR command execution",
            "no PLUR memory read",
            "no PLUR memory write",
            "no bulk migration",
            "no bulk deletion",
            "no automatic candidate promotion",
        ],
    }


def emit(payload: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"status: {payload.get('status')}")
    print(f"schema_version: {payload.get('schema_version')}")
    if "provider_selected" in payload:
        print(f"provider_selected: {payload.get('provider_selected')}")
        print(f"read_only: {payload.get('read_only')}")
        print(f"memory_read: {payload.get('memory_read')}")
        print(f"memory_write: {payload.get('memory_write')}")
        print(f"writes_performed: {payload.get('writes_performed')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read-only PLUR runtime memory bridge status/schema helper."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser(
        "status",
        help="Report read-only provider availability status without reading PLUR memory.",
    )
    status_parser.add_argument(
        "--provider",
        choices=["auto", "noop", "plur"],
        default="auto",
        help="Provider to select. auto intentionally selects noop in v0.7.4-dev S7-S9.",
    )
    status_parser.add_argument("--json", action="store_true")

    schema_parser = subparsers.add_parser(
        "schema",
        help="Print S9 engram/episode/checkpoint/candidate schema mapping.",
    )
    schema_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command == "status":
        emit(build_status(args.provider), as_json=args.json)
        return

    if args.command == "schema":
        emit(build_schema_mapping(), as_json=args.json)
        return

    raise SystemExit(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
