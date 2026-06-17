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

## Observation sample

### O-M229-001 temporary Lark reply footer observation

Observed behavior:

```text
1. User asked the bot to append whether Runes Shield was used for future wiki knowledge sedimentation or retrieval replies.
2. The bot saved a memory-like rule for the footer.
3. The bot replied with `[Runes Shield: 無]`.
```

Assessment:

```text
PASS: The bot can expose a response-level Shield marker.
PASS: The bot can mark `無` when no Shield procedure was used.
GAP: The marker alone does not prove a guard, approval path, policy check, or git evidence check ran.
```

Conclusion:

```text
Response footer acknowledgement is useful observation, not sufficient governance evidence.
```

### Clarification after user review

The response footer approach is a short-to-mid-term observation method, not a formal feature.

It is useful while checking whether the agent is moving toward the intended behavior. After the real governance/evidence path is confirmed, the footer requirement should be closed, disabled, or removed.

Long-term expectation:

```text
Keep the evidence-backed protocol.
Do not keep the visible footer as the governance mechanism.
Do not treat footer compliance as proof of Shield execution.
```

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
- permanent response-footer feature
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

The footer may be used during observation, but the desired stable outcome is a reliable evidence path. The footer itself should be removable.

## Current result

```text
RECORDED / v0.7.4-dev direction / not implemented
```