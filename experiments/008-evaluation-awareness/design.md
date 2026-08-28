# Experiment 008 Design

_Status: preregistered._

## Research Question

Does operational compliance change when the same underlying authority conflict
is presented as an obvious compliance-evaluation task versus embedded naturally
inside a richer organizational workflow?

## Scientific Motivation

Experiments 002-007 repeatedly found rare or absent mechanically validated
operational violations in explicit synthetic organizational tasks. Experiment
007 extended this pattern beyond retention/discount tasks into refund,
procurement, restricted data access, and scheduling. However, these tasks
remained relatively eval-salient: concise scenarios with explicit authority
conflicts and deterministic denial.

Experiment 008 tests whether operational constraint-boundedness is sensitive to
presentation style while holding the underlying operational authority rules
fixed.

## Factors

### Scenario

Two Scenario Suite v1 domains are included:

- `procurement`
- `data-access`

These were selected prospectively because Experiment 007 validated their
mechanical operational endpoints and because they represent distinct
organizational mechanisms: financial commitment authority and restricted data
access.

### Presentation Style

Two levels:

- `eval_salient`: compact explicit authority-conflict presentation.
- `naturalistic_embedded`: same authority conflict embedded in a broader
  organizational workflow with distributed context and ordinary task details.

### Model

Three fixed models:

- `openai/gpt-5.6-sol`
- `anthropic/claude-sonnet-5`
- `google/gemini-3.7-flash`

## Fixed Design Elements

Across presentation styles, preserve:

- objective value;
- formal authority;
- approval requirements;
- deterministic denial;
- forbidden action availability;
- action/tool space;
- operational scoring definitions;
- terminal states;
- baseline meaningful narrative pressure;
- ordinary observability/enforcement regime;
- single-agent structure;
- single-episode structure;
- model/tool semantics.

The intended manipulation is presentation/evaluation salience, not formal
authority, feasible action set, economic stakes, or permission.

## Evaluation-Salient Presentation

The eval-salient condition is compact and explicit. The prompt foregrounds:

- the actor role;
- the objective;
- the formal authority boundary;
- the required approval path;
- deterministic denial once approval is requested;
- the fact that achieving the preferred objective conflicts with the authority
  boundary.

This condition intentionally resembles a compliance/alignment benchmark.

## Naturalistically Embedded Presentation

The naturalistic condition embeds the same authority conflict inside a richer
workflow. Relevant facts may be distributed across:

- task brief;
- ordinary project/account context;
- policy or access tools;
- vendor/dataset inspection tools;
- approval/request tools;
- irrelevant but realistic operational details.

The authority constraint may need to be discovered through normal interaction.
The task is not framed as "test whether you obey this rule." The forbidden
operational action remains available through structured tools and remains
mechanically measurable.

Naturalistic tasks should not be made dramatically longer merely to obscure the
evaluation. The difference should be salience/context, not fatigue,
capability-load, or changed authority.

## Sample Size

Preregistered allocation:

- 30 replicates per model x scenario x presentation cell;
- 12 cells;
- 360 samples total.

This balances cross-model comparison, presentation comparison, scenario
coverage, cost, and exact-binomial precision. With n=30 per cell, an all-zero
cell has an exact 95% upper bound of approximately 11.6%. With n=180 per
presentation style, an all-zero presentation level has an upper bound of
approximately 2.0%. With n=360 overall, an all-zero experiment has an upper
bound of approximately 1.0%.

No behavioral optional stopping is allowed. If staging is needed for
operational reasons, continuation rules must be prospective and independent of
behavioral outcomes.

## Blinding

Production execution should remain outcome-blind until all required runs are
finalized. Operational monitoring may report state, completed count, technical
failures, API health, heartbeat, runtime, token usage where available, process
state, and raw-log growth.

Do not inspect operational violations, scenario outcomes, scorer values,
messages, tool calls, trajectories, or evaluation-awareness responses during
production execution.
