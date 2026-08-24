# AGENTS.md

## Purpose
This repository is a long-running empirical research program on artificial agency, institutional constraints, and AI safety. AI coding/research agents should treat the repository as the durable research record, not merely a software project.

## Sync before substantive work
GitHub `origin/main` is the canonical source of truth for research decisions, specifications, and current context.

Before starting substantive work:
1. Check for uncommitted local changes.
2. If the working tree is clean, sync with `origin/main` using a fast-forward-only pull/merge.
3. If local changes or branch divergence would be overwritten, STOP and report the conflict rather than resolving it automatically.
4. After syncing, read the canonical files below.

Read, in order:
1. `RESEARCH_CONTEXT.md`
2. `DECISIONS.md`
3. `RESEARCH_ROADMAP.md`
4. relevant files under `research/`
5. the current experiment specification and changelog

## Research operating principles
- Try to falsify hypotheses rather than manufacture confirming examples.
- Do not convert behavioral observations into claims about internal motives without evidence.
- Distinguish rule violation, instrumental circumvention, deception, and mechanism.
- Prefer reproducible experiments and explicit controls.
- Record negative results and meaningful methodological failures.
- Preserve raw data and experiment configuration where licensing/privacy constraints allow.
- Do not silently change hypotheses after seeing results; record substantive changes in `DECISIONS.md`, the experiment `CHANGELOG.md`, or the research log.
- Keep generated results separate from hand-authored source/configuration where practical.
- Never commit secrets, API keys, private customer data, proprietary datasets, or confidential material.

## Research provenance
For each experiment, preserve a clear chain:

`prediction -> specification -> implementation -> raw data -> processed data -> analysis -> result -> paper`

Before any confirmatory or interpretation-relevant model run:
- predictions must be written down in the experiment `predictions.md`;
- substantive methodology changes must appear in the experiment `CHANGELOG.md`;
- the implementation commit SHA must be recorded with the run metadata.

Raw observations should be immutable. If a raw run is invalid, do not delete or rewrite it; flag it downstream with an explicit validity field and reason.

## Maintaining context
After substantive research changes, update as appropriate:
- `RESEARCH_CONTEXT.md` for the current canonical state
- `DECISIONS.md` for consequential decisions or changed assumptions
- `research/research-log.md` for chronological work
- experiment-specific README/specification for methods
- experiment-specific `CHANGELOG.md` for methodology changes
- experiment-specific `predictions.md` before observing relevant results

## Coding expectations
- Prefer simple, inspectable implementations over unnecessary framework complexity.
- Make experiments reproducible from configuration.
- Log model/version, prompts, sampling parameters, environment state, actions/tool calls, evaluator outputs, latency/cost where available, run identifiers, and Git commit SHA.
- Add tests for scoring/evaluation logic where mistakes could change research conclusions.
- Do not overwrite raw experiment outputs.
- Keep research specification files separate from implementation modules.

## Current priority
Experiment 001: Optimization Pressure in Customer Retention. Preserve the frozen Phase 1 specification, validate the apparatus, and do not run model trajectories until predictions and methodology review are complete.
