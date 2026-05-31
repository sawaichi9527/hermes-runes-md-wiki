import os
from pathlib import Path

import yaml


def resolve_root() -> Path:
    env_root = os.environ.get("HERMES_MEMORY_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


DEFAULT_CONFIG = resolve_root() / "config/model_profiles.yaml"


def load_model_profiles(path=None):
    config_path = Path(path) if path else DEFAULT_CONFIG
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return data


def select_model_profile(model_name, profiles_data):
    model_name = (model_name or "").lower()

    profiles = profiles_data.get("profiles", {})
    default_name = profiles_data.get("default_profile", "default")

    for profile_name, profile in profiles.items():
        if profile_name == default_name:
            continue

        match = profile.get("match", {})
        model_contains = match.get("model_contains", []) or []

        for token in model_contains:
            if token.lower() in model_name:
                return profile_name, profile

    return default_name, profiles[default_name]


if __name__ == "__main__":
    data = load_model_profiles()

    samples = [
        "Qwen3.6-35B-A3B",
        "gemma-3-27b-it",
        "llama-3.3-70b-instruct",
        "unknown-model",
    ]

    for model in samples:
        name, profile = select_model_profile(model, data)
        print(f"{model} -> {name}")
