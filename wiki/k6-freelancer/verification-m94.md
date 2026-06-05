# M94 Trial Promotion Fixture Minimal Path

Status: PASS / TRIAL FIXTURE VERIFIED
Date: 2026-06-06

## Purpose

M94 addresses the second controlled beta-prep gap recorded by M92:

```text
trial promotion fixture
```

The goal is to let M20.4 promotion governance smoke move from expected clean SKIP to PASS in the `freelancer` trial workspace once a minimal human-reviewed fixture is imported.

## Scope

M94 remains:

```text
personal-local
bounded
explicit
non-enterprise
non-daemon
human-reviewed
```

## Implemented Changes

### Trial fixture

Added:

```text
wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
```

The fixture includes forge front matter:

```text
status: approved
proposal_type: agent_memory
proposed_by: human
provenance: manual_cli
trust_class: reviewed
```

Marker query:

```text
M94 trial promotion fixture real agent-proposed memory draft
```

### M20.4 trial smoke path

Updated:

```text
tools/importer/promotion_governance_smoke.py
```

New behavior for non-legacy workspaces:

```text
If no trial fixture is imported, keep clean SKIP.
If an approved reviewed fixture is retrieved, report PASS.
If a fixture-like result is found but metadata is wrong, report FAIL.
```

Legacy `k6-freelancer` behavior remains unchanged.

## Local Verification Result

Trial checkout verification:

```text
repo: /home/eye/workspace-trial/hermes-runes-md-wiki
head: 7f330c5 Add M94 trial promotion fixture verification lock
working tree: clean
```

Fixture file present:

```text
wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
```

Importer result:

```text
inserted: id=59 chunks=2 project=freelancer path=wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
summary: schema=public import_scope=freelancer imported_or_changed=1 updated=0 skipped=58 chunks_written=2
PASS: Markdown incremental import completed
```

M20.4 promotion governance smoke result:

```text
suite: M20.4 Promotion Governance Smoke
profile: workspace-freelancer
status: PASS
failed: 0
total: 1
id: M20.4-TRIAL-A
summary: approved reviewed trial promotion fixture is retrieval-visible
path: wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
trust_bias: 0
```

Forge metadata verified:

```text
status: approved
trust_class: reviewed
proposal_type: agent_memory
proposed_by: human
provenance: manual_cli
operation_id: M94-trial-promotion-fixture-20260606
```

## Boundaries

M94 does not introduce:

```text
no orchestration daemon
no model router
no secret manager
no enterprise telemetry
no automatic proposal apply
no direct wiki mutation by agent
no runtime authority escalation
```

## Final Lock

```text
M94 Trial Promotion Fixture Minimal Path
PASS / trial fixture verified
```
