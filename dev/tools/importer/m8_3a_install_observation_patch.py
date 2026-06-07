#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.home() / "workspace/hermes-memory"
TARGET = ROOT / "tools/importer/memory_answer_generator.py"
TOOLS = ROOT / "tools/importer"

text = TARGET.read_text(encoding="utf-8")

# Imports
if "import time" not in text:
    text = text.replace("import os\n", "import os\nimport time\n", 1)
if "from observation_logger import" not in text:
    marker = "from typing import Any\n"
    insert = "from observation_logger import build_record, new_trace_id, now_local, write_record\n"
    if marker in text:
        text = text.replace(marker, marker + insert, 1)
    else:
        text = insert + text

# Parser options. Insert after debug raw preview if present; otherwise before return parser.parse_args.
if "--no-observe" not in text:
    obs_args = (
        '    parser.add_argument("--no-observe", action="store_true", help="Disable default lightweight observation logging")\n'
        '    parser.add_argument("--observe-preview", action="store_true", help="Store short redacted previews in observation JSONL")\n'
        '    parser.add_argument("--observe-dir", default=None, help="Override observation base directory")\n'
        '    parser.add_argument("--observe-retention-days", type=int, default=int(os.environ.get("HERMES_OBSERVE_RETENTION_DAYS", "90")))\n'
        '    parser.add_argument("--observe-max-daily-mb", type=int, default=int(os.environ.get("HERMES_OBSERVE_MAX_DAILY_MB", "20")))\n'
    )
    if 'parser.add_argument("--debug-raw-preview"' in text:
        text = re.sub(
            r'(    parser\.add_argument\("--debug-raw-preview".*?\n)',
            r'\1' + obs_args,
            text,
            count=1,
        )
    else:
        text = text.replace("    return parser.parse_args(argv)\n", obs_args + "    return parser.parse_args(argv)\n", 1)

# Add trace variables after args parse.
if "trace_id = new_trace_id()" not in text:
    text = text.replace(
        "def main(argv: list[str]) -> int:\n    args = parse_args(argv)\n\n    try:\n",
        "def main(argv: list[str]) -> int:\n    args = parse_args(argv)\n    trace_id = new_trace_id()\n    started_at = now_local()\n    t0 = time.monotonic()\n    observation_warnings: list[str] = []\n    context_data = None\n    result = None\n    raw_text = \"\"\n\n    try:\n",
        1,
    )

# Phase should now be M8.3a in success/fail output.
text = text.replace('"phase": "M8.2c"', '"phase": "M8.3a"')
text = text.replace('"phase": "M8.2b"', '"phase": "M8.3a"')

# Add trace_id to success result dict.
if '"trace_id": trace_id' not in text:
    text = text.replace(
        '            "usage": llm_data.get("usage"),\n        }\n',
        '            "usage": llm_data.get("usage"),\n            "trace_id": trace_id,\n        }\n',
        1,
    )

# Add observation write before JSON/non-JSON output.
if "observation = build_record(" not in text:
    insert = '''        duration_ms = int((time.monotonic() - t0) * 1000)
        observation = build_record(
            args=args,
            trace_id=trace_id,
            started_at=started_at,
            duration_ms=duration_ms,
            context_data=context_data,
            result=result,
            raw_text=raw_text,
            error=None,
        )
        write_record(observation, args, observation_warnings)
        result["observation_warnings"] = observation_warnings

'''
    text = text.replace("        if args.json:\n", insert + "        if args.json:\n", 1)

# Patch fail branch if exact old block exists. If not, leave runtime success logging still usable.
if 'error["observation_warnings"] = observation_warnings' not in text:
    old = '''        error = {
            "status": "fail",
            "phase": "M8.3a",
            "query": getattr(args, "query", None),
            "error": str(exc),
        }
        print(json.dumps(error, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
'''
    new = '''        duration_ms = int((time.monotonic() - t0) * 1000)
        error_msg = str(exc)
        error = {
            "status": "fail",
            "phase": "M8.3a",
            "query": getattr(args, "query", None),
            "trace_id": trace_id,
            "error": error_msg,
        }
        observation = build_record(
            args=args,
            trace_id=trace_id,
            started_at=started_at,
            duration_ms=duration_ms,
            context_data=context_data,
            result=error,
            raw_text=raw_text,
            error=error_msg,
        )
        write_record(observation, args, observation_warnings)
        error["observation_warnings"] = observation_warnings
        print(json.dumps(error, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
'''
    if old in text:
        text = text.replace(old, new, 1)

TARGET.write_text(text, encoding="utf-8")
print("PASS: patched", TARGET)
