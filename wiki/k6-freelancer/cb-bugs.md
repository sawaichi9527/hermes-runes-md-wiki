# Closed Beta Bug Ledger

Status: OPEN BUGS / M191.1 FINDINGS RECORDED
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
status: CLOSED_VERIFIED
stage_found: M191 BT-001 Read-only Rerun / Evidence Capture
case_id: BT-001
summary: Hermes-agent satisfied read-only output rules but read evidence from developer checkout after trial-local path lookup failed.
observed: The first M191 run attempted /home/eye/freelancer/docs/*.md, then searched and read /home/eye/workspace/hermes-runes-md-wiki/docs/*.md and wiki/k6-freelancer/*.md.
expected: Closed Beta trial evidence should come from the intended trial checkout / workspace context, not from the developer checkout fallback.
severity: high
scope_decision: fix_now
rerun_required: false
closure_evidence: M191.1 rerun used only /home/eye/workspace-trial/hermes-runes-md-wiki attempts and returned path_not_ready instead of falling back to /home/eye/workspace/hermes-runes-md-wiki.
```

### TB-M191-BT001-FU002

```text
id: TB-M191-BT001-FU002
status: OPEN
stage_found: M191.1 Trial Path Isolation Prompt / Environment Rerun Prep
case_id: BT-001
summary: Trial checkout evidence files are missing, preventing BT-001 from producing the final read-only technical answer from trial evidence.
observed: The M191.1 rerun attempted /home/eye/workspace-trial/hermes-runes-md-wiki/docs/m190-read-only-prompt-tightening.md, docs/cb-m191-m196-execution-pack.md, docs/m191-bt001-hermes-agent-run-prompt.md, and docs/m191-1-trial-path-isolation-rerun-prompt.md, but the files were missing or unreadable; Hermes-agent correctly returned path_not_ready.
expected: Trial checkout contains the current M190-M191.1 evidence files so BT-001 can be rerun from trial evidence only.
severity: high
scope_decision: fix_now
rerun_required: true
closure_evidence: PENDING; sync trial checkout to current origin/main, then rerun M191 using the path-isolated prompt.
```

Notes:

```text
The original M191 answer content preserved the read-only boundary:
- no trusted wiki mutation claimed
- no proposal-style content created
- no YAML-style memory block created
- no final_trial_result emitted
- no self-classification for M191 emitted
- candidate_result: ready_for_human_review was present

M191.1 verified the path isolation behavior:
- no developer checkout fallback observed
- path_not_ready was returned when trial evidence files were missing
- candidate_result: ready_for_human_review was present

M191 remains PARTIAL until BT-001 produces the final read-only answer from the synced trial checkout evidence.
```

## Known Limitations Accepted for CB

No known limitations accepted for Closed Beta yet.

## Final Lock

```text
Closed Beta Bug Ledger
OPEN BUGS / TB-M191-BT001-FU001 closed / TB-M191-BT001-FU002 opened
```
