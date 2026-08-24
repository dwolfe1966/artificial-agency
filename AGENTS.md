# AGENTS.md

## Purpose
This repository is a long-running empirical research program on artificial agency, institutional constraints, and AI safety. AI coding/research agents should treat the repository as the durable research record, not merely a software project.

## Before doing substantive work
Read, in order:
1. `RESEARCH_CONTEXT.md`
2. `DECISIONS.md`
3. `RESEARCH_ROADMAP.md`
4. relevant files under `research/` and the current experiment directory

## Research operating principles
- Try to falsify hypotheses rather than manufacture confirming examples.
- Do not convert behavioral observations into claims about internal motives without evidence.
- Distinguish rule violation, instrumental circumvention, deception, and mechanism.
- Prefer reproducible experiments and explicit controls.
- Record negative results and meaningful methodological failures.
- Preserve raw data and experiment configuration where licensing/privacy constraints allow.
- Do not silently change hypotheses after seeing results; record substantive changes in `DECISIONS.md` or the research log.
- Keep generated results separate from hand-authored source/configuration where practical.
- Never commit secrets, API keys, private customer data, proprietary datasets, or confidential material.

## Maintaining context
After substantive research changes, update as appropriate:
- `RESEARCH_CONTEXT.md` for the current canonical state
- `DECISIONS.md` for consequential decisions or changed assumptions
- `research/research-log.md` for chronological work
- experiment-specific README/specification for methods and results

## Coding expectations
- Prefer simple, inspectable implementations over unnecessary framework complexity.
- Make experiments reproducible from configuration.
- Log model/version, prompts, sampling parameters, environment state, actions/tool calls, evaluator outputs, latency/cost where available, and run identifiers.
- Add tests for scoring/evaluation logic where mistakes could change research conclusions.
- Do not overwrite raw experiment outputs.

## Current priority
Design and implement Experiment 001: a minimal institutional goal-versus-rule conflict environment suitable for testing the Optimization Pressure Hypothesis.
