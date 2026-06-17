# Runes Shield Response Footer Observation Boundary

Status: PLANNED / v0.7.4-dev M229 clarification  
Scope: temporary Hermes Agent / Lark bot reply observability

## Decision

The visible `[Runes Shield: 有/無]` reply footer is a short-to-mid-term observation aid only.

It should help observe whether the agent is following the intended Runes Shield boundary while M229 is still being designed.

It should not become the long-term feature, the approval gate, or the governance mechanism.

## Expected lifecycle

```text
1. Use the footer during temporary observation.
2. Compare it against actual evidence such as user approval, guard output, security scan output, policy references, and git commits.
3. Once the real evidence path is reliable, disable or remove the visible footer requirement.
4. Keep the evidence-backed protocol, not the footer convention.
```

## Interpretation

```text
Footer present: useful visibility signal.
Footer absent: acceptable after observation is closed.
Footer says no Shield: useful warning, not complete evidence.
Footer says Shield used: not enough unless backed by evidence.
```

## M229 rule

M229 should solve the evidence gap. It should not turn the reply footer into a permanent user-facing feature.
