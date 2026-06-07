from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Iterable

ALLOWED_PROJECTS = {"sample-project", "freelancer", "k6-freelancer"}
BLOCKED_NAMES = {"tmp", "logs", "observations"}


def git_changed_files(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    files: list[str] = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        files.append(path)
    return files


def project_from_path(path: str) -> str | None:
    parts = Path(path).parts
    if len(parts) >= 3 and parts[0] == "wiki":
        return parts[1]
    return None


def preview_path(path: str) -> dict:
    p = Path(path)
    project = project_from_path(path)
    reasons: list[str] = []
    include = True

    if p.suffix != ".md":
        include = False
        reasons.append("not_markdown")

    if not path.startswith("wiki/"):
        include = False
        reasons.append("outside_wiki")

    if any(part in BLOCKED_NAMES for part in p.parts):
        include = False
        reasons.append("blocked_runtime_path")

    if "manifest" in p.name.lower():
        include = False
        reasons.append("manifest_like_file")

    if project is None:
        include = False
        reasons.append("missing_project_namespace")
    elif project not in ALLOWED_PROJECTS:
        include = False
        reasons.append("blocked_project_namespace")

    if include:
        reasons.append("eligible_markdown_wiki_file")

    return {
        "path": path,
        "project": project,
        "include": include,
        "reasons": reasons,
        "mode": "preview-only",
        "db_write": False,
        "chunk_create": False,
        "index_update": False,
    }


def expand_project(root: Path, project: str) -> Iterable[str]:
    base = root / "wiki" / project
    if not base.exists():
        return []
    return [str(path.relative_to(root)) for path in sorted(base.glob("*.md"))]


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only importer preview helper.")
    parser.add_argument("--changed-files", action="store_true")
    parser.add_argument("--project")
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    candidates: list[str] = []

    if args.changed_files:
        candidates.extend(git_changed_files(root))

    if args.project:
        candidates.extend(expand_project(root, args.project))

    candidates.extend(args.path)

    # Preserve order while de-duplicating.
    candidates = list(dict.fromkeys(candidates))
    results = [preview_path(path) for path in candidates]

    payload = {
        "status": "PASS",
        "mode": "preview-only",
        "count": len(results),
        "results": results,
        "db_write": False,
        "chunk_create": False,
        "index_update": False,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"PASS: importer preview candidates={len(results)}")
        for item in results:
            decision = "include" if item["include"] else "exclude"
            print(f"{decision}: {item['path']} reasons={','.join(item['reasons'])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
