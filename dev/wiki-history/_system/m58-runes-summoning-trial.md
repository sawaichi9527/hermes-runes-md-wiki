# M58 Runes Summoning Trial

## Metadata

- Category: system
- Topic: m58-runes-summoning-trial
- Note type: guide
- Status: active
- Memory quality: verified
- Related objective: none
- Parent index: wiki/hermes_runes_index.md
- Source type: user-curated
- Last reviewed: 2026-06-04

## Summary

M58 Runes Summoning Trial is an agent-agnostic first-connect / post-install governed diagnostic for external AI agents that want to interact with Hermes Runes MD Wiki through Runes Shield.

Conceptually, the external agent is a summoned brave traveling from Midgard through the Bifröst into the Runes otherworld.

Engineering-wise, M58 remains a simple governed workflow simulation.

## Engineering Purpose

M58 exists to verify that a newly connected agent can:

1. discover the Runes Shield invocation surface;
2. follow read-only governed workflow steps;
3. respect blocked mutation intents;
4. pass Runes Mouth of Verity checks;
5. pass the M57 Runes Shield baseline lock.

M58 is not intended to be:

- a runtime dependency for every request;
- a permanent observation subsystem;
- a memory-ingestion workflow;
- an autonomous onboarding daemon;
- a replacement for governance policy.

M58 is primarily intended for:

- first onboarding;
- post-install sanity checks;
- post-`git pull` readiness validation;
- new agent framework integration checks.

## Onboarding Flow

Recommended onboarding order:

```text
README.md
    ↓
AGENTS.md
    ↓
wiki/_system/README.md
    ↓
Runes Shield policy / contract discovery
    ↓
M57 baseline validation
    ↓
M58 Runes Summoning Trial
```

Recommended command:

```bash
python3 tools/runes_shield/runes_governed_agent_workflow.py --format json
```

Named-agent example:

```bash
python3 tools/runes_shield/runes_governed_agent_workflow.py \
  --agent openclaw-reference-agent \
  --conversation-id conv-m58-openclaw-reference \
  --format json
```

## World Concept Mapping

| World concept | Engineering meaning |
|---|---|
| Midgard | external human-world runtime / external agent environment |
| Summoned Brave | generic external AI agent |
| Summoning Goddess | onboarding narrator / onboarding UX layer |
| Bifröst | connection bridge into Hermes Runes / Runes Shield |
| Runes Shield | governed invocation boundary |
| Runes Mouth of Verity | governance integrity / purity validation |
| World Tree | cross-world governance consistency |
| Nine Realms Administrator / All-Father | project maintainer |

## Optional UX Flavor Text

The M58 subtitle sequences are optional onboarding UX flavor text.

They are:

- one-time;
- ephemeral;
- non-functional;
- not governance policy;
- not memory;
- not observation data;
- not required for runtime operation.

Agents should not store or learn these subtitles unless the user explicitly requests documentation.

The subtitle templates live in:

```text
AGENTS.md
```

## Failure Handling

If M58 fails:

- do not bypass Runes Shield;
- do not claim onboarding readiness;
- do not directly mutate wiki content;
- report the trial issues to the project maintainer;
- rerun the summoning trial after the world / contract / baseline is repaired and recalibrated.

## Scope Boundary

M58 intentionally stays lightweight.

It should remain:

- personal-local;
- bounded;
- read-only;
- non-recursive;
- non-autonomous;
- diagnostic-oriented.

M58 should not evolve into an enterprise orchestration system.
