#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

IMPORTER_PARENT = Path(__file__).resolve().parents[1]
if str(IMPORTER_PARENT) not in sys.path:
    sys.path.insert(0, str(IMPORTER_PARENT))


# M93.3 hardening:
# M10 is a checkout-local smoke by default.  Do not let a stale exported
# HERMES_MEMORY_ROOT from another shell/session redirect this smoke to a
# different clone.  Use HERMES_M10_SMOKE_ROOT only for an explicit override.
def resolve_smoke_root() -> Path:
    explicit_root = os.environ.get("HERMES_M10_SMOKE_ROOT")
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()

    # tools/importer/smoke/eval_smoke_m10_observation.py -> repo root
    return Path(__file__).resolve().parents[3]


ROOT = resolve_smoke_root()
IMPORTER = ROOT / "tools" / "importer"
MODEL_ENV_KEYS = ("OPENAI_BASE_URL", "OPENAI_MODEL")
ENV_PATHS = (ROOT / ".env", IMPORTER / ".env")


def load_env_file(path: Path) -> list[str]:
    loaded = []
    if not path.exists():
        return loaded

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value
            loaded.append(key)

    return loaded


def env_source_summary() -> list[dict[str, object]]:
    return [
        {
            "path": str(path),
            "exists": path.exists(),
        }
        for path in ENV_PATHS
    ]


def missing_model_env() -> tuple[list[str], list[str]]:
    loaded = []
    for path in ENV_PATHS:
        loaded.extend(load_env_file(path))
    missing = [key for key in MODEL_ENV_KEYS if not os.environ.get(key)]
    return missing, sorted(set(loaded))


def workspace_slug() -> str:
    return (
        os.environ.get("HERMES_SMOKE_PROJECT")
        or os.environ.get("HERMES_PROJECT")
        or os.environ.get("HERMES_WORKSPACE_SLUG")
        or "k6-freelancer"
    ).strip()


def answer_case() -> dict[str, str]:
    workspace = workspace_slug()

    if workspace in ("", "k6-freelancer"):
        return {
            "profile": "legacy-k6-freelancer",
            "query": "Telegram integration 是什麼？",
            "project": "k6-freelancer",
            "path": "services.md",
            "heading": "Telegram",
        }

    return {
        "profile": f"workspace-{workspace}",
        "query": "Trial-run Workspace Baseline 是什麼？",
        "project": workspace,
        "path": f"wiki/{workspace}",
        "heading": "Trial-run Workspace Baseline",
    }


def source_count(answer: str) -> int:
    citations = set()
    for m in re.finditer(r"\[Source\s+(\d+)\]", answer or ""):
        citations.add(int(m.group(1)))
    return len(citations)


def main():
    case = answer_case()
    missing, loaded_keys = missing_model_env()

    if missing:
        print(json.dumps({
            "suite": "M10 Observation Log Smoke Test",
            "profile": case["profile"],
            "status": "SKIP",
            "reason": "missing_model_env",
            "root": str(ROOT),
            "importer": str(IMPORTER),
            "env_files": env_source_summary(),
            "loaded_keys": loaded_keys,
            "missing": missing,
            "message": "OPENAI-compatible model env is not configured; skipping answer generation smoke.",
        }, ensure_ascii=False, indent=2))
        return

    cmd = [
        sys.executable,
        "answer_generator.py",
        case["query"],
        "--project", case["project"],
        "--path", case["path"],
        "--heading", case["heading"],
        "--max-tokens", "512",
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )

    if proc.returncode != 0:
        print(json.dumps({
            "suite": "M10 Observation Log Smoke Test",
            "profile": case["profile"],
            "status": "FAIL",
            "step": "answer_generator",
            "root": str(ROOT),
            "importer": str(IMPORTER),
            "env_files": env_source_summary(),
            "loaded_keys": loaded_keys,
            "returncode": proc.returncode,
            "stderr_tail": proc.stderr[-2000:],
        }, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    data = json.loads(proc.stdout)
    answer = data.get("answer") or ""
    expected_citations = source_count(answer)

    issues = []

    if not answer.strip():
        issues.append("answer_empty")

    if data.get("answer_chars") != len(answer):
        issues.append("answer_chars_mismatch")

    if data.get("citation_count") != expected_citations:
        issues.append("citation_count_mismatch_final_answer")

    if expected_citations > 0 and data.get("citation_integrity_ok") is not True:
        citation_issues = data.get("citation_issues") or []
        if "invalid_citation_reference" in citation_issues:
            issues.append("invalid_citation_reference")
        elif "missing_citation" in citation_issues:
            issues.append("missing_citation_despite_sources")
        else:
            issues.append("citation_integrity_false_with_sources")

    if data.get("retry_executed") and data.get("retry_success"):
        if data.get("answer_chars") != len(answer):
            issues.append("retry_final_answer_chars_mismatch")

    output = {
        "suite": "M10 Observation Log Smoke Test",
        "profile": case["profile"],
        "status": "FAIL" if issues else "PASS",
        "issues": issues,
        "root": str(ROOT),
        "importer": str(IMPORTER),
        "env_files": env_source_summary(),
        "loaded_keys": loaded_keys,
        "case": case,
        "summary": {
            "answer_chars": data.get("answer_chars"),
            "actual_chars": len(answer),
            "citation_count": data.get("citation_count"),
            "expected_citations": expected_citations,
            "citation_integrity_ok": data.get("citation_integrity_ok"),
            "retry_executed": data.get("retry_executed"),
            "retry_success": data.get("retry_success"),
            "selected_model_profile": data.get("selected_model_profile"),
            "extraction_path": data.get("extraction_path"),
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
