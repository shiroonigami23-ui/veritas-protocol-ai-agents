import json
import tempfile
import unittest
from pathlib import Path

from veritas.dashboard.snapshot import build_snapshot


class TestDashboardSnapshot(unittest.TestCase):
    def test_build_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            proof = dpath / "proof.json"
            proof.write_text(
                json.dumps(
                    {
                        "proof": {
                            "proof_hash": "c" * 64,
                            "public_inputs": {
                                "session_uuid": "s1",
                                "trace_root": "tr",
                                "policy_root": "pr",
                                "compliant": 1,
                            },
                        },
                        "attestation": {"attestation_id": 7},
                    }
                ),
                encoding="utf-8",
            )
            collector = dpath / "collector.json"
            collector.write_text(
                json.dumps({"captured_event_count": 12, "mmr_root": "m" * 64}),
                encoding="utf-8",
            )
            out = dpath / "snapshot.json"
            snap = build_snapshot(str(proof), str(collector), str(out))
            self.assertEqual(snap["attestation_id"], 7)
            self.assertEqual(snap["collector"]["captured_event_count"], 12)


if __name__ == "__main__":
    unittest.main()
