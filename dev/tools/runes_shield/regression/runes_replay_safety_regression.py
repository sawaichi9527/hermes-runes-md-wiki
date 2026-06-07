#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMP_ROOT = ROOT / "tmp" / "m56-4-replay-safety"
PERSIST = ROOT / "tools" / "runes_shield" / "runes_shield_audit_persistence.py"
RECALL = ROOT / "tools" / "runes_shield" / "runes_shield_audit_recall.py"
REGRESSION_VERSION = "m56.4-replay-safety-regression-v1"
OUTPUT_CHOICES = ("table", "json")

FORBIDDEN_TRUE_EFFECTS = {
    "trusted_wiki_write",
    "markdown_mutation",
    "index_update",
    "automatic_apply",
    "automatic_promotion",
    "database_mutation",
    "observation_ingested_to_rag",
    "audit_log_written",
    "session_reexecuted",
    "adapter_reinvoked",
}


def run_process(args, timeout):
    return subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )


def persist_seed(audit_root, timeout):
    request = {
        "agent": "hermes-agent",
        "conversation_id": "conv-m56-4-replay-safety",
        "request": {
            "intent": "check_integrity",
        },
    }
    completed = run_process(
        [
            PERSIST,
            "--raw-json",
            json.dumps(request),
            "--audit-root",
            str(audit_root.relative_to(ROOT)),
            "--write",
            "--format",
            "json",
        ],
        timeout=timeout,
    )
    return json.loads(completed.stdout)


def replay_session(audit_root, session_id, timeout):
    completed = run_process(
        [
            RECALL,
            "replay",
            "--audit-root",
            str(audit_root.relative_to(ROOT)),
            "--session-id",
            session_id,
            "--format",
            "json",
        ],
        timeout=timeout,
    )
    return json.loads(completed.stdout)


def recall_summary(audit_root, timeout):
    completed = run_process(
        [
            RECALL,
            "summary",
            "--audit-root",
            str(audit_root.relative_to(ROOT)),
            "--format",
            "json",
        ],
        timeout=timeout,
    )
    return json.loads(completed.stdout)


def count_audit_lines(audit_root):
    files = sorted(audit_root.glob("**/*.jsonl")) if audit_root.exists() else []
    line_count = 0
    paths = []
    for path in files:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        line_count += len(lines)
        paths.append(str(path.relative_to(ROOT)))
    return {"file_count": len(files), "line_count": line_count, "paths": paths}


