#!/usr/bin/env python3

from smoke_proposal_apply_preview import main as run_preview_smoke
from smoke_proposal_apply_preview_variants import main as run_preview_variants_smoke


def main():
    print("== M45.2 Proposal Apply Preview Aggregator Smoke ==")

    run_preview_smoke()
    run_preview_variants_smoke()

    print("PASS: proposal apply preview aggregator regression completed")


if __name__ == "__main__":
    main()
