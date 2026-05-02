from __future__ import annotations

import json
import statistics
import time

from veritas.prover_network.network import ProverJob, ProverNetwork, ProverNode


def main() -> None:
    network = ProverNetwork(
        nodes=[
            ProverNode("p1", 1000, 0.85),
            ProverNode("p2", 1000, 1.00),
            ProverNode("p3", 1000, 1.10),
            ProverNode("p4", 1000, 0.90),
            ProverNode("p5", 1000, 1.20),
        ]
    )
    p95_samples: list[float] = []
    start = time.time()
    for i in range(200):
        job = ProverJob(
            trace_root=f"trace-{i}",
            policy_root="policy-root",
            reward=100,
            deadline_epoch=2,
            trace_size=1000 + (i % 80) * 20,
        )
        network.submit_job(job)
        race = network.run_race(seed=i + 5)
        p95_samples.append(race.p95_proof_time)
    report = {
        "sessions": len(p95_samples),
        "p95_of_p95_seconds": round(sorted(p95_samples)[int(len(p95_samples) * 0.95) - 1], 3),
        "avg_p95_seconds": round(statistics.mean(p95_samples), 3),
        "duration_seconds": round(time.time() - start, 3),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

