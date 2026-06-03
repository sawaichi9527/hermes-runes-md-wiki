#!/usr/bin/env python3

from smoke_attunement_decision import main as run_decision_smoke
from smoke_attunement_decision_store import main as run_decision_store_smoke


def main():
    print("== M42.2 Human Attunement Decision Aggregator Smoke ==")

    run_decision_smoke()
    run_decision_store_smoke()

    print("PASS: human attunement decision aggregator regression completed")


if __name__ == "__main__":
    main()
