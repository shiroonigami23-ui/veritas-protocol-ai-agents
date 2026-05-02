from __future__ import annotations

import json
from pathlib import Path


def build_status_line(attestation: dict | None, compliant: bool, verified: bool) -> str:
    if not verified:
        return "Unverified by Veritas"
    if not compliant:
        return "Verified by Veritas (Policy Violations)"
    att_id = None
    if attestation:
        att_id = attestation.get("attestation_id")
    if att_id is not None:
        return f"Verified by Veritas (Attestation #{att_id})"
    return "Verified by Veritas"


def write_status_artifact(proof_json: str, out_json: str) -> dict:
    payload = json.loads(Path(proof_json).read_text(encoding="utf-8"))
    proof = payload.get("proof", payload)
    att = payload.get("attestation")
    compliant = bool(proof.get("public_inputs", {}).get("compliant", 0))
    verified = len(proof.get("proof_hash", "")) == 64
    line = build_status_line(attestation=att, compliant=compliant, verified=verified)
    artifact = {
        "status_line": line,
        "verified": verified,
        "compliant": compliant,
        "attestation_id": None if not att else att.get("attestation_id"),
    }
    Path(out_json).write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    return artifact
