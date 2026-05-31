from pathlib import Path
import yaml


ROOT = Path.home() / "workspace/hermes-memory"
DEFAULT_CONFIG = ROOT / "config/model_profiles.yaml"


def load_model_profiles(path=DEFAULT_CONFIG):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
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
