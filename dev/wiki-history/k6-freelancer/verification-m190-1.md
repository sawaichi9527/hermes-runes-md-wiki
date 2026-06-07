# M190.1 Closed Beta Stage Map / Bug Tracking Boundary

Status: PASS / CB STAGE MAP LOCKED / BUG TRACKING BOUNDARY READY
Date: 2026-06-07

## Evidence Record

```text
docs/cb-closed-beta-stage-map.md
wiki/k6-freelancer/cb-sessions/cb-20260607-m190-1-cb-stage-map.md
wiki/k6-freelancer/verification-m190.md
```

## Scope

```text
Closed Beta stage count
M191-to-CB readiness map
lightweight bug ID policy
no runtime feature development
```

## Result

```text
PASS
```

## Verification Notes

```text
M191 to CB-ready is locked as 5 validation stages:
- M191 BT-001 Read-only Rerun / Evidence Capture
- M192 Remaining Read-only Edge Case Pass
- M193 Governed Proposal-path Case Pass
- M194 CB Bug Triage / Rerun Closure Gate
- M195 CB Readiness Lock

M191 to first Closed Beta kickoff is 6 stages if M196 First Closed Beta Kickoff / Tester Evidence Capture is counted.

All validation findings must receive a bug ID before becoming development work.
The default flow remains: assistant updates GitHub, user pulls and verifies.
The CB phase must run existing scenarios through Hermes-agent and Runes Shield rather than expanding product scope.
```

## Bug ID Formats

```text
case-specific: TB-M<source_milestone>-BT<case_number>-FU<sequence>
general CB bug: CB-BUG-<YYYYMMDD>-<sequence>
known limitation: CB-KL-<YYYYMMDD>-<sequence>
```

## Boundary

```text
Allowed:
- scenario execution
- evidence capture
- result classification
- bug ID tracking
- minimal bug fixes only when validation reveals a blocker or high-impact issue

Not allowed by default:
- new major features
- enterprise workflow engine
- daemon/orchestrator layer
- telemetry platform
- automatic proposal apply
- direct trusted wiki mutation by agent
- procedural burden that makes Hermes-agent harder to use
```

## Next Step

```text
M191 BT-001 Read-only Rerun / Evidence Capture
```

## Final Lock

```text
M190.1 Closed Beta Stage Map / Bug Tracking Boundary
PASS / CB stage map locked / bug tracking boundary ready
```
