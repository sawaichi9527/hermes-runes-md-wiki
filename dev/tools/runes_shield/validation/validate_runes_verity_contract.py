#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERITY_CLI = ROOT / "tools" / "runes_shield" / "runes_verity.py"
CONTRACT_VERSION = "m56.1-runes-verity-contract-v1"
OUTPUT_CHOICES = ("table", "json")

REQUIRED_TOP_LEVEL_KEYS = {
    "verity_version",
    "name",
    "name_zh",
    "status",
    "mode",
    "scale",
    "write",
    "audit_root",
    "load_safety",
    "not_enterprise_features",
    "checks",
    "summary",
}

EXPECTED_CHECKS = [
    "integrity_oath",
    "trial_run_oath",
    "invocation_oath",
    "adapter_oath",
    "session_oath",
    "persistence_oath",
    "recall_replay_oath",
    "side_effect_oath",
    "abyss_guard",
    "calamity_guard",
]

REQUIRED_LOAD_SAFETY = {
    "bounded_execution": True,
    "single_shot": True,
    "background_worker": False,
    "recursive_invocation": False,
    "unbounded_audit_scan": False,
    "automatic_remediation": False,
}

FORBIDDEN_ENTERPRISE_FEATURES = {
    "siem",
    "centralized_collector",
    "distributed_tracing_backend",
    "policy_engine",
    "automatic_remediation",
    "background_daemon",
    "multi_tenant_rbac",
}

FORBIDDEN_TRUE_EFFECTS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "session_reexecuted",
    "adapter_reinvoked",
}


