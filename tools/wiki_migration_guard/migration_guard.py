#!/usr/bin/env python3
"""Minimal Runes Wiki migration guard.

Small local-first safety helper for existing installations. It protects the
wiki/ Markdown source-of-truth before repository updates.

This tool intentionally does not integrate with Runes Shield and does not do
schema migrations, merges, automatic restore, or user-owned Markdown edits.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SYSTEM_NAMES = {"README.md", "hermes_runes_index.md"}


class GuardError(RuntimeError):
    pass


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise GuardError(f"command failed: {' '.join(cmd)}\n{detail}")
    return proc


def repo_root() -> Path:
    proc = subprocess.run(["git", "rev-parse", "--show-toplevel"], text=True, capture_output=True)
    if proc.returncode != 0:
        raise GuardError("not inside a Git repository")
    return Path(proc.stdout.strip()).resolve()


def read_text_or_empty(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def git_head(root: Path) -> str:
    return run(["git", "rev-parse", "--short", "HEAD"], root).stdout.strip()


def current_branch(root: Path) -> str:
    return run(["git", "branch", "--show-current"], root).stdout.strip() or "main"


def upstream_ref(root: Path, remote: str, branch: str) -> str:
    proc = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], root, check=False)
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip()
    return f"{remote}/{branch}"


def git_status_lines(root: Path) -> list[str]:
    out = run(["git", "status", "--porcelain"], root).stdout
    return [line for line in out.splitlines() if line.strip()]


def fetch_remote(root: Path, remote: str) -> None:
    run(["git", "fetch", remote], root)


def incoming_files(root: Path, upstream: str) -> list[str]:
    proc = run(["git", "diff", "--name-only", f"HEAD..{upstream}"], root, check=False)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def classify(path: str, wiki_root: str) -> str:
    norm = path.replace("\\", "/").strip("/")
    root = wiki_root.strip("/")
    if norm == root or not norm.startswith(root + "/"):
        return "non-wiki"
    rel = norm[len(root) + 1 :]
    if rel.startswith("_system/"):
        return "system-ish"
    if "/" not in rel and rel in SYSTEM_NAMES:
        return "system-ish"
    return "user-ish"


def scan_wiki(root: Path, wiki_root: str) -> dict[str, Any]:
    wiki_path = root / wiki_root
    files: list[dict[str, str]] = []
    workspaces: list[str] = []
    if not wiki_path.exists():
        return {"exists": False, "workspaces": [], "files": []}

    for child in sorted(wiki_path.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and child.name != "_system":
            direct_md = list(child.glob("*.md"))
            if (child / "README.md").exists() or direct_md:
                workspaces.append(child.name)

    for md in sorted(wiki_path.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        files.append({"path": rel, "class": classify(rel, wiki_root)})

    return {"exists": True, "workspaces": workspaces, "files": files}


def make_plan(changed: list[str], wiki_root: str) -> dict[str, Any]:
    items = [{"path": p, "class": classify(p, wiki_root)} for p in changed]
    user_hits = [i for i in items if i["class"] == "user-ish"]
    system_hits = [i for i in items if i["class"] == "system-ish"]
    wiki_hits = [i for i in items if i["class"] != "non-wiki"]

    if user_hits:
        status = "STOP"
        reason = "incoming update touches possible user-owned wiki Markdown"
    elif system_hits:
        status = "CAUTION"
        reason = "incoming update touches system/index wiki Markdown only"
    elif changed:
        status = "SAFE"
        reason = "incoming update does not touch wiki Markdown"
    else:
        status = "SAFE"
        reason = "no incoming changes detected"

    return {
        "status": status,
        "reason": reason,
        "changed_files": changed,
        "wiki_changed_files": wiki_hits,
        "user_risk_files": user_hits,
        "system_wiki_files": system_hits,
    }


def unique_backup_root(root: Path) -> Path:
    base = root / "backups" / "wiki-migration-guard"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = base / stamp
    if not candidate.exists():
        return candidate

    for index in range(2, 1000):
        candidate = base / f"{stamp}-{index:02d}"
        if not candidate.exists():
            return candidate
    raise GuardError("unable to allocate unique backup directory")


def create_backup(root: Path, wiki_root: str, payload: dict[str, Any]) -> Path:
    backup_root = unique_backup_root(root)
    backup_root.mkdir(parents=True, exist_ok=False)

    wiki_path = root / wiki_root
    if wiki_path.exists():
        shutil.copytree(wiki_path, backup_root / wiki_root)

    (backup_root / "VERSION").write_text(read_text_or_empty(root / "VERSION") + "\n", encoding="utf-8")
    (backup_root / "git-head.txt").write_text(git_head(root) + "\n", encoding="utf-8")
    (backup_root / "report.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return backup_root


def print_text_report(payload: dict[str, Any]) -> None:
    print("Runes Wiki Migration Guard")
    print(f"Version: {payload.get('version') or 'unknown'}")
    print(f"Repo head: {payload.get('head') or 'unknown'}")
    print(f"Wiki root: {payload.get('wiki_root')}")
    if payload.get("backup"):
        print(f"Backup: {payload['backup']}")
    print("")

    workspaces = payload.get("scan", {}).get("workspaces", [])
    if workspaces:
        print("Detected workspaces:")
        for ws in workspaces:
            print(f"- {ws}")
        print("")

    dirty = payload.get("dirty", [])
    if dirty:
        print("Local changes detected:")
        for line in dirty:
            print(f"- {line}")
        print("")

    plan = payload.get("plan") or {}
    if plan:
        print(f"Status: {plan['status']}")
        print(f"Reason: {plan['reason']}")
        if plan.get("changed_files"):
            print("")
            print("Incoming changed files:")
            for path in plan["changed_files"]:
                print(f"- {path}")
        if plan.get("user_risk_files"):
            print("")
            print("Possible user-owned wiki files touched by incoming update:")
            for item in plan["user_risk_files"]:
                print(f"- {item['path']}")
    else:
        print("Status: SCAN")

    print("")
    print("Policy:")
    print("- Unknown wiki/**/*.md is treated as possible user-owned Markdown.")
    print("- This tool never overwrites user-owned Markdown.")
    print("- This tool is not part of Runes Shield.")


def build_payload(root: Path, args: argparse.Namespace, do_fetch: bool) -> dict[str, Any]:
    branch = args.branch or current_branch(root)
    upstream = upstream_ref(root, args.remote, branch)
    if do_fetch:
        fetch_remote(root, args.remote)
    changed = incoming_files(root, upstream)
    return {
        "schema_version": "runes-wiki-migration-guard-report-v1",
        "version": read_text_or_empty(root / "VERSION"),
        "head": git_head(root),
        "upstream": upstream,
        "wiki_root": args.wiki_root,
        "dirty": git_status_lines(root),
        "scan": scan_wiki(root, args.wiki_root),
        "plan": make_plan(changed, args.wiki_root),
    }


def command_plan(args: argparse.Namespace) -> int:
    root = repo_root()
    payload = build_payload(root, args, do_fetch=not args.no_fetch)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text_report(payload)
    return 0 if payload["plan"]["status"] != "STOP" else 2


def command_preflight(args: argparse.Namespace) -> int:
    root = repo_root()
    payload = build_payload(root, args, do_fetch=not args.no_fetch)
    backup = create_backup(root, args.wiki_root, payload)
    payload["backup"] = str(backup.relative_to(root))
    (backup / "report.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text_report(payload)
    return 0 if payload["plan"]["status"] != "STOP" else 2


def command_postflight(args: argparse.Namespace) -> int:
    root = repo_root()
    payload = {
        "schema_version": "runes-wiki-migration-guard-postflight-v1",
        "version": read_text_or_empty(root / "VERSION"),
        "head": git_head(root),
        "wiki_root": args.wiki_root,
        "dirty": git_status_lines(root),
        "scan": scan_wiki(root, args.wiki_root),
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text_report(payload)
    return 0


def command_update(args: argparse.Namespace) -> int:
    root = repo_root()
    payload = build_payload(root, args, do_fetch=not args.no_fetch)
    backup = create_backup(root, args.wiki_root, payload)
    payload["backup"] = str(backup.relative_to(root))
    (backup / "report.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if payload["dirty"]:
        payload["plan"]["status"] = "STOP"
        payload["plan"]["reason"] = "local working tree has changes; backup was created and update was not applied"

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text_report(payload)

    if payload["plan"]["status"] == "STOP":
        return 2
    if args.dry_run:
        print("Dry run: update not applied.")
        return 0

    print("Applying safe repository update with: git pull --ff-only")
    try:
        run(["git", "pull", "--ff-only"], root)
    except GuardError as exc:
        print(str(exc), file=sys.stderr)
        print("Backup is available for wiki/ review.", file=sys.stderr)
        return 1

    post_args = argparse.Namespace(wiki_root=args.wiki_root, json=args.json)
    return command_postflight(post_args)


def command_repair(args: argparse.Namespace) -> int:
    print("Repair is suggestion-only in this MVP.")
    print("Review backups under backups/wiki-migration-guard/ and restore files manually if needed.")
    print("No files were changed.")
    return 0


def add_common_options(p: argparse.ArgumentParser) -> None:
    p.add_argument("--wiki-root", default="wiki", help="Wiki root path relative to repo root. Default: wiki")
    p.add_argument("--remote", default="origin", help="Git remote to fetch. Default: origin")
    p.add_argument("--branch", default=None, help="Remote branch fallback. Default: current branch")
    p.add_argument("--no-fetch", action="store_true", help="Do not run git fetch before planning")
    p.add_argument("--json", action="store_true", help="Print JSON report")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="runes-wiki-migration-guard",
        description="Small local safety guard for wiki/ before Hermes Runes repository updates.",
    )
    add_common_options(p)
    sub = p.add_subparsers(dest="command")

    for name, help_text in [
        ("plan", "Fetch and show incoming update risk without backup or pull"),
        ("preflight", "Create a wiki/ backup and show incoming update risk"),
        ("postflight", "Scan current wiki/ after an update"),
        ("update", "Backup wiki/, check incoming changes, and pull only if safe"),
        ("repair", "Print repair guidance only; no automatic restore"),
    ]:
        sp = sub.add_parser(name, help=help_text)
        add_common_options(sp)
        if name == "update":
            sp.add_argument("--dry-run", action="store_true", help="Plan and backup, but do not pull")
        if name == "repair":
            sp.add_argument("--dry-run", action="store_true", help="Accepted for habit; repair is always dry-run in MVP")
    return p


def main() -> int:
    p = parser()
    args = p.parse_args()
    if not args.command:
        p.print_help()
        return 0

    try:
        if args.command == "plan":
            return command_plan(args)
        if args.command == "preflight":
            return command_preflight(args)
        if args.command == "postflight":
            return command_postflight(args)
        if args.command == "update":
            return command_update(args)
        if args.command == "repair":
            return command_repair(args)
    except GuardError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
