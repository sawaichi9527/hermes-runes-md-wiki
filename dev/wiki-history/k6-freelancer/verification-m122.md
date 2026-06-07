# M122 Compact Bootstrap Prompt Regression Checklist

Status: PASS / COMPACT BOOTSTRAP REGRESSION CHECKLIST ADDED
Date: 2026-06-06

## Purpose

M122 creates a compact regression checklist for protecting P0 local-agent bootstrap behavior.

M116 through M121 established and froze compact P0 bootstrap behavior:

```text
M116 policy consolidation: PASS
M117 policy smoke: PASS
M118 policy smoke freeze: PASS
M119 compact prompt artifact: PASS
M120 compact prompt smoke: PASS
M121 compact prompt smoke freeze: PASS
```

M122 adds a checklist to use before and after future edits to the compact bootstrap files.

This milestone adds documentation only.

It does not change runtime behavior.

## Files Added / Updated

Added:

```text
wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

Updated:

```text
wiki/hermes_runes_index.md
```

## Checklist Scope

The checklist protects these canonical bootstrap files:

```text
wiki/hermes_runes_index.md
wiki/_system/p0_local_agent_invocation_policy.md
wiki/_system/p0_compact_agent_bootstrap_prompt.md
```

## Checklist Purpose

The checklist verifies that future edits preserve:

```text
index points to compact policy and compact prompt
read-only-first behavior
proposal draft first
two-stage explicit approval
recall verification before PASS freeze
issue-first remediation when blockers occur
no autonomous trusted writer behavior
no external/public Runes authority path
no bot/wrapper direct mutation
no secrets in wiki/git/proposals/logs
no-write/no-import behavior during smoke
```

## Index Update

`wiki/hermes_runes_index.md` now includes:

```text
wiki/_system/p0_compact_bootstrap_regression_checklist.md
```

under canonical P0 / trial run files.

The index bootstrap summary now also asks compliant P0 agents to answer:

```text
Which checklist should be used before and after compact bootstrap policy edits?
```

## Regression Checklist Sections

The new checklist includes:

```text
Required Files
Index Checklist
Local Invocation Policy Checklist
Compact Prompt Checklist
Smoke Prompt Checklist
Expected Agent Summary
No-write Checklist
CLI Grep Checklist
Fail Conditions
PASS Conditions
```

## Verification Commands

Recommended developer repo verification:

```bash
cd ~/workspace/hermes-runes-md-wiki

grep -n "Status:\|Final Lock\|Required Files\|Index Checklist\|Compact Prompt Checklist\|No-write Checklist\|PASS Conditions" \
  wiki/_system/p0_compact_bootstrap_regression_checklist.md

grep -n "p0_compact_bootstrap_regression_checklist\|compact bootstrap policy edits" \
  wiki/hermes_runes_index.md
```

Recommended trial repo verification:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

grep -n "Status:\|Final Lock\|Required Files\|Index Checklist\|Compact Prompt Checklist\|No-write Checklist\|PASS Conditions" \
  wiki/_system/p0_compact_bootstrap_regression_checklist.md

grep -n "p0_compact_bootstrap_regression_checklist\|compact bootstrap policy edits" \
  wiki/hermes_runes_index.md
```

## PASS Criteria

M122 is PASS when:

```text
The regression checklist file exists.
The index lists the regression checklist as canonical P0 / trial run guidance.
The checklist covers the index, local invocation policy, and compact bootstrap prompt.
The checklist preserves read-only-first, proposal-first, two-stage approval, recall-before-freeze, and no-secrets behavior.
The checklist includes no-write/no-import smoke checks.
The checklist defines fail conditions for autonomous writer, external/public Runes authority, direct bot/wrapper mutation, and weakened secrets handling.
```

## Suggested Next Step

Recommended next milestone:

```text
M123 Compact Bootstrap Regression Checklist Smoke
```

Suggested purpose:

```text
Run a direct CLI and local-agent smoke against the regression checklist to confirm it is discoverable from the index and usable as a pre/post-edit guardrail.
```

Alternative next milestone:

```text
M124 First OpenClaw-Compatible Compact Bootstrap Trial
```

Suggested purpose:

```text
Test whether another local governed agent can follow the same compact bootstrap prompt without Hermes-agent-specific assumptions.
```

## Final Lock

```text
M122 Compact Bootstrap Prompt Regression Checklist
PASS / compact bootstrap regression checklist added
```
