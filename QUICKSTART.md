# QUICKSTART

Hermes Runes MD Wiki is a local-first Markdown wiki source-of-truth for governed local RAG memory.

This quickstart describes a generic local deployment flow for a single-user environment and is written for a fresh GitHub clone.

---

# 1. Requirements

Recommended environment:

- Linux
- Python 3.12+
- PostgreSQL 16+ or 17
- pgvector
- Docker / Docker Compose for the external PostgreSQL reference backend
- local or LAN OpenAI-compatible LLM endpoint

Optional but recommended:

- `jq`
- `psql`
- `curl`

---

# 2. Clone Repository

Recommended default path:

```bash
mkdir -p ~/workspace
cd ~/workspace

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git hermes-runes-md-wiki
cd hermes-runes-md-wiki
```

Hermes Runes does not require this exact path.

To use a custom path, set:

```bash
export HERMES_MEMORY_ROOT="/your/custom/path"
```

Recommended default for this repository:

```bash
export HERMES_MEMORY_ROOT="$HOME/workspace/hermes-runes-md-wiki"
```

The environment variable is still named `HERMES_MEMORY_ROOT` for compatibility with existing importer, retrieval, and smoke-test tooling.

---

# 3. Read Agent Bootstrap Instructions

Humans and agents should read:

```text
README.md
AGENTS.md
docs/reference-postgres-backend.md
```

`AGENTS.md` is the repository-level bootstrap guide for agent acquisition, backend prerequisite checks, schema migration, missing workspace behavior, and forbidden actions.

Detailed governed runtime policy still lives under:

```text
wiki/_system/
```

---

# 4. Python Virtual Environment

Create the virtual environment under `tools/importer`, then install the lightweight core dependencies from the repository root requirements file:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"
cd tools/importer

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r ../../requirements.txt
```

The core dependency profile intentionally avoids the local embedding stack so a fresh clone does not immediately install large PyTorch / CUDA packages.

If local vector embedding is needed, install the optional embedding profile:

```bash
pip install -r ../../requirements-embedding.txt
```

---

# 5. Environment Configuration

The importer runtime environment lives beside the importer tools.

Use this pair:

```text
tools/importer/.env.example  # public template, tracked by git
tools/importer/.env          # local runtime config, never committed
```

Create your local runtime config:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cp tools/importer/.env.example tools/importer/.env
vi tools/importer/.env
```

Required local values:

```bash
HERMES_MEMORY_ROOT=~/workspace/hermes-runes-md-wiki
HERMES_MEMORY_DATABASE_URL=postgresql://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME

OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_MODEL=your-local-model-name
OPENAI_API_KEY=not-set
```

Do not create a root `.env` for the normal quickstart flow. Keep the active runtime config at `tools/importer/.env` so there is only one authoritative local environment file.

Database connection handling is centralized in:

```text
tools/importer/db_config.py
```

Normal tools should use `HERMES_MEMORY_DATABASE_URL` through this shared helper instead of each script independently parsing PostgreSQL password variables.

Never commit real `.env` files.

---

# 6. Memory Backend Prerequisite

Hermes Runes MD Wiki requires a compatible memory backend before importer, recall, hybrid search, evaluation, or smoke tests can run.

For P0, the reference backend is PostgreSQL + pgvector.

The PostgreSQL Docker service is an external prerequisite. It is not automatically created, reset, or owned by the core repository install flow.

Reference backend guide:

```text
docs/reference-postgres-backend.md
```

Recommended local Docker stack path:

```text
~/docker-stacks/hermes-memory-postgres
```

Freelancer reference host default:

```text
/home/eye/docker-stacks/hermes-memory-postgres
```

If the stack lives somewhere else, set:

```bash
export HERMES_POSTGRES_STACK="/path/to/hermes-memory-postgres"
```

The backend stack owns:

- PostgreSQL service startup
- database user, password, target database, and volume
- pgvector service-level availability
- container health checks

Hermes Runes MD Wiki owns:

- backend readiness checks
- Hermes application schema migration
- importer / recall / smoke verification
- Markdown wiki governance and source-of-truth rules

---

# 7. Backend Guard

Before DB-dependent operations, verify the external backend:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

bash ./bin/hermes-backend-check
```

Expected success:

```json
{"status":"PASS","backend":"postgres","stack":"...","message":"Backend prerequisite is available."}
```

If the backend is missing, stopped, unhealthy, unreachable, or missing pgvector, the command reports a blocked state and exits non-zero.

A blocked backend is not the same as empty memory.

Do not print the backend stack `.env` file.

---

# 8. Hermes Schema Migration

After backend guard passes, initialize or migrate the Hermes application schema from this repository:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

bash ./bin/hermes-memory-migrate
```

This command does not create or manage the PostgreSQL Docker service.

It applies idempotent migrations from:

```text
migrations/postgres/
```

Failed migrations must not be treated as PASS. Restore backend availability, then rerun the migration command.

