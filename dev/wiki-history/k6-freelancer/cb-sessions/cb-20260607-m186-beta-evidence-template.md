# CB-20260607-M186 Beta Evidence Template

Status: PASS / EVIDENCE TEMPLATE LOCKED
Date: 2026-06-07
Milestone: M186
Stage: Beta Candidate Planning

## Purpose

Define the reusable evidence template for future beta-candidate trial runs.

M186 turns the M185 runbook evidence fields into a stable record format.

## Boundary

```text
personal-local scope
evidence template only
no runtime behavior change
no actual trial execution in M186
```

## Inputs

```text
M184 Beta Candidate Operating Plan
M185 Beta Trial Runbook
```

## Evidence Template

```yaml
scenario_id: ""
milestone: ""
date: "2026-06-07"
stage: "Beta Candidate Trial"

input_source:
  prompt_file: ""
  user_request_summary: ""
  workspace_root: "~/workspace-trial/hermes-runes-md-wiki"

scenario_type: ""
expected_behavior:
  - ""

actual_behavior:
  summary: ""
  observed_steps:
    - ""

boundary_result:
  result: "PASS | PARTIAL | BLOCKED"
  notes:
    - ""

observations:
  write_observed: false
  proposal_observed: false
  state_claim_observed: false
  unexpected_path_observed: false
  unrelated_fixture_first_observed: false

files_or_records_touched:
  - ""

follow_up:
  required: false
  issue_id: ""
  note: ""

final_result: "PASS | PARTIAL | BLOCKED"
```

## Required Rules

```text
Use real run evidence for trial execution milestones.
Do not mark a trial run PASS from template preparation alone.
Record both expected and actual behavior.
Record boundary notes even when the run is PASS.
Use absolute trial-root paths when a prompt file is involved.
```

## Scenario Type Values

```text
read_only_technical_input
proposal_first_draft
review_hold_defer
approved_path_explanation
target_first_lookup_state
unknown_workspace_handling
incomplete_input_handling
```

## Result Values

```text
PASS
PARTIAL
BLOCKED
```

## Next Step

```text
M187 Beta Trial Case Pack
```

## Final Lock

```text
M186 Beta Evidence Template
PASS / evidence template locked / ready for M187 case pack
```
