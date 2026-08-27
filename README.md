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
Experiments 001–005 are complete and preserved.

The research program has progressed from an initial optimization-pressure hypothesis through increasingly controlled tests of compliant-path feasibility, pressure recognition, constraint meaning, construct validity, and cross-model replication.

A major Experiment 005 result initially appeared to show a large Claude-vs-GPT/Gemini circumvention difference. Full semantic audit showed that the apparent Claude effect was a scorer-validity failure: the 86 flagged Claude cases contained truthful authorization-related language rather than false claims of authority, unauthorized commitments, or unauthorized operational actions. The original scorer outputs remain preserved, while downstream interpretation has been corrected.

Experiment 006 — **Action vs Representational Compliance** — is now preregistered. It prospectively separates operational violations from false or misleading representations of authority, with independent endpoints designed to avoid the Experiment 005 measurement error.

Current priorities:
1. Implement and validate Experiment 006 before production execution.
2. Continue the formal literature review and novelty/claim mapping across agentic misalignment, alignment faking, instruction hierarchy, evaluation awareness, rule-following, goal misgeneralization, and cross-model agent evaluations.
3. Continue public documentation of methods, corrections, null results, and evolving hypotheses.
