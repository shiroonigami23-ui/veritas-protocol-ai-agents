from __future__ import annotations

import argparse
import json
import sys

from veritas.core.policy_engine import dry_run


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-policy-dryrun")
    parser.add_argument("--policy", action="append", required=True, help="PDL policy file (repeatable)")
    parser.add_argument("--trace", action="append", required=True, help="Trace file (repeatable)")
    parser.add_argument("--out", default="policy-dryrun-report.json")
    args = parser.parse_args()
    report = dry_run(args.policy, args.trace, args.out)
    sys.stdout.write(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()

