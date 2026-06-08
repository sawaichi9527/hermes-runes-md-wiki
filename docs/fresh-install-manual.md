# Fresh Install Manual

Status: M204.3 standalone runbook / procedure confirmation
Target: v0.7.0
Open Beta target: v0.7.0
Date: 2026-06-08

## Scope

This is the standalone fresh install runbook for Hermes Runes MD Wiki on the current `main` development line.

Validated target:

- Ubuntu 24.04.x LTS Desktop or Server
- normal trusted local user
- bash shell
- Docker CE with Docker Compose plugin
- PostgreSQL / pgvector via local Docker stack
- current `main` version: `0.7.0-dev`

Open Beta target is now `v0.7.0`. Do not create or move the `v0.7.0` tag until the final M206 release gate passes.

The default install path is intentionally personal/local:

- one local repository checkout
- one PostgreSQL container
- one Docker named volume
- local-only database port binding on `127.0.0.1:5433`
- core profile first: PostgreSQL / migration / Markdown import / FTS recall / core smoke
- embedding, hybrid/vector recall, answer generation, and agent onboarding are later optional gates

## Safety boundary

Do not put real secrets, tokens, passwords, private keys, or raw sensitive logs into Markdown wiki memory.

Do not commit `tools/importer/.env`.

The demo database credentials below are for local fresh install only:

```env
POSTGRES_DB=hermes_memory
POSTGRES_USER=hermes
POSTGRES_PASSWORD=hermes-rw
```

Adding a user to the `docker` group allows that user to control the local Docker daemon. Use this only for trusted local user accounts.

## Optional removal / strict clean reinstall reset

Use this section only for strict fresh-install simulation or intentional local reset.

PostgreSQL data removal and repository checkout removal are intentionally split. Do not combine them unless you really want a full clean reinstall.

### Inspect existing state first

```bash
echo "== repo workspace =="
ls -ld ~/workspace/hermes-runes-md-wiki 2>/dev/null || true

echo "== repo-local virtual environments =="
ls -ld ~/workspace/hermes-runes-md-wiki/.venv 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki/tools/importer/.venv 2>/dev/null || true

echo "== sibling virtual environments =="
ls -ld ~/workspace/.venv 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki-venv 2>/dev/null || true

echo "== postgres stack =="
ls -ld ~/docker-stacks/hermes-memory-postgres 2>/dev/null || true

echo "== docker container =="
docker ps -a --filter name=hermes-memory-postgres 2>/dev/null || true

echo "== docker volumes =="
docker volume ls 2>/dev/null | grep hermes-memory-postgres || true

echo "== local hermes symlinks =="
ls -l ~/.local/bin/hermes-* 2>/dev/null || true
```

### Remove PostgreSQL stack and data only

This removes the local PostgreSQL container, compose stack directory, and matching PostgreSQL Docker volumes.

It does not remove the `hermes-runes-md-wiki` repository checkout.

```bash
echo "WARNING: this removes local Hermes PostgreSQL container and data volume."
echo "It does NOT remove ~/workspace/hermes-runes-md-wiki."
echo "Press Ctrl+C now if this is not intended."
sleep 8

echo
echo "== leave possible stack cwd =="
cd ~

echo
echo "== inspect postgres before removal =="
echo "-- postgres stack --"
ls -ld ~/docker-stacks/hermes-memory-postgres 2>/dev/null || true

echo "-- docker container --"
docker ps -a --filter name=hermes-memory-postgres 2>/dev/null || true

echo "-- docker volumes --"
docker volume ls 2>/dev/null | grep hermes-memory-postgres || true

echo
echo "== compose down with volume =="
if [ -f ~/docker-stacks/hermes-memory-postgres/compose.yaml ]; then
  cd ~/docker-stacks/hermes-memory-postgres
  docker compose down -v || true
else
  echo "SKIP: compose.yaml not found"
fi

cd ~

echo
echo "== remove leftover container =="
docker rm -f hermes-memory-postgres 2>/dev/null || true

echo
echo "== remove leftover matching docker volumes =="
docker volume ls -q 2>/dev/null | grep 'hermes-memory-postgres' | while read -r vol; do
  echo "removing volume: $vol"
  docker volume rm "$vol" || true
done

echo
echo "== remove postgres stack directory =="
rm -rf ~/docker-stacks/hermes-memory-postgres

echo
echo "== postgres removal verification =="
test ! -e ~/docker-stacks/hermes-memory-postgres && echo "PASS postgres stack removed" || echo "FAIL postgres stack still exists"

echo "-- container check --"
docker ps -a --filter name=hermes-memory-postgres 2>/dev/null || true

echo "-- volume check --"
docker volume ls 2>/dev/null | grep hermes-memory-postgres || echo "PASS no matching postgres volume"

echo "-- repo check, should still exist if it existed before --"
ls -ld ~/workspace/hermes-runes-md-wiki 2>/dev/null || echo "INFO repo checkout not present"

echo
echo "== cwd check =="
pwd
```

