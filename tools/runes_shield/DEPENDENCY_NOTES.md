# Runtime Dependency Notes — tools/runes_shield

This file records runtime dependencies that were copied from `dev/` so that
`tools/runes_shield/` remains self-contained and does not import from `dev/`.

`dev/` is developer-only (see `dev/README.md`); general deployments and
agents must only use `tools/runes_shield/`.

When updating any file listed below, keep the runtime copy in sync with its
`dev/` source.

## Source mapping

| Runtime path (tools/runes_shield/) | dev source path | Notes |
|---|---|---|
| `validate_proposal_fixture.py` | `dev/tools/runes_shield/validation/validate_proposal_fixture.py` | Path-aware validator used by the proposal registry / review queue CLIs. `ROOT = parents[2]` resolves to the repo root only when located under `tools/runes_shield/`; the dev copy lives one level deeper, so the runtime copy is the canonical runtime dependency. |
| `fixtures/proposal_draft_m37_2_valid.json` | `dev/tools/runes_shield/fixtures/proposal_draft_m37_2_valid.json` | Valid M37.2 sample. |
| `fixtures/proposal_draft_m37_3_negative_blocked_status.json` | `dev/tools/runes_shield/fixtures/proposal_draft_m37_3_negative_blocked_status.json` | Negative sample: blocked status. |
| `fixtures/proposal_draft_m37_3_negative_missing_field.json` | `dev/tools/runes_shield/fixtures/proposal_draft_m37_3_negative_missing_field.json` | Negative sample: missing field. |
| `fixtures/proposal_draft_m37_3_negative_wrong_role.json` | `dev/tools/runes_shield/fixtures/proposal_draft_m37_3_negative_wrong_role.json` | Negative sample: wrong role. |

## Background

- Commit `e1cb587` ("Move Runes Shield development assets under dev") moved the
  validator, fixtures, smoke, regression and trial assets under `dev/`, but the
  runtime CLIs in `tools/runes_shield/` (`build_proposal_manifest.py`,
  `build_proposal_draft.py`, `proposal_draft_store.py`) continued to import
  `validate_proposal_fixture` from the same directory, breaking the read-only
  tools (`proposal_registry.py`, `proposal_review_queue.py`).
- This directory now ships the validator and fixtures so the read-only tools
  work for general deployments without importing `dev/`.
- Smoke / regression / trial scripts remain in `dev/` as developer-only assets
  and were removed from `runes_shield_tools_index.json`.
