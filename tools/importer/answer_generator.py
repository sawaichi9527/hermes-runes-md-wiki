from response_sanitizer import sanitize_answer
from extraction_cleanup import cleanup_extracted_answer
from observation_logger import write_observation
#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

from model_profiles import load_model_profiles, select_model_profile
from extraction_quality import evaluate_extraction_quality
from retry_policy import decide_retry
from retry_executor import build_compact_retry_prompt
from retry_validation import validate_retry_answer
from completeness_heuristic import evaluate_completeness
from citation_checker import evaluate_citation_integrity
from extraction_templates import extract_from_reasoning
from cleanup_patterns import PROFILE_CLEANUP_PATTERNS
from answer_boundaries import truncate_at_answer_boundary
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def run_prompt_builder(args):
    cmd = [
        sys.executable,
        str(BASE_DIR / "prompt_builder.py"),
        args.query,
        "--project",
        args.project,
        "--schema",
        args.schema,
        "--limit",
        str(args.limit),
        "--candidates",
        str(args.candidates),
        "--max-chars",
        str(args.max_chars),
        "--per-chunk-chars",
        str(args.per_chunk_chars),
        "--min-rerank-score",
        str(args.min_rerank_score),
        "--json",
    ]

    if args.path:
        cmd += ["--path", args.path]

    if args.heading:
        cmd += ["--heading", args.heading]

    if args.retrieval_query:
        cmd += ["--retrieval-query", args.retrieval_query]

    proc = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)

    return json.loads(proc.stdout)


def call_llm(prompt: str, args):
    load_dotenv(ENV_FILE)

    if args.no_think:
        prompt = "/no_think\n\n" + prompt

    base_url = os.getenv("OPENAI_BASE_URL", "").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "")
    api_key = os.getenv("OPENAI_API_KEY", "not-needed")
    auth_mode = os.getenv("OPENAI_AUTH_MODE", "auto").strip().lower()

    if auth_mode not in {"auto", "none", "bearer"}:
        raise SystemExit("ERROR: OPENAI_AUTH_MODE must be one of: auto, none, bearer")

    if not base_url or not model:
        raise SystemExit("ERROR: OPENAI_BASE_URL and OPENAI_MODEL must be set in .env")

    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are Hermes Memory Assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
    }

    placeholder_keys = {"", "not-needed", "not-set", "none", "null", "local"}
    should_send_auth = (
        auth_mode == "bearer"
        or (
            auth_mode == "auto"
            and api_key.strip().lower() not in placeholder_keys
        )
    )

    if should_send_auth:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:
        raise SystemExit(f"ERROR: LLM request failed: {e}")

    return json.loads(raw)


def execute_bounded_retry(
    args,
    prompt_payload,
    failed_answer,
    retry_reason,
):
    context_text = prompt_payload.get("context_text", "")

    retry_prompt = build_compact_retry_prompt(
        original_question=args.query,
        context_text=context_text,
        failed_answer=failed_answer,
        retry_reason=retry_reason,
    )

    retry_payload = call_llm(retry_prompt, args)

    retry_answer = cleanup_answer(
        extract_answer(retry_payload)
    )

    return {
        "retry_payload": retry_payload,
        "retry_answer": retry_answer,
    }


