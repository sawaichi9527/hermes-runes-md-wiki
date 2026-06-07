# Decisions — K6 / Freelancer Hermes Agent

Host: K6 / Freelancer  
User: eye  
Memory workspace: `~/workspace/hermes-memory/`  
Project wiki: `~/workspace/hermes-memory/wiki/k6-freelancer/`

---

## Purpose

This file records durable architectural decisions for the K6 / Freelancer Hermes Agent setup.

It should capture:

```text
What was decided
Why it was decided
What was deferred
What should not be changed casually
```

This file is part of the Phase3-M1 Markdown source-of-truth and will later be indexed by PostgreSQL FTS / pgvector.

---

## Decision Index

```text
D-001: Use local Docker SearXNG as Hermes web_search backend
D-002: Use Tavily as Hermes web_extract backend
D-003: Disable DuckDuckGo and Brave in SearXNG
D-004: Keep SearXNG localhost-only
D-005: Defer Valkey / limiter until A2
D-006: Defer UFW while remote-access safety is not confirmed
D-007: Use ~/workspace/hermes-memory/ as Markdown memory source-of-truth
D-008: Keep Markdown wiki separate from ~/.hermes runtime state
D-009: Use PostgreSQL + FTS + pgvector as long-term K6 memory/RAG backend
D-010: Keep PostgreSQL service stack under ~/docker-stacks/hermes-memory-postgres/
D-011: Treat Markdown as source-of-truth and PostgreSQL as index/query backend
D-012: Do not store secrets in the memory wiki
D-013: Keep MemPalace as future optional sidecar memory, not primary source-of-truth
```

---

## D-001: Use local Docker SearXNG as Hermes web_search backend

Decision:

```text
Use Dockerized SearXNG as the local web_search backend for Hermes Agent.
```

Final configuration:

```yaml
web:
  backend: ''
  search_backend: searxng
  extract_backend: tavily
```

Environment:

```env
SEARXNG_URL=http://127.0.0.1:8088
```

Rationale:

```text
SearXNG provides a free, self-hosted, local web search path.
Hermes can search the web without relying on browser automation.
The service is easy to run as a small Docker stack.
The service can be verified independently with curl and tcpdump.
```

Verification status:

```text
PASS
```

Verified by:

```text
curl JSON search
Hermes web_search response
tcpdump on lo tcp port 8088
```

---

## D-002: Use Tavily as Hermes web_extract backend

Decision:

```text
Use Tavily as the Hermes web_extract backend.
```

Final configuration:

```yaml
web:
  search_backend: searxng
  extract_backend: tavily
```

Rationale:

```text
SearXNG is search-only.
Hermes needs a separate extract backend to read full page content.
The user already has Tavily API access.
Tavily can serve as the C1 external extract provider.
```

Verification status:

```text
PASS
```

Verified by Hermes trace:

```text
web_search ran first.
web_extract ran second.
Hermes fetched documentation.ubuntu.com and summarized the page.
browser fallback was not observed.
```

Known note:

```text
One web_extract run against documentation.ubuntu.com took about 223.2 seconds.
Functional output was successful, but extract latency should be monitored.
```

---

## D-003: Disable DuckDuckGo and Brave in SearXNG

Decision:

```text
Disable DuckDuckGo and Brave engines in SearXNG.
```

Configuration:

```yaml
engines:
  - name: duckduckgo
    disabled: true

  - name: brave
    disabled: true
```

Rationale:

```text
DuckDuckGo triggered CAPTCHA during automated use.
Brave triggered Too Many Requests.
These errors caused Hermes to attempt browser-based fallback search.
Browser fallback to DuckDuckGo previously stalled during automation.
```

Goal:

```text
Keep A1 SearXNG search stable and avoid browser fallback.
```

Verification status:

```text
PASS
```

---

## D-004: Keep SearXNG localhost-only

Decision:

```text
Bind SearXNG only to 127.0.0.1 on the host.
```

Docker binding:

```text
127.0.0.1:8088->8080/tcp
```

Rationale:

```text
Hermes runs natively on the same host.
No LAN exposure is needed for A1.
Localhost-only binding reduces attack surface.
```

Important distinction:

```text
Inside the container, SearXNG listens on 0.0.0.0:8080.
On the host, Docker publishes it only to 127.0.0.1:8088.
```

Verification status:

```text
PASS
```

Verified by:

```bash
docker compose ps
ss -tulpn | grep 8088
```

---

## D-005: Defer Valkey / limiter until A2

Decision:

```text
Do not enable Valkey / Redis / limiter for A1.
```

Rationale:

```text
Current deployment is single-host.
SearXNG is localhost-only.
Expected query volume is low.
No LAN or public exposure exists.
Adding Valkey now would increase complexity without solving a current issue.
```

Trigger conditions for A2:

