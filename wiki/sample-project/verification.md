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
