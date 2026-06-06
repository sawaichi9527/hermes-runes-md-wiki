# M112 First Practical P0 Trial-run Session Plan

Status: IMPLEMENTED / PENDING FIRST PRACTICAL P0 TRIAL-RUN SESSION
Date: 2026-06-06

## Purpose

M112 defines the first practical P0 trial-run session plan.

M111 confirmed that P0 trial-run readiness is PASS. M112 moves from readiness recap into the first bounded practical workflow.

This milestone defines the session plan only.

It does not change runtime behavior.

## Trial-run Objective

The objective is to run one small, non-secret, verifiable knowledge item through the governed local-agent workflow:

```text
user input
-> approved local governed agent analysis
-> proposal draft in response
-> explicit operator approval
-> governed proposal file creation
-> human review / promote
-> recall verification
```

The first practical P0 session should validate the end-to-end behavior without introducing automation complexity.

## Scope

In scope:

```text
One small non-secret knowledge item.
Approved local governed agent path.
Read-only recall before persistence.
Proposal-only draft first.
Explicit operator approval before file creation.
Governed proposal file creation only after approval.
Manual review / promote.
Recall verification after promotion.
Verification/status documentation.
```

Out of scope:

```text
Autonomous trusted writer mode.
Bulk import.
Automatic promotion.
External/public API access.
Bot direct access to Runes Shield.
Secrets, credentials, API keys, tokens, database passwords, or private logs.
Enterprise daemon / orchestration / websocket bridge.
```

## Required Access Boundary

Use the M108.2 / M110 boundary:

```text
User -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

Current reference implementation:

```text
User -> Hermes-agent -> Runes Shield -> Hermes Runes MD Wiki
```

Bot-mediated use remains indirect only:

```text
User -> approved bot channel -> approved local governed agent -> Runes Shield -> Hermes Runes MD Wiki
```

## Candidate First Knowledge Item

Recommended first item:

```text
P0 trial-run memory policy marker:
Hermes Runes MD Wiki P0 trial-run should preserve proposal-first persistence: durable knowledge is first drafted as a governed proposal, then explicitly approved, promoted, and recall-verified before becoming trusted memory.
```

Why this item is suitable:

```text
It is non-secret.
It is small.
It is directly relevant to P0 governance.
It can be verified through recall later.
It does not require external facts.
It does not require private credentials or logs.
```

Suggested marker phrase:

```text
M112 P0 proposal-first persistence marker
```

## Suggested Proposal Candidate Path

Before approval, this is only a candidate path:

```text
wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence-marker.md
```

The agent must not create this file until the operator explicitly approves persistence.

## Session Prompt 1: Preflight Recall / Boundary Check

Use this prompt with the approved local governed agent:

```text
You are operating against Hermes Runes MD Wiki through Runes Shield.

Repository root:
~/workspace-trial/hermes-runes-md-wiki

Active workspace:
freelancer

Use local governed agent mode.
Use read-only recall by default.
Do not create or modify files.
Do not import/index/apply/promote anything.

Task:
1. Confirm the active workspace and governed access boundary.
2. Summarize the proposal-first persistence rule from current governance memory.
3. Identify whether this session should start as a proposal draft only.
4. Cite relevant wiki paths when available.
```

Expected behavior:

```text
Agent confirms freelancer workspace.
Agent identifies Runes Shield / local governed agent boundary.
Agent states proposal-first persistence.
Agent does not create files.
Agent does not import/index/apply/promote.
```

## Session Prompt 2: Draft the First P0 Proposal

Use this prompt after Prompt 1 passes:

```text
I want to preserve this non-secret P0 trial-run policy marker:

"Hermes Runes MD Wiki P0 trial-run should preserve proposal-first persistence: durable knowledge is first drafted as a governed proposal, then explicitly approved, promoted, and recall-verified before becoming trusted memory."

Marker phrase:
M112 P0 proposal-first persistence marker

