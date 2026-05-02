# Architecture Overview

## Modules
- Core:
  - Trace canonicalization and roots.
  - Policy compiler abstraction.
  - Proof artifact generation.
- Mock Chain:
  - 3-node verification simulation.
  - Immutable in-memory attestation indexing.
- CLI:
  - `veritas-prove`
  - `veritas-verify`

## Data Flow
1. Load trace JSON.
2. Parse and compile PDL.
3. Evaluate compliance and compute public inputs.
4. Emit proof artifact.
5. Verify and anchor attestation (optional flag).
