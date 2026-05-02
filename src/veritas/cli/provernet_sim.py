from __future__ import annotations

import argparse
import json
import sys

from veritas.prover_network.network import ProverJob, ProverNetwork, ProverNode


def main() -> None:
    parser = argparse.ArgumentParser(description="veritas-provernet-sim")
    parser.add_argument("--trace-root", required=True)
    parser.add_argument("--policy-root", required=True)
    parser.add_argument("--trace-size", type=int, default=1000)
    parser.add_argument("--reward", type=int, default=100)
    parser.add_argument("--deadline-epoch", type=int, default=2)
    args = parser.parse_args()

    network = ProverNetwork(
        nodes=[
            ProverNode(node_id="prover-a", stake=1_000, speed_factor=0.9),
            ProverNode(node_id="prover-b", stake=1_000, speed_factor=1.05),
            ProverNode(node_id="prover-c", stake=1_000, speed_factor=1.2),
            ProverNode(node_id="prover-d", stake=1_000, speed_factor=0.8),
        ]
    )
    job = ProverJob(
        trace_root=args.trace_root,
        policy_root=args.policy_root,
        reward=args.reward,
        deadline_epoch=args.deadline_epoch,
        trace_size=args.trace_size,
    )
    network.submit_job(job)
    race = network.run_race()
    segment_proofs = race.all_submissions[:3]
    aggregated = network.aggregate_recursive(segment_proofs)
    cut_result = network.cut_and_choose_verify(
        proof=race.winning_proof,
        expected_trace_root=args.trace_root,
        challenger_ids=["committee-1", "committee-2"],
    )
    result = {
        "winner": race.winner,
        "p95_proof_time_seconds": round(race.p95_proof_time, 3),
        "aggregated": aggregated,
        "cut_and_choose": cut_result,
    }
    sys.stdout.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()