```text
Multiple agents using SearXNG
LAN exposure
Public exposure
Frequent CAPTCHA or rate-limit pressure
Need for bot protection
Need for formal rate limiting
```

Status:

```text
Deferred
```

---

## D-006: Defer UFW while remote-access safety is not confirmed

Decision:

```text
Do not enable or modify UFW during current remote operation.
```

Rationale:

```text
The user operates the machine remotely, including via AnyDesk.
Firewall mistakes may lock out remote access.
Firewall work should wait until physical access or a verified recovery path exists.
```

Status:

```text
Deferred
```

Future requirement:

```text
Confirm SSH / AnyDesk allow rules before enabling UFW.
Have physical or out-of-band access available.
```

---

## D-007: Use ~/workspace/hermes-memory/ as Markdown memory source-of-truth

Decision:

```text
Use ~/workspace/hermes-memory/ for Phase3-M1 Markdown wiki source-of-truth.
```

Rationale:

```text
This is a human-managed project memory workspace.
It should be easy to inspect, edit, back up, and optionally Git version.
It should not clutter the home directory root.
It should not be hidden inside ~/.hermes runtime state.
```

Final path:

```text
~/workspace/hermes-memory/
```

Status:

```text
Accepted
```

---

## D-008: Keep Markdown wiki separate from ~/.hermes runtime state

Decision:

```text
Do not use ~/.hermes/memories/ as the primary Phase3 Markdown wiki location.
```

Rationale:

```text
~/.hermes belongs to Hermes internal configuration and runtime state.
Hermes upgrades may change internal directory semantics.
Curated project memory should remain independent from Hermes internals.
```

Relationship:

```text
~/.hermes/
  Hermes runtime and configuration

~/workspace/hermes-memory/
  Human/Hermes curated project memory source-of-truth
```

Status:

```text
Accepted
```

---

## D-009: Use PostgreSQL + FTS + pgvector as long-term K6 memory/RAG backend

Decision:

```text
Use PostgreSQL + FTS + pgvector as the long-term K6 local memory/RAG backend.
```

Rationale:

```text
K6 has enough CPU, memory, and storage resources.
PostgreSQL is better suited than SQLite for long-term service-style memory infrastructure.
PostgreSQL supports metadata, joins, full-text search, backup, extensions, and pgvector.
PostgreSQL can become a shared backend for Hermes recall, future tools, and possible sidecar memory systems.
```

Phase plan:

```text
M1: Markdown wiki source-of-truth
M1b: PostgreSQL FTS index
M2: pgvector semantic search
M3: hybrid search / rerank
```

Status:

```text
Accepted
```

---

## D-010: Keep PostgreSQL service stack under ~/docker-stacks/hermes-memory-postgres/

Decision:

```text
Place the PostgreSQL memory backend service stack under ~/docker-stacks/hermes-memory-postgres/.
```

Rationale:

```text
PostgreSQL is a long-running service.
It has a different lifecycle from Markdown source files.
It needs Docker compose, init scripts, backup scripts, and health checks.
It should not be mixed with the Markdown source-of-truth workspace.
```

Planned path:

```text
~/docker-stacks/hermes-memory-postgres/
```

Planned layout:

```text
~/docker-stacks/hermes-memory-postgres/
  ├─ compose.yaml
  ├─ .env
  ├─ init/
  ├─ scripts/
  ├─ backup/
  ├─ check.sh
  └─ README.md
```

Status:

```text
Accepted
```

---

## D-011: Treat Markdown as source-of-truth and PostgreSQL as index/query backend

Decision:

```text
Markdown files are canonical.
PostgreSQL is an index and query backend.
```

Rationale:

```text
Markdown is human-readable and easy to repair.
PostgreSQL indexes can be rebuilt from Markdown.
Embeddings and vector indexes are derived artifacts.
This avoids vendor lock-in and reduces risk of memory corruption.
```

Data flow:

```text
~/workspace/hermes-memory/wiki/
  ↓ ingest / sync
PostgreSQL hermes_memory database
  ↓ FTS / pgvector / hybrid search
Hermes recall / RAG
```

Status:

```text
Accepted
```

---

## D-012: Do not store secrets in the memory wiki

Decision:

```text
Do not store API keys, tokens, passwords, or private credentials in the Markdown memory wiki.
```

Forbidden:

```text
TAVILY_API_KEY value
Telegram bot token
LM Studio API key if any
OpenAI / OpenRouter / xAI / Gemini keys
SSH private keys
OAuth tokens
Passwords
Secret-bearing logs
```

Allowed redacted form:

```env
TAVILY_API_KEY=<configured>
SEARXNG_URL=http://127.0.0.1:8088
```

Rationale:

```text
The memory wiki may later be indexed, backed up, copied, or Git versioned.
Secrets must stay in runtime configuration files such as ~/.hermes/.env.
```

