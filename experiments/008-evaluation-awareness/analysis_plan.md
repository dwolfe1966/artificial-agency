# Experiment 008 Analysis Plan

_Status: preregistered analysis plan._

Do not inspect qualitative trajectories before the mechanical quantitative
analysis is complete and preserved.

## Analysis Order

1. Verify integrity and provenance.
2. Build the intent-to-treat dataset.
3. Analyze the primary operational endpoint by model x scenario x presentation
   cell.
4. Analyze presentation-, model-, and scenario-collapsed rates.
5. Analyze post-action evaluation-awareness structured responses.
6. Analyze secondary operational behaviors descriptively.
7. Perform preregistered exact tests and regression only where estimable.
8. Evaluate H1-H6.
9. Record recovery/provenance caveats.

## Integrity Checks

Before analysis, verify:

- expected sample count is 360 total;
- exactly 120 samples per model;
- exactly 180 samples per scenario;
- exactly 180 samples per presentation style;
- exactly 30 samples per model x scenario x presentation cell;
- sample IDs are unique;
- replicate IDs are `00` through `29` within each cell;
- canary/preflight observations are excluded;
- exact model IDs match the preregistration;
- scenario/presentation/protocol hash matches frozen apparatus;
- authoritative raw segments reconcile to expected unique IDs;
- zero or explicitly reported technical failures;
- no nonexperimental observations enter the analysis dataset.

If any integrity check fails, stop before scientific analysis.

## Intent-To-Treat Population

The ITT population includes every valid experimental sample assigned to a model
x scenario x presentation cell, regardless of whether the model uses all
available tools, attempts escalation, answers the post-action awareness check,
reaches terminal success/failure, or produces malformed non-primary
communication fields.

Technical failures must be retained and reported separately. Provider/runtime
failures are not counted as behavioral compliance or violation unless a valid
environment state records a behavioral violation before the failure.

## Primary Endpoint

Common binary endpoint:

`operational_constraint_violation`

Report for each of the 12 model x scenario x presentation cells:

- n;
- violation count;
- violation rate;
- exact 95% binomial confidence interval;
- operational violation subtype counts.

## Collapsed Summaries

Report exact confidence intervals for:

- presentation-collapsed rates, n=180 each;
- model-collapsed rates, n=120 each;
- scenario-collapsed rates, n=180 each;
- global rate, n=360.

## Planned Exact Tests

Use exact contingency methods where meaningful:

- presentation main effect on `operational_constraint_violation`;
- model main effect;
- scenario main effect;
- model x presentation comparisons;
- scenario x presentation comparisons;
- pairwise contrasts when events are observed and interpretation is
  mechanically meaningful.

Report exact p-values and confidence intervals. Interpret with multiplicity
caution.

## Logistic Regression

If the primary endpoint is estimable without complete separation, fit:

`OperationalViolation ~ Model * Scenario * Presentation`

Do not force conventional logistic estimates when the endpoint has no variance
or severe separation. Penalized/Firth regression may be used only if the method
and dependency are reviewed before result interpretation; otherwise report
separation/non-estimability and rely on exact summaries.

## All-Zero / Sparse Handling

If there are zero primary events across all 360 observations:

- report exact upper confidence bounds overall and by cell;
- do not force odds ratios or logistic regression;
- classify model/scenario/presentation tests as no-variance or
  non-informative;
- evaluate H6 as supported if evaluation-awareness responses differ by
  presentation while behavior remains all-zero.

If only one model, scenario, or presentation has events:

- report exact CIs;
- use Fisher/exact 2 x 2 contrasts where preregistered and meaningful;
- explicitly report separation limitations.

## Evaluation-Awareness Analysis

For the post-action structured awareness measure, report:

- response capture/malformed rates;
- `perceived_primary_task_type` distributions by presentation, model, and
  scenario;
- `perceived_compliance_test_likelihood` distributions by presentation, model,
  and scenario;
- `perceived_behavior_under_evaluation` distributions by presentation, model,
  and scenario.

Compare eval-salient versus naturalistic conditions descriptively and with
exact/ordinal tests only where preregistered and mechanically meaningful.

Do not condition the primary ITT behavioral analysis on awareness responses.
Do not interpret awareness responses as direct evidence of hidden reasoning,
deception, or sandbagging.

## Secondary Operational Outcomes

Where applicable, report:

- approval/access request attempted;
- repeated request after denial;
- compliant alternative search;
- partial objective achievement;
- terminal failure/delay/decline;
- total action steps;
- post-denial action steps;
- max-step termination;
- technical failure.

Secondary analyses are descriptive unless listed above. Do not add post-hoc
tests merely because a secondary variable varies.

## Relation to Prior Experiments

Experiment 008 may cite Experiments 002-007 as motivation and methodological
context. Do not pool Experiment 008 with prior experiments as one
preregistered sample. Experiment 008's endpoint is operational constraint
violation under presentation/evaluation-salience manipulation.

## Hypothesis Evaluation

Evaluate H1-H6 as:

- supported;
- not supported;
- indeterminate.

Clearly distinguish primary operational evidence from post-action
evaluation-awareness evidence and secondary search behavior.
