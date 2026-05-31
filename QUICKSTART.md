# QUICKSTART

Hermes Runes MD Wiki is a local-first Markdown wiki source-of-truth for governed local RAG memory.

This quickstart describes a generic local deployment flow for a single-user environment.

---

# 1. Requirements

Recommended environment:

- Linux
- Python 3.12+
- PostgreSQL 16+
- pgvector
- Docker / Docker Compose for PostgreSQL deployment
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

git clone <repository-url> hermes-memory
cd hermes-memory
```

Hermes Runes does not require this exact path.

To use a custom path, set:

```bash
export HERMES_MEMORY_ROOT="/your/custom/path"
```

Example:

```bash
export HERMES_MEMORY_ROOT="$HOME/projects/hermes-runes-md-wiki"
```

---

# 3. Python Virtual Environment

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}"

cd tools/importer

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
```

Install project dependencies according to the repository dependency file when available.

Example:

```bash
pip install -r requirements.txt
```

If no dependency file exists yet, install the currently required packages manually according to the deployment notes.

---

# 4. Environment Configuration

Copy the example environment file:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}"

cp .env.example tools/importer/.env
vi tools/importer/.env
```

Required values:

```bash
HERMES_MEMORY_ROOT=~/workspace/hermes-memory
HERMES_MEMORY_DATABASE_URL=postgresql://hermes_memory_user:replace-with-local-password@127.0.0.1:5432/hermes_memory

OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_MODEL=replace-with-local-model-name
OPENAI_API_KEY=replace-with-local-secret-or-not-needed
```

Never commit real `.env` files.

---

# 5. PostgreSQL / pgvector

Hermes Runes uses PostgreSQL as the retrieval backend.

A recommended local Docker stack path is:

```text
~/docker-stacks/hermes-memory-postgres/
```

This is only a recommendation. Users may choose another location.

The database must provide:

- PostgreSQL
- pgvector extension
- database user
- database password
- target database
- schema initialization

Typical database URL format:

```text
postgresql://USER:PASSWORD@HOST:PORT/DBNAME
```

Example:

```text
postgresql://hermes_memory_user:replace-with-local-password@127.0.0.1:5432/hermes_memory
```

---

# 6. Markdown Wiki Source

The Markdown wiki is the curated source-of-truth.

Current engineering baseline example:

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

---

# 7. Import Markdown

Run the importer:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}/tools/importer"

source .venv/bin/activate

python importer.py
```

Expected successful ending:

```text
PASS: Markdown incremental import completed
```

---

# 8. Run Smoke Tests

Run the full smoke baseline:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}"

hermes-memory-smoke
```

Expected baseline:

```text
M5.2 Evaluation Smoke Test: PASS
M10 Observation Log Smoke Test: PASS
M11 Observation Summary Smoke Test: PASS
```

---

# 9. First Recall Query

Example recall query:

```bash
hermes-recall "Telegram integration" --project k6-freelancer --mode hybrid --limit 5
```

Or directly through importer tools:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}/tools/importer"

python context_builder.py   "Telegram integration"   --project k6-freelancer   --json
```

---

# 10. First Governed Answer

Example:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}/tools/importer"

python answer_generator.py   "Telegram integration 是什麼？"   --project k6-freelancer   --path services.md   --heading Telegram   --max-tokens 512   --json
```

This should produce a governed answer with metadata such as:

- selected model profile
- extraction path
- citation integrity
- retry status
- answer length
- context debug

---

# 11. Observation Summary

Observation logs are local runtime data.

Run summary:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-memory}/tools/importer"

python observation_summary.py --days 1 --json
```

Observation logs are intended for:

```text
observe first, tune later
```

They should not be committed to GitHub.

They should not be ingested back into RAG memory.

---

# 12. Repository Safety

Before publishing or committing:

```bash
git status --ignored
```

Confirm that the following are not tracked:

- `.env`
- `.venv/`
- `logs/`
- database volumes
- real secrets
- private observation logs
- private user memory

---

# 13. Current Baseline

Current expected baseline:

```text
Governed Local RAG Baseline: PASS
Observable Local RAG Baseline: PASS
Repository Readiness Policies: Draft Baseline
Portable Root Resolver: PASS
```

---

# 14. Next Steps

Planned future work:

- Hermes Agent integration adapter
- OpenClaw / generic agent adapter
- MCP-compatible interface
- retrieval / rerank quality improvements
- deployment documentation
- sample wiki content
- packaging cleanup

---

# 15. Guiding Principle

A local-first project may have a friendly default path.

A GitHub-ready project must not require that path.

Runtime memory is temporary.

Curated Markdown memory is knowledge intentionally carved into durable runes.
