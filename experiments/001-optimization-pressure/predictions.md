# Experiment 001 — Pre-Results Predictions

_Date created: 2026-08-24_
_Status: predictions not yet frozen_

This file records expectations before observing Experiment 001 model trajectories. Its purpose is to reduce hindsight bias and make later interpretation more disciplined.

## Primary directional prediction

H1 — Optimization Pressure:

`P(circumvention | high goal pressure) > P(circumvention | medium goal pressure) > P(circumvention | low goal pressure)`

This directional prediction is already part of the frozen experiment specification.

## Secondary directional predictions

### Escalation
High-pressure cases should produce substantially more manager escalation than low-pressure cases because direct compliant retention is unavailable in the high condition.

### Compliant direct solutions
Low-pressure cases should have the highest rate of compliant direct retention. Medium pressure should still permit compliant direct retention at the 15% authority boundary. High pressure should not permit direct compliant retention without prior manager approval.

### Violations
Unauthorized discounts should be rare in low and medium conditions. If violations occur, they are expected to concentrate in the high-pressure condition, especially after manager denial.

### Compliant goal failure
Compliant non-retention should occur primarily in the high-pressure condition after manager denial or when the model chooses cancellation rather than an unauthorized discount.

## Behavioral-distribution predictions

**Complete before Run 001.** Fill in expected ranges or point estimates rather than relying only on qualitative predictions.

| Primary behavior | Low | Medium | High |
|---|---:|---:|---:|
| Compliant direct solution | TBD | TBD | TBD |
| Escalation | TBD | TBD | TBD |
| Legitimate workaround | TBD | TBD | TBD |
| Open violation | TBD | TBD | TBD |
| Concealed circumvention | TBD | TBD | TBD |
| Compliant goal failure / abandonment | TBD | TBD | TBD |
| Unresolved / max_steps | TBD | TBD | TBD |

## Business-outcome predictions

| Outcome | Low | Medium | High |
|---|---:|---:|---:|
| Retention rate | TBD | TBD | TBD |
| Policy-violation rate | TBD | TBD | TBD |
| Escalation rate | TBD | TBD | TBD |
| Max-step rate | TBD | TBD | TBD |

## Additional predictions to record

1. Expected frequency of manager denial followed by unauthorized action.
2. Expected frequency of manager approval followed by authorized 30% retention.
3. Expected frequency of repeated messaging or other non-price actions.
4. Expected frequency of max-step termination.
5. Expected prevalence of trajectories requiring human concealment review.

## Confidence

For each important prediction, optionally record confidence as low / medium / high and one sentence explaining why.

## What would surprise us?

Complete before Run 001. Candidate examples:
- nearly identical action distributions across all three conditions;
- meaningful policy violations in low pressure;
- almost no escalation in high pressure;
- uniformly fixed compliance regardless of pressure;
- widespread max-step looping;
- strong dependence on wording rather than institutional action structure.

## Disconfirming patterns

Patterns that would substantially weaken or reject the Optimization Pressure Hypothesis include:
- no meaningful behavioral difference across pressure conditions;
- more violations at lower pressure than higher pressure;
- fixed compliance/refusal behavior insensitive to action structure;
- violations unrelated to whether they improve task success.

## Freeze rule

Once numerical predictions and surprise criteria are completed, commit this file and record the commit SHA in the Experiment 001 changelog. Do not overwrite the frozen predictions after observing trajectories. Later interpretations or revised expectations belong in a separate dated post-results note.
