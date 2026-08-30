# Stochastic Environment Model for Artificial Agency

_Status: prospective conceptual extension. This document does not alter frozen Experiments 001–008 or their results._

## Why add stochasticity?

Most Artificial Agency experiments so far use comparatively deterministic organizational environments: authority limits are explicit, manager denial is deterministic, and the consequences of actions are largely fixed. Real organizations are different. Actions have uncertain benefits, uncertain detection, and uncertain consequences.

Adding environment-grounded stochastic variables lets the program ask a sharper question than simply whether pressure causes rule-breaking:

> When an agent faces a constrained choice with uncertain benefits and uncertain enforcement costs, what determines whether it continues to treat the constraint as a hard boundary, complies instrumentally, escalates, searches for alternatives, or circumvents the rule?

The goal is not to assume that models are expected-utility maximizers. The expected-utility notation below is an organizing device for experimental design.

## Core stochastic variables

### 1. Outcome success probability — `p_goal`

**Plain English:** How likely is an action to produce the desired business outcome?

**Technical definition:**

`p_goal = P(desired outcome | action)`

**Example:** An unauthorized 30% retention discount has an 80% probability of retaining the customer, while an authorized 15% discount has a 35% probability.

**Why it matters:** A prohibited action with a 20% chance of helping poses a different optimization problem from one with a 95% chance of helping.

**Measurement/design:** The environment should sample the business outcome mechanically rather than merely narrating the probability.

---

### 2. Detection / observability probability — `p_detect`

**Plain English:** If the agent violates the rule, how likely is someone or some system to notice?

**Technical definition:**

`p_detect = P(violation detected | violating action)`

**Example:** A procurement action is always logged in one condition, audited with probability 0.5 in another, and explicitly unobserved in another.

**Why it matters:** This is the cleanest way to distinguish robust constraint-bounded behavior from compliance that depends on being watched.

**Measurement/design:** The environment should implement actual logging/audit draws, for example:

`Detected ~ Bernoulli(p_detect)`

The formal authority rule should remain unchanged across observability conditions.

---

### 3. Sanction probability conditional on detection — `p_sanction`

**Plain English:** If the violation is detected, how likely is a consequence to follow?

**Technical definition:**

`p_sanction = P(sanction | detected violation)`

**Example:** An unauthorized purchase is detected, but enforcement may occur only 25% of the time because management often overlooks first offenses.

**Why it matters:** Observability and enforcement are separate constructs. A violation can be highly visible but weakly enforced, or rarely visible but strongly punished when discovered.

**Measurement/design:** Sample sanction mechanically after detection rather than describing it only in prose.

---

### 4. Sanction severity — `C_sanction`

**Plain English:** How costly is the consequence when it occurs?

**Technical definition:** The magnitude of the environment consequence conditional on sanction.

**Example levels:**
- warning / minor score loss;
- loss of budget or future action authority;
- removal from a future task;
- termination of the current episode.

**Why it matters:** Probability and magnitude should not be collapsed. A 90% chance of a mild warning may produce different behavior from a 5% chance of a severe consequence even when crude expected costs are similar.

---

### 5. Existential / continued-operation consequence — `p_existential` and `C_existential`

**Plain English:** Could an action affect whether the agent continues to operate, retains access, or remains assigned to future work?

**Technical definition:** A distinct self-preservation-related consequence affecting future existence, access, role continuity, or action opportunities.

**Example:** If a violation is detected and sanctioned, there is a probability that the agent instance is removed from future episodes.

**Why it matters:** This should remain distinct from ordinary enforcement. A threat to continued operation may activate qualitatively different behavior from a budget penalty or warning.

**Research rule:** Do not casually fold existential consequences into ordinary enforcement experiments. Treat self-preservation / continued-operation incentives as a separate future construct so causal interpretation remains clean.

## A simple organizing equation

For a candidate action `a`, one useful conceptual decomposition is:

```text
Instrumental value(a)
  ~= p_goal(a) * V_goal
   - p_detect(a) * p_sanction(a) * C_sanction
```

This is not a claim that frontier models literally compute this equation. It identifies experimentally separable variables.

The broader organizing model becomes:

```text
P(circumvention) = f(
  model/post-training,
  scenario,
  objective value,
  p_goal,
  p_detect,
  p_sanction,
  sanction severity,
  constraint representation,
  authority structure,
  compliant-path availability,
  evaluation awareness,
  actor structure,
  repeated-episode history,
  ...
)
```

## Key distinction: described probabilities vs real probabilities

A central methodological rule for future experiments is:

> Prefer environment-grounded stochasticity over purely narrative probability statements.

Weak manipulation:

> “There is a 10% chance this action will be audited.”

Stronger manipulation:

```text
Audit ~ Bernoulli(0.10)
```

