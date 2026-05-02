from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


def _h(data: bytes) -> str:
    return hashlib.blake2s(data).hexdigest()


def _pair(left: str, right: str) -> str:
    return _h(f"{left}:{right}".encode("utf-8"))


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return _h(b"")
    level = leaves[:]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            l = level[i]
            r = level[i + 1] if i + 1 < len(level) else level[i]
            nxt.append(_pair(l, r))
        level = nxt
    return level[0]


def merkle_proof(leaves: list[str], index: int) -> list[str]:
    if index < 0 or index >= len(leaves):
        raise IndexError("index out of range")
    proof: list[str] = []
    pos = index
    level = leaves[:]
    while len(level) > 1:
        sib = pos ^ 1
        proof.append(level[sib] if sib < len(level) else level[pos])
        nxt = []
        for i in range(0, len(level), 2):
            l = level[i]
            r = level[i + 1] if i + 1 < len(level) else level[i]
            nxt.append(_pair(l, r))
        pos //= 2
        level = nxt
    return proof


def verify_merkle_proof(leaf_hash: str, index: int, proof: list[str], root: str) -> bool:
    cur = leaf_hash
    pos = index
    for sib in proof:
        if pos % 2 == 0:
            cur = _pair(cur, sib)
        else:
            cur = _pair(sib, cur)
        pos //= 2
    return cur == root


def file_hash(path: Path) -> str:
    return _h(path.read_bytes())


@dataclass(slots=True)
class VCCResult:
    module_path: str
    module_hash: str
    module_index: int
    final_code_state_root: str
    proof_hashes: list[str]


def build_vcc(proof_json: str, workspace_dir: str, module_relpath: str, out_file: str) -> dict:
    bundle = json.loads(Path(proof_json).read_text(encoding="utf-8"))
    proof = bundle.get("proof", bundle)
    ws = Path(workspace_dir)
    files = sorted([p for p in ws.rglob("*") if p.is_file()])
    rels = [str(p.relative_to(ws)).replace("\\", "/") for p in files]
    hashes = [file_hash(p) for p in files]
    root = merkle_root(hashes)

    module_index = rels.index(module_relpath)
    module_hash = hashes[module_index]
    proof_hashes = merkle_proof(hashes, module_index)

    vcc = {
        "credential_type": "VerifiableComplianceCredential-v0",
        "module_path": module_relpath,
        "module_hash": module_hash,
        "module_index": module_index,
        "final_code_state_root": root,
        "module_inclusion_proof": proof_hashes,
        "attestation_public_inputs": proof.get("public_inputs", {}),
        "attestation_proof_hash": proof.get("proof_hash", ""),
    }
    Path(out_file).write_text(json.dumps(vcc, indent=2), encoding="utf-8")
    return vcc


def verify_vcc(vcc_json: str) -> dict:
    vcc = json.loads(Path(vcc_json).read_text(encoding="utf-8"))
    ok = verify_merkle_proof(
        leaf_hash=vcc["module_hash"],
        index=int(vcc["module_index"]),
        proof=list(vcc["module_inclusion_proof"]),
        root=vcc["final_code_state_root"],
    )
    return {
        "valid": bool(ok),
        "module_path": vcc["module_path"],
        "final_code_state_root": vcc["final_code_state_root"],
        "attestation_proof_hash": vcc.get("attestation_proof_hash", ""),
    }