Expected PostgreSQL removal result:

- PostgreSQL stack path removed
- no `hermes-memory-postgres` container remains
- no matching `hermes-memory-postgres` Docker volume remains
- repository checkout is not removed by this step
- final working directory is the user's home directory

### Remove repository checkout and local venv only

This removes the local repository checkout and any virtual environment stored inside that checkout.

It does not remove the PostgreSQL container, stack directory, or Docker volume.

The normal fresh install venv is under:

```text
~/workspace/hermes-runes-md-wiki/tools/importer/.venv
```

Some local experiments may also create:

```text
~/workspace/hermes-runes-md-wiki/.venv
```

Both are covered by removing the repository checkout.

If a separate sibling venv was manually created beside the repository, this runbook also checks common sibling names, but only removes the explicit Hermes-related sibling path shown below.

```bash
echo "WARNING: this removes ~/workspace/hermes-runes-md-wiki and its local venvs."
echo "It does NOT remove PostgreSQL container, stack, or Docker volume."
echo "Press Ctrl+C now if this is not intended."
sleep 8

echo
echo "== leave possible repo cwd =="
cd ~

echo
echo "== inspect repo and venv before removal =="
ls -ld ~/workspace/hermes-runes-md-wiki 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki/.venv 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki/tools/importer/.venv 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki-venv 2>/dev/null || true

echo
echo "== remove explicit Hermes sibling venv if present =="
rm -rf ~/workspace/hermes-runes-md-wiki-venv

echo
echo "== remove repo checkout, including repo-local venvs =="
rm -rf ~/workspace/hermes-runes-md-wiki

echo
echo "== repo and venv removal verification =="
test ! -e ~/workspace/hermes-runes-md-wiki && echo "PASS repo removed" || echo "FAIL repo still exists"
test ! -e ~/workspace/hermes-runes-md-wiki/.venv && echo "PASS repo .venv removed" || echo "FAIL repo .venv still exists"
test ! -e ~/workspace/hermes-runes-md-wiki/tools/importer/.venv && echo "PASS importer .venv removed" || echo "FAIL importer .venv still exists"
test ! -e ~/workspace/hermes-runes-md-wiki-venv && echo "PASS sibling hermes-runes-md-wiki-venv removed" || echo "FAIL sibling hermes-runes-md-wiki-venv still exists"

echo "-- postgres check, should still exist if it existed before --"
ls -ld ~/docker-stacks/hermes-memory-postgres 2>/dev/null || echo "INFO postgres stack not present"
docker ps -a --filter name=hermes-memory-postgres 2>/dev/null || true
docker volume ls 2>/dev/null | grep hermes-memory-postgres || true

echo
echo "== cwd check =="
pwd
```

Expected repository removal result:

- repo path removed
- repo-local venvs are removed together with the repo
- explicit sibling Hermes venv path is removed if present
- PostgreSQL stack/data is not removed by this step
- final working directory is the user's home directory

### Optional cleanup: local symlinks and stale shell environment

Use this after either PostgreSQL removal or repository removal when preparing a strict fresh-install simulation.

