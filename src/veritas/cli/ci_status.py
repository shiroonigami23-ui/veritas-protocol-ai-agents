from __future__ import annotations

import argparse
import json
import sys

from veritas.ci.status import write_status_artifact


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-ci-status")
    parser.add_argument("--proof", required=True)
    parser.add_argument("--out", default="veritas-status.json")
    args = parser.parse_args()
    artifact = write_status_artifact(args.proof, args.out)
    sys.stdout.write(json.dumps(artifact, indent=2) + "\n")


if __name__ == "__main__":
    main()
