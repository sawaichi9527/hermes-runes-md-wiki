# Trial Promotion Fixture Definition

Status: TEMPLATE / M137 TRIAL PROMOTION FIXTURE
Date: 2026-06-06

## Purpose

This template defines the small trial promotion fixture used by the beta-prep mainline.

It is not trusted memory by itself.

It is not an approved proposal by itself.

It must only become durable memory through the governed proposal flow and human review.

## Fixture Metadata

```text
Fixture ID: TPF-20260606-M137
Workspace slug: freelancer
Project: freelancer
Candidate target path: wiki/freelancer/trial-promotion-fixtures.md
Fixture type: beta-prep governed recall marker
Fixture scope: small / non-sensitive / workspace-scoped
Human review required: yes
Promotion allowed before review: no
```

## Fixture Content Draft

The following content is the approved shape for a future proposal draft.

Do not write it directly into trusted memory during M137.

```markdown
## TPF-20260606-M137 Beta-prep Governed Recall Marker

Status: TEST FIXTURE / HUMAN-REVIEWED BEFORE PROMOTION

Purpose:
- Verify that the beta-prep governed promotion path can preserve a small workspace-scoped fact.
- Verify that the promoted fixture can be recalled after import/index refresh.
- Verify that PASS freeze requires recall evidence.

Recall marker:
- M137 beta-prep trial promotion fixture marker

Expected recall query:
- M137 beta-prep trial promotion fixture marker

Expected source path after approved promotion:
- wiki/freelancer/trial-promotion-fixtures.md

Boundary:
- This fixture contains no private credentials, tokens, keys, personal data, customer data, or external service configuration.
- This fixture must not be promoted without explicit human approval.
- This fixture must not bypass Runes Shield governance.
```

## Required Review Checklist

Before using this fixture in M138/M139, confirm:

```text
[ ] Fixture is small.
[ ] Fixture is non-sensitive.
[ ] Fixture is workspace-scoped to freelancer.
[ ] Fixture has a stable recall marker.
[ ] Candidate target path is explicit.
[ ] Human approval is recorded before promotion.
[ ] No direct trusted memory write occurs.
[ ] No import/index/apply/promote occurs during M137.
```

## Expected Future M139 Evidence

M139 should not be marked PASS unless evidence includes:

```text
approved fixture content
proposal path or identifier
promotion/apply command or manual step
import/index refresh evidence if needed
recall query
recall result
source path evidence
working tree status
PASS / FAIL / BLOCKED classification
```

## Final Lock

```text
Trial Promotion Fixture Definition
TEMPLATE / ready for governed proposal flow / not promoted
```
