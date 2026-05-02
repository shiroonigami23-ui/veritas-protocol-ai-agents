import json
import tempfile
import time
import unittest
from pathlib import Path

from veritas.collector.collector import Collector


class TestIteration1Stability(unittest.TestCase):
    def test_collector_multi_session_stability_smoke(self):
        start = time.time()
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            raw = [
                {
                    "monotonic_timestamp_ns": i,
                    "pid": 4000,
                    "tid": 4000,
                    "syscall": "write",
                    "arguments": {"fd": 3, "offset": 0, "data": str(i)},
                    "return_value": 1,
                }
                for i in range(1, 200)
            ]
            raw.append(
                {
                    "monotonic_timestamp_ns": 201,
                    "pid": 4000,
                    "tid": 4000,
                    "syscall": "exit_group",
                    "arguments": {},
                    "return_value": 0,
                }
            )
            in_file = dpath / "trace.json"
            in_file.write_text(json.dumps(raw), encoding="utf-8")

            for idx in range(25):
                out_file = dpath / f"out-{idx}.json"
                collector = Collector()
                result = collector.run_file(str(in_file), str(out_file))
                self.assertEqual(result["captured_event_count"], 2)
                self.assertEqual(len(result["mmr_root"]), 64)

        self.assertLess(time.time() - start, 10)


if __name__ == "__main__":
    unittest.main()

