#!/usr/bin/env python3
import re


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def split_markdown_by_headings(text: str, max_chars: int = 2500, overlap_chars: int = 200):
    """
    Heading-aware Markdown chunker.

    Goal:
    - Prefer splitting at Markdown headings.
    - Keep each section as an independent chunk when possible.
    - Only split inside a section when the section is too large.
    """

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    sections = []
    current = []

    for line in lines:
        if HEADING_RE.match(line) and current:
            sections.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    chunks = []

    for section in sections:
        if not section:
            continue

        if len(section) <= max_chars:
            chunks.append(section)
            continue

        start = 0
        while start < len(section):
            end = min(start + max_chars, len(section))
            chunk = section[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(section):
                break

            start = max(0, end - overlap_chars)

    return chunks
