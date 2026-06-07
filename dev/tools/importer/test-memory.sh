#!/usr/bin/env bash
set -euo pipefail

QUERY="${1:-phase2}"

echo
echo "========================================"
echo "Memory Query"
echo "========================================"

~/.hermes/memory_adapter.sh "$QUERY"
