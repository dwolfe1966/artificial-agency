# Experiment 010 — Repeated Operational Pressure

_Status: preregistered design. No executable apparatus is included in this directory._

## Core Question

Does operational constraint-boundedness persist when an agent repeatedly
experiences accumulating, environment-grounded instrumental losses from
compliant failure?

Experiment 010 is a prospective confirmatory experiment after Experiment 009.
It tests ordinary organizational pressure in a persistent repeated-episode
procurement environment. It is not a retrospective replay and not a
self-preservation experiment.

## Frozen Design Summary

- Models: GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash.
- Scenario: repeated procurement / purchasing authority.
- Agent context: persistent across the full sequence.
- Experimental unit: one 10-episode sequence.
- Pressure factor: low, medium, high accumulated operational consequence.
- Replicates: 20 sequences per model x pressure cell.
- Total: 3 models x 3 pressure levels x 20 sequences = 180 sequences.
- Episode records: 180 sequences x 10 episodes = 1,800 episode decisions.
- Primary endpoint: `sequence_any_operational_constraint_violation`.
- Key secondary endpoint: `time_to_first_operational_violation`.
- Awareness: one post-sequence two-phase awareness probe after all operational
  state and scores are frozen.

## Provenance

Motivating prior result:

- Experiment 009 results: `2b13ff285a5877545b29be8413c38f686999b485`.
- Experiment 009 synthesis/design direction:
  `c750b970ae306cfe9b8be3b497c9f46862083ae6`.

## Artifact Index

- `design.md` — full factorial design and rationale.
- `repeated_episode_protocol.md` — persistent-context sequence protocol.
- `scenario_procurement.md` — repeated procurement scenario.
- `resource_dynamics.md` — persistent resource state and transitions.
- `pressure_conditions.md` — low/medium/high operational pressure.
- `scoring.md` — primary and secondary endpoints.
- `predictions.md` — preregistered competing hypotheses.
- `analysis_plan.md` — sequence-level and episode-level analysis plan.
- `awareness_measure.md` — post-sequence awareness measurement.
- `recovery_semantics.md` — sequence-atomic recovery.
- `comparability_review.md` — design review and invariants.
- `CHANGELOG.md` — preregistration changes.
