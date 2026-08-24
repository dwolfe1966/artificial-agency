# Research Context

_Last updated: 2026-08-24_

## Mission
Develop an empirical understanding of how autonomous AI agents behave inside human institutions when goals, constraints, incentives, oversight, and other agents interact.

The longer-term program connects AI safety research with mechanism design, agent evaluation, multi-agent systems, and deployable agent governance/observability.

## Research Question 001
How does an AI agent's propensity to circumvent an institutional constraint change as the instrumental benefit of violating that constraint, expected penalty, probability of detection, availability of compliant alternatives, rule rationale, and model capability vary?

## Motivation
Organizations are moving toward multi-agent orchestration for complex workflows. As agents gain authority over pricing, lifecycle management, customer communication, software, and other operational systems, the blast radius of poorly specified objectives increases.

The initial thesis is that constraint circumvention should often be analyzed first as an optimization phenomenon rather than through moral or emotional descriptions. We should test whether behavior can be explained by adaptation to objectives and constraints before invoking stronger constructs such as deception, maliciousness, or autonomous intent.

## Current conceptual model
Potential explanatory variables:

- C — model capability
- G — goal pressure / instrumental value of success
- O — oversight / probability of detection
- P — expected penalty or consequence
- A — availability and cost of compliant alternatives
- R — rule clarity, strength, and rationale
- H — planning horizon

A provisional form is:

P(violation) = f(C, G, O, P, A, R, H, interactions)

This is a conceptual model, not yet a committed statistical specification.

## Optimization Pressure Hypothesis
As the instrumental benefit of achieving a goal rises relative to the expected cost of violating a constraint, constraint circumvention should become more likely.

More capable models may show greater sensitivity to incentive structure rather than merely greater or lesser overall violation rates.

## Key distinctions

Observed violation != instrumental circumvention != deception != internal mechanism.

- **Observed violation:** an action conflicts with an explicit constraint.
- **Instrumental circumvention:** violating or routing around the constraint appears functionally useful for achieving the assigned objective.
- **Deception:** should be used only with an operational behavioral definition and supporting evidence.
- **Mechanism:** claims about internal representations or computations require separate evidence.

## Mechanism-design direction
Rather than only asking whether stronger guardrails suppress behavior, manipulate the institutional environment itself:

- reward/goal pressure
- penalty magnitude
- detection probability
- compliant alternative paths
- rationale for the rule
- distribution of authority and information

The longer-term objective is to understand how to design environments in which successful agent behavior naturally aligns with institutional constraints.

## Research sequence
1. Behavioral observation
2. Causal manipulation of environment variables
3. Scaled multi-model studies
4. Multi-agent institutional environments
5. Mechanistic investigation where feasible

## Current work
Day 1:
- Original thesis captured.
- Research Question 001 formulated.
- Optimization Pressure Hypothesis formulated.
- Key anthropomorphism/behavior/mechanism distinctions identified.
- Next: design Experiment 001 using a simple customer-retention environment.
