# M30.3c Personal-use & Perceived Latency Observation Policy

Status: M30.3c POLICY / PERSONAL-USE OBSERVATION / NO RUNTIME CHANGE
Milestone: M30.3c Personal-use & Perceived Latency Observation Policy
Chinese: M30.3c 個人使用與感知延遲觀察政策
Runes Narrative Concept: Runes Aura Sense / 符文靈氣感知

## Purpose

M30.3c defines how Hermes Runes MD Wiki should think about latency during P0/P1 trial runs.

This is a personal memory project, not an enterprise-grade RAG platform.

Therefore, latency observation must stay lightweight, local, and useful for future decisions without adding unnecessary architecture burden.

## Core Principle

```text
Keep the system simple and durable.
Observe perceived latency only when it helps future P2/P3 decisions.
Do not replace Python, add daemons, add metrics databases, or add observe indexes for small theoretical gains.
```

Chinese summary:

```text
先求簡單耐用。
只觀察個人使用時感受到的等待點。
不要為了理論上快一點而增加架構複雜度。
```

## Scope

This policy applies to:

- Hermes-agent calling Runes Shield tools
- local operator use of `bin/runes`
- governed memory proposal / attunement / promotion / apply / refresh / recall verification
- P0/P1 trial-run evidence gathering
- future P2/P3 optimization decisions

This policy does not require any immediate code change.

## Non-goals

M30.3c does not introduce:

- Go rewrite
- Rust rewrite
- daemon service
- OpenTelemetry
- Prometheus
- metrics database
- observe index
- enterprise tracing
- per-token timing
- automatic optimization
- full prompt logging
- full answer logging
- full memory context logging

## Python Runtime Policy

Python remains the default implementation for P0/P1.

Reason:

```text
The current project is still evolving quickly.
Python maximizes implementation flexibility and maintainability.
Most perceived latency may come from subprocess chains, retrieval, importer refresh, LLM calls, disk I/O, or cold starts rather than Python bytecode execution itself.
```

M30 must not rewrite components to Go/Rust based only on language-level assumptions.

Future runtime replacement is only considered in P2/P3 if observation evidence shows repeated, user-visible, meaningful delay.

## Perceived Latency over Benchmark Latency

This project optimizes for:

```text
personal-use perceived latency
```

not:

```text
enterprise throughput
synthetic microbenchmark wins
theoretical runtime speed
single-digit millisecond improvements
```

Examples of meaningful perceived latency:

- user repeatedly feels Hermes-agent is waiting too long
- governed memory action blocks interaction for several seconds
- recall verification repeatedly feels slow
- importer refresh creates a visible pause
- subprocess chains create repeated avoidable delay

Examples of low-value optimization:

- replacing Python to save a few milliseconds
- adding a daemon for rare commands
- adding metrics storage for unused dashboards
- optimizing a non-hot path by less than 10 percent while adding complexity

## Runes Aura Sense / 符文靈氣感知

The Runes Shield narrative concept for perceived latency is:

```text
Runes Aura Sense / 符文靈氣感知
```

Meaning:

```text
The system senses whether the Runes operating aura feels stable, thin, disturbed, or recovered during governed memory actions.
```

This replaces engineering-style wording like `lag sense` in the narrative layer.

Runes Aura Sense is a user-facing metaphor, not a requirement for heavy observability.

## Canonical Aura Phrases

Allowed ritual phrases:

```text
Runes Aura Stable / 符文靈氣穩定
Runes Aura Thin / 符文靈氣稀薄
Runes Aura Disturbed / 符文靈氣紊亂
Runes Aura Recovered / 符文靈氣恢復
```

Usage examples:

```text
Runes Aura Stable / 符文靈氣穩定。
The governed memory action completed within the expected interaction window.
```

```text
Runes Aura Thin / 符文靈氣稀薄。
The action completed, but the user-visible wait was longer than expected.
No memory mutation failed.
```

```text
Runes Aura Disturbed / 符文靈氣紊亂。
The action experienced repeated delay or failure in a user-visible stage.
No automatic runtime replacement should be performed without review.
```

```text
Runes Aura Recovered / 符文靈氣恢復。
The previously observed delay condition was not reproduced after follow-up verification.
```

## Lightweight Observation Policy

If latency observation is implemented during trial run, it should be:

```text
local JSONL
append-only
best-effort
non-blocking
not ingested into RAG
not stored in DB
not used for automatic tuning
safe to disable
safe to fail
```

Observation failure must never break:

- answer generation
- trusted wiki write
- recall verification
- importer refresh
- rollback behavior

## Minimal Useful Fields

If implemented, P0/P1 latency observation should start with only coarse fields:

```text
timestamp
operation
entrypoint
stage
status
duration_ms
failure_reason_if_any
```

Optional only if already cheap to collect:

```text
subprocess_count
refresh_duration_ms
recall_duration_ms
apply_duration_ms
llm_duration_ms
```

Do not collect by default:

```text
raw prompt
raw answer
full memory context
full retrieved chunks
secrets
environment variables
per-token timing
trace span tree
```

## Optimization Threshold

Do not introduce new runtime architecture for small theoretical gains.

Future optimization should usually require all of these:

```text
user-visible delay
repeated occurrence
clear stage attribution
meaningful improvement potential
low added complexity
preserved durability
```

Rule of thumb:

```text
A less-than-10-percent improvement is usually not worth added runtime architecture complexity unless it removes a clearly painful repeated wait.
```

## Preferred Future Optimization Order

If P2/P3 evidence shows meaningful perceived latency issues, prefer this order:

```text
1. Remove unnecessary subprocess chains.
2. Cache cheap local state safely.
3. Reuse DB connections when practical.
4. Reduce duplicate importer/recall work.
5. Add an optional lightweight local daemon only if repeated delay justifies it.
6. Rewrite a proven hot path in Go/Rust only if evidence justifies the complexity.
```

Do not start with language replacement.

## Entrypoint Design Implication

M30.4 should keep entrypoints implementation-neutral.

That means:

```text
Hermes-agent and users should depend on stable command/API behavior, not on whether the implementation is Python CLI, Python daemon, Go helper, or Rust helper.
```

However, P0/P1 implementation remains Python by default.

## Relationship to Existing Observation Philosophy

This policy aligns with earlier observation goals:

- local-only evidence
- lightweight JSONL when needed
- no raw/full prompt by default
- no raw/full answer by default
- no full memory context by default
- observation logs are not ingested into RAG
- cleanup/logging failures should not break answers
- observe first, tune later

M30.3c narrows that philosophy specifically to perceived latency.

## M30.3c Does Not Authorize

M30.3c does not authorize:

- immediate latency logging implementation
- new daemon
- new database table
- new index
- runtime rewrite
- broad tracing framework
- automatic optimizer
- CLI behavior change

Implementation, if needed, should be planned later and kept personal-use scale.

## Verification Status

M30.3c Personal-use & Perceived Latency Observation Policy:

- personal-use scope defined: PASS
- perceived latency priority defined: PASS
- Python P0/P1 default preserved: PASS
- no Go/Rust assumption policy defined: PASS
- Runes Aura Sense narrative concept defined: PASS
- lightweight observation boundary defined: PASS
- minimal useful fields defined: PASS
- no enterprise observability boundary defined: PASS
- optimization threshold defined: PASS
- M30.4 entrypoint implication defined: PASS
- no-runtime-change boundary preserved: PASS

Overall:

M30.3c Personal-use & Perceived Latency Observation Policy:
PASS / perceived latency policy defined / no runtime change performed
