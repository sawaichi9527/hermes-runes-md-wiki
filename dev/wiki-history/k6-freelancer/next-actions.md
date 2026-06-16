## N-20260614-M221 De-OPC Mainline Rebaseline

Status: READY FOR LOCAL DE-OPC CHECK

Current decision:
- Hermes Agent profile-based OPC/A2A deployment is abandoned for this project.
- `v0.7.2` remains the archived OPC-capable release baseline.
- `archive/v0.7.2-opc` preserves that branch state.
- `main` should return to single-agent / agent-agnostic active baseline.
- Migration guard and existing-installation update flow remain active.

M221 implementation result:
- active OPC overlay references removed from README
- active OPC policy removed from `wiki/_system/README.md` read order
- active OPC docs removed from main
- active `wiki/freelancer/opc/` seed removed from main
- v0.7.2 release notes updated with archive branch note

Suggested local validation:

```bash
cd ~/workspace/hermes-runes-md-wiki

./bin/runes-wiki-migration-guard update
cat VERSION

test ! -e docs/opc-workspace-overlay.md
test ! -e wiki/_system/opc-workspace-overlay-policy.md
test ! -e wiki/freelancer/opc/README.md

python3 -m py_compile tools/wiki_migration_guard/migration_guard.py
./bin/runes-wiki-migration-guard plan --no-fetch
./bin/hermes-memory-smoke

git status
git log --oneline -12

grep -n "Status:\|READY FOR LOCAL DE-OPC CHECK\|M221" \
  dev/wiki-history/k6-freelancer/verification/verification-m221.md \
  dev/wiki-history/k6-freelancer/next-actions.md
```

M221 non-goals:
- no reset of `main`
- no deletion of `v0.7.2` tag
- no deletion of `archive/v0.7.2-opc`
- no migration guard removal
- no Runes Shield schema change
- no VERSION change

---
