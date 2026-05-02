import json
import tempfile
import time
import unittest
from pathlib import Path

from veritas.core.prover import prove
from veritas.mock_chain.chain import MockAuditChain

class TestProverFlow(unittest.TestCase):
    def test_iteration0_exit_gate_scenario(self):
        start = time.time()
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            trace = dpath / 'trace.json'
            policy = dpath / 'policy.pdl'
            out = dpath / 'proof.json'
            trace.write_text(json.dumps([
                {"monotonic_timestamp_ns": 1, "pid": 1, "tid": 1, "syscall": "write", "arguments": {"path": "a.py"}, "return_value": 0},
                {"monotonic_timestamp_ns": 2, "pid": 1, "tid": 1, "syscall": "write", "arguments": {"path": "b.py"}, "return_value": 0},
                {"monotonic_timestamp_ns": 3, "pid": 1, "tid": 1, "syscall": "write", "arguments": {"path": "c.py"}, "return_value": 0},
                {"monotonic_timestamp_ns": 4, "pid": 1, "tid": 1, "syscall": "execve", "arguments": {"cmd": "black ."}, "return_value": 0},
                {"monotonic_timestamp_ns": 5, "pid": 1, "tid": 1, "syscall": "execve", "arguments": {"cmd": "pytest -q"}, "return_value": 0}
            ]), encoding='utf-8')
            policy.write_text('allow syscall.write\nallow syscall.execve\n', encoding='utf-8')
            proof = prove(str(trace), str(policy), str(out))
            self.assertTrue(out.exists())
            self.assertEqual(proof['public_inputs']['compliant'], 1)
            chain = MockAuditChain()
            att = chain.verify_and_attest(proof)
            self.assertEqual(att['attestation_id'], 1)
        self.assertLess(time.time() - start, 120)

if __name__ == '__main__':
    unittest.main()
