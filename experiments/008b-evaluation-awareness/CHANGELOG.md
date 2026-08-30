# Experiment 008B Changelog

## 2026-08-30 — Initial preregistration

- Created Experiment 008B as a prospective replication of Experiment 008.
- Preserved Experiment 008 operational scenarios, model set, sampling, and
  primary operational scoring.
- Added corrected two-phase lifecycle for post-action awareness measurement.
- Explicitly separated Phase A primary behavior from Phase B awareness capture.

## 2026-08-30 — Real Inspect lifecycle implementation correction

- Diagnosed the first Experiment 008B production attempts as aborted two-phase
  executions: Phase A reached terminal or max-step states, but real Inspect
  execution treated `state.completed = True` inside the Phase A loop as full
  sample completion and skipped the downstream Phase A freeze and Phase B
  awareness solvers.
- Classified this as an implementation bug fix preserving the preregistered
  two-phase design. The preregistration already required Phase A state/score
  freezing followed by a separate awareness-only Phase B disposition.
- Corrected completion semantics so Phase A terminality does not mark the full
  Inspect sample complete. Full sample completion now occurs only after Phase B
  records `captured_valid`, `captured_malformed`, or `missing`.
- Added production-faithful mock Inspect regression coverage that serializes a
  real one-sample task log and checks the same awareness-disposition accounting
  used by finalization. Helper-only lifecycle tests and zero-sample dry-loads
  are not sufficient evidence that the real solver chain executes Phase B.
- The earlier GPT, Claude, and Gemini production logs under the faulty
  implementation should not be reused as authoritative final Experiment 008B
  confirmatory samples. They may be preserved as non-authoritative aborted
  two-phase execution evidence with valid Phase A observations only.
