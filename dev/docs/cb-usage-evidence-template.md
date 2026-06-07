# Closed Beta Usage Evidence Template

Status: READY / USE FOR M197 CLOSED BETA EVIDENCE CAPTURE
Date: 2026-06-07

## Purpose

Provide a lightweight template for recording real small-group Closed Beta usage evidence after M196 kickoff.

This template is for evidence capture only. It does not promote content into trusted memory, does not replace human review, and does not create development work by itself.

## Usage Record Template

```text
record_id: CB-USE-YYYYMMDD-NNN
record_date: YYYY-MM-DD
source: human tester / Hermes-agent interaction / reviewer note
workspace: k6-freelancer or other explicit workspace
scenario: short scenario name
input_summary: short sanitized summary
output_summary: short sanitized summary
observed_behavior: what happened
expected_behavior: what should happen, if different
reviewer_notes: human reviewer notes
classification: evidence_only / follow_up_needed / candidate_bug / candidate_improvement / candidate_docs_update
linked_bug_id: none or existing bug ID
secrets_checked: yes / no
raw_sensitive_content_included: no
next_step: none / open bug ID / rerun / docs update / defer
```

## Rules

```text
- Do not include API keys, tokens, passwords, private customer data, or raw confidential payloads.
- Use summaries instead of full prompts or full outputs when sensitive content may exist.
- A usage record is evidence, not trusted memory.
- A candidate bug must be assigned a bug ID in cb-bugs.md before development work starts.
- A candidate docs update must be reviewed before becoming trusted wiki content.
- Do not ingest this file into RAG as factual project memory without review.
```

## Minimal Example

```text
record_id: CB-USE-20260607-001
record_date: 2026-06-07
source: human tester
workspace: k6-freelancer
scenario: read-only status lookup
input_summary: tester asked for current CB status
output_summary: assistant returned M191-M196 state summary
observed_behavior: response preserved read-only boundary and cited current verification files
expected_behavior: same
reviewer_notes: usable as expected
classification: evidence_only
linked_bug_id: none
secrets_checked: yes
raw_sensitive_content_included: no
next_step: none
```

## Final Lock

```text
Closed Beta Usage Evidence Template
READY / use for M197 evidence capture
```
