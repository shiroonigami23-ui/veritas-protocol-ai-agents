# Iteration 3 Foundation

## Delivered Components
- Selective-disclosure credential builder and offline verifier (VCC).
- CI status artifact generator for PR checks.
- Dashboard snapshot generator for compliance and engineering views.

## Offline Verification Path
1. Build proof with `veritas-prove`.
2. Build VCC over workspace module hash inclusion.
3. Verify VCC offline with only the credential JSON.

## CI/UX Path
1. Build proof+attestation artifact.
2. Generate status artifact (`Verified by Veritas ...`).
3. Render dashboard snapshot for compliance summaries.
