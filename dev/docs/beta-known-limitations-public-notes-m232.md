# Beta Run Known Limitations / Public Notes - M232

Status: PASS / PUBLIC NOTES LOCKED / NO RUNTIME CHANGE
Date: 2026-06-08
Milestone: M232

## Purpose

Document current Open Beta known limitations and public notes after M231 locked the Beta Run baseline.

## Current Beta Baseline

- version: 0.1.0-beta.1
- tag: v0.1.0-beta.1
- beta_run_baseline: PASS
- observed: yes
- blocking_issue_found: no
- patch_round_required_now: no
- regression_smoke_replay: PASS

## Known Limitations

- Open Beta is not a stable release.
- Open Beta is not a production support commitment.
- GitHub Release URL and feedback Issue URL are still manual/deferred until publication URLs exist.
- M219.1 manual URL backfill remains deferred.
- The active workspace slug rule is hostname-derived: lowercase(hostname).
- The current dogfood host is Freelancer and current dogfood slug is freelancer; this is not a universal default.
- The legacy wiki/k6-freelancer namespace remains engineering provenance and is not the default public tester workspace.
- Runtime behavior is not changed by Beta observation notes.

## Public Tester Notes

- Start with docs/open-beta-starter.md.
- Use VERSION and tag v0.1.0-beta.1 as the current beta boundary.
- Use hostname-derived workspace slug rules for local workspaces.
- Treat docs/beta-observations/ as observed dogfood evidence, not a production stability guarantee.

## Deferred Items

- M219.1 manual URL backfill: deferred until release_url and feedback_issue_url exist.
- GitHub Release creation: optional manual publication task.
- GitHub Issue creation: optional manual feedback-channel task.

## Decision

- public_notes_locked: yes
- runtime_change_required: no
- documentation_patch_required_now: no
- beta_status_lock_changed: no
- next_action: beta_public_notes_review_or_release_note_alignment

## Next Step

M233 Beta Public Notes Review / Release Note Alignment

## Final Lock

M232 Beta Run Known Limitations / Public Notes
PASS / public notes locked / no runtime change
