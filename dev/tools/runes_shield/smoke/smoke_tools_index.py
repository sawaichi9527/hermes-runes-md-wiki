#!/usr/bin/env python3

from validate_tools_index import main as run_validator


def main():
    print("== M40 Runes Shield Tool Index Smoke ==")

    run_validator()

    print("PASS: Runes Shield tool index regression completed")


if __name__ == "__main__":
    main()
