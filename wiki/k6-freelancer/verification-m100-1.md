# M100.1 Hermes-agent Integration Bootstrap Preflight

Status: IMPLEMENTED / PENDING LOCAL VERIFICATION
Date: 2026-06-06

## Purpose

M100.1 fills the gap between M99 preparation and M100 agent-facing trial execution.

It defines the minimum preflight contract for connecting Hermes-agent to Hermes Runes MD Wiki in read-only and proposal-only mode.

This milestone does not enable direct source mutation.

## Position

Current chain:

```text
M98 Controlled Trial-run Readiness Freeze: PASS
M99 First Agent-facing Trial Usage Preparation: PASS
M100 First Agent-facing Trial Execution Capture: IMPLEMENTED / pending agent trial execution
```

M100.1 is required before M100 execution because Hermes-agent has not yet been connected to Hermes Runes MD Wiki.

## Integration Mode

Initial integration mode:

```text
read-only recall/search
proposal-only memory preparation
operator-confirmed persistence only
```

Hermes-agent may read and summarize governed memory. It may prepare a proposal draft for operator review. It must not directly change approved wiki content during the initial integration trial.

## Required Local Paths

Developer/reference repo:

```text
/home/eye/workspace/hermes-runes-md-wiki
```

Trial repo:

```text
/home/eye/workspace-trial/hermes-runes-md-wiki
```

Initial workspace slug:

```text
freelancer
```

## Required Discovery Docs

Hermes-agent should be able to discover and read these docs before executing M100 scenarios:

```text
wiki/hermes_runes_index.md
wiki/_system/runes_agent_guidance.md
wiki/_system/runes_shield_contract.md
wiki/_system/wiki-operation-policy.md
wiki/_system/memory-policy.md
wiki/_system/source-priority.md
wiki/freelancer/README.md
wiki/freelancer/baselines.md
```

Optional validation fixture:

```text
wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
```

## Read-only Recall Contract

Hermes-agent should call recall/search through an explicit read-only command path.

Reference command form:

```bash
cd ~/workspace/hermes-runes-md-wiki
./bin/hermes-recall "<query>" --project freelancer --limit 5 --json
```

Acceptable initial queries:

```text
Hermes Runes index
Runes Shield contract
freelancer baseline
M94 trial promotion fixture
missing workspace policy
```

Expected behavior:

```text
recall returns governed Markdown sources
agent summarizes sources without treating recall result as write authority
agent names source paths when possible
```

## Active Workspace Contract

Initial active workspace:

```text
freelancer
```

Hermes-agent should not infer unrelated workspaces from old project history.

When workspace is unclear, expected response:

```text
No active workspace is confirmed yet.
Please confirm the workspace slug or approve preparing a governed workspace proposal.
```

## Proposal-only Contract

When the operator asks to preserve a new fact, Hermes-agent should produce a proposal draft structure only.

Expected proposal draft fields:

```text
workspace: freelancer
proposal_type: memory_update
source_summary: <operator supplied fact or source>
proposed_location: <candidate wiki path>
proposed_content: <draft Markdown>
operator_checkpoint: required before persistence
```

The proposal draft may be shown in conversation. It should not be applied to approved wiki files automatically.

## Stop Points

Hermes-agent must stop and ask for operator confirmation before:

```text
creating a new wiki file
editing an existing approved wiki file
importing/indexing a new proposal into long-term memory
changing workspace slug
promoting a draft to approved memory
```

## Preflight Checks

Before running M100 scenarios, verify:

```text
P1: Hermes-agent can locate the repo root.
P2: Hermes-agent can read wiki/hermes_runes_index.md.
P3: Hermes-agent can read wiki/_system/runes_agent_guidance.md.
P4: Hermes-agent can run or request read-only recall for project freelancer.
P5: Hermes-agent can identify active workspace freelancer.
P6: Hermes-agent can explain proposal-only behavior.
P7: Hermes-agent stops before persistence and requests operator confirmation.
```

## Suggested Manual Preflight Prompts

### Preflight Prompt 1

```text
Use Hermes Runes MD Wiki as read-only governed memory. First identify the repository root, then read or recall wiki/hermes_runes_index.md and tell me what workspace you can safely operate in.
```

Expected result:

```text
Agent identifies repository root or asks for it.
Agent names the index document.
Agent identifies freelancer as the initial trial workspace or asks for confirmation.
```

### Preflight Prompt 2

```text
Recall or inspect the Runes Shield and wiki operation guidance. Summarize what you are allowed to do before operator approval.
```

Expected result:

```text
Agent describes read-only and proposal-only behavior.
Agent says persistence requires operator confirmation.
```

### Preflight Prompt 3

```text
Use read-only recall for project freelancer and find the M94 trial promotion fixture. Explain why it exists without modifying anything.
```

Expected result:

```text
Agent finds or names the fixture path.
Agent explains it is trial/governance evidence.
Agent does not modify files.
```

## Completion Criteria

M100.1 can be marked PASS when:

```text
Integration mode is documented.
Repo root and active workspace are documented.
Read-only recall contract is documented.
Proposal-only contract is documented.
Stop points are documented.
Preflight prompts are documented.
Operator confirms this is sufficient before connecting Hermes-agent.
```

## Suggested Next Step

After M100.1 PASS, proceed to either:

```text
M100.2 Hermes-agent Integration Preflight Execution Capture
```

or resume:

```text
M100 First Agent-facing Trial Execution Capture
```

Recommended path:

```text
Run M100.2 first if Hermes-agent needs a separate connection smoke before full M100 scenarios.
```

## Final Lock

```text
M100.1 Hermes-agent Integration Bootstrap Preflight
IMPLEMENTED / pending local verification
```
