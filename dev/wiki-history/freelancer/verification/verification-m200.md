# M200 v0.5.0 Release Readiness Verification

Status: PASS / v0.5.0-rc1 cut / smoke verified / final tag pending  
Version line: 0.5.0-rc1  
Date: 2026-06-08

## Scope

M200 prepares the v0.5.0 release-readiness line after the M198 embedding/runtime smoke restoration and M199 runtime surface cleanup.

This milestone does not tag final `v0.5.0`. It locks the first release-candidate line as `0.5.0-rc1`.

## Locked results

### M200.1 Release Readiness Inventory

Status: PARTIAL / runtime ready / release docs needed

Findings:

- Runtime smoke path was healthy.
- Backend, migration, security, and hybrid recall checks passed.
- Release-facing documentation still referenced v0.3.0 as the latest tester baseline.
- `VERSION` still used `0.5.0-dev`.

Result:

- Do not tag final `v0.5.0` directly from `0.5.0-dev`.
- Proceed to v0.5.0 release documentation alignment.

### M200.2 Release Docs / RC Alignment

Status: PASS

Updated:

- `CHANGELOG.md`
- `docs/v0.5.0-release-readiness.md`

Latest related commit:

- `7a0bc8f Add v0.5.0 release readiness documentation`

Result:

- v0.5.0 release-readiness documentation exists.
- v0.3.0 documents remain historical baseline documents.
- Direct final tag from `0.5.0-dev` is explicitly discouraged.

### M200.3 Version RC Cut Prep

Status: PASS / committed / pushed

Updated:

- `VERSION`: `0.5.0-dev` -> `0.5.0-rc1`
- `CHANGELOG.md`: `[0.5.0-dev]` -> `[0.5.0-rc1]`
- `docs/v0.5.0-release-readiness.md`: `RC preparation` -> `RC candidate`

Latest related commit:

- `c0ad3f8 Cut v0.5.0 rc1 version line`

## Final RC smoke gate

PASS:

- `./bin/hermes-runes decipher freshness --json`
- `./bin/hermes-runes probe policy --json`
- `./bin/hermes-backend-check`
- `./bin/hermes-memory-migrate`
- `./bin/hermes-memory-security-scan`
- `./bin/hermes-recall "forge inbox boundary" --project freelancer --mode hybrid --limit 5 --json`
- `./bin/hermes-memory-smoke`

Accepted SKIP:

- `TB-M1989-FS001`: LLM endpoint unavailable for answer-generation smoke.
- `TB-M1989-FS002`: promotion governance fixture not present in fresh runtime workspace.
- `TB-M19810-RG001`: retrieval governance fixture not present in fresh runtime workspace.

## Release decision

`0.5.0-rc1` is release-candidate ready.

Final `v0.5.0` tag is still pending and must not be created until:

- repository remains clean
- final smoke gate passes again
- final tag decision is explicitly made
- `VERSION` is promoted from `0.5.0-rc1` to `0.5.0`

## Final lock

M200 is locked as:

PASS / v0.5.0-rc1 / smoke verified / final tag pending
