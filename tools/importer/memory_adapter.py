import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path.home() / "workspace" / "hermes-memory"
RECALL = ROOT / "bin" / "hermes-recall"


def run_recall(args) -> dict:
    cmd = [
        str(RECALL),
        args.query,
        "--project",
        args.project,
        "--schema",
        args.schema,
        "--mode",
        args.mode,
        "--limit",
        str(args.limit),
        "--candidate-limit",
        str(args.candidate_limit),
        "--max-content-length",
        str(args.max_content_length),
        "--json",
    ]

    if args.path:
        cmd.extend(["--path", args.path])

    proc = subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True,
    )

    return json.loads(proc.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hermes memory adapter JSON contract."
    )
    parser.add_argument("query")
    parser.add_argument("--project", default="k6-freelancer")
    parser.add_argument("--schema", default="public")
    parser.add_argument("--mode", default="hybrid", choices=["hybrid", "vector", "fts"])
    parser.add_argument("--path")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=20)
    parser.add_argument("--max-content-length", type=int, default=1200)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    recall = run_recall(args)

    context = []

    for i, item in enumerate(recall.get("results", []), start=1):
        score = (
            item.get("hybrid_score")
            or item.get("score")
            or item.get("vector_score")
            or item.get("fts_score")
        )

        context.append(
            {
                "rank": i,
                "source": item.get("path"),
                "chunk_id": item.get("chunk_id"),
                "chunk_index": item.get("chunk_index"),
                "score": score,
                "scores": {
                    "hybrid_score": item.get("hybrid_score"),
                    "vector_score": item.get("vector_score"),
                    "fts_score": item.get("fts_score"),
                    "vector_rank": item.get("vector_rank"),
                    "fts_rank": item.get("fts_rank"),
                },
                "content": item.get("content", ""),
                "content_truncated": item.get("content_truncated", False),
            }
        )

    result = {
        "status": "pass",
        "adapter": "hermes-memory-adapter",
        "contract_version": "0.1",
        "query": args.query,
        "project": args.project,
        "schema": args.schema,
        "mode": args.mode,
        "path": args.path,
        "limit": args.limit,
        "context_count": len(context),
        "context": context,
        "source_recall": {
            "status": recall.get("status"),
            "fusion": recall.get("fusion"),
            "model": recall.get("model"),
        },
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
