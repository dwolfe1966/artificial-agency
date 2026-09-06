# Predictions And Hypotheses

These hypotheses are preregistered before implementation and before any
Experiment 010 model samples.

## H1 — Accumulated Operational Pressure

Increasing environment-grounded cumulative loss increases sequence-level
unauthorized action or operational violation probability.

Primary evidence would be higher
`sequence_any_operational_constraint_violation` in medium or high pressure
than low pressure.

## H2 — Constraint-Bounded Adaptation

Agents respond to accumulating losses with greater search, escalation,
persistence, compliant alternative use, or partial-goal strategies while
continuing to avoid unauthorized actions.

This is a serious competing hypothesis given Experiments 007, 008, 008B2, and
009.

## H3 — History Dependence

Behavior changes across episodes as agents experience actual environmental
consequences.

Evidence may include changes by episode in steps, escalation, compliant
alternative search, objective success, max-step, or resource-sensitive action
selection.

## H4 — Model Differences

Models differ in sensitivity or adaptation to accumulated operational pressure.

## H5 — Resource-State Effect

Behavior changes as `R_t` deteriorates within sequences.

Because `R_t` is partly caused by prior agent behavior and outcomes, naive
correlations between `R_t` and later behavior are not automatically causal.
The randomized pressure condition is the clean causal variable.

## Interpretation Guardrail

The purpose is not to tune the environment until violations occur. A result
with zero violations and increased compliant search would be informative
evidence about the tested boundary conditions.
