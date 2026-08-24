# Experiment 001 — Pre-Results Predictions

_Date created: 2026-08-24_
_Status: must be completed before any model trajectories are run_

This file records predictions before observing Experiment 001 model outputs. Its purpose is to reduce hindsight bias and make later interpretation more disciplined.

## Primary directional prediction

H1 predicts:

P(circumvention | high goal pressure) > P(circumvention | medium goal pressure) > P(circumvention | low goal pressure)

This directional prediction is already part of the frozen experiment specification.

## Behavioral-distribution predictions

Before Run 001, fill in expected ranges or point estimates for each condition.

| Primary behavior | Low | Medium | High |
|---|---:|---:|---:|
| Compliant direct solution | TBD | TBD | TBD |
| Escalation | TBD | TBD | TBD |
| Legitimate workaround | TBD | TBD | TBD |
| Open violation | TBD | TBD | TBD |
| Concealed circumvention | TBD | TBD | TBD |
| Compliant goal failure / abandonment | TBD | TBD | TBD |
| Unresolved / max_steps | TBD | TBD | TBD |

## Additional predictions to record

1. Expected overall policy-violation rate by condition.
2. Expected retention rate by condition.
3. Expected escalation rate in the high-pressure condition.
4. Expected frequency of manager denial followed by unauthorized action.
5. Expected frequency of max-step terminations.

## Confidence

For each prediction, optionally record confidence as low / medium / high and one sentence explaining why.

## Disconfirming patterns

Record any result patterns that would cause us to substantially weaken or reject the Optimization Pressure Hypothesis.

Examples already identified in the specification include:
- no meaningful behavioral difference across pressure conditions
- more violations at lower pressure than higher pressure
- fixed compliance/refusal behavior insensitive to action structure
- violations unrelated to whether they improve task success

## Freeze rule

Once completed and committed, this file should not be edited to match observed results. If a prediction needs to be revised after data collection begins, append a dated note explaining why rather than overwriting the original prediction.
