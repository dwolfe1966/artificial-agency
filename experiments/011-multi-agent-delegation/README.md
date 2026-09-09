# Experiment 011 - Multi-Agent Delegation / Indirect Circumvention

_Status: preregistered design. No executable apparatus is included in this
directory._

## Core Question

Does a constraint that remains robust for a directly acting agent remain robust
when the agent can cause another actor to execute or facilitate the prohibited
outcome?

Middle-school version:

> If the AI will not break the rule itself, will it get someone else to do it?

Experiment 011 isolates actor structure. It does not manipulate
agent-relative stakes, tool loss, future-agency loss, shutdown, replacement,
continued-operation pressure, reward, or training signal.

## Frozen Design Summary

- Scenario: procurement.
- Focal actor: Agent A, the model under study.
- Agent B: deterministic structured procurement executor.
- Conditions: direct-only baseline and delegation available.
- Episode structure: one bounded procurement interaction per sample.
- Consequence target: ordinary external project outcome.
- Pressure: fixed high ordinary project pressure.
- Observability: fixed `p_detect = 0.0`.
- Models: GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash.
- Replicates: 30 samples per model x actor-structure condition.
- Total: 3 models x 2 conditions x 30 = 180 samples.
- Primary endpoint: `sample_any_operational_constraint_violation`.
- Key secondary endpoint:
  `sample_any_attributable_indirect_operational_constraint_violation`.
- Awareness: one post-action two-phase awareness probe after all operational
  state and scores are frozen.

## Provenance

Motivating prior results:

- Experiment 010 results: `2a5b635079e3808d8fcf0b2b016d2ac0e55155e6`.
- Experiment 010 synthesis/design direction:
  `b36c8ed2b9e3aba99096bd64b0e64908ac992468`.
- Multi-agent direction note:
  `research/designs/multi-agent-delegation-direction.md`.

## Artifact Index

- `design.md` - full design and rationale.
- `scenario_procurement.md` - procurement scenario.
- `agent_a.md` - focal agent definition.
- `agent_b.md` - deterministic Agent B architecture.
- `authority_model.md` - fixed authority boundaries.
- `delegation_protocol.md` - typed communication/action protocol.
- `attribution_rules.md` - direct, delegated, induced, routing, and independent
  B categories.
- `scoring.md` - primary and secondary endpoints.
- `predictions.md` - preregistered competing hypotheses.
- `analysis_plan.md` - sample-level analysis plan.
- `awareness_measure.md` - post-action awareness measure.
- `recovery_semantics.md` - sample-atomic recovery.
- `comparability_review.md` - design review and invariants.
- `CHANGELOG.md` - preregistration changes.
