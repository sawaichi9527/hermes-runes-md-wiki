# Public Download Content Audit

Status: PASS / AUDIT COMPLETE / TAG BLOCKED BY REMAINING PUBLIC-FACING LEGACY REFERENCES
Date: 2026-06-07
Milestone: M209

## Purpose

Audit repository content before inviting Open Beta testers or creating the first beta tag.

M209 does not try to rewrite all historical records. It classifies remaining legacy references so the next remediation step can focus on what public testers may actually touch.

## Baseline From M208

```text
canonical_active_slug: freelancer
canonical_wiki_namespace: wiki/freelancer/
main_checkout: ~/workspace/hermes-runes-md-wiki
clean_trial_checkout: ~/workspace/trial/hermes-runes-md-wiki
legacy_engineering_namespace: wiki/k6-freelancer/
deprecated_trial_checkout: ~/workspace-trial/hermes-runes-md-wiki
```

## Audit Result

```text
result: PASS for audit completion
release_tag_ready: no
public_tester_notification_ready: no
reason: remaining public-facing and active-tool legacy references require triage/remediation
```

## Classification Rules

```text
A. Active blocker
   Runtime defaults, public starter commands, public templates, or active tools that a tester may execute.

B. Public docs warning
   Public-facing docs that mention legacy names but can be fixed by clear notes or updated examples.

C. Historical evidence allowed
   Frozen verification records, closed beta sessions, historical bug records, and project evidence.

D. Archive/report/tmp allowed or excluded from starter path
   Archive, reports, backups, tmp, and generated evidence that should not drive public onboarding.
```

## A. Active Blockers Found

```text
Some active tools and smoke/eval files still default to or test against k6-freelancer.
Examples include tools/importer/*, tools/runes/*, smoke/*, and config-adjacent examples.

These may be valid legacy tests, but public tester paths must not accidentally default to k6-freelancer.
```

Required handling:

```text
M210 or follow-up remediation must either:
- switch active public defaults to freelancer, or
- clearly mark legacy-only commands, or
- move old examples under archive / legacy docs.
```

## B. Public Docs / Template Warnings Found

```text
Several docs and templates still mention ~/workspace-trial/hermes-runes-md-wiki or wiki/k6-freelancer.
These are confusing for fresh public testers because M208 changed the expected clean trial path to ~/workspace/trial/hermes-runes-md-wiki and active slug to freelancer.
```

Required handling:

```text
Update public-facing starter docs and templates before tag.
Historical prompt packs may remain if clearly labeled as legacy closed-beta evidence.
```

## C. Historical Evidence Allowed

```text
wiki/k6-freelancer/ contains substantial engineering history, milestone locks, verification records, trial records, and closed beta evidence.
These records may keep historical paths because changing them would corrupt evidence provenance.
```

Policy:

```text
Do not bulk-edit historical verification evidence only to rename old paths.
Keep the namespace as legacy engineering history.
Use docs/workspace-slug-policy.md to explain why it exists.
```

## D. Archive / Reports / Backups / Tmp

```text
archive/
reports/
backups/
tmp/
var/operations/
```

These paths may contain old names as provenance or generated evidence.
They should not be used as public Open Beta onboarding material.

## Public Tag Gate

```text
v0.1.0-beta.1 tag_status: blocked
blocker_type: public-facing legacy reference remediation
next_step: M210 Public Download Remediation / Starter Path Cleanup
```

## Final Lock

```text
M209 Public Download Content Audit
PASS / audit complete / tag blocked until public-facing legacy references are remediated
```