```bash
echo "== remove local hermes symlinks =="
rm -f ~/.local/bin/hermes-backend-check \
      ~/.local/bin/hermes-memory-check \
      ~/.local/bin/hermes-memory-import \
      ~/.local/bin/hermes-memory-migrate \
      ~/.local/bin/hermes-memory-smoke \
      ~/.local/bin/hermes-memory-sync \
      ~/.local/bin/hermes-recall 2>/dev/null || true

echo

echo "== clear stale shell env =="
unset HERMES_MEMORY_DATABASE_URL
unset HERMES_MEMORY_ROOT HERMES_WORKSPACE_SLUG HERMES_PROJECT
unset HERMES_RW_USER HERMES_RW_PASSWORD
unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_PORT POSTGRES_HOST
unset PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD
unset DATABASE_URL

echo

echo "== cleanup verification =="
ls -l ~/.local/bin/hermes-* 2>/dev/null || echo "PASS no local hermes symlinks"
pwd
```

Expected cleanup result:

- no local Hermes symlinks remain
- stale shell DB overrides are cleared for the current shell

For a full strict clean reinstall, run these sections in order:

1. Remove PostgreSQL stack and data only
2. Remove repository checkout and local venv only
3. Optional cleanup: local symlinks and stale shell environment

## 1. Preflight packages and OS check

```bash
echo "== OS =="
. /etc/os-release
echo "$PRETTY_NAME"

echo "== required command checks =="
command -v git || true
command -v curl || true
command -v python3 || true
python3 --version || true
python3 -m venv --help >/dev/null && echo "PASS python3 venv available" || echo "MISSING python3-venv"

sudo apt-get update
sudo apt-get install -y git curl ca-certificates python3 python3-venv python3-pip

python3 --version
python3 -m venv --help >/dev/null && echo "PASS python3 venv available"
```

Expected result:

- Ubuntu 24.04.x host is confirmed
- `git`, `curl`, `python3`, `python3-venv`, and `python3-pip` are installed

## 2. Install Docker CE and enable normal-user Docker access

Check whether Docker is already available:

```bash
echo "== docker availability check =="
docker --version || true
docker compose version || true
systemctl is-active docker || true
id
docker run --rm hello-world || true
```

If `docker run --rm hello-world` succeeds without `sudo`, continue to step 3.

If Docker CE is missing, install it from Docker's official apt repository:

```bash
echo "== install Docker CE prerequisites =="
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

echo "== install Docker official apt key =="
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "== add Docker apt repository =="
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "== install Docker CE packages =="
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "== enable Docker service =="
sudo systemctl enable --now docker
systemctl is-active docker
docker --version
docker compose version
```

Add the current user to the `docker` group:

```bash
echo "== add current user to docker group =="
sudo usermod -aG docker "$USER"

echo
echo "Docker group permission was updated."
echo "Stop here and refresh group membership before continuing."
echo "Use one of: log out/in, reboot, or open a new shell with: newgrp docker"
```

After refreshing group membership, verify:

```bash
echo "== verify Docker as normal user =="
id
docker run --rm hello-world
docker compose version
```

Expected result:

- `id` includes `docker`
- `docker run --rm hello-world` succeeds without `sudo`
- `docker compose version` works

## 3. Clone repository and confirm current main state

This check is branch-oriented. Tags are listed for context only and are not a fresh-install pass/fail gate.

```bash
mkdir -p ~/workspace
cd ~/workspace

test ! -e ~/workspace/hermes-runes-md-wiki || {
  echo "ERROR: ~/workspace/hermes-runes-md-wiki already exists."
  echo "Use git pull for normal update, or run the reset section for strict clean install."
  exit 1
}

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd hermes-runes-md-wiki

echo "== cloned main state =="
git status
git log --oneline -8
cat VERSION
git tag --list --sort=-creatordate | sed -n '1,10p'

echo
echo "== public docs check =="
grep -n "fresh-install-manual.md\|Released baseline\|Current released\|v0.7.0\|v0.5.0\|0.5.0" \
  README.md docs/open-beta-starter.md docs/v0.7.0-tester-checklist.md \
  | sed -n '1,180p'
```

Expected result:

- repository cloned
- working tree clean
- `cat VERSION` shows `0.7.0-dev`
- public docs point current-main fresh installs to `docs/fresh-install-manual.md`
- public docs preserve `v0.5.0` as the released baseline

