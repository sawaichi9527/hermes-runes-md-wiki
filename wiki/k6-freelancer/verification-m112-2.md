# M112.2 Recall/Index Remediation for First P0 Trial-run

Status: IMPLEMENTED / PENDING RECALL INDEX REMEDIATION
Date: 2026-06-06

## Purpose

M112.2 defines the bounded recall/index remediation plan for the first practical P0 trial-run.

M112.1 captured that the first P0 trial-run reached proposal creation and promoted reviewed-file creation, but recall verification failed because the promoted M112 file was not discoverable through the recall/index layer.

This milestone defines the remediation process only.

It does not change runtime behavior.

## Blocking Issue

Current blocking issue:

```text
M112 promoted reviewed file exists at the file level.
Direct grep marker verification passes.
Recall verification returns FAIL / result count: 0.
The promoted M112 file is not yet indexed into the recall database.
```

Blocked file:

```text
wiki/freelancer/m112-p0-proposal-first-persistence.md
```

Marker phrase:

```text
M112 P0 proposal-first persistence marker
```

## Current Trial Repo State

Trial repo:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Observed untracked files:

```text
?? wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md
?? wiki/freelancer/m112-p0-proposal-first-persistence.md
```

Current state must remain visible until remediation is complete.

Do not hide the issue by deleting files.

## Remediation Goal

The goal is to make this command pass, or capture precisely why it cannot pass in the current trial repo:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

python3 tools/runes/recall_verify_m28_3.py \
  --project freelancer \
  "proposal-first persistence" \
  --expected-path wiki/freelancer/m112-p0-proposal-first-persistence.md \
  --required-marker "M112 P0 proposal-first persistence marker"
```

Target result:

```text
PASS
```

## Safety Scope

M112.2 must stay bounded:

```text
Project: freelancer only
Target marker: M112 P0 proposal-first persistence marker only
Target promoted file: wiki/freelancer/m112-p0-proposal-first-persistence.md
No unrelated proposal promotion
No unrelated wiki mutation
No broad multi-workspace import unless the importer design only supports whole-wiki import and that behavior is understood
No secrets in wiki/git/logs
```

## Step 1: Inspect Available Tools

Run from trial repo:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

find bin tools -maxdepth 3 -type f | sort | grep -E "import|index|embed|recall|sync|chunk|smoke"

bash bin/hermes-memory-import --help 2>&1 | head -120 || true
bash bin/hermes-recall --help 2>&1 | head -120 || true
python3 tools/runes/recall_verify_m28_3.py --help 2>&1 | head -120 || true
```

Capture:

```text
Available import/index command: TBD
Available recall command: TBD
Supports project/path scoping: TBD
Requires venv/env: TBD
```

## Step 2: Confirm File-level State Before Indexing

Run:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git status --short

find wiki/freelancer -maxdepth 2 -type f | sort | grep -E "m112|forge-inbox"

grep -n "status:\|trust_class:\|M112 P0 proposal-first persistence marker" \
  wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md \
  wiki/freelancer/m112-p0-proposal-first-persistence.md
```

Expected current state:

```text
forge-inbox proposal status: draft
forge-inbox proposal trust_class: unreviewed
promoted reviewed file status: approved
promoted reviewed file trust_class: reviewed
marker present in both files
```

## Step 3: Fix Promoted File Verification-plan Path

The promoted file currently contains a copied verification command that still references the forge-inbox expected path.

Fix only the promoted file content so its internal verification plan references:

```text
wiki/freelancer/m112-p0-proposal-first-persistence.md
```

Do not change the draft proposal file unless explicitly required.

Suggested bounded edit:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

python3 - <<'PY'
from pathlib import Path
p = Path('wiki/freelancer/m112-p0-proposal-first-persistence.md')
s = p.read_text(encoding='utf-8')
s = s.replace(
    'wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md',
    'wiki/freelancer/m112-p0-proposal-first-persistence.md'
)
p.write_text(s, encoding='utf-8')
PY

grep -n "expected-path\|M112 P0 proposal-first persistence marker" \
  wiki/freelancer/m112-p0-proposal-first-persistence.md
```

## Step 4: Run Bounded Import/Index

Use the least broad correct command discovered in Step 1.

Preferred order:

```text
1. project/path-scoped import/index for freelancer/M112 file
2. project-scoped import/index for freelancer
3. whole-wiki import/index only if that is the existing importer design and no narrower option exists
```

Do not run unrelated destructive commands.

Capture the exact command and summary output.

## Step 5: Re-run Recall Verification

Run:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

python3 tools/runes/recall_verify_m28_3.py \
  --project freelancer \
  "proposal-first persistence" \
  --expected-path wiki/freelancer/m112-p0-proposal-first-persistence.md \
  --required-marker "M112 P0 proposal-first persistence marker"
```

Capture:

```text
Recall verification command: TBD
Recall verification result: PASS / FAIL
Result count: TBD
Matched source path: TBD
Marker found: TBD
```

## Step 6: Post-remediation Git Status

Run:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

git status --short
```

Expected after successful remediation but before final commit decision:

```text
M112 files remain visible as untracked or modified/untracked.
No unrelated files changed unexpectedly.
```

## PASS Criteria

M112.2 can be marked PASS when:

```text
The promoted file verification-plan expected path is corrected.
The correct import/index command is identified and run safely.
Recall verification for the promoted reviewed file returns PASS.
No unrelated workspace or wiki mutation occurs.
No secrets are written to wiki/git/logs.
Post-remediation git status is understood and documented.
```

## PARTIAL Criteria

M112.2 should be marked PARTIAL if:

```text
The file-level issue is corrected.
The import/index command is identified.
Recall still fails due to environment limitation, missing DB, missing embedding model, or unavailable service.
A clear remediation blocker is documented.
```

## FAIL Criteria

M112.2 should be marked FAIL if:

```text
The remediation mutates unrelated files.
The wrong workspace is imported/promoted.
Secrets are written into wiki/git/logs.
The process hides or deletes M112 evidence instead of fixing recall.
The agent bypasses the governed local-agent boundary.
```

## Result Capture Template

After execution, update this file:

```text
Tool inspection: PENDING
File-level state confirmation: PENDING
Promoted file verification-plan path fix: PENDING
Import/index execution: PENDING
Recall verification: PENDING
Post-remediation git status: PENDING
Overall: PENDING
```

## Suggested Next Step After PASS

If M112.2 passes:

```text
M112.3 M112 Trial Files Commit / Verification Lock
```

Suggested purpose:

```text
Commit the two M112 trial files and update M112/M112.1/M112.2 status to reflect the successful first practical P0 trial-run.
```

Then:

```text
M113 First Practical P0 Trial-run Result Freeze
```

Suggested purpose:

```text
Freeze the first practical P0 trial-run result as the baseline for future real-user memory proposal sessions.
```

## Final Lock

```text
M112.2 Recall/Index Remediation for First P0 Trial-run
IMPLEMENTED / pending recall index remediation
```
