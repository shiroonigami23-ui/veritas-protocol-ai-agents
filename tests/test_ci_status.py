import json
import tempfile
import unittest
from pathlib import Path

from veritas.ci.status import write_status_artifact


class TestCIStatus(unittest.TestCase):
    def test_status_verified(self):
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            p = dpath / "proof.json"
            p.write_text(
                json.dumps(
                    {
                        "proof": {"proof_hash": "b" * 64, "public_inputs": {"compliant": 1}},
                        "attestation": {"attestation_id": 9},
                    }
                ),
                encoding="utf-8",
            )
            out = dpath / "status.json"
            art = write_status_artifact(str(p), str(out))
            self.assertTrue(art["verified"])
            self.assertIn("Verified by Veritas", art["status_line"])


if __name__ == "__main__":
    unittest.main()
