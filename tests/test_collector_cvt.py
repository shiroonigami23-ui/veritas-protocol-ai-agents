import json
import tempfile
import unittest
from pathlib import Path

from veritas.collector.collector import CAPTURE_SYSCALLS, Collector, CollectorAbort
from veritas.collector.mmr import MerkleMountainRange


class TestCollectorCVT(unittest.TestCase):
    def test_fr_coll_2_deterministic_capture_tuple(self):
        collector = Collector()
        ev = collector.canonicalize(
            {
                "monotonic_timestamp_ns": 1,
                "pid": 7,
                "tid": 8,
                "syscall": "execve",
                "arguments": {"cmd": "pytest -q"},
                "return_value": 0,
            }
        )
        self.assertIsNotNone(ev)
        self.assertEqual(ev.sequence_number, 1)
        self.assertEqual(ev.syscall, "execve")
        self.assertEqual(len(ev.arguments_hash), 64)
        self.assertIn(ev.syscall, CAPTURE_SYSCALLS)

    def test_fr_coll_3_intent_dedup(self):
        collector = Collector()
        raw = json.loads(
            Path("examples/session_trace_iteration1.json").read_text(encoding="utf-8")
        )
        out = collector.process_events(raw)
        syscalls = [e["syscall"] for e in out["events"]]
        write_count = sum(1 for s in syscalls if s == "write")
        self.assertEqual(write_count, 1)
        self.assertGreaterEqual(len(out["events"]), 2)

    def test_fr_coll_4_mmr_api(self):
        mmr = MerkleMountainRange()
        i0 = mmr.append("a" * 64)
        i1 = mmr.append("b" * 64)
        root = mmr.finalize()
        proof = mmr.get_proof(i1)
        self.assertEqual(i0, 0)
        self.assertEqual(proof.index, 1)
        self.assertEqual(len(root), 64)
        self.assertGreaterEqual(len(proof.siblings), 1)

    def test_fr_coll_6_graceful_abort(self):
        collector = Collector()
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            in_file = dpath / "bad.json"
            out_file = dpath / "collector-out.json"
            in_file.write_text("{ this is not valid json", encoding="utf-8")
            with self.assertRaises(CollectorAbort):
                collector.run_file(str(in_file), str(out_file))
            payload = json.loads(out_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "SessionAborted")
            self.assertIn("partial_mmr_root", payload)


if __name__ == "__main__":
    unittest.main()

