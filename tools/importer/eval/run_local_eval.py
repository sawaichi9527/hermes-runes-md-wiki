from pathlib import Path
import json
import subprocess
import sys
import yaml

ROOT = Path.home() / "workspace/hermes-memory"
IMPORTER = ROOT / "tools/importer"
EVAL_SET = IMPORTER / "eval/local_eval_set.yaml"


def fail(msg):
    print(json.dumps({
        "suite": "M9.1 Local Eval Set",
        "status": "FAIL",
        "error": msg,
    }, ensure_ascii=False, indent=2))
    sys.exit(1)


def run_answer(case):
    cmd = [
        sys.executable,
        "answer_generator.py",
        case["question"],
        "--project", case.get("project", "k6-freelancer"),
        "--path", case["path"],
        "--heading", case["heading"],
        "--max-tokens", "768",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.returncode != 0:
        stderr = proc.stderr or ""
        failure_kind = "generation_failure"
        if "finish_reason" in stderr and "length" in stderr:
            failure_kind = "generation_length_failure"

        return {
            "id": case["id"],
            "type": case.get("type"),
            "status": "FAIL",
            "reason": "answer_generator_failed",
            "failure_kind": failure_kind,
            "stderr_tail": stderr[-800:],
        }

    try:
        data = json.loads(proc.stdout)
    except Exception as e:
        return {
            "id": case["id"],
            "status": "FAIL",
            "reason": f"invalid_json: {e}",
            "stdout": proc.stdout[-500:],
        }

    answer = data.get("answer") or ""
    context_debug = data.get("context_debug") or {}
    selected = context_debug.get("selected_chunks", 0)

    missing_terms = [
        term for term in case.get("must_contain", [])
        if term.lower() not in answer.lower()
    ]

    missing_any_groups = []
    answer_lower = answer.lower()

    for group in case.get("must_contain_any", []):
        if not any(str(term).lower() in answer_lower for term in group):
            missing_any_groups.append(group)

    if not answer:
        return {
            "id": case["id"],
            "status": "FAIL",
            "reason": "empty_answer",
            "data": data,
        }

    if selected <= 0:
        return {
            "id": case["id"],
            "status": "FAIL",
            "reason": "no_selected_context",
            "data": data,
        }

    if missing_terms or missing_any_groups:
        return {
            "id": case["id"],
            "status": "FAIL",
            "reason": "missing_must_contain",
            "missing_terms": missing_terms,
            "missing_any_groups": missing_any_groups,
            "answer_preview": answer[:240],
            "data": data,
        }

    retrieval_summary = data.get(
        "retrieval_summary",
        {}
    ) or {}

    return {
        "id": case["id"],
        "type": case.get("type"),
        "status": "PASS",

        "selected_model_profile": data.get(
            "selected_model_profile"
        ),

        "retrieval_profile": retrieval_summary.get(
            "retrieval_profile"
        ),

        "top_heading": retrieval_summary.get(
            "top_heading"
        ),

        "top_profile_bias": retrieval_summary.get(
            "top_profile_bias"
        ),

        "retrieval_bias_applied": retrieval_summary.get(
            "retrieval_bias_applied"
        ),

        "extraction_quality_ok": data.get(
            "extraction_quality_ok"
        ),

        "quality_issues": data.get(
            "quality_issues"
        ),

        "risk_signals": data.get(
            "risk_signals"
        ),

        "retry_should_run": data.get(
            "retry_should_run"
        ),

        "answer_chars": data.get(
            "answer_chars"
        ),

        "answer_preview": answer[:180],
    }


def main():
    if not EVAL_SET.exists():
        fail(f"missing eval set: {EVAL_SET}")

    cases = yaml.safe_load(EVAL_SET.read_text(encoding="utf-8")).get("cases", [])
    if not cases:
        fail("no eval cases")

    results = [run_answer(case) for case in cases]
    failed = [r for r in results if r.get("status") != "PASS"]

    print(json.dumps({
        "suite": "M9.1 Local Eval Set",
        "status": "PASS" if not failed else "FAIL",
        "total": len(results),
        "failed": len(failed),
        "results": results,
    }, ensure_ascii=False, indent=2))

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