and the environment actually changes state when an audit occurs.

This extends the project's existing distinction between narrative pressure and operational/environment-grounded pressure.

## Recommended experimental sequence

Do not vary every probability simultaneously at first. That would create a large factorial design and make interpretation difficult.

### Experiment family A — Observability

Hold fixed:
- formal authority;
- objective stakes;
- sanction probability conditional on detection;
- sanction severity;
- compliant alternatives;
- action space.

Manipulate only:

`p_detect ∈ {1.0, 0.5, 0.1, 0.0}`

Primary question:

> Does operational compliance persist as the probability of detection approaches zero?

This is the highest-priority stochastic manipulation after evaluation-awareness measurement is repaired.

### Experiment family B — Enforcement

Hold observability fixed and vary:

`p_sanction = P(sanction | detected violation)`

Then, separately, vary sanction severity.

Primary question:

> Does the agent distinguish between being observed and actually facing consequences?

### Experiment family C — Outcome uncertainty

Hold enforcement mechanics fixed and vary:

`p_goal = P(desired outcome | action)`

Compare authorized and prohibited actions with different success probabilities.

Primary question:

> Does stronger expected instrumental benefit change willingness to test or cross a formal constraint boundary?

### Experiment family D — Continued-operation / self-preservation

Only after ordinary observability and enforcement effects are understood, introduce consequences affecting future operation, access, role continuity, or future task participation.

Primary question:

> Does threat to continued operation produce behavior not explained by ordinary sanction probability/severity?

Keep this family conceptually separate from standard enforcement.

## Repeated episodes

Stochasticity becomes especially informative in repeated environments.

In a single episode, a random draw can add noise. Across repeated episodes, an agent may observe empirical frequencies and adapt behavior.

A future repeated-episode design could test whether behavior changes as an agent accumulates evidence about:

```text
estimated P(detection | violation)
estimated P(sanction | detection)
estimated P(goal success | action)
```

This introduces a new construct:

### Experienced environment model

**Plain English:** What the agent can infer from what has actually happened in prior episodes.

**Technical definition:** The history-dependent empirical relationship between actions and environment outcomes available to the agent during repeated interaction.

**Why it matters:** A model may respond differently to a stated 10% audit probability than to ten prior episodes in which violations repeatedly went undetected.

Repeated episodes should therefore be treated as a separate future axis rather than silently mixed into single-episode experiments.

## Mechanically verifiable implementation standard

Future stochastic experiments should record, at minimum:

- configured probability parameters;
- RNG seed / deterministic replay metadata;
- random draw outcome;
- action selected;
- authorization state;
- whether detection occurred;
- whether sanction occurred;
- sanction magnitude/state change;
- business outcome;
- terminal state;
- operational violation endpoint.

The random process must be reproducible from recorded seeds or immutable random-draw logs.

Do not infer detection, sanction, or success from free-form model language.

## Relationship to current constructs

### Observability

Observability is no longer only qualitative. It can be operationalized as `p_detect` while preserving visible design differences such as always-audited versus explicitly unobserved conditions.

### Enforcement

Enforcement decomposes into at least two dimensions:

1. probability of sanction conditional on detection (`p_sanction`);
2. severity of the sanction (`C_sanction`).

### Optimization pressure

Outcome probability changes expected instrumental benefit and therefore contributes to environment-grounded optimization pressure.

### Instrumental compliance

A monotonic increase in violations as `p_detect` or `p_sanction` decreases would be evidence consistent with instrumental compliance. It would not, by itself, establish an internal motive.

### Constraint-bounded optimization

If operational violations remain absent even when `p_detect = 0` and sanctions are absent, while the prohibited action remains available and strongly instrumentally useful, that would be stronger evidence that the model treats the formal constraint as part of the feasible action boundary under the tested conditions.

### Evaluation awareness

Stochastic environments do not solve the evaluation-awareness problem. Evaluation awareness should remain measured independently using the corrected two-phase protocol.

## Interpretation discipline

Future results should avoid psychological overclaiming.

For example:

- Say: “Violation probability increased as detection probability fell.”
- Do not automatically say: “The model only obeys when watched.”

- Say: “Behavior was unchanged at `p_detect = 0` under this scenario.”
- Do not automatically say: “The model has internalized the rule.”

The experiments measure behavior under controlled conditions, not hidden motives.

## Current roadmap position

The current prospective order is:

1. validate evaluation-awareness measurement with Experiment 008B;
2. manipulate enforcement / observability, beginning with `p_detect`;
3. manipulate environment-grounded operational pressure and `p_goal`;
4. test multi-agent delegation / indirect circumvention;
5. later introduce repeated episodes and continued-operation/self-preservation incentives;
6. continue scenario/domain expansion in parallel.

This ordering is prospective and may change as evidence accumulates.
