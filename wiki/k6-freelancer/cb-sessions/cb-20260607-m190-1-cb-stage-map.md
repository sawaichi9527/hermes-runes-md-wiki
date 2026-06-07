# CB-20260607-M190.1 Closed Beta Stage Map / Bug Tracking Boundary

Status: PASS / CB STAGE MAP LOCKED
Date: 2026-06-07
Milestone: M190.1
Stage: Closed Beta Preparation

## Purpose

Record the remaining validation stages from M191 to Closed Beta readiness and lock the lightweight bug ID policy for beta validation findings.

This is documentation and planning only. It does not add new runtime features.

## Operating Decision

```text
Default operation model:
- Assistant directly updates the GitHub repository.
- User pulls and verifies locally.
- If GitHub connector limitations block an update, provide a local patch script.
- If a file is too large for safe code-block patching, provide a complete downloadable file and tell the user the exact overwrite path.
```

## Product Boundary

```text
Current phase: real validation / Closed Beta preparation.
Primary actor: Hermes-agent through existing Runes Shield / governed memory workflows.
Default work type: run scenarios, collect evidence, classify results, assign bug IDs, rerun after fixes.
Not default work type: build new features.
```

## Distance from M191

```text
M191 to CB-ready: 5 validation stages.
M191 to first Closed Beta kickoff: 6 validation stages if the first tester run is counted.
```

## Remaining Stages

```text
M191 BT-001 Read-only Rerun / Evidence Capture
M192 Remaining Read-only Edge Case Pass
M193 Governed Proposal-path Case Pass
M194 CB Bug Triage / Rerun Closure Gate
M195 CB Readiness Lock
M196 First Closed Beta Kickoff / Tester Evidence Capture
```

## Bug ID Rule

```text
Every validation finding must get an ID before becoming development work.
Use TB-M<source_milestone>-BT<case_number>-FU<sequence> for case-specific follow-up.
Use CB-BUG-<YYYYMMDD>-<sequence> for general Closed Beta issues.
Use CB-KL-<YYYYMMDD>-<sequence> for known limitations accepted for Closed Beta.
```

## Closed Beta Entry Criteria

```text
- M191 read-only rerun behavior acceptable or documented as non-blocking known limitation.
- M192 remaining read-only edge cases acceptable.
- M193 governed proposal-path cases acceptable.
- All blocker bugs closed verified.
- All high bugs closed verified or explicitly accepted by the human owner for CB.
- Runbook and evidence template ready for a small number of invited testers.
- Known limitations documented.
```

## Evidence Record

```text
docs/cb-closed-beta-stage-map.md
wiki/k6-freelancer/cb-sessions/cb-20260607-m190-1-cb-stage-map.md
wiki/k6-freelancer/verification-m190-1.md
```

## Next Step

```text
M191 BT-001 Read-only Rerun / Evidence Capture
```

## Final Lock

```text
M190.1 Closed Beta Stage Map / Bug Tracking Boundary
PASS / CB stage map locked / 5 stages to CB-ready
```
