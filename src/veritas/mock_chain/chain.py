import time

class MockAuditChain:
    def __init__(self):
        self.attestations = []

    def verify_and_attest(self, proof: dict) -> dict:
        if len(proof.get('proof_hash', '')) != 64:
            raise ValueError('proof rejected by mock chain')
        att = {
            'attestation_id': len(self.attestations) + 1,
            'timestamp': int(time.time()),
            'proof_hash': proof['proof_hash'],
            'public_inputs': proof['public_inputs'],
            'submitter': 'local-prover',
        }
        self.attestations.append(att)
        return att
