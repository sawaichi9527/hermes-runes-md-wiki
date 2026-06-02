import json
import os
from datetime import datetime
from pathlib import Path

from root_resolver import resolve_root


ROOT = resolve_root()
OBS_ROOT = ROOT / "logs/observations"


def _safe_preview(text: str, limit: int = 240) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = " ".join(text.split())
    return text[:limit]


def write_observation(data: dict) -> None:
    """
    Best-effort local observation logger.

    Rules:
    - Never raise.
    - Do not log full prompt.
    - Do not log full answer.
    - Do not log full memory context.
    - Do not ingest these logs into RAG.
    """

    try:
        now = datetime.now()
        month_dir = OBS_ROOT / now.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)

        log_path = month_dir / f"{now.strftime('%Y%m%d')}.jsonl"

        if data.get("event"):
            allowed_keys = {
                "event",
                "milestone",
                "suite",
                "status",
                "failed",
                "total",
                "reviewed_proposal_visible",
                "reviewed_trust_bias",
                "trusted_wiki_outranks_reviewed",
                "trusted_top_path",
                "reviewed_proposal_path",
                "trust_policy",
            }

            event = {
                "ts": now.isoformat(timespec="seconds"),
            }

            for key in allowed_keys:
                if key in data:
                    event[key] = data.get(key)
        else:
            answer = data.get("answer") or ""

            event = {
                "ts": now.isoformat(timespec="seconds"),
                "model": data.get("model"),
                "selected_model_profile": data.get("selected_model_profile"),
                "extraction_path": data.get("extraction_path"),
                "finish_reason": data.get("finish_reason"),
                "extraction_quality_ok": data.get("extraction_quality_ok"),
                "quality_issues": data.get("quality_issues") or [],
                "risk_signals": data.get("risk_signals") or [],
                "completeness_ok": data.get("completeness_ok"),
                "completeness_issues": data.get("completeness_issues") or [],
                "citation_integrity_ok": data.get("citation_integrity_ok"),
                "citation_issues": data.get("citation_issues") or [],
                "retry_should_run": data.get("retry_should_run"),
                "retry_reason": data.get("retry_reason"),
                "retry_executed": data.get("retry_executed"),
                "retry_success": data.get("retry_success"),
                "answer_chars": len(answer),
                "answer_preview": _safe_preview(answer),
            }

        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    except Exception:
        return
