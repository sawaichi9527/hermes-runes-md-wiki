# Hermes Runes MD Wiki - Repository Boundary Policy

Status: Draft Baseline  
Phase: M11.6 Repository Readiness  
Scope: GitHub readiness, source boundary, secrets boundary, local-state policy

---

# 1. Purpose

This document defines what belongs in the Hermes Runes MD Wiki repository and what must remain local.

Hermes Runes MD Wiki is intended to become a public or shareable repository. Therefore, the repository must clearly separate:

- source code
- curated documentation
- sample configuration
- local runtime state
- private user memory
- secrets
- generated logs
- database data

The goal is to make the repository safe to publish, clone, inspect, and reuse.

---

# 2. Repository Identity

Repository name:

```text
hermes-runes-md-wiki
```

Display name:

```text
Hermes Runes MD Wiki
```

Tagline:

```text
Markdown wiki source-of-truth for governed local RAG memory.
```

Positioning:

Hermes Runes MD Wiki is an agent-agnostic Markdown wiki source-of-truth and governed local RAG memory layer.

Hermes Agent is the first target consumer, but the repository should remain reusable by OpenClaw, MCP-compatible runtimes, local automation frameworks, and future intelligent agents.

---

# 3. What Should Be Committed

The repository may contain:

- source code
- CLI tools
- importer tools
- retrieval tools
- context builder
- answer generator
- governance modules
- sanitizer modules
- retry modules
- observation summary tools
- smoke tests
- SQL schema templates
- Docker Compose templates
- documentation
- `.env.example`
- `.gitignore`
- sample Markdown wiki content
- public-safe examples
- public-safe test fixtures

---

# 4. What Must Not Be Committed

The repository must not contain:

- real `.env`
- API keys
- OpenAI-compatible API keys
- LM Studio API keys
- PostgreSQL passwords
- Telegram bot tokens
- Tavily keys
- service credentials
- private SSH keys
- access tokens
- cookies
- raw full prompts
- full chat transcripts
- full retrieved contexts
- private observation logs
- database volume data
- private user memory
- confidential work documents
- generated local runtime artifacts

---

# 5. Secrets Policy

All real secrets must remain local.

Allowed:

```text
.env.example
```

Forbidden:

```text
.env
.env.local
*.secret
*.key
*.pem
```

Environment files committed to the repository must only contain placeholders.

Example:

```bash
OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_MODEL=example-model-name
OPENAI_API_KEY=replace-with-local-secret
HERMES_MEMORY_DATABASE_URL=postgresql://user:password@localhost:5432/hermes_memory
```

The example values must not be valid production secrets.

---

# 6. Observation Log Policy

Observation logs are local runtime data.

Default location:

```text
logs/observations/
```

Observation logs may contain:

- model profile metadata
- extraction quality flags
- retry status
- citation integrity status
- short answer previews
- failure buckets
- timestamped runtime summaries

Observation logs must not contain by default:

- raw full prompt
- full answer
- full retrieved context
- secrets
- private credentials
- raw conversation transcript

Observation logs should not be committed to GitHub.

Observation logs should not be ingested back into RAG memory.

Observation is for:

```text
observe first, tune later
```

It is not for automatic self-modification.

---

# 7. Markdown Wiki Content Policy

Markdown wiki content is the curated source-of-truth layer.

The repository may contain:

- public-safe sample wiki files
- project documentation safe for publication
- architecture notes safe for publication
- baseline descriptions safe for publication
- generic templates
- policies
- examples

The repository should not contain:

- private user notes
- confidential customer data
- private operational secrets
- unreleased proprietary details
- raw logs
- private chat exports

For the current personal baseline, `wiki/k6-freelancer/` is the main curated engineering memory namespace.

Before public GitHub release, this directory must be reviewed carefully.

Options:

1. Keep only public-safe curated content.
2. Move private content to a local-only wiki.
3. Provide a sanitized sample wiki.
4. Split public templates from private memory.

---

# 8. Database Policy

PostgreSQL is a runtime backend.

The repository may contain:

- schema SQL
- migration templates
- setup scripts
- Docker Compose templates
- documentation

The repository must not contain:

- PostgreSQL data directory
- database dumps with private content
- database backups
- generated indexes
- pgvector data volumes

Database data should remain local.

Recommended local infra path:

```text
~/docker-stacks/hermes-memory-postgres/
```

This is a recommendation, not a hard requirement.

---

# 9. Docker / Infrastructure Policy

Docker Compose templates may be committed when they are generic and public-safe.

Allowed:

- compose templates
- example service names
- placeholder passwords
- documented ports
- volume examples
- healthcheck examples

Forbidden:

- real passwords
- private network credentials
- production tokens
- host-specific secrets
- local-only bind mounts containing private data

Docker service configuration should support environment override.

---

# 10. Generated Files Policy

Generated files should generally not be committed.

Examples:

- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.venv/`
- logs
- temporary JSON output
- benchmark output
- smoke output files
- local backups
- database volumes

Exceptions may be allowed for:

- small public-safe fixtures
- documented expected outputs
- example JSON files used by tests

---

# 11. Backup Policy

Local backups should not be committed by default.

Examples:

```text
backups/
*.bak
*.backup
```

Backups often contain historical private content or environment-specific data.

If a backup is needed as a public fixture, it should be sanitized and placed under a clearly named test fixture directory.

---

# 12. Path Policy

Runtime code must not require the original development path:

```text
/home/eye/workspace/hermes-memory
```

The canonical override variable is:

```text
HERMES_MEMORY_ROOT
```

Recommended default local path:

```text
~/workspace/hermes-memory
```

GitHub users may choose another path and set:

```bash
export HERMES_MEMORY_ROOT="/chosen/path"
```

---

# 13. Public Sample Content Policy

The repository should include enough sample content for a new user to understand and test the system.

Recommended sample content:

```text
wiki/sample-project/README.md
wiki/sample-project/decisions.md
wiki/sample-project/verification.md
```

Sample content should demonstrate:

- Markdown source-of-truth
- source citations
- retrieval
- context building
- smoke testing

Sample content must not include private or real operational secrets.

---

# 14. Local Personal Memory Policy

Hermes Runes can store personal curated knowledge, but a public repository should not automatically include the user's private knowledge.

Personal memory may include:

- anime notes
- 3C hardware notes
- hobby notes
- travel notes
- reading notes
- private project notes

These should remain local unless intentionally sanitized and published.

---

# 15. Agent Integration Boundary

Hermes Runes is agent-agnostic.

The repository may provide adapters for:

- Hermes Agent
- OpenClaw
- MCP-compatible runtimes
- local automation tools

Adapters should call the memory subsystem through stable interfaces.

Adapters should not require direct access to private secrets beyond documented local configuration.

---

# 16. GitHub Readiness Checklist

Before initial GitHub publication:

- [ ] `.gitignore` exists
- [ ] `.env.example` exists
- [ ] real `.env` is not tracked
- [ ] observation logs are not tracked
- [ ] database volumes are not tracked
- [ ] `.venv` is not tracked
- [ ] private wiki content is reviewed
- [ ] public README exists
- [ ] root path policy exists
- [ ] taxonomy/layout policy exists
- [ ] repository boundary policy exists
- [ ] smoke command is documented
- [ ] full smoke passes locally

---

# 17. Guiding Principle

The repository should contain the machinery and public-safe runes.

The user's private memory, secrets, logs, and generated state should remain local.

Hermes Runes MD Wiki should be safe to publish without leaking private knowledge or operational credentials.
