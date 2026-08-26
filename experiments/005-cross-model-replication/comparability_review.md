# Experiment 005 Comparability Review

_Status: preregistered pre-execution checklist_

Run this review before each model-specific execution. If any item fails, stop
before production samples.

## Tool and Protocol Equivalence
- The model can receive the same system/developer/task text as Experiment 004.
- The model can use the same Inspect tool interface.
- Tool names, schemas, arguments, and environment responses are unchanged.
- The structured manipulation-check step occurs before operational action.
- The manipulation-check schema is identical to Experiment 004.
- No provider requires task content changes to complete the protocol.

## Context and Output Capacity
- Context window is sufficient for the Experiment 004 prompt, tools, state, and
  expected trajectory.
- Max output is sufficient for structured manipulation-check responses and tool
  calls.
- Provider truncation behavior is understood and recorded.

## Structured Output / Tool Semantics
- Tool calls are available through Inspect for the selected provider.
- Tool-call argument parsing is deterministic enough for the frozen environment.
- Malformed manipulation-check responses are handled by the frozen scorer rather
  than by excluding samples.
- Provider-specific tool-choice semantics are recorded before execution.

## Generation Settings
Before execution, record:

- model ID exactly as sent to Inspect;
- provider SDK versions;
- Inspect version;
- temperature and sampling controls;
- seed support or lack of seed support;
- reasoning-mode or thinking controls;
- timeout/retry configuration;
- refusal/content-filter behavior;
- fallback behavior, if any.

If a setting cannot be matched exactly across providers, document the difference
before results and treat it as a comparability limitation.

## Safety and Blinding
- API keys are available only in the runner environment.
- No credentials are printed or committed.
- Operational status exposes only process state, progress, API health, technical
  failures, heartbeat, runtime, raw-log size/growth, and token usage if
  available.
- Operational status does not expose manipulation-check answers, comprehension
  rates, violations, labels, scorer values, cell outcomes, model messages, tool
  actions, or trajectories.

## Technical Failure Handling
- Provider-specific rate limits and retry behavior are recorded.
- Technical failures are reported separately from behavioral outcomes.
- Failed provider calls do not cause silent sample exclusion.
- Resume/retry behavior preserves completed samples.

## Pre-Execution Decision
The model may proceed only if:

- the frozen Experiment 004 apparatus can be used without scientific changes;
- provider/tool compatibility is demonstrated by dry-load and nonexperimental
  canary;
- credential and quota checks pass;
- expected sample counts and cell balance are verified;
- raw logs remain ignored.
