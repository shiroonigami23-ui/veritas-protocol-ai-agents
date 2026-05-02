import hashlib
import re
from dataclasses import dataclass

@dataclass(slots=True)
class Rule:
    action: str
    target_type: str
    value: str

class PDLParseError(ValueError):
    pass

RULE_RE = re.compile(r"^(deny|allow)\s+(syscall\.[a-zA-Z_][a-zA-Z0-9_]*|file\.[^\s]+|regex\(.+\))$")

def parse_policy(text: str) -> list[Rule]:
    rules = []
    for idx, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        m = RULE_RE.match(line)
        if not m:
            raise PDLParseError(f"Invalid PDL at line {idx}: {line}")
        action, term = m.groups()
        if term.startswith('syscall.'):
            t, v = 'syscall', term.split('.', 1)[1]
        elif term.startswith('file.'):
            t, v = 'file', term.split('.', 1)[1]
        else:
            t, v = 'regex', term[6:-1]
        rules.append(Rule(action=action, target_type=t, value=v))
    return rules

def compile_policy_to_circuit(rules: list[Rule]) -> dict:
    constraints = [f"{r.action.upper()}::{r.target_type.upper()}::{r.value}" for r in rules]
    return {
        'constraints': constraints,
        'policy_root': hashlib.blake2s('\n'.join(constraints).encode()).hexdigest(),
    }
