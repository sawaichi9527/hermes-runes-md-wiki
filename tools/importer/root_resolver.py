#!/usr/bin/env python3
import os
from pathlib import Path


def resolve_root() -> Path:
    """
    Resolve Hermes Runes / Hermes Memory repository root.

    Resolution order:
    1. HERMES_RUNES_MD_WIKI_ROOT
    2. HERMES_MEMORY_ROOT legacy override
    3. Repository root inferred from this file location
    4. ~/workspace/hermes-runes-md-wiki fallback
    5. ~/workspace/hermes-memory legacy fallback
    """
    env_root = os.environ.get("HERMES_RUNES_MD_WIKI_ROOT") or os.environ.get(
        "HERMES_MEMORY_ROOT"
    )
    if env_root:
        return Path(env_root).expanduser().resolve()

    # tools/importer/root_resolver.py -> repo root is two parents up
    inferred = Path(__file__).resolve().parents[2]
    if (inferred / "wiki").exists() and (inferred / "tools").exists():
        return inferred

    modern_fallback = (Path.home() / "workspace" / "hermes-runes-md-wiki").resolve()
    if (modern_fallback / "wiki").exists() and (modern_fallback / "tools").exists():
        return modern_fallback

    return (Path.home() / "workspace" / "hermes-memory").resolve()


def resolve_importer_dir() -> Path:
    return resolve_root() / "tools" / "importer"


def resolve_wiki_dir() -> Path:
    return resolve_root() / "wiki"


def resolve_observation_log_dir() -> Path:
    return resolve_root() / "logs" / "observations"


if __name__ == "__main__":
    print(resolve_root())
