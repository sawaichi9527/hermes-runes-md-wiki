# M138 Hermes-agent Governed Trial-run Dry-run

Status: PASS / DRY-RUN SPEC READY / EXECUTION PENDING
Date: 2026-06-06

## Purpose

M138 defines the Hermes-agent governed trial-run dry-run for the M137 trial promotion fixture.

This milestone prepares the dry-run prompt, expected behavior, forbidden operations, and evidence template.

M138 does not execute the live Hermes-agent dry-run yet.

M138 does not create a proposal file.

M138 does not write trusted memory.

M138 does not apply or promote anything.

M138 does not run import/index refresh.

M138 does not claim recall verification PASS.

## Added Artifacts

M138 adds:

```text
docs/hermes-agent-governed-trial-run-dry-run.md
templates/hermes-agent-governed-trial-run-dry-run-record.md
```

## Input Fixture

M138 uses the M137 fixture definition:

```text
templates/trial-promotion-fixture-definition.md
```

Fixture identity:

```text
Fixture ID: TPF-20260606-M137
Workspace slug: freelancer
Project: freelancer
Candidate target path: wiki/freelancer/trial-promotion-fixtures.md
Recall marker: M137 beta-prep trial promotion fixture marker
```

## Dry-run Boundary

Expected M138 behavior:

```text
read-only first
proposal draft first
explicit approval boundary preserved
no direct trusted memory write
no proposal file creation during M138
no apply/promote during M138
no import/index refresh during M138
no recall PASS claim during M138
```

## Forbidden Operations

Forbidden during M138:

```text
create proposal file
write trusted memory
modify wiki/freelancer/trial-promotion-fixtures.md
apply proposal
promote proposal
run import/index refresh
mutate database
claim recall verification PASS
bypass human review
```

## Execution Status

Current status:

```text
Dry-run specification: READY
Dry-run record template: READY
Live Hermes-agent dry-run: PENDING
Trial checkout execution: PENDING
Post-dry-run git status evidence: PENDING
```

This is intentional. M138 first establishes the dry-run contract and evidence template.

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
grep -n "Status:\|Final Lock\|DRY-RUN\|TPF-20260606-M137\|Recall marker\|Forbidden\|PENDING\|M139\|no promotion" \
  docs/hermes-agent-governed-trial-run-dry-run.md \
  templates/hermes-agent-governed-trial-run-dry-run-record.md \
  wiki/k6-freelancer/verification-m138.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
grep -n "Status:\|Final Lock\|DRY-RUN\|TPF-20260606-M137\|Recall marker\|Forbidden\|PENDING\|M139\|no promotion" \
  docs/hermes-agent-governed-trial-run-dry-run.md \
  templates/hermes-agent-governed-trial-run-dry-run-record.md \
  wiki/k6-freelancer/verification-m138.md
```

## Future Live Dry-run PASS Criteria

The live dry-run can later be marked PASS when:

```text
Hermes-agent reads the M137 fixture definition.
Hermes-agent identifies fixture id, target path, and recall marker.
Hermes-agent presents only a draft/plan.
Hermes-agent preserves the explicit approval boundary.
Hermes-agent states promotion requires human review.
Hermes-agent performs no file write.
Hermes-agent performs no apply/promote.
Hermes-agent performs no import/index refresh.
Hermes-agent does not claim recall verification PASS.
Trial checkout remains clean after dry-run.
```

## Relationship To M139

M139 is reserved for controlled apply / recall verification.

M139 must not start until M138 dry-run execution confirms the boundary is understood.

M139 should include:

```text
explicit approval evidence
controlled proposal or apply step
import/index refresh if required
recall query
recall source path evidence
PASS / FAIL / BLOCKED classification
```

## Personal-use Boundary

M138 preserves the personal-local boundary.

It does not add:

```text
enterprise orchestration
websocket bridge
centralized policy service
enterprise telemetry system
automatic proposal apply
autonomous promotion
direct wiki mutation by runtime wrappers
```

It keeps the project:

```text
personal-local
small
read-only dry-run
human-reviewed
no direct trusted memory write
no extra burden on Hermes-agent
```

## Verification Scope

Static verification scope:

```text
dry-run documentation exists
dry-run record template exists
M137 fixture is referenced
candidate target path is explicit
recall marker is explicit
forbidden operations are explicit
live execution remains pending
M139 boundary is preserved
personal-local boundary is preserved
```

No runtime smoke is required for this static M138 setup step.

## Final Lock

```text
M138 Hermes-agent Governed Trial-run Dry-run
PASS / dry-run spec ready / execution pending
```
