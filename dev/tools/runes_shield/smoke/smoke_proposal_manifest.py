#!/usr/bin/env python3

import json

from build_proposal_manifest import build_manifest


EXPECTED_FIXTURE_COUNT = 4


def main():
    print("== M38 Proposal Manifest Smoke ==")

    manifest = build_manifest()

    print(json.dumps(manifest, indent=2, ensure_ascii=False))

    if manifest["manifest_version"] != "m38-proposal-registry-v1":
        raise SystemExit("unexpected manifest version")

    if manifest["write"] is not False:
        raise SystemExit("manifest must remain read-only")

    if manifest["entry_count"] < EXPECTED_FIXTURE_COUNT:
        raise SystemExit("proposal fixture count below expected minimum")

    failing_entries = [
        entry
        for entry in manifest["entries"]
        if entry["validation_status"] == "FAIL"
    ]

    if len(failing_entries) < 3:
        raise SystemExit("negative fixtures missing from manifest")

    print("PASS: proposal manifest regression completed")


if __name__ == "__main__":
    main()
