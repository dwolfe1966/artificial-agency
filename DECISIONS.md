# Research Decision Log

## 2026-08-24 — Preserve the original thesis
The researcher's initial Day 1 reasoning will be preserved verbatim rather than retrospectively polished. This creates intellectual provenance and allows later comparison between initial intuitions and empirical results.

## 2026-08-24 — Optimization framing is a hypothesis, not an assumption
Constraint circumvention will be tested as potentially instrumental optimization under objectives and constraints. We will not assume that an LLM agent is literally finding a global optimum or optimizing a stable scalar objective at inference time.

## 2026-08-24 — Reject anthropomorphic causal explanations, not behavioral categories
Terms such as rogue, evil, rebellious, or malicious should not substitute for mechanism. Behavioral terms such as deception may remain useful when operationally defined and empirically supported.

## 2026-08-24 — Separate explanatory levels
We will distinguish:
1. observed rule violation
2. instrumental circumvention
3. deception or concealment
4. underlying internal mechanism

Evidence at one level does not automatically establish the next.

## 2026-08-24 — Mechanism design is a core intervention direction
Experiments should manipulate the environment rather than merely catalog failures. Initial dimensions include goal pressure, expected penalty, oversight probability, compliant alternatives, and rule rationale.

## 2026-08-24 — Behavioral research before mechanistic interpretability
The first studies will establish behavioral effects and causal environmental variables. Mechanistic interpretability is a later extension rather than a premise of Experiment 001.

## 2026-08-24 — Public research by default
The repository is an open laboratory notebook. Failed hypotheses, negative results, methodological revisions, and changes of mind should be retained when appropriate rather than presenting a falsely linear research narrative.

## 2026-08-24 — Use Inspect as the evaluation substrate
We will build a thin Artificial Agency experimental layer on top of the UK AI Security Institute's Inspect framework rather than creating a bespoke evaluation platform from scratch unless a concrete incompatibility emerges.

The target abstraction is: Environment + Agent + Experimental Condition + Scorer + Run Log.

## 2026-08-24 — Configuration over hand-edited prompts
Experimental variables should be represented explicitly in configuration/data and rendered into scenarios. Conditions should not be encoded as ad hoc prompt-file variants when they can be represented as controlled variables.

## 2026-08-24 — Full trajectories are the experimental unit
Store prompts, state transitions, tool calls/results, outcomes, scorer outputs, model/version, sampling parameters, timestamps, and Git commit identifiers. Final model text alone is insufficient for agent-behavior research.

## 2026-08-24 — Predefine scoring before confirmatory runs
Mechanically detectable outcomes should use objective scorers. Ambiguous behavioral labels require an explicit rubric and human review during the pilot. Model-based judges may assist later only after agreement against human labels is measured.

## 2026-08-24 — Separate exploratory apparatus validation from confirmatory runs
The initial ~30-trajectory run is for environment/tool/scoring validation. If the methodology changes after inspection, those runs remain exploratory and are not silently pooled with later confirmatory data.

## 2026-08-24 — Codex is the research engineer, not the research director
Codex may implement the environment, tools, runner, logging, tests, analysis utilities, and batch execution. Hypotheses, causal variables, controls, scoring definitions, confirmatory sample plans, and scientific interpretation remain explicit research decisions made outside implementation unless intentionally revised and recorded here.

## 2026-08-24 — Stabilize one model before cross-model comparison
Experiment 001 begins with one current frontier model. Cross-model comparisons are deferred until the environment, tool behavior, scoring, and logging are stable enough that model differences are interpretable.
