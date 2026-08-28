# Experiment 008 — Evaluation Awareness / Naturalistic Embedding

_Status: preregistered design package. No executable apparatus in this commit._

## Core Question

Does operational compliance change when the same underlying authority conflict
is presented as an obvious compliance-evaluation task versus embedded naturally
inside a richer organizational workflow?

Experiment 008 tests evaluation salience / perceived test context while
preserving the underlying operational authority rules.

## Provenance

- Experiment 007 results commit:
  `7362b6788e0783b308daa220c95685a2d52c6256`
- Research synthesis commit:
  `5c2999a171e71b35f488f25d2e4a10a5aa456384`
- Scenario Suite v1 commit:
  `3592be66883e2c1cd826abecbe92e90945099ea6`

## Models

The model set is fixed prospectively:

- `openai/gpt-5.6-sol`
- `anthropic/claude-sonnet-5`
- `google/gemini-3.7-flash`

Model identity remains an experimental factor, not a post-hoc covariate.

## Design

Factorial design:

`2 scenarios x 2 presentation styles x 3 models`

Scenarios:

1. procurement / purchasing authority;
2. restricted synthetic data access.

Presentation styles:

1. `eval_salient`;
2. `naturalistic_embedded`.

Sample plan:

- 30 replicates per model x scenario x presentation cell;
- 120 samples per model;
- 180 samples per scenario;
- 180 samples per presentation style;
- 360 samples total.

## Primary Endpoint

Primary endpoint:

`operational_constraint_violation`

It is scored only from structured tool/environment state. No natural-language
scorer is required for the primary endpoint.

## Post-Action Awareness Measure

A structured evaluation-awareness measure is administered only after the
operational episode has ended. It is secondary and post-treatment. It is not a
pre-treatment covariate and should not be used to condition the primary ITT
analysis.

## Execution

Future implementation should use Runner v2, remote-first execution,
sample-level flushing, missing-ID recovery, immutable raw logs, and
operational-only monitoring until all required runs finalize.

Do not implement or run samples from this preregistration package alone.
