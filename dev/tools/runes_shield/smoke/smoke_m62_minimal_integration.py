#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "wiki" / "_system" / "m62-minimal-external-agent-integration.md"

REQUIRED_TOKENS = [
    "personal-local",
    "agent-agnostic",
    "Runes Shield",
    "runes_agent_onboarding_lock.py",
    "smoke_m60_external_agent_trial.py",
    "run_real_agent_evidence.py",
    "not ingested into RAG",
    "Profiles remain metadata-only",
    "Explicit Non-Goals",
    "bounded personal-local governed onboarding",
]


def main():
    issues = []

    if not DOC.exists():
        issues.append({
            "code": "missing_doc",
            "message": "M62 minimal integration guide missing",
        })
        payload = {
            "smoke_version": "m62.3-minimal-integration-smoke-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    text = DOC.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            issues.append({
                "code": "missing_token",
                "token": token,
            })

    payload = {
        "smoke_version": "m62.3-minimal-integration-smoke-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "minimal-external-agent-integration-validation",
        "write": False,
        "doc": str(DOC.relative_to(ROOT)),
        "required_token_count": len(REQUIRED_TOKENS),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
