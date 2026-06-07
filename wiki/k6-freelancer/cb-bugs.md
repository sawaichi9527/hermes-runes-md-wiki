# Closed Beta Bug Ledger

Status: OPEN BUGS / M191 FINAL STATE FOLLOW-UP RECORDED
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
status: CLOSED_VERIFIED
stage_found: M191.1 Trial Path Isolation Prompt / Environment Rerun Prep
case_id: BT-001
summary: Trial checkout evidence files were missing, preventing BT-001 from producing the final read-only technical answer from trial evidence.
observed: The M191.1 rerun attempted trial checkout files and returned path_not_ready because evidence was missing or unreadable.
expected: Trial checkout contains the current M190-M191.1 evidence files so BT-001 can be rerun from trial evidence only.
severity: high
scope_decision: fix_now
rerun_required: false
closure_evidence: M191.2 rerun successfully read required M190/M191 evidence files from /home/eye/workspace-trial/hermes-runes-md-wiki and did not fall back to developer checkout.
```

### TB-M191-BT001-FU003

```text
id: TB-M191-BT001-FU003
status: OPEN
stage_found: M191.2 Trial Checkout Sync / Evidence Availability Verification
case_id: BT-001
summary: Final BT-001 answer used trial evidence but did not include the latest M191.1 / M191.2 state, so the technical status summary was stale.
observed: The answer reported M191.1 as pending and TB-M191-BT001-FU001 as OPEN even though M191.1 path isolation had been verified and FU001 should be closed after rerun. The evidence list did not include verification-m191-1.md or verification-m191-2.md.
expected: Final M191 BT-001 answer should use trial checkout evidence and include the latest M191.1 / M191.2 state before M191 can be locked as PASS.
severity: medium
scope_decision: fix_now
rerun_required: true
closure_evidence: PENDING; run M191.3 with updated evidence list including verification-m191-1.md and verification-m191-2.md.
```

Notes:

```text
The original M191 answer content preserved the read-only boundary.
M191.1 verified path isolation behavior.
M191.2 verified trial checkout evidence availability.
M191 still needs one final BT-001 rerun using the updated evidence list so the status summary is current.
```

## Known Limitations Accepted for CB

No known limitations accepted for Closed Beta yet.

## Final Lock

```text
Closed Beta Bug Ledger
OPEN BUGS / TB-M191-BT001-FU003 recorded
```
