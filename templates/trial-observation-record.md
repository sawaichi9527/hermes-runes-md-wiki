# Trial Observation Record: <short title>

## Metadata

- Trial ID: trial-YYYYMMDD-<short-slug>
- Date: YYYY-MM-DD
- Project: freelancer
- Workspace slug: freelancer
- Status: draft
- Scope: personal-local controlled trial-use observation
- Candidate type: <project-memory|decision|baseline|service-note|verification-note|other>
- Source type: <user-provided|local-file|repo-doc|manual-note|other>
- Target Markdown path: wiki/freelancer/<target-file>.md
- Review owner: human

---

## Candidate Summary

Briefly describe the memory candidate in 3-5 lines.

Keep this small. This trial should observe one candidate, not perform bulk ingestion.

---

## Source Reference

Record the source reference without copying local-only values.

Allowed examples:

```text
- user-provided summary in current conversation
- local non-secret document path
- repository document path
- manually curated note
```

Do not include local credentials or private runtime values.

---

## Target Markdown Path

Proposed target:

```text
wiki/freelancer/<target-file>.md
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
- [ ] No local-only private values are included.
- [ ] Target path is explicit.
- [ ] Existing workspace status is checked.
- [ ] Direct wiki mutation is not performed without governed approval.
- [ ] Backend guard is PASS before import / recall / smoke.
- [ ] Manual human review is required before final apply.
