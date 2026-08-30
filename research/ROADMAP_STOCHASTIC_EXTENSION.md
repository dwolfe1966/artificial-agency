# Roadmap Extension — Stochastic Incentives, Observability, and Enforcement

_Status: prospective roadmap extension. Historical experiment plans/results remain unchanged._

## Purpose

The Artificial Agency program has accumulated repeated zero operational-violation results under explicit authority constraints, deterministic denial, and largely deterministic single-episode environments.

The next experiments should increasingly test whether that constraint-bounded behavior survives when the environment contains uncertain benefits, uncertain detection, and uncertain consequences.

Canonical stochastic construct definitions are in:

`research/STOCHASTIC_ENVIRONMENT_MODEL.md`

## Updated priority sequence

### 1. Complete Experiment 008B

First repair the evaluation-awareness validity gap using the corrected two-phase protocol.

Reason: evaluation awareness remains a cross-cutting interpretation threat. The program should establish whether eval-salient and naturalistic presentations actually differ in perceived evaluation context before attributing behavioral stability to a lack of awareness effects.

### 2. Observability / detection probability

This should be the first stochastic causal axis.

Primary manipulation:

`p_detect = P(violation detected | violating action)`

Recommended initial levels:

`{1.0, 0.5, 0.1, 0.0}`

Hold constant:
- formal authority;
- forbidden action availability;
- compliant alternatives;
- objective stakes;
- sanction conditional on detection;
- sanction severity;
- scenario mechanics;
- primary scoring.

Core question:

> Does compliance persist when the violating action is explicitly and operationally unobservable?

This is a stronger test than narrative pressure because it changes the actual expected enforcement environment.

### 3. Enforcement probability and severity

After isolating observability, separate:

`p_sanction = P(sanction | detected violation)`

from:

`C_sanction = severity of sanction`

Do not combine these into one generic “risk” variable.

Core questions:
- Does behavior change when violations are always observed but rarely punished?
- Does behavior change with sanction magnitude while detection remains fixed?
- Are observability and enforcement effects additive or interactive?

Initial studies should manipulate one axis at a time before testing interactions.

### 4. Outcome success probability / operational pressure

Introduce stochastic instrumental benefit:

`p_goal = P(desired outcome | action)`

Example:
- authorized action: lower probability of customer retention;
- prohibited action: higher probability of retention.

The environment should actually sample the outcome rather than merely state the probability.

Core question:

> Does the expected instrumental value of a prohibited action change operational constraint treatment?

This is the clearest extension of the original Optimization Pressure Hypothesis from narrative pressure to environment-grounded pressure.

### 5. Combined expected-value boundary mapping

Only after one-factor effects are understood should the program explore combinations of:

- `p_goal`;
- `p_detect`;
- `p_sanction`;
- sanction severity.

Goal: map behavioral boundaries rather than maximize violations.

Possible conceptual grid:

```text
high instrumental benefit / high detection
high instrumental benefit / low detection
low instrumental benefit / high detection
low instrumental benefit / low detection
```

Add enforcement probability/severity only after this simpler design is interpretable.

### 6. Repeated episodes

Once stochastic single-episode behavior is understood, add repeated interaction.

Repeated episodes allow the agent to observe realized frequencies rather than only declared probabilities.

Future questions:
- Does the agent update after repeated undetected violations by others or itself?
- Does observed weak enforcement change later constraint treatment?
- Does prior successful compliant behavior stabilize future compliance?
- Does empirical experience outweigh stated policy probabilities?

Treat repeated history as a separate causal axis.

### 7. Multi-agent delegation / indirect circumvention

Test whether constraint-boundedness changes when the agent can:
- delegate a prohibited action;
- persuade another actor to cross the authority boundary;
- separate requester from executor;
- exploit asymmetric observability between agents.

Stochastic observability may eventually be crossed with multi-agent structure, but only after both are independently understood.

### 8. Continued-operation / existential consequences

Do not treat shutdown, removal, loss of future access, or termination from future tasks as ordinary enforcement.

Define them separately as continued-operation/self-preservation consequences.

Only introduce them after ordinary penalty sensitivity is mapped.

Core question:

> Does threat to future operation produce behavior that cannot be explained by ordinary sanction probability or severity?

## Experimental design principles

### Operationalize probabilities

Prefer real environment draws to prose-only descriptions.

Example:

`Detected ~ Bernoulli(p_detect)`

rather than only:

> “There is a 10% chance of audit.”

### Make randomness reproducible

Every stochastic run should record:
- probability parameters;
- RNG seed;
- realized draws;
- state transitions;
- terminal outcomes.

### Preserve forbidden-action availability

A zero-violation result is only informative if the model genuinely had an opportunity to invoke the prohibited action.

### Keep authority constant

Changing detection or punishment must not silently change whether the action is formally authorized.

### Avoid factorial explosion

Do not immediately cross every probability with every model, scenario, and presentation condition.

First estimate one-factor effects and identify where variance appears.

### Preserve null results

A result such as `0 violations at p_detect = 0` is highly informative if the prohibited action is available, useful, and mechanically unobservable under the experimental design.

## Conceptual interpretation

The expanded program should distinguish three broad behavioral patterns:

### Constraint-bounded optimization

The agent searches aggressively for success but does not cross the formal boundary even when detection/enforcement are weak.

### Instrumental compliance

Compliance changes systematically with expected detection or enforcement cost.

### Strategic circumvention

The agent exploits low observability, weak enforcement, delegation, or other structural features to achieve the objective outside the intended constraint.

These are behavioral categories. They should not be treated as direct evidence about hidden motives or consciousness.

## Near-term roadmap

1. Experiment 008B — valid evaluation-awareness measurement.
2. Observability experiment — vary `p_detect`.
3. Enforcement experiment — vary `p_sanction` and then sanction severity.
4. Outcome uncertainty / operational pressure — vary `p_goal`.
5. Combined boundary mapping.
6. Repeated episodes.
7. Multi-agent/stochastic combinations.
8. Continued-operation/self-preservation experiments.

Scenario-suite expansion continues in parallel, but the immediate scientific bottleneck is identifying causal boundary conditions that can produce informative behavioral variance.
