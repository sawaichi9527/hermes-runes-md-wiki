# Runes Shield Runtime Acknowledgement Gap

Status: PLANNED / v0.7.4-dev direction  
Scope: Hermes Agent / Lark bot onboarding behavior for `hermes-runes-md-wiki`

## Problem

A freshly onboarded Hermes Agent / Lark bot may verbally acknowledge the `hermes-runes-md-wiki` boundary, but later operate from memorized or prompted rules instead of a verifiable Runes Shield procedure.

Observed behavior:

```text
1. Agent says it has accepted the Runes Wiki / Shield operating boundary.
2. Agent later edits or plans edits by direct file/tool action.
3. Agent self-reports whether Runes Shield was used.
4. The self-report is based on recalled instructions, not a verifiable gate/evidence state.
```

This creates a governance gap:

```text
Prompt compliance != Shield execution evidence
Answer footer != procedural proof
Memory rule != durable governance gate
```

## Why this matters

The active mainline relies on a single main agent, bounded native subagents, lightweight Kanban checkpointing, governed Markdown memory, and Git history.

That model is intentionally simple, but it still needs a minimal way to distinguish:

```text
- policy recalled from memory
- user approval observed in conversation
- migration guard / security scan run
- Runes Shield or equivalent approval path actually used
- direct tool edit without a shield gate
```

Without this distinction, a Lark bot can appear aligned while still bypassing the intended governance path.

## v0.7.4-dev direction

M229 should define a lightweight Runes Shield acknowledgement protocol for fresh Hermes Agent / Lark bot sessions.

The goal is not to build a heavy runtime daemon or enterprise workflow system.

The goal is a small, checkable convention that makes the following visible:

```text
Runes Shield: yes/no/unknown
Evidence: user approval / guard output / security scan / commit hash / none
Action type: read-only / proposal / patch / wiki write / commit
Writable scope: wiki-owned / system docs / dev history / non-wiki repo file
```

## Candidate output footer

For responses involving wiki knowledge, retrieval, edits, or policy-sensitive actions, the bot should include a compact footer similar to:

```text
[Runes Shield]
Status: none | required | approved | bypassed | not-applicable
Basis: user approval | policy recall | guard output | security scan | commit hash | read-only
Action: read-only | proposal | patch | commit | wiki write
Evidence: <path / command / commit / none>
```

Important distinction:

```text
[Runes Shield: none]
```

is not failure by itself for read-only or metadata-only answers.

But for wiki writes or governed knowledge changes, `none` or `bypassed` must stop the action or require explicit human confirmation.

## Minimal expected behavior

Before touching `wiki/**/*.md`, the agent should identify:

```text
- target path
- whether the path is user-owned Markdown
- whether the action is read-only, proposal-only, or a durable write
- whether explicit user approval exists
- whether guard/security evidence exists
```

For non-wiki repo files, direct patch may be acceptable when the user explicitly asked for repo maintenance, but the bot should still state that no Runes Shield was used if no shield-like gate was executed.

## Non-goals

Do not add:

```text
- OPC/profile-agent mesh
- A2A runtime enforcement
- separate Runes Shield daemon
- enterprise approval workflow
- telemetry platform
- queue/broker-based orchestration
```

## Desired end state

A freshly installed Hermes Agent / Lark bot should not merely say it has accepted `hermes-runes-md-wiki` policy.

It should be able to show, for each sensitive action, whether it used a real gate, merely recalled a rule, or performed a direct action.
