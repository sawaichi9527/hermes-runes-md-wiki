# M137 Trial Promotion Fixture Definition

Status: PASS / FIXTURE DEFINED / NOT PROMOTED
Date: 2026-06-06

## Purpose

M137 defines the minimal beta-prep trial promotion fixture.

This milestone follows M136, which confirmed the model endpoint check can safely return SKIP / expected when no model endpoint is configured.

M137 addresses the next controllable beta-prep gap:

```text
trial promotion fixture
```

## Added Artifacts

M137 adds:

```text
templates/trial-promotion-fixture-definition.md
docs/trial-promotion-fixture-definition.md
```

## Fixture Identity

```text
Fixture ID: TPF-20260606-M137
Workspace slug: freelancer
Project: freelancer
Candidate target path: wiki/freelancer/trial-promotion-fixtures.md
Fixture type: beta-prep governed recall marker
Recall marker: M137 beta-prep trial promotion fixture marker
```

## Definition-only Boundary

M137 is definition-only.

It does not:

```text
create trusted memory
create an approved proposal
apply proposal
promote proposal
run import/index refresh for the fixture
claim recall verification PASS
bypass human review
```

## Fixture Constraints

The fixture must remain:

```text
small
non-sensitive
workspace-scoped
human-reviewed before promotion
stable enough for recall verification
safe to keep in git after review
```

The fixture must not include:

```text
credentials
tokens
keys
private customer data
external service configuration
raw logs
```

## Future Recall Expectations

Expected future recall query:

```text
M137 beta-prep trial promotion fixture marker
```

Expected future source path after approved promotion:

```text
wiki/freelancer/trial-promotion-fixtures.md
```

## Relationship To M138 And M139

M138 should use this fixture definition for dry-run validation only.

M139 may use this fixture for controlled apply / recall verification only after the human-reviewed boundary is clear.

Expected future M139 evidence:

```text
approved fixture content
proposal path or identifier
apply/promote command or manual step
import/index refresh evidence if needed
recall query
recall result
source path evidence
working tree status
PASS / FAIL / BLOCKED classification
```

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
grep -n "Status:\|Final Lock\|TPF-20260606-M137\|Recall marker\|not promoted\|NOT DONE\|M138\|M139" \
  templates/trial-promotion-fixture-definition.md \
  docs/trial-promotion-fixture-definition.md \
  wiki/k6-freelancer/verification-m137.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short
grep -n "Status:\|Final Lock\|TPF-20260606-M137\|Recall marker\|not promoted\|NOT DONE\|M138\|M139" \
  templates/trial-promotion-fixture-definition.md \
  docs/trial-promotion-fixture-definition.md \
  wiki/k6-freelancer/verification-m137.md
```

## Personal-use Boundary

M137 preserves the personal-local boundary.

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
Markdown-native
human-reviewed
no direct trusted memory write
no extra burden on Hermes-agent
```

## Verification Scope

Static verification scope:

```text
fixture template exists
fixture documentation exists
fixture id is stable
candidate target path is explicit
recall marker is explicit
M137 does not promote content
M138/M139 follow-up boundary is clear
personal-local boundary is preserved
```

No runtime smoke is required because this milestone defines the fixture only.

## Final Lock

```text
M137 Trial Promotion Fixture Definition
PASS / fixture defined / not promoted
```
