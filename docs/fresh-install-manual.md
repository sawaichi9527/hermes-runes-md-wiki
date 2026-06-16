# Fresh Install Manual

Status: v0.7.3-dev single-agent fresh-install baseline  
Released baseline: v0.7.2  
Current development line: 0.7.3-dev  
Date: 2026-06-17

## Scope

This is the standalone fresh-install runbook for Hermes Runes MD Wiki on the current `main` development line.

Validated target:

- Ubuntu 24.04.x LTS Desktop or Server
- normal trusted local user
- bash shell
- Docker CE with Docker Compose plugin
- PostgreSQL / pgvector via local Docker stack
- repository checkout under `~/workspace/hermes-runes-md-wiki`
- single-agent / agent-agnostic mainline baseline

The default install path is intentionally personal/local:

- one local repository checkout
- one PostgreSQL container
- one Docker named volume
- local-only database port binding on `127.0.0.1:5433`
- core profile first: PostgreSQL / migration / Markdown import / FTS recall / core smoke
- embedding, hybrid/vector recall, answer generation, and agent onboarding are optional gates

## Mainline boundary

`main` is the active single-agent / agent-agnostic baseline.

The old Hermes Agent profile-based OPC overlay is not active on `main`. The archived OPC-capable release baseline is preserved separately as:

```text
v0.7.2
archive/v0.7.2-opc
```

Do not enable profile-agent OPC assumptions during a normal fresh install.

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

## Minimal fresh-install flow

```bash
cd ~/workspace

git clone https://github.com/sawaichi9527/hermes-runes-md-wiki.git
cd ~/workspace/hermes-runes-md-wiki

cat VERSION
bash ./bin/hermes-memory-bootstrap
```

Then configure the local PostgreSQL stack and `tools/importer/.env` according to the local machine. Keep secrets out of Markdown and out of git.

After the database is ready:

```bash
./bin/hermes-memory-import
./bin/hermes-memory-smoke
```

Expected core result:

```text
Core FTS Smoke Test: PASS
```

If embedding dependencies are not installed, hybrid/vector and answer-generation smoke suites are skipped by design.

## Optional embedding profile

Core fresh install does not require embedding dependencies.

To install the optional embedding/full-smoke profile:

```bash
bash ./bin/hermes-memory-bootstrap --with-embedding
```

This installs CPU-only torch first, then `requirements-embedding.txt`, to avoid pulling large CUDA wheels during personal/local setup.

## Existing installation updates

For an existing local checkout, prefer the migration guard instead of a naked pull:

```bash
./bin/runes-wiki-migration-guard update
```

The guard backs up `wiki/`, checks incoming repository changes, and refuses unsafe updates that may touch possible user-owned Markdown.

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

cd ~

if [ -f ~/docker-stacks/hermes-memory-postgres/compose.yaml ]; then
  cd ~/docker-stacks/hermes-memory-postgres
  docker compose down -v || true
fi

cd ~
docker rm -f hermes-memory-postgres 2>/dev/null || true

docker volume ls -q 2>/dev/null | grep 'hermes-memory-postgres' | while read -r vol; do
  echo "removing volume: $vol"
  docker volume rm "$vol" || true
done

rm -rf ~/docker-stacks/hermes-memory-postgres

test ! -e ~/docker-stacks/hermes-memory-postgres && echo "PASS postgres stack removed" || echo "FAIL postgres stack still exists"
ls -ld ~/workspace/hermes-runes-md-wiki 2>/dev/null || echo "INFO repo checkout not present"
```

### Remove repository checkout and local venv only

This removes the local repository checkout and any virtual environment stored inside that checkout.

It does not remove the PostgreSQL container, stack directory, or Docker volume.

```bash
echo "WARNING: this removes ~/workspace/hermes-runes-md-wiki and its local venvs."
echo "It does NOT remove PostgreSQL container, stack, or Docker volume."
echo "Press Ctrl+C now if this is not intended."
sleep 8

cd ~

ls -ld ~/workspace/hermes-runes-md-wiki 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki/.venv 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki/tools/importer/.venv 2>/dev/null || true
ls -ld ~/workspace/hermes-runes-md-wiki-venv 2>/dev/null || true

rm -rf ~/workspace/hermes-runes-md-wiki-venv
rm -rf ~/workspace/hermes-runes-md-wiki

test ! -e ~/workspace/hermes-runes-md-wiki && echo "PASS repo removed" || echo "FAIL repo still exists"
test ! -e ~/workspace/hermes-runes-md-wiki-venv && echo "PASS sibling hermes-runes-md-wiki-venv removed" || echo "FAIL sibling hermes-runes-md-wiki-venv still exists"

ls -ld ~/docker-stacks/hermes-memory-postgres 2>/dev/null || echo "INFO postgres stack not present"
```

## Change Log

- 2026-06-08: Initial standalone fresh-install runbook.
- 2026-06-17: Updated for v0.7.3-dev single-agent mainline after OPC overlay was archived out of active `main`.
