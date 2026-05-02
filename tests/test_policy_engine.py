import json
import tempfile
import unittest
from pathlib import Path

from veritas.core.policy_engine import compose_policies, dry_run


class TestPolicyEngine(unittest.TestCase):
    def test_policy_composition_union(self):
        c = compose_policies(["allow syscall.write\n", "deny syscall.execve\n"])
        self.assertIn("policy_root", c)
        self.assertGreaterEqual(len(c["constraints"]), 2)

    def test_policy_dryrun_report(self):
        with tempfile.TemporaryDirectory() as d:
            dpath = Path(d)
            p1 = dpath / "org.pdl"
            p2 = dpath / "repo.pdl"
            trace = dpath / "trace.json"
            out = dpath / "report.json"
            p1.write_text("allow syscall.write\n", encoding="utf-8")
            p2.write_text("deny syscall.execve\n", encoding="utf-8")
            trace.write_text(
                json.dumps(
                    [
                        {
                            "monotonic_timestamp_ns": 1,
                            "pid": 1,
                            "tid": 1,
                            "syscall": "write",
                            "arguments": {"path": "a.py"},
                            "return_value": 1,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            report = dry_run([str(p1), str(p2)], [str(trace)], str(out))
            self.assertTrue(report["results"][0]["compliant"])
            self.assertTrue(out.exists())


if __name__ == "__main__":
    unittest.main()

