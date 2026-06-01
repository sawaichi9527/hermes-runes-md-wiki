# Sample Project Verification

## V-001: Import Smoke Test

Status: PASS

Verified:
- Sample Markdown files can be imported.
- The importer can create chunks.
- Public-safe sample content is suitable for retrieval testing.

---

## V-002: Retrieval Smoke Test

Status: PASS

Query:
- Markdown source-of-truth

Expected:
- The system should retrieve the decision explaining why Markdown is used as source-of-truth.

---

## V-003: Secret Policy Smoke Test

Status: PASS

Query:
- secrets API keys passwords

Expected:
- The system should retrieve the decision that real secrets must not be stored in Markdown memory.

---

## V-004: M15 Forge Writer Safety Baseline

Status: PASS

Scope:
- M15.4b lock + manifest helper
- M15.5 create-flat dry-run planner
- M15.6a pre-write guard
- M15.6b real-write switch guard
- M15.6c sample-project first real write
- M15.6d duplicate-path guard smoke

Verified:
- Operation IDs are generated for forge actions.
- Manifest writer records planned operations.
- File lock helper prevents overlapping writer ownership.
- `create-flat` defaults to dry-run behavior.
- `--execute` alone does not enable real writes.
- `--execute --allow-real-write` is required for real-write intent.
- Real-write is currently restricted to `sample-project` only.
- `k6-freelancer` is not enabled for real-write forge operations.
- The first sample real-write created `wiki/sample-project/project-first-real-write-overview.md`.
- Duplicate-path protection blocks a second write to the same planned path.
- Index update remains disabled during M15.6.

Safety Notes:
- M15.6 real-write is intentionally limited to sample content.
- Real project namespaces must remain guarded until a separate enablement milestone.
- Forge writer must not ingest generated manifests into RAG memory automatically.
