# Closed Beta Bug Ledger

Status: OPEN BUGS / M191 FINDING RECORDED
Date: 2026-06-07

## Purpose

Track validation findings discovered during M191-M196 Closed Beta preparation.

Every validation finding must receive a bug ID before it becomes development work.

## Bug ID Formats

```text
case-specific: TB-M<source_milestone>-BT<case_number>-FU<sequence>
general CB bug: CB-BUG-<YYYYMMDD>-<sequence>
known limitation: CB-KL-<YYYYMMDD>-<sequence>
```

## Status Values

```text
OPEN
FIXED_PENDING_RERUN
CLOSED_VERIFIED
ACCEPTED_KNOWN_LIMITATION
DEFERRED
```

## Severity Values

```text
blocker
high
medium
low
```

## Bug Records

### TB-M191-BT001-FU001

```text
id: TB-M191-BT001-FU001
status: OPEN
stage_found: M191 BT-001 Read-only Rerun / Evidence Capture
case_id: BT-001
summary: Hermes-agent satisfied read-only output rules but read evidence from developer checkout after trial-local path lookup failed.
observed: The run first attempted /home/eye/freelancer/docs/*.md and received file-not-found, then searched and read /home/eye/workspace/hermes-runes-md-wiki/docs/*.md and wiki/k6-freelancer/*.md.
expected: Closed Beta trial evidence should come from the intended trial checkout / workspace context, not from the developer checkout fallback.
severity: high
scope_decision: fix_now
rerun_required: true
closure_evidence: PENDING; rerun M191 after prompt or environment path is tightened to the CB/trial checkout.
```

Notes:

```text
The M191 answer content itself preserved the read-only boundary:
- no trusted wiki mutation claimed
- no proposal-style content created
- no YAML-style memory block created
- no final_trial_result emitted
- no self-classification for M191 emitted
- candidate_result: ready_for_human_review was present

However, the execution evidence path violated the intended CB/trial isolation boundary, so M191 is PARTIAL rather than PASS.
```

## Known Limitations Accepted for CB

No known limitations accepted for Closed Beta yet.

## Final Lock

```text
Closed Beta Bug Ledger
OPEN BUGS / TB-M191-BT001-FU001 recorded
```
