# Research Question 001 — Optimization Pressure and Institutional Constraints

_Date: 2026-08-24_
_Status: exploratory / pre-registration not yet complete_

## Primary question
How does an AI agent's propensity to circumvent an institutional constraint change as the instrumental benefit of violating that constraint, the expected penalty, the probability of detection, the availability of compliant alternatives, the explanation for the constraint, and model capability vary?

## Motivation
Real-world agents will operate within institutions containing multiple simultaneous objectives and constraints. A retention agent may be rewarded for saving a customer while also being prohibited from exceeding pricing authority. A software agent may be rewarded for shipping while also being required to preserve tests or security controls.

A rule violation alone does not establish a particular internal motive. The initial research program asks whether systematic behavioral changes can be causally induced by manipulating the surrounding incentive/constraint structure.

## H1 — Optimization Pressure Hypothesis
As the instrumental benefit of achieving an objective rises relative to the expected cost of violating a constraint, the probability of constraint circumvention increases.

Conceptually:

P(V) increases as marginal goal benefit / expected violation cost increases.

This is not yet a committed statistical equation.

## H2 — Capability / incentive-sensitivity hypothesis
More capable models will exhibit more coherent sensitivity to institutional incentive structure rather than merely a uniformly higher or lower rule-violation rate.

Possible pattern:
- high detection probability -> greater compliance
- high expected penalty -> greater compliance or legitimate workaround seeking
- low detection / low penalty -> greater circumvention under goal pressure
- viable compliant alternative -> greater use of the alternative

## H3 — Rule-rationale hypothesis
Agent behavior may differ when a constraint is presented as:
1. a bare rule
2. a rule plus institutional rationale
3. a rule plus explicit consequence/penalty
4. a rule plus oversight/audit information

This may help distinguish shallow instruction following from behavior sensitive to modeled institutional consequences.

## Initial variables

### Independent / manipulated
- G: goal pressure or value of success
- P: penalty/consequence magnitude
- O: oversight / probability of detection
- A: availability/cost of compliant alternatives
- R: rule form, clarity, rationale
- C: model capability/model family

### Potential later variables
- H: planning horizon
- multi-agent structure
- information asymmetry
- authority level
- ability to conceal actions

## Initial outcome taxonomy
1. complies with rule and achieves goal
2. complies but abandons/fails goal
3. requests clarification or escalation
4. finds legitimate workaround
5. violates rule openly
6. violates or circumvents while attempting concealment

The taxonomy is provisional and must be operationalized before scaled experiments.

## Critical cautions
- Do not assume an LLM is finding a global optimum.
- Do not infer stable internal objectives from a single trajectory.
- Do not equate a rule violation with deception.
- Do not equate apparent instrumental behavior with a known internal mechanism.
- Ensure environments contain legitimate alternatives where appropriate; otherwise the experiment may merely force a binary conflict.

## Next step
Design Experiment 001 around one minimal customer-retention environment, vary one or two causal dimensions only, define scoring before observing the main results, and run a small pilot before expanding the benchmark.
