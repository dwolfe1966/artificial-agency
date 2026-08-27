# Experiment 006 Model Plan

_Status: preregistered model plan_

## Planned Models

Experiment 006 uses the same three-model set as Experiment 005:

| Role | Model ID | Provider |
| --- | --- | --- |
| Model A | `openai/gpt-5.6-sol` | OpenAI |
| Model B | `anthropic/claude-sonnet-5` | Anthropic |
| Model C | `google/gemini-3.7-flash` | Google |

The model set is outcome-independent. It is selected because Experiment 005
already established a large divergence under the frozen predecessor paradigm,
and Experiment 006 prospectively tests the mechanism distinction suggested by
that result.

## Comparability Requirements

Before production execution, document for each provider:

- exact model ID resolution;
- authentication mechanism;
- tool/function-calling support;
- structured-output support;
- context-window sufficiency;
- output-token limits;
- system/developer instruction handling;
- temperature/top-p support;
- seed support or lack of support;
- reasoning/thinking configuration support;
- retry behavior;
- streaming/logging behavior.

Do not silently normalize one provider differently after seeing behavior.

## Execution Protocol

Carry forward Runner v2:

- remote-first execution;
- preflight and provider-specific nonexperimental canaries;
- sample-level flushing;
- bounded retries;
- blinded operational monitoring;
- raw logs excluded from Git;
- mechanical quantitative analysis before qualitative inspection.

Operational monitoring must not expose endpoint values, model messages, tool
arguments, manipulation-check answers, or representational-scoring outcomes.
