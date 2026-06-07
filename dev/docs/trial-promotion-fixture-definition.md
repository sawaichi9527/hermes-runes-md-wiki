# Trial Promotion Fixture Definition

Status: ACTIVE / TRIAL PROMOTION FIXTURE DEFINED
Date: 2026-06-06

## Purpose

This document defines M137 Trial Promotion Fixture Definition.

M137 prepares a small fixture for later governed promotion testing.

It does not create trusted memory.

It does not apply or promote anything.

It does not run import or index refresh.

It does not require a model endpoint.

## Fixture Artifact

M137 adds:

```text
templates/trial-promotion-fixture-definition.md
```

This template defines the future trial fixture content and the review checklist.

## Fixture Identity

```text
Fixture ID: TPF-20260606-M137
Workspace slug: freelancer
Project: freelancer
Candidate target path: wiki/freelancer/trial-promotion-fixtures.md
Fixture type: beta-prep governed recall marker
```

## Fixture Constraints

The fixture must be:

```text
small
non-sensitive
workspace-scoped
human-reviewed before promotion
stable enough for recall verification
safe to keep in git after review
```

The fixture must not contain:

```text
credentials
tokens
keys
private customer data
external service configuration
raw logs
```

## Governance Boundary

M137 is a definition-only milestone.

Allowed in M137:

```text
define fixture content shape
define candidate target path
define recall marker
define review checklist
define future evidence requirements
```

Not allowed in M137:

```text
create trusted memory
apply proposal
promote proposal
run import/index refresh for the fixture
claim recall verification PASS
bypass human review
```

## Recall Marker

The future fixture recall marker is:

```text
M137 beta-prep trial promotion fixture marker
```

Expected future recall query:

```text
M137 beta-prep trial promotion fixture marker
```

Expected future source path after approved promotion:

```text
wiki/freelancer/trial-promotion-fixtures.md
```

## Relationship To M138 And M139

M138 should use this fixture definition for a governed trial-run dry-run.

M139 may use this fixture only after the dry-run and human review boundary are clear.

M139 should verify:

```text
controlled proposal/apply path
import/index refresh only when required
recall query result
source path evidence
PASS freeze only after recall succeeds
```

## Current Final State

```text
Fixture definition: READY
Trusted memory write: NOT DONE
Apply/promote: NOT DONE
Import/index refresh: NOT DONE
Recall verification: NOT DONE
Next milestone: M138 Hermes-agent Governed Trial-run Dry-run
```

## Personal-use Boundary

M137 remains:

```text
personal-local
small
Markdown-native
human-reviewed
no direct trusted memory write
no enterprise workflow expansion
no extra burden on Hermes-agent
```

## Final Lock

```text
Trial Promotion Fixture Definition
ACTIVE / fixture defined / not promoted
```
