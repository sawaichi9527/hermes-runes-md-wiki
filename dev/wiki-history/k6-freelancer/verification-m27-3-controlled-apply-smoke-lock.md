# M27.3 Controlled Apply Smoke Lock

Status: PASS / SMOKE VERIFIED / REGRESSION BASELINE LOCKED
Milestone: M27.3 Controlled Apply Smoke Lock
Chinese: M27.3 受控套用煙霧測試鎖定

## Purpose

M27.3 locks the first successful controlled trusted wiki mutation baseline.

This milestone converts the temporary local smoke verification into a canonical regression and governance baseline.

M27.3 verifies that M27.2 controlled apply:

- can mutate a single trusted Markdown wiki file
- requires explicit human confirmation
- requires expected pre-apply hash validation
- writes rollback evidence
- writes operation evidence
- preserves non-autonomous governance boundaries
- blocks invalid apply attempts

## Verified Smoke Scenario

Temporary isolated repo root:

```text
/tmp/runes-m27-2-smoke-*
```

Target path:

```text
wiki/k6-freelancer/services.md
```

Proposal ID:

```text
m27-2-smoke-proposal
```

Apply mode:

```text
controlled_apply
```

## PASS Verification

The following behavior was verified:

- controlled apply status: PASS
- target file write: PASS
- rollback snapshot write: PASS
- operation record write: PASS
- pre-apply hash validation: PASS
- confirmation token validation: PASS
- candidate post-hash verification: PASS
- single-target containment: PASS
- trusted wiki mutation boundary: PASS

## Verified Write Evidence

Verified evidence types:

```text
backups/runes-apply/<date>/*.snapshot.md
operations/runes-apply/<date>/*.json
```

Verified metadata:

- pre_apply_sha256
- post_apply_sha256
- expected_pre_hash
- confirmation_token_used
- candidate_meta
- post_apply_verification_required

## Verified Non-Mutation Boundary

The smoke verification confirmed:

- database_mutated: false
- importer_mutated: false
- proposal_state_mutated: false

This preserves the M26.5 and M27 governance contract.

## BLOCKED Verification

The following invalid apply scenario was verified:

```text
expected pre-apply hash does not match current target file hash
```

Verified behavior:

- status: BLOCKED
- target file write prevented
- rollback snapshot prevented
- operation record prevented
- trusted wiki mutation prevented

## Locked Regression Expectations

Future regressions must preserve:

- explicit `--apply` boundary
- expected pre-hash validation
- confirmation-token validation
- single-target-only apply
- rollback snapshot generation
- operation record generation
- no implicit importer execution
- no database mutation
- no autonomous apply

## Relationship to Future Work

M27.3 establishes the first real trusted Markdown mutation baseline.

Future work:

- M27.4 Roadmap / Verification Freeze
- M28 Importer / Retrieval Refresh Boundary

M28 must preserve:

```text
trusted wiki apply != implicit importer mutation
```

## Verification Status

M27.3 Controlled Apply Smoke Lock:

- controlled write path verified: PASS
- rollback evidence verified: PASS
- operation evidence verified: PASS
- wrong-hash blocking verified: PASS
- trusted wiki mutation verified: PASS
- no database mutation verified: PASS
- no importer mutation verified: PASS
- no proposal-state mutation verified: PASS
- governance boundary preserved: PASS

Overall:

M27.3 Controlled Apply Smoke Lock:
PASS / smoke verified / regression baseline locked
