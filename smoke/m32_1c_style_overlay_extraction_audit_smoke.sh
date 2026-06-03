#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "== M32.1c Style Overlay Extraction Audit Smoke =="

style="wiki/_system/agent-style-overlay.md"
legacy="wiki/k6-freelancer/multi-layer-naming-narrative-model.md"

test -f "$style"
test -f "$legacy"

grep -q "Optional Runes-Style Presentation" "$style"
grep -q "style overlay only" "$style"
grep -q "must not change what Hermes-agent is allowed to do" "$style"

grep -q "Historical design source" "$legacy"
grep -q "Active Hermes-agent style guidance has been centralized" "$legacy"
grep -q "wiki/_system/agent-style-overlay.md" "$legacy"
grep -q "Do not treat this file as the current agent-facing style authority" "$legacy"

grep -q "agent-style-overlay.md" wiki/_system/README.md

echo "PASS: M32.1c style overlay extraction audit lock"
