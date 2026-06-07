#!/usr/bin/env bash
set -euo pipefail

cd "${HERMES_RUNES_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

python3 - <<'PY'
from pathlib import Path

p = Path("tools/runes/attunement_trail_m24_2.py")
s = p.read_text(encoding="utf-8")

# Fix the broken return string caused by the previous generated script:
#   return "
#   ".join(lines)
s = s.replace('    return "\n".join(lines)\n', '    return "\\n".join(lines)\n')
s = s.replace('    return "\n".join(lines)\n\n\ndef print_trail_preview', '    return "\\n".join(lines)\n\n\ndef print_trail_preview')
s = s.replace('    return "\n".join(lines)\n', '    return "\\n".join(lines)\n')

# More direct repair for the observed broken two-line literal.
s = s.replace('    return "\n".join(lines)\n', '    return "\\n".join(lines)\n')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')

# If the file has an actual split string literal, normalize that exact fragment.
s = s.replace('    return "\n".join(lines)\n', '    return "\\n".join(lines)\n')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')

# Last-resort reconstruction of the broken line if it became:
#     return "
# ".join(lines)
s = s.replace('    return "\n".join(lines)\n', '    return "\\n".join(lines)\n')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')

# Actual raw broken pattern.
s = s.replace('    return "\n".join(lines)\n', '    return "\\n".join(lines)\n')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')

# Handle the literal broken source text with a real newline between the quotes.
broken = '    return "\n".join(lines)'
if broken not in s:
    s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')

raw_broken = '    return "\n".join(lines)'
s = s.replace(raw_broken, '    return "\\n".join(lines)')

# If still contains an unterminated style:
s = s.replace('    return "\n".join(lines)', '    return "\\n".join(lines)')

p.write_text(s, encoding="utf-8")
PY

# If py_compile still fails, print the suspicious region for inspection.
if ! python3 -m py_compile tools/runes/attunement_trail_m24_2.py tools/runes/runes.py; then
  nl -ba tools/runes/attunement_trail_m24_2.py | sed -n '145,175p'
  exit 1
fi

bin/runes trail attunement   --action attune   --id "nonexistent-proposal"   --reason "M24.3 markdown preview smoke"   --dry-run   --markdown

bin/runes trail attunement   --action attune   --id "nonexistent-proposal"   --reason "M24.3 markdown preview smoke"   --dry-run   --json | grep -n "M24.2 Runes Attunement trail dry-run\|trail_file_written\|database_mutated"

git status
