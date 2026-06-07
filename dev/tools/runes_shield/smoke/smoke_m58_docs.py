#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FILES = {
    "README.md": ROOT / "README.md",
    "AGENTS.md": ROOT / "AGENTS.md",
    "m58-runes-summoning-trial.md": ROOT / "wiki" / "_system" / "m58-runes-summoning-trial.md",
}

REQUIRED_TOKENS = {
    "README.md": [
        "Agent Onboarding / Runes Summoning Trial",
        "wiki/_system/m58-runes-summoning-trial.md",
        "read-only",
        "bounded",
        "diagnostic-oriented",
    ],
    "AGENTS.md": [
        "M58 Runes Summoning Trial / 盧恩符文召喚試煉",
        "Midgard",
        "Bifröst",
        "Runes Mouth of Verity",
        "World Tree",
        "Nine Realms Administrator",
        "Optional onboarding easter egg subtitles",
        "one-time UX flavor text",
        "not a runtime dependency",
    ],
    "m58-runes-summoning-trial.md": [
        "World Concept Mapping",
        "Midgard",
        "Bifröst",
        "World Tree",
        "Runes Shield",
        "Runes Mouth of Verity",
        "first-connect / post-install",
        "do not bypass Runes Shield",
        "personal-local",
        "bounded",
        "read-only",
        "diagnostic-oriented",
    ],
}


def main():
    issues = []
    checked_files = []

    for label, path in FILES.items():
        if not path.exists():
            issues.append({
                "code": "missing_file",
                "file": label,
                "message": f"Required M58 document missing: {label}",
            })
            continue

        content = path.read_text(encoding="utf-8")
        checked_files.append(label)

        for token in REQUIRED_TOKENS[label]:
            if token not in content:
                issues.append({
                    "code": "missing_token",
                    "file": label,
                    "token": token,
                    "message": f"Required M58 wording missing: {token}",
                })

    payload = {
        "smoke_version": "m58.4-docs-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "docs-wording-lock",
        "write": False,
        "checked_file_count": len(checked_files),
        "checked_files": checked_files,
        "required_token_groups": {
            key: len(value)
            for key, value in REQUIRED_TOKENS.items()
        },
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
