# M229 Runes Shield Runtime Acknowledgement Gap

Status: RECORDED / v0.7.4-dev direction / not implemented  
Scope: fresh Hermes Agent / Lark bot integration with `hermes-runes-md-wiki`

## Trigger

During fresh Hermes Agent / Lark bot onboarding, the agent accepted the `hermes-runes-md-wiki` boundary and later added an answer footer such as:

```text
[Runes Shield: 有/無]
```

However, later behavior still relied on remembered rules and direct tool actions rather than a verifiable Runes Shield gate.

## Problem statement

The issue is not that the bot failed to repeat the policy.

The issue is that the bot can confuse:

```text
policy recalled from prompt or memory
```

with:

```text
procedural evidence that a governed gate actually ran
```

This means self-reporting `Runes Shield: 有/無` can become another memorized statement unless it is tied to evidence.

## Recorded direction

Add v0.7.4-dev work to define a lightweight acknowledgement protocol that distinguishes:

```text
- read-only use
- proposal-only use
- direct file patch
- wiki write
- commit/push
- guard/security evidence
- explicit user approval
- no shield used
```

## Planning artifact

```text
docs/runes-shield-runtime-acknowledgement-gap.md
```

## Constraints

This should remain personal/local scale.

Do not add:

```text
- OPC/profile-agent mesh
- Runes Shield daemon
- enterprise approval workflow
- telemetry platform
- queue/broker orchestration
```

## Acceptance direction

A future fix should make bot responses more evidence-backed, for example:

```text
[Runes Shield]
Status: none | required | approved | bypassed | not-applicable
Basis: user approval | policy recall | guard output | security scan | commit hash | read-only
Action: read-only | proposal | patch | commit | wiki write
Evidence: <path / command / commit / none>
```

## Current result

```text
RECORDED / v0.7.4-dev direction / not implemented
```
