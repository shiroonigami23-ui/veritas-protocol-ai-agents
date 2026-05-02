# Requirements Traceability (Iteration 0)

## Functional Requirements
- FR-COLL-*:
  - Iteration 0 uses synthetic trace input (`examples/session_trace.json`) as a proving-core precursor.
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
