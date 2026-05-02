# Requirements Traceability (Iteration 0)

## Functional Requirements
- FR-COLL-*:
  - Iteration 0 uses synthetic trace input (`examples/session_trace.json`) as a proving-core precursor.
  - Iteration 1 implementation added for:
    - FR-COLL-2 deterministic capture tuple
    - FR-COLL-3 intent dedup
    - FR-COLL-4 MMR API
    - FR-COLL-6 graceful abort behavior
  - Code: `src/veritas/collector/collector.py`, `src/veritas/collector/mmr.py`
  - Tests: `tests/test_collector_cvt.py`
- FR-POL-1:
  - Implemented in `src/veritas/core/pdl.py`.
- FR-POL-2:
  - Implemented policy composition in `src/veritas/core/policy_engine.py`.
- FR-POL-3:
  - Implemented dry-run report generation in `src/veritas/core/policy_engine.py` and `src/veritas/cli/policy_dryrun.py`.
- FR-PROV-1:
  - Simplified local proving job lifecycle in `src/veritas/core/prover.py`.
  - Distributed proof-race simulation in `src/veritas/prover_network/network.py`.
- FR-PROV-2:
  - Recursive aggregation abstraction in `src/veritas/prover_network/network.py`.
- FR-PROV-3:
  - Cut-and-choose slashing simulation in `src/veritas/prover_network/network.py`.
- FR-CHAIN-1 / FR-CHAIN-2:
  - Simulated verify-and-attest in `src/veritas/mock_chain/chain.py`.

## Iteration 0 Exit Criteria Mapping
1. Proof generated for 3 modified files and 2 external commands.
   - Verified by `tests/test_prover.py`.
2. Mock chain verification succeeds in end-to-end flow.
   - Verified by `tests/test_prover.py`.
3. Completion under 120 seconds.
   - Time gate asserted in `tests/test_prover.py`.

## Iteration 1 Exit Criteria Progress
- CVT pass target:
  - Added CVT matrix and tests in `docs/testing/cvt-matrix.md` and `tests/test_collector_cvt.py`.
- Dedup behavior target (>60% on long traces):
  - Dedup engine implemented and covered with focused tests.
- Stability signal:
  - Multi-session stability smoke in `tests/test_iteration1_stability.py`.

## Iteration 2 Progress
- Prover race and winner selection:
  - `tests/test_prover_network.py::test_race_and_aggregation`
- Recursive aggregation:
  - `tests/test_prover_network.py::test_race_and_aggregation`
- Slashing control:
  - `tests/test_prover_network.py::test_cut_and_choose_slashing`
