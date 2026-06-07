# CB-20260607-M185 Beta Trial Runbook

Status: PASS / BETA TRIAL RUNBOOK LOCKED
Date: 2026-06-07
Milestone: M185
Stage: Beta Candidate Planning

## Purpose

Define the executable runbook for future beta-candidate trial runs.

M185 converts the M184 operating model into a step-by-step trial procedure.

## Boundary

```text
personal-local scope
runbook/documentation only
no runtime behavior change
no actual trial execution in M185
```

## Inputs

```text
M183 Beta Candidate Baseline Recap
M184 Beta Candidate Operating Plan
```

## Trial Preparation

```text
1. Select one scenario id.
2. Confirm the repo is clean and synced.
3. Confirm whether the scenario is read-only, proposal-first, hold/defer, approved-path, or lookup-state.
4. Prepare a single prompt file under docs/ or cb-sessions/ as appropriate.
5. Use absolute trial-root paths when asking Hermes-agent to read a prompt file.
6. Do not treat a planning milestone as a trial execution result.
```

## Trial Execution Flow

```text
1. Start from the prepared prompt file.
2. Ask Hermes-agent to read and execute only that prompt.
3. Observe whether the agent follows the expected boundary.
4. Record actual behavior as evidence.
5. Classify result as PASS, PARTIAL, or BLOCKED.
6. Record any follow-up issue when needed.
7. Do not mark trial PASS unless real run evidence exists.
```

## Expected Evidence Fields

```text
scenario_id:
input_source:
expected_behavior:
actual_behavior:
boundary_result:
write_observed:
proposal_observed:
state_claim_observed:
follow_up:
final_result:
```

## Candidate Scenario Types

```text
read-only technical input
proposal-first draft
review hold/defer
approved-path explanation
target-first lookup-state
unknown workspace handling
incomplete user input handling
```

## Result Classification

```text
PASS:
- expected behavior observed
- no unexpected file write or state claim
- evidence is recorded

PARTIAL:
- mostly correct behavior with minor friction or incomplete evidence
- follow-up note required

BLOCKED:
- missing required evidence
- unsafe state claim
- unexpected mutation
- wrong workspace or path behavior
```

## Next Step

```text
M186 Beta Evidence Template
```

## Final Lock

```text
M185 Beta Trial Runbook
PASS / runbook locked / ready for M186 evidence template
```
