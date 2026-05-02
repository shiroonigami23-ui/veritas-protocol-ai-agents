import json
import tempfile
import unittest
from pathlib import Path

from veritas.compliance.vcc import build_vcc, verify_vcc


class TestVCC(unittest.TestCase):
    def test_build_and_verify_vcc(self):
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            ws = dpath / "ws"
            ws.mkdir()
            (ws / "a.py").write_text("print('a')\\n", encoding="utf-8")
            (ws / "b.py").write_text("print('b')\\n", encoding="utf-8")
            proof = dpath / "proof.json"
            proof.write_text(
                json.dumps(
                    {
                        "proof": {
                            "proof_hash": "a" * 64,
                            "public_inputs": {
                                "session_uuid": "s1",
                                "trace_root": "t1",
                                "policy_root": "p1",
                                "compliant": 1,
                            },
                        },
                        "attestation": {"attestation_id": 3},
                    }
                ),
                encoding="utf-8",
            )
            out = dpath / "vcc.json"
            vcc = build_vcc(str(proof), str(ws), "a.py", str(out))
            self.assertEqual(vcc["module_path"], "a.py")
            ver = verify_vcc(str(out))
            self.assertTrue(ver["valid"])


if __name__ == "__main__":
    unittest.main()
