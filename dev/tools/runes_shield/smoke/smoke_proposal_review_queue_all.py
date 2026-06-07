#!/usr/bin/env python3

from smoke_proposal_review_queue import main as run_review_queue_smoke
from smoke_proposal_review_queue_payload import main as run_review_queue_payload_smoke


def main():
    print("== M39.2 Proposal Review Queue Aggregator Smoke ==")

    run_review_queue_smoke()
    run_review_queue_payload_smoke()

    print("PASS: proposal review queue aggregator regression completed")


if __name__ == "__main__":
    main()
