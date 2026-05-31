import re


KEEP_AFTER_PATTERNS = [
    r'(?im)^\s*(?:\d+\.\s*)?\*?\*?Refine Output\s*:\*?\*?\s*$',
    r'(?im)^\s*(?:\d+\.\s*)?\*?\*?Final Answer\s*:\*?\*?\s*$',
    r'(?im)^\s*(?:\d+\.\s*)?\*?\*?Draft Answer.*?:\*?\*?\s*$',
]

DROP_FROM_PATTERNS = [
    r'(?im)^\s*Check against constraints\s*:',
    r'(?im)^\s*(?:\d+\.\s*)?Check against Rules\s*:',
    r'(?im)^\s*(?:\d+\.\s*)?Final Review\s*:',
    r'(?im)^\s*All points directly map.*$',
]


def cleanup_extracted_answer(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Prefer the explicitly refined/final block if present.
    for pattern in KEEP_AFTER_PATTERNS:
        matches = list(re.finditer(pattern, text))
        if matches:
            m = matches[-1]
            text = text[m.end():].strip()
            break

    # Drop internal review/checking sections.
    cut = None
    for pattern in DROP_FROM_PATTERNS:
        m = re.search(pattern, text)
        if m and (cut is None or m.start() < cut):
            cut = m.start()

    if cut is not None:
        text = text[:cut].strip()

    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text
