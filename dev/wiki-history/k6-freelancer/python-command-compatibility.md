# Python Command Compatibility Verification Lock

## Metadata

- Category: verification
- Topic: python-command-compatibility
- Note type: verification-lock
- Status: frozen
- Memory quality: verified
- Related objective: k6-freelancer
- Parent index: wiki/k6-freelancer/verification.md
- Source type: user-verified
- Last reviewed: 2026-06-04

## Summary

This document locks the project-level Python command compatibility policy for Ubuntu 24.04.x and similar Linux environments.

Ubuntu 24.04.x provides `python3` by default, but the `python` command is not guaranteed to exist unless the local system installs a compatibility package such as `python-is-python3`.

Hermes Runes MD Wiki must not require that package for active project entrypoints.

## Compatibility Policy

Active shell wrappers should use:

```bash
PYTHON="${PYTHON:-python3}"
"$PYTHON" ...
```

Python scripts should keep:

```python
#!/usr/bin/env python3
```

Project documentation and active user-facing commands should prefer:

```bash
python3 script.py
```

instead of:

```bash
python script.py
```

## Rationale

This keeps the project compatible with Ubuntu 24.04.x defaults without changing system-wide Python behavior.

The project does not require users to run:

```bash
sudo apt install python-is-python3
```

That package remains acceptable as a local convenience, but it is not a project dependency.

## Active Wrapper Cleanup Scope

The active wrapper cleanup covered the project entrypoints under:

- `bin/`
- `tools/importer/hermes-memory-*`

The cleaned wrappers now use the project-level fallback pattern:

```bash
PYTHON="${PYTHON:-python3}"
```

This allows both default execution with `python3` and explicit override, for example:

```bash
PYTHON=tools/importer/.venv/bin/python bin/hermes-memory-smoke
```

## Verified Active Wrappers

The cleanup covered active wrappers including:

- `bin/hermes-memory-eval`
- `bin/hermes-forge`
- `bin/hermes-memory-smoke`
- `bin/hermes-answer`
- `bin/hermes-context`
- `bin/hermes-recall`
- `bin/hermes-observe`
- `bin/hermes-memory-tool`
- `bin/hermes-memory-import`
- `bin/hermes-memory-stale-purge`
- `bin/hermes-memory-sync`
- `bin/hermes-memory-stale-report`
- `bin/hermes-memory-security-scan`
- `bin/hermes-memory-metadata-inspect`
- `bin/hermes-retrieval-governance-smoke`
- `bin/hermes-memory-adapter`
- `bin/hermes-memory-check`
- `tools/importer/hermes-memory-hybrid-search`
- `tools/importer/hermes-memory-fts-search`
- `tools/importer/hermes-memory-vector-search`
- `tools/importer/hermes-memory-embed`

## Explicit Non-scope

The cleanup intentionally does not rewrite generated, archived, or third-party content, including:

- `.venv/`
- `archive/`
- `backups/`
- package metadata under installed site-packages
- historical command transcripts
- prototype snapshots

These are not active project entrypoints.

## Verification Command

The active wrapper compatibility check can be inspected with:

```bash
grep -RIn --exclude-dir=.git --exclude-dir=.venv --exclude-dir=archive --exclude-dir=backups \
  -e "python " \
  -e "/usr/bin/env python" \
  -e "/usr/bin/python" \
  bin tools docs wiki | head -80
```

Expected remaining matches are mostly valid shebangs:

```text
#!/usr/bin/env python3
```

Minor Python-internal usage strings or historical examples may remain, but active shell wrappers must not directly depend on the `python` command.

## User-verified Result

The user verified after pull:

```text
M66.6 freeze smoke: PASS
bin/hermes-recall --help: PASS
```

The remaining grep output no longer shows active shell-wrapper direct `python` invocation in the cleaned wrapper set.

## Final Lock

Python command compatibility is locked as:

```text
Python active wrapper compatibility cleanup
PASS / smoke verified
```

The project standard is:

```text
Use python3 by default.
Allow PYTHON override.
Do not require system-level python aliasing.
```
