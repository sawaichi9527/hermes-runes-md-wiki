#!/usr/bin/env python3

from smoke_proposal_apply_execute import main as run_execute_smoke
from smoke_proposal_apply_execute_variants import (
    main as run_execute_variants_smoke,
)


def main():
    print("== M46.2 Apply Execution Boundary Aggregator Smoke ==")

    run_execute_smoke()
    run_execute_variants_smoke()

    print("PASS: apply execution boundary aggregator regression completed")


if __name__ == "__main__":
    main()
