# Operations Local Retention Policy

Status:
- M31.6d local retention policy
- `operations/` is local-only
- reports may preserve selected frozen snapshots

Purpose:
`operations/` stores runtime operational evidence such as:
- runes apply records
- runes refresh records
- runes recall verification records
- runes reject records

Policy:
- Do not commit `operations/` to git.
- Keep operation JSON records local for troubleshooting and governance review.
- Preserve selected summarized snapshots under `reports/` when they are useful as frozen milestone evidence.
- Do not ingest raw operation logs into RAG memory by default.
- Do not treat operation logs as trusted wiki source-of-truth.

Rationale:
Operation logs are useful local evidence, but they grow quickly and may contain implementation details or noisy runtime state. The Markdown wiki remains the governed source-of-truth. Reports may capture curated snapshots when needed.
