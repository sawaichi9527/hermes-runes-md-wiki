#!/usr/bin/env python3

from smoke_proposal_manifest import main as run_manifest_smoke
from smoke_proposal_registry import main as run_registry_list_smoke
from smoke_proposal_registry_show import main as run_registry_show_smoke
from smoke_proposal_registry_payload import main as run_registry_payload_smoke


def main():
    print("== M38.4 Proposal Registry Aggregator Smoke ==")

    run_manifest_smoke()
    run_registry_list_smoke()
    run_registry_show_smoke()
    run_registry_payload_smoke()

    print("PASS: proposal registry aggregator regression completed")


if __name__ == "__main__":
    main()
