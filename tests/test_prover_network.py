import unittest

from veritas.prover_network.network import ProverJob, ProverNetwork, ProverNode


class TestProverNetwork(unittest.TestCase):
    def test_race_and_aggregation(self):
        n = ProverNetwork(
            nodes=[
                ProverNode("n1", stake=1000, speed_factor=1.0),
                ProverNode("n2", stake=1000, speed_factor=0.8),
                ProverNode("n3", stake=1000, speed_factor=1.2),
            ]
        )
        n.submit_job(ProverJob("tr", "pr", 100, 2, 1200))
        race = n.run_race(seed=3)
        self.assertIn(race.winner, {"n1", "n2", "n3"})
        agg = n.aggregate_recursive(race.all_submissions[:2])
        self.assertEqual(agg["proof_type"], "mock-recursive-snark")
        self.assertEqual(agg["segment_count"], 2)

    def test_cut_and_choose_slashing(self):
        n = ProverNetwork(nodes=[ProverNode("n1", stake=1000, speed_factor=1.0)])
        bad_proof = {
            "node_id": "n1",
            "trace_root": "fake-root",
            "policy_root": "p",
            "proof_hash": "x" * 64,
            "proof_time": 2.0,
            "compliant": 1,
        }
        result = n.cut_and_choose_verify(
            proof=bad_proof,
            expected_trace_root="true-root",
            challenger_ids=["c1", "c2"],
            slash_ratio=0.1,
        )
        self.assertTrue(result["fraud_detected"])
        self.assertEqual(n.nodes[0].stake, 900)


if __name__ == "__main__":
    unittest.main()

