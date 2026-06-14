## N-20260614-M216 v0.7.2 Annotated Tag Lock

Status: READY FOR LOCAL RELEASE CHECK

Current state:
- M214 release prep decision: PASS.
- M215 release notes / VERSION alignment: ready for local release check.
- VERSION is expected to be `0.7.2` after guarded update.

Run locally before tag:

```bash
./bin/runes-wiki-migration-guard update
cat VERSION
python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/runes-wiki-migration-guard update --dry-run --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12
```

If clean and PASS, create the annotated tag:

```bash
git tag -a v0.7.2 -m "Release v0.7.2"
git push origin v0.7.2
```

Do not start M217 until the tag is confirmed.

---
