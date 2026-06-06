# M112.1 P0 Trial-run Issue Capture / Remediation Plan

Status: PASS / M112 ISSUE CAPTURED - RECALL REMEDIATION REQUIRED
Date: 2026-06-06

## Purpose

M112.1 records the first practical P0 trial-run issue discovered during M112 execution.

M112 successfully exercised the proposal-first flow up to proposal file creation and promoted reviewed-file creation, but recall verification did not pass because the new promoted file was not discoverable through the recall/index layer.

This milestone is an issue capture and remediation plan only.

It does not change runtime behavior.

## M112 Execution Summary

Observed M112 execution state:

```text
Prompt 1 Boundary Check: PASS
Prompt 2 Proposal Draft: PASS with minor path/naming note
Prompt 3 Proposal File Creation: PASS
Prompt 4 Promotion / Recall Verification: PARTIAL / BLOCKED
Overall: BLOCKED pending indexing / recall remediation
```

## What Passed

The following passed:

```text
The session started with read-only / proposal-first preflight.
The agent confirmed workspace freelancer.
The agent confirmed proposal-first persistence.
The proposal draft was produced in response first.
The proposal file was created only after explicit operator approval.
The proposal file was created under forge-inbox.
The promoted reviewed file was created under wiki/freelancer/.
Direct grep marker verification passed for both files.
No secret-bearing content was intentionally written.
```

## What Is Blocked

The following did not pass:

```text
Recall verification for the promoted file returned FAIL.
The new promoted reviewed file was not discoverable through the recall/index layer.
The trial repo contains untracked M112 files.
The promoted file still contains a verification command line referencing the forge-inbox expected path.
```

## Trial Repo Actual State

Trial repo:

```text
~/workspace-trial/hermes-runes-md-wiki
```

Observed untracked files:

```text
?? wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md
?? wiki/freelancer/m112-p0-proposal-first-persistence.md
```

Observed file list:

```text
wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md
wiki/freelancer/forge-inbox/m94-trial-promotion-fixture.md
wiki/freelancer/m112-p0-proposal-first-persistence.md
```

## Proposal / Promoted File State

Forge-inbox proposal file:

```text
path: wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md
status: draft
trust_class: unreviewed
marker: M112 P0 proposal-first persistence marker
```

Promoted reviewed file:

```text
path: wiki/freelancer/m112-p0-proposal-first-persistence.md
status: approved
trust_class: reviewed
marker: M112 P0 proposal-first persistence marker
```

This means the proposal and promoted-file split is visible and consistent at the file level.

## Recall Verification Failure

Observed recall command:

```text
python3 tools/runes/recall_verify_m28_3.py --project freelancer "proposal-first persistence" \
  --expected-path wiki/freelancer/m112-p0-proposal-first-persistence.md \
  --required-marker "M112 P0 proposal-first persistence marker"
```

Observed result:

```text
FAIL / result count: 0
```

Observed explanation from the session:

```text
The new file was not yet indexed into the recall database.
Importer/index behavior did not produce searchable chunks for the new file during this session.
Direct file grep verification still passed.
```

## Direct Marker Verification

Direct grep verification passed:

```text
wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md: marker found
wiki/freelancer/m112-p0-proposal-first-persistence.md: marker found
```

The marker phrase is:

```text
M112 P0 proposal-first persistence marker
```

## Minor Content Issue

The promoted file still contains a verification-plan command pointing to the forge-inbox expected path in the copied content.

Problematic expected-path inside promoted content:

```text
wiki/freelancer/forge-inbox/m112-p0-proposal-first-persistence.md
```

Preferred expected-path for promoted/trusted recall verification:

```text
wiki/freelancer/m112-p0-proposal-first-persistence.md
```

This is a content cleanup issue, not the primary recall failure.

## Governance Assessment

Governance assessment:

```text
Proposal-first behavior: PASS
Explicit approval before proposal file creation: PASS
Separate approval before promotion: PASS
Direct marker existence: PASS
Recall/index verification: FAIL
M112 overall: BLOCKED
```

The M112 workflow should not be marked PASS until recall verification succeeds or the remediation decision explicitly defines an acceptable alternative verification path.

## Remediation Plan

Recommended remediation order:

```text
1. Keep both M112 files uncommitted until remediation is decided.
2. Fix the promoted file's internal verification-plan expected-path.
3. Identify the correct local import/index command for the trial repo and freelancer project.
4. Run import/index in a bounded way for the freelancer workspace only.
5. Re-run recall verification for the promoted reviewed file.
6. If recall PASS, update M112 to PASS and freeze with M113.
7. If recall still FAIL, capture the importer/index failure as a separate tooling issue before continuing broader P0 usage.
```

## Suggested Local Diagnostic Commands

Run these from the trial repo to inspect importer/index availability:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

find bin tools -maxdepth 3 -type f | sort | grep -E "import|index|embed|recall|sync|chunk|smoke"

bash bin/hermes-memory-import --help 2>&1 | head -80 || true
bash bin/hermes-recall --help 2>&1 | head -80 || true
python3 tools/runes/recall_verify_m28_3.py --help 2>&1 | head -80 || true
```

Check whether the promoted file is included in the wiki file scan:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

find wiki/freelancer -maxdepth 2 -type f -name '*.md' | sort
```

After the correct import/index command is identified, re-run recall verification:

```bash
cd ~/workspace-trial/hermes-runes-md-wiki

python3 tools/runes/recall_verify_m28_3.py \
  --project freelancer \
  "proposal-first persistence" \
  --expected-path wiki/freelancer/m112-p0-proposal-first-persistence.md \
  --required-marker "M112 P0 proposal-first persistence marker"
```

## Do Not Do Yet

Do not do these until remediation is clear:

```text
Do not mark M112 PASS.
Do not commit the two M112 trial files yet.
Do not delete the draft proposal file just to hide the issue.
Do not broaden import/index to unrelated workspaces without understanding the command scope.
Do not convert this into an autonomous writer flow.
```

## Decision Needed

Before continuing, decide one of the following:

```text
Path A: Fix importer/index and complete M112 recall verification.
Path B: Record M112 as partial and create a separate importer/index remediation milestone.
Path C: Adjust the first P0 trial-run acceptance criteria to allow file-level verification only, if recall DB is intentionally unavailable in the trial repo.
```

Preferred path:

```text
Path A: Fix importer/index and complete M112 recall verification.
```

## Suggested Next Step

Recommended next milestone:

```text
M112.2 Recall/Index Remediation for First P0 Trial-run
```

Suggested purpose:

```text
Identify and run the correct bounded import/index process so the promoted M112 reviewed file becomes recall-verifiable.
```

If remediation succeeds:

```text
M113 First Practical P0 Trial-run Result Freeze
```

Suggested purpose:

```text
Freeze M112 as the first practical P0 trial-run PASS baseline.
```

## Final Lock

```text
M112.1 P0 Trial-run Issue Capture / Remediation Plan
PASS / M112 issue captured - recall remediation required
```
