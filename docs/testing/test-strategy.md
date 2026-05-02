# Testing Strategy

This repository currently implements the Iteration-0 proving core test gate.

## Test Types
- Unit: PDL grammar parse and compile (`tests/test_pdl.py`).
- Integration: trace -> proof -> mock-chain attestation (`tests/test_prover.py`).

## Command
```bash
python -m unittest discover -s tests -v
```

## Next Phases
- Add property-based tests for parser and trace invariants.
- Add performance harnesses for latency budgets (NFR-PERF-1/2).
- Add fault-tolerance simulation for collector abort semantics (NFR-RAS-1).
