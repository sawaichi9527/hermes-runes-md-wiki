#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "m64" / "evidence-replay-boundary.json"

EXPECTED_FORBIDDEN_SCOPE = {
    "proposal-apply-execution",
    "runtime-policy-mutation",
    "direct-wiki-write",
    "direct-database-write",
    "background-worker-trigger",
    "automatic-memory-promotion",
    "authority-token-replay",
    "credential-replay",
    "full-session-reconstruction",
    "private-transcript-replay",
}

EXPECTED_FORBIDDEN_INTERPRETATIONS = {
    "replay implies execution permission",
    "replay implies apply permission",
    "replay implies promotion permission",
    "replay implies trusted memory authority",
    "replay implies runtime override",
    "review replay implies direct wiki mutation",
    "review replay implies direct database mutation",
    "summary replay implies autonomous workflow execution",
}


def main():
    issues = []

    if not FIXTURE.exists():
        issues.append({
            "code": "missing_fixture",
            "message": "M64 replay boundary fixture missing",
        })

        payload = {
            "smoke_version": "m64.6-evidence-replay-boundary-v1",
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

    if fixture.get("governance_principle") != "replay-is-review-not-execution":
        issues.append({
            "code": "governance_principle_drift",
            "actual": fixture.get("governance_principle"),
        })

    replay_rules = fixture.get("replay_rules", {})

    expected_rules = {
        "review_only_replay_allowed": True,
        "replay_is_execution": False,
        "replay_is_apply": False,
        "replay_is_promotion": False,
        "replay_is_authority": False,
        "replay_grants_write": False,
        "replay_grants_database_mutation": False,
        "replay_grants_runtime_policy_override": False,
        "replay_grants_authority_escalation": False,
        "human_review_remains_required": True,
        "authoritative": False,
        "write": False,
        "public_safe": True,
        "summarized_only": True,
    }

    for key, expected in expected_rules.items():
        if replay_rules.get(key) != expected:
            issues.append({
                "code": "replay_rule_violation",
                "field": key,
                "expected": expected,
                "actual": replay_rules.get(key),
            })

    forbidden_scope = set(fixture.get("forbidden_replay_scope", []))

    if forbidden_scope != EXPECTED_FORBIDDEN_SCOPE:
        issues.append({
            "code": "forbidden_scope_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_SCOPE),
            "actual": sorted(forbidden_scope),
        })

    forbidden_interpretations = set(fixture.get("forbidden_interpretations", []))

    if forbidden_interpretations != EXPECTED_FORBIDDEN_INTERPRETATIONS:
        issues.append({
            "code": "forbidden_interpretations_drift",
            "expected": sorted(EXPECTED_FORBIDDEN_INTERPRETATIONS),
            "actual": sorted(forbidden_interpretations),
        })

    replay_classes = fixture.get("replay_classes", [])

    for replay_class in replay_classes:
        if replay_class.get("review_only") is not True:
            issues.append({
                "code": "review_only_violation",
                "class": replay_class.get("id"),
            })

        if replay_class.get("execution") is not False:
            issues.append({
                "code": "execution_violation",
                "class": replay_class.get("id"),
            })

        if replay_class.get("apply") is not False:
            issues.append({
                "code": "apply_violation",
                "class": replay_class.get("id"),
            })

        if replay_class.get("promotion") is not False:
            issues.append({
                "code": "promotion_violation",
                "class": replay_class.get("id"),
            })

        if replay_class.get("authoritative") is not False:
            issues.append({
                "code": "authoritative_violation",
                "class": replay_class.get("id"),
            })

        if replay_class.get("write") is not False:
            issues.append({
                "code": "write_violation",
                "class": replay_class.get("id"),
            })

    expected_result = fixture.get("expected_result", {})

    if expected_result.get("status") != "PASS":
        issues.append({
            "code": "expected_status_violation",
            "actual": expected_result.get("status"),
        })

    if expected_result.get("replay_class_count") != 3:
        issues.append({
            "code": "replay_class_count_violation",
            "actual": expected_result.get("replay_class_count"),
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
        "smoke_version": "m64.6-evidence-replay-boundary-v1",
        "status": "PASS" if not issues else "FAIL",
        "mode": "evidence-replay-boundary",
        "scale": fixture.get("scale"),
        "write": False,
        "authoritative": False,
        "review_only_replay": True,
        "replay_class_count": len(replay_classes),
        "issue_count": len(issues),
        "issues": issues,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
