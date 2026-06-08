# M199 Runtime CLI / Tools Surface Cleanup Verification

Status: PASS / committed / pushed / runtime surface verified  
Version line: 0.5.0-dev  
Date: 2026-06-08

## Scope

M199 cleaned the runtime-facing repository surface by separating:

- runtime CLI wrappers under `bin/`
- runtime/support tooling under root `tools/`
- development-only smoke, fixture, regression, historical, and trial assets under `dev/`

## Locked results

### M199.2 Safe First Relocation

Status: PASS

Moved development-only importer/runes smoke and historical milestone assets under `dev/`.

Latest related commit:

- `49418dc Move development-only smoke assets under dev`

### M199.3 Runes Shield Deep Cleanup

Status: PASS

Moved Runes Shield smoke, fixture, validation, regression, trial-run, and legacy `runes` CLI assets under `dev/`.

Latest related commit:

- `e1cb587 Move Runes Shield development assets under dev`

Bug IDs resolved:

- `TB-M1993-RUNES001`: legacy `bin/runes` depended on moved M21-M26 milestone modules.
- `TB-M1993-RUNES002`: `bin/hermes-runes` executable bit restored.
- `TB-M1993-RUNES003`: Runes Shield fixtures moved individually after directory collision.

### M199.4 Runtime Surface Final Audit

Status: PASS

Runtime support tools were renamed to remove milestone suffixes:

- `metadata_inspect_m6_4.py` -> `metadata_inspect.py`
- `security_scan_m6_3.py` -> `security_scan.py`
- `stale_purge_m6_2.py` -> `stale_purge.py`
- `stale_report_m6_2.py` -> `stale_report.py`

Latest related commits:

- `1b64b93 Rename runtime support tools without milestone suffixes`
- `f19abcf Move growth-aware forge trial under dev`

Bug IDs resolved:

- `TB-M1994-SEC001`: `security_scan.py` no longer defaults to old `~/workspace/hermes-memory`; it now resolves the current repository root.

## Final runtime surface snapshot

Runtime bin count:

- 30 files under `bin/`

Root tools/runes retained files:

- `tools/runes/markdown_source_health.py`
- `tools/runes/markdown_source_health_audit.py`
- `tools/runes/ragnarok_incantation_boundary.py`
- `tools/runes/ragnarok_observation_bundle.py`

Root Runes Shield retained class:

- runtime / agent-facing core modules only
- no root `tools/runes_shield/smoke_*.py`
- no root `tools/runes_shield/fixtures/`
- no root `tools/runes_shield/validate_*.py`

Development archive count:

- 809 files under `dev/`

## Final verification

PASS:

- `./bin/hermes-runes decipher freshness --json`
- `./bin/hermes-runes probe policy --json`
- `./bin/hermes-memory-security-scan`
- `./bin/hermes-memory-smoke`

Accepted SKIP:

- `TB-M1989-FS001`: LLM endpoint unavailable for answer-generation smoke.
- `TB-M1989-FS002`: promotion governance fixture not present in fresh runtime workspace.
- `TB-M19810-RG001`: retrieval governance fixture not present in fresh runtime workspace.

## Final lock

M199 is locked as:

PASS / runtime surface reduced / dev archive separated / smoke verified
