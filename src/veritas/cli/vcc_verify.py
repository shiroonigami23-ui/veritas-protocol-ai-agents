from __future__ import annotations

import argparse
import json
import sys

from veritas.compliance.vcc import verify_vcc


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-vcc-verify")
    parser.add_argument("--vcc", required=True)
    args = parser.parse_args()
    result = verify_vcc(args.vcc)
    sys.stdout.write(json.dumps(result, indent=2) + "\n")
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
