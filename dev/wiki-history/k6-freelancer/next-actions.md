## N-20260617-v0.7.3-dev RC Prep

Status: READY FOR LOCAL RC CHECK

Current baseline:

```text
main: single-agent / agent-agnostic active baseline
VERSION: 0.7.3-dev
v0.7.2: archived release tag
archive/v0.7.2-opc: archived OPC-capable branch
```

Resolved for v0.7.3-dev:

```text
M222 Single-Agent Baseline Sanity Check
PASS / single-agent sanity locally verified

M223 Agent / Subagent / Kanban Role Model
PASS / active guidance approved and documented

M224 hermes-memory-sync Path Fix
PASS / sync path locally verified

M225 Optional Embedding Profile Boundary
PASS / optional embedding boundary locally verified
```

M226 prepared artifacts:

```text
docs/releases/v0.7.3.md
dev/wiki-history/k6-freelancer/verification/verification-m226.md
```

M226 status:

```text
READY FOR LOCAL RC CHECK
```

Required local RC check:

```bash
cat VERSION
python3 -m py_compile tools/importer/root_resolver.py
bash -n bin/hermes-memory-sync
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
git status
git log --oneline -12
```

Expected baseline:

```text
VERSION = 0.7.3-dev
Core FTS smoke PASS
Embedding profile may be skipped when not installed
working tree clean
```

Next selected work:

```text
M226 Local RC Check / Result Lock
```

Do not create the final release tag until the local RC check is confirmed.
