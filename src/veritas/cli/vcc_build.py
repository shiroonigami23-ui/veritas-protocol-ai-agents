from __future__ import annotations

import argparse
import json
import sys

from veritas.compliance.vcc import build_vcc


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-vcc-build")
    parser.add_argument("--proof", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--module", required=True)
    parser.add_argument("--out", default="vcc.json")
    args = parser.parse_args()
    result = build_vcc(args.proof, args.workspace, args.module, args.out)
    sys.stdout.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
