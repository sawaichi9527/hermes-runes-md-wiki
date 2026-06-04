#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m64" / "evidence-retention-boundary.json"

EXPECTED_CLASSES = {
    "smoke_evidence",
    "validation_evidence",
    "runtime_summary",
    "wrapper_profile_evidence",
    "replay_evidence",
    "governance_interpretation",
}

EXPECTED_FORBIDDEN_STORAGE = {
    "full-transcript-archive",
    "raw-prompt-archive",
    "raw-answer-archive",
    "secret-store",
    "credential-store",
    "runtime-state-store",
    "rag-ingestion-source",
    "telemetry-pipeline",
    "siem-export",
    "distributed-tracing-store",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M64 retention boundary fixture missing",
        })

        payload = {
            "smoke_version": "m64.2-evidence-retention-boundary-v1",
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

    if fixture.get("governance_principle") != "retain-minimal-review-evidence-only":
        issues.append({
            "code": "governance_principle_drift",
            "actual": fixture.get("governance_principle"),
        })

    retention_boundary = fixture.get("retention_boundary", {})

    forbidden_storage = set(retention_boundary.get("forbidden_storage", []))

    if forbidden_storage != EXPECTED_FORBIDDEN_STORAGE:
        issues.append({
            "code": "forbidden_storage_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_STORAGE),
            "actual": sorted(forbidden_storage),
        })

    if retention_boundary.get("allowed_retention_style") != "minimal-summary-retention":
        issues.append({
            "code": "retention_style_drift",
            "actual": retention_boundary.get("allowed_retention_style"),
        })

    global_rules = fixture.get("global_retention_rules", {})

    expected_global_rules = {
        "summarized_only": True,
        "public_safe": True,
        "authoritative": False,
        "write": False,
        "contains_secrets": False,
        "contains_private_user_data": False,
        "full_transcript_allowed": False,
        "raw_prompt_allowed": False,
        "raw_answer_allowed": False,
        "credential_allowed": False,
        "rag_ingestion_allowed": False,
        "runtime_state_allowed": False,
        "authority_escalation_allowed": False,
        "retention_failure_blocks_runtime": False,
    }

    for key, expected in expected_global_rules.items():
        if global_rules.get(key) != expected:
            issues.append({
                "code": "global_rule_violation",
                "field": key,
                "expected": expected,
                "actual": global_rules.get(key),
            })

    retention_classes = fixture.get("retention_classes", [])

    class_ids = {item.get("evidence_class") for item in retention_classes}

    if class_ids != EXPECTED_CLASSES:
        issues.append({
            "code": "retention_class_drift",
            "expected": sorted(EXPECTED_CLASSES),
            "actual": sorted(class_ids),
        })

    for retention_class in retention_classes:
        if retention_class.get("review_only") is not True:
            issues.append({
                "code": "review_only_violation",
                "class": retention_class.get("evidence_class"),
            })

        if retention_class.get("authoritative") is not False:
            issues.append({
                "code": "authoritative_violation",
                "class": retention_class.get("evidence_class"),
            })

        if retention_class.get("write") is not False:
            issues.append({
                "code": "write_violation",
                "class": retention_class.get("evidence_class"),
            })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("retention_class_count") != 6:
        issues.append({
            "code": "retention_class_count_violation",
            "actual": expected_result.get("retention_class_count"),
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
        "smoke_version": "m64.2-evidence-retention-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "evidence-retention-boundary",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "retention_class_count": len(retention_classes),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