## 4. Initialize PostgreSQL / pgvector Docker stack

Check for local port conflict first:

```bash
echo "== port 5433 check =="
ss -ltnp | grep ':5433' || echo "PASS no listener on 5433"
```

Create the local PostgreSQL / pgvector stack:

```bash
mkdir -p ~/docker-stacks/hermes-memory-postgres/{config,init,scripts,backup,baselines,migrations}

cd ~/docker-stacks/hermes-memory-postgres

cat > .env <<'ENV'
POSTGRES_DB=hermes_memory
POSTGRES_USER=hermes
POSTGRES_PASSWORD=hermes-rw
ENV

chmod 600 .env

cat > compose.yaml <<'YAML'
services:
  postgres:
    image: pgvector/pgvector:0.8.2-pg17
    container_name: hermes-memory-postgres
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "127.0.0.1:5433:5432"
    volumes:
      - hermes-memory-postgres-data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U hermes -d hermes_memory"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  hermes-memory-postgres-data:
YAML

cat > init/001-init.sql <<'SQL'
CREATE EXTENSION IF NOT EXISTS vector;
SQL

chmod 755 ~/docker-stacks
chmod 755 ~/docker-stacks/hermes-memory-postgres
chmod 755 init
chmod 644 init/001-init.sql
chmod 600 .env

echo "== permissions =="
ls -ld ~/docker-stacks ~/docker-stacks/hermes-memory-postgres init
ls -l .env init/001-init.sql

docker compose up -d

echo "== wait for health =="
for i in $(seq 1 40); do
  state="$(docker inspect -f '{{.State.Status}}' hermes-memory-postgres 2>/dev/null || true)"
  status="$(docker inspect -f '{{.State.Health.Status}}' hermes-memory-postgres 2>/dev/null || true)"
  echo "state=$state health=$status"
  [ "$status" = "healthy" ] && break
  sleep 2
done

echo "== status =="
docker ps --filter name=hermes-memory-postgres

echo "== logs tail =="
docker logs --tail=80 hermes-memory-postgres

echo "== postgres check =="
docker exec hermes-memory-postgres psql -U hermes -d hermes_memory -c "SELECT version();"
docker exec hermes-memory-postgres psql -U hermes -d hermes_memory -c "SELECT extname, extversion FROM pg_extension WHERE extname='vector';"
```

Expected result:

- container `hermes-memory-postgres` becomes healthy
- PostgreSQL reports version 17.x
- pgvector extension reports version 0.8.2
- port binding is local-only: `127.0.0.1:5433 -> 5432`

In this compose form, `POSTGRES_PORT` is not required in the Docker stack `.env` because `compose.yaml` hardcodes `127.0.0.1:5433:5432`.

If an old Docker volume already exists, PostgreSQL may reuse old data and skip init SQL. That is not a strict clean database initialization.

## 5. Configure `tools/importer/.env`

Configure the Hermes importer/runtime environment before bootstrap, migration, import, or smoke tools.

```bash
cd ~/workspace/hermes-runes-md-wiki

test -f tools/importer/.env.example
cp tools/importer/.env.example tools/importer/.env
chmod 600 tools/importer/.env

cat > tools/importer/.env <<'ENV'
# Hermes Runes MD Wiki - local fresh install runtime environment
# Keep this file out of git.

HERMES_MEMORY_ROOT=~/workspace/hermes-runes-md-wiki
HERMES_MEMORY_DATABASE_URL=postgresql://hermes:hermes-rw@127.0.0.1:5433/hermes_memory

# Dogfood/default workspace. Public testers may replace freelancer with lowercase(hostname)
# after a governed workspace exists for that host.
HERMES_DEFAULT_PROJECT=freelancer
HERMES_DEFAULT_SCHEMA=public
HERMES_WORKSPACE_SLUG=freelancer
HERMES_PROJECT=freelancer

# Optional local OpenAI-compatible endpoint placeholders.
OPENAI_BASE_URL=http://127.0.0.1:1234/v1
OPENAI_MODEL=your-local-model-name
OPENAI_API_KEY=not-needed

HERMES_OBSERVATION_LOGGING=1
ENV

chmod 600 tools/importer/.env

unset HERMES_MEMORY_DATABASE_URL
unset HERMES_RW_USER HERMES_RW_PASSWORD
unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_PORT POSTGRES_HOST
unset PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD
unset DATABASE_URL

echo "== importer env check =="
grep -n "HERMES_MEMORY_ROOT\|HERMES_WORKSPACE_SLUG\|HERMES_PROJECT\|HERMES_MEMORY_DATABASE_URL" tools/importer/.env
```

