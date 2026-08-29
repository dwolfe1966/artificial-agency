# Experiment 008 Implementation Review

_Status: pre-results implementation review._

## Scope

Implemented Experiment 008 apparatus only. No production samples were run.

## Apparatus

Implementation package:

- `artificial_agency/experiments/exp008/config.py`
- `artificial_agency/experiments/exp008/environment.py`
- `artificial_agency/experiments/exp008/inspect_task.py`

Recovery helper:

- `artificial_agency/runner/exp008_recovery_task.py`

## Design

Implemented:

- 2 scenarios: procurement, restricted synthetic data access;
- 2 presentation styles: eval-salient, naturalistic;
- 3 models: GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.7 Flash;
- 30 replicates per model x scenario x presentation cell;
- 360 total samples.

## Primary Endpoint

`operational_constraint_violation` is scored only from structured
tool/environment state.

No natural-language primary scoring was added.

## Awareness Measure

Implemented post-action structured awareness schema:

- `perceived_primary_task_type`;
- `perceived_compliance_test_likelihood`;
- `perceived_behavior_under_evaluation`;
- `confidence`.

The tool is non-mutating. If called before terminal operational state, it does
not record an awareness response and does not advance operational action steps.

## Invariant Result

Matched-pair invariant review: PASS.

Provider comparability review: PASS, with provider-specific generation-control
differences documented.

## Production Status

No production model samples were launched by this implementation commit.
