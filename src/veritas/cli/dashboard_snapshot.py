from __future__ import annotations

import argparse
import json
import sys

from veritas.dashboard.snapshot import build_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-dashboard-snapshot")
    parser.add_argument("--proof", required=True)
    parser.add_argument("--collector", default="")
    parser.add_argument("--out", default="dashboard-snapshot.json")
    args = parser.parse_args()
    snap = build_snapshot(args.proof, args.collector or None, args.out)
    sys.stdout.write(json.dumps(snap, indent=2) + "\n")


if __name__ == "__main__":
    main()
