# Experiment 005 Changelog

## 2026-08-26 — Preregister cross-model replication design
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
