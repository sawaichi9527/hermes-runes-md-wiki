#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FORGE_INBOX = ROOT / "wiki" / "forge-inbox"


def forge_inboxes() -> list[Path]:
    paths = []
    default = DEFAULT_FORGE_INBOX
    if default.exists():
        paths.append(default)

    for path in sorted((ROOT / "wiki").glob("*/forge-inbox")):
        if path.is_dir() and path not in paths:
            paths.append(path)

    return paths

REQUIRED_DRAFT = {
    "proposal_type": "agent_memory",
    "trust_class": "unverified",
    "status": "draft",
}

APPROVED_UPDATES = {
    "trust_class": "reviewed",
    "status": "approved",
    "reviewed_by": "human",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def frontmatter(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")

    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")

    raw = text[4:end]
    body = text[end + 5:]

    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")

    return data, raw, body


def replace_or_add(raw: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^({re.escape(key)}\s*:\s*).*$", re.MULTILINE)
    line = f"{key}: {value}"
    if pattern.search(raw):
        return pattern.sub(line, raw)
    if raw.strip():
        return raw.rstrip() + "\n" + line
    return line


def proposal_files() -> list[Path]:
    files = []
    for inbox in forge_inboxes():
        files.extend(inbox.rglob("*.md"))
    return sorted(files)


def proposal_id(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_proposal(pid: str) -> Path:
    candidates = []
    raw = pid.strip()

    direct = ROOT / raw
    if direct.exists() and direct.is_file():
        return direct

    for inbox in forge_inboxes():
        direct = inbox / raw
        if direct.exists() and direct.is_file():
            return direct

        if not raw.endswith(".md"):
            direct_md = inbox / f"{raw}.md"
            if direct_md.exists() and direct_md.is_file():
                return direct_md

    for path in proposal_files():
        rel = proposal_id(path)
        stem = path.stem
        if raw in {rel, stem, path.name}:
            candidates.append(path)

    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise SystemExit(f"FAIL: proposal not found: {pid}")

    print("FAIL: ambiguous proposal id. Matches:")
    for p in candidates:
        print(f"- {proposal_id(p)}")
    raise SystemExit(2)


def cmd_list(args: argparse.Namespace) -> None:
    rows = []
    for path in proposal_files():
        try:
            data, _, _ = frontmatter(read_text(path))
        except Exception as exc:
            rows.append((proposal_id(path), "INVALID", str(exc)))
            continue

        rows.append((
            proposal_id(path),
            data.get("status", "<missing>"),
            data.get("trust_class", "<missing>"),
        ))

    if not rows:
        print("No proposals found.")
        return

    for rel, status, trust in rows:
        print(f"{rel}\tstatus={status}\ttrust_class={trust}")


def cmd_show(args: argparse.Namespace) -> None:
    path = find_proposal(args.proposal_id)
    print(read_text(path))


def cmd_approve(args: argparse.Namespace) -> None:
    path = find_proposal(args.proposal_id)
    text = read_text(path)
    data, raw, body = frontmatter(text)

    for key, expected in REQUIRED_DRAFT.items():
        actual = data.get(key)
        if actual != expected:
            raise SystemExit(
                f"FAIL: proposal is not approvable draft: {proposal_id(path)} "
                f"{key}={actual!r}, expected={expected!r}"
            )

    reviewed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    new_raw = raw
    for key, value in APPROVED_UPDATES.items():
        new_raw = replace_or_add(new_raw, key, value)
    new_raw = replace_or_add(new_raw, "reviewed_at", reviewed_at)

    new_text = f"---\n{new_raw.rstrip()}\n---\n{body}"
    write_text(path, new_text)

    print(f"PASS: approved proposal={proposal_id(path)}")
    print("status=approved")
    print("trust_class=reviewed")
    print(f"reviewed_at={reviewed_at}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Review and approve governed forge proposals.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show")
    p_show.add_argument("proposal_id")
    p_show.set_defaults(func=cmd_show)

    p_approve = sub.add_parser("approve")
    p_approve.add_argument("proposal_id")
    p_approve.set_defaults(func=cmd_approve)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
