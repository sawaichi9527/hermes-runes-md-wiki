# M37 — Proposal Assessment Role Lock

Status: PASS / ROLE LOCK
Stage: P0 Proposal Drafting Preparation
Subsystem: Human-Governed Proposal Workflow
Date: 2026-06-03

## Objective

Lock the role model for M37 before implementing proposal drafting.

M37 must not describe Runes Shield as the governance authority.

Runes Shield is an assessment and decision-support layer.

Human remains the final decision authority.

## Correct Role Model

| Role | Project Term | Responsibility |
|---|---|---|
| Human | Decision Authority / Accountable Reviewer | final accept / reject / revise / defer decision |
| Hermes-agent | Proposal Author / Drafting Agent | understands user content and drafts candidate memory proposals |
| Runes Shield | Assessment Layer / Decision-Support Layer | provides credibility, risk, evidence, and policy-reference analysis |
| wiki/_system policy | Assessment Criteria / Policy Reference | provides criteria used for analysis, not automatic approval |
| Future Attunement | Human Review Workflow | human review and final judgment process |
| Future Forge / Apply | Execution Layer | applies approved changes later, outside M37 |

## Locked Statement

```text
Human governs.
Human decides.
Human remains accountable.

Hermes-agent drafts.
Runes Shield assesses.
Runes Shield does not govern.
```

## M37 Definition

```text
M37 implements agent-authored proposal drafts with Runes Shield assessment for human final decision.
```

Chinese definition:

```text
M37 實作由 Hermes-agent 草擬的記憶提案，Runes Shield 僅提供可信度 / 風險 / policy 對照分析，最後由人類做最終判斷。
```

## Allowed in M37

M37 may implement:

- proposal draft schema
- proposal draft creation
- passive credibility assessment
- passive risk assessment
- source evidence summary
- policy-reference checklist
- quarantine / pending-review output
- human review handoff metadata

## Blocked in M37

M37 must not implement:

- trusted wiki write
- proposal approval
- automatic promotion
- apply execution
- database mutation
- final governance decision
- autonomous memory solidification

## Workflow Boundary

```text
user-provided content
-> Hermes-agent interpretation
-> proposal draft
-> Runes Shield assessment
-> human final review
```

Runes Shield assessment may inform the human reviewer, but it must not replace the reviewer.

## Completion Criteria

M37 role lock is PASS when:

- Runes Shield is defined as assessment / decision-support only
- Human is defined as final decision authority
- Hermes-agent is defined as proposal author / drafting agent
- M37 blocked behaviors are documented
- future apply behavior remains outside M37

## Result

M37 can proceed to proposal drafting implementation without confusing passive assessment with active governance.
