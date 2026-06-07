# Public Notification Manual Send Record

Status: SCAFFOLD / CHANNEL SELECTION PENDING / NOT SENT
Date: 2026-06-08
Milestone: M217

## Purpose

Record the selected public notification channel and manual send status for Hermes Runes MD Wiki Open Beta.

This file is a send-record scaffold. It does not mean the notification has been sent.

## Send Source

```text
final_notification_file: docs/public-tester-notification-final.md
release_tag: v0.1.0-beta.1
version: 0.1.0-beta.1
```

## Candidate Channels

```text
GitHub Release note: recommended primary public channel
GitHub Discussion: optional, if Discussions are enabled
GitHub Issue: optional, if using a public feedback issue
README link/update: optional follow-up
private/internal channel: optional, if inviting known testers first
```

## Recommended Send Order

```text
1. GitHub Release note or repository-visible announcement
2. Optional GitHub Issue/Discussion for feedback collection
3. Optional private/internal tester notification pointing to the public repo and feedback channel
```

## Selected Channel

```text
selected_channel: pending
selected_channel_url: pending
feedback_channel: pending
```

## Send Status

```text
send_decision: ready_for_manual_send
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
SCAFFOLD / channel selection pending / notification not sent
```
