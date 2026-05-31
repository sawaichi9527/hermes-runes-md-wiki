import re


CUT_PATTERN = re.compile(
    r"""(?im)
^\s*
(?:\d+\.\s*)?
(
    Check\s+against\s+Rules
    |Final\s+Review
    |Self-Correction
    |Draft
    |Final\s+Answer
    |Revised\s+Answer
    |Draft\s+Answer
    |Draft\s+Response
)
\s*:
""",
    re.VERBOSE,
)


def normalize_citations(text: str) -> str:
    return re.sub(
        r"\[Source\s*(\d+)\]",
        r"[Source \1]",
        text,
    )


def sanitize_answer(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Cut meta / regeneration sections.
    m = CUT_PATTERN.search(text)

    if m and m.start() >= 20:
        text = text[:m.start()]


    # Deterministic line-based cutoff.
    cutoff_markers = [
        "Check against Rules:",
        "Final Review:",
        "Self-Correction:",
        "Final Answer:",
        "Revised Answer:",
        "Draft Answer:",
        "Draft Response:",
        "4. Check against Rules:",
    ]

    kept_lines = []

    for line in text.splitlines():
        stripped = line.strip()

        should_cut = False

        for marker in cutoff_markers:
            if stripped.startswith(marker) or marker in stripped:
                should_cut = True
                break

        if should_cut:
            break

        kept_lines.append(line)

    text = "\n".join(kept_lines)


    # Remove internal reasoning headings.
    internal_patterns = [
        r"(?im)^\s*\(Internal.*$",
    ]


    artifact_patterns = [
        r"(?im)^\s*Draft\s*:\s*$",
        r"(?im)^\s*in Traditional Chinese\s*:\s*$",
        r"(?im)^\s*Final Answer\s*:\s*$",
    ]


    lines = []

    for line in text.splitlines():
        skip = False

        for ap in artifact_patterns:
            if re.match(ap, line):
                skip = True
                break


        for pattern in internal_patterns:
            if re.match(pattern, line):
                skip = True
                break

        if not skip:
            lines.append(line)

    text = "\n".join(lines)

    # Normalize citations.
    text = normalize_citations(text)

    # Collapse excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
