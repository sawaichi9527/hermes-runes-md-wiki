# Trial Observation Record: <short title>

## Metadata

- Trial ID: trial-YYYYMMDD-<short-slug>
- Date: YYYY-MM-DD
- Project: k6-freelancer
- Status: draft
- Scope: personal-local controlled trial-use observation
- Candidate type: <project-memory|decision|baseline|service-note|verification-note|other>
- Source type: <user-provided|local-file|repo-doc|manual-note|other>
- Target Markdown path: wiki/<workspace-slug>/<target-file>.md
- Review owner: human

---

## Candidate Summary

Briefly describe the memory candidate in 3-5 lines.

Keep this small. This trial should observe one candidate, not perform bulk ingestion.

---

## Source Reference

Record the source reference without copying secrets.

Allowed examples:

```text
- user-provided summary in current conversation
- local non-secret document path
- repository document path
- manually curated note
```

Do not include:

```text
.env contents
API keys
PostgreSQL passwords
Telegram tokens
private credentials
```

---

## Target Markdown Path

Proposed target:

```text
wiki/<workspace-slug>/<target-file>.md
```

If the workspace does not exist, do not create it directly. Prepare a governed workspace proposal instead.

---

## Proposed Memory Content

Draft the candidate memory content here.

Use Markdown-native structure compatible with the target file.

---

## Governance Checks

- [ ] Candidate is small and bounded.
- [ ] Source reference is known.
- [ ] No secrets are included.
- [ ] Target path is explicit.
- [ ] Existing workspace status is checked.
- [ ] Direct wiki mutation is not performed without governed approval.
- [ ] Backend guard is PASS before import / recall / smoke.
- [ ] Manual human review is required before final apply.

---

## Manual Review

Human review decision:

```text
pending / approved / rejected / needs-revision
```

Reviewer notes:

```text
<notes>
```

---

## Manual Record

Record what was manually applied, if anything.

```text
No apply performed yet.
```

If applied, include:

```text
- target file changed:
- summary of change:
- command or manual edit method:
- timestamp:
```

---

## Post-change Verification

Do not mark PASS until verification is complete.

Suggested checks:

```bash
bash ./bin/hermes-backend-check
bash ./bin/hermes-memory-migrate
./bin/hermes-memory-smoke
```

If importer / recall verification is relevant, record the command and observed result.

---

## Observation Notes

Record what was learned from this trial.

Focus on:

```text
clarity of agent instructions
proposal / review friction
target path ambiguity
backend guard usefulness
manual apply usability
retrieval / recall behavior
```

---

## Final Status

```text
DRAFT / BLOCKED / REJECTED / APPLIED / PASS
```

Final lock, if verified:

```text
Trial <trial-id>
PASS / manually reviewed / post-change verified
```
