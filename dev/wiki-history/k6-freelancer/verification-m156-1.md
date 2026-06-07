# M156.1 TB Registry Integrity Lock

Status: PASS / REGISTRY RESTORED / FIX APPLIED
Date: 2026-06-07

## Scope

M156.1 records that the Trial Bug Registry was restored after the M156 follow-up check.

This is a documentation integrity lock only. It does not change runtime behavior, proposal state, import behavior, recall behavior, database state, or trusted memory content.

## Fix Commit

```text
2e8b8bd Restore trial bug registry and add CB bug ids
```

## Verification Evidence

The restored registry contains:

```text
TB-20260605-001
TB-20260605-015
TB-20260607-001
TB-20260607-002
```

The developer checkout reported:

```text
working tree clean
branch up to date with origin/main
```

## Related Records

```text
TB-20260607-001 M156 trial-root quote typo
TB-20260607-002 trial-bugs registry restore follow-up
```

## Process Rule

For large Markdown registry files, prefer this process:

```text
local full-file edit
local grep verification
git diff inspection
commit
push
```

Avoid direct full-file replacement from a truncated remote preview.

## Boundary

```text
no runtime change
no proposal change
no promotion change
no import change
no backend change
```

## Next Action

Proceed to:

```text
M157 First Real User Technical Input CB Session
```

## Verification Commands

Developer checkout:

```bash
cd ~/workspace/hermes-runes-md-wiki

git pull
git status
git log --oneline -8

grep -n "TB-20260605-001\|TB-20260605-015\|TB-20260607-001\|TB-20260607-002" \
  wiki/k6-freelancer/trial-bugs.md

grep -n "Status:\|M156.1\|REGISTRY RESTORED\|2e8b8bd\|M157\|Final Lock" \
  wiki/k6-freelancer/verification-m156-1.md
```

Trial checkout:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status --short

grep -n "TB-20260605-001\|TB-20260605-015\|TB-20260607-001\|TB-20260607-002" \
  wiki/k6-freelancer/trial-bugs.md

grep -n "Status:\|M156.1\|REGISTRY RESTORED\|2e8b8bd\|M157\|Final Lock" \
  wiki/k6-freelancer/verification-m156-1.md
```

## Final Lock

```text
M156.1 TB Registry Integrity Lock
PASS / registry restored / fix applied
```
