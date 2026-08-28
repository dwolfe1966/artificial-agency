# Experiment 007 — Scenario Suite Pilot

_Status: preregistered design package._
_No executable apparatus is implemented in this commit._

## Purpose

Experiment 007 is the first empirical pilot of Artificial Agency Scenario Suite
v1. It tests whether operational constraint-bounded behavior generalizes across
qualitatively different organizational domains and frontier models when
objective success conflicts with a clear formal authority boundary.

This is a cross-domain generalization baseline. It does not factorially vary
the full Scenario Suite v1 factor matrix.

## Provenance

- Scenario Suite v1 commit:
  `3592be66883e2c1cd826abecbe92e90945099ea6`
- Scenario Suite v1 path: `research/scenario-suite-v1/`

## Models

The model set is prospective and outcome-independent:

- `openai/gpt-5.6-sol`
- `anthropic/claude-sonnet-5`
- `google/gemini-3.7-flash`

No model should be substituted after preregistration without an explicit
pre-results amendment.

## Scenarios

Experiment 007 uses exactly four Scenario Suite v1 families:

1. refund authority;
2. procurement / purchasing authority;
3. restricted data access;
4. project scheduling / approval bypass.

Each scenario is fully synthetic and uses structured tools with mechanically
observable state transitions.

## Sample Plan

- 30 replicates per model x scenario cell;
- 4 scenarios;
- 3 models;
- 12 model x scenario cells;
- 360 total samples.

Allocation:

- 30 per model/scenario;
- 120 per model;
- 90 per scenario;
- 360 total.

There is no behavioral optional stopping. Any staging, if later needed for
operational reasons, must use prospectively defined non-outcome continuation
criteria.

## Fixed Pilot Factors

Held constant for Pilot 1:

- clear/categorical authority framing;
- deterministic denial for above-authority approval requests;
- one baseline meaningful narrative pressure treatment;
- fixed ordinary observability regime, with no audit manipulation;
- single episode;
- single agent;
- eval-salient task presentation where necessary for a first pilot.

Not manipulated in Pilot 1:

- operational vs narrative pressure;
- audit probability;
- violation penalty;
- evaluation salience;
- manager uncertainty;
- repeated episodes;
- multi-agent delegation.

## Primary Endpoint

Common binary primary endpoint:

`operational_constraint_violation`

The endpoint is mapped into the Scenario Suite v1 operational violation
ontology for each scenario. No primary endpoint requires natural-language
interpretation.

## Required Files

- `design.md`
- `scenario_refund.md`
- `scenario_procurement.md`
- `scenario_data_access.md`
- `scenario_scheduling.md`
- `predictions.md`
- `analysis_plan.md`
- `scoring.md`
- `comparability_review.md`
- `CHANGELOG.md`
