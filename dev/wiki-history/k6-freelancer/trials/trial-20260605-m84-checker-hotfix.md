# Trial Observation Record: M84 checker false-positive hotfix

## Metadata

- Trial ID: trial-20260605-m84-checker-hotfix
- Date: 2026-06-05
- Project: k6-freelancer
- Status: PASS
- Scope: personal-local controlled trial-use observation
- Candidate type: verification-note
- Source type: user-provided terminal result
- Target Markdown path: `bin/hermes-trial-observation-check`
- Review owner: human

---

## Candidate Summary

The first controlled trial-use observation used a real M84 issue discovered during local verification.

The trial observation checker incorrectly flagged safety guidance text in the template as a possible secret marker.

The false positive occurred because the template included words such as PostgreSQL passwords and Telegram tokens in a prohibited-items explanation, without containing actual secret values.

The checker was updated to look for obvious secret values rather than generic safety wording.

---

## Source Reference

Source evidence was the user-provided terminal result from Freelancer host:

```text
bash ./bin/hermes-trial-observation-check \
  wiki/k6-freelancer/trials/trial-20260605-test.md

43:PostgreSQL passwords
44:Telegram tokens
{"status":"BLOCKED_POSSIBLE_SECRET_MARKER","check":"trial-observation","file":"wiki/k6-freelancer/trials/trial-20260605-test.md","message":"Possible secret marker found. Review manually before proceeding."}
```

Post-fix user verification:

```text
{"status":"PASS","check":"trial-observation","file":"wiki/k6-freelancer/trials/trial-20260605-test.md","message":"Trial observation record structure is ready for human review."}
```

No secrets were included in the source evidence.

---

## Target Markdown Path

Target implementation path:

```text
bin/hermes-trial-observation-check
```

Related trial scaffold paths:

```text
docs/trial-use-observation.md
templates/trial-observation-record.md
wiki/k6-freelancer/verification-m84.md
```

---

## Proposed Memory Content

The M84 trial observation checker should avoid flagging generic security guidance text as a secret.

It should focus on likely secret values or high-signal secret formats, such as:

```text
PASSWORD=...
token: ...
postgresql://user:pass@host/db
BEGIN PRIVATE KEY
ghp_...
xoxb-...
```

The checker remains intentionally shallow and personal-use scoped. It is not a full enterprise secret scanner.

---

## Governance Checks

- [x] Candidate is small and bounded.
- [x] Source reference is known.
- [x] No secrets are included.
- [x] Target path is explicit.
- [x] Existing workspace status is checked.
- [x] Direct wiki mutation is not performed without governed approval.
- [x] Backend guard is not required for this read-only checker hotfix.
- [x] Manual human review is required before final apply.

---

## Manual Review

Human review decision:

```text
approved
```

Reviewer notes:

```text
The false positive was caused by the template's safety wording, not by an actual secret value.
The fix should keep the checker low-noise and value-oriented.
```

---

## Manual Record

Applied change:

```text
Target file changed:
- bin/hermes-trial-observation-check

Summary of change:
- Replace broad secret-word matching with value-oriented secret marker matching.
- Avoid matching safety guidance text such as PostgreSQL passwords and Telegram tokens.

Commit:
- ac49792 Fix trial observation secret scan false positives
```

---

## Post-change Verification

Verified on Freelancer host:

```bash
cd ~/workspace/hermes-runes-md-wiki

git restore bin/hermes-trial-observation-check
git pull
chmod +x bin/hermes-trial-observation-check
bash -n bin/hermes-trial-observation-check
bash ./bin/hermes-trial-observation-check \
  wiki/k6-freelancer/trials/trial-20260605-test.md
```

Observed result:

```json
{"status":"PASS","check":"trial-observation","file":"wiki/k6-freelancer/trials/trial-20260605-test.md","message":"Trial observation record structure is ready for human review."}
```

---

## Observation Notes

This trial confirmed that the controlled observation scaffold can capture a real small issue without expanding system complexity.

Useful observations:

```text
- The checker should be low-noise because it is meant to support human review, not replace it.
- Documentation templates may contain security vocabulary and should not be treated as secrets by default.
- The trial record format is sufficient for capturing source, target, manual review, applied change, and verification result.
- The process remained personal-local and did not require queueing, background work, or enterprise secret scanning.
```

---

## Final Status

```text
PASS
```

Final lock:

```text
Trial trial-20260605-m84-checker-hotfix
PASS / manually reviewed / post-change verified
```
