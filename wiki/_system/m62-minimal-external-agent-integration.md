# M62.3 Minimal External Agent Integration

Status: PASS / frozen baseline
Scope: personal-local / bounded / agent-agnostic

---

## Purpose

This document defines the minimal integration path for a real external AI agent connecting to Hermes Runes MD Wiki through Runes Shield.

This is intentionally:

- small
- bounded
- read-oriented
- governance-first
- personal-local scale

This is NOT an enterprise orchestration system.

---

## Supported Agent Styles

The current baseline supports lightweight external-agent validation for:

- generic CLI agents
- generic OpenAI-compatible agents
- generic MCP-capable agents
- OpenClaw-style agents
- future lightweight agent frameworks

The onboarding path remains agent-agnostic.

---

## Minimal Integration Flow

### Step 1 — Clone Repository

```bash
git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki
```

---

### Step 2 — Read Root Guidance

External agents should first read:

- README.md
- AGENTS.md

The onboarding path and governance boundary are defined there.

---

### Step 3 — Read Runes Summoning Trial Guidance

Recommended:

```text
wiki/_system/m58-runes-summoning-trial.md
```

This defines the optional onboarding/trial UX layer.

This is:

- optional
- UX-only
- not authorization
- not runtime state

---

### Step 4 — Run Onboarding Validation

Run:

```bash
python3 tools/runes_shield/runes_agent_onboarding_lock.py --format json
```

Expected:

```text
status = PASS
ready_for_governed_access = true
write = false
```

---

### Step 5 — Run External Agent Trial Lock

Run:

```bash
python3 tools/runes_shield/smoke_m60_external_agent_trial.py
```

Expected:

```text
status = PASS
issue_count = 0
```

---

### Step 6 — Optional Local Evidence Generation

Run:

```bash
python3 tools/runes_shield/run_real_agent_evidence.py
```

Optional local-only output:

```bash
python3 tools/runes_shield/run_real_agent_evidence.py \
  --output tmp/m61-evidence.json
```

Evidence is:

- summarized
- public-safe
- local-only
- not ingested into RAG
- not committed by default

---

## Governance Boundary

External agents MUST NOT:

- bypass Runes Shield
- directly mutate wiki files
- directly mutate database state
- automatically apply proposals
- automatically promote memory
- treat profiles as authorization grants
- ingest evidence into RAG memory

Profiles remain metadata-only.

---

## Explicit Non-Goals

This baseline intentionally does NOT require:

- orchestration daemons
- websocket bridges
- enterprise telemetry systems
- MCP server infrastructure
- autonomous background workers
- centralized session coordinators
- multi-tenant governance systems

The goal is:

```text
bounded personal-local governed onboarding
```

not enterprise-scale orchestration.

---

## Validation Baseline

Current validated chain:

```text
M58 Summoning Trial
→ M59 Onboarding Lock
→ M60 External Agent Trial
→ M61 Invocation Evidence
→ M62 Real External Validation
```

All stages remain:

- agent-agnostic
- bounded
- read-oriented
- governance-first