---

# 9. Markdown Wiki Source

The Markdown wiki is the curated source-of-truth.

Public-safe sample baseline:

```text
wiki/sample-project/
```

Private engineering baseline example:

```text
wiki/k6-freelancer/
```

Hermes Runes supports both:

```text
flat-first layout:
wiki/tech-pc-hardware-ssd.md

folder-based layout:
wiki/k6-freelancer/verification.md
```

Engineering projects should generally use folder-based layouts.

Small personal knowledge areas may use flat filenames until they grow large enough to justify folders.

If no host/workspace mapping exists, agents should not create wiki files directly. They should offer a governed workspace proposal.

---

# 10. Import Markdown

Run the importer:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"
source .venv/bin/activate

python importer.py
```

Expected successful ending:

```text
PASS: Markdown incremental import completed
```

---

# 11. Run Smoke Tests

Run the smoke baseline:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

./bin/hermes-memory-smoke
```

If you installed the wrapper into `~/.local/bin`, this should also work:

```bash
hermes-memory-smoke
```

Expected full embedding baseline:

```text
Core FTS Smoke Test: PASS
M5.2 Evaluation Smoke Test: PASS
M10 Observation Log Smoke Test: PASS
M11 Observation Summary Smoke Test: PASS
M11.6 Sample Project Smoke Test: PASS
```

If only the core dependencies are installed, the smoke wrapper should run the core FTS test and skip embedding-dependent suites.

---

# 12. First Recall Query

Core-only public-safe recall query using FTS:

```bash
./bin/hermes-recall "sample project" --project sample-project --mode fts --limit 5
```

Hybrid or vector recall requires the optional embedding profile:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"
source .venv/bin/activate
pip install -r ../../requirements-embedding.txt

cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"
./bin/hermes-recall "sample project" --project sample-project --mode hybrid --limit 5
```

Or directly through importer tools:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"

python context_builder.py "sample project" --project sample-project --json
```

Private engineering recall example, only if `wiki/k6-freelancer/` exists locally:

```bash
./bin/hermes-recall "Telegram integration" --project k6-freelancer --mode hybrid --limit 5
```

---

# 13. First Governed Answer

Public-safe example:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"

python answer_generator.py \
  "What is the sample project?" \
  --project sample-project \
  --max-tokens 512 \
  --json
```

This should produce a governed answer with metadata such as:

- selected model profile
- extraction path
- citation integrity
- retry status
- answer length
- context debug

---

# 14. Observation Summary

Observation logs are local runtime data.

Run summary:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"

python observation_summary.py --days 1 --json
```

Observation logs are intended for:

```text
observe first, tune later
```

They should not be committed to GitHub.

They should not be ingested back into RAG memory.

---

# 15. Repository Safety

Before publishing or committing:

```bash
git status --ignored
```

Confirm that the following are not tracked:

- `tools/importer/.env`
- `.env`
- `.venv/`
- `logs/`
- database volumes
- real secrets
- private observation logs
- private user memory

Current safety baseline:

```text
M12.1 Requirements split: PASS
M12.2 Importer-local environment layout: PASS
M12.3 Runtime safety audit: PASS
M12.3a DB config portability cleanup: PASS
```

The only expected database-password-related code reference is the shared compatibility fallback in `tools/importer/db_config.py`; test fixtures and documentation placeholders may also mention placeholder password strings.

---

# 16. Re-clone Migration Check

For validating the GitHub-first external-user flow, move the old local working tree aside and clone into the new repository-named path:

```bash
cd ~/workspace

mv hermes-memory hermes-memory.local-backup-$(date +%Y%m%d-%H%M%S)

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git hermes-runes-md-wiki
cd hermes-runes-md-wiki

export HERMES_MEMORY_ROOT="$HOME/workspace/hermes-runes-md-wiki"
```

Then continue from section 3.

Do not delete the old backup until the new clone has passed backend guard, schema migration, import, smoke, recall, and governed-answer checks.

---

# 17. Current Baseline

Current expected baseline:

```text
Governed Local RAG Baseline: PASS
Observable Local RAG Baseline: PASS
Repository Readiness Policies: Draft Baseline
Portable Root Resolver: PASS
Requirements Split: PASS
Importer-local Environment Layout: PASS
Runtime Safety Audit: PASS
DB Config Portability Cleanup: PASS
External Backend Prerequisite Policy: DESIGN READY
Simple Backend Guard Policy: DESIGN READY
```

---

# 18. Next Steps

Planned future work:

- License selection
- release tag
- issue roadmap
- Hermes Agent integration adapter
- OpenClaw / generic agent adapter
- MCP-compatible interface
- retrieval / rerank quality improvements
- deployment documentation
- packaging cleanup

---

# 19. Guiding Principle

A local-first project may have a friendly default path.

A GitHub-ready project must not require that path.

Runtime memory is temporary.

Curated Markdown memory is knowledge intentionally carved into durable runes.
