from __future__ import annotations

import argparse
import json
import sys

from veritas.collector.collector import Collector, CollectorAbort


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-collectord")
    parser.add_argument("--trace", required=True, help="Raw syscall-like trace JSON")
    parser.add_argument("--out", default="collector-session.json", help="Collector output JSON")
    args = parser.parse_args()

    collector = Collector()
    try:
        result = collector.run_file(args.trace, args.out)
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    except CollectorAbort:
        sys.exit(2)


if __name__ == "__main__":
    main()