def build_regression(iterations=5, timeout=15, keep_tmp=False):
    issues = []

    if iterations <= 0 or iterations > 10:
        issues.append(_issue("invalid_iterations", "iterations must be bounded in range 1..10"))
        iterations = min(max(iterations, 1), 10)

    if TEMP_ROOT.exists():
        shutil.rmtree(TEMP_ROOT)

    seed = persist_seed(TEMP_ROOT, timeout=timeout)
    session_id = seed["session_id"]
    before = count_audit_lines(TEMP_ROOT)

    replays = []
    baseline_chain = None

    for index in range(iterations):
        replay = replay_session(TEMP_ROOT, session_id=session_id, timeout=timeout)
        after_each = count_audit_lines(TEMP_ROOT)
        violations = []
        collect_forbidden_effects(replay, f"replay[{index}]", violations)
        chain_signature = [
            {
                "layer": item.get("layer"),
                "layer_status": item.get("layer_status"),
                "intent": item.get("intent"),
                "tool": item.get("tool"),
                "write": item.get("write"),
            }
            for item in replay.get("chain", [])
        ]

        if baseline_chain is None:
            baseline_chain = chain_signature
        elif chain_signature != baseline_chain:
            issues.append(_issue("replay_chain_drift", f"Replay run {index + 1} chain drifted."))

        run_ok = (
            replay.get("status") == "PASS"
            and replay.get("mode") == "read-only-reconstruction"
            and replay.get("write") is False
            and replay.get("effects", {}).get("session_reexecuted") is False
            and replay.get("effects", {}).get("adapter_reinvoked") is False
            and replay.get("effects", {}).get("audit_log_written") is False
            and not violations
            and after_each["line_count"] == before["line_count"]
        )

        if not run_ok:
            issues.append(_issue("replay_run_failed", f"Replay run {index + 1} violated safety expectations."))

        replays.append(
            {
                "run_index": index + 1,
                "status": "PASS" if run_ok else "FAIL",
                "replay_status": replay.get("status"),
                "mode": replay.get("mode"),
                "write": replay.get("write"),
                "event_count": replay.get("event_count"),
                "chain_count": replay.get("chain_count"),
                "session_reexecuted": replay.get("effects", {}).get("session_reexecuted"),
                "adapter_reinvoked": replay.get("effects", {}).get("adapter_reinvoked"),
                "audit_log_written": replay.get("effects", {}).get("audit_log_written"),
                "audit_lines_after": after_each["line_count"],
                "forbidden_effect_violation_count": len(violations),
                "chain_signature": chain_signature,
            }
        )

    after = count_audit_lines(TEMP_ROOT)
    summary = recall_summary(TEMP_ROOT, timeout=timeout)

    if after["line_count"] != before["line_count"]:
        issues.append(
            _issue(
                "audit_line_count_changed",
                f"Replay changed audit line count from {before['line_count']} to {after['line_count']}.",
            )
        )

    if summary.get("event_count") != before["line_count"]:
        issues.append(_issue("summary_mismatch", "Recall summary event_count differs from audit line count."))

    result = {
        "regression_version": REGRESSION_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "mode": "replay-safety-regression",
        "scale": "personal-local",
        "write": False,
        "audit_root": str(TEMP_ROOT.relative_to(ROOT)),
        "iterations": iterations,
        "seed": {
            "status": seed.get("status"),
            "session_id": session_id,
            "request_id": seed.get("request_id"),
            "trace_id": seed.get("trace_id"),
            "event_count": seed.get("event_count"),
            "write": seed.get("write"),
        },
        "audit_before": before,
        "audit_after": after,
        "summary": {
            "status": summary.get("status"),
            "event_count": summary.get("event_count"),
            "session_count": summary.get("session_count"),
            "write": summary.get("write"),
            "effects": summary.get("effects"),
        },
        "replays": replays,
        "safety_contract": {
            "replay_mode": "read-only-reconstruction",
            "session_reexecuted": False,
            "adapter_reinvoked": False,
            "audit_log_written": False,
            "audit_line_count_unchanged": True,
            "background_worker": False,
            "automatic_remediation": False,
        },
        "issue_count": len(issues),
        "issues": issues,
    }

    if not keep_tmp and TEMP_ROOT.exists():
        shutil.rmtree(TEMP_ROOT)

    return result


def collect_forbidden_effects(value, path, violations):
    if isinstance(value, dict):
        effects = value.get("effects")
        if isinstance(effects, dict):
            for key in FORBIDDEN_TRUE_EFFECTS:
                if effects.get(key) is True:
                    violations.append({"path": f"{path}.effects.{key}", "effect": key})
        for key, child in value.items():
            collect_forbidden_effects(child, f"{path}.{key}", violations)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_forbidden_effects(child, f"{path}[{index}]", violations)


def _issue(code, message):
    return {"code": code, "message": message}


def render_table(payload):
    lines = [
        f"regression_version: {payload['regression_version']}",
        f"status: {payload['status']}",
        f"mode: {payload['mode']}",
        f"scale: {payload['scale']}",
        f"write: {payload['write']}",
        f"iterations: {payload['iterations']}",
        f"seed_session_id: {payload['seed']['session_id']}",
        f"audit_lines_before: {payload['audit_before']['line_count']}",
        f"audit_lines_after: {payload['audit_after']['line_count']}",
        f"issue_count: {payload['issue_count']}",
        "replays:",
    ]
    for replay in payload["replays"]:
        lines.append(
            f"  - run={replay['run_index']} status={replay['status']} "
            f"mode={replay['mode']} lines_after={replay['audit_lines_after']}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Replay safety regression: ensure replay reconstructs provenance without re-execution."
    )
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--keep-tmp", action="store_true")
    parser.add_argument("--format", choices=OUTPUT_CHOICES, default="json")

    args = parser.parse_args()
    payload = build_regression(iterations=args.iterations, timeout=args.timeout, keep_tmp=args.keep_tmp)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_table(payload))


if __name__ == "__main__":
    main()
