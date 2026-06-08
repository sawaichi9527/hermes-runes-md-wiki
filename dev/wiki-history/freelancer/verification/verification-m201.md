# M201 Final v0.5.0 Promotion Verification

Status: PASS / v0.5.0 tagged / pushed / working tree clean  
Version line: 0.5.0  
Date: 2026-06-08

## Scope

M201 promoted the v0.5.0 release line from `0.5.0-rc1` to final `0.5.0`, verified the final smoke gate, and created the annotated `v0.5.0` tag.

## Locked results

### M201.1 Pre-promotion smoke gate

Status: PASS

Verified while still on `0.5.0-rc1`:

- `./bin/hermes-runes decipher freshness --json`
- `./bin/hermes-runes probe policy --json`
- `./bin/hermes-backend-check`
- `./bin/hermes-memory-migrate`
- `./bin/hermes-memory-security-scan`
- `./bin/hermes-recall "forge inbox boundary" --project freelancer --mode hybrid --limit 5 --json`
- `./bin/hermes-memory-smoke`
- `./bin/hermes-retrieval-governance-smoke`

### M201.2 Final version-line promotion

Status: PASS / committed / pushed

Updated:

- `VERSION`: `0.5.0-rc1` -> `0.5.0`
- `CHANGELOG.md`: `[0.5.0-rc1]` -> `[0.5.0]`
- `docs/v0.5.0-release-readiness.md`: `final-ready`, version line `0.5.0`

Latest related commit:

- `3fa580b Promote v0.5.0 final version line`

### M201.3 Annotated tag

Status: PASS / tag pushed

Created annotated tag:

- `v0.5.0`

Tag target:

- `3fa580b Promote v0.5.0 final version line`

Tag message:

- `Hermes Runes MD Wiki v0.5.0`

Remote result:

- `v0.5.0 -> v0.5.0`

## Final smoke result

PASS:

- Runes freshness check
- Runes policy probe
- PostgreSQL backend check
- schema migration check
- security scan
- hybrid recall
- memory smoke

Accepted SKIP:

- `TB-M1989-FS001`: LLM endpoint unavailable for answer-generation smoke.
- `TB-M1989-FS002`: promotion governance fixture not present in fresh runtime workspace.
- `TB-M19810-RG001`: retrieval governance fixture not present in fresh runtime workspace.

## Final lock

M201 is locked as:

PASS / v0.5.0 tagged / pushed / release line clean
