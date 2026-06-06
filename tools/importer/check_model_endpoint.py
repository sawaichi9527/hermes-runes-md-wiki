#!/usr/bin/env python3
"""Lightweight model endpoint preflight for beta-prep.

This checker intentionally does not print API keys or other sensitive values.
It treats a missing model endpoint as SKIP so model-dependent smoke tests do not
block the personal-local beta-prep mainline.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


PLACEHOLDER_KEYS = {"", "not-needed", "not-set", "none", "null", "local"}


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def merged_env(env_file: Path) -> dict[str, str]:
    values = load_env_file(env_file)
    for key in ("OPENAI_BASE_URL", "OPENAI_MODEL", "OPENAI_API_KEY", "OPENAI_AUTH_MODE"):
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def build_headers(api_key: str, auth_mode: str) -> dict[str, str]:
    mode = (auth_mode or "auto").strip().lower()
    if mode not in {"auto", "none", "bearer"}:
        raise ValueError("OPENAI_AUTH_MODE must be one of: auto, none, bearer")

    headers = {"Content-Type": "application/json"}
    should_send_auth = mode == "bearer" or (
        mode == "auto" and api_key.strip().lower() not in PLACEHOLDER_KEYS
    )
    if should_send_auth:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def main() -> int:
    parser = argparse.ArgumentParser(description="Check OpenAI-compatible model endpoint configuration.")
    parser.add_argument(
        "--env-file",
        default=str(Path(__file__).resolve().parent / ".env"),
        help="Path to importer .env file. Defaults to tools/importer/.env.",
    )
    parser.add_argument("--probe", action="store_true", help="Probe the configured /models endpoint.")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout for --probe.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    env_file = Path(args.env_file).expanduser()
    values = merged_env(env_file)

    base_url = values.get("OPENAI_BASE_URL", "").rstrip("/")
    model = values.get("OPENAI_MODEL", "")
    api_key = values.get("OPENAI_API_KEY", "not-needed")
    auth_mode = values.get("OPENAI_AUTH_MODE", "auto")

    result: dict[str, object] = {
        "check": "model-endpoint",
        "env_file": str(env_file),
        "env_file_exists": env_file.exists(),
        "base_url_configured": bool(base_url),
        "model_configured": bool(model),
        "auth_mode": auth_mode,
        "probe_requested": bool(args.probe),
        "write": False,
    }

    try:
        headers = build_headers(api_key, auth_mode)
    except ValueError as exc:
        result.update({"status": "FAIL", "reason": str(exc)})
        print_result(result, args.json)
        return 2

    result["auth_header_would_be_sent"] = "Authorization" in headers

    if not base_url or not model:
        result.update(
            {
                "status": "SKIP",
                "reason": "OPENAI_BASE_URL and OPENAI_MODEL are required for model-dependent smoke.",
                "expected": True,
            }
        )
        print_result(result, args.json)
        return 0

    result.update({"status": "PASS", "reason": "model endpoint configuration present"})

    if args.probe:
        url = f"{base_url}/models"
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                result["probe_status_code"] = response.status
                result["probe_pass"] = 200 <= response.status < 300
        except urllib.error.HTTPError as exc:
            result.update(
                {
                    "status": "FAIL",
                    "reason": f"endpoint probe HTTP error: {exc.code}",
                    "probe_status_code": exc.code,
                    "probe_pass": False,
                }
            )
        except Exception as exc:  # pragma: no cover - depends on local endpoint state
            result.update(
                {
                    "status": "FAIL",
                    "reason": f"endpoint probe failed: {exc}",
                    "probe_pass": False,
                }
            )

    print_result(result, args.json)
    return 0 if result.get("status") in {"PASS", "SKIP"} else 2


def print_result(result: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return

    print(f"status={result['status']}")
    print(f"check={result['check']}")
    print(f"env_file={result['env_file']}")
    print(f"env_file_exists={str(result['env_file_exists']).lower()}")
    print(f"base_url_configured={str(result['base_url_configured']).lower()}")
    print(f"model_configured={str(result['model_configured']).lower()}")
    print(f"auth_mode={result['auth_mode']}")
    print(f"auth_header_would_be_sent={str(result['auth_header_would_be_sent']).lower()}")
    print(f"reason={result['reason']}")


if __name__ == "__main__":
    sys.exit(main())
