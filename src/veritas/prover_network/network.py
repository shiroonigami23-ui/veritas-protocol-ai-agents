from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass, field


@dataclass(slots=True)
class ProverJob:
    trace_root: str
    policy_root: str
    reward: int
    deadline_epoch: int
    trace_size: int


@dataclass(slots=True)
class ProverNode:
    node_id: str
    stake: int
    speed_factor: float
    slashed: int = 0

    def prove(self, job: ProverJob) -> dict:
        # Lower is faster; speed factor approximates hardware profile.
        proof_time = max(1.0, (job.trace_size / 40.0) * self.speed_factor)
        digest = hashlib.blake2s(
            f"{self.node_id}:{job.trace_root}:{job.policy_root}".encode("utf-8")
        ).hexdigest()
        return {
            "node_id": self.node_id,
            "proof_hash": digest,
            "proof_time": proof_time,
            "trace_root": job.trace_root,
            "policy_root": job.policy_root,
            "compliant": 1,
        }


@dataclass(slots=True)
class RaceResult:
    winner: str
    winning_proof: dict
    all_submissions: list[dict]
    p95_proof_time: float


@dataclass(slots=True)
class ProverNetwork:
    nodes: list[ProverNode] = field(default_factory=list)
    mempool: list[ProverJob] = field(default_factory=list)

    def submit_job(self, job: ProverJob) -> None:
        self.mempool.append(job)

    def run_race(self, seed: int = 7) -> RaceResult:
        if not self.mempool:
            raise ValueError("no jobs in mempool")
        random.seed(seed)
        job = self.mempool.pop(0)
        submissions: list[dict] = []
        for n in self.nodes:
            p = n.prove(job)
            # Small jitter to model network variation.
            p["proof_time"] += random.random() * 0.8
            submissions.append(p)
        submissions.sort(key=lambda x: x["proof_time"])
        p95_idx = max(0, int(len(submissions) * 0.95) - 1)
        return RaceResult(
            winner=submissions[0]["node_id"],
            winning_proof=submissions[0],
            all_submissions=submissions,
            p95_proof_time=submissions[p95_idx]["proof_time"],
        )

    def aggregate_recursive(self, segment_proofs: list[dict]) -> dict:
        # Constant-size digest abstraction for recursive SNARK aggregation.
        packed = json.dumps(
            [{"node_id": p["node_id"], "proof_hash": p["proof_hash"]} for p in segment_proofs],
            sort_keys=True,
        ).encode("utf-8")
        return {
            "proof_type": "mock-recursive-snark",
            "segment_count": len(segment_proofs),
            "aggregated_proof_hash": hashlib.blake2s(packed).hexdigest(),
            "cost_model": "sublinear-log",
        }

    def cut_and_choose_verify(
        self, proof: dict, expected_trace_root: str, challenger_ids: list[str], slash_ratio: float = 0.1
    ) -> dict:
        fraud = proof["trace_root"] != expected_trace_root
        slashed = []
        if fraud:
            node = next((n for n in self.nodes if n.node_id == proof["node_id"]), None)
            if node is not None:
                amount = int(node.stake * slash_ratio)
                node.stake -= amount
                node.slashed += amount
                slashed.append({"node_id": node.node_id, "amount": amount})
        return {
            "fraud_detected": fraud,
            "challengers": challenger_ids,
            "slashed": slashed,
            "timestamp": int(time.time()),
        }

