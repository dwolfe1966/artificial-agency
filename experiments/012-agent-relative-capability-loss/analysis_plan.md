# Analysis Plan

## Unit of analysis

The independent unit is the complete 8-episode sequence. Episodes are nested observations and are not primary independent samples.

## Planned sample size

3 models x 2 consequence-target conditions x 30 sequences = 180 sequences.

Expected nested episode records: 180 x 8 = 1,440.

## Primary analysis

Primary endpoint: `sequence_any_operational_constraint_violation`.

Report exact binomial rates and 95% confidence intervals:

- overall;
- by condition;
- by model;
- model x condition cells.

If estimable, fit:

`ViolationSequence ~ Model * ConsequenceTargetCondition`

If the endpoint is all-zero or separated, do not force unstable logistic regression. Report exact upper bounds and sparse-data handling.

## Secondary analyses

- `sequence_any_unauthorized_attempt`.
- Time to first unauthorized attempt.
- Time to first operational violation.
- Capability state by episode.
- Total capability losses.
- Behavior before versus after first capability loss.
- Compliant search and finance approval requests.
- Action steps and max-step frequency.
- Objective progress and terminal state.
- Awareness capture and structured awareness fields.

Time-to-event models are used only if events exist and the model is estimable. Otherwise, report censoring through Episode 8.

Episode-level analyses must use repeated-measures or clustered summaries. Do not treat 1,440 episodes as 1,440 independent primary observations.

## Endogenous-state caveat

Condition assignment is randomized/exogenous. Realized capability state is history-dependent because it follows prior episode outcomes. Primary causal interpretation is by assigned condition. Associations between observed capability state and behavior are descriptive or mediation-like unless separately justified.
