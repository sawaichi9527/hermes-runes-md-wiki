#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M31.7 Final Verification Lock =="

echo "[1/7] git working tree clean"
git diff --quiet || { echo "FAIL git diff dirty"; fail=1; }
git diff --cached --quiet || { echo "FAIL staged changes exist"; fail=1; }

untracked="$(
  git ls-files --others --exclude-standard
)"

if [ -n "$untracked" ]; then
  echo "FAIL untracked files exist:"
  echo "$untracked"
  fail=1
fi

echo "[2/7] M31.4 archive lock smoke"
./smoke/m31_4_archive_lock_smoke.sh || fail=1

echo "[3/7] M31.5 archive boundary smoke"
./smoke/m31_5_archive_boundary_smoke.sh || fail=1

echo "[4/7] hermes-memory-smoke"
./bin/hermes-memory-smoke || fail=1

echo "[5/7] archive README verification"
test -f archive/root-milestone-shell/README.md || fail=1
test -f tools/archive/milestone-shell/README.md || fail=1

echo "[6/7] operations policy verification"
grep -q '^operations/$' .gitignore || {
  echo "FAIL operations/ not ignored"
  fail=1
}

test -f docs/operations-local-retention.md || {
  echo "FAIL missing operations retention policy"
  fail=1
}

echo "[7/7] final archive milestone verification"

archive_shell_count="$(find archive/root-milestone-shell -type f -name '*.sh' | wc -l)"
archive_py_count="$(find tools/archive/milestone-shell -type f -name '*.py' | wc -l)"

echo "archive_shell_count=$archive_shell_count"
echo "archive_py_count=$archive_py_count"

test "$archive_shell_count" = "13" || {
  echo "FAIL archive_shell_count mismatch"
  fail=1
}

test "$archive_py_count" -ge "23" || {
  echo "FAIL archive_py_count too small"
  fail=1
}

if [ "$fail" = "0" ]; then
  echo "PASS: M31.7 final verification lock"
else
  echo "FAIL: M31.7 final verification lock"
  exit 1
fi