def load_payload(path=None, run=False, timeout=15):
    if run:
        completed = subprocess.run(
            [
                sys.executable,
                str(VERITY_CLI),
                "--format",
                "json",
                "--timeout",
                str(timeout),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout + 5,
            check=True,
        )
        return json.loads(completed.stdout)

    if not path:
        return json.loads(sys.stdin.read())

    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_contract(payload):
    issues = []

    _require_keys(issues, "$", payload, REQUIRED_TOP_LEVEL_KEYS)

    _expect_equal(issues, "$.verity_version", payload.get("verity_version"), "m56-runes-mouth-of-verity-v1")
    _expect_equal(issues, "$.name", payload.get("name"), "Runes Mouth of Verity")
    _expect_equal(issues, "$.name_zh", payload.get("name_zh"), "符文真理之口")
    _expect_equal(issues, "$.status", payload.get("status"), "PASS")
    _expect_equal(issues, "$.mode", payload.get("mode"), "truth-gate-runtime-verification")
    _expect_equal(issues, "$.scale", payload.get("scale"), "personal-local")
    _expect_false(issues, "$.write", payload.get("write"))

    checks = payload.get("checks", [])
    if not isinstance(checks, list):
        _add_issue(issues, "invalid_type", "$.checks", "checks must be a list")
        checks = []

    check_names = [check.get("check") for check in checks if isinstance(check, dict)]
    if check_names != EXPECTED_CHECKS:
        _add_issue(
            issues,
            "check_order_mismatch",
            "$.checks",
            f"expected checks {EXPECTED_CHECKS}, got {check_names}",
        )

    for index, check in enumerate(checks):
        path = f"$.checks[{index}]"
        if not isinstance(check, dict):
            _add_issue(issues, "invalid_type", path, "check entry must be an object")
            continue

        _require_keys(
            issues,
            path,
            check,
            {"check", "status", "description", "bounded", "write", "evidence"},
        )
        _expect_equal(issues, f"{path}.status", check.get("status"), "PASS")
        _expect_equal(issues, f"{path}.bounded", check.get("bounded"), True)
        _expect_false(issues, f"{path}.write", check.get("write"))

    load_safety = payload.get("load_safety", {})
    if not isinstance(load_safety, dict):
        _add_issue(issues, "invalid_type", "$.load_safety", "load_safety must be an object")
        load_safety = {}

    for key, expected in REQUIRED_LOAD_SAFETY.items():
        _expect_equal(issues, f"$.load_safety.{key}", load_safety.get(key), expected)

    max_events = load_safety.get("max_events_checked")
    if not isinstance(max_events, int) or max_events <= 0 or max_events > 100:
        _add_issue(
            issues,
            "load_safety_bound_violation",
            "$.load_safety.max_events_checked",
            "max_events_checked must be an integer in range 1..100",
        )

    max_days = load_safety.get("max_recent_days")
    if not isinstance(max_days, int) or max_days <= 0 or max_days > 7:
        _add_issue(
            issues,
            "load_safety_bound_violation",
            "$.load_safety.max_recent_days",
            "max_recent_days must be an integer in range 1..7",
        )

    timeout = load_safety.get("timeout_sec_per_check")
    if not isinstance(timeout, int) or timeout <= 0 or timeout > 30:
        _add_issue(
            issues,
            "load_safety_bound_violation",
            "$.load_safety.timeout_sec_per_check",
            "timeout_sec_per_check must be an integer in range 1..30",
        )

    features = set(payload.get("not_enterprise_features", []))
    missing_features = sorted(FORBIDDEN_ENTERPRISE_FEATURES - features)
    if missing_features:
        _add_issue(
            issues,
            "missing_not_enterprise_features",
            "$.not_enterprise_features",
            f"missing explicit non-enterprise features: {missing_features}",
        )

    _collect_forbidden_effects(payload, "$", issues)

    summary = payload.get("summary", {})
    if isinstance(summary, dict):
        _expect_equal(issues, "$.summary.total", summary.get("total"), len(EXPECTED_CHECKS))
        _expect_equal(issues, "$.summary.failed", summary.get("failed"), 0)
        _expect_equal(issues, "$.summary.passed", summary.get("passed"), len(EXPECTED_CHECKS))
    else:
        _add_issue(issues, "invalid_type", "$.summary", "summary must be an object")

    return {
        "contract_version": CONTRACT_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "schema_target": "m56-runes-mouth-of-verity-v1",
        "write": False,
        "issue_count": len(issues),
        "issues": issues,
        "locked_contract": {
            "required_top_level_keys": sorted(REQUIRED_TOP_LEVEL_KEYS),
            "expected_checks": EXPECTED_CHECKS,
            "required_load_safety": REQUIRED_LOAD_SAFETY,
            "forbidden_true_effects": sorted(FORBIDDEN_TRUE_EFFECTS),
            "scale": "personal-local",
            "mode": "truth-gate-runtime-verification",
        },
    }


def _require_keys(issues, path, obj, required):
    if not isinstance(obj, dict):
        _add_issue(issues, "invalid_type", path, "expected object")
        return
    missing = sorted(required - set(obj))
    if missing:
        _add_issue(issues, "missing_required_keys", path, f"missing keys: {missing}")


def _expect_equal(issues, path, actual, expected):
    if actual != expected:
        _add_issue(issues, "unexpected_value", path, f"expected {expected!r}, got {actual!r}")


def _expect_false(issues, path, actual):
    if actual is not False:
        _add_issue(issues, "expected_false", path, f"expected false, got {actual!r}")


def _collect_forbidden_effects(value, path, issues):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    _add_issue(
                        issues,
                        "forbidden_effect_true",
                        f"{path}.effects.{key}",
                        "forbidden effect must remain false",
                    )
        for key, child in value.items():
            _collect_forbidden_effects(child, f"{path}.{key}", issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _collect_forbidden_effects(child, f"{path}[{index}]", issues)


def _add_issue(issues, code, path, message):
    issues.append({"code": code, "path": path, "message": message})


def render_table(payload):
    lines = [
        f"contract_version: {payload['contract_version']}",
        f"schema_target: {payload['schema_target']}",
        f"status: {payload['status']}",
        f"write: {payload['write']}",
        f"issue_count: {payload['issue_count']}",
    ]
    if payload["issues"]:
        lines.append("issues:")
        for issue in payload["issues"]:
            lines.append(f"  - {issue['code']} {issue['path']}: {issue['message']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate the locked M56 Runes Mouth of Verity output contract."
    )
    parser.add_argument("--input", help="Path to a captured Runes Verity JSON payload. Omit to read stdin unless --run is used.")
    parser.add_argument("--run", action="store_true", help="Run runes_verity.py and validate its live JSON output.")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = load_payload(path=args.input, run=args.run, timeout=args.timeout)
    result = validate_contract(payload)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(render_table(result))


if __name__ == "__main__":
    main()
