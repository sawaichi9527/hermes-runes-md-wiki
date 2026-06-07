# M37.1 — Proposal Draft Schema

Status: PASS / SCHEMA VERIFIED
Stage: P0 Proposal Drafting Layer
Subsystem: Human-Governed Proposal Draft Schema
Date: 2026-06-03

## Objective

Define the first formal proposal draft schema for M37.

The schema represents:

- agent-authored proposal drafts
- passive Runes Shield assessment
- human final review handoff

The schema must not allow approval or apply execution.

## Implemented Components

| Component | Path |
|---|---|
| Proposal schema | `tools/runes_shield/proposal_schema.json` |
| Schema validator | `tools/runes_shield/validate_proposal_schema.py` |
| Schema smoke | `tools/runes_shield/smoke_proposal_schema.py` |

## Draft Status Model

Allowed draft states:

```text
- draft
- quarantine
- pending_human_review
```

Blocked states:

```text
- approved
- applied
- promoted
- trusted
```

## Role Boundary

| Role | Responsibility |
|---|---|
| Hermes-agent | proposal drafting |
| Runes Shield | assessment only |
| Human | final review and decision |

## Required Assessment Fields

The schema requires passive assessment metadata:

- credibility_level
- risk_level
- source_evidence
- policy_notes
- quarantine_recommendation

## Blocked Capabilities

The schema explicitly blocks:

```text
trusted_wiki_write=false
automatic_approval=false
automatic_promotion=false
apply_execution=false
database_mutation=false
```

## Workflow

```text
user-provided content
-> Hermes-agent interpretation
-> proposal draft
-> Runes Shield assessment
-> pending human review
```

## Verification

Run:

```bash
python3 tools/runes_shield/smoke_proposal_schema.py
```

Expected:

```text
PASS: proposal schema validation completed
```

## Result

M37.1 establishes the first formal schema for human-governed proposal drafts in Runes Shield.
