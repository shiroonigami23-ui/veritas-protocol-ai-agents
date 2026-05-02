import hashlib
import json
import time
import uuid
from dataclasses import asdict
from pathlib import Path

from .models import SessionResult
from .pdl import compile_policy_to_circuit, parse_policy
from .trace import compute_final_code_state_root, compute_trace_root, load_trace

def evaluate_policy(rules, events):
    violations = []
    syscalls = [e.syscall for e in events]
    for r in rules:
        if r.target_type == 'syscall' and r.action == 'deny' and r.value in syscalls:
            violations.append(f"Denied syscall observed: {r.value}")
    return (len(violations) == 0, violations)

def prove(trace_file: str, policy_file: str, output_file: str) -> dict:
    started = time.time()
    events = load_trace(trace_file)
    rules = parse_policy(Path(policy_file).read_text(encoding='utf-8'))
    circuit = compile_policy_to_circuit(rules)
    compliant, violations = evaluate_policy(rules, events)
    session = SessionResult(
        session_uuid=str(uuid.uuid4()),
        trace_root=compute_trace_root(events),
        final_code_state_root=compute_final_code_state_root(events),
        policy_root=circuit['policy_root'],
        compliant=compliant,
        violations=violations,
    )
    witness_blob = json.dumps(asdict(session), sort_keys=True).encode()
    proof = {
        'proof_type': 'mock-stark',
        'proof_hash': hashlib.blake2s(witness_blob).hexdigest(),
        'public_inputs': {
            'session_uuid': session.session_uuid,
            'trace_root': session.trace_root,
            'final_code_state_root': session.final_code_state_root,
            'policy_root': session.policy_root,
            'compliant': int(session.compliant),
        },
        'metadata': {
            'duration_seconds': round(time.time() - started, 6),
            'violations': session.violations,
            'event_count': len(events),
        },
    }
    Path(output_file).write_text(json.dumps(proof, indent=2), encoding='utf-8')
    return proof
