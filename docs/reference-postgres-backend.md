# Reference PostgreSQL Backend Setup

Status: P0 reference backend guide

This guide describes the external PostgreSQL + pgvector backend used by the P0 reference implementation of Hermes Runes MD Wiki.

The PostgreSQL service is an external prerequisite. It is not owned by the core Hermes Runes MD Wiki install flow.

Hermes Runes MD Wiki owns Markdown memory policy, importer tooling, retrieval tooling, schema migration, smoke tests, and governance boundaries. The PostgreSQL Docker stack owns only the database service lifecycle.

---

## Boundary

The external PostgreSQL stack is responsible for:

- starting PostgreSQL
- creating the configured database, user, password, and volume
- exposing PostgreSQL on localhost
- enabling or making pgvector available
- providing a basic service health check
- backup / restore of the DB service when explicitly requested

Hermes Runes MD Wiki is responsible for:

- verifying that the backend is available
- applying Hermes-owned application schema migrations
- importing Markdown source-of-truth
- running recall, hybrid search, evaluation, and smoke tests
- preserving governance, citation, proposal, and write-safety rules

Do not put Hermes-specific importer tests, vector tests, retrieval baselines, or application schema ownership into the Docker stack as clean-install requirements. Those belong in this repository.

---

## Default stack path

Generic local default:

```text
~/docker-stacks/hermes-memory-postgres
```

Freelancer reference host default:

```text
/home/eye/docker-stacks/hermes-memory-postgres
```

This path is a host default, not a universal requirement.

Agents may override it with:

```bash
export HERMES_POSTGRES_STACK=/path/to/hermes-memory-postgres
```

---

## Clean reference layout

A clean reference PostgreSQL stack should be small:

```text
hermes-memory-postgres/
├── compose.yaml
├── .env.example
├── .env
├── README.md
├── init/
│   └── 001-enable-pgvector.sql
├── check.sh
└── init-service.sh
```

Optional service-lifecycle directories may exist:

```text
backup/
scripts/
```

Local development artifacts are not required for clean deployment:

```text
baselines/
check-m2.sh
test-vector.sql
test-vector-insert.sql
test-vector-query.sql
Hermes-specific migrations/
Hermes-specific backend tests/
```

Project-specific schema, migration, smoke tests, and backend contract checks should live in Hermes Runes MD Wiki.

---

## Expected Compose service

The P0 reference service uses:

```yaml
services:
  postgres:
    image: pgvector/pgvector:0.8.2-pg17-bookworm
    container_name: hermes-memory-postgres
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "127.0.0.1:${POSTGRES_PORT}:5432"
    volumes:
      - hermes-memory-postgres-data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  hermes-memory-postgres-data:
```

The service name is `postgres` and the expected container name is `hermes-memory-postgres`.

---

## Service-level initialization

The Docker stack may provide:

```bash
./init-service.sh
```

This script should only:

- check that `.env` exists
- check that `compose.yaml` exists
- run `docker compose up -d`
- wait until the container is healthy
- verify PostgreSQL connectivity
- verify pgvector availability

It must not:

- create Hermes application tables
- import Markdown files
- run recall or evaluation
- mutate `wiki/`
- reset database volumes
- overwrite `.env`

Hermes application schema initialization is performed from this repository after backend verification.

---

## Backend guard from Hermes Runes MD Wiki

After cloning or updating Hermes Runes MD Wiki, verify the external backend from the repository root:

```bash
bash ./bin/hermes-backend-check
```

Expected success:

```json
{"status":"PASS","backend":"postgres"}
```

If the backend is missing, stopped, unhealthy, unreachable, or missing pgvector, the command returns a blocked status and a non-zero exit code.

A blocked backend is not the same as empty memory.

---

## Hermes schema migration

After backend guard passes, run the Hermes-owned schema migration:

```bash
bash ./bin/hermes-memory-migrate
```

This command belongs to Hermes Runes MD Wiki, not to the PostgreSQL Docker stack.

The migration command should be idempotent and safe to rerun. Failed migrations must not be marked as applied.

---

## Secret handling

Agents and humans may check that `.env` exists and may load it for local commands.

They must not:

- print `.env`
- paste `.env` into chat
- ingest `.env` into RAG memory
- write `.env` into Markdown wiki files
- commit `.env`
- put PostgreSQL passwords into proposals, logs, or documentation

Use `.env.example` for public templates only.

---

## Missing backend behavior

If the backend stack is missing, agents should stop and report the missing prerequisite.

They may only deploy the reference PostgreSQL backend when the user explicitly asks for backend setup.

If the stack exists but is stopped, agents may start it only when the user requested deployment or environment startup.

Agents must not automatically repair, reset, recreate, or replace the backend.

The goal is personal-use reliability, not enterprise-grade infrastructure automation.
