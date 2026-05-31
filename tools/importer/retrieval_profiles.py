from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parent
PROFILE_FILE = ROOT / "retrieval_profiles.yaml"


def load_retrieval_profiles():
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("profiles", {})


def select_retrieval_profile(query_type: str):
    profiles = load_retrieval_profiles()

    query_type = (query_type or "").strip()

    if query_type in profiles:
        return query_type, profiles[query_type]

    return "default", profiles.get("default", {})


if __name__ == "__main__":
    import json

    for q in [
        "baseline_lookup",
        "verification_lookup",
        "unknown_type",
    ]:
        name, profile = select_retrieval_profile(q)

        print(json.dumps({
            "query_type": q,
            "selected_profile": name,
            "profile": profile,
        }, ensure_ascii=False))
