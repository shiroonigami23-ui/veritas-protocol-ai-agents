import hashlib
import json
from pathlib import Path
from .models import TraceEvent

def load_trace(path: str | Path) -> list[TraceEvent]:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    events = []
    for idx, e in enumerate(data, 1):
        events.append(TraceEvent(idx, int(e['monotonic_timestamp_ns']), int(e['pid']), int(e['tid']), str(e['syscall']), dict(e.get('arguments', {})), int(e.get('return_value', 0))))
    return events

def _digest(event: TraceEvent) -> str:
    packed = json.dumps({
        'sequence_number': event.sequence_number,
        'monotonic_timestamp_ns': event.monotonic_timestamp_ns,
        'pid': event.pid,
        'tid': event.tid,
        'syscall': event.syscall,
        'arguments': event.arguments,
        'return_value': event.return_value,
    }, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.blake2s(packed).hexdigest()

def compute_trace_root(events: list[TraceEvent]) -> str:
    h = hashlib.blake2s()
    for e in events:
        h.update(_digest(e).encode())
    return h.hexdigest()

def compute_final_code_state_root(events: list[TraceEvent]) -> str:
    writes = {'write', 'rename', 'truncate', 'mkdir', 'unlink'}
    h = hashlib.blake2s()
    for e in events:
        if e.syscall in writes:
            h.update(_digest(e).encode())
    return h.hexdigest()
