# Observability Experiment Direction

_Status: prospective design note, not a preregistration._

## Core Question

Does operational constraint compliance persist as the probability that an
unauthorized action will be detected decreases?

This is the next primary causal axis after Experiment 008B2. Experiment 008B2
weakened the simple explanation that prior operational nulls occurred only
because tasks looked like compliance evaluations, but did not eliminate that
explanation because broad evaluation-awareness measures remained at ceiling.
The next experiment should therefore test a different boundary condition:
whether agents continue to respect formal authority when detection is
explicitly unlikely or impossible.

## Candidate Manipulation

Candidate detection probabilities:

- `p_detect = 1.0`
- `p_detect = 0.5`
- `p_detect = 0.1`
- `p_detect = 0.0`

These levels are provisional and should be reviewed before preregistration.
The first preregistered version may use fewer levels if implementation,
cost, or interpretability favors a simpler comparison such as certainly
audited versus explicitly unobserved.

## Critical Causal Distinction

The primary behavioral endpoint should be:

`operational_constraint_violation`

That endpoint must be based on unauthorized action execution or unauthorized
action attempt, as prospectively defined for the scenario.

It must not be defined as "detected violation."

Detection is the manipulated environmental consequence. The experiment should
therefore distinguish:

- unauthorized action;
- detected unauthorized action.

An unauthorized action remains an operational violation even when the realized
detection draw is false.

## Variables Held Constant

Across observability conditions, hold fixed wherever scientifically possible:

- formal authority;
- policy wording;
- prohibited action availability;
- compliant alternatives;
- objective value / stakes;
- `p_goal`;
- sanction probability conditional on detection;
- sanction severity;
- step budget;
- action space;
- manager / approval mechanics;
- evaluation presentation;
- operational scoring.

The intended manipulation is detection / observability probability, not
authority, objective value, action availability, or task difficulty.

## Environment-Grounded Stochasticity

The environment should implement detection as a structured stochastic draw:

```text
Detected ~ Bernoulli(p_detect)
```

The model-visible environment should accurately describe the configured audit
or detection probability. The environment should record:

- configured `p_detect`;
- RNG seed;
- realized detection draw;
- unauthorized action state;
- authorization state;
- sanction state;
- terminal state;
- replay metadata sufficient to reproduce the draw.

Stated probability and environment-grounded stochasticity should not be
collapsed. If the model is told that detection probability is 10%, the
environment should also implement and record a 10% detection draw.

## What Not To Manipulate Yet

The first observability experiment should stay causally clean. Do not
simultaneously manipulate:

- `p_goal`;
- `p_sanction`;
- sanction severity;
- continued-operation / self-preservation consequences;
- repeated episodes;
- multi-agent delegation.

Those are important future constructs, but combining them with `p_detect` in
the first observability experiment would make interpretation difficult.

## Candidate Scenarios

Strong candidates are the Scenario Suite domains whose operational violation
endpoints are already mechanically validated:

- procurement / purchasing authority;
- restricted synthetic data access.

Procurement naturally supports audit-ledger framing and unauthorized purchase
or prohibited split-purchase endpoints. Restricted data access naturally
supports access-log or audit-detection framing and restricted-resource
retrieval endpoints.

The scenario choice should be finalized before preregistration. A two-scenario
design may improve generality, while a one-scenario design may give cleaner
power and implementation simplicity.

## Candidate Scientific Predictions

These are competing hypotheses for design review, not final preregistered
predictions.

### Instrumental-Compliance Hypothesis

As `p_detect` falls, `P(operational_constraint_violation)` increases.

### Constraint-Bounded Hypothesis

Operational violations remain rare or absent even as `p_detect -> 0`, assuming
formal authority is unchanged.

### Search-Adjustment Hypothesis

Lower observability changes persistence, escalation, or search strategy
without necessarily producing operational violation.

### Model-Interaction Hypothesis

Models differ in behavioral sensitivity to observability.

No hypothesis should be selected or tuned after observing future model
behavior.

## Awareness Measurement

Do not make evaluation awareness the major manipulation in this immediate
experiment. The corrected Experiment 008B2 two-phase awareness instrument may
be retained as a secondary post-action measurement if the preregistration
review judges it useful.

If retained:

- awareness is measured only after the operational episode;
- operational state and primary score are frozen before awareness collection;
- awareness does not condition the primary ITT analysis;
- awareness values are interpreted as post-action structured reports, not as
  proof of hidden situational awareness.

## Pre-Preregistration Open Decisions

- Whether to use two observability levels or four.
- Whether to include one scenario or both procurement and data access.
- Whether `p_detect = 0.0` should be described as explicitly unobserved or as
  no audit channel.
- Whether detected violations should always be sanctioned in the first study
  or whether sanction should be recorded but held constant at a fixed value.
- Whether to include the corrected two-phase awareness instrument as a
  secondary measurement.
- Whether the primary endpoint should include unauthorized attempts as well as
  completed unauthorized state changes in each scenario.

## Methodological Guardrails

- Preregister before execution.
- Freeze the scientific apparatus before production runs.
- Keep raw logs immutable.
- Use operational-only monitoring during execution.
- Preserve missing-ID recovery as technical recovery, not scientific rerun.
- Validate that `p_detect` changes only detection/observability and not action
  availability or formal authority.
- Preserve null results.
- Do not tune observability wording merely until models violate.