Expected result:

- `tools/importer/.env` exists with mode `600`
- DB URL points to `postgresql://hermes:hermes-rw@127.0.0.1:5433/hermes_memory`
- stale shell DB overrides are cleared

## 6. Bootstrap Python core profile

```bash
cd ~/workspace/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap
```

Expected result:

- `tools/importer/.venv` exists
- core requirements installed
- embedding requirements skipped

The core profile supports PostgreSQL connection, migration, Markdown import, FTS recall, and core smoke checks.

The core profile does not install `sentence-transformers`, `torch`, or `transformers`. This is expected.

## 7. Backend check

```bash
cd ~/workspace/hermes-runes-md-wiki
./bin/hermes-backend-check
```

Expected result:

- backend check PASS
- application tools connect to user `hermes`
- database is `hermes_memory`
- host/port is `127.0.0.1:5433`

## 8. Database migration

Do not run import before migration PASS.

```bash
cd ~/workspace/hermes-runes-md-wiki
./bin/hermes-memory-migrate
```

Expected result:

- migration PASS
- rerunning migration should be safe and should not recreate fresh data unexpectedly

## 9. Import `wiki/`

```bash
cd ~/workspace/hermes-runes-md-wiki
./bin/hermes-memory-import
```

Expected result:

- `PASS: Markdown incremental import completed`
- reruns may show `skipped` or `updated`; that is normal for incremental import
- forge-inbox placeholder content should remain governed and not become trusted memory by accident

## 10. Core FTS recall smoke

```bash
cd ~/workspace/hermes-runes-md-wiki
./bin/hermes-recall "forge inbox boundary" --project freelancer --mode fts --limit 5 --json
```

Expected result:

- status is pass
- fusion is `fts`
- model is `null`
- result cites imported wiki content

This is the minimum retrieval gate for core fresh install.

## 11. Core smoke

```bash
cd ~/workspace/hermes-runes-md-wiki
./bin/hermes-memory-smoke
```

Expected result:

- Core FTS Smoke Test PASS
- embedding, hybrid/vector, and answer-generation suites may be skipped if embedding profile is not installed

Core fresh install PASS means:

- Docker PostgreSQL / pgvector healthy
- importer `.env` configured
- backend check PASS
- migration PASS
- wiki import PASS
- FTS recall PASS
- core smoke PASS

Core fresh install does not require:

- embeddings
- vector search
- hybrid search
- answer generation
- local LLM endpoint
- Hermes-agent integration

## 12. Optional embedding profile

Only install this when hybrid/vector recall is needed.

```bash
cd ~/workspace/hermes-runes-md-wiki
bash ./bin/hermes-memory-bootstrap --with-embedding
```

Then run embedding writer and hybrid/vector validation according to the current project docs.

## 13. Hermes-agent onboarding

Connect Hermes-agent only after the core fresh install gate is PASS.

Minimum gate before onboarding:

- backend check PASS
- migration PASS
- import PASS
- FTS recall PASS
- core smoke PASS

Suggested onboarding prompt:

```text
You are Hermes-agent connecting to Hermes Runes MD Wiki.

Before answering or proposing memory changes, read and follow these files first:

1. AGENTS.md
2. wiki/hermes_runes_index.md
3. wiki/_system/README.md
4. wiki/_system/memory-boundary.md
5. wiki/_system/forge-policy.md
6. wiki/_system/runes-shield.md

Treat Markdown wiki files as the human-readable source of truth.
Treat PostgreSQL as an index and retrieval backend, not the source of truth.
Do not write directly to trusted wiki memory.
Use governed proposal / forge-inbox / Runes Shield workflows for memory changes.
Do not store secrets, credentials, tokens, passwords, private keys, or raw sensitive logs in Markdown memory.
If the active workspace for this host is missing, ask whether to prepare a governed workspace proposal under wiki/<workspace-slug>/.
```