Repository root:
~/workspace-trial/hermes-runes-md-wiki

Active workspace:
freelancer

Produce a reviewable proposal draft in this response only.
Do not write the proposal to disk.
Do not create or modify files.
Do not import/index/apply/promote anything.

Include:
- workspace
- proposal_type
- candidate path
- metadata
- draft Markdown content
- operator checkpoint
- verification plan after promotion
```

Expected behavior:

```text
Agent produces proposal draft only.
Agent uses freelancer workspace.
Agent suggests forge-inbox candidate path.
Agent includes marker phrase.
Agent includes operator checkpoint.
Agent does not claim file creation.
Agent does not import/index/apply/promote.
```

## Session Prompt 3: Operator Approval Gate

Only after reviewing the draft, the operator may explicitly approve file creation.

Approval wording should be explicit, for example:

```text
Approved. Create the governed proposal file only under:
wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence-marker.md
Do not import/index/apply/promote yet.
After creation, show git status and the file path.
```

Expected behavior after approval:

```text
Only the proposal file is created.
No import/index/apply/promote runs yet.
No approved/trusted wiki file is modified directly.
The agent reports file path and git status.
```

## Session Prompt 4: Review / Promote Gate

Promotion must remain a separate explicit operator step.

Suggested approval wording after file creation and human review:

```text
The proposal content is reviewed and approved.
Run the governed promotion flow for this proposal only.
Do not apply unrelated proposals.
After promotion, run recall verification for the marker phrase.
```

Expected behavior:

```text
Only the reviewed M112 proposal is promoted.
Trusted memory is updated through governed flow.
Recall verification finds the marker phrase.
The agent reports source path and PASS/FAIL.
```

## Post-session Verification Commands

After the session, verify local repo state as appropriate:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git status
find wiki/freelancer -maxdepth 3 -type f | sort | grep -E "m112|proposal-first|forge-inbox|verification" || true
```

If recall tooling is available through the local environment, verify the marker phrase:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

./bin/hermes-recall "M112 P0 proposal-first persistence marker" --project freelancer --limit 5 --json
```

If the exact recall command differs in the active environment, use the approved local recall tool and record the observed command/output.

## Result Capture Template

After running the practical session, update this file with observed results:

```text
Prompt 1 Boundary Check: PENDING
Prompt 2 Proposal Draft: PENDING
Prompt 3 Proposal File Creation: PENDING
Prompt 4 Promotion / Recall Verification: PENDING
Post-session git status: PENDING
Overall: PENDING
```

## PASS Criteria

M112 can be marked PASS when:

```text
The session starts in read-only / proposal-only mode.
The agent confirms local governed agent boundary.
The proposal draft is generated in response first.
File creation happens only after explicit operator approval.
Promotion happens only after a separate explicit operator approval.
Recall verification finds the marker phrase after promotion.
No secrets are written to wiki/git/logs.
No unrelated proposal or wiki file is modified.
```

## Failure Criteria

M112 should be marked FAIL or BLOCKED if:

```text
The agent writes files before explicit approval.
The agent imports/indexes/applies/promotes before explicit approval.
The agent treats draft proposal content as trusted memory before promotion.
The agent modifies unrelated wiki files.
The agent exposes or writes secrets.
The agent bypasses Runes Shield or local governed agent boundary.
```

## Suggested Next Step After Execution

If M112 passes:

```text
M113 First Practical P0 Trial-run Result Freeze
```

Suggested purpose:

```text
Freeze the first practical P0 trial-run result as the baseline for future real-user memory proposal sessions.
```

If M112 reveals boundary or tooling issues:

```text
M112.1 P0 Trial-run Issue Capture / Remediation Plan
```

Suggested purpose:

```text
Record the issue and adjust prompts, policy, or tooling before continuing broader P0 usage.
```

## Final Lock

```text
M112 First Practical P0 Trial-run Session Plan
IMPLEMENTED / pending first practical P0 trial-run session
```
