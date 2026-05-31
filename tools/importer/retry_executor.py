from typing import Dict, Any


def build_compact_retry_prompt(
    original_question: str,
    context_text: str,
    failed_answer: str = "",
    retry_reason: str = "",
) -> str:
    original_question = (original_question or "").strip()
    context_text = (context_text or "").strip()
    failed_answer = (failed_answer or "").strip()
    retry_reason = (retry_reason or "").strip()

    return f"""You are generating a final answer for a local personal RAG system.

Rules:
- Answer in the same language as the user question.
- Do not show reasoning.
- Do not explain your process.
- Use only the provided context.
- Keep the answer concise.
- Include citations like [Source 1] when using context.
- Use only Source numbers that appear in the provided context.
- Do not invent Source numbers.
- If the context only contains [Source 1], do not cite [Source 2] or higher.
- Produce a complete natural-language answer.
- Citation-only answers are invalid.
- The answer must contain at least one factual sentence before citations.
- Produce final answer only.

Retry reason:
{retry_reason}

User question:
{original_question}

Context:
{context_text}

Previous incomplete answer:
{failed_answer}

Final answer:
"""


if __name__ == "__main__":
    print(build_compact_retry_prompt(
        original_question="Telegram integration 是什麼？",
        context_text="[Source 1] Telegram integration is an ingress channel.",
        failed_answer="Telegram integration 是 Hermes",
        retry_reason="quality_issue:ends_mid_sentence",
    ))
