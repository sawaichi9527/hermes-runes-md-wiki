# QUICKSTART

Hermes Runes MD Wiki is a local-first Markdown wiki source-of-truth for governed local RAG memory.

This quickstart describes a generic local deployment flow for a single-user environment and is written for a fresh GitHub clone.

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

# 3. Python Virtual Environment

Create the virtual environment under `tools/importer`, then install dependencies from the repository root requirements file:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cd tools/importer

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r ../../requirements.txt
```

---

# 4. Environment Configuration

Copy the example environment file into the importer runtime location:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

cp .env.example tools/importer/.env
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

Keep the actual value only in your local `.env` file.

---

# 6. Markdown Wiki Source

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

---

# 7. Import Markdown

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

# 8. Run Smoke Tests

Run the full smoke baseline:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

./bin/hermes-memory-smoke
```

If you installed the wrapper into `~/.local/bin`, this should also work:

```bash
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

Public-safe recall query:

```bash
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

# 10. First Governed Answer

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

# 11. Observation Summary

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

# 13. Re-clone Migration Check

For validating the GitHub-first external-user flow, move the old local working tree aside and clone into the new repository-named path:

```bash
cd ~/workspace

mv hermes-memory hermes-memory.local-backup-$(date +%Y%m%d-%H%M%S)

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git hermes-runes-md-wiki
cd hermes-runes-md-wiki

export HERMES_MEMORY_ROOT="$HOME/workspace/hermes-runes-md-wiki"
```

Then continue from section 3.

Do not delete the old backup until the new clone has passed import, smoke, recall, and governed-answer checks.

---

# 14. Current Baseline

Current expected baseline:

```text
Governed Local RAG Baseline: PASS
Observable Local RAG Baseline: PASS
Repository Readiness Policies: Draft Baseline
Portable Root Resolver: PASS
```

---

# 15. Next Steps

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

# 16. Guiding Principle

A local-first project may have a friendly default path.

A GitHub-ready project must not require that path.

Runtime memory is temporary.

Curated Markdown memory is knowledge intentionally carved into durable runes.
