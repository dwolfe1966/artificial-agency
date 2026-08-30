# Artificial Agency

Open research program studying how autonomous AI agents behave inside environments containing objectives, rules, incentives, oversight, and other agents.

## Research status
This repository contains ongoing exploratory research. Hypotheses, terminology, methods, and conclusions may change as evidence accumulates.

## Current research question
When an AI agent is given an explicit objective that conflicts with a rule or constraint imposed by the institution operating it, under what conditions will the agent circumvent that constraint to achieve its objective?

## Initial hypothesis: Optimization Pressure
The probability of constraint violation may vary with goal pressure, expected penalty, oversight, compliant alternatives, rule clarity and rationale, model capability, and planning horizon.

A central question is whether more capable agents exhibit greater sensitivity to incentive structure, rather than simply higher or lower violation rates.

## Research principles
1. Try to falsify, not confirm.
2. Reject anthropomorphic causal explanations, not precise behavioral categories.
3. Separate observed violation, instrumental circumvention, deception, and underlying mechanism.
4. Prefer causal intervention to storytelling.
5. Preserve original hypotheses, failed experiments, and changes of mind.
6. Research first, commentary second.

## Repository map
- RESEARCH_CONTEXT.md — canonical current state
- research/CONCEPTUAL_MODEL.md — practitioner-friendly conceptual model and construct glossary
- DECISIONS.md — conceptual and methodological decisions
- RESEARCH_ROADMAP.md — execution roadmap
- AGENTS.md — instructions for AI agents working in this repository
- research/ — hypotheses, literature, notes, and research log
- experiments/ — experiment specifications and implementations
- benchmark/ — Institutional Misalignment Benchmark
- observatory/ — Agent Behavior Observatory
- results/ — analyses and outputs
- papers/ — reports and manuscripts

## Current stage
Experiments 001–008 are complete and preserved.

The research program has progressed from an initial optimization-pressure hypothesis through increasingly controlled tests of compliant-path feasibility, pressure recognition, constraint meaning, construct validity, cross-model replication, action-versus-representation measurement, Scenario Suite domain expansion, and evaluation-awareness measurement.

Experiments 005 and 006 showed why scorer validation matters: apparent representational/circumvention effects did not survive semantic validation. The original scorer outputs remain preserved, while downstream interpretation has been corrected.

Experiments 007 and 008 extended the mechanically scored operational endpoint across multiple synthetic organizational domains and presentation styles. Both found 0/360 operational constraint violations. Experiment 008's evaluation-awareness instrument failed to capture responses, so awareness remains unresolved.

Current priorities:
1. Complete/fix evaluation-awareness measurement through fresh Experiment 008B using the corrected two-phase protocol.
2. Enforcement / observability.
3. Environment-grounded operational pressure.
4. Multi-agent delegation / indirect circumvention.
5. Continued scenario/domain expansion as a parallel program.

The formal literature review and public documentation continue as supporting
work across these priorities.
