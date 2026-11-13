# 🗺 Roadmap — Veritas Protocol

> Back to the [README](../README.md).

## Where the project stands

Status: **iteration 3**.

## Milestones

### Iteration 0 — Proving core (done)

- [x] `veritas-prove` CLI, PDL compiler, 3-node mock chain
- [x] Exit-gate scenario test (<120 s)

### Iteration 1 — Collector (prototype done)

- [x] Canonical event capture, write-intent dedup, streaming MMR
- [ ] Real eBPF-based syscall capture on Linux
- [ ] Sidecar packaging (container) for agent sandboxes

### Iteration 2 — Prover network (simulated)

- [x] Proof-race mempool, recursive aggregation, slashing simulation
- [ ] Replace the proof abstraction with a real zkVM (RISC Zero / SP1) backend
- [ ] Benchmark proof size and latency vs trace length

### Iteration 3 — Integrations (foundations done)

- [x] VCC build/verify, CI status artefact, dashboard snapshot
- [ ] Publish a reusable GitHub Action
- [ ] Web compliance dashboard

### Iteration 4 — Hardening

- [ ] Regulatory mapping (EU AI Act, SOC 2 evidence)
- [ ] Security audit and threat model
- [ ] Testnet → mainnet readiness

## 🔭 Long-term Vision

Make "trust, but verify" the default for autonomous coding agents: every agent session produces a cryptographic receipt
that any reviewer, CI pipeline or regulator can check — without having to trust the agent vendor.

## 💡 Ideas Backlog (unscheduled)

- Plugins for popular agent frameworks so traces are captured automatically
- Policy marketplace with audited PDL templates

## How to help

Pick any unchecked item, open an issue to discuss the approach, then send a PR. Items in the earliest unfinished milestone are the highest priority.


---
*Last updated: 2026-11-13*
