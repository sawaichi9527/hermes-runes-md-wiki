# Hermes Memory M3.1 Starter Kit

This starter kit creates the formal command layer skeleton for Phase3 M3.1.

Included:

- config/hermes-memory.yaml
- bin/hermes_memory_common.py
- bin/hermes-memory-check
- bin/hermes-memory-import
- placeholders for embed/sync/backup/restore/eval

Install on K6/Freelancer:

```bash
cd ~/workspace/hermes-memory
tar -xzf /path/to/hermes-memory-m3-1-starter.tar.gz
chmod +x bin/hermes-memory-*
```

Initial validation:

```bash
cd ~/workspace/hermes-memory
./bin/hermes-memory-check --project k6-freelancer --full
./bin/hermes-memory-import --project k6-freelancer --all --dry-run --json
```

If using DB checks:

```bash
export HERMES_MEMORY_DATABASE_URL='postgresql://...'
./bin/hermes-memory-check --project k6-freelancer --full --json
```
