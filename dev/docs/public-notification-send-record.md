# Public Notification Manual Send Record

Status: CHANNEL LOCKED / MANUAL SEND PACKAGE READY / NOT SENT
Date: 2026-06-08
Milestone: M218

## Purpose

Record the selected public notification channel and manual send status for Hermes Runes MD Wiki Open Beta.

This file records the selected channels and the manual-send package. It does not mean the notification has been sent.

## Send Source

```text
final_notification_file: docs/public-tester-notification-final.md
release_note_draft: docs/github-release-note-v0.1.0-beta.1.md
feedback_issue_draft: docs/open-beta-feedback-issue-draft.md
release_tag: v0.1.0-beta.1
version: 0.1.0-beta.1
```

## Selected Channels

```text
primary_public_channel: GitHub Release note for v0.1.0-beta.1
feedback_channel: GitHub Issue for Open Beta feedback
optional_channel: private/internal tester message linking to release and feedback issue
```

## Manual Send URLs

```text
release_url: pending_manual_creation
feedback_issue_url: pending_manual_creation
internal_notification_url: optional_pending
```

## Recommended Send Order

```text
1. Create GitHub Release for v0.1.0-beta.1 using docs/github-release-note-v0.1.0-beta.1.md.
2. Create GitHub Issue using docs/open-beta-feedback-issue-draft.md.
3. Optionally send a private/internal tester message linking to the release and feedback issue.
4. Return here and update this record with release_url, feedback_issue_url, sent_at, and sent_by.
```

## Send Status

```text
send_decision: ready_for_manual_send
selected_channel: GitHub Release note
feedback_channel: GitHub Issue
notification_sent: no
manual_send_required: yes
sent_at: pending
sent_by: pending
```

## Required Message Boundary

```text
Open Beta only
not stable release
not production support
not enterprise support
workspace slug is lowercase(hostname)
freelancer is current dogfood host example only
no real secrets in Markdown wiki or git
feedback should include commands/logs/host OS/Python version/workspace slug
```

## Final Lock

```text
Public Notification Manual Send Record
CHANNEL LOCKED / manual send package ready / notification not sent
```
