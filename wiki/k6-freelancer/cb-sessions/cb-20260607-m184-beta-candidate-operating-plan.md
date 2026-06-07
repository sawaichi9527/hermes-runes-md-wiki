# CB-20260607-M184 Beta Candidate Operating Plan

Status: PASS / OPERATING PLAN LOCKED
Date: 2026-06-07
Milestone: M184
Stage: Beta Candidate Planning

## Purpose

Define how the beta candidate baseline should be used after M183.

M184 records the operating model for the next controlled beta-candidate preparation stage.

## Boundary

```text
personal-local scope
planning / operating model only
no runtime behavior change
no broad beta launch
```

## Inputs

```text
M183 Beta Candidate Baseline Recap
M182 Beta Entry Checklist
M181 Candidate Scope Lock
M180 Readiness Review
```

## Operating Model

```text
User role:
- provides technical input or asks for recall/state clarification
- reviews proposed memory changes before they become trusted records

Agent role:
- analyzes input
- drafts governed proposals when memory write is appropriate
- explains approved-path steps without claiming completion
- answers target-first lookup-state questions before broad checks

Wiki/RAG role:
- remains the governed Markdown source-of-truth
- stores reviewed knowledge only after human decision
- provides recall evidence for later technical comparison

Human review role:
- accepts, holds, defers, rejects, or requests revision
- keeps final authority over trusted memory content
```

## Allowed Beta Candidate Behaviors

```text
read-only technical analysis
proposal-first draft response
review hold/defer handling
approved-path explanation
target-first lookup-state answer
trial evidence capture
bounded documentation updates
```

## Not Included

```text
public beta release
enterprise deployment
multi-user production operation
automatic proposal apply
agent direct trusted-memory update
runtime authority expansion
```

## Evidence Policy

```text
Every real beta trial run should record:
- scenario id
- input source
- expected behavior
- actual behavior
- boundary result
- follow-up issue when needed

Run milestones need real run evidence before PASS.
Planning milestones may PASS as documentation locks.
```

## Next Step

```text
M185 Beta Trial Runbook
```

## Final Lock

```text
M184 Beta Candidate Operating Plan
PASS / operating plan locked / ready for M185 runbook
```
