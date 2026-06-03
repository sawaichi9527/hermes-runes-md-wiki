#!/usr/bin/env python3

from smoke_build_proposal_draft import main as run_dry_run_smoke
from smoke_build_proposal_draft_write import main as run_write_draft_smoke
from smoke_manifest_draft_integration import main as run_manifest_integration_smoke
from smoke_proposal_draft_store import main as run_draft_store_smoke


def main():
    print("== M41.4 Proposal Draft Aggregator Smoke ==")

    run_dry_run_smoke()
    run_write_draft_smoke()
    run_manifest_integration_smoke()
    run_draft_store_smoke()

    print("PASS: proposal draft aggregator regression completed")


if __name__ == "__main__":
    main()
