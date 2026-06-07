# CB-20260608-M217 Public Notification Channel Selection

Status: PASS / SEND RECORD SCAFFOLD PREPARED / CHANNEL SELECTION PENDING / NOT SENT
Date: 2026-06-08
Milestone: M217
Stage: Open Beta Publication

## Purpose

Prepare the public notification channel selection and manual send record scaffold without claiming that the Open Beta notification has been sent.

## Inputs

```text
M213 first Open Beta tag: PASS
M214 host-derived workspace slug policy correction: PASS
M214.1 env example host slug hotfix: PASS
M215 public tester notification draft: PASS
M216 public tester notification final review: PASS
release_tag: v0.1.0-beta.1
version: 0.1.0-beta.1
```

## Send Record Location

```text
docs/public-notification-send-record.md
```

## Candidate Channels

```text
GitHub Release note: recommended primary public channel
GitHub Discussion: optional
GitHub Issue: optional feedback collection channel
README link/update: optional follow-up
private/internal channel: optional first tester invitation
```

## Send Decision

```text
send_decision: ready_for_manual_send
selected_channel: pending
notification_sent: no
manual_send_required: yes
```

## Next Step

```text
M218 Manual Notification Send / Feedback Channel Lock
```

## Final Lock

```text
M217 Public Notification Channel Selection / Manual Send Record
PASS / send record scaffold prepared / channel selection pending / not sent
```
