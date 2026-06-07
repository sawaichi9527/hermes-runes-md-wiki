#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m65" / "retention-public-safe-regression.json"

EXPECTED_FORBIDDEN_REGRESSION = {
    "full-transcript-archive-enabled",
    "raw-prompt-retention-enabled",
    "raw-answer-retention-enabled",
    "secret-retention-enabled",
    "credential-retention-enabled",
    "private-user-data-retention-enabled",
    "rag-ingestion-source-enabled",
    "runtime-state-store-enabled",
    "retention-failure-blocks-runtime",
    "evidence-retention-grants-authority",
}

EXPECTED_FORBIDDEN_INFRA = {
    "enterprise-content-scanning-platform",
    "automatic-redaction-pipeline",
    "dlp-platform",
    "siem-platform",
    "telemetry-pipeline",
    "evidence-database",
    "runtime-state-store",
    "archive-service",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M65 retention/public-safe regression fixture missing",
        })

        payload = {
            "smoke_version": "m65.5-retention-public-safe-regression-v1",
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

    if fixture.get("regression_principle") != "retention-public-safe-regression-is-minimal-summary-only":
        issues.append({
            "code": "regression_principle_drift",
            "actual": fixture.get("regression_principle"),
        })

    semantics = fixture.get("protected_retention_semantics", {})

    expected_semantics = {
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
        "full_transcript_allowed": False,
        "raw_prompt_allowed": False,
        "raw_answer_allowed": False,
        "credential_allowed": False,
        "rag_ingestion_allowed": False,
        "runtime_state_allowed": False,
        "authority_escalation_allowed": False,
        "retention_failure_blocks_runtime": False,
        "runtime_dependency_required": False,
        "content_scanning_platform_required": False,
        "automatic_redaction_pipeline_required": False,
    }

    for key, expected in expected_semantics.items():
        if semantics.get(key) != expected:
            issues.append({
                "code": "protected_semantic_violation",
                "field": key,
                "expected": expected,
                "actual": semantics.get(key),
            })

    regression_cases = fixture.get("regression_cases", [])

    for case in regression_cases:
        if case.get("write") is not False:
            issues.append({
                "code": "regression_case_write_violation",
                "case": case.get("id"),
            })

    forbidden_regression = set(fixture.get("forbidden_retention_regression", []))

    if forbidden_regression != EXPECTED_FORBIDDEN_REGRESSION:
        issues.append({
            "code": "forbidden_regression_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_REGRESSION),
            "actual": sorted(forbidden_regression),
        })

    forbidden_infra = set(fixture.get("forbidden_infrastructure", []))

    if forbidden_infra != EXPECTED_FORBIDDEN_INFRA:
        issues.append({
            "code": "forbidden_infrastructure_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_INFRA),
            "actual": sorted(forbidden_infra),
        })

    expected_result = fixture.get("expected_result", {})

    expected_result_rules = {
        "status": "PASS",
        "regression_case_count": 4,
        "authoritative": False,
        "write": False,
        "runtime_dependency_required": False,
        "public_safe": True,
        "summarized_only": True,
        "issue_count": 0,
    }

    for key, expected in expected_result_rules.items():
        if expected_result.get(key) != expected:
            issues.append({
                "code": "expected_result_violation",
                "field": key,
                "expected": expected,
                "actual": expected_result.get(key),
            })

    payload = {
        "smoke_version": "m65.5-retention-public-safe-regression-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "retention-public-safe-regression",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "runtime_dependency_required": False,
        "public_safe": True,
        "summarized_only": True,
        "regression_case_count": len(regression_cases),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
