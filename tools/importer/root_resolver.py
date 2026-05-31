#!/usr/bin/env python3
import os
from pathlib import Path


def resolve_root() -> Path:
    """
    Resolve Hermes Runes / Hermes Memory repository root.

    Resolution order:
    1. HERMES_MEMORY_ROOT
    2. Repository root inferred from this file location
    3. ~/workspace/hermes-memory fallback
    """
    env_root = os.environ.get("HERMES_MEMORY_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    # tools/importer/root_resolver.py -> repo root is two parents up
    inferred = Path(__file__).resolve().parents[2]
    if (inferred / "wiki").exists() and (inferred / "tools").exists():
        return inferred

    return (Path.home() / "workspace" / "hermes-memory").resolve()


def resolve_importer_dir() -> Path:
    return resolve_root() / "tools" / "importer"


def resolve_wiki_dir() -> Path:
    return resolve_root() / "wiki"


def resolve_observation_log_dir() -> Path:
    return resolve_root() / "logs" / "observations"


if __name__ == "__main__":
    print(resolve_root())