## Hermes-agent onboarding prompt

After a fresh install, you may ask Hermes-agent to read the local guide files before using Hermes Runes MD Wiki.

Use this prompt:

```text
請讀取 ~/workspace/hermes-runes-md-wiki 的導讀文件，理解 Hermes Runes MD Wiki 如何作為 governed Markdown memory 使用。

請先看：

README.md
AGENTS.md
wiki/README.md
wiki/hermes_runes_index.md
wiki/_system/README.md
wiki/_system/runes_shield_contract.md
wiki/_system/runes_invocation_policy.md
wiki/_system/memory-policy.md
wiki/_system/security-policy.md
docs/fresh-install-manual.md

讀完後請用簡短條列回報：
1. 專案用途
2. Hermes-agent 如何接入
3. recall 怎麼用
4. memory proposal 怎麼建立
5. 哪些操作禁止

請不要修改任何檔案。不要直接寫入 trusted wiki。不要保存 secrets。
```

Expected behavior:

- Hermes-agent reads the guide files first.
- Hermes-agent summarizes the project purpose and governance boundary.
- Hermes-agent does not directly modify trusted Markdown memory.
- Hermes-agent does not modify `_system/` policy files.
- Hermes-agent does not save secrets, tokens, passwords, API keys, private keys, or raw sensitive logs.
- Any memory write must go through proposal / review / promotion governance.

For repository-local checks, prefer:

```bash
./bin/hermes-backend-check
./bin/hermes-recall "forge inbox boundary" --project freelancer --mode fts --limit 5 --json
./bin/hermes-memory-smoke
```

## Troubleshooting data to collect

When reporting a fresh-install failure, collect the smallest useful evidence:

```bash
cd ~/workspace/hermes-runes-md-wiki 2>/dev/null || true

echo "== repo =="
git status 2>/dev/null || true
git log --oneline -5 2>/dev/null || true
cat VERSION 2>/dev/null || true

echo "== docker =="
docker ps -a --filter name=hermes-memory-postgres 2>/dev/null || true
docker logs --tail=120 hermes-memory-postgres 2>/dev/null || true

echo "== env file =="
ls -l tools/importer/.env 2>/dev/null || true
grep -n "HERMES_MEMORY_ROOT\|HERMES_WORKSPACE_SLUG\|HERMES_PROJECT\|HERMES_MEMORY_DATABASE_URL" tools/importer/.env 2>/dev/null || true

echo "== backend =="
./bin/hermes-backend-check 2>/dev/null || true
```

## Known fresh-install findings

### TB-M204-DOC001: PostgreSQL init bind mount permission requirement

Symptom:

- container restart loop
- logs mention unreadable `/docker-entrypoint-initdb.d/`

Status:

- Documented.
- Keep stack parent traversable and init SQL readable:
  - `chmod 755 ~/docker-stacks`
  - `chmod 755 ~/docker-stacks/hermes-memory-postgres`
  - `chmod 755 init`
  - `chmod 644 init/001-init.sql`
  - `chmod 600 .env`

### TB-M204-DOC002: backend stack `.env` POSTGRES_PORT mismatch

Status:

- Clarified.
- Current compose hardcodes `127.0.0.1:5433:5432`, so Docker stack `.env` does not need `POSTGRES_PORT`.
- If a future compose template uses `${POSTGRES_PORT}:5432`, add `POSTGRES_PORT=5433` back.

### TB-M204-DOC003: bootstrap must be explicit

Status:

- Documented.
- Fresh clone users must run `bash ./bin/hermes-memory-bootstrap` before importer, recall, migration, or smoke tools.

### TB-M204-DOC004: clone sanity check should be branch-oriented, not tag-grep oriented

Status:

- Documented.
- Tag list is informational only. Current-main fresh install validation relies on `git status`, recent log, `cat VERSION`, and public docs linkage.

### TB-M204-DOC005: existing PostgreSQL volume can hide clean-init problems

Status:

- Documented.
- Strict fresh-install simulation requires removing the old stack and Docker volume before PostgreSQL initialization.

### TB-M204-DOC006: full removal/reset path required

Status:

- Documented.
- Reset path is destructive and intentionally separated from the normal install path.

### TB-M204-DOC007: Docker CE and normal-user Docker permission required

Status:

- Documented.
- Fresh users must install Docker CE and verify `docker run --rm hello-world` works without `sudo`.

### TB-M204-DOC008: local port 5433 conflict check required

Status:

- Documented.
- Check `ss -ltnp | grep ':5433'` before starting the PostgreSQL stack.

### TB-M204-DOC009: freelancer dogfood workspace versus generic hostname workspace

Status:

- Documented.
- Fresh install uses `freelancer` as the verified dogfood/default workspace. Other hosts should use governed workspace creation rather than silently treating a missing workspace as trusted memory.

### TB-M204-DOC010: reset script must leave possible repo working directory before deletion

Status:

- Documented and dry-run verified.
- Repository removal now runs `cd ~` before removing `~/workspace/hermes-runes-md-wiki`.
- Final reset verification includes `pwd` and expects the user's home directory.

### TB-M204-DOC011: reset script should remove leftover matching Docker volumes

Status:

- Documented and dry-run verified.
- PostgreSQL removal runs `docker compose down -v` when compose metadata exists, then removes any leftover Docker volume matching `hermes-memory-postgres`.

### TB-M204-DOC012: PostgreSQL removal and repository removal must be separate

Status:

- Documented.
- PostgreSQL stack/data removal and `hermes-runes-md-wiki` repository checkout removal are separate runbook sections to avoid confusing fresh-install validation state.

### TB-M204-DOC013: repository removal must account for repo-local and sibling venvs

Status:

- Documented.
- Repository removal explicitly inspects repo-local venv paths and removes the repo checkout that contains the default importer venv.
- A common explicit sibling venv path, `~/workspace/hermes-runes-md-wiki-venv`, is also inspected and removed if present.

### TB-M204-AG001: Hermes-agent onboarding must define required entry files and no-direct-write boundary

Status:

- Documented.
- Agent onboarding is post-install only and must read the required policy entry files first.

### TB-M204-FI002: hermes-memory-check still expects removed eval_all.py

Status:

- Known non-blocker for core fresh install.
- Future tooling alignment should check current smoke entrypoints.

### TB-M204-FI003: shell env can override `tools/importer/.env`

Status:

- Documented.
- Clear stale DB-related shell variables before backend check, migration, import, and smoke.

### TB-M204-FI004: retrieval governance smoke is not core-profile aware

Status:

- Known non-blocker for core fresh install.
- Core profile is valid without embedding dependencies.
- Future tooling alignment should SKIP in core-only profile instead of FAIL.

## Current M204 result

Fresh install core profile is verified as:

```text
PASS / Docker CE / PostgreSQL pgvector / importer env / bootstrap core / backend check / migration / import / FTS recall / core smoke
```

## Hermes-agent onboarding read-only smoke

M209 adds a repository-local smoke test for the Hermes-agent onboarding prompt.

This smoke does not start Hermes-agent, does not mutate trusted Markdown memory, and does not touch PostgreSQL. It only validates that the local guide files and onboarding prompt markers are present.

Run:

```bash
./bin/hermes-agent-onboarding-smoke
```

Expected result:

```text
"status": "PASS"
```

This smoke complements the manual Hermes-agent onboarding trial. It confirms that a fresh clone contains the files and prompt needed for a read-only onboarding run.

## Workspace seed cleanup note

A fresh workspace seed should use the generic form:

```text
wiki/<workspace slug>/
```

The `freelancer` workspace is only the demonstration PC workspace slug.

Default workspace Markdown files should not include milestone verification files such as `verification-m*.md`. Historical milestone notes belong under `dev/wiki-history/<workspace slug>/verification/`, not under the runtime workspace seed.
