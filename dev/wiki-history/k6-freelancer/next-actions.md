## N-20260617-v0.7.3-final

Status: READY FOR FINAL TAG CHECK

Current baseline:

```text
main: single-agent / agent-agnostic active baseline
VERSION: 0.7.3
v0.7.2: archived release point
archive/v0.7.2-opc: archived branch
```

Resolved:

```text
M222 PASS / single-agent sanity locally verified
M223 PASS / active guidance approved and documented
M224 PASS / sync path locally verified
M225 PASS / optional embedding boundary locally verified
M226 PASS / RC locally verified / ready for final release
```

Current work:

```text
M227 v0.7.3 Final Release Lock
```

M227 prepared artifacts:

```text
VERSION
docs/releases/v0.7.3.md
dev/wiki-history/k6-freelancer/verification/verification-m227.md
```

Final local check:

```text
cat VERSION
python3 -m py_compile tools/importer/root_resolver.py
bash -n bin/hermes-memory-sync
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke
git status
```

Expected:

```text
VERSION = 0.7.3
migration guard plan SAFE
Core FTS smoke PASS
working tree clean
```

After final local check passes, create the release tag manually:

```bash
git tag -a v0.7.3 -m "Release v0.7.3"
git push origin v0.7.3
```
