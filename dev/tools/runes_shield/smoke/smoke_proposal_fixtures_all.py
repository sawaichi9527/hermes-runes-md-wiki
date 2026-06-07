#!/usr/bin/env python3

from smoke_proposal_fixture import main as run_positive_smoke
from smoke_proposal_negative_fixtures import main as run_negative_smoke


def main():
    print("== M37.4 Proposal Fixtures Aggregator Smoke ==")

    run_positive_smoke()
    run_negative_smoke()

    print("PASS: proposal fixture aggregator regression completed")


if __name__ == "__main__":
    main()
