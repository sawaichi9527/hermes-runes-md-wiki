#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

echo "== M31.5 Archive Boundary Enforcement Smoke =="

echo "[1/6] archive directories exist"
test -d dev/archive/root-milestone-shell || { echo "FAIL missing dev/archive/root-milestone-shell"; fail=1; }
test -d tools/archive/milestone-shell || { echo "FAIL missing tools/archive/milestone-shell"; fail=1; }

echo "[2/6] root milestone shell scripts remain archived"
root_shell_count="$(find . -maxdepth 1 -type f \( -name 'm24_*.sh' -o -name 'm25_*.sh' -o -name 'm26_*.sh' \) | wc -l)"
test "$root_shell_count" = "0" || { echo "FAIL root_shell_count=$root_shell_count expected=0"; fail=1; }

echo "[3/6] active runes tree has no archived milestone-era tools"
active_runes_count="$(find tools/runes -maxdepth 1 -type f | grep -E 'm21|m22|m23|m24|m25|m26|import_refresh_m28_2|offer_policy' | wc -l || true)"
test "$active_runes_count" = "0" || { echo "FAIL active_runes_count=$active_runes_count expected=0"; fail=1; }

echo "[4/6] active code does not import from tools.archive"
archive_import_hits="$(
  grep -RInE '(^|[^A-Za-z0-9_])(from|import)[[:space:]]+tools\.archive' \
    bin smoke tools/importer tools/forge tools/runes \
    --exclude='m31_4_archive_lock_smoke.sh' \
    --exclude='m31_5_archive_boundary_smoke.sh' \
    --exclude='*.pyc' \
    --exclude-dir='.venv' \
    --exclude-dir='__pycache__' \
    --exclude-dir='*.dist-info' \
    --exclude-dir='site-packages' \
    2>/dev/null || true
)"
if [ -n "$archive_import_hits" ]; then
  echo "FAIL active archive reference detected:"
  echo "$archive_import_hits"
  fail=1
fi

echo "[5/6] archive scripts are not symlinked into active paths"
active_symlink_hits="$(
  find bin smoke tools/importer tools/forge tools/runes -type l -print 2>/dev/null \
    | while read -r link; do
        target="$(readlink "$link" || true)"
        case "$target" in
          *dev/archive/root-milestone-shell*|*tools/archive/milestone-shell*)
            echo "$link -> $target"
            ;;
        esac
      done
)"
if [ -n "$active_symlink_hits" ]; then
  echo "FAIL active symlink to archive detected:"
  echo "$active_symlink_hits"
  fail=1
fi

echo "[6/6] archive policy README files exist"
test -f dev/archive/root-milestone-shell/README.md || { echo "FAIL missing dev/archive/root-milestone-shell/README.md"; fail=1; }
test -f tools/archive/milestone-shell/README.md || { echo "FAIL missing tools/archive/milestone-shell/README.md"; fail=1; }

if [ "$fail" = "0" ]; then
  echo "PASS: M31.5 archive boundary enforcement smoke"
else
  echo "FAIL: M31.5 archive boundary enforcement smoke"
  exit 1
fi
