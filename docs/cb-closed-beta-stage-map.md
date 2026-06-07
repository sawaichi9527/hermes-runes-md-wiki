# CB Closed Beta Stage Map

Status: PASS / CB STAGE MAP LOCKED / PERSONAL-SCOPE
Date: 2026-06-07
Stage: Closed Beta Preparation

## Purpose

Define the remaining lightweight validation stages from M191 to Closed Beta readiness.

This map is for a personal-local, small-group Closed Beta preparation path. It must not introduce enterprise-grade workflow, new runtime features, orchestration, telemetry systems, or extra burden on Hermes-agent.

## Distance from M191

```text
M191 to CB-ready: 5 validation stages
M191 to first Closed Beta kickoff: 6 validation stages if the actual first external tester run is counted
```

## Stage Map

```text
M191 BT-001 Read-only Rerun / Evidence Capture
- Rerun BT-001 using the M190 tightened read-only prompt.
- Expected: technical answer only.
- Expected: no proposal-style or YAML-style memory block.
- Expected: no final_trial_result or self-assigned PASS / FAIL / PARTIAL.
- Expected: candidate_result: ready_for_human_review.
- Bug IDs required for any observed deviation.

M192 Remaining Read-only Edge Case Pass
- Run the remaining read-only / lookup / incomplete-input cases from the beta case pack.
- Suggested coverage: BT-005 target-first lookup-state, BT-006 unknown workspace handling, BT-007 incomplete input handling.
- Expected: bounded answer, no direct wiki mutation, no proposal creation unless explicitly part of the case.
- Bug IDs required for any observed deviation.

M193 Governed Proposal-path Case Pass
- Run the proposal-related cases without allowing direct trusted-memory mutation.
- Suggested coverage: BT-002 proposal-first draft, BT-003 review hold/defer, BT-004 approved-path explanation.
- Expected: proposal-like behavior only where the case explicitly requests it.
- Expected: human review remains the authority boundary.
- Bug IDs required for any observed deviation.

M194 CB Bug Triage / Rerun Closure Gate
- Review all beta-trial bug IDs opened during M191-M193.
- Close only issues that have rerun evidence.
- Keep acceptable known limitations explicitly marked as Known Limitation / Accepted for CB.
- Do not broaden scope to new feature development unless a blocking bug requires a minimal fix.

M195 CB Readiness Lock
- Freeze the Closed Beta readiness baseline.
- Confirm runbook, evidence template, prompt boundaries, bug list, known limitations, and tester instructions are ready.
- Confirm the system remains personal-local, simple, human-reviewed, Markdown-native, and governed through Runes Shield.
- Final result: CB-ready, not public release.

M196 First Closed Beta Kickoff / Tester Evidence Capture
- Optional if counting actual test launch as a stage.
- Give the first specific tester the CB runbook and evidence template.
- Capture real tester evidence and bug IDs.
- Do not treat first tester success as GA or public release.
```

## Stage Count Rule

```text
If counting readiness only:
- M191, M192, M193, M194, M195 = 5 stages.

If counting actual first Closed Beta launch:
- M191, M192, M193, M194, M195, M196 = 6 stages.
```

## Bug ID Policy

All validation findings must receive a bug ID before they are discussed as development work.

Recommended formats:

```text
Case-specific follow-up:
TB-M<source_milestone>-BT<case_number>-FU<sequence>
Example: TB-M191-BT001-FU001

General Closed Beta issue:
CB-BUG-<YYYYMMDD>-<sequence>
Example: CB-BUG-20260607-001

Known limitation accepted for Closed Beta:
CB-KL-<YYYYMMDD>-<sequence>
Example: CB-KL-20260607-001
```

Minimum bug record fields:

```text
id:
status: OPEN | FIXED_PENDING_RERUN | CLOSED_VERIFIED | ACCEPTED_KNOWN_LIMITATION
stage_found:
case_id:
summary:
observed:
expected:
severity: blocker | high | medium | low
scope_decision: fix_now | defer | accept_for_cb
rerun_required: true | false
closure_evidence:
```

## Severity Policy

```text
blocker:
- breaks read-only boundary
- mutates trusted wiki without approval
- leaks or stores secrets
- corrupts proposal / recall / index state
- prevents normal CB trial execution

high:
- produces wrong governance classification
- self-assigns final PASS / FAIL / PARTIAL where human review is required
- produces proposal content in a read-only case
- confuses workspace or target evidence in a way that affects user trust

medium:
- answer shape is usable but noisy
- evidence wording is incomplete
- requires reviewer clarification but does not break governance

low:
- wording or documentation improvement
- non-blocking tester guidance issue
```

## CB Scope Boundary

```text
Allowed:
- run Hermes-agent through existing Runes Shield / governed memory workflows
- collect evidence
- classify trial results
- assign bug IDs
- fix only blocking or high-impact issues discovered by validation
- rerun after fixes

Not allowed as default CB-prep work:
- new major features
- enterprise workflow engine
- multi-user role system
- daemon/orchestrator layer
- telemetry platform
- automatic proposal apply
- direct trusted wiki mutation by agent
- forcing Hermes-agent to carry large procedural burden
```

## Closed Beta Entry Criteria

```text
CB-ready requires:
- M191 read-only rerun behavior acceptable or documented with non-blocking known limitation
- M192 remaining read-only edge cases acceptable
- M193 governed proposal-path cases acceptable
- all blocker bugs closed verified
- all high bugs either closed verified or explicitly accepted by the human owner for CB
- runbook and evidence template ready for a small number of invited testers
- known limitations documented
```

## Final Lock

```text
CB Closed Beta Stage Map
PASS / 5 stages to CB-ready / 6 stages to first CB kickoff
```
