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
BUG_ID_LLM_ENDPOINT_GATE = "TB-M1989-FS001"


LLM_ENDPOINT_BLOCKER_PATTERNS = (
    "Connection refused",
    "[Errno 111]",
    "urlopen error",
    "timed out",
    "TimeoutError",
    "ConnectionError",
    "Max retries exceeded",
    "Name or service not known",
    "Temporary failure in name resolution",
    "Failed to establish a new connection",
)


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

    # v0.5.0-dev runtime seed smoke.
    # Historical Trial-run Workspace Baseline content is retained under
    # dev/wiki-history and is no longer a public runtime seed target.
    return {
        "profile": f"workspace-{workspace}",
        "query": "forge inbox boundary 是什麼？",
        "project": workspace,
        "path": f"wiki/{workspace}",
        "heading": "Boundaries",
    }


def source_count(answer: str) -> int:
    citations = set()
    for m in re.finditer(r"\[Source\s+(\d+)\]", answer or ""):
        citations.add(int(m.group(1)))
    return len(citations)


def m10_max_tokens() -> str:
    # M93.5: Qwen thinking-style local models may spend most of a 512-token
    # budget in reasoning_content and stop with finish_reason=length before a
    # final answer is emitted.  Keep this a smoke-local default, and allow a
    # simple local override without introducing model routing complexity.
    return os.environ.get("HERMES_M10_MAX_TOKENS", "1536")


def llm_endpoint_blocked(stderr: str) -> bool:
    text = stderr or ""
    return any(pattern in text for pattern in LLM_ENDPOINT_BLOCKER_PATTERNS)


def print_skip(case, loaded_keys, max_tokens, reason, message, **extra):
    print(json.dumps({
        "suite": "M10 Observation Log Smoke Test",
        "profile": case["profile"],
        "status": "SKIP",
        "reason": reason,
        "bug_id": BUG_ID_LLM_ENDPOINT_GATE,
        "root": str(ROOT),
        "importer": str(IMPORTER),
        "env_files": env_source_summary(),
        "loaded_keys": loaded_keys,
        "max_tokens": max_tokens,
        "case": case,
        "message": message,
        **extra,
    }, ensure_ascii=False, indent=2))


def main():
    case = answer_case()
    missing, loaded_keys = missing_model_env()
    max_tokens = m10_max_tokens()

    if missing:
        print_skip(
            case,
            loaded_keys,
            max_tokens,
            "missing_model_env",
            "OPENAI-compatible model env is not configured; skipping answer generation smoke.",
            missing=missing,
        )
        return

    cmd = [
        sys.executable,
        "answer_generator.py",
        case["query"],
        "--project", case["project"],
        "--path", case["path"],
        "--heading", case["heading"],
        "--max-tokens", max_tokens,
        "--json",
    ]

    proc = subprocess.run(
        cmd,
        cwd=IMPORTER,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )

    if proc.returncode != 0:
        if llm_endpoint_blocked(proc.stderr):
            print_skip(
                case,
                loaded_keys,
                max_tokens,
                "llm_endpoint_unavailable",
                "OPENAI-compatible endpoint is configured but unavailable; skipping answer generation smoke.",
                returncode=proc.returncode,
                stderr_tail=proc.stderr[-2000:],
            )
            return

        print(json.dumps({
            "suite": "M10 Observation Log Smoke Test",
            "profile": case["profile"],
            "status": "FAIL",
            "step": "answer_generator",
            "root": str(ROOT),
            "importer": str(IMPORTER),
            "env_files": env_source_summary(),
            "loaded_keys": loaded_keys,
            "max_tokens": max_tokens,
            "case": case,
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
        "max_tokens": max_tokens,
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
            "finish_reason": data.get("finish_reason"),
        },
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
