import re
from typing import Dict, Any, List


SOURCE_RE = re.compile(r"\[Source\s+(\d+)\]")


def extract_citations(answer: str) -> List[int]:
    answer = answer or ""

    out = []

    for m in SOURCE_RE.finditer(answer):
        try:
            out.append(int(m.group(1)))
        except Exception:
            pass

    return sorted(set(out))


def evaluate_citation_integrity(
    answer: str,
    selected_chunks_count: int,
) -> Dict[str, Any]:
    answer = (answer or "").strip()

    issues = []

    citations = extract_citations(answer)

    invalid = []

    for n in citations:
        if n < 1 or n > selected_chunks_count:
            invalid.append(n)

    if invalid:
        issues.append("invalid_citation_reference")

    # Missing citation heuristic.
    has_citation = len(citations) > 0

    if answer and not has_citation:
        issues.append("missing_citation")

    # Dangling citation fragments.
    if re.search(r"\[S(?:o(?:u(?:r(?:c(?:e)?)?)?)?)?$", answer):
        issues.append("dangling_citation_fragment")

    ok = len(issues) == 0

    return {
        "ok": ok,
        "issues": issues,
        "citation_count": len(citations),
        "citations": citations,
        "invalid_citations": invalid,
        "missing_citation": "missing_citation" in issues,
    }


if __name__ == "__main__":
    import json

    samples = [
        {
            "name": "good",
            "answer": "Telegram integration 是入口通道 [Source 1]。",
            "chunks": 1,
        },
        {
            "name": "invalid",
            "answer": "Telegram integration [Source 3]",
            "chunks": 1,
        },
        {
            "name": "missing",
            "answer": "Telegram integration 是入口通道。",
            "chunks": 1,
        },
    ]

    for s in samples:
        result = evaluate_citation_integrity(
            answer=s["answer"],
            selected_chunks_count=s["chunks"],
        )

        print(json.dumps({
            "sample": s["name"],
            **result,
        }, ensure_ascii=False))
