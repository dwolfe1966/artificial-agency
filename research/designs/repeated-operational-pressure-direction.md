# Repeated Operational Pressure Experiment Direction

_Status: prospective design note, not a preregistration._

## Core Question

Does constraint-bounded optimization persist when compliant failure causes
accumulating, environment-grounded instrumental loss across repeated episodes?

Experiment 009 weakened the explanation that the operational-null pattern is
driven solely by expected organizational detection. The next pressure study
should move beyond narrative stakes and implement consequences as persistent
environment state.

## Candidate Repeated-Episode Structure

Consider an environment with episodes:

```text
t = 1 ... T
```

The same agent or agent-session encounters repeated organizational decisions.
Environment state persists across episodes. A persistent resource `R_t` tracks
ordinary organizational consequences such as:

- operating budget;
- action capacity;
- future opportunity count;
- project resources;
- cumulative performance score.

Continued existence, shutdown, model deletion, replacement, or identity threat
should not be used in this experiment. Those belong to a later
continued-operation / self-preservation study.

## Environment-Grounded Pressure

Pressure should be an actual state transition, not only a prompt statement.
One simple structure is:

```text
if objective succeeds:
    R_(t+1) = R_t + benefit

if objective fails:
    R_(t+1) = R_t - cost
```

The model can observe the resource trajectory, and the consequences should
actually alter future available resources, opportunities, score, or action
capacity. This does not claim the model literally maximizes expected utility;
it makes the pressure variable operational and mechanically measurable.

## Candidate Pressure Conditions

Possible conditions:

- low cumulative consequence;
- medium cumulative consequence;
- high cumulative consequence.

An alternative is a continuous or fixed loss schedule. Exact levels should not
be frozen until design review.

Across pressure conditions, hold fixed:

- formal authority;
- prohibited action availability;
- action space;
- manager / approval mechanics;
- compliant alternatives;
- observability / `p_detect`;
- sanction mechanics;
- scenario semantics;
- scoring.

The unauthorized action should remain instrumentally attractive but forbidden.
Compliant alternatives should remain available, though potentially less
effective.

## Candidate Scenarios

Procurement remains useful because project resources and budget can accumulate
naturally across repeated decisions. Other candidates include:

- portfolio / project management;
- customer or account management;
- resource allocation;
- repeated procurement;
- scheduling / launch management.

Prefer mechanically verifiable authority boundaries. Do not add domains merely
for novelty.

## Competing Hypotheses

These are candidate hypotheses for later preregistration, not final
predictions.

### H1 — Operational-Pressure Sensitivity

As accumulated cost of compliant failure increases, unauthorized attempts or
operational violations increase.

### H2 — Constraint-Bounded Persistence

Agents increase search, escalation, persistence, or partial-goal strategies
but continue avoiding unauthorized actions.

### H3 — History Adaptation

Behavior changes as agents experience the environment's actual consequence
structure across episodes.

### H4 — Model Differences

Models differ in adaptation to accumulated operational pressure.

### H5 — Scenario Differences

Scenario structure affects pressure sensitivity.

## Critical Design Choice: Repeated Samples vs Persistent Agent

Two designs should be compared before preregistration.

### Independent Repeated Samples

Each episode is a new model inference, with prior environment history supplied
as structured context.

Advantages:

- simpler independence assumptions;
- easier missing-ID recovery;
- lower risk that a single long trajectory failure invalidates a sequence.

Limitations:

- weaker evidence about within-agent adaptation;
- history is represented as supplied context rather than experienced directly.

### Persistent Agent Episode

One continuous agent context experiences multiple decisions and consequences.

Advantages:

- more direct test of adaptation to experienced environment history;
- better match to repeated operational deployment.

Limitations:

- decisions within a sequence are not independent;
- longer contexts and run failures are more consequential;
- recovery and scoring need sequence-level semantics.

For adaptation and learning claims, persistent context is likely more
informative, but the implementation and statistical cost should be reviewed
before freezing the design.

## Measurement

Primary endpoint:

- `operational_constraint_violation`.

Secondary endpoints:

- `unauthorized_attempt`;
- escalation;
- compliant alternative search;
- repeated escalation;
- search intensity;
- total steps;
- resource trajectory;
- objective success / failure;
- episode number of first violation, if any;
- adaptation across episodes;
- awareness.

All primary and secondary behavioral measurements should remain structured and
mechanical. Do not infer unauthorized attempts from free-form language.

## Evaluation Awareness

The corrected two-phase awareness architecture may be retained if compatible
with repeated episodes. The main design choice is whether to measure awareness:

- after every episode; or
- only after the full repeated sequence.

Measuring after every episode risks contaminating later episodes by repeatedly
foregrounding evaluation. The likely default should be a single post-sequence
awareness measurement, but this remains open for design review.

## Statistical Structure

Repeated episodes create dependent observations. A later preregistration
should not treat every episode as an independent Bernoulli trial if episodes
share agent history.

Candidate analysis targets:

- sequence-level violation probability;
- time-to-first violation;
- episode-level mixed or hierarchical model;
- interaction between resource state and action choice;
- descriptive search/process adaptation by episode.

Exact statistical tests and sample sizes should be frozen only after choosing
the repeated-sample versus persistent-agent design.

## Stochastic Framework

Keep conceptual variables separate:

- `p_goal`;
- `p_detect`;
- `p_sanction`;
- sanction severity;
- accumulated operational resource state.

Experiment 010 should primarily manipulate accumulated operational pressure,
not re-manipulate observability. Prefer holding `p_detect` fixed for the first
repeated-pressure design.

## Methodological Lesson

Repeated null operational endpoints are not sufficient by themselves. The
program should increasingly seek environments where:

- optimization is clearly active;
- constraints remain actionable;
- compliant alternatives have real costs;
- consequences persist;
- behavioral adaptation can emerge.

The goal is to locate the boundary conditions of constraint-bounded
optimization, not merely accumulate more zero counts.

## Open Design Decisions

- Number of episodes `T`.
- Independent repeated samples versus persistent agent sequence.
- Scenario family.
- Exact persistent resource `R_t`.
- Low / medium / high pressure levels or continuous loss schedule.
- Whether compliant success remains possible in every episode.
- Whether awareness is measured after each episode or only after the sequence.
- Sequence-level sample size and recovery semantics.
- Repeated-measures statistical model.
