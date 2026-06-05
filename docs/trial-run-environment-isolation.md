# Trial-run Environment Isolation Baseline

Status: M86 design baseline

This guide defines how to run a realistic fresh-user trial-run while preserving the developer environment for continued debugging and feature refinement.

The goal is to simulate a real user installation without deleting or contaminating the active developer working tree.

---

## Baseline decision

Do not delete the active developer checkout for trial-run simulation.

Use two separate local clones:

```text
Developer environment:
~/workspace/hermes-runes-md-wiki

Trial-run user environment:
~/workspace-trial/hermes-runes-md-wiki
```

Use one shared external PostgreSQL Docker service if desired, but separate runtime databases:

```text
Developer DB:
hermes_memory

Trial-run DB:
hermes_memory_trial
```

This keeps the system simple while preventing importer, migration, recall, and smoke outputs from contaminating the developer baseline.

---

## Responsibility split

The shared Docker service may provide:

```text
PostgreSQL process
pgvector extension availability
container health check
localhost port binding
```

Each clone owns its own:

```text
project root
local runtime config
Python virtual environment
runtime database target
logs and observations
trial records
```

---

## Recommended environment variables

Developer shell:

```bash
export HERMES_MEMORY_ROOT="$HOME/workspace/hermes-runes-md-wiki"
export HERMES_POSTGRES_STACK="$HOME/docker-stacks/hermes-memory-postgres"
```

Trial-run shell:

```bash
export HERMES_MEMORY_ROOT="$HOME/workspace-trial/hermes-runes-md-wiki"
export HERMES_POSTGRES_STACK="$HOME/docker-stacks/hermes-memory-postgres"
```

The trial clone should configure its own local runtime settings so that runtime database operations target the trial database, not the developer database.

---

## Runtime DB target rule

Schema migration, import, recall, and smoke should use the runtime database configured by the clone.

For schema migration, `bin/hermes-memory-migrate` resolves the target in this order:

```text
1. runtime database URL from current shell
2. runtime database URL from importer-local config
3. fallback to external PostgreSQL stack default database
```

For realistic trial-run isolation, use option 1 or 2.

Do not rely on fallback to the Docker stack default database for trial-run.

---

## Trial database preparation

Before a trial-run migration, prepare a separate trial database in the existing local PostgreSQL service.

Example intent:

```text
connect to the existing local PostgreSQL service
check whether database hermes_memory_trial exists
create hermes_memory_trial if missing
```

Keep this step explicit and human-visible.

Do not print local secret files.

Do not commit local runtime credentials.

---

## Trial clone flow

```bash
mkdir -p ~/workspace-trial
cd ~/workspace-trial

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git hermes-runes-md-wiki
cd hermes-runes-md-wiki

export HERMES_MEMORY_ROOT="$HOME/workspace-trial/hermes-runes-md-wiki"
export HERMES_POSTGRES_STACK="$HOME/docker-stacks/hermes-memory-postgres"
```

Then follow `QUICKSTART.md`.

Before migration, configure the trial clone local runtime settings so the runtime database target is:

```text
hermes_memory_trial
```

Do not paste real credentials into documentation, chat, wiki, or trial records.

---

## Guard and migration checks

From the trial clone:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
bash ./bin/hermes-memory-migrate
```

Expected behavior:

```text
backend guard checks the shared external PostgreSQL service
schema migration applies to the trial runtime database
second migration is idempotent
```

The migration output should show a `db_source` field indicating that runtime DB resolution was used.

---

## Git and artifact rules

The trial clone is not the developer repo.

Trial artifacts may appear in:

```text
wiki/k6-freelancer/trials/
logs/
local runtime config
local virtual environment
```

Do not push trial clone changes unless the human explicitly decides to promote a trial observation record back to the developer repo.

The developer repo remains the place for curated commits and GitHub pushes.

---

## Why not separate Docker service by default?

A second PostgreSQL Docker stack would be more isolated, but it also increases setup friction, port management, backup complexity, and agent burden.

For P0 / early trial-run, the recommended baseline is:

```text
shared PostgreSQL Docker service
separate runtime databases
separate repo clones
separate local runtime configs
```

This is mature enough to prevent contamination while staying simple for personal-local use.
