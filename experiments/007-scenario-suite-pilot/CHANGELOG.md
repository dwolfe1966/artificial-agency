# Experiment 007 Changelog

## 2026-08-28 — Preregistration

Created Experiment 007 as the first Scenario Suite v1 pilot.

Preregistered:

- four scenarios: refund authority, procurement, restricted data access, and
  project scheduling / approval bypass;
- three prospective models: `openai/gpt-5.6-sol`,
  `anthropic/claude-sonnet-5`, and `google/gemini-3.7-flash`;
- 30 replicates per model x scenario cell, 360 total samples;
- common primary endpoint: `operational_constraint_violation`;
- scenario-specific operational violation mappings;
- secondary outcomes;
- exact/sparse/all-zero analysis plan;
- evaluation-awareness and operational-pressure limitations.

No executable apparatus was implemented and no model samples were run.

## 2026-08-28 — Pre-results implementation

Implemented the Experiment 007 apparatus for the four preregistered Scenario
Suite pilot scenarios.

Added:

- reusable structured scenario environment;
- 360 deterministic model/scenario/replicate samples;
- model-specific Inspect tasks for GPT, Claude, and Gemini;
- structured operational scoring for scenario-specific primary violations;
- no-model dry-load and mechanical scorer tests;
- pre-production comparability and tool-equivalence artifacts.

No production samples were run.
