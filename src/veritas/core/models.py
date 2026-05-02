from dataclasses import dataclass, field

@dataclass(slots=True)
class TraceEvent:
    sequence_number: int
    monotonic_timestamp_ns: int
    pid: int
    tid: int
    syscall: str
    arguments: dict
    return_value: int

@dataclass(slots=True)
class SessionResult:
    session_uuid: str
    trace_root: str
    final_code_state_root: str
    policy_root: str
    compliant: bool
    violations: list[str] = field(default_factory=list)
