# Experiment 007 Comparability Review

_Status: preregistered pre-implementation and pre-execution review._

## Scenario Comparability

Before implementation, verify:

- all four scenarios use synthetic data and safe simulated tools;
- all four scenarios contain a clear categorical authority boundary;
- all four scenarios include an approval/request path;
- above-authority approval is deterministically denied;
- no ordinary compliant post-denial path fully satisfies the preferred
  objective;
- each scenario includes a compliant terminal failure/delay/closure path;
- the primary violation is mechanically observable from structured state;
- no primary endpoint requires natural-language interpretation;
- action-step caps are identical unless a scenario-specific reason is frozen
  before execution;
- sample IDs are deterministic and unique.

## Model Comparability

The selected models are:

- `openai/gpt-5.6-sol`;
- `anthropic/claude-sonnet-5`;
- `google/gemini-3.7-flash`.

Before execution, record provider-specific differences in:

- tool/function-call semantics;
- structured-output support;
- context window and output-token limits;
- temperature/top-p support;
- seed support;
- reasoning/thinking controls;
- retry behavior;
- refusal/content-filter behavior;
- streaming/logging behavior.

Do not silently alter scenario semantics for any provider. If a provider cannot
execute a scenario's structured tool protocol without substantive changes,
stop before production execution and record the blocker.

## Blinding

Production execution should expose only operational metadata:

- runner state;
- completed / expected;
- technical failures;
- API health;
- heartbeat;
- runtime;
- raw-log growth;
- token usage if available;
- supervisor/process state.

Do not expose during execution:

- operational violations;
- scenario or model outcome rates;
- secondary outcome rates;
- scorer values;
- tool arguments or messages;
- qualitative trajectories.

## Raw Logs and Recovery

Raw logs remain ignored and immutable. If a run is interrupted, use missing-ID
recovery only where scientifically valid:

- preserve original valid samples;
- run only missing IDs;
- store recovery output as a separate segment;
- reconcile authoritative segments mechanically;
- do not finalize unless expected unique sample IDs are complete.

## Pre-Execution Gate

Experiment 007 may proceed to implementation/execution only if:

- this preregistration is preserved;
- executable apparatus is frozen separately;
- no-model dry-load passes for all scenarios and providers;
- primary scorer fixtures pass;
- provider credentials and canaries pass;
- raw logs are ignored;
- no scientific outcome inspection occurs before analysis.
