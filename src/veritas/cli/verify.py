import argparse
import json
from pathlib import Path

from veritas.mock_chain.chain import MockAuditChain

def main():
    parser = argparse.ArgumentParser(description='veritas-verify')
    parser.add_argument('--proof', required=True)
    args = parser.parse_args()

    proof = json.loads(Path(args.proof).read_text(encoding='utf-8'))
    chain = MockAuditChain()
    print(json.dumps(chain.verify_and_attest(proof), indent=2))

if __name__ == '__main__':
    main()
