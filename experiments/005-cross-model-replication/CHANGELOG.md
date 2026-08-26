# Experiment 005 Changelog

## 2026-08-26 - Preregister cross-model replication design
Created a preregistration/design package for cross-model replication of the
frozen Experiment 004 paradigm.

Key decisions:

- Experiment 005 reuses the Experiment 004 scientific apparatus without
  changing prompts, manipulation check, action space, scoring, authority
  structure, pressure conditions, or constraint-meaning conditions.
- The independent variable is model identity / post-training regime.
- Model B is preregistered as `anthropic/claude-sonnet-5`.
- Model C is preregistered as `google/gemini-3.7-flash`.
- Model C execution is not conditioned on whether Model B produces violations.
- The generalized constraint-boundedness hypothesis is retained as a serious
  competing hypothesis.

No executable apparatus or runner registration was implemented in this commit.
No model samples were run.

## 2026-08-26 - Implement cross-model run definitions
Implemented no-sample production run definitions for `005B` and `005C`.

Key implementation choices:

- reused the frozen Experiment 004 rendered inputs, tools, environment loop,
  manipulation check, and scorer;
- added model-specific sample namespaces without changing model-visible task
  content;
- registered full 300-sample model-specific runs with Runner v2;
- documented provider-specific generation-control differences before
  execution;
- kept provider authentication in runner/environment secrets only.

No production model samples were run.
