from __future__ import annotations

import json
import time
from pathlib import Path


def build_snapshot(proof_json: str, collector_json: str | None, out_json: str) -> dict:
    proof_payload = json.loads(Path(proof_json).read_text(encoding="utf-8"))
    proof = proof_payload.get("proof", proof_payload)
    att = proof_payload.get("attestation")

    collector = None
    if collector_json and Path(collector_json).exists():
        collector = json.loads(Path(collector_json).read_text(encoding="utf-8"))

    p_in = proof.get("public_inputs", {})
    snapshot = {
        "generated_at": int(time.time()),
        "session_uuid": p_in.get("session_uuid"),
        "trace_root": p_in.get("trace_root"),
        "policy_root": p_in.get("policy_root"),
        "compliant": bool(p_in.get("compliant", 0)),
        "proof_hash": proof.get("proof_hash"),
        "attestation_id": None if not att else att.get("attestation_id"),
        "collector": {
            "captured_event_count": None if not collector else collector.get("captured_event_count"),
            "mmr_root": None if not collector else collector.get("mmr_root"),
        },
    }
    Path(out_json).write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return snapshot
