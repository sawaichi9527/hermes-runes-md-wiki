#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m64" / "public-safe-evidence-verification.json"

EXPECTED_FORBIDDEN_FIELDS = {
    "raw_prompt",
    "raw_answer",
    "full_prompt",
    "full_answer",
    "full_transcript",
    "secret",
    "token",
    "password",
    "database_password",
    "api_key",
    "private_user_data",
    "credential",
    "authorization_header",
    "runtime_state",
    "session_cookie",
}

EXPECTED_FORBIDDEN_BEHAVIORS = {
    "committing raw prompts",
    "committing raw answers",
    "committing full transcripts",
    "committing secrets or credentials",
    "committing private user data",
    "committing runtime state",
    "using public evidence as authority",
    "ingesting public evidence into RAG memory",
    "requiring an enterprise content scanning platform",
    "requiring a telemetry pipeline",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M64 public-safe evidence fixture missing",
        })
        payload = {
            "smoke_version": "m64.3-public-safe-evidence-verification-v1",
            "status": "FAIL",
            "write": False,
            "issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    if fixture.get("scale") != "personal-local":
        issues.append({
            "code": "scale_drift",
            "actual": fixture.get("scale"),
        })

    if fixture.get("governance_principle") != "public-safe-summary-only":
        issues.append({
            "code": "governance_principle_drift",
            "actual": fixture.get("governance_principle"),
        })

    public_safe_rules = fixture.get("public_safe_rules", {})
    expected_rules = {
        "summarized_only": True,
        "public_safe": True,
        "authoritative": False,
        "write": False,
        "contains_secrets": False,
        "contains_private_user_data": False,
        "contains_raw_prompt": False,
        "contains_raw_answer": False,
        "contains_full_transcript": False,
        "contains_credentials": False,
        "contains_runtime_state": False,
        "rag_ingestion_allowed": False,
        "runtime_state_allowed": False,
        "authority_escalation_allowed": False,
        "automatic_redaction_pipeline_required": False,
        "content_scanning_platform_required": False,
    }

    for key, expected in expected_rules.items():
        if public_safe_rules.get(key) != expected:
            issues.append({
                "code": "public_safe_rule_violation",
                "field": key,
                "expected": expected,
                "actual": public_safe_rules.get(key),
            })

    forbidden_fields = set(fixture.get("forbidden_public_fields", []))
    if forbidden_fields != EXPECTED_FORBIDDEN_FIELDS:
        issues.append({
            "code": "forbidden_fields_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_FIELDS),
            "actual": sorted(forbidden_fields),
        })

    forbidden_behaviors = set(fixture.get("forbidden_behaviors", []))
    if forbidden_behaviors != EXPECTED_FORBIDDEN_BEHAVIORS:
        issues.append({
            "code": "forbidden_behaviors_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_BEHAVIORS),
            "actual": sorted(forbidden_behaviors),
        })

    sample = fixture.get("sample_public_safe_evidence", {})
    sample_keys = set(sample.keys())

    if sample.get("status") != "PASS":
        issues.append({
            "code": "sample_status_violation",
            "actual": sample.get("status"),
        })

    if sample.get("scale") != "personal-local":
        issues.append({
            "code": "sample_scale_violation",
            "actual": sample.get("scale"),
        })

    if sample.get("write") is not False:
        issues.append({
            "code": "sample_write_violation",
            "actual": sample.get("write"),
        })

    if sample.get("authoritative") is not False:
        issues.append({
            "code": "sample_authoritative_violation",
            "actual": sample.get("authoritative"),
        })

    forbidden_sample_overlap = sample_keys & EXPECTED_FORBIDDEN_FIELDS
    if forbidden_sample_overlap:
        issues.append({
            "code": "sample_contains_forbidden_fields",
            "fields": sorted(forbidden_sample_overlap),
        })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("authoritative") is not False:
        issues.append({
            "code": "expected_authoritative_violation",
            "actual": expected_result.get("authoritative"),
        })

    if expected_result.get("write") is not False:
        issues.append({
            "code": "expected_write_violation",
            "actual": expected_result.get("write"),
        })

    if expected_result.get("issue_count") != 0:
        issues.append({
            "code": "expected_issue_count_violation",
            "actual": expected_result.get("issue_count"),
        })

    payload = {
        "smoke_version": "m64.3-public-safe-evidence-verification-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "public-safe-evidence-verification",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "public_safe": True,
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
