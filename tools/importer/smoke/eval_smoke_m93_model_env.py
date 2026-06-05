#!/usr/bin/env python3
"""M93 minimal beta model environment verifier.

This verifier intentionally does not call the model endpoint.  It only checks
that the local OpenAI-compatible environment is present and structurally sane.

M10 remains the actual answer-generation smoke:
- missing env  -> clean SKIP
- configured   -> endpoint call and observation validation
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

IMPORTER_PARENT = Path(__file__).resolve().parents[1]
if str(IMPORTER_PARENT) not in sys.path:
    sys.path.insert(0, str(IMPORTER_PARENT))

from root_resolver import resolve_root, resolve_importer_dir

ROOT = resolve_root()
IMPORTER = resolve_importer_dir()
MODEL_ENV_KEYS = ("OPENAI_BASE_URL", "OPENAI_MODEL")
OPTIONAL_ENV_KEYS = ("OPENAI_API_KEY",)
ENV_PATHS = (ROOT / ".env", IMPORTER / ".env")


def load_env_file(path: Path) -> list[str]:
    loaded = []
    if not path.exists():
        return loaded

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value
            loaded.append(key)

    return loaded


def env_source_summary() -> list[dict[str, object]]:
    summary = []
    for path in ENV_PATHS:
        summary.append({
            "path": str(path),
            "exists": path.exists(),
        })
    return summary


def masked_value(key: str, value: str) -> str:
    if not value:
        return ""
    if key.endswith("KEY") or "PASSWORD" in key or "TOKEN" in key:
        return "<set>"
    if len(value) <= 16:
        return value
    return value[:12] + "..."


def validate_base_url(value: str) -> list[str]:
    issues = []
    parsed = urlparse(value)

    if parsed.scheme not in {"http", "https"}:
        issues.append("OPENAI_BASE_URL_scheme_must_be_http_or_https")
    if not parsed.netloc:
        issues.append("OPENAI_BASE_URL_missing_host")
    if value.endswith("/chat/completions"):
        issues.append("OPENAI_BASE_URL_should_point_to_api_root_not_chat_completions")

    return issues


def main() -> None:
    loaded = []
    for path in ENV_PATHS:
        loaded.extend(load_env_file(path))

    missing = [key for key in MODEL_ENV_KEYS if not os.environ.get(key)]
    issues = []

    base_url = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "")
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if base_url:
        issues.extend(validate_base_url(base_url))

    if model and model in {"your-local-model-name", "local-model-name"}:
        issues.append("OPENAI_MODEL_still_uses_placeholder")

    if api_key in {"", "not-set"}:
        api_key_state = "placeholder_or_empty"
    elif api_key == "not-needed":
        api_key_state = "local_placeholder"
    else:
        api_key_state = "set"

    if missing:
        status = "SKIP"
        reason = "missing_model_env"
    elif issues:
        status = "FAIL"
        reason = "invalid_model_env"
    else:
        status = "PASS"
        reason = "model_env_ready"

    output = {
        "suite": "M93 Model Env Minimal Beta Setting",
        "status": status,
        "reason": reason,
        "env_files": env_source_summary(),
        "loaded_keys": sorted(set(loaded)),
        "required_keys": list(MODEL_ENV_KEYS),
        "optional_keys": list(OPTIONAL_ENV_KEYS),
        "missing": missing,
        "issues": issues,
        "configured": {
            "OPENAI_BASE_URL": masked_value("OPENAI_BASE_URL", base_url),
            "OPENAI_MODEL": masked_value("OPENAI_MODEL", model),
            "OPENAI_API_KEY": api_key_state,
        },
        "message": (
            "Model env is ready for M10 observation smoke."
            if status == "PASS"
            else "Configure local .env to enable model-dependent M10 observation smoke."
        ),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    if status == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
