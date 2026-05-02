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
- FR-PROV-1:
  - Simplified local proving job lifecycle in `src/veritas/core/prover.py`.
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
