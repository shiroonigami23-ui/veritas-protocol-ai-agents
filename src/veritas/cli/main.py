import argparse
import json
import sys
from pathlib import Path

from veritas.core.prover import prove
from veritas.mock_chain.chain import MockAuditChain

def main():
    parser = argparse.ArgumentParser(description='veritas-prove')
    parser.add_argument('--trace', required=True)
    parser.add_argument('--policy', required=True)
    parser.add_argument('--out', default='proof.json')
    parser.add_argument('--anchor', action='store_true')
    parser.add_argument('--bundle-out', default='')
    args = parser.parse_args()

    proof = prove(args.trace, args.policy, args.out)
    output = {'proof': proof}
    if args.anchor:
        chain = MockAuditChain()
        output['attestation'] = chain.verify_and_attest(proof)
    if args.bundle_out:
        Path(args.bundle_out).write_text(json.dumps(output, indent=2), encoding="utf-8")
    sys.stdout.write(json.dumps(output, indent=2) + '\n')

if __name__ == '__main__':
    main()