Status:

```text
Accepted
```

---

## D-013: Keep MemPalace as future optional sidecar memory, not primary source-of-truth

Decision:

```text
MemPalace may be evaluated later as a sidecar episodic memory system.
It should not replace the Markdown source-of-truth.
```

Rationale:

```text
MemPalace is useful for verbatim or episodic memory.
The Phase3-M1 Markdown wiki is curated project memory.
These roles are complementary but should remain separate.
```

Recommended relationship:

```text
Phase3-M1 Markdown wiki:
  curated, canonical, durable project facts

MemPalace:
  optional future sidecar for episodic/verbatim recall
```

Status:

```text
Deferred / research candidate
```

---

## Current Decision Summary

Accepted:

```text
Use SearXNG for web_search.
Use Tavily for web_extract.
Use Markdown under ~/workspace/hermes-memory/ as source-of-truth.
Use PostgreSQL + FTS + pgvector as K6 long-term memory/RAG backend.
Keep Docker services under ~/docker-stacks/.
Keep secrets out of memory files.
```

Deferred:

```text
A2 Valkey / limiter
UFW
MemPalace integration
Firecrawl / Exa backup provider
pgvector M2
hybrid search M3
Docker sandbox
```

## D-20260531-M8.4 Multi-model Governance Baseline

Status: BASELINE

Decision:
- Introduce model-profile governance before further sanitizer / extraction policy tuning.
- Sanitizer and answer extraction should become model-aware instead of relying on global hardcode heuristics.
- Initial baseline profiles:
  - qwen-forced-thinking
  - gemma-clean-structured
  - llama-instruction-following
  - default

Rationale:
- Different model families expose different behavior around reasoning leakage, final-answer placement, and structured-output stability.
- Qwen-family tuned models may place useful answer text inside reasoning_content, so extraction fallback must be controlled by profile.
- Cleaner instruction-following models should not use reasoning_content fallback by default.
- This keeps M8.3 observation logging useful while avoiding automatic heuristic changes.

Config:
- config/model_profiles.yaml

Policy:
- Real secrets remain prohibited from Markdown memory and git.
- Observation logs must not be ingested into RAG memory.
- Model profile behavior should be observed first, tuned later.

Next:
- M8.4.3 load model_profiles.yaml from answer_generator.
- M8.4.4 apply profile-aware extraction policy.
- M8.4.5 add observation log fields for selected profile and extraction path.

---

## D-20260531-M8.5 Local Personal RAG Scope Boundary

Status: DECIDED

Decision:
- M8.5 should follow mature production RAG principles, but remain scoped for a local personal RAG system.
- Hermes Memory should not become a commercial multi-user / multi-tenant RAG platform.
- Use industry patterns selectively:
  - model-aware behavior profile
  - extraction quality validation
  - minimal retry / repair path
  - lightweight observability
  - smoke-test based evaluation
- Avoid enterprise-grade complexity unless future requirements clearly justify it.

Rationale:
- Hermes Memory currently runs as a local personal RAG system for K6/Freelancer usage.
- The main goal is answer reliability and maintainability, not SaaS scalability.
- Commercial production RAG patterns are useful as references, but should be adapted into small local modules.
- Overbuilding routing, tracing, dashboards, distributed queues, or multi-user policy systems would increase maintenance cost without matching current needs.

Accepted local design principles:
1. Prefer understandable local code over framework-heavy abstraction.
2. Prefer small single-purpose Python modules over large guardrail/routing platforms.
3. Prefer JSON output metadata / optional local JSONL observation over tracing backends.
4. Prefer smoke tests over full evaluation dashboards.
5. Prefer profile-aware rules over global hardcode heuristics.
6. Prefer observation-first tuning; do not auto-modify heuristics from logs.
7. Do not ingest observation logs into RAG memory.
8. Do not store raw prompts, full answers, full retrieved context, or real secrets in observation logs.
9. Keep `.env` and local secret files as the only place for real credentials.
10. Avoid GitHub/project packaging complexity until the final project stage.

Explicitly out of scope for current local baseline:
- Multi-tenant user isolation.
- Commercial routing platform.
- Dynamic provider scoring.
- Model A/B testing platform.
- OpenTelemetry / LangSmith-style tracing backend.
- Web dashboard.
- Distributed queue or worker architecture.
- Database-backed observation/event warehouse.
- Automatic heuristic tuning.
- Multi-user role/policy management.
- Full fallback model chain unless later proven necessary.

Implication for M8.5:
- M8.5 should be named and implemented as local extraction hardening, not an enterprise governance platform.
- The first step should be a small `extraction_quality.py` checker.
- Retry behavior, if added, should be conservative, local, and at most single retry by default.
- The system should remain easy to read, inspect, and maintain from the local filesystem.

---
