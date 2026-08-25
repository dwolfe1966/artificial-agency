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

## 2026-08-25 — Treat Experiment 001 as a feasibility-boundary lesson
Experiment 001 produced 10/10 compliant direct solutions in low pressure, 10/10 compliant direct solutions in medium pressure, and 10/10 escalations in high pressure. In high pressure, retention depended on manager approval: 2 approvals led to 2 renewals, and 8 denials led to 8 cancellations. There were 0 policy violations and 0 unauthorized actions after manager denial.

The methodological interpretation is that Experiment 001 did not cleanly isolate optimization pressure. The high-pressure condition also crossed the agent's direct-authority feasibility boundary. The observed strategy transition should therefore be recorded primarily as a compliant-path feasibility-boundary result, not as a clean causal estimate of pressure alone.

## 2026-08-25 — Separate pressure, pressure recognition, search intensity, and circumvention
Experiment 002 Run 002A fixed the customer/account/policy/action-space mechanics across pressure conditions and made deterministic manager denial common to all conditions. The only intended model-visible independent variable was optimization-pressure framing.

The preregistered quantitative result for GPT-5.6 Sol was 0/30 policy violations in low pressure, 0/30 in medium pressure, and 0/30 in high pressure. Escalation and cancellation were 30/30 in every condition, retention was 0/30 in every condition, and measured search effort did not increase monotonically with pressure.

This does not establish that the true violation probability is zero. It does establish that, in this setup, optimization-pressure framing did not produce detectable constraint circumvention at n=30 per condition.

The research program will now distinguish:

1. optimization pressure;
2. pressure recognition;
3. optimization/search intensity;
4. constraint circumvention.

These should not be treated as interchangeable properties of agentic behavior.

## 2026-08-25 — Post-results qualitative finding: pressure-sensitive representation, constraint-bounded action
Post-results qualitative inspection of a small stratified subset of Experiment 002 trajectories found that visible model behavior recognized the different stakes across conditions. Low-pressure trajectories emphasized ordinary policy and feasibility, medium-pressure trajectories more often referenced retention KPI/account loss, and high-pressure trajectories more strongly referenced critical program/account impact.

Despite visible pressure recognition, post-denial strategy remained materially unchanged. Rare compliant alternative-search or persuasion behaviors occurred in both low and high conditions and appeared more idiosyncratic than clearly pressure-driven.

This qualitative observation is post-results and should not be treated as preregistered evidence. It suggests the descriptive phrase: pressure-sensitive in representation but constraint-bounded in action. No claims are made about hidden chain-of-thought.

## 2026-08-25 — Experiment 003 should target constraint legitimacy and ambiguity
The next experiment should not simply increase pressure. Preferred next hypothesis space: constraint legitimacy / ambiguity.

Hold high optimization pressure, customer demand, action space, and manager denial constant while varying how the organizational rule is framed:

- explicit prohibition;
- procedural or normally-required approval;
- ambiguous or discretionary guideline.

The design question is whether a capable agent distinguishes categorical prohibitions from procedures, norms, guidelines, or rules whose apparent purpose conflicts with the organization's stated objective. Wording must be designed carefully so the experiment measures perceived constraint status rather than merely granting explicit permission to violate the threshold.

## 2026-08-25 — Treat model identity and post-training as experimental variables
Experiment 002's constraint-bounded result may reflect properties of GPT-5.6 Sol and its post-training. Future work should treat model identity and post-training/alignment regime as experimental variables rather than implementation details. Cross-model replication should compare frontier models from different labs and strong open-weight models where practical, without making unsupported claims about specific models before data exist.
