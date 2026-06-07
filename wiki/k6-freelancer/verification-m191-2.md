# M191.2 Trial Checkout Sync / Evidence Availability Verification

Status: READY / TRIAL CHECKOUT SYNC REQUIRED
Date: 2026-06-07

## Evidence Record

```text
wiki/k6-freelancer/verification-m191.md
wiki/k6-freelancer/verification-m191-1.md
wiki/k6-freelancer/cb-bugs.md
docs/m191-1-trial-path-isolation-rerun-prompt.md
```

## Scope

```text
TB-M191-BT001-FU002 follow-up
trial checkout sync verification
evidence file availability check
no runtime feature development
```

## Result

```text
READY
```

## Required Trial Checkout Files

```text
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/m190-read-only-prompt-tightening.md
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/cb-m191-m196-execution-pack.md
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/m191-bt001-hermes-agent-run-prompt.md
/home/eye/workspace-trial/hermes-runes-md-wiki/docs/m191-1-trial-path-isolation-rerun-prompt.md
/home/eye/workspace-trial/hermes-runes-md-wiki/wiki/k6-freelancer/verification-m190.md
/home/eye/workspace-trial/hermes-runes-md-wiki/wiki/k6-freelancer/verification-m190-1.md
/home/eye/workspace-trial/hermes-runes-md-wiki/wiki/k6-freelancer/verification-m191.md
/home/eye/workspace-trial/hermes-runes-md-wiki/wiki/k6-freelancer/cb-bugs.md
```

## Local Verification Commands

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git pull
git status
git log --oneline -5

for f in \
  docs/m190-read-only-prompt-tightening.md \
  docs/cb-m191-m196-execution-pack.md \
  docs/m191-bt001-hermes-agent-run-prompt.md \
  docs/m191-1-trial-path-isolation-rerun-prompt.md \
  wiki/k6-freelancer/verification-m190.md \
  wiki/k6-freelancer/verification-m190-1.md \
  wiki/k6-freelancer/verification-m191.md \
  wiki/k6-freelancer/cb-bugs.md
  do
    test -f "$f" && echo "FOUND $f" || echo "MISSING $f"
  done
```

## Expected Result

```text
All required files should be FOUND in the trial checkout.
working tree should remain clean.
```

## Next Step

```text
After all required files are available in trial checkout, rerun BT-001 using docs/m191-1-trial-path-isolation-rerun-prompt.md.
```

## Final Lock

```text
M191.2 Trial Checkout Sync / Evidence Availability Verification
READY / trial checkout sync required
```
