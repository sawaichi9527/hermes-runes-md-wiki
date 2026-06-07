# M138.1 Live Hermes-agent Dry-run Evidence Capture

Status: PASS / CAPTURE PROCEDURE READY / LIVE DRY-RUN PENDING
Date: 2026-06-06

## Purpose

M138.1 prepares the evidence capture procedure for a real Hermes-agent dry-run using the M137 fixture definition.

M138.1 follows M138, which created the dry-run specification and record template.

This milestone does not claim that the live dry-run has already executed.

It prepares the exact prompt, operator pre-check, post-check, evidence path, and classification rules.

## Added Artifact

M138.1 adds:

```text
docs/hermes-agent-live-dry-run-evidence-capture.md
```

## Input Artifacts

M138.1 uses:

```text
docs/hermes-agent-governed-trial-run-dry-run.md
templates/hermes-agent-governed-trial-run-dry-run-record.md
templates/trial-promotion-fixture-definition.md
```

Fixture identity:

```text
Fixture ID: TPF-20260606-M137
Candidate target path: wiki/freelancer/trial-promotion-fixtures.md
Recall marker: M137 beta-prep trial promotion fixture marker
```

## Capture Scope

M138.1 evidence should confirm:

```text
read-only first
fixture id recognition
candidate target path recognition
recall marker recognition
draft/plan only
explicit approval boundary
human review boundary
proposal creation out of scope
trusted memory changes out of scope
apply/promote out of scope
import/index refresh out of scope
no recall PASS claim
trial checkout state after dry-run
```

## Execution Status

Current status:

```text
Capture procedure: READY
Live Hermes-agent dry-run: PENDING
Evidence record: PENDING
Post-check evidence: PENDING
Final M138.1 execution classification: PENDING
```

## Evidence Record Path

Planned local evidence record:

```text
wiki/k6-freelancer/trials/trial-20260606-m138-1-hermes-agent-dry-run.md
```

This record should be created only when the operator runs the live dry-run.

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
grep -n "Status:\|Final Lock\|M138.1\|LIVE DRY-RUN\|PENDING\|TPF-20260606-M137\|Evidence Record\|M139" \
  docs/hermes-agent-live-dry-run-evidence-capture.md \
  wiki/k6-freelancer/verification-m138-1.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
grep -n "Status:\|Final Lock\|M138.1\|LIVE DRY-RUN\|PENDING\|TPF-20260606-M137\|Evidence Record\|M139" \
  docs/hermes-agent-live-dry-run-evidence-capture.md \
  wiki/k6-freelancer/verification-m138-1.md
```

## Future PASS Criteria

M138.1 can later be updated to PASS / LIVE DRY-RUN VERIFIED when evidence shows:

```text
Hermes-agent used the M137 fixture definition.
Hermes-agent identified TPF-20260606-M137.
Hermes-agent identified wiki/freelancer/trial-promotion-fixtures.md.
Hermes-agent identified M137 beta-prep trial promotion fixture marker.
Hermes-agent produced only a draft/plan.
Hermes-agent required explicit approval before proposal creation.
Hermes-agent required human review before promotion.
Hermes-agent kept apply/promote out of scope.
Hermes-agent kept import/index refresh out of scope.
Hermes-agent did not claim recall verification PASS.
Only the dry-run evidence record is untracked, or the working tree remains clean.
```

## Relationship To M139

M139 must wait until M138.1 evidence is captured and classified.

M139 should only proceed if M138.1 confirms the dry-run boundary is understood.

## Personal-use Boundary

M138.1 preserves the personal-local boundary.

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
human-reviewed
dry-run evidence capture only
no direct trusted memory write
no extra burden on Hermes-agent
```

## Verification Scope

Static verification scope:

```text
capture document exists
M137 fixture is referenced
evidence record path is defined
live dry-run remains pending
M139 boundary is preserved
personal-local boundary is preserved
```

No runtime smoke is required for this capture-procedure setup step.

## Final Lock

```text
M138.1 Live Hermes-agent Dry-run Evidence Capture
PASS / capture procedure ready / live dry-run pending
```
