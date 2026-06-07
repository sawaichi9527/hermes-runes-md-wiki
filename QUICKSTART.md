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

```bash
mkdir -p ~/workspace
cd ~/workspace

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git hermes-runes-md-wiki
cd hermes-runes-md-wiki

export HERMES_MEMORY_ROOT="$HOME/workspace/hermes-runes-md-wiki"
```

The environment variable is still named `HERMES_MEMORY_ROOT` for compatibility with existing importer, retrieval, and smoke-test tooling.

---

# 3. Read First

Humans and agents should read:

```text
README.md
AGENTS.md
docs/open-beta-starter.md
docs/reference-postgres-backend.md
docs/workspace-slug-policy.md
wiki/README.md
wiki/hermes_runes_index.md
```

Detailed governed runtime policy lives under:

```text
wiki/_system/
```

---

# 4. Python Virtual Environment

For a normal fresh clone, use the bootstrap wrapper. It creates `tools/importer/.venv` and installs only the lightweight core dependency profile.

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

bash ./bin/hermes-memory-bootstrap
```

Default bootstrap behavior:

```text
- creates tools/importer/.venv if missing
- installs requirements-core.txt only
- does not install torch / CUDA / sentence-transformers
- does not touch Docker
- does not create or edit .env secrets
- does not run migrations
```

Manual equivalent:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"
cd tools/importer

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r ../../requirements.txt
```

`requirements.txt` is intentionally a lightweight alias to `requirements-core.txt`.

If local vector embedding is needed, install the optional embedding profile through the bootstrap wrapper:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

bash ./bin/hermes-memory-bootstrap --with-embedding
```

The embedding path installs CPU-only torch first, then installs `requirements-embedding.txt`, to avoid pulling large CUDA wheels during personal-local fresh clone setup.

---

# 5. Environment Configuration

The importer runtime environment lives beside the importer tools.

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

Required local values include:

```text
HERMES_MEMORY_ROOT
HERMES_MEMORY_DATABASE_URL
OPENAI_BASE_URL
OPENAI_MODEL
OPENAI_API_KEY
```

Use placeholders only in committed docs. Never commit real `.env` files.

---

# 6. Memory Backend Prerequisite

Hermes Runes MD Wiki requires a compatible memory backend before importer, recall, hybrid search, evaluation, or smoke tests can run.

For P0, the reference backend is PostgreSQL + pgvector.

Reference backend guide:

```text
docs/reference-postgres-backend.md
```

Recommended local Docker stack path:

```text
~/docker-stacks/hermes-memory-postgres
```

If the stack lives somewhere else, set:

```bash
export HERMES_POSTGRES_STACK="/path/to/hermes-memory-postgres"
```

Do not print the backend stack `.env` file.

---

# 7. Backend Guard

Before DB-dependent operations, verify the external backend:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

bash ./bin/hermes-backend-check
```

A blocked backend is not the same as empty memory.

---

# 8. Hermes Schema Migration

After backend guard passes, initialize or migrate the Hermes application schema:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}"

bash ./bin/hermes-memory-migrate
```

This applies idempotent migrations from:

```text
migrations/postgres/
```

Failed migrations must not be treated as PASS.

---

# 9. Markdown Wiki Source

The Markdown wiki is the curated source-of-truth.

Clean runtime seed:

```text
wiki/
  _system/
  freelancer/
```

For other installations, create or use a workspace based on the local hostname:

```text
wiki/<lowercase-hostname>/
```

Developer history, trial evidence, beta observations, and old fixtures are stored outside runtime memory:

```text
dev/wiki-history/
dev/docs/
```

Do not import `dev/` as runtime user memory by default.

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

---

# 12. First Recall Query

Use the active workspace slug. For the current dogfood host:

```bash
./bin/hermes-recall "preferences" --project freelancer --mode fts --limit 5
```

For another host, replace `freelancer` with that host's lowercase hostname-derived workspace slug.

Hybrid or vector recall requires the optional embedding profile.

---

# 13. First Governed Answer

Example using the current dogfood workspace:

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"

python answer_generator.py \
  "What preferences are recorded?" \
  --project freelancer \
  --max-tokens 512 \
  --json
```

---

# 14. Observation Summary

Observation logs are local runtime data.

```bash
cd "${HERMES_MEMORY_ROOT:-$HOME/workspace/hermes-runes-md-wiki}/tools/importer"

python observation_summary.py --days 1 --json
```

Observation logs should not be committed to GitHub and should not be ingested back into RAG memory.

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

---

# 16. Guiding Principle

Runtime memory is temporary.

Curated Markdown memory is knowledge intentionally carved into durable runes.

The database is an index and retrieval backend.

The Markdown wiki remains the human-readable source-of-truth.
