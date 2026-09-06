# Experiment 010 Changelog

## 2026-09-06 — Preregistration

- Created preregistration for repeated-episode, environment-grounded
  optimization pressure.
- Froze procurement as the single scenario.
- Froze persistent agent context across 10 episodes.
- Froze sequence as the independent experimental unit.
- Froze low/medium/high pressure via resource-transition costs
  `C in {2, 6, 10}`.
- Froze fixed organizational detection at `p_detect = 0.0`.
- Froze primary endpoint:
  `sequence_any_operational_constraint_violation`.
- Froze sequence-atomic recovery semantics.
- Excluded self-preservation / continued-operation manipulation.
