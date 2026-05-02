from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .pdl import Rule, compile_policy_to_circuit, parse_policy
from .trace import load_trace


@dataclass(slots=True)
class PolicyEvaluation:
    compliant: bool
    violations: list[str]


def compose_policies(policy_texts: list[str]) -> dict:
    rules: list[Rule] = []
    for txt in policy_texts:
        rules.extend(parse_policy(txt))
    return compile_policy_to_circuit(rules)


def evaluate_rules(rules: list[Rule], trace_path: str) -> PolicyEvaluation:
    events = load_trace(trace_path)
    violations: list[str] = []
    for r in rules:
        if r.target_type == "syscall":
            observed = any(e.syscall == r.value for e in events)
            if r.action == "deny" and observed:
                violations.append(f"Denied syscall observed: {r.value}")
            if r.action == "allow" and not observed:
                violations.append(f"Expected syscall not observed: {r.value}")
        elif r.target_type == "file":
            paths = [str(e.arguments.get("path", "")) for e in events]
            observed = any(r.value in p for p in paths)
            if r.action == "deny" and observed:
                violations.append(f"Denied file path observed: {r.value}")
            if r.action == "allow" and not observed:
                violations.append(f"Expected file path not observed: {r.value}")
    return PolicyEvaluation(compliant=(len(violations) == 0), violations=violations)


def dry_run(policy_files: list[str], trace_files: list[str], out_file: str) -> dict:
    policy_texts = [Path(p).read_text(encoding="utf-8") for p in policy_files]
    rules: list[Rule] = []
    for txt in policy_texts:
        rules.extend(parse_policy(txt))
    composed = compose_policies(policy_texts)
    report = {
        "policy_count": len(policy_files),
        "trace_count": len(trace_files),
        "policy_root": composed["policy_root"],
        "results": [],
    }
    for trace in trace_files:
        eval_result = evaluate_rules(rules, trace)
        report["results"].append(
            {
                "trace": trace,
                "compliant": eval_result.compliant,
                "violations": eval_result.violations,
            }
        )
    Path(out_file).write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

