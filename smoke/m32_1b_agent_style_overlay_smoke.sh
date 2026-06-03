#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

file="wiki/_system/agent-style-overlay.md"

echo "== M32.1b Agent Style Overlay Smoke =="

test -f "$file"

grep -q "Not a replacement for Hermes-agent \`soul.md\`" "$file"
grep -q "style overlay only" "$file"
grep -q "must not change what Hermes-agent is allowed to do" "$file"
grep -q "Forge / 鑄造" "$file"
grep -q "Attunement / 調律" "$file"
grep -q "Relic / 遺物" "$file"
grep -q "Optional Runes-Style Presentation" "$file"
grep -q "They must not imply" "$file"

grep -q "agent-style-overlay.md" wiki/_system/README.md

echo "PASS: M32.1b agent style overlay boundary"