def cleanup_answer(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    text = truncate_at_answer_boundary(text)

    # Qwen/HauhauCS may leak internal outline into final content.
    # Keep only text after the final "Synthesize Answer" marker.
    marker = "Synthesize Answer"
    idx = text.lower().rfind(marker.lower())
    if idx >= 0:
        tail = text[idx:]
        lines = tail.splitlines()

        if len(lines) >= 2:
            text = "\n".join(lines[1:]).strip()
        else:
            text = tail.replace(marker, "", 1).strip(" :*-")

    # Remove common reasoning contamination sections.
    contamination_patterns = [
        r"\n?4\.\s+\*\*Check Against Rules:\*\*.*",
        r"\n?5\.\s+\*\*Refine Output:\*\*.*",
        r"\n?Checks:.*",
        r"\n?Ready\.?✅?.*",
        r"\n?Output matches.*",
        r"\n?Proceeds\..*",
    ]

    for pattern in contamination_patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.DOTALL,
        ).strip()

    # Remove leftover markdown heading wrappers if any.
    text = re.sub(
        r"^\s*(?:\d+\.\s*)?\*\*[^*]*\*\*:\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    # Fallback: if a final Chinese answer starts later, trim prior analysis.
    final_patterns = [
        r"Telegram integration\s+是",
        r"Telegram Integration\s+是",
        r"作為\s+Hermes",
        r"僅作為",
        r"-\s*Role/Purpose:",
    ]

    for pat in final_patterns:
        m = re.search(pat, text)
        if m and m.start() > 0:
            text = text[m.start():].strip()
            break

    return text.strip()


def get_finish_reason(payload) -> str:
    try:
        return payload["choices"][0].get("finish_reason", "")
    except Exception:
        return ""


def detect_extraction_path(payload, answer: str) -> dict:
    try:
        msg = payload["choices"][0]["message"]
        content = (msg.get("content") or "").strip()
        reasoning = msg.get("reasoning_content") or ""

        if content:
            return {
                "extraction_path": "message.content",
                "reasoning_fallback_used": False,
            }

        if answer and "Draft Response" in reasoning:
            return {
                "extraction_path": "reasoning_content.draft_response",
                "reasoning_fallback_used": True,
            }

        if answer and "Synthesize Answer" in reasoning:
            return {
                "extraction_path": "reasoning_content.synthesize_answer",
                "reasoning_fallback_used": True,
            }

        if answer and reasoning:
            return {
                "extraction_path": "reasoning_content.unknown",
                "reasoning_fallback_used": True,
            }

        return {
            "extraction_path": "empty",
            "reasoning_fallback_used": False,
        }
    except Exception:
        return {
            "extraction_path": "error",
            "reasoning_fallback_used": False,
        }


def trim_incomplete_answer_tail(text: str) -> str:
    text = (text or "").rstrip()

    # Remove truncated citation fragments.
    text = re.sub(r"\s*\[S(?:o(?:u(?:r(?:c(?:e(?:\s*\d*)?)?)?)?)?)?$", "", text).rstrip()
    text = re.sub(r"\s*\[Source\s+\d*$", "", text).rstrip()
    text = re.sub(r"\s*\[$", "", text).rstrip()

    # Remove dangling markdown bullet/header fragments.
    text = re.sub(r"\n\s*[-*]\s*\*{0,2}$", "", text).rstrip()
    text = re.sub(r"\n\s*[-*]\s+\*\*[^：:]{0,20}$", "", text).rstrip()

    # If cut mid-sentence, keep the last complete sentence.
    terminal_marks = ["。", "！", "？", ".", "!", "?"]
    if text and not any(text.endswith(mark) for mark in terminal_marks):
        last_pos = max(text.rfind(mark) for mark in terminal_marks)
        if last_pos > 40:
            text = text[:last_pos + 1].rstrip()

    for suffix in ("`", "**", "__", "~~"):
        if text.endswith(suffix):
            text = text[:-len(suffix)].rstrip()

    return text.strip()


def extract_answer(payload, selected_profile=None):
    try:
        selected_profile = selected_profile or {}
        extraction = selected_profile.get("extraction", {})
        allow_reasoning_fallback = extraction.get("allow_reasoning_fallback", False)
        max_reasoning_fallback_chars = int(extraction.get("max_reasoning_fallback_chars", 0) or 0)

        msg = payload["choices"][0]["message"]

        content = msg.get("content", "")
        if content and content.strip():
            return content.strip()

        # M8.4 model-aware gate:
        # reasoning_content fallback is allowed only by selected model profile.
        if not allow_reasoning_fallback:
            return ""

        # Some thinking models may place the complete draft in reasoning_content
        # and stop before emitting final assistant content.
        reasoning = msg.get("reasoning_content", "")

        profile_name = selected_profile.get("_profile_name", "")

        extracted = extract_from_reasoning(
            reasoning=reasoning,
            profile_name=profile_name,
        )

        if extracted:
            return extracted.strip()
        if reasoning:
            marker = "Internal Draft in Traditional Chinese):"
            if marker in reasoning:
                draft = reasoning.split(marker, 1)[1]
                draft = draft.split("\n\n4.", 1)[0]
                draft = draft.strip()
                if draft:
                    if max_reasoning_fallback_chars > 0:
                        draft = draft[:max_reasoning_fallback_chars].strip()
                    return draft

            marker = "Synthesize Answer"
            if marker in reasoning and "[Source" in reasoning:
                lines = []
                capture = False
                for line in reasoning.splitlines():
                    if "Telegram integration" in line or "Telegram Integration" in line:
                        capture = True
                    if capture:
                        if line.strip().startswith(("4.", "5.", "Check against Rules")):
                            break
                        if line.strip():
                            lines.append(line.strip())
                draft = "\n".join(lines).strip()
                if draft:
                    if max_reasoning_fallback_chars > 0:
                        draft = draft[:max_reasoning_fallback_chars].strip()
                    return draft

            marker = "Draft Response"
            if marker in reasoning:
                draft = reasoning.split(marker, 1)[1]
                draft = draft.split("\n\n6.", 1)[0]
                draft = draft.strip()

                # Remove markdown heading residue such as "**:" if present.
                if draft.startswith("(Mental Refinement):"):
                    draft = draft.split(":", 1)[1].strip()
                if draft.startswith("**"):
                    draft = draft.split("\n", 1)[1].strip() if "\n" in draft else draft.strip("*: ")

                if draft:
                    if max_reasoning_fallback_chars > 0:
                        draft = draft[:max_reasoning_fallback_chars].strip()
                    return draft

        return ""
    except Exception:
        return ""


def main():
    parser = argparse.ArgumentParser(description="Hermes Memory Answer Generator MVP")
    parser.add_argument("query")
    parser.add_argument("--project", required=True)
    parser.add_argument("--schema", default="public")
    parser.add_argument("--path", default=None)
    parser.add_argument("--heading", default=None)
    parser.add_argument("--retrieval-query", default=None)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidates", type=int, default=10)
    parser.add_argument("--max-chars", type=int, default=8000)
    parser.add_argument("--per-chunk-chars", type=int, default=2500)
    parser.add_argument("--min-rerank-score", type=float, default=8.0)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--no-think", action="store_true", default=True)
    parser.add_argument("--show-raw-on-empty", action="store_true", default=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    prompt_payload = run_prompt_builder(args)
    llm_payload = call_llm(prompt_payload["prompt"], args)

    context_debug = prompt_payload.get("context_debug", {}) or {}

    retrieval_summary = {
        "retrieval_profile": context_debug.get("retrieval_profile"),
        "top_heading": context_debug.get("top_heading"),
        "top_profile_bias": context_debug.get("top_profile_bias"),
        "retrieval_bias_applied": bool(
            (context_debug.get("top_profile_bias") or 0) > 0
        ),
    }

    model_name = llm_payload.get("model") or getattr(args, "model", "")
    profiles_data = load_model_profiles()
    selected_model_profile, selected_profile = select_model_profile(model_name, profiles_data)

    selected_profile["_profile_name"] = selected_model_profile

    answer = cleanup_answer(extract_answer(llm_payload, selected_profile))
    answer = trim_incomplete_answer_tail(answer)
    extraction_meta = detect_extraction_path(llm_payload, answer)
    finish_reason = get_finish_reason(llm_payload)
    extraction_quality = evaluate_extraction_quality(
        answer=answer,
        finish_reason=finish_reason,
        extraction_path=extraction_meta.get("extraction_path"),
        reasoning_fallback_used=extraction_meta.get("reasoning_fallback_used"),
    )

    completeness = evaluate_completeness(
        question=args.query,
        answer=answer,
    )

    citation_integrity = evaluate_citation_integrity(
        answer=answer,
        selected_chunks_count=prompt_payload.get(
            "context_debug", {}
        ).get("selected_chunks", 0),
    )
    merged_quality = dict(extraction_quality)

    merged_quality["quality_issues"] = (
        extraction_quality.get("quality_issues", [])
        + completeness.get("issues", [])
    )

    merged_quality["ok"] = (
        extraction_quality.get("ok")
        and completeness.get("ok")
    )

    retry_policy = decide_retry(
        quality=merged_quality,
        selected_model_profile=selected_model_profile,
        retry_count=0,
        max_retries=1,
    )

    retry_executed = False
    retry_success = False

    if retry_policy.get("retry_should_run"):
        retry_result = execute_bounded_retry(
            args=args,
            prompt_payload=prompt_payload,
            failed_answer=answer,
            retry_reason=retry_policy.get("retry_reason", ""),
        )

        retry_answer = retry_result.get("retry_answer", "").strip()

        retry_executed = True

        retry_validation = validate_retry_answer(retry_answer)

        if retry_validation.get("ok"):
            answer = retry_answer
            retry_success = True
        else:
            retry_success = False

    initial_answer_empty = not bool(answer.strip())

    final_answer_empty = not bool(answer.strip())

    citation_integrity = evaluate_citation_integrity(
        answer=answer,
        selected_chunks_count=prompt_payload.get(
            "context_debug", {}
        ).get("selected_chunks", 0),
    )

    if final_answer_empty and args.show_raw_on_empty:
        print("ERROR: final answer still empty after governance pipeline", file=sys.stderr)
        print(json.dumps(llm_payload, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(1)

    final_answer = sanitize_answer(cleanup_extracted_answer(answer))

    result = {
        "query": args.query,
        "retrieval_query": prompt_payload.get("retrieval_query"),
        "project": args.project,
        "path": args.path,
        "heading": args.heading,
        "answer": final_answer,
        "selected_model_profile": selected_model_profile,
        "initial_answer_empty": initial_answer_empty,
        "final_answer_empty": final_answer_empty,
        "extraction_path": extraction_meta.get("extraction_path"),
        "reasoning_fallback_used": extraction_meta.get("reasoning_fallback_used"),
        "finish_reason": finish_reason,
        "extraction_quality_ok": extraction_quality.get("ok"),
        "extraction_quality_issues": extraction_quality.get("issues"),
        "quality_issues": extraction_quality.get("quality_issues"),
        "risk_signals": extraction_quality.get("risk_signals"),
        "completeness_ok": completeness.get("ok"),
        "completeness_issues": completeness.get("issues"),

        "citation_integrity_ok": citation_integrity.get("ok"),
        "citation_issues": citation_integrity.get("issues"),
        "citation_count": citation_integrity.get("citation_count"),
        "invalid_citations": citation_integrity.get("invalid_citations"),

        "retry_should_run": retry_policy.get("retry_should_run"),
        "retry_reason": retry_policy.get("retry_reason"),
        "retry_mode": retry_policy.get("retry_mode"),
        "retry_executed": retry_executed,
        "retry_success": retry_success,
        "retry_validation_issues": (
            retry_validation.get("issues")
            if retry_executed else []
        ),
        "answer_chars": len(final_answer),
        "prompt_chars": prompt_payload.get("prompt_chars"),
        "retrieval_summary": retrieval_summary,
        "context_debug": prompt_payload.get("context_debug"),
        "model": os.getenv("OPENAI_MODEL"),
    }

    if args.json:
        write_observation(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.debug:
        print("=== DEBUG ===")
        print(json.dumps({k: v for k, v in result.items() if k != "answer"}, ensure_ascii=False, indent=2))
        print("")

    print(final_answer)


if __name__ == "__main__":
    main()
