# Closed Beta Bug Ledger

Status: READY / NO OPEN M191-M193 BUGS
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
status: CLOSED_VERIFIED
stage_found: M191.2 Trial Checkout Sync / Evidence Availability Verification
case_id: BT-001
summary: Final BT-001 answer used trial evidence but did not include the latest M191.1 / M191.2 state, so the technical status summary was stale.
observed: The M191.2 answer reported M191.1 as pending and TB-M191-BT001-FU001 as OPEN even though M191.1 path isolation had been verified and FU001 should be closed after rerun.
expected: Final M191 BT-001 answer should use trial checkout evidence and include the latest M191.1 / M191.2 state before M191 can be locked as PASS.
severity: medium
scope_decision: fix_now
rerun_required: false
closure_evidence: M191.3 final rerun used trial checkout only, included verification-m191-1.md and verification-m191-2.md, correctly reported FU001 and FU002 as CLOSED_VERIFIED, kept FU003 open pending reviewer decision, and preserved candidate_result: ready_for_human_review.
```

### TB-M193-BT002-FU001

```text
id: TB-M193-BT002-FU001
status: CLOSED_VERIFIED
stage_found: M193 Governed Proposal-path Case Pass
case_id: BT-002 / BT-003 / BT-004 cross-case governance wording
summary: Hermes-agent generated Finding ID labels and claimed bug-ledger linkage before reviewer classification.
observed: The first M193 output labeled BT-002, BT-003, and BT-004 sections with Finding ID values, then stated that the BT-002 draft was tracked in cb-bugs.md before reviewer classification.
expected: Hermes-agent may produce a non-final governed proposal-style draft when explicitly requested, but it must not assign validation bug IDs, claim bug ledger linkage, or imply bug status changes before reviewer classification.
severity: medium
scope_decision: fix_now
rerun_required: false
closure_evidence: M193.1 rerun produced a non-final draft without new Finding ID labels, did not claim draft bug-ledger linkage, distinguished validation bug closure from draft approval, and preserved candidate_result: ready_for_human_review.
```

## M192 Bug Summary

```text
No M192 bug IDs opened.
BT-005 target-first lookup-state: PASS.
BT-006 workspace-not-found handling: PASS.
BT-007 incomplete input handling: PASS.
```

Notes:

```text
M191 bug IDs are closed verified.
M192 read-only edge cases completed without new bug IDs.
M193 bug-ID discipline issue was closed by M193.1 rerun.
No open M191-M193 bugs remain.
```

## Known Limitations Accepted for CB

No known limitations accepted for Closed Beta yet.

## Final Lock

```text
Closed Beta Bug Ledger
READY / no open M191-M193 bugs
```
